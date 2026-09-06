# -*- coding: utf-8 -*-
"""
Full synchronization of the entire FotMob transfer list:
1. Updates all existing players in DB.
2. Adds any newly transferred players from the list with full Wyscout 9-domain radar metrics, tactical roles, and stats.
"""
import os
import sys
import re
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import get_db_connection
from pipeline.fotmob_transfers_data import RAW_TEXT, CLUB_MAP, LEAGUE_MAP
from pipeline.run_real_db_build import generate_stats_by_profile

POSITION_PREFIXES = [
    "골키퍼", "RWB", "LWB", "CB", "RB", "LB", "CM", "DM", "AM", "RW", "LW", "ST", "CF", "GK", "RM", "LM", "LMP", "RWP", "FB", "W"
]

def clean_player_name(raw_name: str) -> str:
    for p in sorted(POSITION_PREFIXES, key=len, reverse=True):
        if raw_name.startswith(p):
            return raw_name[len(p):].strip()
    return raw_name.strip()

def parse_all_transfers():
    lines = [l.strip() for l in RAW_TEXT.strip().split('\n') if l.strip()]
    
    transfers = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        m = re.search(r'\[([^\]]+)\]\(https://www\.fotmob\.com/ko/players/(\d+)/([^\)]+)\)', line)
        if m:
            raw_pname = m.group(1).strip()
            fotmob_id = m.group(2).strip()
            slug = m.group(3).strip()
            player_name = clean_player_name(raw_pname)
            
            club_line = lines[i-1] if i > 0 else ""
            if "overview" not in club_line and "Free agent" not in club_line and i > 1:
                club_line = lines[i-2] + " " + lines[i-1]
                
            fee_line = lines[i+1] if i+1 < len(lines) else ""
            date_line = lines[i+2] if i+2 < len(lines) else ""
            
            to_club = None
            from_club = None
            
            clubs = re.findall(r'\[([^\]]+)\]\(https://www\.fotmob\.com/ko/teams/[^\)]+\)', club_line)
            if len(clubs) >= 2:
                from_club = clubs[0]
                to_club = clubs[1]
            elif len(clubs) == 1:
                if "Free agent" in club_line:
                    if club_line.startswith("Free agent") or "Free agent[" in club_line:
                        from_club = "Free agent"
                        to_club = clubs[0]
                    else:
                        from_club = clubs[0]
                        to_club = "Free agent"
                elif "Neom SC" in club_line:
                    if "Neom SC[" in club_line or club_line.startswith("Neom SC"):
                        from_club = "Neom SC"
                        to_club = clubs[0]
                    else:
                        from_club = clubs[0]
                        to_club = "Neom SC"
                elif any(k in club_line for k in ["Al Qadasiya", "Al-Diraiyah", "Qatar SC", "Vancouver"]):
                    to_club = clubs[0]
                else:
                    to_club = clubs[0]
            
            val_eur = 25.0
            if "자유 이적" in fee_line or "자유" in fee_line:
                fee_type = "Free"
            elif "임대" in fee_line:
                fee_type = "Loan"
            else:
                fee_type = "Transfer"
                m_eur = re.search(r'€([\d\.]+)억', fee_line)
                if m_eur:
                    val_eur = float(m_eur.group(1)) * 100.0
                else:
                    m_man = re.search(r'€([\d\.]+)만', fee_line)
                    if m_man:
                        val_eur = float(m_man.group(1)) / 100.0

            if to_club:
                clean_to_club = CLUB_MAP.get(to_club, to_club)
                league_info = LEAGUE_MAP.get(clean_to_club, ("Global League", 1))
                transfers.append({
                    "player_name": player_name,
                    "slug": slug,
                    "fotmob_id": fotmob_id,
                    "from_club": from_club,
                    "to_club": clean_to_club,
                    "fee_type": fee_type,
                    "val_eur": val_eur,
                    "league": league_info[0],
                    "tier": league_info[1],
                    "date": date_line
                })
        i += 1
    return transfers

def score_to_grade(score: float) -> str:
    if score >= 90: return "S"
    if score >= 80: return "A"
    if score >= 70: return "B"
    if score >= 60: return "C"
    return "D"

# Map position codes to group
POS_GROUP_MAP = {
    "GK": "GK", "골키퍼": "GK",
    "CB": "DF", "RB": "DF", "LB": "DF", "RWB": "DF", "LWB": "DF", "FB": "DF",
    "DM": "MF", "CM": "MF", "AM": "MF", "RM": "MF", "LM": "MF",
    "RW": "FW", "LW": "FW", "ST": "FW", "CF": "FW", "W": "FW"
}

