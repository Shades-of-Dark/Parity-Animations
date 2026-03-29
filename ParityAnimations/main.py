import json
from manim import *

COLORS = json.load(open("parity_theme.json"))


class IntroAnimation(Scene):
    def construct(self):
        self.camera.background_color = COLORS["background"]

        primary = COLORS["accent"]["primary"]
        highlight = COLORS["accent"]["highlight"]
        text_color = COLORS["text"]["primary"]
        text_secondary = COLORS["text"]["secondary"]
        accent_secondary = COLORS["accent"]["secondary"]
        accent_warm = COLORS["accent"]["warm"]
        accent_pop = COLORS["accent"]["pop"]
        math_constant = COLORS["math"]["constant"]
        diamond_center = ORIGIN + UP * 0.4
        semantic_correct = COLORS["semantic"]["correct"]
        symbol_colors = [primary, text_secondary, highlight,
                         accent_secondary, primary, text_secondary]

        symbols = VGroup(*[
            MathTex(sym, color=col).scale(1.15).set_opacity(1)
            for sym, col in zip(
                [r"2 + 2", r"x^2", r"\int", r"f(x)", r"\Sigma", r"\vec{v}"],
                symbol_colors
            )
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
        inner_diamond.set_stroke(accent_secondary, width=1.2)
        inner_diamond.set_fill(opacity=0)
        inner_diamond.move_to(diamond_center)
        inner_diamond.scale(0.75 * 0.55)

        # --- Particle ring ---
        num_particles = 28
        ring_radius = 1.1
        particles = VGroup(*[
            Dot(radius=0.04,
                color=accent_warm if i % 5 == 0 else (primary if i % 2 == 0 else accent_secondary)).move_to(
                diamond_center + ring_radius * np.array([
                    np.cos(2 * PI * i / num_particles),
                    np.sin(2 * PI * i / num_particles),
                    0
                ])
            ).set_opacity(0.6)
            for i in range(num_particles)
        ])

        # --- Text ---
        title = Text("Parity", font_size=48, color=text_color)
        title.move_to(ORIGIN + DOWN * 0.54)
        title.set_z_index(1)
        rule = Line(LEFT * 1.1, RIGHT * 1.1, stroke_width=0.8, color=highlight)
        rule.move_to(ORIGIN + DOWN * 0.77)
        rule.set_opacity(0.5)

        subtitle = Text(
            '"STEM made clearer"',
            font_size=16,
            color=text_secondary,
            slant=ITALIC
        )
        subtitle.move_to(ORIGIN + DOWN * 0.96)
        # --- Construction lines (compass arcs feel) ---
        # These are the "working lines" that appear before the diamond snaps clean
        construction_lines = VGroup(
            Line(diamond_center + LEFT * 1.2, diamond_center + RIGHT * 1.2,
                 stroke_width=0.6, color=accent_secondary).set_opacity(0.4),
            Line(diamond_center + UP * 1.2, diamond_center + DOWN * 1.2,
                 stroke_width=0.6, color=accent_secondary).set_opacity(0.4),
            DashedVMobject(
                Circle(radius=0.72, color=accent_secondary).move_to(diamond_center),
                num_dashes=30
            ).set_opacity(0.3),
        )
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

        # 2. Charge up to highlight color
        self.play(
            LaggedStart(
                *[s.animate.set_color(accent_warm).scale(1.3) for s in symbols],
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

        # 5a. Construction lines appear as symbols collapse
        self.play(
            LaggedStart(
                *[
                    FadeOut(s, target_position=diamond_center, run_time=0.4)
                    for s in symbols
                ],
                lag_ratio=0.07
            ),
            LaggedStart(
                *[Create(line) for line in construction_lines],
                lag_ratio=0.3
            ),
            run_time=1.6
        )

        # 5b. Brief pause — the construction lines "guide" the diamond
        self.wait(0.2)

        # 5c. Diamond snaps into place, construction lines vanish simultaneously
        self.play(
            Create(diamond, rate_func=smooth),
            FadeOut(construction_lines),
            run_time=0.7
        )

        logo_p = ImageMobject("parity_p.png")
        logo_p.rotate(-PI / 4)
        logo_p.scale(0.14)
        logo_p.set_color(math_constant)
        logo_p.move_to(diamond_center)
        logo_group = Group(inner_diamond, logo_p)
        # Then reveal it after inner diamond locks in
        self.play(
            GrowFromCenter(inner_diamond),
            FadeIn(logo_p),
            run_time=0.45
        )

        # 7. Particle ring materializes
        self.play(
            LaggedStart(
                *[GrowFromCenter(p) for p in particles],
                lag_ratio=0.03
            ),
            run_time=0.8
        )

        # 8.
        self.play(
            Rotate(particles, angle=PI / num_particles, about_point=diamond_center),
            diamond.animate.scale(1.07),
            logo_group.animate.scale(1.07),  # was inner_diamond
            run_time=0.35
        )

        # 9.
        self.play(
            Flash(diamond_center,
                  color=accent_pop,
                  flash_radius=0.95,
                  line_length=0.18,
                  num_lines=12),
            diamond.animate.scale(1 / 1.07),
            logo_group.animate.scale(1 / 1.07),  # was inner_diamond
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
            Rotate(logo_group, angle=PI / 4, about_point=diamond_center),
            run_time=1.8,
            rate_func=smooth
        )

        self.wait(1.5)
