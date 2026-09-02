"""
FM Scout AI (FC Finder) - Database Builder & Feature Normalization Pipeline
Generates seed data for 150+ European top 5 league stars, Korean/Asian international stars,
second-tier prospects, and hidden gems.
Calculates per-90 metrics, min-max normalized features, and custom F~SSS tier ratings.
"""
import os
import sys
import json
import sqlite3
import numpy as np

# Ensure backend path is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database import get_db_connection, init_db
from pipeline.generate_expanded_data import get_mega_player_dataset
from pipeline.expand_roster_generator import generate_additional_world_players
from pipeline.mega_roster_generator import generate_mega_dataset

def score_to_grade(score: float) -> str:
    """
    Score mapping rule:
    Score >= 95: SSS (👑 World Class)
    90 <= Score < 95: SS (🔥 Elite Big League)
    85 <= Score < 90: S (✨ League Best XI)
    80 <= Score < 85: A (📈 Big League Starter)
    70 <= Score < 80: B (Solid Rotation)
    60 <= Score < 70: C (Squad Backup)
    50 <= Score < 60: D (Development Prospect)
    Score < 50: F (Excluded / Low Sample)
    """
    if score >= 95.0:
        return "SSS"
    elif score >= 90.0:
        return "SS"
    elif score >= 85.0:
        return "S"
    elif score >= 80.0:
        return "A"
    elif score >= 70.0:
        return "B"
    elif score >= 60.0:
        return "C"
    elif score >= 50.0:
        return "D"
    else:
        return "F"

