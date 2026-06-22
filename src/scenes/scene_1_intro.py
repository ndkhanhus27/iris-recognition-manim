from manim import *
import sys
import os

sys.path.insert(0, os.getcwd())
from src.theme import *
from src.components.base_scene import BaseScene


class Scene1Intro(BaseScene):
    """
    Scene 1 — The Rise of Iris Biometrics (~35s)

    3 Shots:
        Shot 1 (0s-10s):  Traditional Authentication — password field + smart card
        Shot 2 (10s-22s): Birth of Biometrics — WHO YOU ARE → SVG icons
        Shot 3 (22s-35s): Focus on the Iris — zoom, scan rings, annotations
    
    All objects are VMobject (VGroup-compatible).
    SVG assets loaded from assets/images/scene1_intro/.
    No raster images. No pipeline.
    """

    # ─────────────────────────────────────────────
    # HELPER: Password Login Field
    # ─────────────────────────────────────────────
    def create_password_field(self):
        """Draws a realistic password login form using Manim shapes."""
        # Outer card
        container = RoundedRectangle(
            width=5.0, height=3.2, corner_radius=0.2,
            fill_color="#0D1B2A", fill_opacity=0.95,
            stroke_color=MUTED_TEXT_COLOR, stroke_width=1,
        )

        # Lock icon (circle arc + rectangle body)
        lock_body = RoundedRectangle(
            width=0.4, height=0.3, corner_radius=0.04,
            fill_color=MUTED_TEXT_COLOR, fill_opacity=0.5,
            stroke_color=MUTED_TEXT_COLOR, stroke_width=1.5,
        )
        lock_arc = Arc(
            radius=0.15, start_angle=0, angle=PI,
            stroke_color=MUTED_TEXT_COLOR, stroke_width=2,
        )
        lock_arc.next_to(lock_body, UP, buff=0)
        lock_icon = VGroup(lock_body, lock_arc)
        lock_icon.move_to(container.get_top() + DOWN * 0.55)

        # Title
        title = Text("Sign In", font=MAIN_FONT, font_size=int(BODY_FONT_SIZE * 0.8),
                      color=TEXT_COLOR, weight=BOLD)
        title.next_to(lock_icon, DOWN, buff=0.25)

        # Input field background
        field_bg = RoundedRectangle(
            width=3.8, height=0.55, corner_radius=0.08,
            fill_color=WHITE, fill_opacity=0.05,
            stroke_color=MUTED_TEXT_COLOR, stroke_width=1,
        )
        field_bg.next_to(title, DOWN, buff=0.45)

        # "Password" placeholder label
        field_label = Text("Password", font=MAIN_FONT,
                           font_size=int(SMALL_FONT_SIZE * 0.7),
                           color=MUTED_TEXT_COLOR)
        field_label.next_to(field_bg, UP, buff=0.1, aligned_edge=LEFT)

        # Password dots
        dots = Text("●  ●  ●  ●  ●  ●  ●", font=MAIN_FONT,
                     font_size=int(SMALL_FONT_SIZE * 0.5), color=TEXT_COLOR)
        dots.move_to(field_bg)

        # Cursor blink line
        cursor = Line(
            UP * 0.18, DOWN * 0.18,
            stroke_color=PRIMARY_COLOR, stroke_width=2,
        )
        cursor.next_to(dots, RIGHT, buff=0.15)

        return VGroup(container, lock_icon, title, field_bg, field_label, dots, cursor)

    # ─────────────────────────────────────────────
    # HELPER: Smart Card
    # ─────────────────────────────────────────────
    def create_smart_card(self):
        """Draws a realistic smart card with EMV chip using Manim shapes."""
        # Card body
        card = RoundedRectangle(
            width=4.2, height=2.7, corner_radius=0.15,
            fill_color="#0D1B2A", fill_opacity=0.95,
            stroke_color=MUTED_TEXT_COLOR, stroke_width=1,
        )

        # EMV Chip
        chip = RoundedRectangle(
            width=0.6, height=0.45, corner_radius=0.05,
            fill_color="#C9A94E", fill_opacity=0.7,
            stroke_color="#DAA520", stroke_width=1,
        )
        chip.move_to(card.get_center() + LEFT * 1.1 + UP * 0.45)

        # Chip contact pattern (horizontal + vertical lines)
        chip_lines = VGroup()
        for i in range(3):
            h = Line(LEFT * 0.25, RIGHT * 0.25,
                     stroke_color="#DAA520", stroke_width=0.6)
            h.move_to(chip.get_center() + UP * (i - 1) * 0.12)
            chip_lines.add(h)
        v = Line(UP * 0.18, DOWN * 0.18,
                 stroke_color="#DAA520", stroke_width=0.6)
        v.move_to(chip.get_center())
        chip_lines.add(v)

        # Contactless NFC symbol (3 arcs)
        nfc = VGroup()
        for r in [0.13, 0.22, 0.31]:
            arc = Arc(radius=r, start_angle=PI / 4, angle=PI / 2,
                      stroke_color=MUTED_TEXT_COLOR, stroke_width=1,
                      stroke_opacity=0.5)
            nfc.add(arc)
        nfc.move_to(card.get_center() + RIGHT * 1.3 + UP * 0.45)

        # Card label
        card_label = Text("SMART CARD", font=MAIN_FONT,
                          font_size=int(SMALL_FONT_SIZE * 0.75),
                          color=MUTED_TEXT_COLOR)
        card_label.move_to(card.get_center() + DOWN * 0.7)

        # Fake card number dots
        num_dots = Text("●●●●   ●●●●   ●●●●   1234", font=MONO_FONT,
                        font_size=int(SMALL_FONT_SIZE * 0.4),
                        color=MUTED_TEXT_COLOR)
        num_dots.move_to(card.get_center() + DOWN * 0.15)

        return VGroup(card, chip, chip_lines, nfc, card_label, num_dots)

    # ─────────────────────────────────────────────
    # HELPER: Detailed Iris Graphic (Vector)
    # ─────────────────────────────────────────────
    def create_iris_graphic(self, center=ORIGIN, base_radius=2.0):
        """Draws a detailed concentric-ring iris pattern, pure vector."""
        rings = VGroup()

        # Pupil
        pupil = Circle(
            radius=base_radius * 0.15,
            fill_color="#050510", fill_opacity=1,
            stroke_color=PRIMARY_COLOR, stroke_width=1.5, stroke_opacity=0.6,
        ).move_to(center)
        rings.add(pupil)

        # Iris rings with varying opacity
        for ratio, sw, op in [
            (0.22, 2.0, 0.8), (0.35, 1.5, 0.6), (0.50, 1.2, 0.5),
            (0.65, 1.0, 0.4), (0.80, 0.8, 0.3), (0.95, 2.5, 0.7),
        ]:
            ring = Circle(
                radius=base_radius * ratio,
                stroke_color=PRIMARY_COLOR, stroke_width=sw, stroke_opacity=op,
                fill_opacity=0,
            ).move_to(center)
            rings.add(ring)

        # Radial texture lines
        for angle in range(0, 360, 12):
            rad = angle * DEGREES
            start = center + base_radius * 0.18 * (np.cos(rad) * RIGHT + np.sin(rad) * UP)
            end = center + base_radius * 0.92 * (np.cos(rad) * RIGHT + np.sin(rad) * UP)
            line = Line(
                start=start, end=end,
                stroke_color=PRIMARY_COLOR, stroke_width=0.4,
                stroke_opacity=0.12 + 0.08 * abs(np.sin(rad)),
            )
            rings.add(line)

        return rings

    # ═════════════════════════════════════════════
    # MAIN CONSTRUCT
    # ═════════════════════════════════════════════
    def construct(self):
        # ==========================================
        # SHOT 1 — Traditional Authentication
        # ==========================================

        pwd_field = self.create_password_field()
        smart_card = self.create_smart_card()

        auth_group = VGroup(pwd_field, smart_card).arrange(RIGHT, buff=1.5)
        auth_group.move_to(ORIGIN + UP * 0.5)

        # ── Audio 1a: "In modern security architectures..." ──
        self.play_audio("assets/audios/scene1_intro/1a.mp3")

        self.play(
            FadeIn(pwd_field, shift=UP * 0.3),
            FadeIn(smart_card, shift=UP * 0.3),
            run_time=DEFAULT_RUN_TIME,
        )
        self.wait_audio()

        # ── Audio 1b: "Passwords can be forgotten..." ──
        self.play_audio("assets/audios/scene1_intro/1b.mp3")

        pwd_vuln = Text("Can be Forgotten", font=MAIN_FONT,
                        font_size=SMALL_FONT_SIZE, color=ERROR_COLOR)
        pwd_vuln.next_to(pwd_field, DOWN, buff=1.0)
        pwd_arrow = Arrow(
            start=pwd_field.get_bottom(), end=pwd_vuln.get_top(),
            color=ERROR_COLOR, stroke_width=DEFAULT_STROKE_WIDTH,
            buff=0.1, max_tip_length_to_length_ratio=0.2,
        )

        self.play(Create(pwd_arrow), run_time=0.8)
        self.play(FadeIn(pwd_vuln), run_time=FAST_RUN_TIME)
        self.wait(0.3)

        card_vuln = Text("Can be Lost", font=MAIN_FONT,
                         font_size=SMALL_FONT_SIZE, color=ERROR_COLOR)
        card_vuln.next_to(smart_card, DOWN, buff=1.0)
        card_arrow = Arrow(
            start=smart_card.get_bottom(), end=card_vuln.get_top(),
            color=ERROR_COLOR, stroke_width=DEFAULT_STROKE_WIDTH,
            buff=0.1, max_tip_length_to_length_ratio=0.2,
        )

        self.play(Create(card_arrow), run_time=0.8)
        self.play(FadeIn(card_vuln), run_time=FAST_RUN_TIME)
        self.wait_audio()

        # Transition: converge to center dot
        all_shot1 = VGroup(pwd_field, smart_card, pwd_arrow, card_arrow, pwd_vuln, card_vuln)
        center_dot = Circle(
            radius=0.1, color=PRIMARY_COLOR,
            fill_opacity=SOLID_FILL_OPACITY, stroke_width=0,
        ).move_to(ORIGIN)

        self.play(ReplacementTransform(all_shot1, center_dot), run_time=1.5)
        self.wait(0.3)

        # ==========================================
        # SHOT 2 — Birth of Biometrics
        # ==========================================

        # ── Audio 2a: "Biometric authentication addresses..." ──
        self.play_audio("assets/audios/scene1_intro/2a.mp3")

        who_text = Text(
            "WHO YOU ARE", font=MAIN_FONT,
            font_size=int(TITLE_FONT_SIZE * 1.5),
            color=SUCCESS_COLOR, weight=BOLD,
        )
        who_glow = who_text.copy().set_stroke(
            color=SUCCESS_COLOR, width=12, opacity=0.25
        ).set_fill(opacity=0)
        who_group = VGroup(who_glow, who_text)

        self.play(FadeOut(center_dot), FadeIn(who_group, scale=0.5), run_time=DEFAULT_RUN_TIME)
        self.wait_audio()
        self.play(FadeOut(who_group), run_time=FAST_RUN_TIME)

        # ── Audio 2b: "Among these natural traits..." ──
        self.play_audio("assets/audios/scene1_intro/2b.mp3")

        fingerprint_svg = SVGMobject("assets/images/scene1_intro/fingerprint.svg")
        fingerprint_svg.set_color(SECONDARY_COLOR).scale_to_fit_height(2.0)

        face_svg = SVGMobject("assets/images/scene1_intro/face.svg")
        face_svg.set_color(SECONDARY_COLOR).scale_to_fit_height(2.0)

        iris_svg = SVGMobject("assets/images/scene1_intro/iris.svg")
        iris_svg.set_color(PRIMARY_COLOR).scale_to_fit_height(2.0)

        fp_label = Text("Fingerprint", font=MAIN_FONT, font_size=SMALL_FONT_SIZE, color=TEXT_COLOR)
        face_label = Text("Face", font=MAIN_FONT, font_size=SMALL_FONT_SIZE, color=TEXT_COLOR)
        iris_label = Text("Iris", font=MAIN_FONT, font_size=SMALL_FONT_SIZE, color=PRIMARY_COLOR)

        fp_group = VGroup(fingerprint_svg, fp_label).arrange(DOWN, buff=0.3)
        face_group = VGroup(face_svg, face_label).arrange(DOWN, buff=0.3)
        iris_group = VGroup(iris_svg, iris_label).arrange(DOWN, buff=0.3)

        iris_group.move_to(UP * 1.2)
        fp_group.move_to(DOWN * 1.2 + LEFT * 3.5)
        face_group.move_to(DOWN * 1.2 + RIGHT * 3.5)

        bio_groups = VGroup(fp_group, face_group, iris_group)

        for g in bio_groups:
            g.save_state()
            g.move_to(ORIGIN).scale(0.01).set_opacity(0)

        self.play(
            LaggedStart(*[g.animate.restore() for g in bio_groups], lag_ratio=0.3),
            run_time=1.5,
        )
        self.wait(0.8)

        bio_frame = RoundedRectangle(
            width=config.frame_width * 0.78, height=config.frame_height * 0.68,
            corner_radius=0.2,
            stroke_color=SECONDARY_COLOR, stroke_width=THIN_STROKE_WIDTH,
            fill_opacity=0,
        ).move_to(ORIGIN)

        bio_frame_glow = bio_frame.copy().set_stroke(
            color=SUCCESS_COLOR, width=6, opacity=0.12
        )

        bio_title = Text(
            "BIOMETRICS", font=MAIN_FONT,
            font_size=int(TITLE_FONT_SIZE * 1.3),
            color=PRIMARY_COLOR, weight=BOLD,
        )
        bio_title.next_to(bio_frame, UP, buff=0.3)
        bio_title_glow = bio_title.copy().set_stroke(
            color=PRIMARY_COLOR, width=10, opacity=0.2
        ).set_fill(opacity=0)

        self.play(Create(bio_frame_glow), Create(bio_frame), run_time=DEFAULT_RUN_TIME)
        self.play(FadeIn(VGroup(bio_title_glow, bio_title)), run_time=0.8)
        self.wait_audio()

        # Transition: hide fingerprint/face, keep only iris
        self.play(
            FadeOut(fp_group),
            FadeOut(face_group),
            FadeOut(bio_frame), FadeOut(bio_frame_glow),
            FadeOut(bio_title), FadeOut(bio_title_glow),
            run_time=DEFAULT_RUN_TIME,
        )

        # ==========================================
        # SHOT 3 — Focus on the Iris
        # ==========================================

        # ── Audio 3a: "The human iris is recognized..." ──
        self.play_audio("assets/audios/scene1_intro/3a.mp3")

        iris_graphic = self.create_iris_graphic(center=ORIGIN, base_radius=2.5)

        self.play(
            ReplacementTransform(iris_group, iris_graphic),
            self.camera.frame.animate.move_to(ORIGIN),
            run_time=SLOW_RUN_TIME,
        )

        for radius_start in [0.4, 0.7]:
            ring = Circle(
                radius=radius_start, color=PRIMARY_COLOR,
                stroke_width=2, stroke_opacity=0.7,
            ).move_to(ORIGIN)
            self.play(Create(ring), run_time=0.3)
            self.play(
                ring.animate.scale(5).set_stroke(opacity=0),
                run_time=1.2,
            )
            self.remove(ring)

        self.wait_audio()

        # ── Audio 3b: "Its intricate pattern..." ──
        self.play_audio("assets/audios/scene1_intro/3b.mp3")

        annotations = [
            ("Unique Pattern",  UP * 2.8 + LEFT * 3.2),
            ("Stable Structure", DOWN * 2.8 + RIGHT * 3.2),
            ("High Entropy",     RIGHT * 3.8 + UP * 0.5),
        ]
        annotation_groups = VGroup()
        for text, pos in annotations:
            lbl = Text(text, font=MAIN_FONT, font_size=SMALL_FONT_SIZE, color=TEXT_COLOR)
            lbl.move_to(pos)
            connector = DashedLine(
                start=pos, end=ORIGIN,
                stroke_color=MUTED_TEXT_COLOR, stroke_width=1,
                stroke_opacity=0.3, dash_length=0.1,
            )
            annotation_groups.add(VGroup(connector, lbl))

        self.play(
            LaggedStart(
                *[FadeIn(ag, shift=UP * 0.2) for ag in annotation_groups],
                lag_ratio=0.3,
            ),
            run_time=1.5,
        )
        self.wait_audio()
        self.play(FadeOut(annotation_groups), run_time=FAST_RUN_TIME)

        # Final fade to black
        self.play(
            FadeOut(iris_graphic),
            run_time=1.5,
        )


