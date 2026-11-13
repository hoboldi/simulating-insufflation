"""Manim scenes for part 3 (BridgeSplat) of the Pair B kick-off.

What is constrained, what is free, and what backpropagation changes when the only
observation is a monocular video. Based on Fehrentz et al., "BridgeSplat", MICCAI 2025
(arXiv 2509.18501), Sec. 2.

Scenes
  S1_ConstrainedParams  one Gaussian: free / constrained / fixed, 3DGS vs BridgeSplat
  S2_GradientFlow       computation graph: where the photometric gradient goes and where it stops
  S3_MonoRay            why mono video needs the mesh: dE/dmu is perpendicular to the ray;
                        the CT fixes each face's size, so the image can push faces in depth
  S4_MonoTracking       toy 2-D BridgeSplat optimised for real on a mono "video" (toy_splat2d.py),
                        against free 3DGS-style Gaussians

Preview:   .venv/bin/manim -pql bridgesplat_scenes.py S1_ConstrainedParams
Final:     ./render.sh            (1080p30, copies the mp4s to ../slides/assets/)

No LaTeX needed: all maths is Pango markup.
"""
from __future__ import annotations

import os

import numpy as np
from manim import *

import toy_splat2d as T

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache", "toy.npz")
FONT = "Helvetica Neue"

# deck palette (slides/theme/pair-b.css) + a gradient red as in the paper's Fig. 1
FG = ManimColor("#1f2933")
ACCENT = ManimColor("#1e5aa8")   # learned freely
WARN = ManimColor("#c2620a")     # learned, but constrained / regularised
WARN_TXT = ManimColor("#9c4a04")
MUTED = ManimColor("#6b7785")    # fixed / given / derived by a rule
GRAD = ManimColor("#d1242f")     # gradients
SOFT = {"free": ManimColor("#eaf1fa"), "con": ManimColor("#fdf3e8"), "fix": ManimColor("#eef0f2"),
        "der": ManimColor("#ffffff"), "loss": ManimColor("#fdecec")}
EDGE = {"free": ACCENT, "con": WARN, "fix": MUTED, "der": FG, "loss": GRAD}
TXT = {"free": ACCENT, "con": WARN_TXT, "fix": MUTED, "der": FG, "loss": GRAD}
TISSUE = [ManimColor(c) for c in ("#d9655f", "#e8a49c", "#8a2a30", "#e9c46a")]


# ============================================================================ helpers


def _scripts(s: str, size: float) -> str:
    """Pango's <sub>/<sup> come out tiny in manim; use a 'smaller' span with a size-scaled rise."""
    sub = f'<span font_size="smaller" rise="{int(-48 * size)}">'
    sup = f'<span font_size="smaller" rise="{int(125 * size)}">'
    return s.replace("<sub>", sub).replace("<sup>", sup).replace("</sub>", "</span>").replace("</sup>", "</span>")


def M(s: str, size: float = 24, color=FG, **kw) -> MarkupText:
    return MarkupText(_scripts(s, size), font=FONT, font_size=size, color=color, **kw)


def lock_icon(color=MUTED, h: float = 0.2) -> VGroup:
    body = RoundedRectangle(width=0.9 * h, height=0.68 * h, corner_radius=0.12 * h)
    body.set_fill(color, 1).set_stroke(width=0)
    arc = Arc(radius=0.27 * h, start_angle=0, angle=PI, arc_center=body.get_top())
    arc.set_stroke(color, width=max(1.5, 11 * h))
    legs = VGroup(*[Line(body.get_top() + s * 0.27 * h * RIGHT, body.get_top() + s * 0.27 * h * RIGHT + 0.08 * h * DOWN)
                    .set_stroke(color, width=max(1.5, 11 * h)) for s in (-1, 1)])
    return VGroup(arc, legs, body)


def chip(markup: str, kind: str, width: float | None = None, size: float = 18, lock: bool = False) -> VGroup:
    t = M(markup, size=size, color=TXT[kind])
    w = width or t.width + 0.34 + (0.25 if lock else 0)
    box = RoundedRectangle(width=w, height=t.height + 0.2, corner_radius=0.08)
    box.set_fill(SOFT[kind], 1).set_stroke(EDGE[kind], width=1.6)
    g = VGroup(box, t)
    if lock:
        lk = lock_icon(TXT[kind], h=0.2).move_to(box.get_left() + RIGHT * 0.22)
        t.shift(RIGHT * 0.12)
        g.add(lk)
    return g


def gauss_blob(c, a: float, b: float, ang: float, color, op: float = 0.9, with_dot: bool = True) -> VGroup:
    """A Gaussian drawn as three nested ellipses (a, b = semi-axes in scene units)."""
    c = np.asarray(c, dtype=float)
    if c.shape == (2,):
        c = np.array([c[0], c[1], 0.0])
    g = VGroup(*[Ellipse(width=max(2 * a * k, 1e-3), height=max(2 * b * k, 1e-3))
                 .set_fill(color, op * f).set_stroke(width=0)
                 for k, f in ((1.0, 0.3), (0.68, 0.45), (0.4, 0.7))])
    g.rotate(ang).move_to(c)
    if with_dot:
        g.add(Dot(c, radius=0.035, color=FG))
    return g


def proj_simplex(v: np.ndarray) -> np.ndarray:
    """Euclidean projection onto {b >= 0, sum b = 1}."""
    u = np.sort(v)[::-1]
    css = np.cumsum(u)
    rho = np.nonzero(u * np.arange(1, len(v) + 1) > (css - 1))[0][-1]
    return np.maximum(v - (css[rho] - 1) / (rho + 1), 0)


def p3(p) -> np.ndarray:
    return np.array([p[0], p[1], 0.0])


def camera_icon(center, s: float = 1.0) -> VGroup:
    """Small pinhole-camera glyph; `center` is the projection centre (lens tip)."""
    center = p3(center)
    lens = Polygon(center + s * np.array([-0.12, 0.1, 0]), center + s * np.array([0.12, 0.1, 0]), center,
                   ).set_fill(FG, 1).set_stroke(width=0)
    body = RoundedRectangle(width=0.44 * s, height=0.26 * s, corner_radius=0.04 * s)
    body.set_fill(FG, 1).set_stroke(width=0).move_to(center + s * np.array([0, 0.23, 0]))
    return VGroup(body, lens)


def caption(markup: str, y: float = -3.45, size: float = 22, color=FG) -> MarkupText:
    return M(markup, size=size, color=color).move_to([0, y, 0])


# ============================================================================ scene 1


