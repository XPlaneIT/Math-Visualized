from manim import *
from manim_voiceover import VoiceoverScene
from _010voice_helper import EdgeTTSService
import numpy as np

# ============================================================
# PORTRAIT CONFIGURATION (9:16 Vertical Video — 1080x1920)
# ============================================================
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9.0
config.frame_height = 16.0


class InverseFunctionDemo(VoiceoverScene):
    """Show f(x)=x² on x≥0, mirror line y=x, a tracked point P
    and its reflection Q, then the full inverse curve f⁻¹(x)=√x."""

    def construct(self):
        self.set_speech_service(EdgeTTSService(voice="en-US-AndrewNeural"))

        # ---------- Title & Stacked Header Labels ----------
        title = Text(
            "Inverse Functions:\nReflection in y = x",
            font_size=38, weight=BOLD, color=WHITE, line_spacing=1.15
        ).to_edge(UP, buff=0.7)

        step_label = Text(
            "0. Start: f(x) = x², x ≥ 0",
            font_size=26, color=BLUE_B
        ).next_to(title, DOWN, buff=0.45)

        eq_label = MathTex(
            r"f(x) = x^2,\quad x \geq 0",
            font_size=36, color=BLUE_B
        ).next_to(step_label, DOWN, buff=0.35)

        # ---------- Axes (Equal scale so 45° reflection is faithful) ----------
        axes = Axes(
            x_range=[-0.5, 5, 1],
            y_range=[-0.5, 5, 1],
            x_length=7.4,
            y_length=7.4,
            axis_config={"include_tip": True, "stroke_width": 2.5},
        ).shift(DOWN * 1.1)

        def make_curve(func, x_min, x_max, color, width=4):
            return axes.plot(
                func, x_range=[x_min, x_max],
                color=color, stroke_width=width
            )

        # ==================================================
        # STEP 0 — Base curve f(x) = x² for x ≥ 0
        # ==================================================
        f = lambda x: x ** 2
        px, py = 1.4, f(1.4)           # P = (1.4, 1.96)
        curve_f = make_curve(f, 0, 2.2, BLUE_B)

        dot_P = Dot(color=RED_B, radius=0.12).move_to(axes.c2p(px, py))
        p_lbl = MathTex("P", font_size=32, color=RED_B).next_to(dot_P, UR, buff=0.06)

        with self.voiceover(
            text="To find the inverse of a function visually, we start with f of x equals x squared, restricted to x greater than or equal to zero. Let's track point P on this curve."
        ) as tracker:
            self.play(Write(title), Create(axes), run_time=min(1.6, tracker.duration * 0.35))
            self.add(step_label, eq_label)
            self.play(Create(curve_f), run_time=min(1.4, tracker.duration * 0.35))
            self.play(FadeIn(dot_P), Write(p_lbl), run_time=min(1.0, tracker.duration * 0.3))

        # ==================================================
        # STEP 1 — Add mirror line y = x
        # ==================================================
        mirror = make_curve(lambda x: x, 0, 4.7, GREY_B, width=2.5)
        mirror.set_stroke(opacity=0.6)
        mirror_lbl = MathTex("y = x", font_size=28, color=GREY_B)
        mirror_lbl.next_to(axes.c2p(4.4, 4.4), UL, buff=0.12)

        new_step = Text(
            "1. Mirror line: y = x",
            font_size=26, color=GREY_B
        ).next_to(title, DOWN, buff=0.45)

        with self.voiceover(text="Next, we draw the mirror line, y equals x.") as tracker:
            self.play(
                Create(mirror), Write(mirror_lbl),
                Transform(step_label, new_step),
                run_time=min(1.4, tracker.duration * 0.85)
            )

        # ==================================================
        # STEP 2 — Reflect P across y = x → Q
        # ==================================================
        new_step = Text(
            "2. Reflect P across y = x → Q",
            font_size=26, color=GREEN_B
        ).next_to(title, DOWN, buff=0.45)

        dot_Q = Dot(color=GREEN_B, radius=0.12).move_to(axes.c2p(py, px))
        dash_PQ = DashedLine(
            axes.c2p(px, py), axes.c2p(py, px),
            color=YELLOW, stroke_width=2.5,
        )
        q_lbl = MathTex("Q", font_size=32, color=GREEN_B).next_to(dot_Q, DR, buff=0.06)
        p_coord = MathTex(r"(1.4,\ 1.96)", font_size=24, color=RED_B).next_to(dot_P, UL, buff=0.08)
        q_coord = MathTex(r"(1.96,\ 1.4)", font_size=24, color=GREEN_B).next_to(q_lbl, DOWN, buff=0.08)

        with self.voiceover(
            text="Reflecting point P across this line swaps its coordinates, landing at point Q."
        ) as tracker:
            self.play(
                Transform(step_label, new_step),
                Create(dash_PQ),
                FadeIn(dot_Q),
                run_time=min(1.5, tracker.duration * 0.45)
            )
            self.play(
                Write(q_lbl), Write(p_coord), Write(q_coord),
                run_time=min(1.4, tracker.duration * 0.45)
            )

        self.play(FadeOut(dash_PQ), run_time=0.4)

        # ==================================================
        # STEP 3 — Full inverse curve f⁻¹(x) = √x
        # ==================================================
        new_step = Text(
            "3. Full inverse: f⁻¹(x) = √x",
            font_size=26, color=GREEN_B
        ).next_to(title, DOWN, buff=0.45)

        new_eq = MathTex(
            r"f^{-1}(x) = \sqrt{x}",
            font_size=36, color=GREEN_B
        ).next_to(new_step, DOWN, buff=0.35)

        inv_curve = make_curve(
            lambda x: np.sqrt(np.maximum(x, 0)),
            0, py * py, GREEN_B
        )

        with self.voiceover(
            text="Doing this for every point gives us the full inverse curve: f inverse of x equals the square root of x."
        ) as tracker:
            self.play(
                Transform(step_label, new_step),
                Transform(eq_label, new_eq),
                Create(inv_curve),
                run_time=min(2.0, tracker.duration * 0.8)
            )

        # ==================================================
        # STEP 4 — Domain ↔ Range swap & Final note
        # ==================================================
        new_step = Text(
            "4. Domain ↔ Range swap",
            font_size=26, color=YELLOW
        ).next_to(title, DOWN, buff=0.45)

        swap_text = MathTex(
            r"\text{Dom}(f) = \text{Range}(f^{-1}) = [0,\ \infty)",
            font_size=28, color=BLUE_B,
        ).to_edge(DOWN, buff=0.9)

        final_note = Text(
            "f⁻¹ is the reflection of f in the line y = x",
            font_size=26, color=GOLD_A
        ).to_edge(DOWN, buff=0.9)

        with self.voiceover(
            text="Notice how the domain and range swap places. Geometrically, f inverse is always the reflection of f across the line y equals x."
        ) as tracker:
            self.play(
                Transform(step_label, new_step),
                Write(swap_text),
                run_time=min(1.5, tracker.duration * 0.4)
            )
            self.wait(max(0.4, tracker.duration * 0.25))
            self.play(
                ReplacementTransform(swap_text, final_note),
                run_time=min(1.2, tracker.duration * 0.35)
            )

        self.wait(1.5)
        