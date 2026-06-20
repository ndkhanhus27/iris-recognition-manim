import os
import sys
from manim import *

sys.path.insert(0, os.getcwd())
from src.components.base_scene import BaseScene
from src.theme import *

AUDIO_DIR = "assets/audios/scene9_evaluation"

class Scene9Evaluation(BaseScene):
    """
    Scene 9 — System Evaluation: Advantages and Limitations
    Duration: ~30 seconds
    """

    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # SHOT 0  [Audio 1]
        # Scene Title & Transition
        # ══════════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/1.mp3", fallback_duration=8.0)
        self.play_scene_title("9. System Evaluation")

        # ══════════════════════════════════════════════════════════════════════
        # SHOT 1
        # Top Title Fade-in
        # ══════════════════════════════════════════════════════════════════════
        # Title
        title = Tex(r"\textsf{\textbf{System Evaluation}}", font_size=52, color=TEXT_COLOR)
        title.move_to(UP * 3.2)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.6)
        
        self.wait_audio()

        # ══════════════════════════════════════════════════════════════════════
        # SHOT 2  [Audio 2 & 3]  8–30 s
        # Comparison Board
        # ══════════════════════════════════════════════════════════════════════
        
        # Headers
        adv_title = Tex(r"\textsf{\textbf{Advantages}}", font_size=44, color=SUCCESS_COLOR)
        lim_title = Tex(r"\textsf{\textbf{Limitations}}", font_size=44, color=ERROR_COLOR)
        
        adv_title.move_to(LEFT * 3.5 + UP * 2.0)
        lim_title.move_to(RIGHT * 3.5 + UP * 2.0)
        
        divider = Line(UP * 2.2, DOWN * 3.0, color=MUTED_TEXT_COLOR, stroke_width=2).set_opacity(0.4)

        self.play_audio(f"{AUDIO_DIR}/2.mp3", fallback_duration=5.0)
        
        self.play(
            FadeIn(adv_title, shift=UP * 0.2),
            FadeIn(lim_title, shift=UP * 0.2),
            Create(divider),
            run_time=0.8
        )

        # Advantages Points
        adv1 = self._point(r"\checkmark", "Exceptional Accuracy", "Very low False Accept Rate", SUCCESS_COLOR)
        adv2 = self._point(r"\checkmark", "Lifelong Stability", "Texture remains highly stable", SUCCESS_COLOR)
        adv3 = self._point(r"\checkmark", "Difficult to Forge", "Micro-texture is hard to replicate", SUCCESS_COLOR)

        advs = VGroup(adv1, adv2, adv3).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        advs.next_to(adv_title, DOWN, buff=0.8).align_to(adv_title, LEFT).shift(LEFT * 1.5)

        self.play(FadeIn(adv1, shift=RIGHT * 0.2), run_time=0.6)
        self.wait_audio()
        
        self.play_audio(f"{AUDIO_DIR}/3.mp3", fallback_duration=4.0)
        self.play(FadeIn(adv2, shift=RIGHT * 0.2), run_time=0.6)
        self.wait_audio()
        
        self.play_audio(f"{AUDIO_DIR}/4.mp3", fallback_duration=5.0)
        self.play(FadeIn(adv3, shift=RIGHT * 0.2), run_time=0.6)
        self.wait_audio()

        # Limitations Points
        lim1 = self._point(r"\times", "Specialized Hardware", "Requires near-infrared imaging", ERROR_COLOR)
        lim2 = self._point(r"\times", "Capture Sensitivity", "Reflections and off-angle views", ERROR_COLOR)
        lim3 = self._point(r"\times", "User Cooperation", "Active positioning required", ERROR_COLOR)

        lims = VGroup(lim1, lim2, lim3).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        lims.next_to(lim_title, DOWN, buff=0.8).align_to(lim_title, LEFT).shift(LEFT * 1.5)

        self.play_audio(f"{AUDIO_DIR}/5.mp3", fallback_duration=5.0)
        self.play(FadeIn(lim1, shift=LEFT * 0.2), run_time=0.6)
        self.wait_audio()
        
        self.play_audio(f"{AUDIO_DIR}/6.mp3", fallback_duration=4.0)
        self.play(FadeIn(lim2, shift=LEFT * 0.2), run_time=0.6)
        self.wait_audio()
        
        self.play_audio(f"{AUDIO_DIR}/7.mp3", fallback_duration=5.0)
        self.play(FadeIn(lim3, shift=LEFT * 0.2), run_time=0.6)
        self.wait_audio()
        
        # ══════════════════════════════════════════════════════════════════════
        # SHOT 3  [Outro]
        # Final Summary
        # ══════════════════════════════════════════════════════════════════════
        
        self.play(
            FadeOut(adv_title, lim_title, divider, advs, lims, title),
            run_time=0.8
        )
        
        self.play_audio(f"{AUDIO_DIR}/8.mp3", fallback_duration=6.0)

        summary = Tex(
            r"\textsf{\textbf{One of the most accurate biometric technologies ever developed.}}",
            font_size=42, color=PRIMARY_COLOR
        )
        self.play(FadeIn(summary, shift=UP * 0.2), run_time=1.0)
        
        self.wait_audio()
        
        self.play(FadeOut(summary), run_time=0.3)


    # ──────────────────────────────────────────────────────────────────────────
    # HELPER METHODS
    # ──────────────────────────────────────────────────────────────────────────

    def _point(self, icon_tex: str, title: str, desc: str, color: str) -> VGroup:
        """Create a bullet point with an icon, title, and description."""
        icon = MathTex(icon_tex, font_size=38, color=color)
        t_title = Tex(rf"\textsf{{\textbf{{{title}}}}}", font_size=32, color=TEXT_COLOR)
        t_desc = Tex(rf"\textsf{{{desc}}}", font_size=24, color=MUTED_TEXT_COLOR)
        
        text_group = VGroup(t_title, t_desc).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        point_group = VGroup(icon, text_group).arrange(RIGHT, aligned_edge=UP, buff=0.3)
        return point_group
