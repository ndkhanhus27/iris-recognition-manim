import os
import sys
import numpy as np
from manim import *

sys.path.insert(0, os.getcwd())
from src.components.base_scene import BaseScene
from src.theme import *
from src.components.formulas import (
    FORMULA_HD_NUMERATOR,
    FORMULA_HD_DENOMINATOR,
    FORMULA_HD_NORM,
)

AUDIO_DIR = "assets/audios/scene8_matching"

# ── Color aliases ─────────────────────────────────────────────────────────────
MATCH_COLOR    = SUCCESS_COLOR    # green  — matching bits
MISMATCH_COLOR = ERROR_COLOR      # red    — differing bits
CODE_A_COLOR   = PRIMARY_COLOR    # cyan   — IrisCode A
CODE_B_COLOR   = WARNING_COLOR    # amber  — IrisCode B
MASK_COLOR     = SECONDARY_COLOR  # teal   — valid mask bits
INVALID_COLOR  = "#334155"        # dark slate — masked / invalid bits


class Scene8Matching(BaseScene):
    """
    Scene 8 — Iris Matching via Masked Hamming Distance  (~60 s)

    No opening title card. No transition to Scene 9.

    Shot 1  (0 – 8 s)   Two IrisCodes
    Shot 2  (8 – 20 s)  XOR Bit Comparison
    Shot 3  (20 – 32 s) Noise Masks
    Shot 4  (32 – 40 s) Valid Bit Selection (AND filter)
    Shot 5  (40 – 50 s) Hamming Distance Formula
    Shot 6  (50 – 60 s) Matching Decision
    """

    # ── Sample data: 12 representative bits ──────────────────────────────────
    N      = 12
    CODE_A = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1]
    CODE_B = [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1]
    MASK_A = [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1]   # pos 4: eyelid
    MASK_B = [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1]   # pos 6: eyelash

    def construct(self):
        XOR   = [a ^ b for a, b in zip(self.CODE_A, self.CODE_B)]
        VALID = [ma & mb for ma, mb in zip(self.MASK_A, self.MASK_B)]
        n_dif = sum(x & v for x, v in zip(XOR, VALID))   # 2
        n_val = sum(VALID)                                 # 10
        hd    = n_dif / n_val                              # 0.20

        # ══════════════════════════════════════════════════════════════════════
        # SHOT 1  [Audio 1]  0–8 s
        # Two IrisCodes slide in side by side
        # ══════════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/1.mp3", fallback_duration=8.0)

        title1 = self._sec("Two IrisCodes", CODE_A_COLOR)
        self.play(FadeIn(title1, shift=DOWN * 0.2), run_time=0.5)

        lbl_A, cells_A, row_A = self._row("Code A", self.CODE_A, CODE_A_COLOR)
        lbl_B, cells_B, row_B = self._row("Code B", self.CODE_B, CODE_B_COLOR)
        
        cells_A.move_to(UP * 1.0)
        lbl_A.next_to(cells_A, LEFT, buff=0.4)
        row_A = VGroup(lbl_A, cells_A)
        
        cells_B.move_to(UP * 0.0)
        lbl_B.next_to(cells_B, LEFT, buff=0.4)
        row_B = VGroup(lbl_B, cells_B)

        sfx_A = Tex(r"\textsf{$\cdots$ 2048 bits}", font_size=24, color=MUTED_TEXT_COLOR)
        sfx_B = Tex(r"\textsf{$\cdots$ 2048 bits}", font_size=24, color=MUTED_TEXT_COLOR)
        sfx_A.next_to(cells_A, RIGHT, buff=0.25)
        sfx_B.next_to(cells_B, RIGHT, buff=0.25)

        self.play(FadeIn(row_A, shift=RIGHT * 0.5), run_time=0.7)
        self.play(FadeIn(sfx_A), run_time=0.3)
        self.play(FadeIn(row_B, shift=RIGHT * 0.5), run_time=0.7)
        self.play(FadeIn(sfx_B), run_time=0.3)
        self.wait_audio()

        # ══════════════════════════════════════════════════════════════════════
        # SHOT 2  [Audio 2]  8–20 s
        # Scanning XOR operation — match (green) vs mismatch (red)
        # ══════════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/2.mp3", fallback_duration=12.0)

        title2 = self._sec("XOR Bit Comparison", MISMATCH_COLOR)
        lbl_x, cells_x, row_x = self._row(r"A \oplus B", XOR, MUTED_TEXT_COLOR)
        cells_x.move_to(DOWN * 1.0)
        lbl_x.next_to(cells_x, LEFT, buff=0.4)
        row_x = VGroup(lbl_x, cells_x)

        self.play(
            FadeOut(title1, sfx_A, sfx_B),
            row_A.animate.shift(UP * 0.5),
            row_B.animate.shift(UP * 0.25),
            FadeIn(title2, shift=DOWN * 0.2),
            run_time=0.6
        )
        self.play(FadeIn(row_x, shift=UP * 0.3), run_time=0.5)

        xor_tbl = self._xor_table().move_to(RIGHT * 5.2 + UP * 0.25)
        self.play(FadeIn(xor_tbl), run_time=0.4)

        # Scan: color each bit position according to XOR result
        scan_anims = []
        for i in range(self.N):
            col  = MATCH_COLOR if XOR[i] == 0 else MISMATCH_COLOR
            fill = interpolate_color(ManimColor(BG_COLOR), ManimColor(col), 0.28)
            scan_anims.append(AnimationGroup(
                cells_A[i][0].animate.set_fill(color=fill, opacity=0.88).set_stroke(color=col, width=1.8),
                cells_A[i][1].animate.set_color(col),
                cells_B[i][0].animate.set_fill(color=fill, opacity=0.88).set_stroke(color=col, width=1.8),
                cells_B[i][1].animate.set_color(col),
                cells_x[i][0].animate.set_fill(color=fill, opacity=0.92).set_stroke(color=col, width=1.8),
                cells_x[i][1].animate.set_color(col),
                run_time=0.4
            ))
        self.play(LaggedStart(*scan_anims, lag_ratio=0.82), run_time=5.5)
        self.wait_audio()

        # ══════════════════════════════════════════════════════════════════════
        # SHOT 3  [Audio 3]  20–32 s
        # Noise Masks — eyelid / eyelash occlusion
        # ══════════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/3.mp3", fallback_duration=12.0)

        title3 = self._sec("Noise Masks", MASK_COLOR)
        lbl_mA, cells_mA, row_mA = self._row("Mask A", self.MASK_A, MASK_COLOR, mask=True)
        lbl_mB, cells_mB, row_mB = self._row("Mask B", self.MASK_B, MASK_COLOR, mask=True)
        cells_mA.move_to(UP * 1.25)
        lbl_mA.next_to(cells_mA, LEFT, buff=0.4)
        row_mA = VGroup(lbl_mA, cells_mA)
        
        cells_mB.move_to(DOWN * 1.25)
        lbl_mB.next_to(cells_mB, LEFT, buff=0.4)
        row_mB = VGroup(lbl_mB, cells_mB)

        self.play(
            FadeOut(title2, xor_tbl, row_x),
            row_A.animate.shift(UP * 0.75).set_opacity(0.55),
            row_B.animate.shift(DOWN * 0.5).set_opacity(0.55),
            FadeIn(title3, shift=DOWN * 0.2),
            run_time=0.6
        )
        self.play(FadeIn(row_mA, shift=DOWN * 0.3), run_time=0.6)
        self.play(FadeIn(row_mB, shift=DOWN * 0.3), run_time=0.6)

        # Annotate invalid positions
        note_A = Tex(r"\textsf{eyelid occlusion}", font_size=20, color=MISMATCH_COLOR)
        note_B = Tex(r"\textsf{eyelash interference}", font_size=20, color=MISMATCH_COLOR)
        note_A.next_to(cells_mA[4], UP, buff=0.18)
        note_B.next_to(cells_mB[6], DOWN, buff=0.18)

        self.play(
            cells_mA[4][0].animate.set_stroke(color=MISMATCH_COLOR, width=2.5),
            cells_mA[4][1].animate.set_color(MISMATCH_COLOR),
            FadeIn(note_A),
            run_time=0.5
        )
        self.play(
            cells_mB[6][0].animate.set_stroke(color=MISMATCH_COLOR, width=2.5),
            cells_mB[6][1].animate.set_color(MISMATCH_COLOR),
            FadeIn(note_B),
            run_time=0.5
        )
        self.play(
            cells_A[4].animate.set_opacity(0.18),
            cells_B[6].animate.set_opacity(0.18),
            run_time=0.5
        )
        self.wait_audio()

        # ══════════════════════════════════════════════════════════════════════
        # SHOT 4  [Audio 4]  32–40 s
        # Logical AND of both masks — only valid regions participate
        # ══════════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/4.mp3", fallback_duration=8.0)

        title4 = self._sec("Valid Bit Selection", MASK_COLOR)
        and_fml = MathTex(
            r"\text{mask}_A \cap \text{mask}_B",
            font_size=42, color=MASK_COLOR
        ).move_to(DOWN * 0.2)

        self.play(
            FadeOut(title3, note_A, note_B, row_mA, row_mB),
            row_A.animate.shift(DOWN * 0.45).set_opacity(0.28),
            row_B.animate.shift(UP * 1.05).set_opacity(0.28),
            FadeIn(title4, shift=DOWN * 0.2),
            run_time=0.6
        )
        self.play(FadeIn(and_fml), run_time=0.5)

        lbl_v, cells_v, row_v = self._row("Valid", VALID, MASK_COLOR)
        cells_v.move_to(DOWN * 1.2)
        lbl_v.next_to(cells_v, LEFT, buff=0.4)
        row_v = VGroup(lbl_v, cells_v)
        self.play(FadeIn(row_v, shift=UP * 0.2), run_time=0.6)
        self.play(
            cells_v[4].animate.set_opacity(0.18),
            cells_v[6].animate.set_opacity(0.18),
            run_time=0.4
        )

        n_lbl = Tex(
            rf"\textsf{{\textbf{{n = {n_val} valid bits available for comparison}}}}",
            font_size=28, color=MASK_COLOR
        ).move_to(DOWN * 2.3)
        self.play(FadeIn(n_lbl, shift=UP * 0.1), run_time=0.5)
        self.wait_audio()

        # ══════════════════════════════════════════════════════════════════════
        # SHOT 5  [Audio 5]  40–50 s
        # Hamming Distance formula — numerator / denominator highlighted
        # ══════════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/5.mp3", fallback_duration=10.0)

        title5 = self._sec("Hamming Distance", CODE_A_COLOR)
        self.play(
            FadeOut(title4, row_A, row_B, and_fml, row_v, n_lbl),
            FadeIn(title5, shift=DOWN * 0.2),
            run_time=0.6
        )

        # Build fraction: numer / bar / denom, then place HD= label to the left
        hd_eq  = MathTex(r"HD =", font_size=52, color=CODE_A_COLOR)
        numer  = MathTex(
            FORMULA_HD_NUMERATOR,
            font_size=34, color=MISMATCH_COLOR
        )
        bar    = Line(LEFT * 4.6, RIGHT * 4.6, color=TEXT_COLOR, stroke_width=2.5)
        denom  = MathTex(
            FORMULA_HD_DENOMINATOR,
            font_size=34, color=MATCH_COLOR
        )
        frac   = VGroup(numer, bar, denom).arrange(DOWN, buff=0.35)
        # Position the full formula
        VGroup(hd_eq, frac).arrange(RIGHT, buff=0.5).move_to(UP * 0.7)

        self.play(FadeIn(hd_eq), run_time=0.4)
        self.play(FadeIn(numer, shift=DOWN * 0.2), run_time=0.5)
        self.play(Create(bar), run_time=0.3)

        # Annotate numerator
        n_box  = SurroundingRectangle(numer, color=MISMATCH_COLOR, stroke_width=1.5, buff=0.08)
        n_note = Tex(r"\textsf{Disagreeing Valid Bits}", font_size=22, color=MISMATCH_COLOR)
        n_note.next_to(numer, RIGHT, buff=0.25)
        self.play(Create(n_box), FadeIn(n_note), run_time=0.4)
        self.wait(0.6)
        self.play(FadeOut(n_box, n_note), run_time=0.25)

        self.play(FadeIn(denom, shift=UP * 0.2), run_time=0.5)

        # Annotate denominator
        d_box  = SurroundingRectangle(denom, color=MATCH_COLOR, stroke_width=1.5, buff=0.08)
        d_note = Tex(r"\textsf{Total Valid Bits}", font_size=22, color=MATCH_COLOR)
        d_note.next_to(denom, RIGHT, buff=0.25)
        self.play(Create(d_box), FadeIn(d_note), run_time=0.4)
        self.wait(0.6)
        self.play(FadeOut(d_box, d_note), run_time=0.25)

        # Example result
        example  = MathTex(
            rf"=\ \frac{{{n_dif}}}{{{n_val}}}\ =\ {hd:.2f}",
            font_size=52, color=MATCH_COLOR
        ).next_to(frac, DOWN, buff=0.6)
        real_note = MathTex(
            r"\text{full IrisCode example:} \quad 18 / 225 \approx 0.08",
            font_size=28, color=MUTED_TEXT_COLOR
        ).next_to(example, DOWN, buff=0.3)

        self.play(Write(example), run_time=0.8)
        self.play(FadeIn(real_note), run_time=0.4)
        self.wait_audio()

        # ══════════════════════════════════════════════════════════════════════
        # SHOT 6  [Audio 6]  50–60 s
        # Matching Decision — dynamic HD counter, threshold, verdict
        # ══════════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/6.mp3", fallback_duration=10.0)

        title6 = self._sec("Matching Decision", MATCH_COLOR)
        self.play(
            FadeOut(title5, hd_eq, numer, bar, denom, example, real_note),
            FadeIn(title6, shift=DOWN * 0.2),
            run_time=0.6
        )

        # Number line axis
        axis = NumberLine(
            x_range=[0, 0.55, 0.1], length=9,
            include_numbers=True,
            numbers_to_include=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
            font_size=22, color=MUTED_TEXT_COLOR
        ).move_to(DOWN * 0.25)
        axis_lbl = Tex(r"\textsf{Hamming Distance (HD)}", font_size=24,
                       color=MUTED_TEXT_COLOR).next_to(axis, DOWN, buff=0.22)
        self.play(Create(axis), FadeIn(axis_lbl), run_time=0.6)

        # Threshold marker at 0.32
        t_pt   = axis.number_to_point(0.32)
        t_line = DashedLine(t_pt + UP * 1.5, t_pt + DOWN * 0.9,
                             color=WARNING_COLOR, stroke_width=2.5)
        t_lbl  = MathTex(r"\theta = 0.32", font_size=24, color=WARNING_COLOR)
        t_lbl.next_to(t_line, UP, buff=0.1)
        self.play(Create(t_line), FadeIn(t_lbl), run_time=0.5)

        # ── Animated dot + counter ──────────────────────────────────────────
        hd_vt   = ValueTracker(0.50)

        dot = Dot(radius=0.14, color=MISMATCH_COLOR)
        counter = DecimalNumber(0.50, num_decimal_places=2, font_size=60,
                                color=MISMATCH_COLOR).move_to(UP * 2.0)
        hd_prefix = MathTex(r"HD =", font_size=38, color=MUTED_TEXT_COLOR)
        hd_prefix.next_to(counter, LEFT, buff=0.3)

        def _upd_dot(m):
            v = hd_vt.get_value()
            c = interpolate_color(ManimColor(MATCH_COLOR), ManimColor(MISMATCH_COLOR),
                                  min(v * 2.2, 1.0))
            m.set_color(c).move_to(axis.number_to_point(v))

        def _upd_ctr(m):
            v = hd_vt.get_value()
            c = interpolate_color(ManimColor(MATCH_COLOR), ManimColor(MISMATCH_COLOR),
                                  min(v * 2.2, 1.0))
            m.set_value(v).set_color(c)

        def _upd_pfx(m):
            m.next_to(counter, LEFT, buff=0.3)

        dot.add_updater(_upd_dot)
        counter.add_updater(_upd_ctr)
        hd_prefix.add_updater(_upd_pfx)
        self.add(dot, counter, hd_prefix)

        # Case 1: Same Eye  (0.50 → 0.08)
        self.play(hd_vt.animate.set_value(0.08), run_time=2.2, rate_func=rush_from)
        self.wait(0.3)

        same_lbl = MathTex(r"\text{Same Eye}", font_size=42, color=MATCH_COLOR).move_to(DOWN * 1.7)
        self.play(FadeIn(same_lbl, shift=UP * 0.2), run_time=0.5)
        self.wait(0.9)

        # Case 2: Different Eyes  (0.08 → 0.45)
        self.play(FadeOut(same_lbl), run_time=0.3)
        self.play(hd_vt.animate.set_value(0.45), run_time=1.2, rate_func=smooth)
        self.wait(0.3)

        diff_lbl = MathTex(r"\text{Different Eyes } \times", font_size=42, color=MISMATCH_COLOR).move_to(DOWN * 1.7)
        self.play(FadeIn(diff_lbl, shift=UP * 0.2), run_time=0.5)
        self.wait(0.6)

        # Clear updaters and show brief normalized HD panel
        dot.clear_updaters()
        counter.clear_updaters()
        hd_prefix.clear_updaters()

        norm = self._norm_panel().move_to(DOWN * 3.0)
        self.play(FadeIn(norm), run_time=0.5)
        self.wait_audio()

    # ──────────────────────────────────────────────────────────────────────────
    # HELPER METHODS
    # ──────────────────────────────────────────────────────────────────────────

    def _sec(self, text: str, color: str = None) -> Tex:
        """
        Section subtitle at top of frame.
        Uses Tex with \\textsf{\\textbf{}} for math-safe rendering.
        Delegates positioning to BaseScene._section_title convention (UP * 3.2).
        """
        return Tex(
            rf"\textsf{{\textbf{{{text}}}}}",
            font_size=42, color=color or TEXT_COLOR
        ).move_to(UP * 3.2)

    def _cell(self, bit_val: int, color: str, w: float = 0.52, h: float = 0.52) -> VGroup:
        """Single bit cell: rounded rectangle + digit label."""
        fill = interpolate_color(ManimColor(BG_COLOR), ManimColor(color), 0.22)
        rect = Rectangle(width=w, height=h, fill_color=fill, fill_opacity=0.85,
                         stroke_color=color, stroke_width=1.5)
        lbl  = Text(str(bit_val), font=MAIN_FONT, font_size=24, color=color, weight=BOLD)
        return VGroup(rect, lbl)

    def _row(self, label_text: str, bits, color: str,
             w: float = 0.52, mask: bool = False):
        """
        Returns (label, cells, row_vgroup).
        mask=True: 0-bits rendered in INVALID_COLOR.
        """
        cells = VGroup(*[
            self._cell(b, color if (not mask or b == 1) else INVALID_COLOR, w)
            for b in bits
        ]).arrange(RIGHT, buff=0.06)
        
        if "oplus" in label_text:
            lbl = MathTex(label_text, font_size=34, color=color)
        else:
            lbl = Tex(rf"\textsf{{\textbf{{{label_text}}}}}", font_size=32, color=color)
            
        lbl.next_to(cells, LEFT, buff=0.4)
        return lbl, cells, VGroup(lbl, cells)

    def _xor_table(self) -> VGroup:
        """Compact XOR truth table panel."""
        data = [
            (r"0 \oplus 0 = 0", MATCH_COLOR),
            (r"1 \oplus 1 = 0", MATCH_COLOR),
            (r"0 \oplus 1 = 1", MISMATCH_COLOR),
            (r"1 \oplus 0 = 1", MISMATCH_COLOR),
        ]
        entries = VGroup(*[
            MathTex(t, font_size=24, color=c) for t, c in data
        ]).arrange(DOWN, buff=0.22)
        hdr = MathTex(r"\text{XOR } \oplus", font_size=28, color=MUTED_TEXT_COLOR)
        hdr.next_to(entries, UP, buff=0.25)
        panel = VGroup(hdr, entries)
        bg    = SurroundingRectangle(panel, color=MUTED_TEXT_COLOR, stroke_width=1.5,
                                     fill_color=BG_COLOR, fill_opacity=0.92,
                                     buff=0.25, corner_radius=0.15)
        return VGroup(bg, panel)

    def _norm_panel(self) -> VGroup:
        """Brief normalized Hamming Distance formula panel."""
        formula = MathTex(
            FORMULA_HD_NORM,
            font_size=24, color=MUTED_TEXT_COLOR
        )
        note = Tex(r"\textsf{Statistical normalization for varying valid bit count $n$}",
                   font_size=20, color=MUTED_TEXT_COLOR)
        note.next_to(formula, DOWN, buff=0.14)
        panel = VGroup(formula, note)
        bg    = SurroundingRectangle(panel, color=MUTED_TEXT_COLOR, stroke_width=1,
                                     fill_color=BG_COLOR, fill_opacity=0.92,
                                     buff=0.18, corner_radius=0.12)
        return VGroup(bg, panel)