def generate_all_players():
    base_players = get_mega_player_dataset()

    additional_stars = [
        # --- KOREAN & ASIAN STARS ---
        ("p_lee_jaesung", "J. S. Lee", "Lee Jae-sung", "이재성", 32, "South Korea", "KR", "Mainz Red", "Bundesliga", 1, "AM", "CM", "MF", "Left", 180, 4.0, 30.0, 2026,
         "Intelligent High-Pressing 10",
         {"kp": 1.9, "prog_p": 4.8, "pass_acc": 82.0, "passes_att": 44.0, "through_balls": 0.42, "crosses_box": 0.6, "shots": 1.4, "box_shots": 1.0, "sot_pct": 36.0, "xg": 0.22, "npxg": 0.22, "goals": 0.18, "dribbles": 1.4, "dribble_pct": 58.0, "carry_dist": 180.0, "fouls_drawn": 1.7, "prog_carries": 3.1, "interceptions": 1.2, "tackles_won": 2.2, "clearances": 0.8, "blocks": 0.8, "recoveries": 6.8, "aerial_pct": 52.0, "ground_duels": 6.1, "aerial_duels": 1.8, "pressures": 23.0}),

        ("p_hwang_inbeom", "I. B. Hwang", "Hwang In-beom", "황인범", 28, "South Korea", "KR", "Rotterdam White", "Eredivisie", 2, "CM", "DM", "MF", "Both", 177, 10.0, 35.0, 2028,
         "Relentless Metronome & Box-to-Box Passer",
         {"kp": 2.3, "prog_p": 7.2, "pass_acc": 88.5, "passes_att": 72.0, "through_balls": 0.52, "crosses_box": 0.8, "shots": 1.4, "box_shots": 0.5, "sot_pct": 33.0, "xg": 0.14, "npxg": 0.14, "goals": 0.11, "dribbles": 1.6, "dribble_pct": 65.0, "carry_dist": 220.0, "fouls_drawn": 1.8, "prog_carries": 3.6, "interceptions": 1.4, "tackles_won": 2.5, "clearances": 1.1, "blocks": 1.0, "recoveries": 7.6, "aerial_pct": 48.0, "ground_duels": 6.5, "aerial_duels": 0.9, "pressures": 22.8}),

        ("p_oh_hyeongyu", "H. G. Oh", "Oh Hyeon-gyu", "오현규", 23, "South Korea", "KR", "Genk Blue", "Belgian Pro League", 3, "ST", "CF", "FW", "Right", 185, 4.5, 15.0, 2028,
         "Physical Bull-Dozer Target Striker",
         {"kp": 0.9, "prog_p": 1.5, "pass_acc": 73.0, "passes_att": 18.0, "through_balls": 0.15, "crosses_box": 0.2, "shots": 3.4, "box_shots": 3.0, "sot_pct": 47.0, "xg": 0.62, "npxg": 0.55, "goals": 0.65, "dribbles": 1.4, "dribble_pct": 52.0, "carry_dist": 140.0, "fouls_drawn": 2.4, "prog_carries": 2.5, "interceptions": 0.3, "tackles_won": 0.8, "clearances": 0.9, "blocks": 0.4, "recoveries": 2.8, "aerial_pct": 56.0, "ground_duels": 6.2, "aerial_duels": 2.6, "pressures": 16.5}),

        ("p_eom_jisung", "J. S. Eom", "Eom Ji-sung", "엄지성", 22, "South Korea", "KR", "Swansea White", "Championship", 2, "W", "LW", "FW", "Right", 178, 3.5, 12.0, 2028,
         "Agile Cutting Inverted Winger",
         {"kp": 1.8, "prog_p": 3.4, "pass_acc": 80.0, "passes_att": 30.0, "through_balls": 0.35, "crosses_box": 1.1, "shots": 2.5, "box_shots": 1.6, "sot_pct": 40.0, "xg": 0.32, "npxg": 0.32, "goals": 0.28, "dribbles": 3.2, "dribble_pct": 59.0, "carry_dist": 250.0, "fouls_drawn": 2.2, "prog_carries": 5.4, "interceptions": 0.6, "tackles_won": 1.5, "clearances": 0.4, "blocks": 0.5, "recoveries": 4.6, "aerial_pct": 34.0, "ground_duels": 5.6, "aerial_duels": 0.5, "pressures": 18.0}),

        ("p_paik_seungho", "S. H. Paik", "Paik Seung-ho", "백승호", 27, "South Korea", "KR", "Birmingham Blue", "League One", 3, "CM", "DM", "MF", "Right", 182, 3.0, 15.0, 2026,
         "La Masia Educated Press-Resistant 8",
         {"kp": 1.6, "prog_p": 5.8, "pass_acc": 89.0, "passes_att": 62.0, "through_balls": 0.38, "crosses_box": 0.6, "shots": 1.2, "box_shots": 0.4, "sot_pct": 31.0, "xg": 0.10, "npxg": 0.10, "goals": 0.08, "dribbles": 1.4, "dribble_pct": 68.0, "carry_dist": 200.0, "fouls_drawn": 1.8, "prog_carries": 2.8, "interceptions": 1.3, "tackles_won": 2.3, "clearances": 1.2, "blocks": 0.9, "recoveries": 7.0, "aerial_pct": 50.0, "ground_duels": 6.1, "aerial_duels": 1.1, "pressures": 20.5}),

        ("p_doan_ritsu", "R. Doan", "Ritsu Doan", "도안 리츠", 26, "Japan", "JP", "Freiburg Red", "Bundesliga", 1, "W", "RW", "FW", "Left", 172, 18.0, 40.0, 2027,
         "Hard-Working Inverted Slasher",
         {"kp": 2.1, "prog_p": 4.2, "pass_acc": 80.0, "passes_att": 36.0, "through_balls": 0.45, "crosses_box": 1.3, "shots": 2.4, "box_shots": 1.6, "sot_pct": 38.0, "xg": 0.32, "npxg": 0.32, "goals": 0.28, "dribbles": 2.4, "dribble_pct": 57.0, "carry_dist": 220.0, "fouls_drawn": 2.0, "prog_carries": 4.5, "interceptions": 0.8, "tackles_won": 1.9, "clearances": 0.6, "blocks": 0.7, "recoveries": 5.4, "aerial_pct": 38.0, "ground_duels": 6.1, "aerial_duels": 0.6, "pressures": 21.0}),

        ("p_minamino", "T. Minamino", "Takumi Minamino", "미나미노 타쿠미", 29, "Japan", "JP", "Monaco Red-White", "Ligue 1", 1, "AM", "SS", "FW", "Right", 174, 15.0, 60.0, 2026,
         "Shadow Striker & Space Exploiter",
         {"kp": 2.0, "prog_p": 3.9, "pass_acc": 79.0, "passes_att": 34.0, "through_balls": 0.40, "crosses_box": 0.7, "shots": 2.6, "box_shots": 2.0, "sot_pct": 42.0, "xg": 0.42, "npxg": 0.42, "goals": 0.38, "dribbles": 1.8, "dribble_pct": 56.0, "carry_dist": 190.0, "fouls_drawn": 1.7, "prog_carries": 3.6, "interceptions": 0.7, "tackles_won": 1.6, "clearances": 0.4, "blocks": 0.6, "recoveries": 4.9, "aerial_pct": 36.0, "ground_duels": 5.4, "aerial_duels": 0.5, "pressures": 22.0}),

        ("p_tomiyasu", "T. Tomiyasu", "Takehiro Tomiyasu", "토미야스 타케히로", 25, "Japan", "JP", "London Red", "Premier League", 1, "FB", "CB", "DF", "Both", 188, 35.0, 100.0, 2026,
         "Two-Footed Lockdown Defensive Fullback",
         {"kp": 0.8, "prog_p": 4.6, "pass_acc": 87.5, "passes_att": 56.0, "through_balls": 0.18, "crosses_box": 0.5, "shots": 0.5, "box_shots": 0.4, "sot_pct": 30.0, "xg": 0.05, "npxg": 0.05, "goals": 0.04, "dribbles": 0.8, "dribble_pct": 65.0, "carry_dist": 170.0, "fouls_drawn": 1.1, "prog_carries": 2.2, "interceptions": 1.6, "tackles_won": 2.7, "clearances": 2.8, "blocks": 1.2, "recoveries": 6.5, "aerial_pct": 65.0, "ground_duels": 6.4, "aerial_duels": 2.8, "pressures": 16.0}),

        ("p_ito_hiroki", "H. Ito", "Hiroki Ito", "이토 히로키", 25, "Japan", "JP", "München Rot", "Bundesliga", 1, "CB", "LB", "DF", "Left", 188, 30.0, 80.0, 2028,
         "Left-Footed Progressive Diagonal Passer",
         {"kp": 0.6, "prog_p": 5.8, "pass_acc": 89.0, "passes_att": 74.0, "through_balls": 0.32, "crosses_box": 0.4, "shots": 0.4, "box_shots": 0.2, "sot_pct": 28.0, "xg": 0.04, "npxg": 0.04, "goals": 0.03, "dribbles": 0.5, "dribble_pct": 70.0, "carry_dist": 180.0, "fouls_drawn": 0.8, "prog_carries": 1.6, "interceptions": 1.5, "tackles_won": 2.2, "clearances": 3.4, "blocks": 1.1, "recoveries": 6.8, "aerial_pct": 62.0, "ground_duels": 5.6, "aerial_duels": 2.2, "pressures": 12.0}),

        # --- PREMIER LEAGUE STARS ---
        ("p_bruno_g", "B. Guimarães", "Bruno Guimarães", "브루노 기마랑이스", 26, "Brazil", "BR", "Newcastle Black-White", "Premier League", 1, "CM", "DM", "MF", "Right", 182, 85.0, 180.0, 2028,
          "Complete Dynamic Deep Playmaker",
          {"kp": 2.1, "prog_p": 6.9, "pass_acc": 88.0, "passes_att": 68.0, "through_balls": 0.65, "crosses_box": 0.6, "shots": 1.5, "box_shots": 0.6, "sot_pct": 34.0, "xg": 0.18, "npxg": 0.18, "goals": 0.16, "dribbles": 2.3, "dribble_pct": 66.0, "carry_dist": 230.0, "fouls_drawn": 3.2, "prog_carries": 3.8, "interceptions": 1.3, "tackles_won": 2.6, "clearances": 1.2, "blocks": 1.1, "recoveries": 7.4, "aerial_pct": 52.0, "ground_duels": 7.6, "aerial_duels": 1.2, "pressures": 23.0}),

        ("p_gordon", "A. Gordon", "Anthony Gordon", "앤서니 고든", 23, "England", "GB-ENG", "Newcastle Black-White", "Premier League", 1, "W", "LW", "FW", "Right", 183, 60.0, 120.0, 2028,
          "High-Speed Direct Runner & Presser",
          {"kp": 2.1, "prog_p": 3.8, "pass_acc": 79.5, "passes_att": 31.0, "through_balls": 0.42, "crosses_box": 1.4, "shots": 2.7, "box_shots": 2.0, "sot_pct": 42.0, "xg": 0.42, "npxg": 0.36, "goals": 0.38, "dribbles": 2.8, "dribble_pct": 55.0, "carry_dist": 270.0, "fouls_drawn": 2.6, "prog_carries": 5.8, "interceptions": 0.6, "tackles_won": 1.8, "clearances": 0.4, "blocks": 0.6, "recoveries": 5.1, "aerial_pct": 38.0, "ground_duels": 5.9, "aerial_duels": 0.6, "pressures": 21.5}),

        ("p_macallister", "A. Mac Allister", "Alexis Mac Allister", "알렉시스 맥 알리스터", 25, "Argentina", "AR", "Liverpool Red", "Premier League", 1, "CM", "DM", "MF", "Right", 176, 75.0, 160.0, 2028,
          "Press-Resistant Midfield Maestro",
          {"kp": 1.9, "prog_p": 6.8, "pass_acc": 89.2, "passes_att": 66.0, "through_balls": 0.55, "crosses_box": 0.6, "shots": 1.6, "box_shots": 0.6, "sot_pct": 33.0, "xg": 0.16, "npxg": 0.16, "goals": 0.15, "dribbles": 1.6, "dribble_pct": 65.0, "carry_dist": 210.0, "fouls_drawn": 2.0, "prog_carries": 3.2, "interceptions": 1.4, "tackles_won": 2.8, "clearances": 1.1, "blocks": 1.0, "recoveries": 7.5, "aerial_pct": 52.0, "ground_duels": 6.8, "aerial_duels": 1.1, "pressures": 23.5}),

        ("p_szoboszlai", "D. Szoboszlai", "Dominik Szoboszlai", "도미니크 소보슬라이", 23, "Hungary", "HU", "Liverpool Red", "Premier League", 1, "CM", "AM", "MF", "Right", 186, 75.0, 150.0, 2028,
          "Long-Range Cannon & Physical Engine",
          {"kp": 2.4, "prog_p": 6.1, "pass_acc": 86.0, "passes_att": 58.0, "through_balls": 0.60, "crosses_box": 1.4, "shots": 2.4, "box_shots": 0.9, "sot_pct": 36.0, "xg": 0.22, "npxg": 0.22, "goals": 0.20, "dribbles": 2.1, "dribble_pct": 62.0, "carry_dist": 250.0, "fouls_drawn": 1.8, "prog_carries": 4.5, "interceptions": 1.0, "tackles_won": 1.9, "clearances": 0.8, "blocks": 0.8, "recoveries": 6.6, "aerial_pct": 56.0, "ground_duels": 5.9, "aerial_duels": 1.4, "pressures": 22.0}),

        ("p_diaz", "L. Díaz", "Luis Díaz", "루이스 디아스", 27, "Colombia", "CO", "Liverpool Red", "Premier League", 1, "W", "LW", "FW", "Right", 178, 65.0, 140.0, 2027,
          "Relentless Chaos Carrier & Dribbler",
          {"kp": 2.0, "prog_p": 3.6, "pass_acc": 82.0, "passes_att": 34.0, "through_balls": 0.38, "crosses_box": 1.2, "shots": 3.1, "box_shots": 2.4, "sot_pct": 40.0, "xg": 0.46, "npxg": 0.46, "goals": 0.42, "dribbles": 3.6, "dribble_pct": 58.0, "carry_dist": 280.0, "fouls_drawn": 2.5, "prog_carries": 6.4, "interceptions": 0.6, "tackles_won": 1.4, "clearances": 0.3, "blocks": 0.5, "recoveries": 4.8, "aerial_pct": 44.0, "ground_duels": 6.2, "aerial_duels": 0.8, "pressures": 18.5}),

        ("p_eze", "E. Eze", "Eberechi Eze", "에베레치 에제", 26, "England", "GB-ENG", "South London Eagles", "Premier League", 1, "AM", "LW", "MF", "Right", 178, 60.0, 100.0, 2027,
          "Silky High-Skill Creative Dribbler",
          {"kp": 2.7, "prog_p": 5.4, "pass_acc": 83.5, "passes_att": 46.0, "through_balls": 0.72, "crosses_box": 1.3, "shots": 3.2, "box_shots": 1.8, "sot_pct": 39.0, "xg": 0.42, "npxg": 0.36, "goals": 0.38, "dribbles": 3.5, "dribble_pct": 64.0, "carry_dist": 270.0, "fouls_drawn": 2.7, "prog_carries": 5.5, "interceptions": 0.6, "tackles_won": 1.3, "clearances": 0.3, "blocks": 0.5, "recoveries": 4.9, "aerial_pct": 32.0, "ground_duels": 6.0, "aerial_duels": 0.4, "pressures": 16.0}),

        ("p_kudus", "M. Kudus", "Mohammed Kudus", "모하메드 쿠두스", 24, "Ghana", "GH", "East London Claret", "Premier League", 1, "W", "AM", "FW", "Left", 177, 50.0, 90.0, 2028,
          "Unstoppable Physical Duel Dribbler",
          {"kp": 1.9, "prog_p": 3.6, "pass_acc": 79.0, "passes_att": 30.0, "through_balls": 0.35, "crosses_box": 1.0, "shots": 2.8, "box_shots": 2.1, "sot_pct": 42.0, "xg": 0.40, "npxg": 0.40, "goals": 0.36, "dribbles": 4.4, "dribble_pct": 68.0, "carry_dist": 290.0, "fouls_drawn": 3.0, "prog_carries": 6.2, "interceptions": 0.8, "tackles_won": 2.2, "clearances": 0.6, "blocks": 0.7, "recoveries": 5.6, "aerial_pct": 52.0, "ground_duels": 8.4, "aerial_duels": 1.2, "pressures": 20.0}),

        ("p_caicedo", "M. Caicedo", "Moisés Caicedo", "모이세스 카이세도", 22, "Ecuador", "EC", "West London Blue", "Premier League", 1, "DM", "CM", "MF", "Right", 178, 75.0, 150.0, 2031,
          "Dynamic Midfield Vacuum & Ball Winner",
          {"kp": 1.2, "prog_p": 5.8, "pass_acc": 91.0, "passes_att": 64.0, "through_balls": 0.28, "crosses_box": 0.3, "shots": 0.9, "box_shots": 0.3, "sot_pct": 28.0, "xg": 0.08, "npxg": 0.08, "goals": 0.05, "dribbles": 1.4, "dribble_pct": 68.0, "carry_dist": 190.0, "fouls_drawn": 2.1, "prog_carries": 2.4, "interceptions": 1.7, "tackles_won": 3.5, "clearances": 1.6, "blocks": 1.4, "recoveries": 8.2, "aerial_pct": 58.0, "ground_duels": 7.6, "aerial_duels": 1.6, "pressures": 25.5}),

        ("p_enzo", "E. Fernández", "Enzo Fernández", "엔소 페르난데스", 23, "Argentina", "AR", "West London Blue", "Premier League", 1, "CM", "DM", "MF", "Right", 178, 75.0, 180.0, 2031,
          "Deep Diagonal Distributor",
          {"kp": 2.0, "prog_p": 7.4, "pass_acc": 87.5, "passes_att": 76.0, "through_balls": 0.68, "crosses_box": 0.8, "shots": 1.8, "box_shots": 0.7, "sot_pct": 32.0, "xg": 0.18, "npxg": 0.14, "goals": 0.15, "dribbles": 1.4, "dribble_pct": 62.0, "carry_dist": 210.0, "fouls_drawn": 1.6, "prog_carries": 3.1, "interceptions": 1.2, "tackles_won": 2.4, "clearances": 1.2, "blocks": 0.9, "recoveries": 7.2, "aerial_pct": 54.0, "ground_duels": 6.2, "aerial_duels": 1.2, "pressures": 20.0}),

        ("p_mainoo", "K. Mainoo", "Kobbie Mainoo", "코비 메이누", 19, "England", "GB-ENG", "Manchester Red", "Premier League", 1, "CM", "DM", "MF", "Right", 175, 55.0, 60.0, 2027,
          "Silky Press-Evader & Wonderkid Controller",
          {"kp": 1.4, "prog_p": 5.2, "pass_acc": 88.5, "passes_att": 48.0, "through_balls": 0.32, "crosses_box": 0.4, "shots": 1.2, "box_shots": 0.6, "sot_pct": 35.0, "xg": 0.14, "npxg": 0.14, "goals": 0.15, "dribbles": 2.4, "dribble_pct": 72.0, "carry_dist": 230.0, "fouls_drawn": 2.2, "prog_carries": 3.8, "interceptions": 1.3, "tackles_won": 2.5, "clearances": 1.4, "blocks": 1.2, "recoveries": 6.8, "aerial_pct": 46.0, "ground_duels": 6.9, "aerial_duels": 0.8, "pressures": 22.0}),

        # --- LA LIGA STARS ---
        ("p_raphinha", "Raphinha", "Raphael Dias Belloli", "하피냐", 27, "Brazil", "BR", "Catalan Blue", "La Liga", 1, "W", "LW", "FW", "Left", 176, 60.0, 200.0, 2027,
          "High-Workrate Direct Creative Winger",
          {"kp": 3.2, "prog_p": 5.1, "pass_acc": 80.5, "passes_att": 42.0, "through_balls": 0.78, "crosses_box": 2.1, "shots": 3.4, "box_shots": 2.4, "sot_pct": 43.0, "xg": 0.52, "npxg": 0.48, "goals": 0.52, "dribbles": 2.6, "dribble_pct": 56.0, "carry_dist": 260.0, "fouls_drawn": 2.2, "prog_carries": 5.6, "interceptions": 0.9, "tackles_won": 1.8, "clearances": 0.5, "blocks": 0.7, "recoveries": 5.8, "aerial_pct": 42.0, "ground_duels": 6.2, "aerial_duels": 0.8, "pressures": 22.0}),

        ("p_pedri2", "Pedri", "Pedro González", "페드리", 21, "Spain", "ES", "Catalan Blue", "La Liga", 1, "CM", "AM", "MF", "Right", 174, 80.0, 180.0, 2026,
          "Silky Pocket Controller & Space Manipulator",
          {"kp": 2.6, "prog_p": 7.8, "pass_acc": 89.8, "passes_att": 66.0, "through_balls": 0.78, "crosses_box": 0.6, "shots": 1.2, "box_shots": 0.7, "sot_pct": 36.0, "xg": 0.16, "npxg": 0.16, "goals": 0.14, "dribbles": 2.2, "dribble_pct": 69.0, "carry_dist": 240.0, "fouls_drawn": 1.9, "prog_carries": 3.8, "interceptions": 1.1, "tackles_won": 1.8, "clearances": 0.5, "blocks": 0.8, "recoveries": 7.1, "aerial_pct": 38.0, "ground_duels": 5.9, "aerial_duels": 0.4, "pressures": 20.0}),

        ("p_zubimendi", "M. Zubimendi", "Martín Zubimendi", "마르틴 수비멘디", 25, "Spain", "ES", "San Sebastián Blue", "La Liga", 1, "DM", "CM", "MF", "Right", 181, 60.0, 75.0, 2027,
          "Press-Resistant Pivot Controller",
          {"kp": 1.2, "prog_p": 6.4, "pass_acc": 89.5, "passes_att": 62.0, "through_balls": 0.35, "crosses_box": 0.3, "shots": 0.9, "box_shots": 0.5, "sot_pct": 30.0, "xg": 0.09, "npxg": 0.09, "goals": 0.08, "dribbles": 1.1, "dribble_pct": 72.0, "carry_dist": 180.0, "fouls_drawn": 1.8, "prog_carries": 2.2, "interceptions": 1.6, "tackles_won": 2.6, "clearances": 1.9, "blocks": 1.2, "recoveries": 7.4, "aerial_pct": 63.0, "ground_duels": 6.5, "aerial_duels": 2.3, "pressures": 19.0}),

        ("p_alvarez", "J. Álvarez", "Julián Álvarez", "훌리안 알바레스", 24, "Argentina", "AR", "Madrid Red", "La Liga", 1, "ST", "SS", "FW", "Right", 170, 75.0, 180.0, 2030,
          "Relentless Spider Presser & Complete Forward",
          {"kp": 2.3, "prog_p": 4.1, "pass_acc": 82.0, "passes_att": 35.0, "through_balls": 0.52, "crosses_box": 1.1, "shots": 3.4, "box_shots": 2.5, "sot_pct": 44.0, "xg": 0.58, "npxg": 0.52, "goals": 0.55, "dribbles": 2.0, "dribble_pct": 58.0, "carry_dist": 220.0, "fouls_drawn": 1.9, "prog_carries": 4.2, "interceptions": 0.7, "tackles_won": 1.5, "clearances": 0.4, "blocks": 0.6, "recoveries": 4.9, "aerial_pct": 40.0, "ground_duels": 5.8, "aerial_duels": 0.7, "pressures": 22.0}),

        # --- SERIE A STARS ---
        ("p_pulisic", "C. Pulisic", "Christian Pulisic", "크리스천 풀리식", 25, "United States", "US", "Milan Red-Black", "Serie A", 1, "W", "RW", "FW", "Right", 178, 40.0, 90.0, 2027,
          "Clinical Dynamic Inverted Winger",
          {"kp": 2.4, "prog_p": 4.0, "pass_acc": 82.5, "passes_att": 36.0, "through_balls": 0.48, "crosses_box": 1.2, "shots": 2.8, "box_shots": 2.2, "sot_pct": 44.0, "xg": 0.48, "npxg": 0.48, "goals": 0.46, "dribbles": 2.8, "dribble_pct": 60.0, "carry_dist": 250.0, "fouls_drawn": 2.4, "prog_carries": 5.2, "interceptions": 0.6, "tackles_won": 1.4, "clearances": 0.4, "blocks": 0.5, "recoveries": 4.5, "aerial_pct": 36.0, "ground_duels": 5.8, "aerial_duels": 0.5, "pressures": 16.5}),

        ("p_theo", "T. Hernández", "Theo Hernández", "테오 에르난데스", 26, "France", "FR", "Milan Red-Black", "Serie A", 1, "FB", "LB", "DF", "Left", 184, 60.0, 120.0, 2026,
          "Unstoppable Locomotive Fullback",
          {"kp": 1.8, "prog_p": 5.2, "pass_acc": 84.0, "passes_att": 54.0, "through_balls": 0.40, "crosses_box": 1.4, "shots": 1.4, "box_shots": 0.8, "sot_pct": 35.0, "xg": 0.16, "npxg": 0.16, "goals": 0.15, "dribbles": 2.9, "dribble_pct": 65.0, "carry_dist": 310.0, "fouls_drawn": 2.8, "prog_carries": 6.2, "interceptions": 1.3, "tackles_won": 2.2, "clearances": 1.6, "blocks": 0.9, "recoveries": 6.4, "aerial_pct": 58.0, "ground_duels": 6.8, "aerial_duels": 1.6, "pressures": 15.0}),

        ("p_lookman", "A. Lookman", "Ademola Lookman", "아데몰라 루크먼", 26, "Nigeria", "NG", "Bergamo Black-Blue", "Serie A", 1, "W", "SS", "FW", "Right", 174, 40.0, 60.0, 2026,
          "Explosive Hat-Trick Matchwinner",
          {"kp": 2.5, "prog_p": 4.2, "pass_acc": 81.0, "passes_att": 35.0, "through_balls": 0.55, "crosses_box": 1.3, "shots": 3.4, "box_shots": 2.6, "sot_pct": 45.0, "xg": 0.54, "npxg": 0.54, "goals": 0.56, "dribbles": 3.4, "dribble_pct": 62.0, "carry_dist": 275.0, "fouls_drawn": 2.3, "prog_carries": 5.9, "interceptions": 0.6, "tackles_won": 1.4, "clearances": 0.3, "blocks": 0.5, "recoveries": 4.8, "aerial_pct": 34.0, "ground_duels": 5.9, "aerial_duels": 0.4, "pressures": 18.0}),

        # --- BUNDESLIGA STARS ---
        ("p_olise", "M. Olise", "Michael Olise", "마이클 올리세", 22, "France", "FR", "München Rot", "Bundesliga", 1, "W", "RW", "FW", "Left", 184, 65.0, 140.0, 2029,
          "Silky Left-Footed Playmaking Winger",
          {"kp": 3.2, "prog_p": 5.6, "pass_acc": 83.5, "passes_att": 46.0, "through_balls": 0.90, "crosses_box": 2.0, "shots": 2.8, "box_shots": 1.8, "sot_pct": 42.0, "xg": 0.44, "npxg": 0.44, "goals": 0.45, "dribbles": 3.2, "dribble_pct": 63.0, "carry_dist": 260.0, "fouls_drawn": 2.4, "prog_carries": 5.5, "interceptions": 0.7, "tackles_won": 1.7, "clearances": 0.4, "blocks": 0.6, "recoveries": 5.2, "aerial_pct": 42.0, "ground_duels": 6.2, "aerial_duels": 0.8, "pressures": 17.5}),

        ("p_boniface", "V. Boniface", "Victor Boniface", "빅터 보니페이스", 23, "Nigeria", "NG", "Leverkusen", "Bundesliga", 1, "ST", "CF", "FW", "Right", 189, 45.0, 60.0, 2028,
          "Dribbling Power Striker",
          {"kp": 1.7, "prog_p": 2.8, "pass_acc": 74.5, "passes_att": 24.0, "through_balls": 0.35, "crosses_box": 0.4, "shots": 4.4, "box_shots": 3.6, "sot_pct": 44.0, "xg": 0.74, "npxg": 0.68, "goals": 0.72, "dribbles": 2.9, "dribble_pct": 58.0, "carry_dist": 220.0, "fouls_drawn": 2.5, "prog_carries": 4.4, "interceptions": 0.3, "tackles_won": 0.8, "clearances": 0.7, "blocks": 0.4, "recoveries": 3.2, "aerial_pct": 52.0, "ground_duels": 6.8, "aerial_duels": 1.9, "pressures": 15.0}),

        ("p_xavi_simons", "X. Simons", "Xavi Simons", "사비 시몬스", 21, "Netherlands", "NL", "Leipzig Red", "Bundesliga", 1, "AM", "LW", "MF", "Right", 179, 80.0, 110.0, 2027,
          "Electric Creative Pocket Slasher",
          {"kp": 2.9, "prog_p": 5.4, "pass_acc": 82.0, "passes_att": 48.0, "through_balls": 0.78, "crosses_box": 1.4, "shots": 2.7, "box_shots": 1.6, "sot_pct": 40.0, "xg": 0.36, "npxg": 0.36, "goals": 0.34, "dribbles": 3.4, "dribble_pct": 61.0, "carry_dist": 280.0, "fouls_drawn": 2.9, "prog_carries": 5.8, "interceptions": 0.7, "tackles_won": 1.6, "clearances": 0.3, "blocks": 0.6, "recoveries": 5.1, "aerial_pct": 32.0, "ground_duels": 6.2, "aerial_duels": 0.4, "pressures": 18.5}),

        ("p_openda", "L. Openda", "Loïs Openda", "로이스 오펜다", 24, "Belgium", "BE", "Leipzig Red", "Bundesliga", 1, "ST", "CF", "FW", "Right", 177, 60.0, 90.0, 2028,
          "Speed Infiltrator & Box Finisher",
          {"kp": 1.3, "prog_p": 1.8, "pass_acc": 76.0, "passes_att": 19.0, "through_balls": 0.22, "crosses_box": 0.3, "shots": 3.8, "box_shots": 3.3, "sot_pct": 46.0, "xg": 0.72, "npxg": 0.64, "goals": 0.70, "dribbles": 1.7, "dribble_pct": 52.0, "carry_dist": 180.0, "fouls_drawn": 1.8, "prog_carries": 3.4, "interceptions": 0.4, "tackles_won": 0.7, "clearances": 0.5, "blocks": 0.3, "recoveries": 2.9, "aerial_pct": 42.0, "ground_duels": 5.1, "aerial_duels": 1.1, "pressures": 15.0}),

        # --- LIGUE 1 & OTHER GEMS ---
        ("p_david", "J. David", "Jonathan David", "조너선 데이비드", 24, "Canada", "CA", "Lille Red-Blue", "Ligue 1", 1, "ST", "SS", "FW", "Both", 175, 45.0, 70.0, 2025,
          "Intelligent Box Poacher & Link-Up 9",
          {"kp": 1.6, "prog_p": 2.6, "pass_acc": 81.0, "passes_att": 26.0, "through_balls": 0.32, "crosses_box": 0.3, "shots": 3.2, "box_shots": 2.8, "sot_pct": 47.0, "xg": 0.64, "npxg": 0.52, "goals": 0.62, "dribbles": 1.3, "dribble_pct": 54.0, "carry_dist": 160.0, "fouls_drawn": 1.8, "prog_carries": 2.8, "interceptions": 0.5, "tackles_won": 1.1, "clearances": 0.6, "blocks": 0.4, "recoveries": 3.5, "aerial_pct": 46.0, "ground_duels": 5.4, "aerial_duels": 1.2, "pressures": 18.0}),

        ("p_cherki", "R. Cherki", "Rayan Cherki", "라얀 체르키", 21, "France", "FR", "Lyon White", "Ligue 1", 1, "AM", "RW", "MF", "Both", 176, 20.0, 45.0, 2026,
          "Two-Footed Pure Dribble Magician",
          {"kp": 3.4, "prog_p": 6.2, "pass_acc": 82.5, "passes_att": 44.0, "through_balls": 0.92, "crosses_box": 1.8, "shots": 2.6, "box_shots": 1.4, "sot_pct": 38.0, "xg": 0.30, "npxg": 0.30, "goals": 0.22, "dribbles": 4.6, "dribble_pct": 68.0, "carry_dist": 290.0, "fouls_drawn": 2.6, "prog_carries": 6.2, "interceptions": 0.4, "tackles_won": 0.9, "clearances": 0.2, "blocks": 0.4, "recoveries": 4.2, "aerial_pct": 28.0, "ground_duels": 5.8, "aerial_duels": 0.3, "pressures": 13.0})
    ]

    for item in additional_stars:
        base_players.append({
            "id": item[0],
            "name": item[1],
            "full_name": item[2],
            "korean_name": item[3],
            "age": item[4],
            "nationality": item[5],
            "nat_code": item[6],
            "club": item[7],
            "league": item[8],
            "league_tier": item[9],
            "primary_pos": item[10],
            "secondary_pos": item[11],
            "pos_group": item[12],
            "foot": item[13],
            "height_cm": item[14],
            "market_value_eur": item[15],
            "wage_eur_pw": item[16],
            "contract_until": item[17],
            "tactical_role": item[18],
            "stats": {
                "matches": 30, "minutes": 2500,
                **item[19]
            }
        })

    world_players = generate_additional_world_players()
    base_players.extend(world_players)

    mega_players = generate_mega_dataset()
    base_players.extend(mega_players)

    return base_players

