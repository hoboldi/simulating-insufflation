from manim import *
import numpy as np

config.background_color = "#000000"
FONT = "Latin Modern Roman"
FG = "#EAEAEA"
MUTED = "#8A8A8A"
GAS = "#83C167"
PERI = "#83C167"
ORG = "#C0707E"       # organs inside the sac
ORGF = "#3A1F27"
RETRO = "#C0707E"
HL = "#F7D96F"


def T(s, size=30, color=FG, **kw):
    return Text(s, font=FONT, font_size=size, color=color, **kw)


class Insufflation2(Scene):
    def construct(self):
        a, b, cy, th = 4.1, 2.0, -1.3, 0.34
        L = 0.95                       # final lift of the wall top
        lift = ValueTracker(0.0)       # 0..1
        push = ValueTracker(0.0)       # 0..1 organs pushed down
        flow = ValueTracker(0.0)       # time for gas particles
        flow_on = ValueTracker(0.0)    # 0/1 visibility
        ndl = ValueTracker(0.0)        # needle insertion 0 (out) .. 1 (in)

        def P(t):
            return np.sin(t) ** 1.6

        def pt(r_off, t, l):
            x = (a - r_off) * np.cos(t) + l * L * 0.22 * np.cos(t) * np.sin(t)
            y = cy + (b - r_off) * np.sin(t) + l * L * 1.25 * P(t)
            return np.array([x, y, 0])

        def curve(r_off, l, n=90, t0=0, t1=PI):
            return [pt(r_off, t, l) for t in np.linspace(t0, t1, n)]

        def top_inner(l):
            return pt(th, PI / 2, l)[1]

        # ---------- static back half (fixed on the table)
        bo = [[a * np.cos(t), cy + b * np.sin(t), 0] for t in np.linspace(PI, 2 * PI, 90)]
        bi = [[(a - th) * np.cos(t), cy + (b - th) * np.sin(t), 0] for t in np.linspace(2 * PI, PI, 90)]
        back = Polygon(*bo, *bi, stroke_color=FG, stroke_width=2, fill_color=FG, fill_opacity=0.16)
        table = Line([-5.6, cy - b - 0.05, 0], [5.6, cy - b - 0.05, 0], color=MUTED)
        hatch = VGroup(*[Line([x, cy - b - 0.05, 0], [x - 0.2, cy - b - 0.3, 0], color=MUTED, stroke_width=1.5)
                         for x in np.arange(-5.4, 5.7, 0.35)])

        def wall():
            l = lift.get_value()
            return Polygon(*curve(0, l), *curve(th, l)[::-1], stroke_color=FG, stroke_width=2,
                           fill_color=FG, fill_opacity=0.16)

        def peri():  # parietal peritoneum = inner wall surface
            l = lift.get_value()
            return VMobject(stroke_color=PERI, stroke_width=4).set_points_smoothly(curve(th + 0.02, l, t0=0.03, t1=PI - 0.03))

        # ---------- organs
        def inner_y0(x):
            return cy + (b - th) * np.sqrt(max(0, 1 - (x / (a - th)) ** 2))

        DROP = 0.55
        tops = [(-2.4, 0.78, 0.6), (-0.82, 0.8, 0.66), (0.82, 0.8, 0.66), (2.4, 0.78, 0.6)]
        top_base = [(x, inner_y0(x) - h - 0.03 - (0.1 if abs(x) > 2 else 0), w, h) for x, w, h in tops]

        def organs():
            p = push.get_value()
            g = VGroup()
            for x, y, w, h in top_base:
                d = DROP * p * (1.0 if abs(x) < 2 else 0.75)
                hh = h * (1 - 0.18 * p)
                g.add(Ellipse(width=2 * w * (1 + 0.06 * p), height=2 * hh, stroke_color=ORG, stroke_width=2,
                              fill_color=ORGF, fill_opacity=1).move_to([x, y - d - (h - hh) * 0.6, 0]))
            for x in (-1.25, 1.25):
                g.add(Ellipse(width=1.5 * (1 + 0.08 * p), height=0.62 * (1 - 0.15 * p), stroke_color=ORG, stroke_width=2,
                              fill_color=ORGF, fill_opacity=1).move_to([x, cy - 0.55 - 0.12 * p, 0]))
            return g

        def organ_top(x):
            # approx. upper boundary of organs, for the gas region
            p = push.get_value()
            s_ = np.clip((abs(x) - 1.6) / 0.8, 0, 1)
            wgt = 1 - 0.25 * (3 * s_ ** 2 - 2 * s_ ** 3)
            return inner_y0(x) - 0.03 - DROP * p * wgt

        retro = VGroup(
            Ellipse(width=1.0, height=0.55, stroke_color=RETRO, stroke_width=2, fill_color="#3A1F27", fill_opacity=1).move_to([-2.35, cy - 1.45, 0]),
            Ellipse(width=1.0, height=0.55, stroke_color=RETRO, stroke_width=2, fill_color="#3A1F27", fill_opacity=1).move_to([2.35, cy - 1.45, 0]),
            Circle(radius=0.22, stroke_color=RETRO, stroke_width=2, fill_color="#3A1F27", fill_opacity=1).move_to([0.75, cy - 1.35, 0]),
        )
        spine = Circle(radius=0.33, color=MUTED, stroke_width=2).move_to([0, cy - b + 0.55, 0])

        def gas():
            l = lift.get_value()
            if l < 0.01:
                return VMobject()
            ts = np.linspace(0.1, PI - 0.1, 90)
            upper = [pt(th + 0.03, t, l) for t in ts]
            lower = []
            for t in ts[::-1]:
                x0 = (a - th) * np.cos(t)
                lower.append([x0, min(organ_top(x0), pt(th + 0.03, t, l)[1]), 0])
            return Polygon(*upper, *lower, stroke_width=0, fill_color=GAS, fill_opacity=0.45 * min(1, l / 0.15))

        # ---------- Veress needle at the umbilicus
        def needle():
            n = ndl.get_value()
            if n < 0.01:
                return VMobject()
            l = lift.get_value()
            skin = pt(0, PI / 2, l)[1]
            tip_in = top_inner(l) - 0.32
            tip_out = skin + 0.7
            tip = tip_out + (tip_in - tip_out) * n
            hub = tip + 1.25
            shaft = Line([0, tip, 0], [0, hub, 0], color=FG, stroke_width=5)
            grip = RoundedRectangle(width=0.34, height=0.5, corner_radius=0.06, color=FG, fill_color="#555555",
                                    fill_opacity=1, stroke_width=2).move_to([0, hub + 0.25, 0])
            hose = Line([0, hub + 0.5, 0], [0, hub + 0.95, 0], color=GAS, stroke_width=4)
            return VGroup(shaft, grip, hose).set_z_index(5)

        rng = np.random.default_rng(3)
        N = 26
        offs = rng.random(N)
        tx = rng.uniform(-2.9, 2.9, N)
        tf = rng.uniform(0.25, 0.85, N)

        def particles():
            if flow_on.get_value() < 0.5 or ndl.get_value() < 0.95:
                return VGroup()
            l = lift.get_value()
            hub = top_inner(l) - 0.32 + 1.25
            tip = top_inner(l) - 0.32
            g = VGroup()
            for i in range(N):
                p = (flow.get_value() + offs[i]) % 1.0
                if p < 0.45:
                    y = hub - (hub - tip) * (p / 0.45)
                    pos = np.array([0, y, 0])
                    op = 1
                else:
                    q = (p - 0.45) / 0.55
                    x = tx[i]
                    ytop = top_inner(l) * 0 + pt(th + 0.05, np.arccos(np.clip(x / (a - th), -1, 1)), l)[1]
                    ybot = organ_top(x)
                    y_t = ybot + (ytop - ybot) * tf[i]
                    pos = np.array([0, tip, 0]) * (1 - q) + np.array([x, y_t, 0]) * q
                    op = 1 - q
                g.add(Dot(pos, radius=0.055, color=GAS).set_opacity(op).set_z_index(6))
            return g

        wall_m, peri_m, org_m = always_redraw(wall), always_redraw(peri), always_redraw(organs)
        gas_m, ndl_m, par_m = always_redraw(gas), always_redraw(needle), always_redraw(particles)

        def caption(s, col=FG):
            return T(s, 36, col).to_corner(UL, buff=0.45)

        # ================= 1. before
        cap = caption("Before: CT without gas")
        self.add(gas_m)
        self.play(Create(back), FadeIn(table), FadeIn(hatch), Create(spine), run_time=1.0)
        self.play(Create(wall_m), FadeIn(org_m), FadeIn(retro), Write(cap), run_time=1.4)
        self.wait(1.2)

        # ================= 2. needle in
        self.add(ndl_m)
        self.play(Transform(cap, caption("1  Needle in")))
        self.play(ndl.animate.set_value(1), run_time=1.4, rate_func=smooth)
        self.wait(0.4)

        # ================= 3. gas in: wall lifts, organs pushed down
        self.add(par_m)
        flow_on.set_value(1)
        self.play(Transform(cap, caption("2  CO₂ in: wall up, organs down", GAS)),
                  flow.animate.set_value(1.2), run_time=1.2, rate_func=linear)
        self.play(lift.animate.set_value(1), push.animate.set_value(1), flow.animate.set_value(6.2),
                  run_time=5.0, rate_func=linear)
        self.play(flow.animate.set_value(7.2), run_time=1.0, rate_func=linear)
        flow_on.set_value(0)

        # ================= 4. needle out, pressure held
        self.play(Transform(cap, caption("3  Needle out, gas stays")),
                  ndl.animate.set_value(0), run_time=1.4)
        self.remove(ndl_m)
        lg = T("CO₂", 30, GAS).move_to([0, top_inner(1) - 0.45, 0])
        self.play(FadeIn(lg))
        self.wait(0.6)

        # ================= 5. mismatch
        ghost_wall = DashedVMobject(VMobject().set_points_smoothly(curve(0, 0)), num_dashes=70,
                                    color=HL, stroke_width=2)
        top0, top1 = pt(0, PI / 2, 0)[1], pt(0, PI / 2, 1)[1]
        arr = DoubleArrow([-4.5, top0, 0], [-4.5, top1, 0], color=HL, buff=0, stroke_width=3, tip_length=0.18)
        g0 = DashedLine([-4.5, top0, 0], [-0.3, top0, 0], color=HL, stroke_width=1)
        g1 = DashedLine([-4.5, top1, 0], [-0.3, top1, 0], color=HL, stroke_width=1)
        la = T("several cm", 30, HL).next_to(arr, LEFT, buff=0.12)
        self.play(Transform(cap, caption("4  CT (dashed) no longer fits", HL)), Create(ghost_wall), run_time=1.4)
        self.play(GrowFromCenter(arr), Create(g0), Create(g1), FadeIn(la))
        self.wait(3)