class S1_ConstrainedParams(Scene):
    """One Gaussian: what may the optimiser change? 3DGS (all free) vs BridgeSplat (rigged)."""

    def construct(self):
        # ------------------------------------------------------------ table on the right
        xn, xg, xb = 0.35, 3.0, 5.42
        ys = [2.2, 1.38, 0.56, -0.26, -1.08, -1.9]
        hdr = VGroup(
            M("parameter", 19, MUTED).move_to([xn, 2.95, 0], aligned_edge=LEFT),
            M("<b>3DGS</b>", 22).move_to([xg, 2.95, 0]),
            M("<b>BridgeSplat</b>", 22).move_to([xb, 2.95, 0]),
        )
        rule = Line([xn, 2.68, 0], [6.95, 2.68, 0]).set_stroke(MUTED, 1.2)
        names = ["mean  <i>μ</i>", "rotation  <i>q</i>", "scale  <i>s</i>", "opacity  <i>α</i>",
                 "colour  <i>c</i>  (SH)", "mesh vertices"]
        name_m = VGroup(*[M(n, 20).move_to([xn, y, 0], aligned_edge=LEFT) for n, y in zip(names, ys)])
        gs = [chip(t, "free", width=1.6) for t in ("free  ∈ ℝ³", "free", "free  ∈ ℝ³", "free", "free")]
        gs.append(M("—  no mesh", 18, MUTED))
        for c, y in zip(gs, ys):
            c.move_to([xg, y, 0])
        bs = [
            chip("on its own triangle\nb ≥ 0,  Σ b = 1", "con", width=2.95, size=17),
            chip("= triangle normal\nnot learned", "fix", width=2.95, size=17, lock=True),
            chip("2 tangent: learned, capped\nnormal: fixed, tiny", "con", width=2.95, size=17),
            chip("free", "free", width=2.95, size=17),
            chip("free", "free", width=2.95, size=17),
            chip("only via θ<sub>t</sub>: anchors δ<sub>k</sub>\nregularised by ARAP", "con", width=2.95, size=17),
        ]
        for c, y in zip(bs, ys):
            c.move_to([xb, y, 0])
        legend = VGroup(chip("learned freely", "free", size=16), chip("learned, constrained", "con", size=16),
                        chip("fixed / given", "fix", size=16, lock=True)).arrange(RIGHT, buff=0.22)
        legend.move_to([xn, -3.05, 0], aligned_edge=LEFT)

        # ------------------------------------------------------------ phase A: free 3DGS Gaussian
        head = M("3D Gaussian Splatting: every parameter is free", 26).move_to([-6.85, 3.5, 0], aligned_edge=LEFT)
        self.play(FadeIn(head), FadeIn(hdr), Create(rule), FadeIn(name_m), FadeIn(legend), run_time=1.2)

        states = [
            ((-3.6, 0.7), 0.6, 0.3, 20 * DEGREES, TISSUE[0], 0.9),
            ((-2.0, 1.8), 0.95, 0.2, 75 * DEGREES, TISSUE[0], 0.9),
            ((-5.0, -0.5), 0.35, 0.35, 75 * DEGREES, TISSUE[2], 0.9),
            ((-3.0, 0.1), 1.2, 0.55, 140 * DEGREES, TISSUE[1], 0.35),
            ((-3.6, 0.7), 0.6, 0.3, 20 * DEGREES, TISSUE[0], 0.9),
        ]
        blob = gauss_blob(*states[0], with_dot=False)
        self.play(FadeIn(blob, scale=0.6), run_time=0.6)
        for i, st in enumerate(states[1:]):
            anims = [Transform(blob, gauss_blob(*st, with_dot=False))]
            if i < 3:
                anims.append(FadeIn(VGroup(*gs[i * 2:i * 2 + 2]) if i < 2 else VGroup(gs[4], gs[5]), shift=LEFT * 0.15))
            self.play(*anims, run_time=1.3)
        free_note = M("roams, rotates and stretches wherever it fits the image best", 18, MUTED)
        free_note.move_to([-3.6, -1.85, 0])
        self.play(FadeIn(free_note), run_time=0.6)
        self.wait(1.2)

        # ------------------------------------------------------------ phase B: rigged to a mesh triangle
        head2 = M("BridgeSplat: every Gaussian is rigged to a CT-mesh triangle", 26).move_to(head, aligned_edge=LEFT)
        pts = {
            "v1": (-5.0, -0.1), "v2": (-2.0, -0.3), "v3": (-3.4, 2.45),
            "nr": (-0.7, 1.6), "nl": (-6.4, 1.8), "nb": (-3.5, -1.1), "nt": (-1.7, 3.0),
        }
        dots = {k: Dot(p3(p), radius=0.055, color=FG if k.startswith("v") else MUTED) for k, p in pts.items()}
        tris = [("v1", "v2", "v3"), ("v2", "nr", "v3"), ("v1", "v3", "nl"), ("v1", "nb", "v2"), ("v3", "nr", "nt")]

        def mesh():
            g = VGroup()
            for i, tri in enumerate(tris):
                poly = Polygon(*[dots[k].get_center() for k in tri])
                if i == 0:
                    poly.set_fill(ManimColor("#fbeee9"), 1).set_stroke(FG, 2.5)
                else:
                    poly.set_fill(opacity=0).set_stroke(MUTED, 1.4, opacity=0.7)
                g.add(poly)
            return g

        mesh_m = always_redraw(mesh)
        vlabels = VGroup(*[always_redraw(lambda k=k, d=d: M(f"v<sub>{k}</sub>", 18).next_to(dots[f"v{k}"], d, buff=0.08))
                           for k, d in ((1, DL), (2, DR), (3, UP))])

        # Gaussian state (all trackers; geometry follows the triangle)
        ib = [ValueTracker(1 / 3), ValueTracker(1 / 3)]      # intended barycentrics (may leave the simplex)
        sa, sb = ValueTracker(0.55), ValueTracker(0.3)          # tangent scales
        SA0, SB0, CAP = 0.55, 0.3, 1.6
        op, colt = ValueTracker(0.9), ValueTracker(0.0)

        def tri_pts():
            return [dots[k].get_center() for k in ("v1", "v2", "v3")]

        def bary():
            b = np.array([ib[0].get_value(), ib[1].get_value(), 1 - ib[0].get_value() - ib[1].get_value()])
            return b, proj_simplex(b)

        def colour():
            t = colt.get_value() % len(TISSUE)
            i = int(np.floor(t))
            return interpolate_color(TISSUE[i], TISSUE[(i + 1) % len(TISSUE)], t - i)

        def rigged():
            P = tri_pts()
            _, b = bary()
            c = sum(bi * pi for bi, pi in zip(b, P))
            ang = angle_of_vector(P[1] - P[0])
            return gauss_blob(c, min(sa.get_value(), CAP * SA0), min(sb.get_value(), CAP * SB0), ang,
                              colour(), op.get_value())

        P = tri_pts()
        target = rigged()
        self.play(FadeOut(free_note), Transform(head, head2), run_time=0.8)
        self.play(Create(mesh_m), *[FadeIn(d) for d in dots.values()], FadeIn(vlabels), run_time=1.2)
        self.add_foreground_mobjects(*dots.values())
        self.play(Transform(blob, target), run_time=1.0)
        self.remove(blob)
        blob_m = always_redraw(rigged)
        self.add(blob_m)

        # ---- row 0: mean = barycentric, clamped to the triangle
        def bars():
            _, b = bary()
            g = VGroup()
            for i, bi in enumerate(b):
                x = -6.35 + 0.45 * i
                r = Rectangle(width=0.3, height=max(1.0 * bi, 0.01)).set_fill(WARN, 0.85).set_stroke(width=0)
                r.move_to([x, -3.45, 0], aligned_edge=DOWN)
                g.add(r, M(f"b<sub>{i + 1}</sub>", 16).move_to([x, -3.68, 0]))
            g.add(Line([-6.6, -3.45, 0], [-5.25, -3.45, 0]).set_stroke(FG, 1.2))
            g.add(M(f"Σ b = {b.sum():.2f}", 16, WARN_TXT).move_to([-4.55, -3.0, 0]))
            return g

        def ghost():
            bi, b = bary()
            if np.all(bi >= -1e-6):
                return VGroup()
            P = tri_pts()
            x = sum(v * p for v, p in zip(bi, P))
            c = sum(v * p for v, p in zip(b, P))
            return VGroup(DashedLine(c, x, dash_length=0.06).set_stroke(GRAD, 2),
                          Circle(radius=0.16).set_stroke(GRAD, 2).move_to(x),
                          M("✕", 18, GRAD).move_to(x))

        bars_m, ghost_m = always_redraw(bars), always_redraw(ghost)
        mu_note = M("the mean is a barycentric blend of the 3 vertices,\nclamped to the triangle", 17, WARN_TXT)
        mu_note.move_to([-3.6, -1.85, 0])
        self.play(Indicate(name_m[0], color=WARN), FadeIn(bars_m), FadeIn(mu_note), run_time=1.0)
        self.add(ghost_m)
        for target_b in ((0.6, 0.25), (0.15, 0.55), (0.62, 0.62), (0.75, 0.55), (0.4, 0.4)):
            self.play(ib[0].animate.set_value(target_b[0]), ib[1].animate.set_value(target_b[1]), run_time=1.1)
        self.play(FadeIn(bs[0], shift=LEFT * 0.15), run_time=0.6)
        self.wait(0.4)

        # ---- row 1 + 2: orientation fixed to the face, normal scale fixed, tangent scales capped
        tilt = ValueTracker(0.0)
        inset_c = np.array([-1.9, -2.95, 0])

        def side_view():
            ang = tilt.get_value()
            d = np.array([np.cos(ang), np.sin(ang), 0])
            n = np.array([-np.sin(ang), np.cos(ang), 0])
            g = VGroup(Line(inset_c - 1.35 * d, inset_c + 1.35 * d).set_stroke(FG, 2.5))
            e = Ellipse(width=2 * min(sa.get_value(), CAP * SA0), height=0.07).set_fill(colour(), op.get_value())
            e.set_stroke(width=0).rotate(ang).move_to(inset_c + 0.045 * n)
            g.add(e, Arrow(inset_c, inset_c + 0.38 * n, buff=0, stroke_width=2.5, tip_length=0.11,
                            max_tip_length_to_length_ratio=0.3, color=MUTED))
            g.add(M("<i>n</i>", 16, MUTED).move_to(inset_c + 0.38 * n + 0.18 * normalize(d + n)))
            return g

        frame_box = RoundedRectangle(width=3.6, height=1.05, corner_radius=0.08).set_stroke(MUTED, 1.2).move_to(inset_c + 0.12 * UP)
        frame_lbl = M("side view of the triangle", 15, MUTED).next_to(frame_box, DOWN, buff=0.07)
        side_m = always_redraw(side_view)

        def axes_face():
            P = tri_pts()
            _, b = bary()
            c = sum(bi * pi for bi, pi in zip(b, P))
            t1 = normalize(P[1] - P[0])
            nz = np.cross(P[1] - P[0], P[2] - P[0])
            t2 = normalize(np.cross(nz, t1)) if np.linalg.norm(nz) > 0 else UP
            return VGroup(
                Arrow(c, c + 0.75 * t1, buff=0, stroke_width=2.5, tip_length=0.12, color=MUTED),
                Arrow(c, c + 0.75 * t2, buff=0, stroke_width=2.5, tip_length=0.12, color=MUTED),
                M("t<sub>1</sub>", 15, MUTED).move_to(c + 0.95 * t1), M("t<sub>2</sub>", 15, MUTED).move_to(c + 0.95 * t2),
            )

        axes_m = always_redraw(axes_face)
        q_note = M("its axes come from the triangle: it lies flat in the face", 17, MUTED).move_to([-3.6, -1.85, 0])
        self.play(FadeOut(bars_m), FadeOut(mu_note), FadeIn(frame_box), FadeIn(frame_lbl), FadeIn(side_m),
                  FadeIn(axes_m), Indicate(name_m[1], color=MUTED), run_time=1.0)
        self.remove(ghost_m)
        self.play(FadeIn(q_note), run_time=0.5)
        self.play(tilt.animate.set_value(25 * DEGREES), run_time=1.0)
        self.play(tilt.animate.set_value(-15 * DEGREES), run_time=1.0)
        self.play(tilt.animate.set_value(0), FadeIn(bs[1], shift=LEFT * 0.15), run_time=0.9)

        def cap_ellipse():
            P = tri_pts()
            _, b = bary()
            c = sum(bi * pi for bi, pi in zip(b, P))
            e = DashedVMobject(Ellipse(width=2 * CAP * SA0, height=2 * CAP * SB0), num_dashes=40)
            return e.set_stroke(WARN, 2).rotate(angle_of_vector(P[1] - P[0])).move_to(c)

        cap_m = always_redraw(cap_ellipse)
        s_note = M("tangent scales grow only up to the cap;\nthickness along <i>n</i> never changes", 17, WARN_TXT)
        s_note.move_to(q_note)
        self.play(FadeOut(q_note), FadeOut(axes_m), FadeIn(cap_m), Indicate(name_m[2], color=WARN), run_time=0.8)
        self.play(FadeIn(s_note), run_time=0.5)
        self.play(sa.animate.set_value(1.4), sb.animate.set_value(0.16), run_time=1.6)
        self.play(Indicate(cap_m, color=WARN, scale_factor=1.05), run_time=0.7)
        self.play(sa.animate.set_value(0.55), sb.animate.set_value(0.3), FadeIn(bs[2], shift=LEFT * 0.15), run_time=1.0)

        # ---- rows 3 + 4: opacity and colour stay free
        a_note = M("opacity and colour stay free", 17, ACCENT).move_to(q_note)
        self.play(FadeOut(s_note), FadeOut(cap_m), FadeIn(a_note),
                  Indicate(name_m[3], color=ACCENT), Indicate(name_m[4], color=ACCENT), run_time=0.8)
        self.play(colt.animate.set_value(2.0), op.animate.set_value(0.35), run_time=1.3)
        self.play(colt.animate.set_value(4.0), op.animate.set_value(0.9), FadeIn(bs[3], shift=LEFT * 0.15),
                  FadeIn(bs[4], shift=LEFT * 0.15), run_time=1.3)

        # ---- row 5: vertices move only through the deformation field; the Gaussian rides along
        v_note = M("vertices move only through the deformation field θ<sub>t</sub>;\nthe Gaussian rides along (same b)",
                   17, WARN_TXT).move_to(q_note)
        self.play(FadeOut(a_note), FadeOut(frame_box), FadeOut(frame_lbl), FadeOut(side_m),
                  FadeIn(v_note), Indicate(name_m[5], color=WARN), run_time=0.8)
        moves = [Arrow(dots["v2"].get_center(), dots["v2"].get_center() + np.array([0.7, 0.75, 0]), buff=0.1,
                       color=WARN, stroke_width=3, tip_length=0.15),
                 Arrow(dots["v3"].get_center(), dots["v3"].get_center() + np.array([0.6, -0.35, 0]), buff=0.1,
                       color=WARN, stroke_width=3, tip_length=0.15)]
        self.play(*[GrowArrow(a) for a in moves], run_time=0.6)
        self.play(dots["v2"].animate.shift([0.7, 0.75, 0]), dots["v3"].animate.shift([0.6, -0.35, 0]),
                  FadeOut(VGroup(*moves)), run_time=1.6)
        self.play(dots["v2"].animate.shift([-0.3, -0.5, 0]), dots["v1"].animate.shift([0.3, 0.3, 0]), run_time=1.2)
        self.play(FadeIn(bs[5], shift=LEFT * 0.15), run_time=0.6)

        # ---- the point
        final = M("Gaussians can't roam away to explain the image:\n<b>the mesh itself has to deform.</b>", 20, FG)
        final.move_to([-3.6, -2.2, 0])
        self.play(FadeOut(v_note), FadeIn(final), run_time=0.8)
        self.wait(3)


