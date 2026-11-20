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


class QuadraticTransformations(VoiceoverScene):
    def construct(self):
        self.set_speech_service(EdgeTTSService(voice="en-US-AndrewNeural"))

        # ============================================================
        # TITLE & TOP STACKED LABELS
        # ============================================================
        title = Text("Transformations of y = x²", font_size=40, weight=BOLD, color=WHITE).to_edge(UP, buff=0.7)
        step_label = Text("0. Start: y = x²", font_size=26, color=YELLOW).next_to(title, DOWN, buff=0.45)
        eq_label   = MathTex(r"y = x^2", font_size=38, color=BLUE_B).next_to(step_label, DOWN, buff=0.35)

        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-4, 10, 1],
            x_length=7.8,
            y_length=9.2,
            axis_config={"include_tip": True, "stroke_width": 2.5},
        ).shift(DOWN * 1.4)

        def make_curve(func, x_min, x_max, color):
            return axes.plot(func, x_range=[x_min, x_max], color=color, stroke_width=4)

        dot_left   = Dot(color=WHITE,  radius=0.11)
        dot_right  = Dot(color=WHITE,  radius=0.11)
        dot_vertex = Dot(color=YELLOW, radius=0.14)

        f0 = lambda x: x ** 2
        curve = make_curve(f0, -2.5, 2.5, BLUE_B)

        dot_left.move_to(axes.c2p(-2.5, f0(-2.5)))
        dot_right.move_to(axes.c2p(2.5, f0(2.5)))
        dot_vertex.move_to(axes.c2p(0, f0(0)))

        # Intro + Step 0 synced to narration
        with self.voiceover(text="Let's walk through the transformations of the basic parabola, y equals x squared.") as tracker:
            self.play(Write(title), Create(axes), run_time=min(1.5, tracker.duration * 0.45))
            self.add(step_label)
            self.play(
                Create(curve),
                Write(eq_label),
                FadeIn(dot_left, dot_right, dot_vertex),
                run_time=max(0.8, tracker.duration * 0.55)
            )

        # ============================================================
        # ALL STEPS WITH VOICEOVER SCRIPTS
        # ============================================================
        steps = [
            (lambda x: (x-2)**2, -0.5, 4.5, 2, GREEN_B,
             "1. Horizontal shift: +2", r"y = (x-2)^2", 38, False,
             "First, subtracting two inside the parentheses shifts the graph two units to the right."),

            (lambda x: (x-2)**2 + 3, -0.5, 4.5, 2, YELLOW,
             "2. Vertical shift: +3", r"y = (x-2)^2 + 3", 38, False,
             "Adding three outside lifts the entire parabola up by three units."),

            (lambda x: x**2, -2.5, 2.5, 0, BLUE_B,
             "3. Reset to y = x²", r"y = x^2", 38, False,
             "Resetting back to y equals x squared."),

            (lambda x: (1.3*x)**2, -1.8, 1.8, 0, ORANGE,
             "4. Horizontal compress: (1.3x)²", r"y = (1.3x)^2", 38, False,
             "Multiplying x by one point three compresses the parabola horizontally, making it narrower."),

            (lambda x: 1.5*(1.3*x)**2, -1.8, 1.8, 0, PINK,
             "5. Vertical stretch: 1.5(1.3x)²", r"y = 1.5(1.3x)^2", 36, False,
             "Multiplying the whole function by one point five stretches it vertically."),

            (lambda x: x**2, -2.5, 2.5, 0, BLUE_B,
             "6. Reset to y = x²", r"y = x^2", 38, False,
             "Resetting once more to our base curve."),

            (lambda x: x**2, 0, 2.5, 0, TEAL_B,
             "7. Restrict to x ≥ 0", r"y = x^2,\ x \geq 0", 38, True,
             "Now, we restrict the domain to x greater than or equal to zero, fading out the left branch."),

            (lambda x: 1.5*(0.5*(x-2))**2 + 1, 0, 4, 2, PURPLE_A,
             "8. Combine: 1.5(0.5(x-2))² + 1", r"y = 1.5(0.5(x-2))^2 + 1", 32, False,
             "Next, we combine a horizontal stretch, a right shift of two, a vertical stretch, and an upward shift of one."),

            (lambda x: -(1.5*(0.5*(x-2))**2 + 1), 0, 4, 2, RED_B,
             "9. Reflect in x-axis", r"y = -[1.5(0.5(x-2))^2 + 1]", 30, False,
             "Putting a negative sign in front reflects the curve upside down across the x axis."),

            (lambda x: -(1.5*(0.5*(-x-2))**2 + 1), -4, 0, -2, GOLD_A,
             "10. Reflect in y-axis", r"y = -[1.5(0.5(-x-2))^2 + 1]", 28, False,
             "Finally, replacing x with negative x mirrors the curve across the y axis."),
        ]

        for (func, xmin, xmax, vx, color, step_text, eq_latex, eq_font, fade_left, narration) in steps:
            new_curve = make_curve(func, xmin, xmax, color)

            new_step_label = Text(step_text, font_size=26, color=color)
            if new_step_label.width > 7.8:
                new_step_label.set_width(7.8)
            new_step_label.next_to(title, DOWN, buff=0.45)

            new_eq_label = MathTex(eq_latex, font_size=eq_font, color=color)
            if new_eq_label.width > 7.8:
                new_eq_label.set_width(7.8)
            new_eq_label.next_to(new_step_label, DOWN, buff=0.35)

            p_left   = axes.c2p(xmin, func(xmin))
            p_right  = axes.c2p(xmax, func(xmax))
            p_vertex = axes.c2p(vx,   func(vx))

            with self.voiceover(text=narration) as tracker:
                anim_time = min(1.8, tracker.duration * 0.75)

                if fade_left:
                    left_branch  = make_curve(func, -2.5, 0, curve.get_color())
                    right_branch = make_curve(func, 0, 2.5, curve.get_color())
                    self.remove(curve)
                    self.add(left_branch, right_branch)
                    curve = right_branch

                    self.play(
                        FadeOut(left_branch),
                        Transform(curve, new_curve),
                        Transform(step_label, new_step_label),
                        Transform(eq_label, new_eq_label),
                        dot_left.animate.move_to(p_left),
                        dot_right.animate.move_to(p_right),
                        dot_vertex.animate.move_to(p_vertex),
                        run_time=anim_time,
                    )
                else:
                    self.play(
                        Transform(curve, new_curve),
                        Transform(step_label, new_step_label),
                        Transform(eq_label, new_eq_label),
                        dot_left.animate.move_to(p_left),
                        dot_right.animate.move_to(p_right),
                        dot_vertex.animate.move_to(p_vertex),
                        run_time=anim_time,
                    )

        self.wait(1.5)