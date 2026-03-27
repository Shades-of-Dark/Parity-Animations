from manim import *
# Notes:
# Username is parity from here on out
# 3/26/26
# First video


class CreateCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)
        self.play(Create(circle))


