import os
import sys
from manim import *

sys.path.insert(0, os.getcwd())
from src.components.base_scene import BaseScene
from src.components.formulas import *
from src.theme import *

class Scene3Overview(BaseScene):
    """
    Scene 3 — Pipeline Overview
    
    This scene introduces the Daugman Iris Recognition Pipeline.
    It flows through each stage: Eye Image -> Localization -> Normalization -> Feature Extraction -> IrisCode -> Matching.
    Then it transitions to Scene 4: Iris Localization.
    """
    def construct(self):
        # ----------------------------------------------------
        # ----------------------------------------------------
        # SHOT 1 — Pipeline Construction & Scene Title
        # ----------------------------------------------------
        self.play_audio("assets/audios/scene3_overview/0.mp3", fallback_duration=3.5)
        self.play_scene_title("3. Pipeline Overview")
        self.wait_audio()
        self.wait(0.5)
        
        # Pipeline Data
        stages = [
            {"label": "Eye Image", "title": None, "formula": None, "audio": "1.mp3", "fallback": 5.0},
            {"label": "Localization", "title": "Detect Iris Boundaries", "formula": FORMULA_LOCALIZATION, "audio": "3.mp3", "fallback": 3.3},
            {"label": "Normalization", "title": "Rubber Sheet Model", "formula": FORMULA_NORMALIZATION, "audio": "4.mp3", "fallback": 3.3},
            {"label": "Feature\nExtraction", "title": "2D Gabor Wavelets", "formula": FORMULA_FEATURE_EXTRACTION, "audio": "5.mp3", "fallback": 3.3},
            {"label": "IrisCode", "title": "Binary Encoding", "formula": FORMULA_IRIS_CODE, "audio": "6.mp3", "fallback": 3.3},
            {"label": "Matching", "title": "Hamming Distance", "formula": FORMULA_MATCHING, "audio": "7.mp3", "fallback": 3.5}
        ]
        
        # Build Pipeline Nodes
        self.nodes = VGroup()
        for stage in stages:
            node = self.create_node(stage["label"])
            self.nodes.add(node)
        
        self.nodes.arrange(RIGHT, buff=0.4)
        self.nodes.move_to(ORIGIN)
        
        # Build Connecting Arrows
        self.arrows = VGroup()
        for i in range(len(self.nodes) - 1):
            arrow = Arrow(
                start=self.nodes[i].get_right(),
                end=self.nodes[i+1].get_left(),
                buff=0.1,
                color=TEXT_COLOR,
                stroke_width=DEFAULT_STROKE_WIDTH,
                max_tip_length_to_length_ratio=0.15
            )
            self.arrows.add(arrow)

        # Title
        title_text = "Daugman's Iris Recognition Pipeline"
        title = self.create_title(title_text)
        # Căn giữa tiêu đề lên trên cùng (phải center() trước vì to_edge(UP) giữ nguyên toạ độ X)
        title.center().to_edge(UP, buff=0.5)

        # Animation: Build Pipeline
        self.play_audio(f"assets/audios/scene3_overview/{stages[0]['audio']}", fallback_duration=stages[0]['fallback'])
        
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=DEFAULT_RUN_TIME)
        
        for i in range(len(self.nodes)):
            self.play(FadeIn(self.nodes[i]), run_time=0.5)
            if i < len(self.arrows):
                self.play(Create(self.arrows[i]), run_time=0.4)
                
        self.wait_audio()
        self.wait(0.5)

        # ----------------------------------------------------
        # SHOT 2 — Data Flow Through Pipeline
        # ----------------------------------------------------
        pulse = Dot(color=PRIMARY_COLOR, radius=0.08)

        # 1. Eye Image
        self.play_audio("assets/audios/scene3_overview/2.mp3", fallback_duration=3.3)
        self.highlight_node(self.nodes[0], color=WARNING_COLOR)
        self.wait_audio()
        self.wait(0.3)

        # Iterate over remaining stages
        for i in range(1, len(stages)):
            stage = stages[i]
            prev_node = self.nodes[i-1]
            curr_node = self.nodes[i]
            arrow = self.arrows[i-1]
            
            self.animate_pipeline_step(
                prev_node=prev_node,
                curr_node=curr_node,
                arrow=arrow,
                pulse=pulse,
                audio_file=f"assets/audios/scene3_overview/{stage['audio']}",
                fallback_dur=stage['fallback'],
                title_text=stage['title'],
                formula_tex=stage['formula']
            )

        # ----------------------------------------------------
        # SHOT 3 — Pipeline Summary & Transition to Scene 4
        # ----------------------------------------------------
        self.play_audio("assets/audios/scene3_overview/8.mp3", fallback_duration=4.5)
        
        # All blocks glow simultaneously
        self.play(
            *[n[0].animate.set_color(WARNING_COLOR).set_fill(WARNING_COLOR, opacity=0.2) for n in self.nodes],
            *[n[1].animate.set_color(WARNING_COLOR) for n in self.nodes],
            *[a.animate.set_color(WARNING_COLOR) for a in self.arrows],
            run_time=DEFAULT_RUN_TIME
        )
        self.wait_audio()
        self.wait(0.5)

        # Transition to Scene 4: Zoom to Localization node (Stage 2)
        self.play_audio("assets/audios/scene3_overview/9.mp3", fallback_duration=4.0)
        
        localization_node = self.nodes[1]
        
        self.play(
            *[FadeOut(m) for m in self.mobjects if m not in [localization_node]],
            run_time=DEFAULT_RUN_TIME
        )
        self.play(
            localization_node.animate.scale(3.0).move_to(ORIGIN).set_opacity(0),
            run_time=1.5
        )
        self.wait_audio()

        # Display New Title for Scene 4
        self.play_scene_title("4. Iris Localization")

    # ----------------------------------------------------
    # REUSABLE HELPER METHODS
    # ----------------------------------------------------
    def create_node(self, label_text):
        """Creates a pipeline node."""
        box = RoundedRectangle(
            width=1.8, height=1.0, corner_radius=0.2, 
            color=TEXT_COLOR, stroke_width=2, 
            fill_color=BG_COLOR, fill_opacity=1
        )
        if "\n" in label_text:
            lines = label_text.split("\n")
            t1 = Text(lines[0], font=MAIN_FONT, font_size=14, color=TEXT_COLOR)
            t2 = Text(lines[1], font=MAIN_FONT, font_size=14, color=TEXT_COLOR)
            text = VGroup(t1, t2).arrange(DOWN, buff=0.1)
        else:
            text = Text(label_text, font=MAIN_FONT, font_size=14, color=TEXT_COLOR)
            
        text.move_to(box.get_center())
        return VGroup(box, text)
    
    def highlight_node(self, node, color=PRIMARY_COLOR):
        """Highlights a specific node."""
        self.play(
            node[0].animate.set_color(color).set_fill(color, opacity=0.2),
            node[1].animate.set_color(color),
            run_time=0.5
        )
        
    def unhighlight_node(self, node):
        """Removes highlight from a node."""
        self.play(
            node[0].animate.set_color(TEXT_COLOR).set_fill(BG_COLOR, opacity=1),
            node[1].animate.set_color(TEXT_COLOR),
            run_time=0.5
        )
        
    def play_data_pulse(self, pulse, arrow):
        """Animates a data pulse traveling along an arrow."""
        if pulse not in self.mobjects:
            self.add(pulse)
        pulse.move_to(arrow.get_start())
        self.play(
            pulse.animate.move_to(arrow.get_end()),
            run_time=1.0,
            rate_func=linear
        )

    def animate_pipeline_step(self, prev_node, curr_node, arrow, pulse, audio_file, fallback_dur, title_text, formula_tex):
        """Animates a single stage transition in the pipeline with modular and reusable components."""
        self.play_audio(audio_file, fallback_duration=fallback_dur)
        
        self.unhighlight_node(prev_node)
        self.play_data_pulse(pulse, arrow)
        self.highlight_node(curr_node, color=WARNING_COLOR)
        
        if title_text and formula_tex:
            preview_label = Text(title_text, font=MAIN_FONT, font_size=SMALL_FONT_SIZE, color=PRIMARY_COLOR)
            
            # Format IrisCode binary correctly if using MathTex
            preview_formula = MathTex(formula_tex, font_size=36, color=TEXT_COLOR)
            
            teaser_group = VGroup(preview_label, preview_formula).arrange(DOWN, buff=0.3)
            teaser_group.next_to(self.nodes, DOWN, buff=1.0)
            
            self.play(FadeIn(teaser_group, shift=UP*0.2), run_time=1.0)
            # Chờ audio kết thúc hoàn toàn để tránh cắt âm
            self.wait_audio()
            self.play(FadeOut(teaser_group), run_time=0.5)
            self.wait(0.2)
        else:
            self.wait_audio()
            self.wait(0.2)

