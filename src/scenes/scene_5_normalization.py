import os
import sys
import numpy as np
from manim import *

sys.path.insert(0, os.getcwd())
from src.components.base_scene import BaseScene
from src.components.formulas import (
    FORMULA_RUBBER_SHEET_OVERVIEW,
    FORMULA_RUBBER_SHEET_X,
    FORMULA_RUBBER_SHEET_Y,
    FORMULA_POLAR_RANGE,
)
from src.theme import *


# ─── Layout constants ───────────────────────────────────────────────────────
L_COL   = LEFT  * 3.3      # center of left column
R_COL   = RIGHT * 3.0      # center of right column
TITLE_Y = UP    * 3.0      # top title strip center

# Iris geometry (annulus-based, no eye-drawing to allow full control)
INNER_R = 0.65   # pupil boundary radius
OUTER_R = 2.05   # iris outer (limbic) boundary radius
# ─────────────────────────────────────────────────────────────────────────────


class Scene5Normalization(BaseScene):
    """
    Scene 5 — Iris Normalization: Daugman's Rubber Sheet Model

    Visual sequence per SCENE5_GENERATION_RULES.md:
      Shot 1  — Same iris, different pupil dilation → appearance changes
      Shot 2  — Direct pixel comparison fails
      Shot 3  — Rubber Sheet Model: annular iris concept
      Shot 4  — Polar coordinate grid overlay on the iris
      Shot 5  — Radial mapping equations (left iris | right equations)
      Shot 6  — Linear interpolation: moving point along a radial ray
      Shot 7  — Unwrapping: annulus → rectangular strip
      Shot 8  — Normalized strip, checkmark, transition to Feature Extraction
    """

    # ─────────────────────────────────────────────────────────────────────────
    # CONSTRUCT
    # ─────────────────────────────────────────────────────────────────────────
    def construct(self):

        # ═══════════════════════════════════════════════════════════════════
        # SHOT 1  [Audio 1 ≈ 9s]
        # Problem: same iris looks different at different pupil dilations
        # Layout: two iris diagrams side-by-side, centered as a pair
        # ═══════════════════════════════════════════════════════════════════
        self.play_audio("assets/audios/scene5_normalization/1.mp3",
                        fallback_duration=7.0)

        title1 = self._section_title("Same Iris — Different Appearance",
                                     color=MUTED_TEXT_COLOR)

        # Build two iris cross-sections
        eye_L = self._build_eye_diagram(pupil_r=0.32, iris_r=1.15,
                                        caption="Constricted Pupil")
        eye_R = self._build_eye_diagram(pupil_r=0.72, iris_r=1.15,
                                        caption="Dilated Pupil")
        eye_L.move_to(LEFT * 3.3)
        eye_R.move_to(RIGHT * 3.3)

        dbl_arrow = DoubleArrow(
            eye_L.get_right() + RIGHT * 0.15,
            eye_R.get_left()  + LEFT  * 0.15,
            buff=0.05, color=WARNING_COLOR, stroke_width=5,
            tip_length=0.25
        )
        neq_label = MathTex(r"\neq\;?", font_size=52,
                             color=WARNING_COLOR).next_to(dbl_arrow, UP, buff=0.2)

        self.play(FadeIn(title1, shift=DOWN * 0.3), run_time=0.6)
        self.play(
            FadeIn(eye_L, shift=RIGHT * 0.5),
            FadeIn(eye_R, shift=LEFT  * 0.5),
            run_time=1.2
        )
        self.play(GrowArrow(dbl_arrow),
                  FadeIn(neq_label, scale=0.6), run_time=0.8)
        self.wait_audio()

        # ═══════════════════════════════════════════════════════════════════
        # SHOT 2  [Audio 2 ≈ 7s]
        # Direct comparison fails — need canonical representation
        # Layout: centered text + big red X
        # ═══════════════════════════════════════════════════════════════════
        self.play_audio("assets/audios/scene5_normalization/2.mp3",
                        fallback_duration=6.5)

        fail_bg  = RoundedRectangle(
            width=7.5, height=1.3, corner_radius=0.2,
            fill_color=ERROR_COLOR, fill_opacity=0.12,
            stroke_color=ERROR_COLOR, stroke_width=2
        ).move_to(ORIGIN + DOWN * 2.3)
        fail_txt = Text(
            "Direct pixel comparison fails.",
            font=MAIN_FONT, font_size=32,
            color=ERROR_COLOR, weight=BOLD
        ).move_to(fail_bg.get_center())

        big_cross = Cross(stroke_color=ERROR_COLOR,
                          stroke_width=12).scale(0.6).move_to(ORIGIN + DOWN * 0.3)

        self.play(FadeIn(fail_bg), FadeIn(fail_txt, shift=UP * 0.2),
                  run_time=0.8)
        self.play(FadeIn(big_cross, scale=0.4), run_time=0.7)
        self.wait_audio()

        # ═══════════════════════════════════════════════════════════════════
        # SHOT 3  [Audio 3 ≈ 9s]
        # Rubber Sheet Model — centered annular iris, labels outside
        # Layout: single-column centered. Labels with arrows on each side.
        # ═══════════════════════════════════════════════════════════════════
        self.play_audio("assets/audios/scene5_normalization/3.mp3",
                        fallback_duration=9.0)

        # clear
        self.play(
            FadeOut(title1), FadeOut(eye_L), FadeOut(eye_R),
            FadeOut(dbl_arrow), FadeOut(neq_label),
            FadeOut(fail_bg), FadeOut(fail_txt), FadeOut(big_cross),
            run_time=0.7
        )
        self.wait(0.2)

        title3 = self._section_title("Daugman's Rubber Sheet Model",
                                     color=PRIMARY_COLOR)

        # ── Annular iris centered at ORIGIN ──────────────────────────────
        iris_fill = Annulus(
            inner_radius=INNER_R, outer_radius=OUTER_R,
            fill_color=SECONDARY_COLOR, fill_opacity=0.30, stroke_width=0
        )
        # Add subtle radial texture inside the annulus
        iris_texture = self._make_iris_texture(INNER_R, OUTER_R,
                                               n=80, seed=42)
        pupil_fill   = Circle(radius=INNER_R,
                              fill_color="#111111", fill_opacity=1,
                              stroke_width=0)
        pupil_ring   = Circle(radius=INNER_R,
                              color=PRIMARY_COLOR, stroke_width=4)
        limbic_ring  = Circle(radius=OUTER_R,
                              color=SECONDARY_COLOR, stroke_width=4)
        center_dot   = Dot(ORIGIN, color=ERROR_COLOR, radius=0.08)

        eye_all = VGroup(iris_fill, iris_texture, pupil_fill,
                         pupil_ring, limbic_ring, center_dot)

        # ── Labels with arrows, placed outside the diagram ───────────────
        p_label_txt = VGroup(
            Text("Pupillary Boundary", font=MAIN_FONT, font_size=28,
                 color=PRIMARY_COLOR, weight=BOLD),
            MathTex("(r = 0)", font_size=28, color=PRIMARY_COLOR)
        ).arrange(DOWN, buff=0.1).move_to(LEFT * 4.8 + UP * 0.3)

        l_label_txt = VGroup(
            Text("Limbic Boundary", font=MAIN_FONT, font_size=28,
                 color=SECONDARY_COLOR, weight=BOLD),
            MathTex("(r = 1)", font_size=28, color=SECONDARY_COLOR)
        ).arrange(DOWN, buff=0.1).move_to(RIGHT * 4.8 + UP * 0.3)

        # Arrows from labels to the respective circles
        p_arrow = Arrow(
            p_label_txt.get_right(), LEFT * INNER_R + UP * 0.3,
            buff=0.1, color=PRIMARY_COLOR, stroke_width=3, tip_length=0.2
        )
        l_arrow = Arrow(
            l_label_txt.get_left(), RIGHT * OUTER_R + UP * 0.3,
            buff=0.1, color=SECONDARY_COLOR, stroke_width=3, tip_length=0.2
        )

        self.play(FadeIn(title3, shift=DOWN * 0.3), run_time=0.6)
        self.play(
            FadeIn(iris_fill), FadeIn(iris_texture), FadeIn(pupil_fill),
            Create(pupil_ring), Create(limbic_ring), FadeIn(center_dot),
            run_time=1.2
        )
        self.play(
            FadeIn(p_label_txt, shift=RIGHT * 0.3), GrowArrow(p_arrow),
            FadeIn(l_label_txt, shift=LEFT * 0.3),  GrowArrow(l_arrow),
            run_time=0.9
        )
        self.wait_audio()

        # ═══════════════════════════════════════════════════════════════════
        # SHOT 4  [Audio 4 ≈ 9s]
        # Polar coordinate grid on the iris
        # Layout: single-column. Grid fades in over the iris.
        # ═══════════════════════════════════════════════════════════════════
        self.play_audio("assets/audios/scene5_normalization/4.mp3",
                        fallback_duration=10.0)

        title4 = self._section_title("Polar Coordinate System  (r, θ)",
                                     color=WARNING_COLOR)

        self.play(
            FadeOut(title3),
            FadeIn(title4, shift=DOWN * 0.2),
            FadeOut(p_label_txt), FadeOut(p_arrow),
            FadeOut(l_label_txt), FadeOut(l_arrow),
            run_time=0.6
        )

        # Concentric dashed rings (4 equidistant between INNER and OUTER)
        rings = VGroup()
        for k in [0.25, 0.50, 0.75]:
            r_k = INNER_R + k * (OUTER_R - INNER_R)
            rings.add(DashedVMobject(
                Circle(radius=r_k, color=WARNING_COLOR, stroke_width=1.8),
                num_dashes=36, dashed_ratio=0.5
            ))

        # Radial spokes (every 30°)
        spokes = VGroup()
        for deg in range(0, 360, 30):
            rad = np.deg2rad(deg)
            spokes.add(DashedVMobject(
                Line(
                    INNER_R * np.array([np.cos(rad), np.sin(rad), 0]),
                    OUTER_R * np.array([np.cos(rad), np.sin(rad), 0]),
                    color=WARNING_COLOR, stroke_width=1.8
                ),
                num_dashes=5, dashed_ratio=0.5
            ))

        # r arrow (horizontal, from center to right edge of iris)
        r_arrow = Arrow(ORIGIN, RIGHT * OUTER_R,
                        buff=0, color=PRIMARY_COLOR,
                        stroke_width=5, tip_length=0.25)
        r_lbl   = MathTex("r", font_size=38,
                           color=PRIMARY_COLOR).next_to(r_arrow, UP, buff=0.08)

        # θ arc (from 0 to 45°, shown at radius 2.4)
        theta_r = OUTER_R + 0.28
        t_arc   = Arc(radius=theta_r, start_angle=0, angle=PI/4,
                      color=WARNING_COLOR, stroke_width=3,
                      arc_center=ORIGIN)
        t_lbl   = MathTex(r"\theta", font_size=38,
                           color=WARNING_COLOR).move_to(
            theta_r * 1.18 * np.array(
                [np.cos(PI/8), np.sin(PI/8), 0]) + RIGHT * 0.1)

        self.play(
            LaggedStart(*[Create(ring) for ring in rings], lag_ratio=0.3),
            run_time=1.1
        )
        self.play(
            LaggedStart(*[Create(sp) for sp in spokes], lag_ratio=0.06),
            run_time=1.0
        )
        self.play(
            GrowArrow(r_arrow), FadeIn(r_lbl),
            Create(t_arc), FadeIn(t_lbl),
            run_time=0.8
        )
        self.wait_audio()

        # ═══════════════════════════════════════════════════════════════════
        # SHOT 5  [Audio 5 ≈ 10s]
        # Radial mapping equations
        # Layout: LEFT col = iris+grid (scaled 0.65), RIGHT col = equations
        # ═══════════════════════════════════════════════════════════════════
        self.play_audio("assets/audios/scene5_normalization/5.mp3",
                        fallback_duration=8.0)

        title5 = self._section_title("Radial Mapping", color=PRIMARY_COLOR)

        # Scale everything to left column
        iris_group_full = VGroup(
            iris_fill, iris_texture, pupil_fill, pupil_ring, limbic_ring,
            center_dot, rings, spokes, r_arrow, r_lbl, t_arc, t_lbl
        )
        self.play(
            FadeOut(title4),
            FadeIn(title5, shift=DOWN * 0.2),
            iris_group_full.animate.scale(0.60).move_to(L_COL + DOWN * 0.2),
            run_time=0.8
        )

        # ── Equations (right column) ──────────────────────────────────────
        # I(x(r,θ), y(r,θ)) → I(r,θ)
        eq0 = MathTex(
            *FORMULA_RUBBER_SHEET_OVERVIEW,
            font_size=36
        )
        eq0[0].set_color(MUTED_TEXT_COLOR)
        eq0[1].set_color(TEXT_COLOR)
        eq0[2].set_color(PRIMARY_COLOR)

        eq_x = MathTex(
            FORMULA_RUBBER_SHEET_X,
            font_size=34, color=TEXT_COLOR
        )
        eq_y = MathTex(
            FORMULA_RUBBER_SHEET_Y,
            font_size=34, color=TEXT_COLOR
        )
        eq_range = MathTex(
            FORMULA_POLAR_RANGE,
            font_size=30, color=MUTED_TEXT_COLOR
        )

        eq_group = VGroup(eq0, eq_x, eq_y, eq_range)\
            .arrange(DOWN, buff=0.4, aligned_edge=LEFT)\
            .move_to(R_COL + DOWN * 0.2)

        # Thin separator line
        sep = Line(UP * 2.5, DOWN * 2.5,
                   color=MUTED_TEXT_COLOR, stroke_width=1,
                   stroke_opacity=0.4).move_to(ORIGIN)

        self.play(Create(sep), run_time=0.4)
        self.play(Write(eq0), run_time=1.0)
        self.play(Write(eq_x), run_time=0.9)
        self.play(Write(eq_y), run_time=0.9)
        self.play(FadeIn(eq_range, shift=UP * 0.15), run_time=0.6)
        self.wait_audio()

        # ═══════════════════════════════════════════════════════════════════
        # SHOT 6  [Audio 6 ≈ 11s]
        # Linear interpolation: point moves r=0 → r=1 along one radial ray
        # Layout: iris LEFT col, live r-value readout RIGHT col
        # ═══════════════════════════════════════════════════════════════════
        self.play_audio("assets/audios/scene5_normalization/6.mp3",
                        fallback_duration=12.0)

        title6 = self._section_title(
            "Linear Interpolation Along a Radial Ray",
            color=WARNING_COLOR
        )

        # ── Reset iris back to center, remove equations ───────────────────
        iris_group_full.remove(r_arrow, r_lbl, t_arc, t_lbl)
        self.play(
            FadeOut(title5), FadeOut(eq_group), FadeOut(sep),
            FadeOut(r_arrow), FadeOut(r_lbl), FadeOut(t_arc), FadeOut(t_lbl),
            FadeIn(title6, shift=DOWN * 0.2),
            iris_group_full.animate.scale(1 / 0.60).move_to(ORIGIN),
            run_time=0.8
        )

        # ── Highlight a single ray at 45° ─────────────────────────────────
        ray_ang  = PI / 4
        cos_a, sin_a = np.cos(ray_ang), np.sin(ray_ang)

        # Actual positions (iris_group_full is now back at ORIGIN)
        p_pt = np.array([INNER_R * cos_a, INNER_R * sin_a, 0])
        s_pt = np.array([OUTER_R * cos_a, OUTER_R * sin_a, 0])

        highlight_ray = Line(p_pt, s_pt, color=PRIMARY_COLOR, stroke_width=6)

        dot_p = Dot(p_pt, color=PRIMARY_COLOR, radius=0.13)
        dot_s = Dot(s_pt, color=SECONDARY_COLOR, radius=0.13)

        # Labels for endpoints placed OUTSIDE the iris
        lbl_r0 = MathTex("r=0", font_size=34, color=PRIMARY_COLOR)\
            .add_background_rectangle(color=BLACK, opacity=0.6, buff=0.05)\
            .next_to(dot_p, UL, buff=0.1)
        lbl_r1 = MathTex("r=1", font_size=34, color=SECONDARY_COLOR)\
            .add_background_rectangle(color=BLACK, opacity=0.6, buff=0.05)\
            .next_to(dot_s, UR, buff=0.15)

        # Tracker
        r_trk = ValueTracker(0.0)
        moving_dot = always_redraw(
            lambda: Dot(
                p_pt + r_trk.get_value() * (s_pt - p_pt),
                color=WARNING_COLOR, radius=0.15
            )
        )

        # Live r readout on the right (well clear of the iris)
        r_readout = always_redraw(
            lambda: VGroup(
                MathTex(r"r =", font_size=40, color=WARNING_COLOR),
                MathTex(
                    f"{r_trk.get_value():.2f}",
                    font_size=52, color=WARNING_COLOR
                )
            ).arrange(RIGHT, buff=0.15).move_to(RIGHT * 4.8 + DOWN * 0.2)
        )
        r_readout_title = Text(
            "Current sample point", font=MAIN_FONT, font_size=28,
            color=MUTED_TEXT_COLOR
        ).move_to(RIGHT * 4.8 + UP * 0.6)

        self.play(
            Create(highlight_ray),
            FadeIn(dot_p), FadeIn(dot_s),
            FadeIn(lbl_r0), FadeIn(lbl_r1),
            run_time=0.8
        )
        self.add(moving_dot, r_readout)
        self.play(FadeIn(r_readout_title), run_time=0.4)

        # r: 0 → 1 → 0
        self.play(r_trk.animate.set_value(1.0),
                  run_time=3.5, rate_func=linear)
        self.play(r_trk.animate.set_value(0.0),
                  run_time=1.5, rate_func=smooth)
        self.wait_audio()

        # ═══════════════════════════════════════════════════════════════════
        # SHOT 7  [Audio 7 ≈ 12s]
        # Unwrapping: annular iris → rectangular normalized strip
        # Layout: LEFT = iris with full-circle radial rays, RIGHT = strip
        # ═══════════════════════════════════════════════════════════════════
        self.play_audio("assets/audios/scene5_normalization/7.mp3",
                        fallback_duration=11.0)

        title7 = self._section_title(
            "Unwrapping the Iris into a Rectangle",
            color=PRIMARY_COLOR
        )

        # Clean up shot-6 overlays
        self.remove(moving_dot, r_readout)
        self.play(
            FadeOut(title6),
            FadeOut(highlight_ray), FadeOut(dot_p), FadeOut(dot_s),
            FadeOut(lbl_r0), FadeOut(lbl_r1),
            FadeOut(r_readout_title),
            FadeIn(title7, shift=DOWN * 0.2),
            run_time=0.7
        )

        # ── Add full-circle spokes on the iris ─────────────────────────────
        N_RAYS = 18
        full_rays = VGroup()
        for i in range(N_RAYS):
            ang   = 2 * PI * i / N_RAYS
            c_, s_ = np.cos(ang), np.sin(ang)
            full_rays.add(Line(
                INNER_R * np.array([c_, s_, 0]),
                OUTER_R * np.array([c_, s_, 0]),
                color=SECONDARY_COLOR, stroke_width=2.0, stroke_opacity=0.75
            ))

        self.play(
            LaggedStart(*[Create(r_) for r_ in full_rays], lag_ratio=0.05),
            run_time=0.9
        )
        self.wait(0.3)

        # ── Move iris to LEFT col, build rectangle on RIGHT ────────────────
        iris_unwrap_group = VGroup(iris_group_full, full_rays)

        # Rectangle geometry (right column)
        R_X0, R_X1 = 0.4, 6.3      # x limits for the rectangle
        R_Y0, R_Y1 = -1.5, 1.5     # y limits (height = 3.0 → nice and big)
        rect_w, rect_h = R_X1 - R_X0, R_Y1 - R_Y0
        rect_cx = (R_X0 + R_X1) / 2
        rect_cy = (R_Y0 + R_Y1) / 2

        # Vertical lines inside the rectangle matching the N_RAYS spokes
        target_vlines = VGroup()
        for i in range(N_RAYS + 1):
            x_ = R_X0 + (i / N_RAYS) * rect_w
            target_vlines.add(Line(
                np.array([x_, R_Y0, 0]), np.array([x_, R_Y1, 0]),
                color=SECONDARY_COLOR, stroke_width=2.0, stroke_opacity=0.7
            ))

        norm_rect  = Rectangle(
            width=rect_w, height=rect_h,
            color=PRIMARY_COLOR, stroke_width=4
        ).move_to(np.array([rect_cx, rect_cy, 0]))
        norm_fill  = Rectangle(
            width=rect_w, height=rect_h,
            fill_color=SECONDARY_COLOR, fill_opacity=0.18, stroke_width=0
        ).move_to(norm_rect.get_center())

        # Axis arrows below and to the left of the rectangle
        theta_ax   = Arrow(
            np.array([R_X0, R_Y0 - 0.45, 0]),
            np.array([R_X1, R_Y0 - 0.45, 0]),
            buff=0, color=WARNING_COLOR, stroke_width=4, tip_length=0.22
        )
        theta_lbl  = MathTex(r"\theta:\ 0 \to 2\pi", font_size=30,
                              color=WARNING_COLOR)\
            .next_to(theta_ax, DOWN, buff=0.15)
        r_ax       = Arrow(
            np.array([R_X0 - 0.45, R_Y1, 0]),
            np.array([R_X0 - 0.45, R_Y0, 0]),
            buff=0, color=PRIMARY_COLOR, stroke_width=4, tip_length=0.22
        )
        r_ax_lbl   = MathTex(r"r:\ 0 \to 1", font_size=30,
                              color=PRIMARY_COLOR)\
            .next_to(r_ax, LEFT, buff=0.15)
        norm_lbl   = Text(
            "Normalized Iris Strip",
            font=MAIN_FONT, font_size=30, color=PRIMARY_COLOR, weight=BOLD
        ).next_to(norm_rect, UP, buff=0.28)

        self.play(
            iris_unwrap_group.animate
                .scale(0.60)
                .move_to(np.array([-4.2, rect_cy, 0])),
            run_time=0.8
        )

        # Transform: spokes → vertical lines
        self.play(
            ReplacementTransform(full_rays.copy(), target_vlines),
            run_time=2.0, rate_func=smooth
        )
        self.play(
            FadeIn(norm_fill), Create(norm_rect),
            run_time=0.7
        )
        self.play(
            Write(norm_lbl),
            GrowArrow(theta_ax), FadeIn(theta_lbl),
            GrowArrow(r_ax),     FadeIn(r_ax_lbl),
            run_time=0.9
        )
        self.wait_audio()

        # ═══════════════════════════════════════════════════════════════════
        # SHOT 8  [Audio 8 ≈ 10s]
        # Final: centered strip + iris texture pattern + checkmark → Scene 6
        # ═══════════════════════════════════════════════════════════════════
        self.play_audio("assets/audios/scene5_normalization/8.mp3",
                        fallback_duration=12.0)

        # Fade out iris, center the strip
        strip_group = VGroup(
            norm_fill, norm_rect, norm_lbl,
            target_vlines,
            theta_ax, theta_lbl,
            r_ax,     r_ax_lbl
        )
        self.play(
            FadeOut(iris_unwrap_group),
            FadeOut(title7),
            strip_group.animate.move_to(ORIGIN + DOWN * 0.3),
            run_time=0.9
        )

        # Add iris-pattern texture lines inside the centered strip
        pattern = self._make_strip_pattern(strip_group, n=35, seed=11)
        self.play(
            LaggedStart(*[Create(ln) for ln in pattern], lag_ratio=0.03),
            run_time=1.0
        )

        # ── Checkmark ────────────────────────────────────────────────────
        check  = self.create_check_icon().scale(0.65).move_to(UP * 2.8)
        done_t = Text(
            "Normalization Complete",
            font=MAIN_FONT, font_size=30, color=SUCCESS_COLOR
        ).next_to(check, RIGHT, buff=0.4)
        done_g = VGroup(check, done_t).move_to(UP * 2.8)

        self.play(FadeIn(check, scale=0.5),
                  FadeIn(done_t, shift=UP * 0.2), run_time=0.8)
        self.wait(1.8)

        # Zoom-out + fade → transition
        all_out = VGroup(strip_group, pattern, done_g)
        self.play(all_out.animate.scale(3.5).set_opacity(0), run_time=1.5)
        self.wait(2)

        self.play_scene_title("6. Feature Extraction")
        self.wait_audio()

    # ─────────────────────────────────────────────────────────────────────────
    # HELPER METHODS
    # ─────────────────────────────────────────────────────────────────────────

    def _section_title(self, text: str, color: str = None) -> "Text":
        """Delegates to BaseScene._section_title() — kept as alias for compatibility."""
        return super()._section_title(text, color)

    def _build_eye_diagram(
        self, pupil_r: float, iris_r: float, caption: str
    ) -> VGroup:
        """
        A polished vector iris cross-section for the comparison shot.
        Includes sclera, iris texture, pupil, and boundary highlights.
        """
        group = VGroup()

        # Sclera
        sclera = Ellipse(
            width=iris_r * 2.85, height=iris_r * 2.1,
            fill_color="#DADADA", fill_opacity=0.95, stroke_width=0
        )
        # Iris base
        iris_base = Circle(
            radius=iris_r, fill_color="#2E3A2F",
            fill_opacity=1, stroke_width=0
        )
        # Iris texture (thin radial lines)
        rng_ = np.random.default_rng(seed=99)
        tex  = VGroup()
        for _ in range(60):
            ang_ = rng_.uniform(0, 2 * PI)
            r0_  = rng_.uniform(0.7, 1.0)
            r1_  = rng_.uniform(1.1, 0.97 * iris_r / pupil_r * pupil_r
                                 if pupil_r < iris_r else iris_r)
            r1_  = min(r1_, iris_r * 0.97)
            c_, s_ = np.cos(ang_), np.sin(ang_)
            tex.add(Line(
                r0_ * pupil_r * np.array([c_, s_, 0]),
                r1_           * np.array([c_, s_, 0]),
                stroke_color="#6E8C6F",
                stroke_width=rng_.uniform(0.4, 1.4),
                stroke_opacity=rng_.uniform(0.2, 0.55)
            ))

        # Pupil
        pupil = Circle(
            radius=pupil_r, fill_color="#090909",
            fill_opacity=1, stroke_width=0
        )
        # Catchlight
        catch = Circle(
            radius=0.06, fill_color=WHITE,
            fill_opacity=0.85, stroke_width=0
        ).move_to(pupil_r * 0.55 * np.array([np.cos(PI/4), np.sin(PI/4), 0]))

        # Boundary rings
        p_ring = Circle(radius=pupil_r,
                        color=PRIMARY_COLOR, stroke_width=3)
        l_ring = Circle(radius=iris_r,
                        color=SECONDARY_COLOR, stroke_width=3)

        # Caption below
        cap = Text(caption, font=MAIN_FONT, font_size=26,
                   color=MUTED_TEXT_COLOR).next_to(sclera, DOWN, buff=0.22)

        group.add(sclera, iris_base, tex, pupil, catch, p_ring, l_ring, cap)
        return group

    def _make_iris_texture(
        self, inner_r: float, outer_r: float,
        n: int = 80, seed: int = 0
    ) -> VGroup:
        """
        Subtle radial lines inside the iris annulus to simulate texture.
        """
        rng_  = np.random.default_rng(seed=seed)
        lines = VGroup()
        for _ in range(n):
            ang_ = rng_.uniform(0, 2 * PI)
            r_s  = rng_.uniform(inner_r + 0.04, outer_r * 0.45)
            r_e  = rng_.uniform(outer_r * 0.55, outer_r - 0.04)
            c_   = np.cos(ang_)
            s_   = np.sin(ang_)
            lines.add(Line(
                r_s * np.array([c_, s_, 0]),
                r_e * np.array([c_, s_, 0]),
                stroke_color="#5DBCB2",
                stroke_width=rng_.uniform(0.4, 1.5),
                stroke_opacity=rng_.uniform(0.12, 0.40)
            ))
        return lines

    def _make_strip_pattern(self, strip_ref: VGroup, n: int, seed: int) -> VGroup:
        """
        Vertical lines inside the normalized strip to simulate iris pattern.
        Positions are computed relative to the (possibly moved) strip_ref.
        """
        rng_   = np.random.default_rng(seed=seed)
        cx     = strip_ref.get_center()
        w_half = strip_ref.get_width()  / 2 * 0.85
        h_half = strip_ref.get_height() / 2 * 0.75
        lines  = VGroup()
        for _ in range(n):
            x_ = cx[0] + rng_.uniform(-w_half, w_half)
            lines.add(Line(
                np.array([x_, cx[1] - h_half, 0]),
                np.array([x_, cx[1] + h_half, 0]),
                color=SECONDARY_COLOR,
                stroke_width=rng_.uniform(0.8, 2.5),
                stroke_opacity=rng_.uniform(0.18, 0.55)
            ))
        return lines

    def _create_check_icon(self) -> VGroup:
        """Delegates to inherited BaseScene.create_check_icon()."""
        return self.create_check_icon()
