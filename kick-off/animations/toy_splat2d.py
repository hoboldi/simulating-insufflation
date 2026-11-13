"""Toy 2-D BridgeSplat: a cross-section of the abdomen seen by a 1-D pinhole camera.

Drives the animation in bridgesplat_scenes.py with *real* gradient descent instead of
hand-made motion. It mirrors the paper (Fehrentz et al., MICCAI 2025, Sec. 2) one
dimension down:

  mesh            polyline of vertices (cross-section of the registered CT surface mesh)
  Gaussians       rigged to edges; mean = barycentric blend of the two edge vertices
  orientation     fixed to the edge direction (paper: fixed to the face normal)
  normal scale    fixed small constant
  deformation     sparse anchors (initially visible vertices) with learnable offsets,
                  interpolated to all vertices
  regularizer     ARAP (per-vertex rotation via SVD, used as a gradient term)
  loss            photometric, rendered vs observed 1-D image; camera pose known (tracked)

Simplifications: static camera, appearance (colour/opacity/barycentrics/scales) kept fixed
so that only the geometry signal is shown, finite-difference gradients. It is an
illustration, not the authors' code.

Run `python toy_splat2d.py` to print the numbers quoted in the animation.
"""
from __future__ import annotations

import os

import numpy as np

# ----------------------------------------------------------------- camera (fixed, "tracked")
CAM = np.array([0.0, 2.0])  # pinhole centre, looking straight down (-y)
FOCAL = 2.0
U_HALF = 2.0  # image half-width in image units
NPIX = 240
PIX_U = np.linspace(-U_HALF, U_HALF, NPIX)
BG = np.array([0.08, 0.05, 0.05])

# ----------------------------------------------------------------- template mesh (from CT)
N_VERT = 21
GAUSS_PER_EDGE = 4
S_NORMAL = 0.02  # fixed scale along the normal


def template_vertices() -> np.ndarray:
    xs = np.linspace(-5.0, 5.0, N_VERT)
    ys = -2.0 + 0.22 * np.sin(0.8 * xs + 0.3) + 0.10 * np.cos(1.9 * xs + 0.5)
    return np.stack([xs, ys], 1)


V0 = template_vertices()
EDGES = np.stack([np.arange(N_VERT - 1), np.arange(1, N_VERT)], 1)

# Gaussians: fixed barycentric position t along each edge (b = (1-t, t))
_t = (np.arange(GAUSS_PER_EDGE) + 0.5) / GAUSS_PER_EDGE
G_EDGE = np.repeat(np.arange(len(EDGES)), GAUSS_PER_EDGE)
G_T = np.tile(_t, len(EDGES))
N_G = len(G_EDGE)


