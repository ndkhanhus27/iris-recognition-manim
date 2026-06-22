import os
import sys
from manim import *

sys.path.insert(0, os.getcwd())
from src.components.base_scene import BaseScene
from src.components.formulas import *
from src.theme import *

class Scene4Localization(BaseScene):
    """
    Scene 4 — Iris Localization Using Daugman's Integro-Differential Operator
    
    Explains the mathematical model and visually demonstrates the scanning process
    for detecting the pupillary and limbic boundaries using a native vector eye.
    """
    def construct(self):
        # Scene directly starts here (Title was shown at the end of Scene 3)

        # ----------------------------------------------------
        # SHOT 1: Why Localization Matters (0s - 10s)
        # ----------------------------------------------------
        self.play_audio("assets/audios/scene4_localization/1.mp3", fallback_duration=9.0)
        
        # Load vector eye
        eye_image = self.create_vector_eye()
        # Scale to match the previous scale, keep at ORIGIN for initial explanation
        eye_image.scale(0.8)
        
        self.play(FadeIn(eye_image), run_time=1.0)
        
        # Labels cleanly arranged on the right
        labels = VGroup(
            Text("Sclera", font=MAIN_FONT, font_size=SMALL_FONT_SIZE, color=TEXT_COLOR),
            Text("Iris", font=MAIN_FONT, font_size=SMALL_FONT_SIZE, color=SECONDARY_COLOR),
            Text("Pupil", font=MAIN_FONT, font_size=SMALL_FONT_SIZE, color=MUTED_TEXT_COLOR)
        ).arrange(DOWN, buff=1.0).move_to(RIGHT * 4.5 + UP * 0.5)
        
        # Connector lines (accurate)
        sclera_point = eye_image.get_center() + RIGHT * 2.5 + UP * 0.5
        iris_point = eye_image.get_center() + RIGHT * 1.2 + UP * 0.3
        pupil_point = eye_image.get_center() + RIGHT * 0.4 + UP * 0.1
        
        connectors = VGroup(
            Line(labels[0].get_left(), sclera_point, stroke_color=MUTED_TEXT_COLOR, stroke_width=2),
            Line(labels[1].get_left(), iris_point, stroke_color=SECONDARY_COLOR, stroke_width=2),
            Line(labels[2].get_left(), pupil_point, stroke_color=MUTED_TEXT_COLOR, stroke_width=2)
        )
        
        # Add dots
        dots = VGroup(
            Dot(sclera_point, color=MUTED_TEXT_COLOR, radius=0.06),
            Dot(iris_point, color=SECONDARY_COLOR, radius=0.06),
            Dot(pupil_point, color=MUTED_TEXT_COLOR, radius=0.06)
        )

        for l, c, d in zip(labels, connectors, dots):
            self.play(FadeIn(l, shift=LEFT*0.2), Create(c), FadeIn(d), run_time=0.5)
            
        # Question marks around boundaries
        q_inner = Text("?", font=MAIN_FONT, font_size=TITLE_FONT_SIZE, color=WARNING_COLOR, weight=BOLD)
        q_outer = Text("?", font=MAIN_FONT, font_size=TITLE_FONT_SIZE, color=WARNING_COLOR, weight=BOLD)
        q_inner.move_to(eye_image.get_center() + LEFT*0.3 + UP*0.3)
        q_outer.move_to(eye_image.get_center() + RIGHT*1.5 + DOWN*1.5)
        
        self.play(
            FadeIn(q_inner, scale=0.5), 
            FadeIn(q_outer, scale=0.5), 
            run_time=0.8
        )
        self.play(
            q_inner.animate.scale(1.2).set_color(ERROR_COLOR),
            q_outer.animate.scale(1.2).set_color(ERROR_COLOR),
            rate_func=there_and_back, run_time=1.0
        )
        self.wait_audio()
        
        self.play(
            FadeOut(q_inner), FadeOut(q_outer), 
            FadeOut(labels), FadeOut(connectors), FadeOut(dots),
            run_time=0.5
        )
        self.wait(0.5)

        # ----------------------------------------------------
        # SHOT 2: Displaying the Mathematical Model (10s - 20s)
        # ----------------------------------------------------
        self.play_audio("assets/audios/scene4_localization/2.mp3", fallback_duration=7.0)
        
        # Shift eye right and shrink
        self.play(eye_image.animate.scale(0.8).move_to(RIGHT * 3.0), run_time=1.0)
        
        # Daugman Operator Formula (imported from formulas.py)
        formula = MathTex(*FORMULA_DAUGMAN, font_size=46, color=TEXT_COLOR)
        # Center in the left column safely
        formula.move_to(LEFT * 3.5)
        
        self.play(Write(formula), run_time=1.5)
        self.wait(1.0)
        
        # Highlight important symbols with high contrast
        contour = formula[1]      # \oint
        intensity = formula[3]    # I(x,y)
        
        self.play(
            intensity.animate.set_color(PRIMARY_COLOR),
            contour.animate.set_color(SECONDARY_COLOR),
            run_time=1.0
        )
        
        self.wait_audio()
        self.wait(0.5)

        # ----------------------------------------------------
        # SHOT 3: Searching for the Pupil Boundary
        # ----------------------------------------------------
        self.play_audio("assets/audios/scene4_localization/3.mp3", fallback_duration=8.0)
        
        # Candidate Center
        candidate_center = Dot(color=ERROR_COLOR, radius=0.06).move_to(eye_image.get_center() + LEFT*0.5 + UP*0.3)
        center_label = MathTex("(x_0, y_0)", font_size=24, color=ERROR_COLOR).next_to(candidate_center, UP, buff=0.1)
        
        # Scanning circle
        radius_tracker = ValueTracker(0.2)
        center_tracker = ValueTracker(0.0) # Used to offset center slightly
        
        scan_circle = always_redraw(
            lambda: Circle(
                radius=radius_tracker.get_value(),
                color=SUCCESS_COLOR,
                stroke_width=2,
                stroke_opacity=0.8
            ).move_to(candidate_center.get_center() + RIGHT * center_tracker.get_value())
        )
        
        self.play(FadeIn(candidate_center), FadeIn(center_label), run_time=0.5)
        self.add(scan_circle)
        
        # Animate searching behavior
        self.play(
            radius_tracker.animate.set_value(0.6),
            center_tracker.animate.set_value(0.2),
            run_time=2.0, rate_func=there_and_back
        )
        self.play(
            radius_tracker.animate.set_value(1.2),
            center_tracker.animate.set_value(-0.3),
            run_time=2.0, rate_func=there_and_back
        )
        
        self.wait_audio()

        # ----------------------------------------------------
        # SHOT 4: Measuring brightness
        # ----------------------------------------------------
        self.play_audio("assets/audios/scene4_localization/4.mp3", fallback_duration=9.0)
        
        # More searching
        self.play(
            radius_tracker.animate.set_value(0.8),
            center_tracker.animate.set_value(0.4),
            run_time=2.0, rate_func=there_and_back
        )
        
        # Approaching true center slightly
        true_pupil_center = eye_image.get_center()
        
        # Let's show measuring brightness by highlighting the scan circle
        self.play(
            scan_circle.animate.set_stroke(width=4, color=YELLOW),
            run_time=1.0, rate_func=there_and_back
        )
        
        self.play(
            candidate_center.animate.move_to(true_pupil_center + RIGHT*0.1 + UP*0.1),
            center_label.animate.move_to(true_pupil_center + RIGHT*0.1 + UP*0.3),
            center_tracker.animate.set_value(0),
            radius_tracker.animate.set_value(0.4),
            run_time=1.5
        )
        
        self.wait_audio()

        # ----------------------------------------------------
        # SHOT 5: Boundary Locking (Pupil)
        # ----------------------------------------------------
        self.play_audio("assets/audios/scene4_localization/5.mp3", fallback_duration=12.0)
        
        # Approaching true center completely
        self.play(
            candidate_center.animate.move_to(true_pupil_center),
            center_label.animate.move_to(true_pupil_center + UP*0.2),
            run_time=1.0
        )
        
        true_pupil_radius = 0.6 * 0.8 # eye scale is 0.8
        self.play(
            radius_tracker.animate.set_value(true_pupil_radius),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Snap!
        pupil_circle = Circle(radius=true_pupil_radius, color=PRIMARY_COLOR, stroke_width=4).move_to(true_pupil_center)
        pupil_label = Text("Pupillary Boundary", font=MAIN_FONT, font_size=SMALL_FONT_SIZE, color=PRIMARY_COLOR, weight=BOLD)
        pupil_label.next_to(pupil_circle, DOWN, buff=0.2)
        
        lock_icon = self.create_lock_icon().scale(0.3)
        lock_icon.next_to(pupil_circle, RIGHT, buff=0.2)
        
        self.remove(scan_circle)
        self.play(
            ReplacementTransform(scan_circle.copy(), pupil_circle),
            FadeIn(pupil_label, shift=UP*0.2),
            FadeIn(lock_icon, scale=0.5),
            run_time=0.5
        )
        # Pulse effect for "sharp intensity change"
        self.play(
            pupil_circle.animate.set_stroke(width=8, opacity=0.5),
            rate_func=there_and_back, run_time=0.8
        )
        
        self.wait_audio()
        self.play(FadeOut(lock_icon), FadeOut(pupil_label), FadeOut(center_label), run_time=0.5)
        self.wait(0.5)

        # ----------------------------------------------------
        # SHOT 6: Detecting the Outer Iris Boundary
        # ----------------------------------------------------
        self.play_audio("assets/audios/scene4_localization/6.mp3", fallback_duration=11.0)
        
        outer_radius_tracker = ValueTracker(1.0)
        outer_scan_circle = always_redraw(
            lambda: Circle(
                radius=outer_radius_tracker.get_value(),
                color=SUCCESS_COLOR,
                stroke_width=2,
                stroke_opacity=0.6
            ).move_to(true_pupil_center)
        )
        
        self.add(outer_scan_circle)
        self.play(
            outer_radius_tracker.animate.set_value(2.5),
            run_time=2.5, rate_func=rush_from
        )
        
        true_iris_radius = 2.5 * 0.8
        self.play(
            outer_radius_tracker.animate.set_value(true_iris_radius),
            run_time=1.0, rate_func=rate_functions.ease_out_bounce
        )
        
        limbic_circle = Circle(radius=true_iris_radius, color=SECONDARY_COLOR, stroke_width=4).move_to(true_pupil_center)
        limbic_label = Text("Limbic Boundary", font=MAIN_FONT, font_size=SMALL_FONT_SIZE, color=SECONDARY_COLOR, weight=BOLD)
        limbic_label.next_to(limbic_circle, UP, buff=0.2)
        
        lock_icon_2 = self.create_lock_icon().scale(0.3)
        lock_icon_2.next_to(limbic_circle, RIGHT, buff=0.2)

        self.remove(outer_scan_circle)
        self.play(
            ReplacementTransform(outer_scan_circle.copy(), limbic_circle),
            FadeIn(limbic_label, shift=DOWN*0.2),
            FadeIn(lock_icon_2, scale=0.5),
            run_time=0.5
        )
        
        self.wait_audio()
        self.play(FadeOut(lock_icon_2), FadeOut(limbic_label), run_time=0.5)
        self.wait(0.5)

        # ----------------------------------------------------
        # SHOT 7: Handling Occlusion and Reflections
        # ----------------------------------------------------
        self.play_audio("assets/audios/scene4_localization/7.mp3", fallback_duration=12.0)
        
        # Save current scene state to a group so we can split
        main_scene = VGroup(eye_image, pupil_circle, limbic_circle, candidate_center)
        
        # Create vector occlusion eye
        occ_eye = self.create_vector_eye().scale(0.5)
        occ_eye.move_to(LEFT * 3.5 + DOWN * 0.5)
        # Add eyelid polygon (Realistic Intersection Eyelid)
        eyelid_base = Ellipse(width=8.5*0.5, height=5.5*0.5).move_to(occ_eye.get_center())
        eyelid_cutter = Ellipse(width=10.0*0.5, height=6.0*0.5).move_to(occ_eye.get_center() + DOWN*1.5)
        eyelid = Difference(eyelid_base, eyelid_cutter, fill_color="#E5C298", fill_opacity=1, stroke_width=0)
        occ_group = VGroup(occ_eye, eyelid)
        
        # Create vector reflection eye
        refl_eye = self.create_vector_eye().scale(0.5)
        refl_eye.move_to(RIGHT * 3.5 + DOWN * 0.5)
        # Add realistic 4-pane window glare reflection
        glare = VGroup(
            RoundedRectangle(corner_radius=0.02, width=0.15, height=0.15, fill_color=WHITE, fill_opacity=0.9, stroke_width=0).move_to(refl_eye.get_center() + UP*0.2 + RIGHT*0.2),
            RoundedRectangle(corner_radius=0.02, width=0.15, height=0.15, fill_color=WHITE, fill_opacity=0.9, stroke_width=0).move_to(refl_eye.get_center() + UP*0.2 + RIGHT*0.38),
            RoundedRectangle(corner_radius=0.02, width=0.15, height=0.15, fill_color=WHITE, fill_opacity=0.9, stroke_width=0).move_to(refl_eye.get_center() + UP*0.02 + RIGHT*0.2),
            RoundedRectangle(corner_radius=0.02, width=0.15, height=0.15, fill_color=WHITE, fill_opacity=0.9, stroke_width=0).move_to(refl_eye.get_center() + UP*0.02 + RIGHT*0.38)
        ).rotate(PI/12)
        # Add glow around glare
        glare_glow = self.add_glow(glare, color=WHITE, width=20, opacity=0.4)
        refl_group = VGroup(refl_eye, glare_glow)
        
        occ_label = Text("Eyelid Occlusion", font=MAIN_FONT, font_size=SMALL_FONT_SIZE, color=TEXT_COLOR).next_to(occ_eye, UP, buff=0.8)
        refl_label = Text("Specular Reflection", font=MAIN_FONT, font_size=SMALL_FONT_SIZE, color=TEXT_COLOR).next_to(refl_eye, UP, buff=0.8)
        
        # Move main scene out and hide formula to avoid overlaps
        self.play(
            main_scene.animate.scale(0.01).move_to(UP*5).set_opacity(0),
            FadeOut(formula),
            FadeIn(occ_group), FadeIn(refl_group),
            FadeIn(occ_label), FadeIn(refl_label),
            run_time=1.0
        )
        
        # Left Panel (Occlusion) overlays
        occ_iris_radius = 2.5 * 0.5
        top_arc = Arc(radius=occ_iris_radius, start_angle=PI/4, angle=PI/2, color=ERROR_COLOR, stroke_width=6, arc_center=occ_eye.get_center())
        occ_cross = Cross(top_arc, stroke_color=ERROR_COLOR, stroke_width=4).scale(0.5)
        
        # Right Panel (Reflection) overlays
        refl_cross = Cross(stroke_color=ERROR_COLOR, stroke_width=8).scale(0.3).move_to(glare.get_center())
        
        self.play(
            Create(top_arc), Create(occ_cross),
            Create(refl_cross),
            run_time=1.0
        )
        
        self.wait_audio()

        # ----------------------------------------------------
        # SHOT 8: Masking and Final Result
        # ----------------------------------------------------
        self.play_audio("assets/audios/scene4_localization/8.mp3", fallback_duration=10.0)
        
        # Integration path (lateral arcs)
        left_arc = Arc(radius=occ_iris_radius, start_angle=3*PI/4, angle=PI/2, color=SUCCESS_COLOR, stroke_width=5, arc_center=occ_eye.get_center())
        right_arc = Arc(radius=occ_iris_radius, start_angle=-PI/4, angle=PI/2, color=SUCCESS_COLOR, stroke_width=5, arc_center=occ_eye.get_center())
        
        self.play(
            Create(left_arc), Create(right_arc),
            run_time=1.0
        )
        self.wait(1.0)
        
        self.play(
            FadeOut(occ_group), FadeOut(refl_group),
            FadeOut(occ_label), FadeOut(refl_label),
            FadeOut(top_arc), FadeOut(occ_cross), FadeOut(refl_cross),
            FadeOut(left_arc), FadeOut(right_arc),
            run_time=0.8
        )
        
        # Bring main scene back to ORIGIN to avoid formula overlaps
        self.play(
            main_scene.animate.scale(100).move_to(ORIGIN).set_opacity(1),
            run_time=1.0
        )
        
        # Highlight Iris Region beautifully while keeping the original eye visible
        inner_bound = DashedVMobject(Circle(radius=true_pupil_radius, color=PRIMARY_COLOR, stroke_width=4).move_to(pupil_circle.get_center()), num_dashes=30)
        outer_bound = DashedVMobject(Circle(radius=true_iris_radius, color=PRIMARY_COLOR, stroke_width=4).move_to(pupil_circle.get_center()), num_dashes=60)
        
        iris_highlight = Annulus(
            inner_radius=true_pupil_radius, outer_radius=true_iris_radius, 
            color=PRIMARY_COLOR, fill_opacity=0.3, stroke_width=0
        ).move_to(pupil_circle.get_center())
        
        extract_label = Text("Extracted Iris Region", font=MAIN_FONT, font_size=SMALL_FONT_SIZE, color=PRIMARY_COLOR, weight=BOLD).next_to(outer_bound, UP, buff=0.5)
        
        # Restore checkmark as requested
        check_icon = self.create_check_icon(radius=0.8).move_to(RIGHT * 4.0)
        done_text = Text("Localization Complete", font=MAIN_FONT, font_size=SMALL_FONT_SIZE, color=SUCCESS_COLOR).next_to(check_icon, DOWN)
        
        self.play(
            FadeIn(iris_highlight), Create(inner_bound), Create(outer_bound),
            Write(extract_label),
            run_time=1.0
        )
        
        self.play(
            FadeIn(check_icon, scale=0.5), FadeIn(done_text, shift=UP*0.2),
            run_time=0.8
        )
        
        self.wait(1.0)
        
        self.play(
            FadeOut(check_icon), FadeOut(done_text), FadeOut(extract_label),
            run_time=0.5
        )
        
        # Zoom into the highlighted iris region to transition
        # Group everything related to the eye so it scales smoothly together
        eye_group = VGroup(main_scene, iris_highlight, inner_bound, outer_bound, pupil_circle, limbic_circle)
        
        self.play(
            eye_group.animate.scale(4.0).set_opacity(0),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Use the consistent BaseScene title transition
        self.play_scene_title("5. Iris Normalization")
        self.wait_audio()

    # ----------------------------------------------------
    # HELPER METHODS (Native Vector Graphics)
    # ----------------------------------------------------
    def create_lock_icon(self):
        """Creates a native vector lock icon (scene-specific)."""
        body = RoundedRectangle(width=1.0, height=0.8, corner_radius=0.1, fill_color=PRIMARY_COLOR, fill_opacity=1, stroke_width=0)
        shackle = Arc(radius=0.3, start_angle=0, angle=PI, color=TEXT_COLOR, stroke_width=10)
        shackle.next_to(body, UP, buff=-0.1)
        keyhole = Circle(radius=0.1, fill_color=BG_COLOR, fill_opacity=1, stroke_width=0)
        keyhole_base = Polygon(
            keyhole.get_center() + LEFT*0.08 + DOWN*0.05,
            keyhole.get_center() + RIGHT*0.08 + DOWN*0.05,
            keyhole.get_center() + RIGHT*0.15 + DOWN*0.25,
            keyhole.get_center() + LEFT*0.15 + DOWN*0.25,
            fill_color=BG_COLOR, fill_opacity=1, stroke_width=0
        )
        return VGroup(shackle, body, keyhole, keyhole_base)
    # Note: create_check_icon() is inherited from BaseScene.
