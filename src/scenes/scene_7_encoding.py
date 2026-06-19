import os
import sys
import numpy as np
from manim import *

sys.path.insert(0, os.getcwd())
from src.components.base_scene import BaseScene
from src.components.formulas import *
from src.theme import *

# ─── Layout constants ─────────────────────────────────────────────────────────
AUDIO_DIR = "assets/audios/scene7_encoding"

# ─── Color aliases ─────────────────────────────────────────────────────────────
PHASE_COLOR   = PRIMARY_COLOR    # cyan   — phase / phasor
REAL_COLOR    = WARNING_COLOR    # amber  — real component
IMAG_COLOR    = ACCENT_COLOR     # purple — imaginary component
BIT_COLOR     = SUCCESS_COLOR    # green  — binary bits / IrisCode
DISCARD_COLOR = ERROR_COLOR      # red    — magnitude (discarded)
PLANE_COLOR   = SECONDARY_COLOR  # teal   — complex plane axes


class Scene7Encoding(BaseScene):
    """
    Scene 7 — Phase Quantization and IrisCode Generation (~45 s)
    """

    def construct(self):
        # ═══════════════════════════════════════════════════════════════════
        # SHOT 1  [Audio 1]  0–8 s
        # From Feature Response → Correct Complex Number
        # ═══════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/1.mp3", fallback_duration=14.0)

        title1 = self._section_title("Feature Response to Complex Number", color=PHASE_COLOR)
        self.play(FadeIn(title1, shift=DOWN * 0.3), run_time=0.5)

        # ── Feature map echo (visual anchor from Scene 6) ─────────────────
        feat_map = self._build_feature_map_echo(center=UP * 1.0, rows=3, cols=10)
        self.play(FadeIn(feat_map, shift=UP * 0.1), run_time=0.7)

        # Highlight one cell
        selected = feat_map[1 * 10 + 4]
        hl_rect = SurroundingRectangle(selected, color=PHASE_COLOR, stroke_width=2.5, buff=0.06)
        self.play(Create(hl_rect), run_time=0.3)

        # ── Fix 1: Correct formula derivation (stepped) ───────────────────
        re_eq  = MathTex(r"\operatorname{Re} = A\cos\phi", font_size=32, color=REAL_COLOR)
        im_eq  = MathTex(r"\operatorname{Im} = A\sin\phi", font_size=32, color=IMAG_COLOR)
        VGroup(re_eq, im_eq).arrange(RIGHT, buff=1.0).move_to(DOWN * 0.6)

        comb_eq = MathTex(
            r"z = \operatorname{Re} + j\operatorname{Im} = A e^{j\phi}",
            font_size=36, color=PHASE_COLOR
        ).move_to(DOWN * 1.6)

        self.play(Write(re_eq), Write(im_eq), run_time=0.9)
        self.play(FadeIn(comb_eq, shift=UP * 0.1), run_time=0.6)

        # ── Daugman formula watermark (Moved to bottom & cleaned up) ──────
        daugman_formula = MathTex(
            r"h_{\{Re,Im\}} = ", 
            r"\operatorname{sgn}_{\{Re,Im\}}", 
            r"\left( \int_{\rho}\int_{\phi} I(\rho,\phi)\,e^{-i\omega(\theta_0-\phi)} e^{-\frac{(r_0-\rho)^2}{\alpha^2}} e^{-\frac{(\theta_0-\phi)^2}{\beta^2}} \rho\, d\rho\, d\phi \right)",
            font_size=22, color=MUTED_TEXT_COLOR
        )
        daugman_panel = VGroup(
            SurroundingRectangle(daugman_formula, color=MUTED_TEXT_COLOR, stroke_width=1, fill_color=BG_COLOR, fill_opacity=0.8, buff=0.15),
            daugman_formula
        ).move_to(DOWN * 2.8)

        self.play(FadeIn(daugman_panel), run_time=0.5)

        # Highlight sgn in Daugman formula
        sgn_highlight = SurroundingRectangle(
            daugman_formula[1], color=PHASE_COLOR, stroke_width=2.0, buff=0.05
        )
        self.play(Create(sgn_highlight), run_time=0.5)
        self.wait_audio()

        # ═══════════════════════════════════════════════════════════════════
        # SHOT 2  [Audio 2]  8–15 s
        # Discarding Magnitude — Only Phase Matters
        # ═══════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/2.mp3", fallback_duration=12.0)

        title2 = self._section_title("Discard Magnitude — Keep Phase", color=PHASE_COLOR)
        self.play(
            FadeOut(feat_map), FadeOut(hl_rect), FadeOut(re_eq),
            FadeOut(im_eq), FadeOut(comb_eq),
            FadeOut(daugman_panel), FadeOut(sgn_highlight), FadeOut(title1),
            FadeIn(title2, shift=DOWN * 0.2),
            run_time=0.6
        )

        # Complex plane (left half)
        plane_cx = LEFT * 3.0 + DOWN * 0.2
        plane2   = self._build_complex_plane(center=plane_cx, half=2.3)
        self.play(Create(plane2), run_time=0.5)

        # Phasor with explicit updaters
        angle_vt = ValueTracker(PI / 4)
        r_vt     = ValueTracker(1.3)

        phasor2    = Arrow(ORIGIN, ORIGIN, color=PHASE_COLOR, buff=0, tip_length=0.20, stroke_width=4)
        arc2       = Arc(radius=0.4, start_angle=0, angle=PI/4, arc_center=ORIGIN,
                         color=PHASE_COLOR, stroke_width=2.5)
        phi_lbl2   = MathTex(r"\phi", font_size=28, color=PHASE_COLOR)
        mag_lbl2   = MathTex(r"A", font_size=26, color=DISCARD_COLOR)

        def upd_phasor2(m):
            a, r = angle_vt.get_value(), r_vt.get_value()
            tip  = plane_cx + np.array([r * np.cos(a), r * np.sin(a), 0])
            m.become(Arrow(plane_cx, tip, color=PHASE_COLOR, buff=0, tip_length=0.20, stroke_width=4))

        def upd_arc2(m):
            a = angle_vt.get_value()
            m.become(Arc(radius=0.4, start_angle=0, angle=a,
                         arc_center=plane_cx, color=PHASE_COLOR, stroke_width=2.5))

        def upd_phi2(m):
            a = angle_vt.get_value()
            m.move_to(plane_cx + np.array([0.72 * np.cos(a/2), 0.72 * np.sin(a/2), 0]))

        def upd_mag2(m):
            a, r = angle_vt.get_value(), r_vt.get_value()
            mid  = plane_cx + np.array([0.5 * r * np.cos(a), 0.5 * r * np.sin(a), 0])
            m.move_to(mid + UP * 0.2)

        phasor2.add_updater(upd_phasor2)
        arc2.add_updater(upd_arc2)
        phi_lbl2.add_updater(upd_phi2)
        mag_lbl2.add_updater(upd_mag2)
        self.add(phasor2, arc2, phi_lbl2, mag_lbl2)

        # Right annotations
        discard_grp = VGroup(
            Text("Magnitude  A", font=MAIN_FONT, font_size=24, color=DISCARD_COLOR, weight=BOLD),
            Text("varies with lighting,", font=MAIN_FONT, font_size=18, color=MUTED_TEXT_COLOR),
            Text("contrast, sensor gain", font=MAIN_FONT, font_size=18, color=MUTED_TEXT_COLOR),
        ).arrange(DOWN, buff=0.15).move_to(RIGHT * 2.8 + UP * 1.1)

        keep_grp = VGroup(
            Text("Phase  \u03d5", font=MAIN_FONT, font_size=24, color=PHASE_COLOR, weight=BOLD),
            Text("stable under", font=MAIN_FONT, font_size=18, color=MUTED_TEXT_COLOR),
            Text("varying conditions", font=MAIN_FONT, font_size=18, color=MUTED_TEXT_COLOR),
        ).arrange(DOWN, buff=0.15).move_to(RIGHT * 2.8 + DOWN * 0.9)

        self.play(FadeIn(discard_grp, shift=LEFT * 0.2), run_time=0.5)
        # Animate: magnitude shrinks / grows while angle stays fixed
        self.play(r_vt.animate.set_value(0.4), run_time=0.5)
        self.play(r_vt.animate.set_value(1.9), run_time=0.5)
        self.play(r_vt.animate.set_value(0.35), run_time=0.4)

        # Cross out ONLY the title "Magnitude A" to avoid overlapping paragraph
        cross = Cross(discard_grp[0], color=DISCARD_COLOR, stroke_width=4.0)
        self.play(Create(cross), run_time=0.4)
        self.play(FadeIn(keep_grp, shift=LEFT * 0.2), run_time=0.5)
        self.play(r_vt.animate.set_value(1.3), run_time=0.4)
        self.wait_audio()

        # ═══════════════════════════════════════════════════════════════════
        # SHOT 3  [Audio 3]  15–25 s
        # Complex Plane — 4 Quadrants
        # ═══════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/3.mp3", fallback_duration=11.5)

        title3 = self._section_title("Phase Quantization — 4 Quadrants", color=PHASE_COLOR)

        phasor2.clear_updaters()
        arc2.clear_updaters()
        phi_lbl2.clear_updaters()
        mag_lbl2.clear_updaters()

        self.play(
            FadeOut(title2), FadeOut(plane2),
            FadeOut(phasor2), FadeOut(arc2), FadeOut(phi_lbl2), FadeOut(mag_lbl2),
            FadeOut(discard_grp), FadeOut(keep_grp), FadeOut(cross),
            FadeIn(title3, shift=DOWN * 0.2),
            run_time=0.6
        )

        plane_cx3 = DOWN * 0.3
        half3     = 2.7
        big_plane = self._build_complex_plane(center=plane_cx3, half=half3 + 0.4)
        quads     = self._build_quadrant_shading(center=plane_cx3, half=half3)
        self.play(Create(big_plane), run_time=0.5)
        self.play(FadeIn(quads), run_time=0.5)

        # Phasor on big plane
        angle_vt3 = ValueTracker(PI / 5)
        r3        = 2.1
        phasor3   = Arrow(ORIGIN, ORIGIN, color=PHASE_COLOR, buff=0, tip_length=0.22, stroke_width=5)
        arc3      = Arc(radius=0.55, start_angle=0, angle=PI/5, arc_center=ORIGIN,
                        color=PHASE_COLOR, stroke_width=3)
        phi_lbl3  = MathTex(r"\phi", font_size=30, color=PHASE_COLOR)

        def upd_phasor3(m):
            a = angle_vt3.get_value()
            m.become(Arrow(plane_cx3,
                           plane_cx3 + np.array([r3*np.cos(a), r3*np.sin(a), 0]),
                           color=PHASE_COLOR, buff=0, tip_length=0.22, stroke_width=5))

        def upd_arc3(m):
            a = angle_vt3.get_value()
            m.become(Arc(radius=0.55, start_angle=0, angle=a,
                         arc_center=plane_cx3, color=PHASE_COLOR, stroke_width=3))

        def upd_phi3(m):
            a = angle_vt3.get_value()
            m.move_to(plane_cx3 + np.array([0.95*np.cos(a/2), 0.95*np.sin(a/2), 0]))

        phasor3.add_updater(upd_phasor3)
        arc3.add_updater(upd_arc3)
        phi_lbl3.add_updater(upd_phi3)
        self.add(phasor3, arc3, phi_lbl3)

        for target in [2.5, PI + 0.4, -2.2, -0.5, PI / 5]:
            self.play(angle_vt3.animate.set_value(target), run_time=0.85, rate_func=smooth)
            self.wait(0.25)

        self.wait_audio()

        # ═══════════════════════════════════════════════════════════════════
        # SHOT 4  [Audio 4]  25–35 s
        # Quadrant → 2-Bit Encoding + Bit Rule Table
        # ═══════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/4.mp3", fallback_duration=12.0)

        title4 = self._section_title("Quadrant \u2192 2-Bit Encoding", color=BIT_COLOR)
        self.play(FadeOut(title3), FadeIn(title4, shift=DOWN * 0.2), run_time=0.5)

        rule_panel = self._build_rule_table(center=RIGHT * 5.0 + UP * 0.6)
        self.play(FadeIn(rule_panel), run_time=0.5)

        bit_txt = Text("?", font=MONO_FONT, font_size=64, color=BIT_COLOR)
        bit_txt.move_to(RIGHT * 5.0 + DOWN * 1.5)
        self.add(bit_txt)

        quad_data = [
            (PI / 4,     "11", "Re\u22650,  Im\u22650"),
            (3 * PI / 4, "01", "Re<0,   Im\u22650"),
            (-3*PI/4,    "00", "Re<0,   Im<0"),
            (-PI / 4,    "10", "Re\u22650,  Im<0"),
        ]

        for angle, bits, sign_str in quad_data:
            new_bit = Text(bits, font=MONO_FONT, font_size=64, color=BIT_COLOR)
            new_bit.move_to(RIGHT * 5.0 + DOWN * 1.5)
            sign_lbl = Text(sign_str, font=MONO_FONT, font_size=17, color=MUTED_TEXT_COLOR)
            sign_lbl.move_to(RIGHT * 5.0 + DOWN * 2.35)

            self.play(
                angle_vt3.animate.set_value(angle),
                Transform(bit_txt, new_bit),
                FadeIn(sign_lbl, shift=UP * 0.1),
                run_time=0.7, rate_func=smooth
            )
            self.wait(0.5)
            self.play(FadeOut(sign_lbl), run_time=0.25)

        self.wait_audio()

        # ═══════════════════════════════════════════════════════════════════
        # SHOT 5  [Audio 5]  35–42 s
        # Append Bits — Patch → Bits → Stream
        # ═══════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/5.mp3", fallback_duration=10.0)

        title5 = self._section_title("Building the IrisCode", color=BIT_COLOR)
        phasor3.clear_updaters()
        arc3.clear_updaters()
        phi_lbl3.clear_updaters()

        self.play(
            FadeOut(title4), FadeOut(big_plane), FadeOut(quads),
            FadeOut(phasor3), FadeOut(arc3), FadeOut(phi_lbl3),
            FadeOut(rule_panel), FadeOut(bit_txt),
            FadeIn(title5, shift=DOWN * 0.2),
            run_time=0.6
        )

        # Mini iris strip with 4 highlighted regions (Fixed lines overlay issue)
        strip_mini = self._build_mini_strip(center=UP * 1.8, width=8.5, height=0.8)
        self.play(FadeIn(strip_mini), run_time=0.4)

        patch_xs   = [-3.0, -1.0, 1.0, 3.0]
        patch_bits = ["11", "01", "10", "00"]
        patch_cols = [REAL_COLOR, IMAG_COLOR, WARNING_COLOR, MUTED_TEXT_COLOR]

        patch_grp = VGroup()
        bit_grp   = VGroup()
        arrow_grp = VGroup()

        for px, bits, col in zip(patch_xs, patch_bits, patch_cols):
            box  = Rectangle(width=0.9, height=0.8, fill_color=col, fill_opacity=0.25,
                              stroke_color=col, stroke_width=2)
            box.move_to(np.array([px, 1.8, 0])) # Box over the strip at UP*1.8
            btxt = Text(bits, font=MONO_FONT, font_size=28, color=BIT_COLOR, weight=BOLD)
            btxt.move_to(np.array([px, 0.6, 0]))
            arr  = Arrow(box.get_bottom(), btxt.get_top(), buff=0.05,
                         color=col, stroke_width=2, tip_length=0.15)
            patch_grp.add(box)
            bit_grp.add(btxt)
            arrow_grp.add(arr)

        self.play(FadeIn(patch_grp), run_time=0.5)
        self.play(LaggedStart(*[
            AnimationGroup(Create(arrow_grp[i]), Write(bit_grp[i]))
            for i in range(4)
        ], lag_ratio=0.3), run_time=1.8)

        # Combine into stream arrow + bit sequence (Fixed monospace text kerning)
        stream_lbl = MathTex(r"\texttt{1101101000...}", font_size=36, color=BIT_COLOR)
        stream_lbl.move_to(DOWN * 0.8)
        combine_arrow = Arrow(
            UP * 0.1, DOWN * 0.4,
            color=MUTED_TEXT_COLOR, stroke_width=2, tip_length=0.18
        )
        self.play(FadeIn(combine_arrow), run_time=0.3)
        self.play(Write(stream_lbl), run_time=0.6)

        size_lbl = VGroup(
            Text("2048 bits", font=MAIN_FONT, font_size=22, color=BIT_COLOR, weight=BOLD),
            Text("(256 bytes)", font=MAIN_FONT, font_size=18, color=MUTED_TEXT_COLOR),
        ).arrange(RIGHT, buff=0.3).move_to(DOWN * 1.8)
        self.play(FadeIn(size_lbl, shift=UP * 0.1), run_time=0.5)

        self.wait_audio()

        # ═══════════════════════════════════════════════════════════════════
        # SHOT 6  [Audio 6]  42–45 s
        # Final IrisCode — glowing binary signature
        # ═══════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/6.mp3", fallback_duration=10.0)

        title6 = self._section_title("IrisCode — 2048-bit Digital Signature", color=BIT_COLOR)
        self.play(
            FadeOut(title5), FadeOut(strip_mini),
            FadeOut(patch_grp), FadeOut(arrow_grp), FadeOut(bit_grp),
            FadeOut(combine_arrow), FadeOut(stream_lbl), FadeOut(size_lbl),
            FadeIn(title6, shift=DOWN * 0.2),
            run_time=0.6
        )

        iris_code = self._build_iriscode_matrix(rows=8, cols=34, center=DOWN * 0.3)
        self.play(FadeIn(iris_code, shift=UP * 0.2), run_time=1.0)
        self.play(iris_code.animate.set_opacity(0.65), run_time=0.5, rate_func=there_and_back)

        final_lbl = VGroup(
            Text("IrisCode", font=MAIN_FONT, font_size=38, color=BIT_COLOR, weight=BOLD),
            Text("Compact  \u00b7  Robust  \u00b7  Fast Matching",
                 font=MAIN_FONT, font_size=18, color=MUTED_TEXT_COLOR),
        ).arrange(DOWN, buff=0.15)
        final_lbl.next_to(iris_code, DOWN, buff=0.3)

        self.play(FadeIn(final_lbl, shift=UP * 0.2), run_time=0.7)
        self.wait_audio()

        # Transition to Scene 8
        self.play(FadeOut(iris_code), FadeOut(title6), FadeOut(final_lbl), run_time=0.2)
        self.play_scene_title("8. Iris Matching")

    # ─────────────────────────────────────────────────────────────────────────
    # HELPER METHODS
    # ─────────────────────────────────────────────────────────────────────────

    def _section_title(self, text: str, color: str = None) -> "Text":
        color = color or TEXT_COLOR
        return Text(text, font=MAIN_FONT, font_size=34, color=color, weight=BOLD).move_to(UP * 3.2)

    def _build_complex_plane(self, center, half: float) -> VGroup:
        axes = VGroup(
            Arrow(center + LEFT * half, center + RIGHT * half,
                  color=PLANE_COLOR, stroke_width=2.5, buff=0, tip_length=0.18),
            Arrow(center + DOWN * half, center + UP * half,
                  color=PLANE_COLOR, stroke_width=2.5, buff=0, tip_length=0.18),
        )
        re_lbl = Text("Re", font=MAIN_FONT, font_size=20, color=REAL_COLOR)
        re_lbl.next_to(axes[0].get_end(), RIGHT, buff=0.12)
        im_lbl = Text("Im", font=MAIN_FONT, font_size=20, color=IMAG_COLOR)
        im_lbl.next_to(axes[1].get_end(), UP, buff=0.12)
        return VGroup(axes, re_lbl, im_lbl)

    def _build_quadrant_shading(self, center, half: float) -> VGroup:
        quad_fills = [
            (RIGHT * half/2 + UP   * half/2, "#0a2a1a"),   # I   green
            (LEFT  * half/2 + UP   * half/2, "#0a0a2a"),   # II  blue
            (LEFT  * half/2 + DOWN * half/2, "#2a0a0a"),   # III red
            (RIGHT * half/2 + DOWN * half/2, "#2a1a0a"),   # IV  amber
        ]
        quad_labels = [
            (RIGHT * half * 0.68 + UP   * half * 0.72, "11", REAL_COLOR),
            (LEFT  * half * 0.68 + UP   * half * 0.72, "01", IMAG_COLOR),
            (LEFT  * half * 0.68 + DOWN * half * 0.72, "00", MUTED_TEXT_COLOR),
            (RIGHT * half * 0.68 + DOWN * half * 0.72, "10", WARNING_COLOR),
        ]
        grp = VGroup()
        for offset, fill_c in quad_fills:
            rect = Rectangle(width=half, height=half,
                             fill_color=fill_c, fill_opacity=0.85, stroke_width=0)
            rect.move_to(center + offset)
            grp.add(rect)
        for offset, bits, col in quad_labels:
            lbl = Text(bits, font=MONO_FONT, font_size=28, color=col, weight=BOLD)
            lbl.move_to(center + offset)
            grp.add(lbl)
        return grp

    def _build_rule_table(self, center) -> VGroup:
        rules = VGroup(
            MathTex(r"\operatorname{Re}\ge0\;\Rightarrow\;\text{Bit}_1=1",
                    font_size=20, color=REAL_COLOR),
            MathTex(r"\operatorname{Re}<0\;\Rightarrow\;\text{Bit}_1=0",
                    font_size=20, color=REAL_COLOR),
            MathTex(r"\operatorname{Im}\ge0\;\Rightarrow\;\text{Bit}_2=1",
                    font_size=20, color=IMAG_COLOR),
            MathTex(r"\operatorname{Im}<0\;\Rightarrow\;\text{Bit}_2=0",
                    font_size=20, color=IMAG_COLOR),
        ).arrange(DOWN, buff=0.2).move_to(center)
        bg = SurroundingRectangle(rules, color=PLANE_COLOR, stroke_width=1.5,
                                  fill_color=BG_COLOR, fill_opacity=0.92,
                                  buff=0.22, corner_radius=0.18)
        return VGroup(bg, rules)

    def _build_feature_map_echo(self, center, rows: int, cols: int) -> VGroup:
        rng      = np.random.default_rng(seed=31)
        ridge_xs = np.linspace(-4.0, 4.0, 5)
        strip_w  = 8.0
        cell_w, cell_h = 0.60, 0.50
        w  = cols * cell_w
        h  = rows * cell_h
        cx0 = center[0] - w / 2 + cell_w / 2
        cy0 = center[1] + h / 2 - cell_h / 2
        cells = VGroup()
        for r in range(rows):
            for c in range(cols):
                x_pos    = -strip_w/2 + (c / (cols - 1)) * strip_w
                min_dist = min(abs(x_pos - rx) for rx in ridge_xs)
                response = float(np.clip(np.exp(-12 * min_dist**2)
                                         + rng.uniform(-0.1, 0.1), 0, 1))
                col  = interpolate_color(ManimColor(BG_COLOR), ManimColor(BIT_COLOR), response)
                cell = Rectangle(
                    width=cell_w * 0.86, height=cell_h * 0.86,
                    fill_color=col, fill_opacity=0.30 + response * 0.65,
                    stroke_color=MUTED_TEXT_COLOR, stroke_width=0.7
                ).move_to(np.array([cx0 + c * cell_w, cy0 - r * cell_h, 0]))
                cells.add(cell)
        return cells

    def _build_mini_strip(self, center, width: float, height: float) -> VGroup:
        # Build around ORIGIN first to prevent movement bugs
        fill   = Rectangle(width=width, height=height,
                           fill_color=PLANE_COLOR, fill_opacity=0.15, stroke_width=0)
        border = Rectangle(width=width, height=height,
                           color=PHASE_COLOR, stroke_width=2.5, fill_opacity=0)
        ridge_xs = np.linspace(-width * 0.4, width * 0.4, 7)
        lines = VGroup()
        for rx in ridge_xs:
            lines.add(Line(
                np.array([rx, -height*0.44, 0]),
                np.array([rx, height*0.44, 0]),
                color=TEXT_COLOR, stroke_width=3.0, stroke_opacity=0.6
            ))
        grp = VGroup(fill, border, lines)
        grp.move_to(np.array([center[0], center[1], 0]))
        return grp

    def _build_iriscode_matrix(self, rows: int, cols: int, center) -> VGroup:
        rng    = np.random.default_rng(seed=42)
        cell_w, cell_h = 0.18, 0.22  # Tightened dimensions
        w  = cols * cell_w
        h  = rows * cell_h
        cx0 = center[0] - w / 2 + cell_w / 2
        cy0 = center[1] + h / 2 - cell_h / 2
        cells = VGroup()
        for r in range(rows):
            for c in range(cols):
                bit = int(rng.integers(0, 2))
                col = BIT_COLOR if bit == 1 else MUTED_TEXT_COLOR
                txt = Text(str(bit), font=MONO_FONT, font_size=14, color=col)
                txt.move_to(np.array([cx0 + c * cell_w, cy0 - r * cell_h, 0]))
                cells.add(txt)
                
        border = SurroundingRectangle(
            cells, color=BIT_COLOR, stroke_width=2.5,
            fill_color=BG_COLOR, fill_opacity=0.5, buff=0.25
        )
        return VGroup(border, cells)