def build_database():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    players = generate_all_players()

    keys = [
        "kp", "prog_p", "pass_acc", "passes_att", "through_balls", "crosses_box",
        "shots", "box_shots", "sot_pct", "xg", "npxg", "goals",
        "dribbles", "dribble_pct", "carry_dist", "fouls_drawn", "prog_carries",
        "interceptions", "tackles_won", "clearances", "blocks", "recoveries",
        "aerial_pct", "ground_duels", "aerial_duels", "pressures"
    ]

    min_vals = {k: min(p["stats"][k] for p in players) for k in keys}
    max_vals = {k: max(p["stats"][k] for p in players) for k in keys}

    def normalize(val: float, key: str) -> float:
        min_v = min_vals[key]
        max_v = max_vals[key]
        if max_v == min_v:
            return 50.0
        return float(np.clip(((val - min_v) / (max_v - min_v)) * 100.0, 0.0, 100.0))

    cursor.execute("DELETE FROM tactical_ratings")
    cursor.execute("DELETE FROM player_stats_per90")
    cursor.execute("DELETE FROM players")

    leagues_data = [
        ("Premier League", "England", "GB-ENG", 1, 95),
        ("La Liga", "Spain", "ES", 1, 93),
        ("Bundesliga", "Germany", "DE", 1, 90),
        ("Serie A", "Italy", "IT", 1, 89),
        ("Ligue 1", "France", "FR", 1, 86),
        ("Eredivisie", "Netherlands", "NL", 2, 80),
        ("Liga Portugal", "Portugal", "PT", 2, 79),
        ("Belgian Pro League", "Belgium", "BE", 3, 75),
        ("Austrian Bundesliga", "Austria", "AT", 2, 74),
        ("Championship", "England", "GB-ENG", 2, 78),
        ("MLS", "United States", "US", 2, 72),
        ("Danish Superliga", "Denmark", "DK", 2, 73),
        ("Serbian SuperLiga", "Serbia", "RS", 2, 70),
        ("League One", "England", "GB-ENG", 3, 65),
        ("Saudi Pro League", "Saudi Arabia", "SA", 2, 75),
        ("K-League 1", "South Korea", "KR", 3, 75),
        ("J-League 1", "Japan", "JP", 3, 74),
    ]
    cursor.executemany("""
    INSERT OR REPLACE INTO leagues (id, name, country, country_code, tier, reputation)
    VALUES (?, ?, ?, ?, ?, ?)
    """, [(l[0], l[0], l[1], l[2], l[3], l[4]) for l in leagues_data])

    for p in players:
        cursor.execute("""
        INSERT INTO players (
            id, name, full_name, korean_name, age, nationality, nat_code, club, league,
            league_tier, primary_pos, secondary_pos, pos_group, foot,
            height_cm, market_value_eur, wage_eur_pw, contract_until, avatar_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["id"], p["name"], p["full_name"], p.get("korean_name"), p["age"], p["nationality"], p["nat_code"],
            p["club"], p["league"], p["league_tier"], p["primary_pos"], p["secondary_pos"],
            p["pos_group"], p["foot"], p["height_cm"], p["market_value_eur"], p["wage_eur_pw"],
            p["contract_until"], "silhouette_generic"
        ))

        s = p["stats"]
        cursor.execute("""
        INSERT INTO player_stats_per90 (
            player_id, matches_played, minutes_played,
            key_passes, progressive_passes, pass_completion_pct, passes_attempted, through_balls, crosses_into_box,
            shots, box_shots, shots_on_target_pct, xg, npxg, goals,
            dribbles_completed, dribble_success_pct, carrying_dist_prog, fouls_drawn, progressive_carries,
            interceptions, tackles_won, clearances, blocks, ball_recoveries,
            aerial_won_pct, ground_duels_won, aerial_duels_won, pressures
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["id"], s["matches"], s["minutes"],
            s["kp"], s["prog_p"], s["pass_acc"], s["passes_att"], s["through_balls"], s["crosses_box"],
            s["shots"], s["box_shots"], s["sot_pct"], s["xg"], s["npxg"], s["goals"],
            s["dribbles"], s["dribble_pct"], s["carry_dist"], s["fouls_drawn"], s["prog_carries"],
            s["interceptions"], s["tackles_won"], s["clearances"], s["blocks"], s["recoveries"],
            s["aerial_pct"], s["ground_duels"], s["aerial_duels"], s["pressures"]
        ))

        # 1. Vision & Pass
        norm_kp = normalize(s["kp"], "kp")
        norm_prog_p = normalize(s["prog_p"], "prog_p")
        norm_pass_acc = normalize(s["pass_acc"], "pass_acc")
        vision_score = round(norm_kp * 0.40 + norm_prog_p * 0.40 + norm_pass_acc * 0.20, 1)

        # 2. Striking & xG
        norm_shots = normalize(s["shots"], "shots")
        norm_box_shots = normalize(s["box_shots"], "box_shots")
        norm_sot = normalize(s["sot_pct"], "sot_pct")
        striking_score = round(norm_shots * 0.30 + norm_box_shots * 0.50 + norm_sot * 0.20, 1)

        # 3. Dribble & Carry
        norm_dribbles = normalize(s["dribbles"], "dribbles")
        norm_carry = normalize(s["carry_dist"], "carry_dist")
        norm_fouls = normalize(s["fouls_drawn"], "fouls_drawn")
        dribble_score = round(norm_dribbles * 0.40 + norm_carry * 0.40 + norm_fouls * 0.20, 1)

        # 4. Defense
        norm_inter = normalize(s["interceptions"], "interceptions")
        norm_tackles = normalize(s["tackles_won"], "tackles_won")
        norm_clear = normalize(s["clearances"], "clearances")
        defense_score = round(norm_inter * 0.35 + norm_tackles * 0.35 + norm_clear * 0.30, 1)

        # 5. Physical
        norm_aerial = normalize(s["aerial_pct"], "aerial_pct")
        norm_ground = normalize(s["ground_duels"], "ground_duels")
        physical_score = round(norm_aerial * 0.50 + norm_ground * 0.50, 1)

        pos = p["primary_pos"]
        if pos in ["ST", "CF"]:
            overall_score = round(striking_score * 0.60 + dribble_score * 0.25 + physical_score * 0.15, 1)
        elif pos in ["W", "LW", "RW"]:
            overall_score = round(dribble_score * 0.45 + striking_score * 0.30 + vision_score * 0.25, 1)
        elif pos == "AM":
            overall_score = round(vision_score * 0.55 + dribble_score * 0.30 + striking_score * 0.15, 1)
        elif pos == "CM":
            overall_score = round(vision_score * 0.35 + defense_score * 0.30 + dribble_score * 0.20 + physical_score * 0.15, 1)
        elif pos == "DM":
            overall_score = round(defense_score * 0.45 + physical_score * 0.30 + vision_score * 0.25, 1)
        elif pos in ["FB", "LB", "RB", "LWB", "RWB"]:
            overall_score = round(defense_score * 0.35 + dribble_score * 0.30 + vision_score * 0.20 + physical_score * 0.15, 1)
        elif pos == "CB":
            overall_score = round(defense_score * 0.50 + physical_score * 0.35 + vision_score * 0.15, 1)
        else:
            overall_score = round(defense_score * 0.35 + physical_score * 0.25 + vision_score * 0.20 + dribble_score * 0.20, 1)

        cursor.execute("""
        INSERT INTO tactical_ratings (
            player_id,
            vision_score, vision_grade,
            striking_score, striking_grade,
            dribble_score, dribble_grade,
            defense_score, defense_grade,
            physical_score, physical_grade,
            overall_score, overall_grade,
            tactical_role
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["id"],
            vision_score, score_to_grade(vision_score),
            striking_score, score_to_grade(striking_score),
            dribble_score, score_to_grade(dribble_score),
            defense_score, score_to_grade(defense_score),
            physical_score, score_to_grade(physical_score),
            overall_score, score_to_grade(overall_score),
            p["tactical_role"]
        ))

    conn.commit()
    conn.close()
    print(f"Successfully loaded and calculated {len(players)} player tactical profiles into scout_hub.sqlite")

if __name__ == "__main__":
    build_database()
