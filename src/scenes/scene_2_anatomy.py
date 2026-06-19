import os
import sys
import random
import numpy as np
from manim import *

sys.path.insert(0, os.getcwd())
from src.components.base_scene import BaseScene
from src.theme import *

class Scene2Anatomy(BaseScene):
    def construct(self):
        # Display chapter title
        self.play_scene_title("2. Anatomy of the Iris")

        # ==========================================
        # SETUP: Load Real Image or Draw Vector Eye
        # ==========================================
        image_path = os.path.join(os.getcwd(), "assets", "scene_2_anatomy", "grayscale_eye.png")
        if os.path.exists(image_path):
            eye = ImageMobject(image_path).scale_to_fit_height(config.frame_height)
            is_vector = False
        else:
            eye = self.create_vector_eye()
            is_vector = True

        # ==========================================
        # SHOT 1 — The Grayscale Eye
        # ==========================================
        # Audio 1: "The iris is the thin, circular, pigmented diaphragm..."
        self.play_audio("assets/audios/scene2_anatomy/1.mp3", fallback_duration=8.0)
        
        self.play(FadeIn(eye), run_time=1.5)
        
        # Subtle slow continuous zoom into the iris (less extreme so labels fit)
        self.play(
            self.camera.frame.animate.scale(0.7).move_to(ORIGIN),
            run_time=4.0
        )
        
        self.wait_audio()

        # ==========================================
        # SHOT 2 — Anatomical Breakdown
        # ==========================================
        # Audio 2: "Its highly complex visual texture is formed..."
        self.play_audio("assets/audios/scene2_anatomy/2.mp3", fallback_duration=9.0)

        pupil_radius = 0.6 if is_vector else 0.8
        iris_radius = 2.5 if is_vector else 2.5
        sclera_radius = 4.0 if is_vector else 4.0

        l_pupil = self.create_anatomical_label("Pupil", ORIGIN + UP*pupil_radius, UP*1.2 + RIGHT*0.8)
        l_iris = self.create_anatomical_label("Iris", ORIGIN + RIGHT*(iris_radius - 0.5), RIGHT*1.5 + UP*0.5)
        l_sclera = self.create_anatomical_label("Sclera", ORIGIN + DOWN*(iris_radius + 0.8), DOWN*0.5 + LEFT*1.5)

        anatomy_labels = VGroup(l_pupil, l_iris, l_sclera)
        
        self.play(
            LaggedStart(
                FadeIn(l_pupil, shift=UP*0.2),
                FadeIn(l_iris, shift=UP*0.2),
                FadeIn(l_sclera, shift=UP*0.2),
                lag_ratio=0.3
            ),
            run_time=1.5
        )

        self.wait_audio(extra_wait=-1.0)
        
        # Transition out labels
        self.play(FadeOut(anatomy_labels), run_time=1.0)

        # ==========================================
        # SHOT 3 — Complex Microstructures
        # ==========================================
        # Audio 3: "Consisting of chaotic microstructures like furrows..."
        self.play_audio("assets/audios/scene2_anatomy/3.mp3", fallback_duration=6.0)

        # Highlight iris ring by darkening outer sclera and inner pupil
        outer_darkener = Annulus(
            inner_radius=iris_radius, outer_radius=15,
            fill_color=BLACK, fill_opacity=0.6, stroke_width=0
        )
        inner_darkener = Circle(radius=pupil_radius, fill_color=BLACK, fill_opacity=0.6, stroke_width=0)
        
        self.play(FadeIn(outer_darkener), FadeIn(inner_darkener), run_time=1.0)

        # Scanning glow
        scanner = Circle(radius=pupil_radius, color=PRIMARY_COLOR, stroke_width=5)
        self.play(FadeIn(scanner), run_time=0.5)
        self.play(scanner.animate.scale(iris_radius / pupil_radius).set_stroke(opacity=0), run_time=2.0)
        
        # Points of interest
        crypt_pos = RIGHT * 1.6 + UP * 0.4
        furrow_pos = LEFT * 1.8 + DOWN * 1.2
        corona_pos = UP * 0.9 + LEFT * 0.3

        p_crypt = self.create_micro_label("Crypts", crypt_pos, RIGHT*0.8 + UP*0.5)
        p_furrow = self.create_micro_label("Furrows", furrow_pos, LEFT*0.8 + DOWN*0.5)
        p_corona = self.create_micro_label("Corona", corona_pos, UP*0.8 + LEFT*0.5)

        micro_labels = VGroup(p_crypt, p_furrow, p_corona)

        self.play(
            LaggedStart(
                FadeIn(p_furrow),
                FadeIn(p_crypt),
                FadeIn(p_corona),
                lag_ratio=0.4
            ),
            run_time=2.0
        )

        self.wait_audio(extra_wait=-1.0)
        
        # Transition out micro labels
        self.play(FadeOut(micro_labels), FadeOut(outer_darkener), FadeOut(inner_darkener), FadeOut(scanner), run_time=1.0)

        # ==========================================
        # SHOT 4 — Uniqueness (Left vs Right)
        # ==========================================
        # Audio 4: "...the patterns are so unique that even the left and right eyes..."
        self.play_audio("assets/audios/scene2_anatomy/4.mp3", fallback_duration=9.0)

        # Zoom out back to normal
        self.play(self.camera.frame.animate.scale(1/0.7), run_time=1.5)

        # Duplicate eye
        left_eye = eye
        right_eye = eye.copy()
        
        # Flip the pattern without rotating the sclera
        right_eye.flip(RIGHT)

        scale_factor = 0.65
        shift_amount = 3.2

        self.play(
            left_eye.animate.scale(scale_factor).shift(LEFT * shift_amount),
            FadeIn(right_eye.scale(scale_factor).shift(RIGHT * shift_amount)),
            run_time=1.5
        )

        lbl_left = Text("Left Eye", font=MAIN_FONT, font_size=SMALL_FONT_SIZE, color=TEXT_COLOR).next_to(left_eye, DOWN, buff=0.3)
        lbl_right = Text("Right Eye", font=MAIN_FONT, font_size=SMALL_FONT_SIZE, color=TEXT_COLOR).next_to(right_eye, DOWN, buff=0.3)
        
        neq = Text("≠", font=MAIN_FONT, font_size=TITLE_FONT_SIZE, color=PRIMARY_COLOR, weight=BOLD).move_to(ORIGIN)
        
        # Independent features layout
        indep = Text("Independent Features", font=MAIN_FONT, font_size=SMALL_FONT_SIZE, color=SUCCESS_COLOR).move_to(DOWN * 2.8)
        
        # Elegant arrows connecting the concept
        arrow_left = Arrow(start=indep.get_top() + LEFT*0.5, end=lbl_left.get_bottom(), color=SUCCESS_COLOR, stroke_width=2, max_tip_length_to_length_ratio=0.1)
        arrow_right = Arrow(start=indep.get_top() + RIGHT*0.5, end=lbl_right.get_bottom(), color=SUCCESS_COLOR, stroke_width=2, max_tip_length_to_length_ratio=0.1)

        self.play(
            FadeIn(lbl_left), FadeIn(lbl_right),
            run_time=0.8
        )
        self.play(Write(neq), run_time=0.5)
        self.play(
            FadeIn(indep, shift=UP*0.2),
            Create(arrow_left), Create(arrow_right),
            run_time=1.0
        )

        self.wait_audio(extra_wait=-1.5)

        # Final fade to black
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=1.5
        )

    # ----------------------------------------------------
    # Helper Methods
    # ----------------------------------------------------

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

    def create_anatomical_label(self, text_str, start_point, offset):
        """Creates an elegant line and text label for anatomy."""
        end_point = start_point + offset
        
        line = Line(start=start_point, end=end_point, color=PRIMARY_COLOR, stroke_width=1.5)
        dot = Dot(start_point, color=PRIMARY_COLOR, radius=0.04)
        
        lbl = Text(text_str, font=MAIN_FONT, font_size=int(SMALL_FONT_SIZE*0.9), color=PRIMARY_COLOR, weight=BOLD)
        
        if offset[0] >= 0:
            lbl.next_to(line.get_end(), RIGHT, buff=0.1)
        else:
            lbl.next_to(line.get_end(), LEFT, buff=0.1)
            
        return VGroup(dot, line, lbl)

    def create_micro_label(self, text_str, point, offset):
        """Creates a pointer for microstructures without large circles."""
        end_point = point + offset
        
        dot = Dot(point, color=PRIMARY_COLOR, radius=0.04)
        line = DashedLine(start=point, end=end_point, color=PRIMARY_COLOR, stroke_width=1.5)
        
        lbl = Text(text_str, font=MAIN_FONT, font_size=int(SMALL_FONT_SIZE*0.9), color=PRIMARY_COLOR, weight=BOLD)
        
        if offset[0] >= 0:
            lbl.next_to(line.get_end(), RIGHT, buff=0.1)
        else:
            lbl.next_to(line.get_end(), LEFT, buff=0.1)
        
        return VGroup(dot, line, lbl)
