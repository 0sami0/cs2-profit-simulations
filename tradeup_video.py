# Save this code as tradeup_video.py
from manim import *
import random
import numpy as np

# --- DATA & CONFIGURATION ---

# 1. Color Palette
class Colors:
    BACKGROUND = "#152B57"
    TEXT = "#FFFFFF"
    AXES = "#FFFFFF"
    LINE_BLUE = "#61AFEF"
    DOT_GOLD = "#61AFEF"
    BALANCE_GREEN = "#98C379"
    RED_LOSS = "#C82822"
    GOLD_RARITY = GOLD

# 2. Trade-Up Specific Data
# --- NEW: Added the Steam Fee Multiplier ---
STEAM_FEE_MULTIPLIER = 0.85 # Represents the 85% you keep after the 15% fee

COST_PER_ATTEMPT = 4.33
STARTING_BALANCE = 200.00
NUM_ATTEMPTS = 52

TRADE_UP_OUTCOMES = {
    'Galil AR | Stone Cold': 15.11,
    'M249 | Nebula Crusader': 9.05,
    'P250 | Wingshot': 7.40,
    'MP7 | Special Delivery': 7.40,
    'USP-S | Ticket to Hell': 1.89,
    'M4A1-S | Night Terror': 1.99,
    'G3SG1 | Dream Glade': 2.11,
    'PP-Bizon | Space Cat': 1.61,
    'XM1014 | Zombie Offensive': 1.58,
}
raw_probs = [13.64, 13.64, 13.64, 9.09, 9.09, 9.09, 9.09, 9.09, 9.09]
PROBABILITIES = np.array(raw_probs) / sum(raw_probs)

# --- THE MANIM ANIMATION SCENE ---

class TradeUpAnimation(Scene):
    def construct(self):
        random.seed(42) # This seed still produces a profit, which is a great story!
        self.camera.background_color = Colors.BACKGROUND

        # --- 1. SETUP THE SCENE ---
        axes = Axes(
            x_range=[0, NUM_ATTEMPTS, 10],
            y_range=[0, 500, 100],
            x_length=7,
            y_length=5.5,
            axis_config={"color": Colors.AXES},
            y_axis_config={"decimal_number_config": {"num_decimal_places": 0, "color": Colors.AXES}}
        ).to_corner(DL, buff=0.75)
        x_label = axes.get_x_axis_label(Text("Attempts", color=Colors.TEXT, font_size=32))
        y_label = axes.get_y_axis_label(Text("Balance ($)", color=Colors.TEXT, font_size=32).rotate(90 * DEGREES))
        graph_area = VGroup(axes, x_label, y_label)

        title = Text("The High-Stakes Trade-Up (with Fees)", font_size=40, color=Colors.TEXT).to_edge(UP)
        attempt_counter = VGroup(Text("Attempt:", color=Colors.TEXT), Integer(0, color=Colors.TEXT)).arrange(RIGHT, buff=0.2)
        balance_tracker = VGroup(Text("Balance: $", color=Colors.TEXT), DecimalNumber(STARTING_BALANCE, color=Colors.BALANCE_GREEN, num_decimal_places=2)).arrange(RIGHT, buff=0.2)
        trade_cost_text = Text(f"Cost per Attempt: ${COST_PER_ATTEMPT:.2f}", color=Colors.TEXT, font_size=28)
        info_panel = VGroup(attempt_counter, balance_tracker, trade_cost_text).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_corner(UR, buff=1.2)
        outcome_box = RoundedRectangle(width=4.5, height=2.5, corner_radius=0.2, color=Colors.AXES, stroke_width=2).next_to(info_panel, DOWN, buff=0.5) # Made box slightly taller

        self.play(Write(title), Create(graph_area), Write(info_panel), Create(outcome_box))
        self.wait(1)

        # --- 2. RUN THE SIMULATION WITH FEE CALCULATION ---
        dot = Dot(point=axes.c2p(0, STARTING_BALANCE), color=Colors.DOT_GOLD)
        line_trace = TracedPath(dot.get_center, stroke_color=Colors.LINE_BLUE, stroke_width=4)
        self.add(line_trace, dot)

        current_balance = STARTING_BALANCE
        outcome_names = list(TRADE_UP_OUTCOMES.keys())

        for i in range(1, NUM_ATTEMPTS + 1):
            current_balance -= COST_PER_ATTEMPT
            chosen_outcome_name = np.random.choice(outcome_names, p=PROBABILITIES)
            outcome_value = TRADE_UP_OUTCOMES[chosen_outcome_name]
            
            # --- CORE LOGIC CHANGE: CALCULATE AND APPLY THE FEE ---
            value_after_fees = outcome_value * STEAM_FEE_MULTIPLIER
            fee_amount = outcome_value - value_after_fees
            current_balance += value_after_fees # Add the post-fee value to the balance
            
            # Profit is now calculated based on the post-fee value
            profit_or_loss = value_after_fees - COST_PER_ATTEMPT
            result_color = Colors.BALANCE_GREEN if profit_or_loss >= 0 else Colors.RED_LOSS

            # --- VISUAL CHANGE: DISPLAY THE FEE IN THE OUTCOME BOX ---
            name_text = Text(str(chosen_outcome_name), color=Colors.TEXT, font_size=24)
            value_text = Text(f"Market Value: ${outcome_value:.2f}", color=Colors.TEXT, font_size=20)
            fee_text = Text(f"- ${fee_amount:.2f} (15% Fee)", color=Colors.RED_LOSS, font_size=20)
            profit_text = Text(f"Net Profit: {profit_or_loss:+.2f}", color=result_color, font_size=24)
            outcome_display = VGroup(name_text, value_text, fee_text, profit_text).arrange(DOWN).move_to(outcome_box.get_center())

            new_point = axes.c2p(i, current_balance)

            self.play(
                attempt_counter[1].animate.set_value(i),
                balance_tracker[1].animate.set_value(current_balance),
                FadeIn(outcome_display),
                dot.animate.move_to(new_point),
                run_time=0.75
            )
            self.wait(0.5)
            self.play(FadeOut(outcome_display), run_time=0.5)
        
        self.wait(1)
        
        # --- 3. DYNAMIC TRANSITION FOR YOUR AFTER EFFECTS WORK ---
        full_graph_group = VGroup(graph_area, line_trace, dot)
        shrunken_graph_target = full_graph_group.copy().scale(0.65).to_corner(UL)

        self.play(
            FadeOut(info_panel, outcome_box, title),
            Transform(full_graph_group, shrunken_graph_target),
            run_time=1.5
        )
        
        self.wait(5)