import json
from manim import *

COLORS = json.load(open("parity_theme.json"))


class IntroAnimation(Scene):
    def construct(self):
        self.camera.background_color = COLORS["background"]

        primary = COLORS["accent"]["primary"]
        highlight = COLORS["accent"]["highlight"]
        text_color = COLORS["text"]["primary"]
        secondary = COLORS["text"]["secondary"]

        diamond_center = ORIGIN + UP * 0.4

        # --- STEM symbols ---
        symbols = VGroup(*[
            MathTex(sym, color=text_color).scale(1.15).set_opacity(1)
            for sym in [r"\int", r"\Sigma", r"f(x)", r"\Delta", r"\pi", r"\vec{v}"]
        ])

        positions = [
            UL * 2.2, UP * 2.4, UR * 2.2,
            LEFT * 3.2, RIGHT * 3.2, DOWN * 2.0
        ]
        for mob, pos in zip(symbols, positions):
            mob.move_to(pos)

        # --- Diamond ---
        diamond = Square(side_length=1.25)
        diamond.rotate(PI / 4)
        diamond.set_stroke(primary, width=3)
        diamond.set_fill(primary, opacity=0.12)
        diamond.move_to(diamond_center)
        diamond.scale(0.75)

        # --- Inner diamond ---
        inner_diamond = Square(side_length=1.25)
        inner_diamond.rotate(PI / 4)
        inner_diamond.set_stroke(highlight, width=1.2)
        inner_diamond.set_fill(opacity=0)
        inner_diamond.move_to(diamond_center)
        inner_diamond.scale(0.75 * 0.55)

        # --- Particle ring ---
        num_particles = 28
        ring_radius = 1.1
        particles = VGroup(*[
            Dot(radius=0.04, color=primary).move_to(
                diamond_center + ring_radius * np.array([
                    np.cos(2 * PI * i / num_particles),
                    np.sin(2 * PI * i / num_particles),
                    0
                ])
            ).set_opacity(0.6)
            for i in range(num_particles)
        ])

        # --- Text ---
        title = Text("Parity", font_size=52, color=text_color)
        title.move_to(ORIGIN + DOWN * 0.55)

        rule = Line(LEFT * 1.1, RIGHT * 1.1, stroke_width=0.8, color=primary)
        rule.move_to(ORIGIN + DOWN * 0.88)
        rule.set_opacity(0.5)

        subtitle = Text(
            '"STEM made clearer"',
            font_size=16,
            color=secondary,
            slant=ITALIC
        )
        subtitle.move_to(ORIGIN + DOWN * 1.12)

        # ── ANIMATION ──────────────────────────────────────────

        # 1. Symbols drift in with stagger
        self.play(
            LaggedStart(
                *[GrowFromCenter(s) for s in symbols],
                lag_ratio=0.2
            ),
            run_time=2.0
        )
        self.wait(0.3)
        # 2. Symbols charge up — ripple outward from center symbol
        self.play(
            LaggedStart(
                *[
                    s.animate.set_color(text_color).scale(1.3)
                    for s in symbols
                ],
                lag_ratio=0.1
            ),
            run_time=0.7
        )

        # 3. Hold the charge for a beat
        self.wait(0.2)

        # 4. All snap back simultaneously
        self.play(
            *[s.animate.set_color(text_color).scale(1 / 1.3) for s in symbols],
            run_time=0.25
        )

        # 5. Symbols spiral/collapse into diamond as stroke draws on
        self.play(
            LaggedStart(
                *[
                    FadeOut(s, target_position=diamond_center, run_time=0.4)
                    for s in symbols
                ],
                lag_ratio=0.07
            ),
            Create(diamond, rate_func=smooth),
            run_time=1.6
        )

        # 6. Inner diamond locks in
        self.play(
            GrowFromCenter(inner_diamond),
            run_time=0.45,
            rate_func=smooth
        )

        # 7. Particle ring materializes
        self.play(
            LaggedStart(
                *[GrowFromCenter(p) for p in particles],
                lag_ratio=0.03
            ),
            run_time=0.8
        )

        # 8. Ring rotates + pulse — sequential: rotation first
        self.play(
            Rotate(particles, angle=PI / num_particles, about_point=diamond_center),
            diamond.animate.scale(1.07),
            inner_diamond.animate.scale(1.07),
            run_time=0.35
        )

        # 9. Then flash lines shoot out AFTER the pulse peak
        self.play(
            Flash(
                diamond_center,
                color=highlight,
                flash_radius=0.95,
                line_length=0.18,
                num_lines=12
            ),
            diamond.animate.scale(1 / 1.07),
            inner_diamond.animate.scale(1 / 1.07),
            run_time=0.4
        )

        # 10. Particles fly outward first and fully vanish
        self.play(
            LaggedStart(
                *[
                    p.animate.move_to(
                        diamond_center + 2.8 * (p.get_center() - diamond_center)
                    ).set_opacity(0)
                    for p in particles
                ],
                lag_ratio=0.015
            ),
            run_time=0.7
        )
        self.remove(*particles)

        # 11. Title rises in once particles are gone
        self.play(
            FadeIn(title, shift=UP * 0.3),
            run_time=0.85,
            rate_func=smooth
        )

        # 12. Rule draws across
        self.play(
            Create(rule),
            run_time=0.45
        )

        # 13. Subtitle types in
        self.play(
            AddTextLetterByLetter(subtitle, time_per_char=0.048),
            run_time=1.0
        )

        # 14. Inner diamond breathes slowly
        self.play(
            Rotate(inner_diamond, angle=PI / 4, about_point=diamond_center),
            run_time=1.8,
            rate_func=smooth
        )

        self.wait(1.5)