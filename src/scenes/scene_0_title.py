import os
import sys
from manim import *

sys.path.insert(0, os.getcwd())
from src.components.base_scene import BaseScene
from src.theme import *

AUDIO_DIR = "assets/audios/scene0_title"

class Scene0Title(BaseScene):
    """
    Scene 0 — Title Scene
    Duration: ~10 seconds
    """

    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # SHOT 1  [Audio 1]
        # Main Title
        # ══════════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/1.mp3", fallback_duration=5.0)

        title = Tex(r"\textsf{\textbf{IRIS RECOGNITION}}", font_size=68, color=PRIMARY_COLOR)
        subtitle = Tex(r"\textsf{Using Daugman's Method}", font_size=40, color=TEXT_COLOR)
        
        main_group = VGroup(title, subtitle).arrange(DOWN, buff=0.6)
        main_group.move_to(ORIGIN)

        self.play(
            FadeIn(main_group, shift=UP * 0.2, scale=0.9),
            run_time=1.5
        )

        # ══════════════════════════════════════════════════════════════════════
        # SHOT 2
        # Academic Information
        course = Tex(r"\textsf{Pattern Recognition}", font_size=28, color=MUTED_TEXT_COLOR)
        student = Tex(r"\textsf{Nguyen Duy Khanh — 23120051}", font_size=28, color=MUTED_TEXT_COLOR)
        
        academic_group = VGroup(course, student).arrange(DOWN, buff=0.3)
        academic_group.move_to(DOWN * 2.5)

        self.play(FadeIn(academic_group), run_time=1.0)
        
        self.wait_audio()

        # ══════════════════════════════════════════════════════════════════════
        # SHOT 3  [Audio 2]
        # Transition to Scene 1
        # ══════════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/2.mp3", fallback_duration=5.0)

        self.play(FadeOut(academic_group), run_time=0.5)

        # Shrink to a glowing node
        node = Dot(color=PRIMARY_COLOR, radius=0.15)
        node_glow = Dot(color=PRIMARY_COLOR, radius=0.4).set_opacity(0.3)
        node_group = VGroup(node_glow, node)

        self.play(
            ReplacementTransform(main_group, node_group),
            run_time=1.0
        )
        self.wait(0.5)

        self.play(FadeOut(node_group), run_time=0.5)
        self.play_scene_title("1. Introduction")
        
        self.wait_audio()