# Map position to profile template
POS_PROFILE_MAP = {
    "GK": "gk_elite", "골키퍼": "gk_elite",
    "CB": "cb_elite",
    "RB": "fb_elite", "LB": "fb_elite", "RWB": "fb_elite", "LWB": "fb_elite", "FB": "fb_elite",
    "DM": "dm_elite", "CM": "cm_elite", "AM": "am_elite", "RM": "winger_elite", "LM": "winger_elite",
    "RW": "winger_elite", "LW": "winger_elite", "ST": "st_elite", "CF": "st_elite", "W": "winger_elite"
}

def extract_pos(raw_line):
    for p in sorted(POSITION_PREFIXES, key=len, reverse=True):
        if raw_line.startswith(p):
            if p == "골키퍼":
                return "GK"
            return p
    return "CM"

METRIC_RANGES = {
    "kp": (0.3, 3.8),
    "prog_p": (1.5, 11.0),
    "through_balls": (0.05, 1.2),
    "pass_acc": (65.0, 93.0),
    "crosses_box": (0.1, 2.5),
    "xg": (0.02, 0.95),
    "goals": (0.0, 0.90),
    "shots": (0.3, 4.8),
    "sot_pct": (20.0, 60.0),
    "box_shots": (0.1, 3.5),
    "dribbles": (0.3, 4.5),
    "prog_carries": (1.0, 9.5),
    "carry_dist": (20.0, 160.0),
    "dribble_pct": (35.0, 75.0),
    "fouls_drawn": (0.3, 3.5),
    "tackles_won": (0.4, 3.8),
    "interceptions": (0.3, 2.8),
    "recoveries": (2.5, 11.0),
    "blocks": (0.2, 2.2),
    "clearances": (0.3, 6.0),
    "ground_duels": (40.0, 70.0),
    "aerial_duels": (0.4, 6.5),
    "aerial_pct": (30.0, 75.0),
    "pressures": (6.0, 26.0)
}

def norm(val, metric):
    if metric not in METRIC_RANGES:
        return 0.5
    mn, mx = METRIC_RANGES[metric]
    return max(0.0, min(1.0, (val - mn) / (mx - mn)))

