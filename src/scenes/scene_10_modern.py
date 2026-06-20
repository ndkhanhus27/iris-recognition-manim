import os
import sys
from manim import *

sys.path.insert(0, os.getcwd())
from src.components.base_scene import BaseScene
from src.theme import *

AUDIO_DIR = "assets/audios/scene10_modern"

class Scene10Modern(BaseScene):
    """
    Scene 10 — Modern Iris Recognition and Deep Learning
    Duration: ~40-45 seconds
    """

    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # SHOT 1  [Audio 1]
        # Scene Introduction
        # ══════════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/1.mp3", fallback_duration=8.0)
        self.play_scene_title("10. Modern Iris Recognition")

        title = Tex(r"\textsf{\textbf{Modern Iris Recognition}}", font_size=42, color=TEXT_COLOR)
        subtitle = Tex(r"\textsf{From Daugman's Method to Deep Learning}", font_size=28, color=MUTED_TEXT_COLOR)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.2)
        title_group.move_to(UP * 3.2)
        
        self.play(FadeIn(title_group, shift=DOWN * 0.2), run_time=0.6)

        # ══════════════════════════════════════════════════════════════════════
        # SHOT 2
        # Classical Pipeline Review
        # ══════════════════════════════════════════════════════════════════════
        classic_label = Tex(r"\textsf{Classical Pipeline}", font_size=24, color=MUTED_TEXT_COLOR)
        classic_label.move_to(UP * 2.0 + LEFT * 4.5)
        
        # Build Classical Pipeline
        c_stages = ["Eye Image", "Localization", "Normalization", "Feature\nExtraction", "IrisCode", "Matching"]
        c_nodes, c_arrows = self._create_pipeline(c_stages, scale=1.0)
        c_pipeline = VGroup(c_nodes, c_arrows).move_to(UP * 1.0)
        
        self.play(FadeIn(classic_label, shift=RIGHT * 0.2), run_time=0.5)
        for i in range(len(c_nodes)):
            self.play(FadeIn(c_nodes[i], shift=RIGHT * 0.1), run_time=0.2)
            if i < len(c_arrows):
                self.play(Create(c_arrows[i]), run_time=0.1)
                
        # Highlight it all briefly
        self.play(
            *[n[0].animate.set_stroke(color=WARNING_COLOR).set_fill(color=WARNING_COLOR, opacity=0.2) for n in c_nodes],
            *[a.animate.set_color(WARNING_COLOR) for a in c_arrows],
            run_time=0.5
        )
        self.play(
            *[n[0].animate.set_stroke(color=TEXT_COLOR).set_fill(color=BG_COLOR, opacity=1) for n in c_nodes],
            *[a.animate.set_color(TEXT_COLOR) for a in c_arrows],
            run_time=0.5
        )
        self.wait_audio()

        # ══════════════════════════════════════════════════════════════════════
        # SHOT 3  [Audio 2]
        # Modern Deep Learning Pipeline
        # ══════════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/2.mp3", fallback_duration=8.0)

        dl_label = Tex(r"\textsf{Deep Learning Pipeline}", font_size=24, color=PRIMARY_COLOR)
        dl_label.move_to(DOWN * 0.5 + LEFT * 4.5)

        # Deep Learning Nodes
        dl_stages = ["Eye Image", "CNN", "Embedding", "Matching"]
        dl_nodes, dl_arrows = self._create_pipeline(dl_stages, scale=1.0, color=PRIMARY_COLOR)
        dl_pipeline = VGroup(dl_nodes, dl_arrows).move_to(DOWN * 1.5).align_to(c_pipeline, LEFT)

        # Replace standard CNN node with a procedural 3D-looking block
        cnn_procedural = self._create_cnn_block()
        cnn_procedural.move_to(dl_nodes[1].get_center())
        dl_nodes.submobjects[1] = cnn_procedural

        # Replace Embedding node with procedural vector
        emb_procedural = self._create_embedding_vector()
        emb_procedural.move_to(dl_nodes[2].get_center())
        dl_nodes.submobjects[2] = emb_procedural

        self.play(FadeIn(dl_label, shift=RIGHT * 0.2), run_time=0.5)
        for i in range(len(dl_nodes)):
            self.play(FadeIn(dl_nodes[i], shift=RIGHT * 0.1), run_time=0.3)
            if i < len(dl_arrows):
                self.play(Create(dl_arrows[i]), run_time=0.2)

        # Particle flow through CNN
        particles = VGroup(*[Dot(radius=0.05, color=SUCCESS_COLOR) for _ in range(5)])
        particles.arrange(RIGHT, buff=0.1).next_to(dl_arrows[0].get_start(), LEFT)
        
        self.play(particles.animate.next_to(dl_arrows[-1].get_end(), RIGHT), run_time=1.5, rate_func=linear)
        self.play(FadeOut(particles), run_time=0.3)

        self.wait_audio()

        # ══════════════════════════════════════════════════════════════════════
        # SHOT 4  [Audio 3]
        # Handcrafted Features vs Learned Features (Split-Screen transform)
        # ══════════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/3.mp3", fallback_duration=8.0)

        # Move pipelines up to make room
        self.play(
            title_group.animate.shift(UP * 5), # hide title
            c_pipeline.animate.shift(UP * 2.5),
            classic_label.animate.shift(UP * 2.5),
            dl_pipeline.animate.shift(UP * 2.5),
            dl_label.animate.shift(UP * 2.5),
            run_time=0.8
        )

        handcrafted_text = Tex(r"\textsf{Handcrafted Features}", font_size=28, color=WARNING_COLOR)
        handcrafted_text.move_to(DOWN * 1.0 + LEFT * 3.5)
        
        learned_text = Tex(r"\textsf{Learned Features}", font_size=28, color=PRIMARY_COLOR)
        learned_text.move_to(DOWN * 1.0 + RIGHT * 3.5)
        
        arrow_transform = Arrow(LEFT * 1.0, RIGHT * 1.0, color=TEXT_COLOR)
        arrow_transform.move_to(DOWN * 2.0)

        # Procedural Gabor
        gabor = self._create_gabor_icon().move_to(DOWN * 2.2 + LEFT * 3.5)
        # Procedural Feature Maps
        feature_maps = self._create_cnn_block().move_to(DOWN * 2.2 + RIGHT * 3.5)

        self.play(
            FadeIn(handcrafted_text), FadeIn(gabor),
            run_time=0.6
        )
        self.play(Create(arrow_transform))
        
        # Morph
        gabor_copy = gabor.copy()
        self.play(
            FadeIn(learned_text),
            Transform(gabor_copy, feature_maps),
            run_time=1.2
        )
        
        # Pulse feature maps
        self.play(
            gabor_copy.animate.set_color(SUCCESS_COLOR),
            run_time=0.5
        )
        self.play(
            gabor_copy.animate.set_color(PRIMARY_COLOR),
            run_time=0.5
        )

        self.wait(0.5)
        
        # Cleanup shot 4
        self.play(
            FadeOut(handcrafted_text, learned_text, arrow_transform, gabor, gabor_copy),
            run_time=0.5
        )
        self.wait_audio()

        # ══════════════════════════════════════════════════════════════════════
        # SHOT 5  [Audio 4]
        # Shared Foundation
        # ══════════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/4.mp3", fallback_duration=8.0)

        # Bring pipelines back down slightly
        self.play(
            c_pipeline.animate.shift(DOWN * 1.5),
            classic_label.animate.shift(DOWN * 1.5),
            dl_pipeline.animate.shift(DOWN * 1.5),
            dl_label.animate.shift(DOWN * 1.5),
            run_time=0.8
        )

        # Connect Normalization (c_nodes[2]) to CNN (dl_nodes[1])
        norm_node = c_nodes[2]
        cnn_node = dl_nodes[1]
        
        connection = DashedLine(
            start=norm_node.get_bottom(),
            end=cnn_node.get_top(),
            color=SUCCESS_COLOR,
            stroke_width=3
        )
        
        shared_text = Tex(r"\textsf{\textbf{Shared Foundation}}", font_size=24, color=SUCCESS_COLOR)
        shared_text.next_to(connection, RIGHT, buff=0.3)

        self.play(Create(connection), run_time=0.6)
        self.play(FadeIn(shared_text, shift=LEFT * 0.1))

        # Pulse energy
        energy = Dot(color=SUCCESS_COLOR, radius=0.06).move_to(connection.get_start())
        self.play(energy.animate.move_to(connection.get_end()), run_time=1.0)
        self.play(FadeOut(energy), run_time=0.2)

        self.wait_audio()

        # ══════════════════════════════════════════════════════════════════════
        # SHOT 6  [Audio 5 & 6]
        # Final Technology Statement & Outro
        # ══════════════════════════════════════════════════════════════════════
        self.play_audio(f"{AUDIO_DIR}/5.mp3", fallback_duration=6.0)

        self.play(
            FadeOut(classic_label, dl_label, shared_text, connection),
            run_time=0.5
        )

        # Merge into a single pipeline: Eye Image -> Normalization -> CNN -> Embedding -> Matching
        final_stages = ["Eye Image", "Normalization", "CNN", "Embedding", "Matching"]
        f_nodes, f_arrows = self._create_pipeline(final_stages, scale=1.0, color=SUCCESS_COLOR)
        f_pipeline = VGroup(f_nodes, f_arrows).move_to(ORIGIN)
        
        # Replace specific nodes to keep consistency
        f_nodes.submobjects[2] = self._create_cnn_block(color=SUCCESS_COLOR).move_to(f_nodes[2].get_center())
        f_nodes.submobjects[3] = self._create_embedding_vector(color=SUCCESS_COLOR).move_to(f_nodes[3].get_center())

        # Transform both old pipelines into the final unified pipeline
        self.play(
            Transform(c_pipeline, f_pipeline),
            Transform(dl_pipeline, f_pipeline),
            run_time=1.5
        )
        
        # Pipeline glows softly
        self.play(
            *[n[0].animate.set_stroke(color=SUCCESS_COLOR).set_fill(color=SUCCESS_COLOR, opacity=0.2) if isinstance(n, VGroup) and len(n)>0 and hasattr(n[0], 'set_fill') else n.animate for n in f_nodes],
            run_time=1.0
        )
        self.wait_audio()

        # Audio 6 starts
        self.play_audio(f"{AUDIO_DIR}/6.mp3", fallback_duration=8.0)

        self.play(FadeOut(c_pipeline, dl_pipeline, f_pipeline), run_time=1.0)

        final_math = Tex(r"\textsf{Classical Mathematics}", font_size=42, color=WARNING_COLOR)
        final_plus = Tex(r"\textsf{+}", font_size=36, color=TEXT_COLOR)
        final_dl = Tex(r"\textsf{Deep Learning}", font_size=42, color=PRIMARY_COLOR)
        
        final_eq = VGroup(final_math, final_plus, final_dl).arrange(DOWN, buff=0.3)
        final_eq.move_to(UP * 0.5)

        self.play(FadeIn(final_eq, shift=UP * 0.2), run_time=1.0)
        self.wait(1.0)

        final_outro = Tex(r"\textsf{\textbf{The Evolution of Iris Recognition}}", font_size=48, color=SUCCESS_COLOR)
        final_outro.next_to(final_eq, DOWN, buff=1.0)
        
        self.play(FadeIn(final_outro, shift=UP * 0.2), run_time=1.2)

        self.wait_audio()
        
        # Fade to black (End of Video)
        self.play(FadeOut(final_eq, final_outro), run_time=2.0)


    # ──────────────────────────────────────────────────────────────────────────
    # HELPER METHODS FOR PROCEDURAL ASSETS
    # ──────────────────────────────────────────────────────────────────────────

    def _create_pipeline(self, stages, scale=1.0, color=TEXT_COLOR):
        nodes = VGroup()
        arrows = VGroup()
        
        w = 1.6 * scale
        h = 0.9 * scale
        fs = int(24 * scale)

        for i, stage_name in enumerate(stages):
            box = RoundedRectangle(
                width=w, height=h, corner_radius=0.1, 
                color=color, stroke_width=2, 
                fill_color=BG_COLOR, fill_opacity=1
            )
            if "\n" in stage_name:
                lines = stage_name.split("\n")
                t1 = Tex(rf"\textsf{{{lines[0]}}}", font_size=fs, color=color)
                t2 = Tex(rf"\textsf{{{lines[1]}}}", font_size=fs, color=color)
                text = VGroup(t1, t2).arrange(DOWN, buff=0.05)
            else:
                text = Tex(rf"\textsf{{{stage_name}}}", font_size=fs, color=color)
                
            text.move_to(box.get_center())
            group = VGroup(box, text)
            if i > 0:
                group.next_to(nodes[-1], RIGHT, buff=0.4 * scale)
            nodes.add(group)
            
        for i in range(len(nodes) - 1):
            arrow = Arrow(
                start=nodes[i].get_right(),
                end=nodes[i+1].get_left(),
                buff=0.1,
                color=color,
                max_tip_length_to_length_ratio=0.15
            )
            arrows.add(arrow)
            
        return nodes, arrows

    def _create_cnn_block(self, color=PRIMARY_COLOR):
        """Creates a procedural stacked feature map icon."""
        layers = VGroup()
        num_layers = 3
        for i in range(num_layers):
            rect = RoundedRectangle(width=0.8, height=1.0, corner_radius=0.1, color=color, fill_color=BG_COLOR, fill_opacity=0.9)
            rect.shift(RIGHT * i * 0.15 + UP * i * 0.15)
            layers.add(rect)
        layers.move_to(ORIGIN)
        text = Tex(r"\textsf{CNN}", font_size=18, color=color).move_to(layers[-1].get_center())
        return VGroup(layers, text)

    def _create_embedding_vector(self, color=PRIMARY_COLOR):
        """Creates a procedural feature vector array icon."""
        cells = VGroup()
        for i in range(5):
            cell = Rectangle(width=0.25, height=0.25, color=color, stroke_width=1)
            # pseudo-random fill
            if i % 2 == 0:
                cell.set_fill(color, opacity=0.4)
            cells.add(cell)
        cells.arrange(DOWN, buff=0)
        
        box = RoundedRectangle(width=1.0, height=1.6, corner_radius=0.1, color=color, stroke_width=2, fill_opacity=0)
        text = Tex(r"\textsf{Embed}", font_size=14, color=color).next_to(cells, UP, buff=0.1)
        
        group = VGroup(box, cells, text).move_to(ORIGIN)
        cells.move_to(box.get_center() + DOWN * 0.1)
        text.next_to(cells, UP, buff=0.1)
        return group

    def _create_gabor_icon(self):
        """Creates a procedural Gabor wavelet icon."""
        group = VGroup()
        box = RoundedRectangle(width=1.2, height=1.2, corner_radius=0.1, color=WARNING_COLOR, stroke_width=2)
        
        # Create wavy lines
        for offset in [-0.3, 0, 0.3]:
            curve = FunctionGraph(
                lambda x: 0.2 * np.sin(5 * x) * np.exp(-2 * x**2),
                color=WARNING_COLOR,
                x_range=[-0.5, 0.5]
            ).shift(UP * offset)
            group.add(curve)
            
        group.add(box)
        return group