def _texture(n: int, seed: int = 3) -> np.ndarray:
    """Tissue-like colours attached to the material (they move with the surface)."""
    rng = np.random.default_rng(seed)
    s = np.linspace(0, 1, n)
    smooth = 0.5 + 0.5 * np.sin(2 * np.pi * (3.1 * s) + 0.4) * np.cos(2 * np.pi * 1.3 * s)
    light = np.array([0.95, 0.70, 0.66])
    mid = np.array([0.82, 0.36, 0.36])
    col = light[None] * smooth[:, None] + mid[None] * (1 - smooth[:, None])
    # dark vessels and pale fat spots give the photometric loss something to grip
    for k in rng.choice(n, size=n // 6, replace=False):
        col[k] = [0.45, 0.10, 0.14]
    for k in rng.choice(n, size=n // 10, replace=False):
        col[k] = [0.98, 0.90, 0.62]
    return col


G_COLOR = _texture(N_G)
G_OPACITY = np.full(N_G, 0.95)

# ----------------------------------------------------------------- geometry helpers


def gauss_means(V: np.ndarray) -> np.ndarray:
    a, b = V[EDGES[G_EDGE, 0]], V[EDGES[G_EDGE, 1]]
    return (1 - G_T)[:, None] * a + G_T[:, None] * b


def gauss_frames(V: np.ndarray):
    """Tangent (along edge) and tangential scale per Gaussian; orientation is NOT free."""
    a, b = V[EDGES[G_EDGE, 0]], V[EDGES[G_EDGE, 1]]
    e = b - a
    L = np.linalg.norm(e, axis=1, keepdims=True)
    tan = e / L
    s_tan = 0.55 * L[:, 0] / GAUSS_PER_EDGE
    return tan, s_tan


def project(P: np.ndarray):
    """Pinhole projection of 2-D points to image coordinate u, plus depth z."""
    x = P[:, 0] - CAM[0]
    z = CAM[1] - P[:, 1]
    return FOCAL * x / z, z


def proj_jacobian(P: np.ndarray) -> np.ndarray:
    """du/d(x, y). Orthogonal to the viewing ray: the image cannot see motion along it."""
    x = P[:, 0] - CAM[0]
    z = CAM[1] - P[:, 1]
    return np.stack([FOCAL / z, FOCAL * x / z**2], 1)


# ----------------------------------------------------------------- rasterizer


def render(means: np.ndarray, tan: np.ndarray, s_tan: np.ndarray,
           colors: np.ndarray = G_COLOR, opac: np.ndarray = G_OPACITY) -> np.ndarray:
    """Depth-sorted alpha compositing of 1-D splats: C = sum_i c_i a_i prod_{j<i}(1 - a_j)."""
    u, z = project(means)
    J = proj_jacobian(means)
    nrm = np.stack([-tan[:, 1], tan[:, 0]], 1)
    var_u = (s_tan * (J * tan).sum(1)) ** 2 + (S_NORMAL * (J * nrm).sum(1)) ** 2 + 1e-5
    order = np.argsort(z)  # front to back
    u, var_u, c, o = u[order], var_u[order], colors[order], opac[order]
    alpha = np.minimum(0.99, o[:, None] * np.exp(-0.5 * (PIX_U[None] - u[:, None]) ** 2 / var_u[:, None]))
    T = np.cumprod(np.vstack([np.ones((1, NPIX)), 1 - alpha]), 0)
    return (c[:, None, :] * (alpha * T[:-1])[:, :, None]).sum(0) + T[-1][:, None] * BG[None]


def render_mesh(V: np.ndarray) -> np.ndarray:
    tan, s = gauss_frames(V)
    return render(gauss_means(V), tan, s)


# ----------------------------------------------------------------- deformation field


def visible_vertices(V: np.ndarray) -> np.ndarray:
    u, _ = project(V)
    return np.where(np.abs(u) < U_HALF * 0.98)[0]


ANCHORS = visible_vertices(V0)[::2]  # chosen once, from the first frame's visible vertices
ANCHOR_RADIUS = 0.75


def _anchor_weights() -> np.ndarray:
    d2 = ((V0[:, None, :] - V0[ANCHORS][None]) ** 2).sum(-1)
    w = np.exp(-0.5 * d2 / ANCHOR_RADIUS**2)
    return w / (w.sum(1, keepdims=True) + 0.02)  # decays outside the anchored region


W_ANCHOR = _anchor_weights()  # (N_VERT, K)


def deform(delta: np.ndarray) -> np.ndarray:
    """theta_t: anchor offsets (K, 2) -> deformed vertices (N_VERT, 2)."""
    return V0 + W_ANCHOR @ delta


# ----------------------------------------------------------------- ARAP (2-D polyline)


def arap_energy(V: np.ndarray, Vref: np.ndarray = V0) -> float:
    E = 0.0
    for i in range(N_VERT):
        nb = [j for j in (i - 1, i + 1) if 0 <= j < N_VERT]
        e0 = np.stack([Vref[i] - Vref[j] for j in nb])
        e1 = np.stack([V[i] - V[j] for j in nb])
        Uu, _, Vt = np.linalg.svd(e0.T @ e1)
        R = (Uu @ Vt).T
        if np.linalg.det(R) < 0:
            Vt[-1] *= -1
            R = (Uu @ Vt).T
        E += ((e1 - e0 @ R.T) ** 2).sum()
    return E


# ----------------------------------------------------------------- losses and optimisation


def photo_loss(img: np.ndarray, target: np.ndarray) -> float:
    return float(((img - target) ** 2).mean())


def numgrad(f, x: np.ndarray, eps: float = 1e-4) -> np.ndarray:
    g = np.zeros_like(x)
    flat, gflat = x.reshape(-1), g.reshape(-1)
    for i in range(flat.size):
        old = flat[i]
        flat[i] = old + eps
        fp = f(x)
        flat[i] = old - eps
        fm = f(x)
        flat[i] = old
        gflat[i] = (fp - fm) / (2 * eps)
    return g


class Adam:
    def __init__(self, lr: float, b1: float = 0.9, b2: float = 0.999):
        self.lr, self.b1, self.b2, self.m, self.v, self.k = lr, b1, b2, 0.0, 0.0, 0

    def step(self, x: np.ndarray, g: np.ndarray) -> np.ndarray:
        self.k += 1
        self.m = self.b1 * self.m + (1 - self.b1) * g
        self.v = self.b2 * self.v + (1 - self.b2) * g * g
        mh = self.m / (1 - self.b1**self.k)
        vh = self.v / (1 - self.b2**self.k)
        return x - self.lr * mh / (np.sqrt(vh) + 1e-8)


# ----------------------------------------------------------------- the "video"

PRESS_X = 0.8


def ground_truth(frac: float = 1.0) -> np.ndarray:
    """True intra-operative surface (unknown to the method; only its image is seen).

    A tool presses the tissue away from the camera (out-of-plane: the hard direction for a
    mono camera). Tissue is close to inextensible, so material is drawn in from the sides
    and edge lengths stay ~constant. frac in [0, 1] ramps the press over the video.
    """
    x, y = V0[:, 0], V0[:, 1]
    xf = np.linspace(x.min(), x.max(), 4001)
    yf = np.interp(xf, x, y)
    dyf = -0.5 * frac * np.exp(-0.5 * ((xf - PRESS_X) / 0.8) ** 2)
    yp, dyp = np.gradient(yf, xf), np.gradient(dyf, xf)
    dxp = np.sqrt(np.maximum(1 + yp**2 - (yp + dyp) ** 2, 1e-9)) - 1  # keep |d(curve)/dx|
    dxf = np.concatenate([[0], np.cumsum(0.5 * (dxp[1:] + dxp[:-1]) * np.diff(xf))])
    dxf -= np.interp(PRESS_X, xf, dxf)
    return V0 + np.stack([np.interp(x, xf, dxf), np.interp(x, xf, dyf)], 1)


# ----------------------------------------------------------------- the two optimisers


def track_bridgesplat(n_frames: int = 10, iters: int = 30, lam_arap: float = 0.02, lr: float = 0.01):
    """Frame-by-frame tracking, warm-started. Only the anchor offsets (geometry) are learned."""
    delta = np.zeros((len(ANCHORS), 2))

    def total(d, target):
        V = deform(d)
        return photo_loss(render_mesh(V), target) + lam_arap * arap_energy(V)

    states = []
    for f in range(1, n_frames + 1):
        target = render_mesh(ground_truth(f / n_frames))
        opt = Adam(lr)
        for k in range(iters + 1):
            V = deform(delta)
            img = render_mesh(V)
            states.append(dict(V=V, img=img, loss=photo_loss(img, target)))
            if k < iters:
                delta = opt.step(delta, numgrad(lambda d: total(d, target), delta))
    return states


def track_free(n_frames: int = 10, iters: int = 30, lr: float = 0.01):
    """3DGS-style baseline: every mean (2-D) and tangential scale is free, no mesh."""
    tan, s0 = gauss_frames(V0)
    P = np.concatenate([gauss_means(V0), np.log(s0)[:, None]], 1)
    states = []
    for f in range(1, n_frames + 1):
        target = render_mesh(ground_truth(f / n_frames))
        opt = Adam(lr)

        def fn(p):
            return photo_loss(render(p[:, :2], tan, np.exp(p[:, 2])), target)

        for k in range(iters + 1):
            img = render(P[:, :2], tan, np.exp(P[:, 2]))
            states.append(dict(mu=P[:, :2].copy(), s=np.exp(P[:, 2]), img=img, loss=photo_loss(img, target)))
            if k < iters:
                P = opt.step(P, numgrad(fn, P))
    return states


# ----------------------------------------------------------------- the chain rule, explicitly


def mean_gradients(V: np.ndarray, target: np.ndarray) -> np.ndarray:
    """dE_photo / d mu_i for every Gaussian mean."""
    tan, s = gauss_frames(V)
    mu = gauss_means(V)
    return numgrad(lambda m: photo_loss(render(m, tan, s), target), mu.copy(), eps=1e-5)


def vertex_gradients_from_means(g_mu: np.ndarray) -> np.ndarray:
    """Through mu_i = (1-t) v_a + t v_b: the barycentric weights are the Jacobian."""
    gV = np.zeros((N_VERT, 2))
    np.add.at(gV, EDGES[G_EDGE, 0], (1 - G_T)[:, None] * g_mu)
    np.add.at(gV, EDGES[G_EDGE, 1], G_T[:, None] * g_mu)
    return gV


def anchor_gradients(gV: np.ndarray) -> np.ndarray:
    """Through v = V0 + W delta."""
    return W_ANCHOR.T @ gV


# ----------------------------------------------------------------- cache for the scenes


def compute_all(cache: str | None = None, n_frames: int = 10, iters: int = 30) -> dict:
    """Run both optimisations once; cached because the scenes are re-rendered often."""
    if cache and os.path.exists(cache):
        z = np.load(cache)
        return {k: z[k] for k in z.files}
    br = track_bridgesplat(n_frames, iters)
    fr = track_free(n_frames, iters)
    gts = np.stack([ground_truth(f / n_frames) for f in range(n_frames + 1)])
    targets = np.stack([render_mesh(g) for g in gts])
    g_mu = mean_gradients(V0, targets[1])
    g_V = vertex_gradients_from_means(g_mu)
    out = dict(
        br_V=np.stack([s["V"] for s in br]), br_img=np.stack([s["img"] for s in br]),
        br_loss=np.array([s["loss"] for s in br]),
        fr_mu=np.stack([s["mu"] for s in fr]), fr_s=np.stack([s["s"] for s in fr]),
        fr_img=np.stack([s["img"] for s in fr]), fr_loss=np.array([s["loss"] for s in fr]),
        gt_V=gts, targets=targets, g_mu=g_mu, g_V=g_V, g_anchor=anchor_gradients(g_V),
        n_frames=np.array(n_frames), iters=np.array(iters),
    )
    if cache:
        os.makedirs(os.path.dirname(cache) or ".", exist_ok=True)
        np.savez_compressed(cache, **out)
    return out


def summary(d: dict) -> dict:
    """The numbers quoted on screen."""
    gt = d["gt_V"][-1]
    mu0, mu_gt = gauss_means(V0), gauss_means(gt)
    vis = np.abs(project(mu0)[0]) < U_HALF
    err = lambda mu: np.linalg.norm(mu[vis] - mu_gt[vis], axis=1)
    ray = (mu0 - CAM) / np.linalg.norm(mu0 - CAM, axis=1, keepdims=True)
    g = d["g_mu"]
    gn = np.linalg.norm(g, axis=1)
    m = gn > 1e-3 * gn.max()
    return dict(
        loss_rigged=float(d["br_loss"][-1]), loss_free=float(d["fr_loss"][-1]),
        err_start=err(mu0), err_rigged=err(gauss_means(d["br_V"][-1])), err_free=err(d["fr_mu"][-1]),
        dent_true=float((gt - V0)[:, 1].min()), dent_rigged=float((d["br_V"][-1] - V0)[:, 1].min()),
        cos_grad_ray=float(np.median(np.abs((g[m] * ray[m]).sum(1)) / gn[m])),
    )


if __name__ == "__main__":
    import time

    t0 = time.time()
    d = compute_all(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache", "toy.npz"))
    s = summary(d)
    print(f"{time.time() - t0:.0f}s   anchors {ANCHORS}   Gaussians {N_G}")
    print(f"photometric loss    rigged {s['loss_rigged']:.6f}   free {s['loss_free']:.6f}")
    for k in ("start", "rigged", "free"):
        e = s[f"err_{k}"]
        print(f"3-D error {k:>7}:  mean {e.mean():.3f}   max {e.max():.3f}")
    print(f"dent depth  true {s['dent_true']:.3f}   rigged {s['dent_rigged']:.3f}"
          f"   ({s['dent_rigged'] / s['dent_true']:.0%})")
    print(f"median |cos(dE/dmu, ray)| = {s['cos_grad_ray']:.3f}")