# ============================================================================ scene 2


class S2_GradientFlow(Scene):
    """Forward pass, then where the photometric (and ARAP) gradient flows and where it stops."""

    def construct(self):
        def node(markup, kind, pos, w=2.45, size=18, lock=False):
            t = M(markup, size=size, color=TXT[kind])
            h = max(0.6, t.height + 0.26)
            box = RoundedRectangle(width=w, height=h, corner_radius=0.1).set_fill(SOFT[kind], 1)
            box.set_stroke(EDGE[kind], 2.4 if kind != "der" else 1.5)
            g = VGroup(box, t).move_to(p3(pos))
            if lock:
                badge = VGroup(Circle(radius=0.16).set_fill(WHITE, 1).set_stroke(EDGE[kind], 1.5),
                               lock_icon(TXT[kind], 0.17))
                g.add(badge.move_to(box.get_corner(UR) + np.array([-0.02, -0.02, 0])))
            return g

        c0, c1, c2, c3, c4 = -5.75, -2.6, 0.3, 3.05, 5.7
        N = dict(
            s=node("tangent scales  s<sub>‖</sub>", "con", (c1, 3.25)),
            mesh=node("CT mesh  T<sub>CT</sub>·M\n(registered once)", "fix", (c0, 2.0), lock=True),
            delta=node("anchor offsets  δ<sub>k</sub>", "con", (c0, 0.85)),
            V=node("vertices\nv<sub>t</sub> = θ<sub>t</sub>(T<sub>CT</sub>·M)", "der", (c1, 1.55)),
            Sig=node("covariance  Σ = R S S<sup>T</sup> R<sup>T</sup>\nR = face normal,  s<sub>⊥</sub> fixed", "der",
                     (c2, 2.5), w=2.9, size=17),
            mu=node("means\nμ = Σ<sub>k</sub> b<sub>k</sub> v<sub>k</sub>", "der", (c2, 0.75)),
            arap=node("E<sub>ARAP</sub>(v<sub>t</sub>)", "loss", (c1, 0.25), w=2.1, size=19),
            b=node("barycentric  b", "con", (c1, -0.85)),
            ac=node("opacity  α,  colour  c", "free", (c1, -1.7)),
            P=node("camera pose  P<sub>t</sub>\n(tracker)", "fix", (c1, -2.6), lock=True),
            rast=node("render  Î<sub>t</sub>\nsplat + α-blend", "der", (c3, 0.0), w=2.2),
            E=node("E<sub>photo</sub> = ‖ I<sub>t</sub> − Î<sub>t</sub> ‖", "loss", (c4, 0.0), w=2.45, size=19),
            I=node("video frame  I<sub>t</sub>\n(mono RGB)", "fix", (c4, -1.5), w=2.3, lock=True),
        )
        arap_note = M("+ neighbour &amp; invisible-area penalties", 14, GRAD).next_to(N["arap"], DOWN, buff=0.06)

        def anchor(n, side):
            return N[n][0].get_critical_point(side)

        spec = [  # (from, to, from_side, to_side)
            ("mesh", "V", RIGHT, LEFT), ("delta", "V", RIGHT, LEFT),
            ("V", "Sig", UR, LEFT), ("s", "Sig", RIGHT, LEFT),
            ("V", "mu", RIGHT, LEFT), ("b", "mu", RIGHT, DOWN),
            ("V", "arap", DOWN, UP),
            ("Sig", "rast", RIGHT, UP), ("mu", "rast", RIGHT, LEFT), ("ac", "rast", RIGHT, DOWN + LEFT * 0.4),
            ("P", "rast", RIGHT, DOWN),
            ("rast", "E", RIGHT, LEFT), ("I", "E", UP, DOWN),
        ]
        edges = {}
        for a, b_, sa_, sb_ in spec:
            s, e = anchor(a, sa_), anchor(b_, sb_)
            edges[(a, b_)] = Arrow(s, e, buff=0.05, stroke_width=2.4, color=FG, tip_length=0.14,
                                   max_tip_length_to_length_ratio=0.15)

        # ---------------------------------------------------------- build up + forward pass
        legend = VGroup(chip("learned freely", "free", size=15), chip("learned, constrained", "con", size=15),
                        chip("fixed / given", "fix", size=15, lock=True), chip("derived", "der", size=15),
                        chip("loss", "loss", size=15)).arrange(RIGHT, buff=0.15)
        legend.move_to([0, 3.62, 0]).to_edge(RIGHT, buff=0.15)
        self.play(LaggedStart(*[FadeIn(N[k]) for k in ("mesh", "delta", "s", "b", "ac", "P", "I")], lag_ratio=0.12),
                  FadeIn(legend), run_time=1.6)
        fwd_cap = caption("forward: deform the CT mesh → place Gaussians on it → render with the tracked pose → compare",
                          y=-3.4, size=19, color=MUTED)
        self.play(FadeIn(fwd_cap), run_time=0.5)
        waves = [
            [("mesh", "V"), ("delta", "V")],
            [("V", "Sig"), ("s", "Sig"), ("V", "mu"), ("b", "mu"), ("V", "arap")],
            [("Sig", "rast"), ("mu", "rast"), ("ac", "rast"), ("P", "rast")],
            [("rast", "E"), ("I", "E")],
        ]
        targets = [["V"], ["Sig", "mu", "arap"], ["rast"], ["E"]]
        for w, tg in zip(waves, targets):
            self.play(*[GrowArrow(edges[e]) for e in w], run_time=0.8)
            self.play(*[FadeIn(N[k], scale=0.95) for k in tg], *([FadeIn(arap_note)] if "arap" in tg else []),
                      run_time=0.6)
        self.wait(1.5)

        # ---------------------------------------------------------- backward pass
        bwd_cap = caption("backward: ∂E/∂(·) flows back along every edge, until it hits something fixed",
                          y=-3.4, size=19, color=GRAD)
        self.play(*[e.animate.set_stroke(opacity=0.22).set_fill(opacity=0.22) for e in edges.values()],
                  Transform(fwd_cap, bwd_cap), run_time=0.8)

        def back(a, b_):
            fe = edges[(a, b_)]
            return Arrow(fe.get_end(), fe.get_start(), buff=0.0, stroke_width=4, color=GRAD, tip_length=0.17,
                         max_tip_length_to_length_ratio=0.2)

        def blocked(a, b_):
            fe = edges[(a, b_)]
            s, e = fe.get_end(), fe.get_start()
            mid = s + 0.55 * (e - s)
            ar = Arrow(s, mid, buff=0.0, stroke_width=4, color=GRAD, tip_length=0.0001,
                       max_tip_length_to_length_ratio=0.01)
            bar = Line(mid + 0.13 * normalize(rotate_vector(e - s, PI / 2)), mid - 0.13 * normalize(rotate_vector(e - s, PI / 2)))
            return VGroup(ar, bar.set_stroke(GRAD, 5))

        def updated(k):
            box = N[k][0]
            badge = VGroup(Circle(radius=0.15).set_fill(GRAD, 1).set_stroke(WHITE, 1.5), M("∇", 15, WHITE))
            return badge.move_to(box.get_corner(UL) + np.array([0.02, -0.02, 0]))

        # wave 1: from the two losses
        self.play(GrowArrow(back("rast", "E")), Create(blocked("I", "E")), GrowArrow(back("V", "arap")), run_time=0.9)
        self.play(Indicate(N["I"], color=MUTED, scale_factor=1.05), run_time=0.7)
        self.wait(0.4)
        # wave 2: renderer -> means, covariances, appearance; pose is fixed
        self.play(GrowArrow(back("mu", "rast")), GrowArrow(back("Sig", "rast")), GrowArrow(back("ac", "rast")),
                  Create(blocked("P", "rast")), run_time=0.9)
        self.play(FadeIn(updated("ac"), scale=0.5), Indicate(N["P"], color=MUTED, scale_factor=1.05), run_time=0.8)
        self.wait(0.4)
        # wave 3: means -> vertices + barycentrics; covariance -> tangent scales + vertices (via the face normal)
        self.play(GrowArrow(back("V", "mu")), GrowArrow(back("b", "mu")), GrowArrow(back("s", "Sig")),
                  GrowArrow(back("V", "Sig")), run_time=0.9)
        self.play(FadeIn(updated("b"), scale=0.5), FadeIn(updated("s"), scale=0.5), run_time=0.7)
        self.wait(0.4)
        # wave 4: vertices -> anchor offsets; the CT mesh / registration is fixed
        self.play(GrowArrow(back("delta", "V")), Create(blocked("mesh", "V")), run_time=0.9)
        self.play(FadeIn(updated("delta"), scale=0.5), Indicate(N["mesh"], color=MUTED, scale_factor=1.05), run_time=0.8)
        self.wait(1.0)

        summary = VGroup(
            M("<b>changed by backprop:</b>  δ<sub>k</sub> (→ every vertex → every Gaussian),  b,  s<sub>‖</sub>,  α,  c",
              19, GRAD),
            M("<b>never changed:</b>  P<sub>t</sub>,  T<sub>CT</sub>,  CT mesh topology,  the orientation rule,  s<sub>⊥</sub>",
              19, MUTED),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([0, -3.45, 0])
        self.play(FadeOut(fwd_cap), FadeIn(summary), run_time=0.8)
        self.wait(4.5)


# ============================================================================ scene 3


class S3_MonoRay(Scene):
    """Why a mono video needs the mesh: dE/dmu is perpendicular to the viewing ray."""

    C = np.array([0.0, 2.35, 0.0])          # projection centre; the camera looks straight down
    PANEL_Y, PANEL_W, K = 3.45, 6.4, 3.2    # 1-D image panel, magnified: panel_x = K * x / z

    def u_of(self, X):
        X = np.asarray(X)
        return (X[0] - self.C[0]) / (self.C[1] - X[1])

    def px(self, X):
        return self.K * self.u_of(X)

    def footprint(self, X, s, color=None, outline=False, h=0.24):
        """Projection of a Gaussian with tangential half-size s at X onto the image panel."""
        z = self.C[1] - np.asarray(X)[1]
        r = Rectangle(width=max(2 * self.K * s / z, 0.04), height=h).move_to([self.px(X), self.PANEL_Y, 0])
        if outline:
            return r.set_fill(opacity=0).set_stroke(GRAD, 3)
        return r.set_fill(color, 1).set_stroke(width=0)

    def perp_toward(self, X, du_sign):
        """Unit vector perpendicular to the ray through X that moves its image in direction du_sign."""
        r = normalize(np.asarray(X) - self.C)
        p = np.array([-r[1], r[0], 0])
        if np.sign(self.u_of(X + 1e-3 * p) - self.u_of(X)) != np.sign(du_sign):
            p = -p
        return p

    def construct(self):
        C = self.C
        cam = camera_icon(C, 1.2)
        panel = Rectangle(width=self.PANEL_W, height=0.34).set_fill(ManimColor("#f3f4f6"), 1).set_stroke(MUTED, 1.2)
        panel.move_to([0, self.PANEL_Y, 0])
        panel_lbl = M("what the camera sees\n(1-D image)", 16, MUTED).next_to(panel, LEFT, buff=0.25)
        fr = VGroup(*[DashedLine(C, C + 4.7 * np.array([s * self.PANEL_W / 2 / self.K, -1, 0]), dash_length=0.1)
                      .set_stroke(MUTED, 1.2, opacity=0.6) for s in (-1, 1)])
        self.play(FadeIn(cam), FadeIn(panel), FadeIn(panel_lbl), Create(fr), run_time=1.2)

        # ------------------------------------------------- beat 1: depth along the ray is invisible
        A = p3((1.9, -0.9))
        ray = Line(C, C + 1.35 * (A - C)).set_stroke(FG, 1.5, opacity=0.7)
        s_along = ValueTracker(1.0)
        ang = angle_of_vector(A - C) + PI / 2

        def g_on_ray():
            k = s_along.get_value()
            return gauss_blob(C + k * (A - C), 0.55 * k, 0.17 * k, ang, TISSUE[0], 0.95)

        g1 = always_redraw(g_on_ray)
        fp1 = always_redraw(lambda: self.footprint(C + s_along.get_value() * (A - C), 0.55 * s_along.get_value(),
                                                   TISSUE[0]))
        cap1 = caption("Slide a Gaussian along its viewing ray (and rescale it): <b>the image does not change.</b>", -3.3, 21)
        self.play(Create(ray), FadeIn(g1), FadeIn(fp1), run_time=1.0)
        self.play(FadeIn(cap1), run_time=0.5)
        self.play(s_along.animate.set_value(0.45), run_time=1.8)
        self.play(s_along.animate.set_value(1.3), run_time=2.0)
        self.play(s_along.animate.set_value(1.0), run_time=1.0)
        self.wait(0.6)

        # ------------------------------------------------- beat 2: the gradient is perpendicular to the ray
        obs = self.footprint(A, 0.55, outline=True).shift(LEFT * 0.55)
        key = VGroup(
            VGroup(Rectangle(width=0.32, height=0.2).set_fill(TISSUE[0], 1).set_stroke(width=0), M("rendered", 15)),
            VGroup(Rectangle(width=0.32, height=0.2).set_fill(opacity=0).set_stroke(GRAD, 2.5), M("observed (video)", 15, GRAD)),
        )
        for k in key:
            k.arrange(RIGHT, buff=0.1)
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(panel, RIGHT, buff=0.3)
        obs_lbl, rnd_lbl = key[1], key[0]
        p = self.perp_toward(A, -1)
        garrow = Arrow(A, A + 1.15 * p, buff=0, color=GRAD, stroke_width=5, tip_length=0.2)
        glbl = M("−∂E/∂μ", 20, GRAD).next_to(garrow.get_end(), DOWN, buff=0.1)
        ra = RightAngle(Line(A, A + 0.6 * normalize(C - A)), Line(A, A + 0.6 * p), length=0.2, quadrant=(1, 1))
        ra.set_stroke(GRAD, 2)
        s = T.summary(T.compute_all(CACHE))
        cap2 = VGroup(
            M("The loss gradient on a mean is <b>perpendicular to its ray</b>: one image can only push it sideways.", 21),
            M(f"(true for any pinhole camera;  toy model: median |cos(∂E/∂μ, ray)| = {s['cos_grad_ray']:.3f})", 16, MUTED),
        ).arrange(DOWN, buff=0.1).move_to([0, -3.35, 0])
        self.play(FadeIn(obs), FadeIn(obs_lbl), FadeIn(rnd_lbl), run_time=0.7)
        self.play(GrowArrow(garrow), FadeIn(glbl), Create(ra), FadeOut(cap1), FadeIn(cap2), run_time=1.0)
        self.wait(3.2)

        # ------------------------------------------------- beat 3: free Gaussians vs a rigged face
        self.play(*[FadeOut(m) for m in (g1, fp1, ray, garrow, glbl, ra, obs, cap2)], run_time=0.7)
        vL, vR = p3((-1.9, 0.15)), p3((1.9, 0.15))
        drop = np.array([0, -1.5, 0])              # the tissue really moved away from the camera
        ts, SG = (0.12, 0.5, 0.88), 0.36
        G = [(1 - t) * vL + t * vR for t in ts]
        Gt = [g + drop for g in G]
        cols = [TISSUE[0], TISSUE[3], TISSUE[2]]
        true_face = DashedLine(vL + drop, vR + drop, dash_length=0.12).set_stroke(MUTED, 3)
        true_lbl = M("true tissue position (unknown)", 16, MUTED).next_to(true_face, DOWN, buff=0.12)
        face = Line(vL, vR).set_stroke(FG, 3)
        vdots = VGroup(Dot(vL, radius=0.07, color=FG), Dot(vR, radius=0.07, color=FG))
        blobs = VGroup(*[gauss_blob(g, SG, 0.09, 0, c, 0.95) for g, c in zip(G, cols)])
        rays = VGroup(*[DashedLine(C, gt, dash_length=0.08).set_stroke(FG, 1.1, opacity=0.5) for gt in Gt])
        fps = VGroup(*[self.footprint(g, SG, c) for g, c in zip(G, cols)])
        obs_fps = VGroup(*[self.footprint(gt, SG, outline=True) for gt in Gt])
        cap3 = caption("The tissue moved <b>away</b> from the camera: in the image the patch only looks smaller.", -3.3, 21)
        self.play(Create(face), FadeIn(vdots), FadeIn(blobs), FadeIn(fps), run_time=1.0)
        self.play(Create(true_face), FadeIn(true_lbl), FadeIn(obs_fps), Create(rays), FadeIn(cap3), run_time=1.2)
        self.wait(1.0)

        def grad_arrow(i, L=0.8):
            du = self.u_of(Gt[i]) - self.u_of(G[i])
            return Arrow(G[i], G[i] + L * self.perp_toward(G[i], du), buff=0, color=GRAD, stroke_width=5,
                         tip_length=0.18)

        garrows = VGroup(grad_arrow(0), grad_arrow(2))
        zero = M("0", 16, GRAD).next_to(G[1], UP, buff=0.2)
        cap3b = caption("Each Gaussian is pushed <b>perpendicular to its own ray</b> (the middle one sees no change).",
                        -3.3, 21)
        self.play(*[GrowArrow(a) for a in garrows], FadeIn(zero), FadeOut(cap3), FadeIn(cap3b), run_time=0.9)
        self.wait(2.0)

        # (a) free Gaussians: slide perpendicular to their rays and shrink -> image matches, depth wrong
        def slide_target(i):
            g, gt = G[i], Gt[i]
            if abs(self.u_of(gt) - self.u_of(g)) < 1e-6:
                return g
            pp = self.perp_toward(g, self.u_of(gt) - self.u_of(g))
            dd = normalize(gt - C)  # observed ray: solve g + a pp = C + b dd
            a, _ = np.linalg.solve(np.array([[pp[0], -dd[0]], [pp[1], -dd[1]]]), (C - g)[:2])
            return g + a * pp

        free_pos = [slide_target(i) for i in range(3)]
        shrink = [(C[1] - f[1]) / (C[1] - gt[1]) for f, gt in zip(free_pos, Gt)]
        free_blobs = VGroup(*[gauss_blob(f, SG * k, 0.09, 0, c, 0.95) for f, k, c in zip(free_pos, shrink, cols)])
        free_fps = VGroup(*[self.footprint(f, SG * k, c) for f, k, c in zip(free_pos, shrink, cols)])
        tag_free = M("<b>free Gaussians (3DGS)</b>", 21, ACCENT).move_to([-4.7, 0.9, 0])
        cap4 = caption("Free: they slide sideways and shrink. <b>The image matches; the depth is still wrong.</b>", -3.3, 21)
        self.play(FadeIn(tag_free), FadeOut(cap3b), run_time=0.5)
        self.play(Transform(blobs, free_blobs), Transform(fps, free_fps), FadeOut(garrows), FadeOut(zero),
                  FadeOut(face), FadeOut(vdots), run_time=1.8)
        errs = VGroup(*[DoubleArrow(f, gt, buff=0.08, color=MUTED, stroke_width=2.5, tip_length=0.14)
                        for f, gt in zip(free_pos, Gt)])
        self.play(FadeIn(errs), FadeIn(cap4), run_time=0.7)
        self.wait(2.8)

        # (b) rigged to a CT face of known size: the pushes add up to a move in depth
        tag_rig = M("<b>rigged to a CT face (BridgeSplat)</b>", 21, WARN_TXT).move_to(tag_free, aligned_edge=LEFT)
        self.play(FadeOut(errs), FadeOut(cap4),
                  Transform(blobs, VGroup(*[gauss_blob(g, SG, 0.09, 0, c, 0.95) for g, c in zip(G, cols)])),
                  Transform(fps, VGroup(*[self.footprint(g, SG, c) for g, c in zip(G, cols)])),
                  FadeIn(face), FadeIn(vdots), Transform(tag_free, tag_rig), run_time=1.0)
        garrows = VGroup(grad_arrow(0, 0.7), grad_arrow(2, 0.7))
        self.play(*[GrowArrow(a) for a in garrows], run_time=0.6)
        gv = []                                     # chain rule: weights (1-t) and t
        for vi in range(2):
            tot = np.zeros(3)
            for i in (0, 2):
                w = (1 - ts[i]) if vi == 0 else ts[i]
                tot += w * self.perp_toward(G[i], self.u_of(Gt[i]) - self.u_of(G[i]))
            gv.append(1.3 * tot)
        verts = (vL, vR)
        varrows = VGroup(*[Arrow(v, v + g, buff=0, color=GRAD, stroke_width=5, tip_length=0.18) for v, g in zip(verts, gv)])
        horiz = VGroup(*[DashedLine(v, v + np.array([g[0], 0, 0]), dash_length=0.06).set_stroke(GRAD, 3)
                         for v, g in zip(verts, gv)])
        vert = VGroup(*[Arrow(v, v + np.array([0, g[1], 0]), buff=0, color=GRAD, stroke_width=6, tip_length=0.2)
                        for v, g in zip(verts, gv)])
        crosses = VGroup(*[M("✕", 20, GRAD).move_to(h.get_center() + 0.25 * UP) for h in horiz])
        cap5 = VGroup(
            M("Rigged: the pushes collect on the vertices. The face can't shrink (its size comes from the CT,", 20),
            M("ARAP keeps it), so the inward parts cancel and <b>the pushes away from the camera add up.</b>", 20),
        ).arrange(DOWN, buff=0.1).move_to([0, -3.35, 0])
        self.play(ReplacementTransform(garrows, varrows), FadeIn(cap5), run_time=1.0)
        self.wait(1.0)
        self.play(ReplacementTransform(varrows, VGroup(horiz, vert)), run_time=0.8)
        self.play(FadeIn(crosses), horiz.animate.set_stroke(opacity=0.35), run_time=0.6)
        self.wait(1.0)
        self.play(VGroup(face, vdots, blobs).animate.shift(drop), FadeOut(vert), FadeOut(horiz), FadeOut(crosses),
                  Transform(fps, VGroup(*[self.footprint(gt, SG, c) for gt, c in zip(Gt, cols)])), run_time=2.0)
        cap6 = VGroup(
            M("<b>'Smaller in the image' can only mean 'farther away'</b>: the mesh moves in depth.", 21),
            M("The cue is weak: it scales with face size / distance. A depth prior (DA3, stereo) would make it strong.",
              16, MUTED),
        ).arrange(DOWN, buff=0.1).move_to([0, -3.35, 0])
        self.play(FadeOut(cap5), FadeIn(cap6), Flash(face.get_center(), color=WARN, flash_radius=0.6), run_time=1.0)
        self.wait(4)


# ============================================================================ scene 4


class S4_MonoTracking(Scene):
    """Toy 2-D BridgeSplat optimised for real on a mono video of a tool pressing tissue."""

    OFF = np.array([0.0, 0.05, 0.0])
    STRIP_W, STRIP_H = 7.2, 0.34

    def w2s(self, P):
        P = np.atleast_2d(P)
        return np.c_[P[:, 0], P[:, 1], np.zeros(len(P))] + self.OFF

    def strip(self, img):
        arr = (np.clip(img, 0, 1) * 255).astype(np.uint8)
        rgba = np.concatenate([arr, np.full((arr.shape[0], 1), 255, np.uint8)], 1)
        return np.repeat(rgba[None], 2, 0)

    def residual(self, a, b, gain=6.0):
        r = np.clip(np.abs(a - b).sum(1) * gain, 0, 1)[:, None]
        red = np.array(GRAD.to_rgb())[None]
        return np.ones((len(r), 3)) * (1 - r) + red * r

    def make_strip(self, img, y):
        m = ImageMobject(self.strip(img))
        m.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        m.stretch_to_fit_width(self.STRIP_W).stretch_to_fit_height(self.STRIP_H).move_to([0, y, 0])
        return m

    def gaussians(self, mu, tan, s, alpha=1.0, outline=None):
        g = VGroup()
        for i in range(T.N_G):
            e = Ellipse(width=max(2 * 1.5 * s[i], 0.02), height=0.085)
            e.set_fill(ManimColor.from_rgb(T.G_COLOR[i]), 0.95 * alpha)
            e.set_stroke(outline or WHITE, 2.0 if outline else 0, opacity=alpha)
            e.rotate(angle_of_vector(p3(tan[i]))).move_to(self.w2s(mu[i])[0])
            g.add(e)
        return g

    def construct(self):
        d = T.compute_all(CACHE)
        summ = T.summary(d)
        nf, it = int(d["n_frames"]), int(d["iters"])
        per = it + 1
        Vt0 = T.V0

        # ---------------------------------------------------------- camera, frustum, strips
        cam_c = self.w2s(T.CAM)[0]
        cam = camera_icon(cam_c, 1.0)
        zfar = 4.45
        frustum = VGroup(*[DashedLine(cam_c, cam_c + np.array([s * zfar * T.U_HALF / T.FOCAL, -zfar, 0]),
                                      dash_length=0.1).set_stroke(MUTED, 1.5, opacity=0.7) for s in (-1, 1)])
        pose_lbl = VGroup(lock_icon(MUTED, 0.2), M("pose P<sub>t</sub> from the tracker", 17, MUTED)).arrange(RIGHT, buff=0.1)
        pose_lbl.next_to(cam, RIGHT, buff=0.35).shift(DOWN * 0.05)
        ys = (3.55, 3.1, 2.65)
        labels = VGroup(M("video frame  I<sub>t</sub>", 18), M("render  Î<sub>t</sub>", 18),
                        M("| I<sub>t</sub> − Î<sub>t</sub> |", 18, GRAD))
        for l, y in zip(labels, ys):
            l.move_to([-self.STRIP_W / 2 - 0.2, y, 0], aligned_edge=RIGHT)
        frames = VGroup(*[Rectangle(width=self.STRIP_W, height=self.STRIP_H).set_stroke(MUTED, 1).move_to([0, y, 0])
                          for y in ys])

        self.play(FadeIn(cam), Create(frustum), FadeIn(pose_lbl), run_time=1.0)

        # ---------------------------------------------------------- the CT template with its Gaussians
        tan0, s0 = T.gauss_frames(Vt0)

        def mesh_line(V, color=FG, width=2.2):
            return VMobject().set_points_as_corners(self.w2s(V)).set_stroke(color, width)

        def vdots(V):
            g = VGroup(*[Dot(self.w2s(v)[0], radius=0.035, color=FG) for v in V])
            for k in T.ANCHORS:
                g.add(Square(0.13).rotate(PI / 4).set_fill(WARN, 1).set_stroke(WHITE, 1).move_to(self.w2s(V[k])[0]))
            return g

        tmpl_lbl = M("CT mesh after registration = template", 18, FG).move_to([-4.6, -1.0, 0])
        g0 = self.gaussians(T.gauss_means(Vt0), tan0, s0)
        mesh0, dots0 = mesh_line(Vt0), vdots(Vt0)
        self.play(Create(mesh0), FadeIn(dots0), FadeIn(tmpl_lbl), run_time=1.0)
        self.play(FadeIn(g0), run_time=0.8)
        self.bring_to_front(mesh0, dots0)

        img0 = d["targets"][0]
        s_obs, s_ren, s_res = (self.make_strip(img0, ys[0]), self.make_strip(img0, ys[1]),
                               self.make_strip(self.residual(img0, img0), ys[2]))
        self.play(FadeIn(labels), FadeIn(s_obs), FadeIn(s_ren), FadeIn(s_res), FadeIn(frames), run_time=1.0)

        legend = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.4).set_stroke(FG, 2.2), M("mesh", 16)).arrange(RIGHT, buff=0.1),
            VGroup(Square(0.13).rotate(PI / 4).set_fill(WARN, 1).set_stroke(width=0),
                   M("anchor: learned offset δ<sub>k</sub>", 16, WARN_TXT)).arrange(RIGHT, buff=0.1),
            VGroup(DashedLine(ORIGIN, RIGHT * 0.4, dash_length=0.07).set_stroke(MUTED, 2.5),
                   M("true surface (unknown to the method)", 16, MUTED)).arrange(RIGHT, buff=0.1),
        ).arrange(RIGHT, buff=0.45).move_to([0, -3.7, 0])
        self.play(FadeIn(legend), FadeOut(tmpl_lbl), run_time=0.6)

        # ---------------------------------------------------------- frame 1: the tool presses
        TOOL_DIR, TOOL_LEN = normalize(np.array([0.55, 1.0, 0])), 2.6

        def tool(V_gt):
            tip = self.w2s(V_gt[np.argmin(np.abs(T.V0[:, 0] - T.PRESS_X))])[0] + np.array([0, 0.1, 0])
            rod = Line(tip, tip + TOOL_LEN * TOOL_DIR).set_stroke(ManimColor("#9aa3ad"), 14, opacity=0.75)
            return VGroup(rod, Dot(tip, radius=0.07, color=ManimColor("#9aa3ad")))

        gt_k = ValueTracker(0)

        def gt_line():
            f = int(round(gt_k.get_value()))
            return DashedVMobject(mesh_line(d["gt_V"][f], MUTED, 2.5), num_dashes=90)

        gt_m = always_redraw(gt_line)
        tool_m = always_redraw(lambda: tool(d["gt_V"][int(round(gt_k.get_value()))]))
        tool_top = self.w2s(d["gt_V"][0][np.argmin(np.abs(T.V0[:, 0] - T.PRESS_X))])[0] + TOOL_LEN * TOOL_DIR
        tool_lbl = M("tool\n(masked out of I<sub>t</sub>)", 16, MUTED).next_to(tool_top, RIGHT, buff=0.15)
        self.add(gt_m)
        self.play(FadeIn(tool_m), FadeIn(tool_lbl), run_time=0.8)
        self.play(gt_k.animate.set_value(1), run_time=0.6)
        s_obs.pixel_array = self.strip(d["targets"][1])
        s_res.pixel_array = self.strip(self.residual(d["targets"][1], img0))
        cap = caption("Frame 1: the video changed, the render did not yet. Residual → photometric loss.", -3.05, 20)
        hl = SurroundingRectangle(frames[2], buff=0.05, color=GRAD, stroke_width=3)
        self.play(FadeIn(cap), Create(hl), run_time=1.0)
        self.play(FadeOut(hl), run_time=0.5)
        self.wait(1.0)

        # ---------------------------------------------------------- the chain rule, drawn
        mu0 = T.gauss_means(Vt0)
        gmu = -d["g_mu"]
        gmax = np.linalg.norm(gmu, axis=1).max()
        sel = [i for i in range(T.N_G) if np.linalg.norm(gmu[i]) > 0.1 * gmax]
        arrows_mu = VGroup(*[Arrow(self.w2s(mu0[i])[0], self.w2s(mu0[i] + 1.3 * gmu[i] / gmax)[0], buff=0,
                                   color=GRAD, stroke_width=3.5, tip_length=0.12, max_tip_length_to_length_ratio=0.35)
                             for i in sel])
        top = sorted(sel, key=lambda i: -np.linalg.norm(gmu[i]))
        show_rays = [top[0], top[2], top[4]]
        rays = VGroup(*[Line(cam_c, self.w2s(mu0[i])[0]).set_stroke(FG, 1.2, opacity=0.55) for i in show_rays])
        cap_a = caption("−∂E/∂μ on each Gaussian: always <b>perpendicular to its own ray</b>", -3.05, 20)
        self.play(FadeOut(cap), FadeIn(cap_a), Create(rays), LaggedStart(*[GrowArrow(a) for a in arrows_mu],
                                                                           lag_ratio=0.03), run_time=1.6)
        self.wait(1.8)
        gV = -d["g_V"]
        gvmax = np.linalg.norm(gV, axis=1).max()
        vsel = [k for k in range(T.N_VERT) if np.linalg.norm(gV[k]) > 0.05 * gvmax]
        arrows_v = VGroup(*[Arrow(self.w2s(Vt0[k])[0], self.w2s(Vt0[k] + 0.9 * gV[k] / gvmax)[0], buff=0, color=GRAD,
                                  stroke_width=4.5, tip_length=0.14, max_tip_length_to_length_ratio=0.35) for k in vsel])
        cap_b = caption("chain rule through μ = Σ b<sub>k</sub> v<sub>k</sub>: the pushes collect on the <b>vertices</b>",
                        -3.05, 20)
        self.play(FadeOut(cap_a), FadeIn(cap_b), ReplacementTransform(arrows_mu, arrows_v), FadeOut(rays), run_time=1.3)
        self.wait(1.5)
        gA = -d["g_anchor"]
        gamax = np.linalg.norm(gA, axis=1).max()
        arrows_a = VGroup(*[Arrow(self.w2s(Vt0[k])[0], self.w2s(Vt0[k] + 1.1 * gA[j] / gamax)[0], buff=0, color=GRAD,
                                  stroke_width=6, tip_length=0.18, max_tip_length_to_length_ratio=0.4)
                            for j, k in enumerate(T.ANCHORS) if np.linalg.norm(gA[j]) > 0.04 * gamax])
        cap_c = caption("… and through θ<sub>t</sub> on the <b>anchor offsets δ<sub>k</sub></b>: the only geometry that is learned",
                        -3.05, 20)
        self.play(FadeOut(cap_b), FadeIn(cap_c), ReplacementTransform(arrows_v, arrows_a), run_time=1.3)
        self.wait(1.8)
        self.play(FadeOut(arrows_a), FadeOut(cap_c), run_time=0.6)

        # ---------------------------------------------------------- play the tracking (BridgeSplat)
        k = ValueTracker(0)
        n_br = len(d["br_V"])

        def idx():
            return int(np.clip(round(k.get_value()), 0, n_br - 1))

        def frame_of(i):
            return 1 + i // per

        def rig_scene():
            V = d["br_V"][idx()]
            tan, s = T.gauss_frames(V)
            return VGroup(self.gaussians(T.gauss_means(V), tan, s), mesh_line(V), vdots(V))

        self.remove(g0, mesh0, dots0)
        rig_m = always_redraw(rig_scene)
        self.add(rig_m)

        def upd_strips(_):
            i = idx()
            f = frame_of(i)
            s_obs.pixel_array = self.strip(d["targets"][f])
            s_ren.pixel_array = self.strip(d["br_img"][i])
            s_res.pixel_array = self.strip(self.residual(d["targets"][f], d["br_img"][i]))
            gt_k.set_value(f)

        dummy = Mobject().add_updater(upd_strips)
        self.add(dummy)
        info = always_redraw(lambda: VGroup(
            M(f"frame {frame_of(idx())} / {nf}", 19),
            M(f"step {idx() % per:2d} / {it}", 16, MUTED),
            M(f"E<sub>photo</sub> = {d['br_loss'][idx()]:.5f}", 17, GRAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([5.75, 3.15, 0]))
        cap_d = caption("Each frame: a few gradient steps on δ<sub>k</sub>, warm-started from the last frame", -3.05, 20)
        self.play(FadeIn(info), FadeIn(cap_d), run_time=0.6)
        self.play(k.animate.set_value(n_br - 1), run_time=14, rate_func=linear)
        self.wait(0.6)
        cap_e = caption(f"Image matched. The dent is recovered, but only to <b>{summ['dent_rigged'] / summ['dent_true']:.0%}</b>"
                        " of its true depth.", -3.05, 20)
        self.play(FadeOut(cap_d), FadeIn(cap_e), run_time=0.6)
        self.wait(2.2)

        # ---------------------------------------------------------- same video, free 3DGS-style Gaussians
        dummy.clear_updaters()
        self.remove(dummy, rig_m)
        V_end = d["br_V"][-1]
        tan_e, s_e = T.gauss_frames(V_end)
        rig_static = VGroup(self.gaussians(T.gauss_means(V_end), tan_e, s_e), mesh_line(V_end), vdots(V_end))
        self.add(rig_static)
        cap_f = caption("Same video, <b>free Gaussians</b> (3DGS-style: means and scales unconstrained, no mesh)", -3.05, 20)
        free_tag = M("free Gaussians", 18, ACCENT).move_to([-4.9, -0.75, 0])
        self.play(FadeOut(cap_e), FadeIn(cap_f), rig_static.animate.set_opacity(0.0), FadeIn(free_tag), run_time=0.9)
        self.remove(rig_static)

        kf = ValueTracker(0)
        n_fr = len(d["fr_mu"])

        def fidx():
            return int(np.clip(round(kf.get_value()), 0, n_fr - 1))

        free_m = always_redraw(lambda: self.gaussians(d["fr_mu"][fidx()], tan0, d["fr_s"][fidx()], outline=ACCENT))

        def upd_free(_):
            i = fidx()
            f = frame_of(i)
            s_obs.pixel_array = self.strip(d["targets"][f])
            s_ren.pixel_array = self.strip(d["fr_img"][i])
            s_res.pixel_array = self.strip(self.residual(d["targets"][f], d["fr_img"][i]))

        dummy2 = Mobject().add_updater(upd_free)
        gt_k.set_value(0)
        self.remove(info)
        info2 = always_redraw(lambda: VGroup(
            M(f"frame {frame_of(fidx())} / {nf}", 19),
            M(f"step {fidx() % per:2d} / {it}", 16, MUTED),
            M(f"E<sub>photo</sub> = {d['fr_loss'][fidx()]:.5f}", 17, GRAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([5.75, 3.15, 0]))
        self.add(free_m, dummy2, info2)
        gt_follow = Mobject().add_updater(lambda _: gt_k.set_value(frame_of(fidx())))
        self.add(gt_follow)
        self.play(kf.animate.set_value(n_fr - 1), run_time=9, rate_func=linear)
        dummy2.clear_updaters()
        gt_follow.clear_updaters()
        self.remove(dummy2, gt_follow)
        self.wait(0.5)

        # ---------------------------------------------------------- side by side
        rig_back = VGroup(self.gaussians(T.gauss_means(V_end), tan_e, s_e, alpha=0.35), mesh_line(V_end, FG, 3), vdots(V_end))
        rig_tag = M("rigged mesh (BridgeSplat)", 18, FG).move_to([-4.9, -1.25, 0])
        self.play(FadeIn(rig_back), FadeIn(rig_tag), FadeOut(tool_m), FadeOut(tool_lbl), run_time=1.0)

        e0, er, ef = summ["err_start"], summ["err_rigged"], summ["err_free"]
        rows = [("", "image\nloss", "3-D error\nmean / max"),
                ("free 3DGS", f"{summ['loss_free']:.1e}", f"{ef.mean():.2f} / {ef.max():.2f}"),
                ("BridgeSplat", f"{summ['loss_rigged']:.1e}", f"{er.mean():.2f} / {er.max():.2f}"),
                ("no update", "—", f"{e0.mean():.2f} / {e0.max():.2f}")]
        tbl = VGroup()
        y = 2.05
        for r, (a, b_, c_) in enumerate(rows):
            col = [MUTED, ACCENT, FG, MUTED][r]
            row = VGroup(M(a, 15, col).move_to([3.75, 0, 0], aligned_edge=LEFT),
                         M(b_, 15, col).move_to([5.25, 0, 0]),
                         M(c_, 15, col).move_to([6.3, 0, 0]))
            row.shift(UP * y)
            y -= 0.42 if r == 0 else 0.3
            tbl.add(row)
        tbl_box = SurroundingRectangle(tbl, buff=0.12, corner_radius=0.06).set_stroke(MUTED, 1).set_fill(WHITE, 0.92)
        dent = M(f"true dent depth {-summ['dent_true']:.2f} (toy units)", 14, MUTED).next_to(tbl_box, DOWN, buff=0.08)
        self.remove(info2)
        cap_g = VGroup(
            M("<b>Same image, different geometry.</b> Only the rigged mesh turns the image residual into depth.", 20),
        ).move_to([0, -3.05, 0])
        foot = M("toy 2-D cross-section · static tracked camera · only δ<sub>k</sub> learned · real gradient descent "
                 "(toy_splat2d.py)", 14, MUTED).move_to([0, -3.7, 0])
        self.play(FadeIn(tbl_box), FadeIn(tbl), FadeIn(dent), FadeOut(cap_f), FadeIn(cap_g), FadeOut(legend),
                  FadeIn(foot), run_time=1.0)
        self.wait(5)
