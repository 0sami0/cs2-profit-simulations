# Save this code as case_opener_video.py
from manim import *
import random
import numpy as np

# --- DATA & CONFIGURATION (FEVER CASE) ---

# 1. Color Palette
class Colors:
    BACKGROUND = "#152B57"
    TEXT = "#FFFFFF"
    AXES = "#FFFFFF"
    LINE_BLUE = "#61AFEF"
    DOT_GOLD = "#61AFEF"
    BALANCE_GREEN = "#12DA2D"
    RED_LOSS = "#C82822"
    RARITY_COLORS = {'Blue': "#4269e2", 'Purple': "#85349b", 'Pink': "#D32CE6", 'Red': "#C82822", 'Gold': GOLD}

# 2. Case Specific Data
COST_PER_CASE = 3.48
STARTING_BALANCE = 200.00
NUM_CASES_TO_OPEN = 52

# 3. Item Pools with StatTrak™
SKINS = {
    'Blue': {'M4A4 | Choppa': 0.10, 'MP7 | Nexus': 0.12, 'MAC-10 | Resupply': 0.08, 'P2000 | Sure Grip': 0.09, 'SG 553 | Mockingbird': 0.11},
    'ST_Blue': {'ST M4A4 | Choppa': 0.30, 'ST MP7 | Nexus': 0.35, 'ST MAC-10 | Resupply': 0.25, 'ST P2000 | Sure Grip': 0.28, 'ST SG 553 | Mockingbird': 0.32},
    'Purple': {'Nova | Rising Sun': 0.50, 'P90 | Wave Breaker': 0.55, 'FAMAS | Bad Trip': 0.45, 'Galil AR | Control': 0.60, 'USP-S | PC-GRN': 0.40},
    'ST_Purple': {'ST Nova | Rising Sun': 1.50, 'ST P90 | Wave Breaker': 1.60, 'ST FAMAS | Bad Trip': 1.40, 'ST Galil AR | Control': 1.75, 'ST USP-S | PC-GRN': 1.20},
    'Pink': {'Desert Eagle | Serpent Strike': 3.00, 'UMP-45 | K.O. Factory': 2.20, 'Glock-18 | Shinobu': 2.50},
    'ST_Pink': {'ST Desert Eagle | Serpent Strike': 7.00, 'ST UMP-45 | K.O. Factory': 5.50, 'ST Glock-18 | Shinobu': 6.00},
    'Red': {'AK-47 | Searing Rage': 12.00, 'AWP | Printstream': 75.00},
    'ST_Red': {'ST AK-47 | Searing Rage': 30.00, 'ST AWP | Printstream': 200.00},
    'Gold': {'Navaja Knife | Slaughter': 280.00, 'Stiletto Knife | Case Hardened': 350.00, 'Ursus Knife | Doppler': 400.00, 'Talon Knife | Tiger Tooth': 500.00}
}
PROBABILITIES = {
    'Blue': 0.71928, 'ST_Blue': 0.07992,
    'Purple': 0.14382, 'ST_Purple': 0.01598,
    'Pink': 0.0288, 'ST_Pink': 0.0032,
    'Red': 0.00576, 'ST_Red': 0.00064,
    'Gold': 0.0026
}

# --- THE MANIM ANIMATION SCENE ---

