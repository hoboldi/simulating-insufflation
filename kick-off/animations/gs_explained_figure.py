"""Three-panel Gaussian splatting explainer for the kick-off deck (slide "Gaussian splatting in pictures").

Regenerate from kick-off/slides:
    uv run --with matplotlib --with numpy python ../animations/gs_explained_figure.py assets/gs_explained.png assets/gs_gaussian.png
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle, Polygon

out = sys.argv[1]
BG, FG, MUTED, PANEL = "#0e1116", "#e8eaed", "#9aa0a6", "#1c2128"
ORANGE, BLUE, GREEN = "#f0a030", "#4aa3ff", "#3ecf8e"
plt.rcParams.update({
    "font.family": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "mathtext.fontset": "dejavusans",
    "text.color": FG, "figure.facecolor": BG, "axes.facecolor": BG,
})

def rgb(h):
    h = h.lstrip("#"); return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])

def blob(ax, cx, cy, a, b, ang, color, opacity, extent, n=500):
    """Soft 2D Gaussian; a, b = 1-sigma semi-axes, ang in degrees."""
    x0, x1, y0, y1 = extent
    X, Y = np.meshgrid(np.linspace(x0, x1, n), np.linspace(y0, y1, max(2, int(n * (y1 - y0) / (x1 - x0)))))
    t = np.deg2rad(ang); c, s = np.cos(t), np.sin(t)
    u, v = c * (X - cx) + s * (Y - cy), -s * (X - cx) + c * (Y - cy)
    rgba = np.zeros(X.shape + (4,)); rgba[..., :3] = rgb(color)
    rgba[..., 3] = opacity * np.exp(-0.5 * ((u / a) ** 2 + (v / b) ** 2))
    ax.imshow(rgba, extent=extent, origin="lower", interpolation="bilinear", zorder=2)

def ellipse_pts(cx, cy, a, b, ang, k=2.0, n=400):
    t = np.deg2rad(ang); th = np.linspace(0, 2 * np.pi, n)
    x, y = k * a * np.cos(th), k * b * np.sin(th)
    return cx + np.cos(t) * x - np.sin(t) * y, cy + np.sin(t) * x + np.cos(t) * y

out_gauss = sys.argv[2]
TS = 20

# ---------- separate small figure: one Gaussian (goes next to the parameter row) ----------
fg = plt.figure(figsize=(3.4, 2.3), dpi=180)
ax1 = fg.add_axes([0, 0, 1, 1]); ax1.set_axis_off()
E1 = (-1.85, 1.85, -1.25, 1.25)
a, b, ang = 0.72, 0.36, 25
blob(ax1, 0, 0, a, b, ang, ORANGE, 0.95, E1)
ex, ey = ellipse_pts(0, 0, a, b, ang)
ax1.plot(ex, ey, ls="--", lw=1.2, color=ORANGE, alpha=0.7, zorder=3)
t = np.deg2rad(ang)
for dx, dy in [(a * np.cos(t), a * np.sin(t)), (-b * np.sin(t), b * np.cos(t))]:
    ax1.annotate("", xy=(dx, dy), xytext=(0, 0), zorder=4,
                 arrowprops=dict(arrowstyle="-|>", color=FG, lw=1.8, mutation_scale=16))
ax1.plot(0, 0, "o", color=FG, ms=6, zorder=5)
ax1.text(0.06, -0.36, r"$p$", fontsize=20, color=FG, zorder=5)
ax1.text(1.22, 0.78, r"$\Sigma$", fontsize=20, color=ORANGE, zorder=5)
ax1.set_xlim(E1[0], E1[1]); ax1.set_ylim(E1[2], E1[3]); ax1.set_aspect("equal")
fg.savefig(out_gauss, facecolor=BG, bbox_inches="tight", pad_inches=0.05)
print("saved", out_gauss)

# ---------- main figure: render one frame ----------
fig = plt.figure(figsize=(13.5, 4.5), dpi=180)
gs = fig.add_gridspec(1, 2, width_ratios=[2.25, 1.6], wspace=0.06, left=0.01, right=0.99, top=0.86, bottom=0.03)
ax2, ax3 = (fig.add_subplot(gs[0, i]) for i in range(2))
for ax in (ax2, ax3):
    ax.set_axis_off()

# ---------- panel 2: splatting, side view ----------
E2 = (-0.7, 7.1, -1.55, 1.75)
ZP = 1.6                       # image plane distance
m = 0.12                       # slope of the highlighted pixel ray
G = [(2.9, 0.40, 0.40, 0.20, 25, ORANGE),
     (4.3, 0.78, 0.52, 0.24, -30, BLUE),
     (5.8, 0.55, 0.58, 0.28, 15, GREEN)]
for cx, cy, ga, gb, gang, col in G:
    blob(ax2, cx, cy, ga, gb, gang, col, 0.9, E2)
    ox, oy = ellipse_pts(cx, cy, ga, gb, gang)
    ax2.plot(ox, oy, ls="--", lw=1.0, color=col, alpha=0.5, zorder=3)
# image plane
ax2.add_patch(Rectangle((ZP - 0.12, -1.25), 0.24, 2.6, facecolor=PANEL, edgecolor=MUTED, lw=1.2, zorder=3))
ax2.text(ZP, -1.48, "image plane", fontsize=16, color=MUTED, ha="center")
# camera
ax2.add_patch(Polygon([(-0.55, 0.28), (-0.55, -0.28), (0, 0)], closed=True, facecolor=MUTED, zorder=4))
ax2.text(-0.3, -0.55, "camera", fontsize=16, color=MUTED, ha="center")
# projections: tangent rays + footprint on the image plane
for i, (cx, cy, ga, gb, gang, col) in enumerate(G):
    px, py = ellipse_pts(cx, cy, ga, gb, gang)
    sl = py / px
    lo, hi = sl.min(), sl.max()
    for s_ in (lo, hi):
        j = np.argmin(np.abs(sl - s_))
        ax2.plot([0, px[j]], [0, py[j]], ls=(0, (4, 3)), lw=1.0, color=col, alpha=0.55, zorder=1)
    ax2.add_patch(Ellipse((ZP + (i - 1) * 0.06, ZP * (lo + hi) / 2), 0.16, ZP * (hi - lo),
                          facecolor=col, alpha=0.6, edgecolor="none", zorder=4))
ax2.text(ZP + 0.22, ZP * 0.45, "splats", fontsize=16, color=FG, va="center")
# highlighted pixel ray
ax2.plot([0, 7.0], [0, 7.0 * m], color=FG, lw=1.8, zorder=6)
ax2.add_patch(Rectangle((ZP - 0.12, ZP * m - 0.03), 0.24, 0.06, facecolor=FG, zorder=7))
ax2.annotate("one pixel", xy=(ZP, ZP * m - 0.04), xytext=(ZP + 0.35, -0.75), fontsize=16, color=FG,
             arrowprops=dict(arrowstyle="-", color=FG, lw=1.0), zorder=7)
for i, (cx, *_ ) in enumerate(G):
    ax2.plot(cx, cx * m, "o", ms=17, color=FG, zorder=8)
    ax2.text(cx, cx * m - 0.005, str(i + 1), fontsize=13, color=BG, ha="center", va="center", zorder=9, weight="bold")
ax2.text(5.55, -1.0, "sorted by depth: 1 → 2 → 3", fontsize=16, color=MUTED, ha="center")
ax2.set_xlim(E2[0], E2[1]); ax2.set_ylim(E2[2], E2[3]); ax2.set_aspect("equal")

# ---------- panel 3: compositing one pixel ----------
ax3.set_xlim(0, 1); ax3.set_ylim(0, 1)
alphas = [0.5, 0.6, 0.8]; cols = [ORANGE, BLUE, GREEN]
T, w = 1.0, []
for al in alphas:
    w.append(T * al); T *= 1 - al
rows = [r"$\alpha_1 = 0.5$  of the 100 % $\rightarrow$ 50 %",
        r"$\alpha_2 = 0.6$  of the 50 % left $\rightarrow$ 30 %",
        r"$\alpha_3 = 0.8$  of the 20 % left $\rightarrow$ 16 %"]
for i, (txt, col) in enumerate(zip(rows, cols)):
    y = 0.90 - i * 0.10
    ax3.scatter([0.035], [y], s=330, color=col, zorder=3)
    ax3.text(0.035, y - 0.002, str(i + 1), fontsize=13, color=BG, ha="center", va="center", weight="bold", zorder=4)
    ax3.text(0.085, y, txt, fontsize=16.5, color=FG, va="center")
# stacked bar of weights
x, y0, h, L = 0.02, 0.45, 0.12, 0.70
for wi, col in zip(w, cols):
    ax3.add_patch(Rectangle((x, y0), L * wi, h, facecolor=col, edgecolor=BG, lw=1.5))
    ax3.text(x + L * wi / 2, y0 + h / 2, f"{wi:.2f}", fontsize=15, color=BG, ha="center", va="center", weight="bold")
    x += L * wi
ax3.add_patch(Rectangle((x, y0), L * T, h, facecolor=PANEL, edgecolor=MUTED, lw=1.0))
ax3.text(0.02, y0 + h + 0.035, "weights = share of the pixel colour", fontsize=15, color=MUTED)
ax3.text(0.02 + L, y0 - 0.05, f"{T:.2f} background", fontsize=14, color=MUTED, ha="right")
# resulting pixel colour
C = sum(wi * rgb(c) for wi, c in zip(w, cols)) + T * rgb(BG)
ax3.text(0.765, y0 + h / 2, "=", fontsize=22, color=FG, ha="center", va="center")
ax3.add_patch(Rectangle((0.81, y0 - 0.01), 0.14, h + 0.02, facecolor=C, edgecolor=FG, lw=1.2))
ax3.text(0.88, y0 - 0.06, "pixel", fontsize=15, color=FG, ha="center")
ax3.text(0.02, 0.21, r"$C = \sum_i\, c_i\, \alpha_i \prod_{j<i} (1-\alpha_j)$", fontsize=21, color=FG)
ax3.text(0.02, 0.0, r"same weights $\times$ depth $z_i$ $\rightarrow$ depth map", fontsize=16, color=MUTED)

fig.canvas.draw()
for ax, title in [(ax2, "1 · splat onto the image"), (ax3, "2 · blend one pixel, front to back")]:
    fig.text(ax.get_position().x0 + 0.005, 0.94, title, fontsize=TS, color=FG, va="top")
fig.savefig(out, facecolor=BG, bbox_inches="tight", pad_inches=0.12)
print("saved", out)
