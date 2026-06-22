from manim import *
import os
import textwrap
from contextlib import contextmanager
from mutagen.mp3 import MP3
import numpy as np
import random
from src.theme import *

class BaseScene(MovingCameraScene):
    def setup(self):
        """Called automatically before construct() in every scene."""
        super().setup()
        self.camera.background_color = BG_COLOR
    def create_title(self, text):
        """Creates a standardized title with a glowing underline."""
        title = Text(text, font=MAIN_FONT, font_size=TITLE_FONT_SIZE, color=TEXT_COLOR, weight=BOLD)
        title.to_corner(UL)
        
        # Glowing underline
        underline = Line(
            start=title.get_corner(DL) + DOWN * 0.1, 
            end=title.get_corner(DR) + DOWN * 0.1,
            color=PRIMARY_COLOR,
            stroke_width=DEFAULT_STROKE_WIDTH
        )
        # Glow effect by adding a thicker, transparent line
        glow = Line(
            start=underline.get_start(),
            end=underline.get_end(),
            color=PRIMARY_COLOR,
            stroke_width=THICK_STROKE_WIDTH,
            stroke_opacity=0.3
        )
        
        return VGroup(glow, underline, title)
        
    def show_subtitle(self, raw_text, audio_file=None):
        """
        Displays a subtitle on the screen and queues the audio.
        Returns the Subtitle VGroup so it can be removed later with self.remove(sub).
        """
        if audio_file:
            self.add_sound(audio_file)
            
        # Wrap text to fit screen
        wrapped_text = "\n".join(textwrap.wrap(raw_text, width=70))
        
        sub = Text(wrapped_text, font=MAIN_FONT, font_size=SUBTITLE_FONT_SIZE, color=TEXT_COLOR)
        
        # Subtle background box for readability over animations
        sub_bg = SurroundingRectangle(sub, color=BLACK, fill_opacity=0.7, stroke_width=0, corner_radius=0.1, buff=0.2)
        sub_group = VGroup(sub_bg, sub)
        sub_group.to_edge(DOWN, buff=0.3)
        
        self.add(sub_group)
        return sub_group

    def add_glow(self, mobject, color=SUCCESS_COLOR, width=10, opacity=0.2):
        """Creates a glowing effect behind a mobject."""
        glow = mobject.copy().set_stroke(color=color, width=width, opacity=opacity)
        sub_group = VGroup(glow, mobject)
        self.add(sub_group)
        return sub_group

    def play_scene_title(self, title_text):
        """Displays a chapter title card before the scene starts."""
        title = Text(title_text, font=MAIN_FONT, font_size=TITLE_FONT_SIZE, color=TEXT_COLOR, weight=BOLD)
        
        # Add a subtle glow
        glow = title.copy().set_stroke(color=PRIMARY_COLOR, width=10, opacity=0.2).set_fill(opacity=0)
        group = VGroup(glow, title)
        
        self.play(FadeIn(group, shift=UP*0.5), run_time=1.0)
        self.wait(1.5)
        self.play(FadeOut(group, shift=UP*0.5), run_time=1.0)
        self.wait(0.5)

    def play_audio(self, audio_file, fallback_duration=5.0):
        """
        Plays an audio file and records its start time and duration for later syncing.
        If the file is missing, it skips the audio and uses fallback_duration for syncing.
        """
        audio_path = os.path.join(os.getcwd(), audio_file)
        if not os.path.exists(audio_path):
            print(f"\n[WARNING] Audio file not found: {audio_path}. Using fallback duration of {fallback_duration}s.\n")
            self.current_audio_duration = fallback_duration
            self.current_audio_start_time = self.renderer.time
            return
            
        self.current_audio_duration = MP3(audio_path).info.length
        self.current_audio_start_time = self.renderer.time
        print(f"[AUDIO] Successfully loaded {audio_path} (Duration: {self.current_audio_duration:.2f}s)")
        self.add_sound(audio_path)

    def wait_audio(self, extra_wait=0.0):
        """
        Waits for the remaining duration of the currently playing audio.
        If the audio has already finished, it only waits for extra_wait.
        """
        if not hasattr(self, 'current_audio_duration'):
            return
            
        elapsed_time = self.renderer.time - self.current_audio_start_time
        remaining_time = self.current_audio_duration - elapsed_time
        
        wait_time = remaining_time + extra_wait
        if wait_time > 0:
            self.wait(wait_time)
        elif extra_wait > 0 and remaining_time <= 0:
            self.wait(extra_wait)

    # ── Shared UI helpers ─────────────────────────────────────────────────────

    def _section_title(self, text: str, color: str = None) -> "Text":
        """
        Centered top-strip section title used across multiple scenes.
        Placed at UP * 3.2 by convention.
        """
        from src.theme import TEXT_COLOR, MAIN_FONT
        color = color or TEXT_COLOR
        return Text(
            text, font=MAIN_FONT, font_size=34,
            color=color, weight=BOLD
        ).move_to(UP * 3.2)

    def create_check_icon(self, radius: float = 0.9) -> "VGroup":
        """
        Native vector check-mark inside a circle.
        Consistent style used in Scene 4 and Scene 5.
        """
        from src.theme import SUCCESS_COLOR
        circle = Circle(
            radius=radius,
            fill_color=SUCCESS_COLOR, fill_opacity=0.18,
            stroke_color=SUCCESS_COLOR, stroke_width=4
        )
        check = VGroup(
            Line(
                LEFT * 0.35 * radius + UP * 0.08 * radius,
                LEFT * 0.08 * radius + DOWN * 0.28 * radius,
                stroke_color=SUCCESS_COLOR, stroke_width=8
            ),
            Line(
                LEFT * 0.08 * radius + DOWN * 0.28 * radius,
                RIGHT * 0.45 * radius + UP * 0.38 * radius,
                stroke_color=SUCCESS_COLOR, stroke_width=8
            )
        ).move_to(circle.get_center())
        return VGroup(circle, check)

    def create_vector_eye(self):
        """Creates a highly detailed grayscale vector representation of an eye."""
        eye_group = VGroup()

        # Sclera (White background) - Reduced width to avoid cartoonish look
        sclera = Ellipse(width=8.5, height=5.5, fill_color="#E0E0E0", fill_opacity=1, stroke_width=0)
        eye_group.add(sclera)

        # Iris base
        iris_radius = 2.5
        iris_base = Circle(radius=iris_radius, fill_color="#3a3a3a", fill_opacity=1, stroke_width=0)
        eye_group.add(iris_base)

        # Iris texture (complex)
        np.random.seed(42) # Consistent pattern
        random.seed(42)
        for _ in range(150):
            angle = random.uniform(0, 2 * PI)
            r_start = random.uniform(0.7, 1.0)
            r_end = random.uniform(1.2, 2.4)
            
            start = np.array([np.cos(angle)*r_start, np.sin(angle)*r_start, 0])
            end = np.array([np.cos(angle)*r_end, np.sin(angle)*r_end, 0])
            
            line = Line(start, end, stroke_width=random.uniform(0.3, 1.5), stroke_color="#808080", stroke_opacity=random.uniform(0.1, 0.5))
            eye_group.add(line)
            
        for _ in range(50):
            angle = random.uniform(0, 2 * PI)
            r_start = random.uniform(1.5, 2.3)
            
            # Draw crypts as elegant thin arcs, not solid dark blobs (avoids creepy/trypophobia look)
            crypt = Ellipse(width=random.uniform(0.1, 0.4), height=random.uniform(0.05, 0.1), fill_opacity=0, stroke_color="#202020", stroke_width=1.5)
            crypt.move_to(np.array([np.cos(angle)*r_start, np.sin(angle)*r_start, 0]))
            crypt.rotate(angle + PI/2)
            eye_group.add(crypt)

        # Pupil
        pupil = Circle(radius=0.6, fill_color=BLACK, fill_opacity=1, stroke_width=0)
        eye_group.add(pupil)

        # Catchlight (Reflection) - Make it smaller, more realistic
        catchlight = Circle(radius=0.08, fill_color=WHITE, fill_opacity=0.8, stroke_width=0)
        catchlight.move_to(RIGHT * 0.4 + UP * 0.4)
        eye_group.add(catchlight)

        return eye_group
