from manim import *
import os
import textwrap
from contextlib import contextmanager
from mutagen.mp3 import MP3
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
        self.add_sound(audio_file)

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
