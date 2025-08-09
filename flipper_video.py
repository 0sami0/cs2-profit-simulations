# Save this code as flipper_video.py
from manim import *
import random

# --- DATA & CONFIGURATION ---

# 1. Color Palette
class Colors:
    BACKGROUND = "#152B57"
    TEXT = "#FFFFFF"
    AXES = "#FFFFFF"
    LINE_BLUE = "#61AFEF"
    DOT_GOLD = "#61AFEF"
    BALANCE_GREEN = "#12DA2D"
    RED_LOSS = "#C82822"

# 2. Skin Flipper Specific Data
INITIAL_CAPITAL = 200.00
BUY_PRICE_PER_UNIT = 2.70
NUM_UNITS = 74
INITIAL_COST = BUY_PRICE_PER_UNIT * NUM_UNITS

STEAM_FEE_MULTIPLIER = 0.85
DAYS_TO_SIMULATE = 90

BREAK_EVEN_PRICE = BUY_PRICE_PER_UNIT / STEAM_FEE_MULTIPLIER
BREAK_EVEN_PORTFOLIO_VALUE = BREAK_EVEN_PRICE * NUM_UNITS

# --- THE MANIM ANIMATION SCENE ---

class FlipperAnimation(Scene):
    def construct(self):
        random.seed(5) 
        self.camera.background_color = Colors.BACKGROUND

        # --- 1. SETUP & "BUY" EVENT ---
        title = Text("The Skin Flipper's Ordeal", font_size=48, color=Colors.TEXT).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        buy_box_text = VGroup(
            Text("BUY", color=Colors.TEXT, weight=BOLD),
            Text(f"{NUM_UNITS} x AK-47 | Slate", color=Colors.LINE_BLUE),
            Text(f"@ ${BUY_PRICE_PER_UNIT:.2f} / unit", color=Colors.TEXT)
        ).arrange(DOWN, buff=0.3)
        buy_box = VGroup(SurroundingRectangle(buy_box_text, buff=0.4, color=Colors.AXES), buy_box_text)
        
        self.play(FadeIn(buy_box, scale=0.8))
        self.wait(2)
        self.play(FadeOut(buy_box))

        # --- 2. THE SIMULATION (FINAL REFINED LAYOUT) ---
        axes = Axes(
            x_range=[0, DAYS_TO_SIMULATE, 15],
            y_range=[150, 300, 25],
            x_length=8,
            y_length=4.5,
            axis_config={"color": Colors.AXES},
            y_axis_config={"decimal_number_config": {"num_decimal_places": 0, "color": Colors.AXES}}
        ).to_corner(DL, buff=1.0)
        
        x_label = axes.get_x_axis_label(Text("Days", color=Colors.TEXT, font_size=32))
        y_label = Text("Portfolio Value ($)", color=Colors.TEXT, font_size=32).rotate(90 * DEGREES).next_to(axes.get_y_axis(), LEFT, buff=0.2)
        graph_area = VGroup(axes, x_label)
        self.play(Create(graph_area), Write(y_label))

        # --- KEY CHANGE: Live stats are now anchored to the middle-right of the screen ---
        day_counter = VGroup(Text("Day:", color=Colors.TEXT), Integer(0, color=Colors.TEXT)).arrange(RIGHT)
        portfolio_value_text = VGroup(Text("Value: $", color=Colors.TEXT), DecimalNumber(INITIAL_COST, color=Colors.BALANCE_GREEN, num_decimal_places=2)).arrange(RIGHT)
        live_stats = VGroup(day_counter, portfolio_value_text).arrange(DOWN, aligned_edge=LEFT)
        live_stats.to_edge(RIGHT, buff=0.75) # Position on right edge, vertically centered.
        
        self.play(FadeIn(live_stats))

        # Break-even line and its safe label position
        break_even_line = DashedLine(
            start=axes.c2p(0, BREAK_EVEN_PORTFOLIO_VALUE),
            end=axes.c2p(DAYS_TO_SIMULATE, BREAK_EVEN_PORTFOLIO_VALUE),
            color=Colors.RED_LOSS,
            stroke_width=3
        )
        break_even_label = Text("Break-Even Point", color=Colors.RED_LOSS, font_size=24).next_to(break_even_line, UP, buff=0.1).align_to(break_even_line, LEFT)
        self.play(Create(break_even_line), Write(break_even_label))
        
        # Run the realistic random walk
        dot = Dot(point=axes.c2p(0, INITIAL_COST), color=Colors.DOT_GOLD)
        line_trace = TracedPath(dot.get_center, stroke_color=Colors.LINE_BLUE, stroke_width=4)
        self.add(line_trace, dot)

        current_price_per_unit = BUY_PRICE_PER_UNIT
        final_price = 0
        final_portfolio_value = 0
        for day in range(1, DAYS_TO_SIMULATE + 1):
            total_daily_change = random.uniform(-0.05, 0.065)
            current_price_per_unit += total_daily_change
            current_portfolio_value = current_price_per_unit * NUM_UNITS
            new_point = axes.c2p(day, current_portfolio_value)
            
            self.play(
                day_counter[1].animate.set_value(day),
                portfolio_value_text[1].animate.set_value(current_portfolio_value),
                dot.animate.move_to(new_point),
                run_time=0.05
            )
            if day == DAYS_TO_SIMULATE:
                final_price = current_price_per_unit
                final_portfolio_value = current_portfolio_value
        
        self.wait(1)
        
        # --- 3. THE "SELL" EVENT (UPGRADED AND REPOSITIONED) ---
        sell_box_text = VGroup(
            Text("SELL", color=Colors.BALANCE_GREEN, weight=BOLD, font_size=28),
            Text(f"{NUM_UNITS}x AK-47 | Slate", color=Colors.LINE_BLUE, font_size=24),
            Text(f"@ ${final_price:.2f} / unit", color=Colors.TEXT, font_size=24),
            Text(f"Final Value: ${final_portfolio_value:.2f}", color=Colors.BALANCE_GREEN, font_size=24)
        ).arrange(DOWN, buff=0.25)
        
        sell_box = VGroup(SurroundingRectangle(sell_box_text, buff=0.5, color=Colors.AXES), sell_box_text)
        
        # Position the sell box exactly where the live stats were for a seamless transition.
        sell_box.move_to(live_stats.get_center())
        
        self.play(ReplacementTransform(live_stats, sell_box))
        self.wait(2)
        
        # --- 4. CREATE THE CLEAN PLATE FOR AFTER EFFECTS ---
        self.play(FadeOut(sell_box, title, break_even_label, y_label))
        self.wait(5)