class CaseOpeningAnimation(Scene):
    def construct(self):
        random.seed(42)
        np.random.seed(42) # Also seed numpy for consistency
        self.camera.background_color = Colors.BACKGROUND

        # --- 1. SETUP THE SCENE ---
        title = Text("The Fever Case Gamble", font_size=40, color=Colors.TEXT).to_edge(UP)
        axes = Axes(x_range=[0, NUM_CASES_TO_OPEN, 10], y_range=[0, 300, 50], x_length=7, y_length=5.5, axis_config={"color": Colors.AXES}, y_axis_config={"decimal_number_config": {"num_decimal_places": 0, "color": Colors.AXES}}).to_corner(DL, buff=0.75)
        graph_area = VGroup(axes, axes.get_x_axis_label(Text("Weeks", color=Colors.TEXT, font_size=32)), axes.get_y_axis_label(Text("Balance ($)", color=Colors.TEXT, font_size=32).rotate(90 * DEGREES)))

        week_counter = VGroup(Text("Week:", color=Colors.TEXT), Integer(0, color=Colors.TEXT)).arrange(RIGHT, buff=0.2)
        balance_tracker = VGroup(Text("Balance: $", color=Colors.TEXT), DecimalNumber(STARTING_BALANCE, color=Colors.BALANCE_GREEN, num_decimal_places=2)).arrange(RIGHT, buff=0.2)
        live_stats = VGroup(week_counter, balance_tracker).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_corner(UR, buff=1.2)
        
        # --- KEY CHANGE: The box is no longer created or displayed ---
        self.play(Write(title), Create(graph_area), Write(live_stats)); self.wait(1)

        # --- 2. RUN THE SIMULATION ---
        dot = Dot(point=axes.c2p(0, STARTING_BALANCE), color=Colors.DOT_GOLD)
        line_trace = TracedPath(dot.get_center, stroke_color=Colors.LINE_BLUE, stroke_width=4)
        self.add(line_trace, dot)

        current_balance = STARTING_BALANCE
        for i in range(1, NUM_CASES_TO_OPEN + 1):
            outcome_display = None # Reset display object
            if current_balance < COST_PER_CASE:
                new_point = axes.c2p(i, current_balance)
            else:
                current_balance -= COST_PER_CASE
                chosen_rarity = np.random.choice(list(PROBABILITIES.keys()), p=list(PROBABILITIES.values()))
                skin_pool = SKINS[chosen_rarity]
                skin_name = random.choice(list(skin_pool.keys()))
                skin_value = skin_pool[skin_name]
                current_balance += skin_value
                
                clean_rarity = chosen_rarity.replace('ST_', '')
                rarity_color = Colors.RARITY_COLORS[clean_rarity]
                
                rarity_text = Text(f"{chosen_rarity.replace('_', ' ')}", color=rarity_color, weight=BOLD)
                name_text = Text(f"{skin_name}", color=Colors.TEXT, font_size=24)
                value_text = Text(f"+${skin_value:.2f}", color=rarity_color, font_size=32)
                
                # --- KEY CHANGE: Position the text directly, without a box ---
                outcome_display = VGroup(rarity_text, name_text, value_text).arrange(DOWN, buff=0.2)
                outcome_display.next_to(live_stats, DOWN, buff=0.75)

                new_point = axes.c2p(i, current_balance)
                self.play(FadeIn(outcome_display, shift=UP), run_time=0.75)
            
            self.play(week_counter[1].animate.set_value(i), balance_tracker[1].animate.set_value(current_balance), dot.animate.move_to(new_point), run_time=0.75 if outcome_display else 0.2)
            if outcome_display:
                self.play(FadeOut(outcome_display, shift=DOWN), run_time=0.5)

        # --- 3. FINAL RESULTS ---
        self.wait(1)
        net_result = current_balance - STARTING_BALANCE
        result_color = Colors.RED_LOSS if net_result < 0 else Colors.BALANCE_GREEN

        final_balance_text = VGroup(Text("Final Balance: $", color=Colors.TEXT), DecimalNumber(current_balance, color=Colors.BALANCE_GREEN, num_decimal_places=2)).arrange(RIGHT)
        net_result_text = VGroup(Text("Net Result: $", color=Colors.TEXT), DecimalNumber(net_result, color=result_color, num_decimal_places=2, include_sign=True)).arrange(RIGHT)
        final_display = VGroup(final_balance_text, net_result_text).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        
        # --- KEY CHANGE: Final display replaces the live stats cleanly ---
        final_display.move_to(live_stats.get_center())
        
        self.play(FadeOut(live_stats), FadeIn(final_display, scale=1.2)); self.wait(5)
        