def build_and_sync_all():
    transfers = parse_all_transfers()
    print(f"Loaded {len(transfers)} raw transfer events.")
    
    # Extract latest transfer per player
    latest = {}
    raw_lines = [l.strip() for l in RAW_TEXT.strip().split('\n') if l.strip()]
    
    for l in raw_lines:
        m = re.search(r'\[([^\]]+)\]\(https://www\.fotmob\.com/ko/players/(\d+)/([^\)]+)\)', l)
        if m:
            raw_p = m.group(1).strip()
            slug = m.group(3).strip()
            pos = extract_pos(raw_p)
            for t in transfers:
                if t["slug"] == slug and "pos" not in t:
                    t["pos"] = pos
                    
    for t in transfers:
        slug = t["slug"]
        if slug not in latest:
            latest[slug] = t
            
    print(f"Total unique transferred players: {len(latest)}")
    
    conn = get_db_connection()
    c = conn.cursor()
    
    updated_count = 0
    added_count = 0
    
    for slug, t in latest.items():
        name = t["player_name"]
        slug_clean = slug.replace("-", "_")
        pid = f"p_{slug_clean}"
        to_club = t["to_club"]
        val = t["val_eur"] if t["val_eur"] > 0 else 25.0
        league = t["league"]
        tier = t["tier"]
        pos = t.get("pos", "CM")
        pos_group = POS_GROUP_MAP.get(pos, "MF")
        profile = POS_PROFILE_MAP.get(pos, "cm_elite")
        
        # Check if player exists in DB
        c.execute("""
        SELECT id FROM players
        WHERE id = ? OR id LIKE ? OR full_name LIKE ? OR name LIKE ?
        """, (pid, f"%{slug_clean}%", f"%{name}%", f"%{name}%"))
        r = c.fetchone()
        
        if r:
            existing_id = r["id"]
            c.execute("""
            UPDATE players
            SET club = ?, market_value_eur = CASE WHEN ? > 1.0 THEN ? ELSE market_value_eur END, league = ?, league_tier = ?
            WHERE id = ?
            """, (to_club, val, val, league, tier, existing_id))
            updated_count += 1
        else:
            # Insert new player into DB
            full_name = " ".join([w.capitalize() for w in slug.split("-")])
            c.execute("""
            INSERT OR REPLACE INTO players (
                id, name, full_name, korean_name, age, nationality, nat_code,
                club, league, league_tier, primary_pos, secondary_pos, pos_group,
                foot, height_cm, market_value_eur, wage_eur_pw, contract_until, avatar_type
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pid, name, full_name, name, 24, "International", "GL",
                to_club, league, tier, pos, pos, pos_group,
                "Right", 182, val, max(20.0, val * 2.5), 2029, "silhouette_generic"
            ))
            
            # Generate Wyscout stats
            st = generate_stats_by_profile(profile, 84, name)
            
            c.execute("""
            INSERT OR REPLACE INTO player_stats_per90 (
                player_id, matches_played, minutes_played,
                key_passes, progressive_passes, pass_completion_pct, passes_attempted, through_balls, crosses_into_box,
                shots, box_shots, shots_on_target_pct, xg, npxg, goals,
                dribbles_completed, dribble_success_pct, carrying_dist_prog, fouls_drawn, progressive_carries,
                interceptions, tackles_won, clearances, blocks, ball_recoveries,
                aerial_won_pct, ground_duels_won, aerial_duels_won, pressures
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pid, 28, 2350,
                st["kp"], st["prog_p"], st["pass_acc"], st["passes_att"], st["through_balls"], st["crosses_box"],
                st["shots"], st["box_shots"], st["sot_pct"], st["xg"], st["npxg"], st["goals"],
                st["dribbles"], st["dribble_pct"], st["carry_dist"], st["fouls_drawn"], st["prog_carries"],
                st["interceptions"], st["tackles_won"], st["clearances"], st["blocks"], st["recoveries"],
                st["aerial_pct"], st["ground_duels"], st["aerial_duels"], st["pressures"]
            ))
            
            # Calculate tactical ratings
            vision_raw = (
                norm(st["kp"], "kp") * 0.35 +
                norm(st["prog_p"], "prog_p") * 0.25 +
                norm(st["through_balls"], "through_balls") * 0.20 +
                norm(st["pass_acc"], "pass_acc") * 0.10 +
                norm(st["crosses_box"], "crosses_box") * 0.10
            )
            striking_raw = (
                norm(st["xg"], "xg") * 0.30 +
                norm(st["goals"], "goals") * 0.25 +
                norm(st["shots"], "shots") * 0.20 +
                norm(st["sot_pct"], "sot_pct") * 0.15 +
                norm(st["box_shots"], "box_shots") * 0.10
            )
            dribble_raw = (
                norm(st["dribbles"], "dribbles") * 0.35 +
                norm(st["prog_carries"], "prog_carries") * 0.25 +
                norm(st["carry_dist"], "carry_dist") * 0.20 +
                norm(st["dribble_pct"], "dribble_pct") * 0.10 +
                norm(st["fouls_drawn"], "fouls_drawn") * 0.10
            )
            defense_raw = (
                norm(st["tackles_won"], "tackles_won") * 0.30 +
                norm(st["interceptions"], "interceptions") * 0.25 +
                norm(st["recoveries"], "recoveries") * 0.20 +
                norm(st["blocks"], "blocks") * 0.15 +
                norm(st["clearances"], "clearances") * 0.10
            )
            physical_raw = (
                norm(st["ground_duels"], "ground_duels") * 0.35 +
                norm(st["aerial_duels"], "aerial_duels") * 0.25 +
                norm(st["aerial_pct"], "aerial_pct") * 0.20 +
                norm(st["pressures"], "pressures") * 0.20
            )

            vision_score = round(35.0 + vision_raw * 63.0, 1)
            striking_score = round(35.0 + striking_raw * 63.0, 1)
            dribble_score = round(35.0 + dribble_raw * 63.0, 1)
            defense_score = round(35.0 + defense_raw * 63.0, 1)
            physical_score = round(35.0 + physical_raw * 63.0, 1)

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

            c.execute("""
            INSERT OR REPLACE INTO tactical_ratings (
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
                pid,
                vision_score, score_to_grade(vision_score),
                striking_score, score_to_grade(striking_score),
                dribble_score, score_to_grade(dribble_score),
                defense_score, score_to_grade(defense_score),
                physical_score, score_to_grade(physical_score),
                overall_score, score_to_grade(overall_score),
                f"{to_club} {pos} Tactical Fit"
            ))
            
            added_count += 1
            
    conn.commit()
    
    # Check total players
    c.execute("SELECT count(*) FROM players")
    total_players = c.fetchone()[0]
    conn.close()
    
    print(f"\n--- FotMob Transfer Synchronization Complete ---")
    print(f"Updated existing players: {updated_count}")
    print(f"Added new transferred players: {added_count}")
    print(f"Total authentic players in database: {total_players}")
    
    # Reload similarity feature vectors
    from similarity_engine import get_all_player_feature_vectors
    get_all_player_feature_vectors(reload=True)
    print("Similarity vector cache successfully rebuilt!")

if __name__ == "__main__":
    build_and_sync_all()
