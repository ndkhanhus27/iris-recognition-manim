import os
import sys
import numpy as np
from manim import *

sys.path.insert(0, os.getcwd())
from src.components.base_scene import BaseScene
from src.components.formulas import FORMULA_GABOR_GAUSS, FORMULA_GABOR_SIN
from src.theme import *

# ─── Layout constants ───────────────────────────────────────────────────────
L_COL = LEFT  * 3.4
R_COL = RIGHT * 3.2
AUDIO_DIR = "assets/audios/scene6_feature_extraction"

# ─── Color aliases for readability ──────────────────────────────────────────
GABOR_COLOR    = PRIMARY_COLOR       # cyan
REAL_COLOR     = WARNING_COLOR       # amber
IMAG_COLOR     = ACCENT_COLOR        # purple
ORIENT_COLOR   = SECONDARY_COLOR     # teal
RESPONSE_COLOR = SUCCESS_COLOR       # green
# ─────────────────────────────────────────────────────────────────────────────

class Scene6FeatureExtraction(BaseScene):
    """
    Scene 6 — Feature Extraction using 2D Complex Gabor Wavelets (~60 s)
    """

    def construct(self):
        # ═══════════════════════════════════════════════════════════════════
        # SHOT 1  [Audio 1]
        # Normalized iris strip from Scene 5 appears
        # ═══════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/1.mp3", fallback_duration=6.0)

        title1 = self._section_title("Normalized Iris Texture", color=GABOR_COLOR)

        # Build a deterministic strip with known ridge positions for later
        self.strip_w = 9.0
        self.strip_h = 2.0
        self.ridge_xs = np.linspace(-self.strip_w*0.4, self.strip_w*0.4, 7)
        strip = self._build_norm_strip_known_ridges(width=self.strip_w, height=self.strip_h)
        strip.move_to(ORIGIN + DOWN * 0.3)

        self.play(FadeIn(title1, shift=DOWN * 0.3), run_time=0.5)
        self.play(FadeIn(strip[0]), Create(strip[1]), run_time=0.7)
        self.play(
            LaggedStart(*[Create(ln) for ln in strip[2]], lag_ratio=0.03),
            run_time=0.8
        )
        self.wait_audio()

        # ═══════════════════════════════════════════════════════════════════
        # SHOT 2  [Audio 2]
        # Fix 1: Raw Pixels Are Unreliable (Illumination change)
        # ═══════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/2.mp3", fallback_duration=8.0)

        title2 = self._section_title("Raw Pixels Are Unreliable", color=ERROR_COLOR)

        self.play(
            FadeOut(title1),
            FadeOut(strip),
            FadeIn(title2, shift=DOWN * 0.2),
            run_time=0.6
        )

        patch_a_vals = np.array([
            [120, 118, 121],
            [119, 122, 117],
            [118, 120, 121]
        ])
        patch_b_vals = patch_a_vals + 28  # Brighter

        patch_grp, cell_vg, text_vg = self._build_value_grid(patch_a_vals, cell_size=0.8)
        patch_grp.move_to(ORIGIN + UP * 0.5)

        lbl_same_tex = Text("Same Texture", font=MAIN_FONT, font_size=28, color=SUCCESS_COLOR)
        lbl_diff_pix = Text("Different Pixel Values", font=MAIN_FONT, font_size=28, color=ERROR_COLOR)
        lbl_grp = VGroup(lbl_same_tex, lbl_diff_pix).arrange(DOWN, buff=0.2).next_to(patch_grp, DOWN, buff=0.6)

        self.play(FadeIn(patch_grp, shift=UP*0.2), run_time=0.8)
        self.wait(0.5)

        # Animate illumination change
        new_cells, new_texts = self._build_value_grid_elements(patch_b_vals, cell_size=0.8, center=patch_grp.get_center())
        
        illum_label = Text("Illumination Increase", font=MAIN_FONT, font_size=24, color=WARNING_COLOR).next_to(patch_grp, UP, buff=0.4)
        self.play(
            FadeIn(lbl_same_tex, shift=DOWN*0.1),
            FadeIn(illum_label, shift=DOWN*0.1),
            Transform(cell_vg, new_cells),
            Transform(text_vg, new_texts),
            run_time=1.5
        )
        self.play(FadeIn(lbl_diff_pix, shift=DOWN*0.1), run_time=0.6)
        
        warn_box = self._component_badge("Conclusion: Raw Pixels Are Unreliable", "", ERROR_COLOR)
        warn_box.move_to(DOWN * 2.8)
        self.play(FadeIn(warn_box, shift=UP*0.2), run_time=0.8)
        self.wait_audio()

        # ═══════════════════════════════════════════════════════════════════
        # SHOT 3  [Audio 3]
        # Fix 2: Explain Role of Gabor Components
        # ═══════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/3.mp3", fallback_duration=10.0)

        title3 = self._section_title("2D Complex Gabor Wavelet", color=GABOR_COLOR)

        self.play(
            FadeOut(title2), FadeOut(patch_grp), FadeOut(lbl_grp), FadeOut(warn_box),
            FadeOut(illum_label),
            FadeIn(title3, shift=DOWN * 0.2),
            run_time=0.6
        )

        sep = Line(UP * 2.5, DOWN * 3.0, color=MUTED_TEXT_COLOR, stroke_opacity=0.35).move_to(DOWN*0.2)
        self.play(Create(sep), run_time=0.4)

        # Left col: Formula
        eq_label = Text("G(x, y)  =", font=MAIN_FONT, font_size=34, color=GABOR_COLOR, weight=BOLD).move_to(L_COL + UP * 1.1)

        eq_gauss = MathTex(
            FORMULA_GABOR_GAUSS,
            font_size=36, color=REAL_COLOR
        ).move_to(L_COL + DOWN * 0.05)

        eq_dot = MathTex(r"\times", font_size=44, color=MUTED_TEXT_COLOR).move_to(L_COL + DOWN * 0.95)

        eq_sinusoid = MathTex(
            FORMULA_GABOR_SIN,
            font_size=36, color=IMAG_COLOR
        ).move_to(L_COL + DOWN * 1.95)

        formula_group = VGroup(eq_label, eq_gauss, eq_dot, eq_sinusoid)

        # Right col: Viz with explanatory labels
        gauss_viz = self._build_gaussian_viz(center=R_COL + UP * 1.5, width=3.5, height=1.0)
        gauss_lbl = VGroup(
            Text("Localized Spatial Window", font=MAIN_FONT, font_size=20, color=REAL_COLOR, weight=BOLD),
            Text("Restricts analysis to a local iris region", font=MAIN_FONT, font_size=14, color=MUTED_TEXT_COLOR)
        ).arrange(DOWN, buff=0.05).next_to(gauss_viz, UP, buff=0.1)

        times_txt = MathTex(r"\times", font_size=36, color=MUTED_TEXT_COLOR).move_to(R_COL + UP * 0.6)

        sin_viz = self._build_sinusoid_viz(center=R_COL + DOWN * 0.7, width=3.5, height=1.0)
        sin_lbl = VGroup(
            Text("Frequency Detector", font=MAIN_FONT, font_size=20, color=IMAG_COLOR, weight=BOLD),
            Text("Detects repeating texture patterns", font=MAIN_FONT, font_size=14, color=MUTED_TEXT_COLOR)
        ).arrange(DOWN, buff=0.05).next_to(sin_viz, UP, buff=0.1)

        arrow_down = MathTex(r"\downarrow", font_size=36, color=MUTED_TEXT_COLOR).move_to(R_COL + DOWN * 1.6)

        gabor_viz = self._build_gabor_viz(center=R_COL + DOWN * 2.6, width=3.5, height=1.0)
        gabor_lbl = VGroup(
            Text("Localized Frequency Analyzer", font=MAIN_FONT, font_size=20, color=GABOR_COLOR, weight=BOLD),
            Text("Detects local texture structures\nwhile preserving spatial information", font=MAIN_FONT, font_size=14, color=MUTED_TEXT_COLOR).set_opacity(0.8)
        ).arrange(DOWN, buff=0.05).next_to(gabor_viz, DOWN, buff=0.1)

        self.play(FadeIn(gauss_viz, shift=UP * 0.1), FadeIn(gauss_lbl), Write(eq_gauss), run_time=0.8)
        self.play(FadeIn(times_txt), FadeIn(eq_dot), run_time=0.3)
        self.play(FadeIn(sin_viz, shift=DOWN * 0.1), FadeIn(sin_lbl), Write(eq_sinusoid), run_time=0.8)
        self.play(FadeIn(arrow_down), Write(eq_label), run_time=0.4)
        self.play(FadeIn(gabor_viz, shift=DOWN * 0.1), FadeIn(gabor_lbl), run_time=0.8)
        self.wait_audio()

        # ═══════════════════════════════════════════════════════════════════
        # SHOT 4  [Audio 4]
        # Fix 3: Applying the Gabor Filter (Convolution Demo)
        # ═══════════════════════════════════════════════════════════════════
        # Using audio 4 for this new section, shifting others if needed, 
        # or just combine with existing audio if we have 7 total.
        self.play_audio(f"{AUDIO_DIR}/4.mp3", fallback_duration=8.0)

        title4 = self._section_title("Applying the Gabor Filter", color=GABOR_COLOR)

        self.play(
            FadeOut(title3), FadeOut(sep), FadeOut(formula_group),
            FadeOut(gauss_viz), FadeOut(gauss_lbl), FadeOut(times_txt),
            FadeOut(sin_viz), FadeOut(sin_lbl), FadeOut(arrow_down),
            FadeOut(gabor_viz), FadeOut(gabor_lbl),
            FadeIn(title4, shift=DOWN*0.2),
            run_time=0.6
        )

        # Bring back the strip
        strip.move_to(UP * 0.5)
        self.play(FadeIn(strip), run_time=0.6)

        # Gabor Kernel overlay
        kernel = Ellipse(width=1.2, height=self.strip_h, color=GABOR_COLOR, stroke_width=2, fill_opacity=0.2)
        stripes = VGroup(*[Line(UP*self.strip_h/2, DOWN*self.strip_h/2, color=GABOR_COLOR, stroke_width=1).move_to(kernel.get_center() + RIGHT*k*0.15) for k in [-2,-1,0,1,2]])
        kernel_grp = VGroup(kernel, stripes)
        
        start_x = strip.get_left()[0] + 0.6
        end_x = strip.get_right()[0] - 0.6
        kernel_grp.move_to(np.array([start_x, strip.get_center()[1], 0]))

        lbl_flow = VGroup(
            Text("Texture", font=MAIN_FONT, font_size=22, color=MUTED_TEXT_COLOR),
            MathTex(r"\downarrow", color=MUTED_TEXT_COLOR),
            Text("Sliding Gabor Filter", font=MAIN_FONT, font_size=22, color=GABOR_COLOR)
        ).arrange(DOWN, buff=0.1).next_to(strip, UP, buff=0.15)
        self.play(FadeIn(kernel_grp), FadeIn(lbl_flow), run_time=0.5)

        # Response curve axes
        ax = Axes(
            x_range=[start_x, end_x, 1],
            y_range=[-1, 1, 0.5],
            x_length=end_x - start_x,
            y_length=1.5,
            axis_config={"color": MUTED_TEXT_COLOR, "include_tip": False, "include_ticks": False}
        ).move_to(DOWN * 1.6)
        
        lbl_resp = VGroup(
            MathTex(r"\downarrow", color=MUTED_TEXT_COLOR),
            Text("Response Signal", font=MAIN_FONT, font_size=22, color=RESPONSE_COLOR)
        ).arrange(DOWN, buff=0.1).next_to(ax, UP, buff=0.05)
        
        self.play(Create(ax), FadeIn(lbl_resp), run_time=0.6)

        # Sweep and draw curve
        sweep_vt = ValueTracker(start_x)
        kernel_grp.add_updater(lambda m: m.move_to(np.array([sweep_vt.get_value(), strip.get_center()[1], 0])))
        
        # Pseudo-response function (peaks at ridges)
        def resp_func(x):
            val = 0
            for rx in self.ridge_xs:
                # global x to local strip x
                lx = x - strip.get_center()[0]
                val += np.exp(-15 * (lx - rx)**2) * np.cos(10 * (lx - rx))
            return val * 0.8

        curve = always_redraw(lambda: ax.plot(
            lambda x: resp_func(x),
            x_range=[start_x, sweep_vt.get_value() + 0.01],
            color=RESPONSE_COLOR, stroke_width=3
        ))

        resp_val_txt = always_redraw(lambda: Text(
            f"Response = {resp_func(sweep_vt.get_value()):+.2f}",
            font=MONO_FONT, font_size=18, color=RESPONSE_COLOR
        ).next_to(kernel_grp, UP, buff=0.2))

        self.add(curve, resp_val_txt)
        self.play(sweep_vt.animate.set_value(end_x), run_time=4.0, rate_func=linear)
        kernel_grp.clear_updaters()
        self.remove(resp_val_txt)
        self.wait_audio()

        # ═══════════════════════════════════════════════════════════════════
        # SHOT 5  [Audio 5]
        # Fix 4: Real Component Visualization
        # ═══════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/5.mp3", fallback_duration=9.0)

        title5 = self._section_title("Real Component — Symmetric Texture Response", color=REAL_COLOR)

        self.play(
            FadeOut(title4), FadeOut(lbl_flow), FadeOut(lbl_resp),
            FadeOut(ax), FadeOut(curve), FadeOut(kernel_grp),
            FadeIn(title5, shift=DOWN*0.2),
            run_time=0.6
        )

        strip.generate_target()
        strip.target.move_to(ORIGIN)
        self.play(MoveToTarget(strip), run_time=0.6)

        sweep_x = ValueTracker(strip.get_left()[0])
        sweep_line = always_redraw(lambda: Line(
            np.array([sweep_x.get_value(), strip.get_top()[1], 0]),
            np.array([sweep_x.get_value(), strip.get_bottom()[1], 0]),
            color=REAL_COLOR, stroke_width=3
        ))

        # Highlights only at ridge centers
        ridge_highlights = VGroup()
        for rx in self.ridge_xs:
            gx = strip.get_center()[0] + rx
            hl = Rectangle(width=0.15, height=self.strip_h*0.9, fill_color=REAL_COLOR, fill_opacity=0.6, stroke_width=0).move_to(np.array([gx, strip.get_center()[1], 0]))
            ridge_highlights.add(hl)

        # Reveal highlights as sweep passes
        def hl_updater(m):
            for i, hl in enumerate(ridge_highlights):
                if sweep_x.get_value() >= hl.get_center()[0]:
                    hl.set_opacity(0.6)
                else:
                    hl.set_opacity(0)
        
        ridge_highlights.set_opacity(0)
        self.add(ridge_highlights, sweep_line)
        ridge_highlights.add_updater(hl_updater)

        lbl_real_desc = Text("Strong response where texture matches the symmetric filter pattern", font=MAIN_FONT, font_size=24, color=REAL_COLOR).next_to(strip, DOWN, buff=0.4)
        self.play(FadeIn(lbl_real_desc))

        self.play(sweep_x.animate.set_value(strip.get_right()[0]), run_time=3.5, rate_func=linear)
        ridge_highlights.clear_updaters()
        self.remove(sweep_line)
        self.wait_audio()

        # ═══════════════════════════════════════════════════════════════════
        # SHOT 6  [Audio 6]
        # Fix 5: Imaginary Component Visualization
        # ═══════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/6.mp3", fallback_duration=9.0)

        title6 = self._section_title("Imaginary Component — Texture Transition Response", color=IMAG_COLOR)

        self.play(
            FadeOut(title5), FadeOut(lbl_real_desc), FadeOut(ridge_highlights),
            FadeIn(title6, shift=DOWN*0.2),
            run_time=0.6
        )

        sweep_x.set_value(strip.get_left()[0])
        sweep_line.set_color(IMAG_COLOR)

        # Highlights at transitions (edges of ridges)
        edge_highlights = VGroup()
        for rx in self.ridge_xs:
            gx = strip.get_center()[0] + rx
            # Left edge
            hl_l = Rectangle(width=0.08, height=self.strip_h*0.9, fill_color=IMAG_COLOR, fill_opacity=0.6, stroke_width=0).move_to(np.array([gx - 0.15, strip.get_center()[1], 0]))
            # Right edge
            hl_r = Rectangle(width=0.08, height=self.strip_h*0.9, fill_color=IMAG_COLOR, fill_opacity=0.6, stroke_width=0).move_to(np.array([gx + 0.15, strip.get_center()[1], 0]))
            edge_highlights.add(hl_l, hl_r)

        def edge_hl_updater(m):
            for hl in edge_highlights:
                if sweep_x.get_value() >= hl.get_center()[0]:
                    hl.set_opacity(0.6)
                else:
                    hl.set_opacity(0)
        
        edge_highlights.set_opacity(0)
        self.add(edge_highlights, sweep_line)
        edge_highlights.add_updater(edge_hl_updater)

        lbl_imag_desc = Text("Strong response at local intensity transitions and texture boundaries", font=MAIN_FONT, font_size=24, color=IMAG_COLOR).next_to(strip, DOWN, buff=0.4)
        self.play(FadeIn(lbl_imag_desc))

        self.play(sweep_x.animate.set_value(strip.get_right()[0]), run_time=3.5, rate_func=linear)
        edge_highlights.clear_updaters()
        self.remove(sweep_line)
        self.wait_audio()

        # ═══════════════════════════════════════════════════════════════════
        # SHOT 7  [Audio 7]
        # Fix 6: Simplify Multiple Orientations
        # ═══════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/7.mp3", fallback_duration=8.0)

        title7 = self._section_title("Multi-Orientation Filtering", color=ORIENT_COLOR)

        self.play(
            FadeOut(title6), FadeOut(strip), FadeOut(lbl_imag_desc), FadeOut(edge_highlights),
            FadeIn(title7, shift=DOWN*0.2),
            run_time=0.6
        )

        # Single texture patch in center
        patch = self._build_texture_patch_mixed(width=4.0, height=4.0, center=ORIGIN)
        self.play(FadeIn(patch), run_time=0.6)

        orientations = [
            (0, "Horizontal Filter", "Horizontal Structures"),
            (45, "Diagonal Filter", "Diagonal Structures"),
            (90, "Vertical Filter", "Vertical Structures")
        ]

        lbl_filter = Text("", font=MAIN_FONT, font_size=26, color=ORIENT_COLOR).move_to(UP*2.5)
        lbl_resp2 = Text("", font=MAIN_FONT, font_size=24, color=RESPONSE_COLOR).move_to(DOWN*2.5)
        self.add(lbl_filter, lbl_resp2)

        for ang_deg, f_text, r_text in orientations:
            ang = np.deg2rad(ang_deg)
            
            # Update labels
            self.play(
                Transform(lbl_filter, Text(f"{ang_deg}° — {f_text}", font=MAIN_FONT, font_size=26, color=ORIENT_COLOR, weight=BOLD).move_to(UP*2.5)),
                Transform(lbl_resp2, Text(r_text, font=MAIN_FONT, font_size=24, color=RESPONSE_COLOR).move_to(DOWN*2.5)),
                run_time=0.4
            )

            # Kernel overlay
            shell = Ellipse(width=3.8, height=1.5, color=ORIENT_COLOR, stroke_width=3, fill_opacity=0).rotate(ang)
            stripes = VGroup(*[Line(DOWN*0.7, UP*0.7, color=ORIENT_COLOR, stroke_width=2).move_to(RIGHT*k*0.4) for k in [-3,-2,-1,0,1,2,3]]).rotate(ang)
            kernel_viz = VGroup(shell, stripes)
            
            # Response highlight overlay (lines perpendicular to filter angle)
            resp_lines = VGroup(*[Line(DOWN*1.8, UP*1.8, color=RESPONSE_COLOR, stroke_width=4, stroke_opacity=0.6).move_to(RIGHT*k*0.6).rotate(ang) for k in [-2,-1,0,1,2]])

            self.play(FadeIn(kernel_viz, scale=0.8), run_time=0.5)
            self.play(FadeIn(resp_lines), run_time=0.5)
            self.wait(0.6)
            self.play(FadeOut(kernel_viz), FadeOut(resp_lines), run_time=0.4)

        self.play(FadeOut(patch), FadeOut(lbl_filter), FadeOut(lbl_resp2), run_time=0.5)
        self.wait_audio()

        # ═══════════════════════════════════════════════════════════════════
        # SHOT 8  [Audio 8]
        # Gabor Feature Responses emerging from sweep
        # ═══════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/8.mp3", fallback_duration=6.0)

        title8 = self._section_title("Gabor Feature Responses", color=RESPONSE_COLOR)
        
        self.play(
            FadeOut(title7),
            FadeIn(title8, shift=DOWN*0.2),
            run_time=0.6
        )

        strip.move_to(UP * 1.0)
        self.play(FadeIn(strip), run_time=0.5)

        # Feature map grid below
        feat_map = self._build_feature_map(center=DOWN * 1.0, rows=4, cols=14, cell_w=0.52, cell_h=0.52, ridge_xs=self.ridge_xs, strip_w=self.strip_w)
        
        # Hide all cells initially
        for cell in feat_map:
            cell.set_opacity(0)
            cell.set_stroke(opacity=0)
            
        self.add(feat_map)

        sweep_x3 = ValueTracker(strip.get_left()[0])
        sweep_line3 = always_redraw(lambda: Line(
            np.array([sweep_x3.get_value(), strip.get_top()[1], 0]),
            np.array([sweep_x3.get_value(), strip.get_bottom()[1], 0]),
            color=GABOR_COLOR, stroke_width=4
        ))
        
        self.add(sweep_line3)

        # Update cells based on sweep position
        def map_updater(m):
            # cols = 14
            progress = (sweep_x3.get_value() - strip.get_left()[0]) / strip.get_width()
            col_idx = int(progress * 14)
            for r in range(4):
                for c in range(14):
                    if c <= col_idx:
                        idx = r * 14 + c
                        cell = feat_map[idx]
                        if cell.get_fill_opacity() == 0:
                            # Reveal
                            orig_op = cell.target_opacity
                            cell.set_fill(opacity=orig_op)
                            cell.set_stroke(opacity=0.5)
                            if orig_op > 0.4:
                                cell.set_stroke(color=RESPONSE_COLOR, width=2, opacity=0.9)

        feat_map.add_updater(map_updater)

        self.play(sweep_x3.animate.set_value(strip.get_right()[0]), run_time=3.5, rate_func=linear)
        feat_map.clear_updaters()
        self.remove(sweep_line3)
        self.wait_audio()

        # ═══════════════════════════════════════════════════════════════════
        # SHOT 9  [Audio 9]
        # Transition to Stage 4
        # ═══════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/9.mp3", fallback_duration=4.0)

        all_out = VGroup(strip, feat_map)
        self.play(
            FadeOut(title8),
            all_out.animate.scale(0.0).set_opacity(0),
            run_time=2.5
        )
        self.wait(2.0)  # đợi thêm 2 giây
        self.play_scene_title("7. IrisCode Generation")

        self.wait_audio()
    # ─────────────────────────────────────────────────────────────────────────
    # HELPER METHODS
    # ─────────────────────────────────────────────────────────────────────────

    def _section_title(self, text: str, color: str = None) -> "Text":
        """Delegates to BaseScene._section_title() — kept as alias for compatibility."""
        return super()._section_title(text, color)

    def _build_norm_strip_known_ridges(self, width: float, height: float) -> VGroup:
        fill = Rectangle(width=width, height=height, fill_color=SECONDARY_COLOR, fill_opacity=0.18, stroke_width=0)
        border = Rectangle(width=width, height=height, color=GABOR_COLOR, stroke_width=3, fill_opacity=0)
        
        lines = VGroup()
        # Add background noise lines
        rng = np.random.default_rng(seed=42)
        cx = fill.get_center()
        for _ in range(30):
            x_ = cx[0] + rng.uniform(-width * 0.46, width * 0.46)
            lines.add(Line(
                np.array([x_, cx[1] - height * 0.44, 0]),
                np.array([x_, cx[1] + height * 0.44, 0]),
                color=SECONDARY_COLOR, stroke_width=rng.uniform(0.5, 1.5), stroke_opacity=rng.uniform(0.1, 0.3)
            ))
        # Add prominent ridges
        for rx in self.ridge_xs:
            x_ = cx[0] + rx
            lines.add(Line(
                np.array([x_, cx[1] - height * 0.48, 0]),
                np.array([x_, cx[1] + height * 0.48, 0]),
                color=TEXT_COLOR, stroke_width=3.5, stroke_opacity=0.6
            ))
            
        return VGroup(fill, border, lines)

    def _build_value_grid(self, values: np.ndarray, cell_size: float):
        rows, cols = values.shape
        grid_grp = VGroup()
        cell_vg = VGroup()
        text_vg = VGroup()
        
        w = cols * cell_size
        h = rows * cell_size
        cx0 = -w / 2 + cell_size / 2
        cy0 = h / 2 - cell_size / 2
        
        for r in range(rows):
            for c in range(cols):
                val = values[r, c]
                # Normalize color for viz
                col_val = val / 255.0
                cell = Square(side_length=cell_size * 0.95, fill_color=rgb_to_color([col_val]*3), fill_opacity=1, stroke_color=MUTED_TEXT_COLOR, stroke_width=1)
                cell.move_to(np.array([cx0 + c * cell_size, cy0 - r * cell_size, 0]))
                txt = Text(str(val), font=MONO_FONT, font_size=18, color=TEXT_COLOR if col_val < 0.6 else BLACK).move_to(cell.get_center())
                
                cell_vg.add(cell)
                text_vg.add(txt)
                
        grid_grp.add(cell_vg, text_vg)
        return grid_grp, cell_vg, text_vg

    def _build_value_grid_elements(self, values: np.ndarray, cell_size: float, center):
        rows, cols = values.shape
        cell_vg = VGroup()
        text_vg = VGroup()
        
        w = cols * cell_size
        h = rows * cell_size
        cx0 = center[0] - w / 2 + cell_size / 2
        cy0 = center[1] + h / 2 - cell_size / 2
        
        for r in range(rows):
            for c in range(cols):
                val = values[r, c]
                col_val = val / 255.0
                cell = Square(side_length=cell_size * 0.95, fill_color=rgb_to_color([col_val]*3), fill_opacity=1, stroke_color=MUTED_TEXT_COLOR, stroke_width=1)
                cell.move_to(np.array([cx0 + c * cell_size, cy0 - r * cell_size, 0]))
                txt = Text(str(val), font=MONO_FONT, font_size=18, color=TEXT_COLOR if col_val < 0.6 else BLACK).move_to(cell.get_center())
                
                cell_vg.add(cell)
                text_vg.add(txt)
                
        return cell_vg, text_vg

    def _component_badge(self, name: str, formula_str: str, color: str) -> VGroup:
        name_txt  = Text(name, font=MAIN_FONT, font_size=26, color=color, weight=BOLD)
        content = VGroup(name_txt)
        if formula_str:
            form_txt = MathTex(formula_str, font_size=26, color=color)
            content.add(form_txt)
            content.arrange(DOWN, buff=0.08)
            
        bg = SurroundingRectangle(content, corner_radius=0.2, color=color, stroke_width=2, fill_color=BG_COLOR, fill_opacity=0.9, buff=0.2)
        return VGroup(bg, content)

    def _build_gaussian_viz(self, center, width: float, height: float) -> VGroup:
        axes = Axes(x_range=[-3.2, 3.2, 1], y_range=[0, 1.15, 0.5], x_length=width, y_length=height, axis_config={"color": MUTED_TEXT_COLOR, "stroke_width": 1.5, "include_tip": False, "include_ticks": False}).move_to(center)
        curve = axes.plot(lambda x: np.exp(-0.5 * x ** 2), color=REAL_COLOR, stroke_width=3)
        fill = axes.get_area(curve, x_range=[-3.0, 3.0], color=REAL_COLOR, opacity=0.18)
        return VGroup(axes, fill, curve)

    def _build_sinusoid_viz(self, center, width: float, height: float) -> VGroup:
        axes = Axes(x_range=[-3.2, 3.2, 1], y_range=[-1.2, 1.2, 0.5], x_length=width, y_length=height, axis_config={"color": MUTED_TEXT_COLOR, "stroke_width": 1.5, "include_tip": False, "include_ticks": False}).move_to(center)
        curve = axes.plot(lambda x: np.sin(2.2 * x), color=IMAG_COLOR, stroke_width=3)
        return VGroup(axes, curve)

    def _build_gabor_viz(self, center, width: float, height: float) -> VGroup:
        axes = Axes(x_range=[-3.2, 3.2, 1], y_range=[-1.2, 1.2, 0.5], x_length=width, y_length=height, axis_config={"color": MUTED_TEXT_COLOR, "stroke_width": 1.5, "include_tip": False, "include_ticks": False}).move_to(center)
        curve = axes.plot(lambda x: np.exp(-0.5 * x ** 2) * np.sin(2.2 * x), color=GABOR_COLOR, stroke_width=3)
        return VGroup(axes, curve)

    def _build_texture_patch_mixed(self, width: float, height: float, center) -> VGroup:
        rng = np.random.default_rng(seed=12)
        patch = VGroup()
        border = Rectangle(width=width, height=height, color=MUTED_TEXT_COLOR, stroke_width=2, fill_color=BG_COLOR, fill_opacity=1)
        patch.add(border)
        # Add random mixed lines (horiz, vert, diag)
        for _ in range(40):
            ang = rng.choice([0, np.pi/4, np.pi/2, 3*np.pi/4])
            c, s = np.cos(ang), np.sin(ang)
            r = rng.uniform(0.5, 1.5)
            cx, cy = rng.uniform(-width/2.5, width/2.5), rng.uniform(-height/2.5, height/2.5)
            patch.add(Line(np.array([cx - c*r, cy - s*r, 0]), np.array([cx + c*r, cy + s*r, 0]), color=WHITE, stroke_width=rng.uniform(1, 3), stroke_opacity=rng.uniform(0.1, 0.4)))
        patch.move_to(center)
        return patch

    def _build_feature_map(self, center, rows: int, cols: int, cell_w: float, cell_h: float, ridge_xs=None, strip_w=9.0) -> VGroup:
        rng = np.random.default_rng(seed=31)
        cells = VGroup()
        w = cols * cell_w
        h = rows * cell_h
        cx0 = center[0] - w / 2 + cell_w / 2
        cy0 = center[1] + h / 2 - cell_h / 2

        for r in range(rows):
            for c in range(cols):
                if ridge_xs is not None:
                    x_pos = -strip_w/2 + (c / (cols - 1)) * strip_w
                    min_dist = min([abs(x_pos - rx) for rx in ridge_xs])
                    response = np.exp(-12 * min_dist**2)
                    response = np.clip(response + rng.uniform(-0.1, 0.1), 0, 1)
                else:
                    response = rng.beta(2, 2)
                    
                col = interpolate_color(ManimColor(BG_COLOR), ManimColor(RESPONSE_COLOR), response)
                cell = Rectangle(
                    width=cell_w * 0.88, height=cell_h * 0.88,
                    fill_color=col,
                    stroke_color=MUTED_TEXT_COLOR,
                    stroke_width=0.7
                ).move_to(np.array([cx0 + c * cell_w, cy0 - r * cell_h, 0]))
                # Save target opacity for later animation
                cell.target_opacity = 0.30 + response * 0.65
                cells.add(cell)
        return cells
