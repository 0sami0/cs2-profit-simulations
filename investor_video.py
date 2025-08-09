# Save this code as investor_video.py
from manim import *
import random
import numpy as np

# --- DATA & CONFIGURATION ---

# 1. Color Palette
class Colors:
    BACKGROUND = "#152B57"
    TEXT = "#FFFFFF"
    AXES = "#FFFFFF"
    DEPOSITS_LINE = "#61AFEF"
    APY_LINE = "#12DA2D"
    ASSET_LINE = "#E5C07B"
    MARKER_RED = "#E06C75"

# 2. Smart Investor Specific Data
INITIAL_CAPITAL = 200.00
WEEKLY_DEPOSIT = 0.50
WEEKS_TO_SIMULATE = 156 
APY = 0.15
ASSET_APPRECIATION = 0.30

# --- THE MANIM ANIMATION SCENE ---

class SmartInvestorAnimation(Scene):
    def construct(self):
        self.camera.background_color = Colors.BACKGROUND

        # --- 1. DATA GATHERING FOR THE FULL 3-YEAR PERIOD ---
        principal_history, deposits_history, apy_gains_history, asset_gains_history = [], [], [], []
        current_principal, total_deposits, total_apy_gains = INITIAL_CAPITAL, 0, 0

        for week in range(WEEKS_TO_SIMULATE + 1):
            if week > 0:
                current_principal += WEEKLY_DEPOSIT
                total_deposits += WEEKLY_DEPOSIT
                weekly_apy_rate = (1 + APY)**(1/52) - 1
                apy_gain_this_week = current_principal * weekly_apy_rate
                total_apy_gains += apy_gain_this_week
                current_principal += apy_gain_this_week
            base_value_for_asset_gain = INITIAL_CAPITAL + total_deposits + total_apy_gains
            total_asset_gains = base_value_for_asset_gain * (ASSET_APPRECIATION * (week / WEEKS_TO_SIMULATE))
            principal_history.append(INITIAL_CAPITAL); deposits_history.append(total_deposits); apy_gains_history.append(total_apy_gains); asset_gains_history.append(total_asset_gains)

        x_values = list(range(WEEKS_TO_SIMULATE + 1))
        y_baseline = np.add(principal_history, deposits_history)
        y_with_apy = np.add(y_baseline, apy_gains_history)
        y_total = np.add(y_with_apy, asset_gains_history)
        
        # --- 2. SETUP FOR YEAR 1 ---
        title = Text("The Smart Investor's Strategy", font_size=48, color=Colors.TEXT).to_edge(UP)
        axes_y1 = Axes(x_range=[0, 52, 10], y_range=[0, 400, 100], x_length=8, y_length=5.0, axis_config={"color": Colors.AXES}, y_axis_config={"decimal_number_config": {"num_decimal_places": 0, "color": Colors.AXES}}).to_corner(DL, buff=0.75)
        
        info_panel = VGroup()
        week_counter = VGroup(Text("Week:", font_size=36, color=Colors.TEXT), Integer(0, font_size=36, color=Colors.TEXT)).arrange(RIGHT)
        total_value_text = VGroup(Text("Total Value: $", font_size=36, color=Colors.TEXT), DecimalNumber(INITIAL_CAPITAL, font_size=36, color=Colors.ASSET_LINE, num_decimal_places=2)).arrange(RIGHT)
        live_stats = VGroup(week_counter, total_value_text).arrange(DOWN, aligned_edge=LEFT)
        legend = VGroup(VGroup(Square(color=Colors.DEPOSITS_LINE, side_length=0.3), Text("Capital + Deposits", font_size=24, color=Colors.TEXT)).arrange(RIGHT), VGroup(Square(color=Colors.APY_LINE, side_length=0.3), Text("+ 15% APY from Fees", font_size=24, color=Colors.TEXT)).arrange(RIGHT), VGroup(Square(color=Colors.ASSET_LINE, side_length=0.3), Text("+ 30% Asset Growth", font_size=24, color=Colors.TEXT)).arrange(RIGHT)).arrange(DOWN, aligned_edge=LEFT)
        info_panel.add(live_stats, legend).arrange(DOWN, buff=0.75, aligned_edge=LEFT).to_edge(RIGHT, buff=0.75)
        self.play(Write(title), Create(axes_y1), FadeIn(info_panel))

        # --- 3. ANIMATE YEAR 1 & CREATE FIRST MARKER ---
        line_group_y1 = VGroup(*[axes_y1.plot_line_graph(x_values=x_values[:53], y_values=y_data[:53], add_vertex_dots=False, line_color=color, stroke_width=width)["line_graph"] for y_data, color, width in [(y_baseline, Colors.DEPOSITS_LINE, 4), (y_with_apy, Colors.APY_LINE, 4), (y_total, Colors.ASSET_LINE, 5)]])
        self.play(Create(line_group_y1), week_counter[1].animate.set_value(52), total_value_text[1].animate.set_value(y_total[52]), run_time=2.0)
        marker_y1 = VGroup(Dot(axes_y1.c2p(52, y_total[52]), color=Colors.MARKER_RED), DashedLine(axes_y1.c2p(0, y_total[52]), axes_y1.c2p(52, y_total[52]), color=Colors.MARKER_RED), DashedLine(axes_y1.c2p(52, 0), axes_y1.c2p(52, y_total[52]), color=Colors.MARKER_RED))
        self.play(Create(marker_y1)); self.wait(1.5)

        # --- 4. DYNAMIC TRANSFORMATION TO YEAR 2 ---
        look_ahead_text_y2 = Text("Simulating Year 2...", font_size=32, color=Colors.TEXT).next_to(info_panel, DOWN, buff=-5.5, aligned_edge=LEFT)
        self.play(Write(look_ahead_text_y2))
        axes_y2 = Axes(x_range=[0, 104, 10], y_range=[0, 700, 100], x_length=8, y_length=5.0, axis_config={"color": Colors.AXES}, y_axis_config={"decimal_number_config": {"num_decimal_places": 0, "color": Colors.AXES}}).to_corner(DL, buff=0.75)
        line_group_y2 = VGroup(*[axes_y2.plot_line_graph(x_values=x_values[:105], y_values=y_data[:105], add_vertex_dots=False, line_color=color, stroke_width=width)["line_graph"] for y_data, color, width in [(y_baseline, Colors.DEPOSITS_LINE, 4), (y_with_apy, Colors.APY_LINE, 4), (y_total, Colors.ASSET_LINE, 5)]])
        marker_y1_target_y2 = VGroup(Dot(axes_y2.c2p(52, y_total[52]), color=Colors.MARKER_RED), DashedLine(axes_y2.c2p(0, y_total[52]), axes_y2.c2p(52, y_total[52]), color=Colors.MARKER_RED), DashedLine(axes_y2.c2p(52, 0), axes_y2.c2p(52, y_total[52]), color=Colors.MARKER_RED))
        self.play(ReplacementTransform(axes_y1, axes_y2), ReplacementTransform(line_group_y1, line_group_y2), ReplacementTransform(marker_y1, marker_y1_target_y2), week_counter[1].animate.set_value(104), total_value_text[1].animate.set_value(y_total[104]), run_time=2.5)
        self.play(FadeOut(look_ahead_text_y2))
        marker_y2 = VGroup(Dot(axes_y2.c2p(104, y_total[104]), color=Colors.MARKER_RED), DashedLine(axes_y2.c2p(0, y_total[104]), axes_y2.c2p(104, y_total[104]), color=Colors.MARKER_RED), DashedLine(axes_y2.c2p(104, 0), axes_y2.c2p(104, y_total[104]), color=Colors.MARKER_RED))
        self.play(Create(marker_y2)); self.wait(1.5)

        # --- 5. DYNAMIC TRANSFORMATION TO YEAR 3 ---
        look_ahead_text_y3 = Text("Simulating Year 3...", font_size=32, color=Colors.TEXT).next_to(info_panel, DOWN, buff=-5.5, aligned_edge=LEFT)
        self.play(Write(look_ahead_text_y3))
        axes_y3 = Axes(x_range=[0, 156, 10], y_range=[0, 1000, 100], x_length=8, y_length=5.0, axis_config={"color": Colors.AXES}, y_axis_config={"decimal_number_config": {"num_decimal_places": 0, "color": Colors.AXES}}).to_corner(DL, buff=0.75)
        line_group_y3 = VGroup(*[axes_y3.plot_line_graph(x_values=x_values, y_values=y_data, add_vertex_dots=False, line_color=color, stroke_width=width)["line_graph"] for y_data, color, width in [(y_baseline, Colors.DEPOSITS_LINE, 4), (y_with_apy, Colors.APY_LINE, 4), (y_total, Colors.ASSET_LINE, 5)]])
        marker_y1_target_y3 = VGroup(Dot(axes_y3.c2p(52, y_total[52]), color=Colors.MARKER_RED), DashedLine(axes_y3.c2p(0, y_total[52]), axes_y3.c2p(52, y_total[52]), color=Colors.MARKER_RED), DashedLine(axes_y3.c2p(52, 0), axes_y3.c2p(52, y_total[52]), color=Colors.MARKER_RED))
        marker_y2_target_y3 = VGroup(Dot(axes_y3.c2p(104, y_total[104]), color=Colors.MARKER_RED), DashedLine(axes_y3.c2p(0, y_total[104]), axes_y3.c2p(104, y_total[104]), color=Colors.MARKER_RED), DashedLine(axes_y3.c2p(104, 0), axes_y3.c2p(104, y_total[104]), color=Colors.MARKER_RED))
        self.play(ReplacementTransform(axes_y2, axes_y3), ReplacementTransform(line_group_y2, line_group_y3), ReplacementTransform(marker_y1_target_y2, marker_y1_target_y3), ReplacementTransform(marker_y2, marker_y2_target_y3), week_counter[1].animate.set_value(156), total_value_text[1].animate.set_value(y_total[-1]), run_time=2.5)
        self.play(FadeOut(look_ahead_text_y3))
        marker_y3 = VGroup(Dot(axes_y3.c2p(156, y_total[-1]), color=Colors.MARKER_RED), DashedLine(axes_y3.c2p(0, y_total[-1]), axes_y3.c2p(156, y_total[-1]), color=Colors.MARKER_RED), DashedLine(axes_y3.c2p(156, 0), axes_y3.c2p(156, y_total[-1]), color=Colors.MARKER_RED))
        self.play(Create(marker_y3)); self.wait(2)
        
        # --- 6. THE FINAL "ANNUAL GROWTH" PAYOFF ---
        profit_y1 = y_total[52] - INITIAL_CAPITAL
        profit_y2 = y_total[104] - y_total[52]
        profit_y3 = y_total[-1] - y_total[104]
        
        analysis_title = Text("Annual Growth Breakdown", font_size=32, weight=BOLD)
        growth_y1 = VGroup(Text("Year 1:", font_size=28), Text(f"+${profit_y1:.2f}", font_size=32, color=Colors.APY_LINE, weight=BOLD)).arrange(RIGHT, buff=0.3)
        growth_y2 = VGroup(Text("Year 2:", font_size=28), Text(f"+${profit_y2:.2f}", font_size=32, color=Colors.APY_LINE, weight=BOLD)).arrange(RIGHT, buff=0.3)
        growth_y3 = VGroup(Text("Year 3:", font_size=28), Text(f"+${profit_y3:.2f}", font_size=32, color=Colors.APY_LINE, weight=BOLD)).arrange(RIGHT, buff=0.3)
        
        analysis_panel = VGroup(analysis_title, growth_y1, growth_y2, growth_y3).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        analysis_panel.move_to(info_panel.get_center())
        
        self.play(ReplacementTransform(info_panel, analysis_panel))
        self.wait(5)
        
        # --- 7. CREATE THE CLEAN PLATE FOR AFTER EFFECTS ---
        self.play(FadeOut(analysis_panel, title, marker_y1_target_y3, marker_y2_target_y3, marker_y3))
        self.wait(5)