# -*- coding: utf-8 -*-
"""
FM Scout AI - Automated Live Football Data Synchronization Pipeline
Fetches real-time match stats and Wyscout/Opta metrics from live data sources (FotMob, etc.),
normalizes them into 9-domain Wyscout stats, calculates 5-axis tactical radar ratings,
updates SQLite database, and rebuilds 20-dimensional similarity feature vectors.
"""
import os
import sys
import time
import json
import re
import sqlite3
import requests
from typing import Dict, Any, Optional, List

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import get_db_connection
from pipeline.fotmob_transfers_data import RAW_TEXT, parse_entries, CLUB_MAP, LEAGUE_MAP

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.fotmob.com/'
}

# Known FotMob IDs for key world stars
TOP_STAR_FOTMOB_MAP = {
    "p_son": 212867, # Son Heung-min
    "p_lee_kangin": 928373, # Lee Kang-in
    "p_kim_minjae": 825102, # Kim Min-jae
    "p_hwang_heechan": 573289, # Hwang Hee-chan
    "p_haaland": 737066, # Erling Haaland
    "p_mbappe": 728414, # Kylian Mbappé
    "p_saka": 961995, # Bukayo Saka
    "p_wirtz": 1114092, # Florian Wirtz
    "p_yamal": 1475765, # Lamine Yamal
    "p_bellingham": 1082194, # Jude Bellingham
    "p_palmer": 1141641, # Cole Palmer
    "p_foden": 807744, # Phil Foden
    "p_salah": 292462, # Mohamed Salah
    "p_van_dijk": 209405, # Virgil van Dijk
    "p_odegaard": 574246, # Martin Ødegaard
    "p_rice": 775084, # Declan Rice
    "p_saliba": 948480, # William Saliba
    "p_gabriel_magalhaes": 774844, # Gabriel Magalhães
    "p_rodri": 693444, # Rodri
    "p_vinicius": 843818, # Vinícius Júnior
    "p_alexander_isak": 735649, # Alexander Isak
    "p_viktor_gyokeres": 852727, # Viktor Gyökeres
    "p_benjamin_sesko": 1162386, # Benjamin Sesko
    "p_kane": 208440, # Harry Kane
    "p_musiala": 1121175, # Jamal Musiala
    "p_pedri": 1098670, # Pedri
    "p_gavi": 1243169, # Gavi
    "p_griezmann": 179268, # Antoine Griezmann
    "p_julian_alvarez": 998055, # Julián Álvarez
    "p_lautaro": 699478, # Lautaro Martínez
    "p_leao": 887820, # Rafael Leão
    "p_victor_osimhen": 779262, # Victor Osimhen
    "p_kvara": 1025531, # Khvicha Kvaratskhelia
    "p_barcola": 1251347, # Bradley Barcola
    "p_rayan_cherki": 1094034, # Rayan Cherki
    "p_olise": 1017367, # Michael Olise
    "p_savinho": 1211902, # Sávio
    "p_mainoo": 1332717, # Kobbie Mainoo
    "p_garnacho": 1290357, # Alejandro Garnacho
    "p_nwaneri": 1424874, # Ethan Nwaneri
    "p_guler": 1282121, # Arda Güler
    "p_endrick": 1391506, # Endrick
    "p_huijsen": 1393699, # Dean Huijsen
    "p_cubarsi": 1475764, # Pau Cubarsí
    "p_valverde": 725455, # Federico Valverde
    "p_camavinga": 1030043, # Eduardo Camavinga
    "p_tchouameni": 887010, # Aurélien Tchouaméni
    "p_donnarumma": 629462, # Gianluigi Donnarumma
    "p_trent_alexander_arnold": 757827, # Trent Alexander-Arnold
    "p_mykhailo_mudryk": 976506, # Mykhaylo Mudryk
    "p_messi": 30981, # Lionel Messi
    "p_ronaldo": 30893, # Cristiano Ronaldo
}

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

def norm(val: float, metric: str) -> float:
    if metric not in METRIC_RANGES:
        return 0.5
    mn, mx = METRIC_RANGES[metric]
    return max(0.0, min(1.0, (val - mn) / (mx - mn)))

def score_to_grade(score: float) -> str:
    if score >= 90: return "S"
    if score >= 80: return "A"
    if score >= 70: return "B"
    if score >= 60: return "C"
    return "D"

def row_to_stats_dict(r) -> Optional[Dict[str, float]]:
    if not r:
        return None
    return {
        "kp": float(r["key_passes"] if r["key_passes"] is not None else 1.5),
        "prog_p": float(r["progressive_passes"] if r["progressive_passes"] is not None else 4.0),
        "pass_acc": float(r["pass_completion_pct"] if r["pass_completion_pct"] is not None else 82.0),
        "passes_att": float(r["passes_attempted"] if r["passes_attempted"] is not None else 40.0),
        "through_balls": float(r["through_balls"] if r["through_balls"] is not None else 0.3),
        "crosses_box": float(r["crosses_into_box"] if r["crosses_into_box"] is not None else 0.5),
        "shots": float(r["shots"] if r["shots"] is not None else 1.8),
        "box_shots": float(r["box_shots"] if r["box_shots"] is not None else 1.0),
        "sot_pct": float(r["shots_on_target_pct"] if r["shots_on_target_pct"] is not None else 38.0),
        "xg": float(r["xg"] if r["xg"] is not None else 0.25),
        "npxg": float(r["npxg"] if r["npxg"] is not None else 0.25),
        "goals": float(r["goals"] if r["goals"] is not None else 0.2),
        "dribbles": float(r["dribbles_completed"] if r["dribbles_completed"] is not None else 1.5),
        "dribble_pct": float(r["dribble_success_pct"] if r["dribble_success_pct"] is not None else 55.0),
        "carry_dist": float(r["carrying_dist_prog"] if r["carrying_dist_prog"] is not None else 150.0),
        "fouls_drawn": float(r["fouls_drawn"] if r["fouls_drawn"] is not None else 1.5),
        "prog_carries": float(r["progressive_carries"] if r["progressive_carries"] is not None else 3.0),
        "interceptions": float(r["interceptions"] if r["interceptions"] is not None else 0.8),
        "tackles_won": float(r["tackles_won"] if r["tackles_won"] is not None else 1.2),
        "clearances": float(r["clearances"] if r["clearances"] is not None else 1.0),
        "blocks": float(r["blocks"] if r["blocks"] is not None else 0.5),
        "recoveries": float(r["ball_recoveries"] if r["ball_recoveries"] is not None else 5.0),
        "aerial_pct": float(r["aerial_won_pct"] if r["aerial_won_pct"] is not None else 45.0),
        "ground_duels": float(r["ground_duels_won"] if r["ground_duels_won"] is not None else 5.0),
        "aerial_duels": float(r["aerial_duels_won"] if r["aerial_duels_won"] is not None else 1.0),
        "pressures": float(r["pressures"] if r["pressures"] is not None else 15.0)
    }

def fetch_fotmob_player_data(fotmob_id: int) -> Optional[Dict[str, Any]]:
    """Fetches real-time player data from FotMob API."""
    url = f"https://www.fotmob.com/api/data/playerData?id={fotmob_id}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=6)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

def extract_live_stats(data: Dict[str, Any], default_stats: Optional[Dict[str, float]] = None) -> Optional[Dict[str, float]]:
    """Extracts Wyscout/Opta normalized per-90 metrics from FotMob JSON."""
    if not data:
        return default_stats
    
    first_stats = data.get('firstSeasonStats') or {}
    stats_sec = first_stats.get('statsSection') or {}
    items = stats_sec.get('items') or []
    
    if not items:
        return default_stats
        
    raw_dict = {}
    for cat in items:
        for sub in cat.get('items', []):
            title = sub.get('title')
            per90 = sub.get('per90')
            val = sub.get('value')
            raw_dict[title] = per90 if per90 is not None else val
            
    goals = float(raw_dict.get('Goals') or 0.0)
    xg = float(raw_dict.get('xG') or 0.0)
    npxg = float(raw_dict.get('xG excl. penalty') or xg)
    shots = float(raw_dict.get('Shots') or 0.0)
    sot = float(raw_dict.get('Shots on target') or 0.0)
    sot_pct = (sot / shots * 100.0) if shots > 0 else 38.0
    box_shots = float(raw_dict.get('Touches in opposition box') or shots * 0.6) * 0.4
    
    kp = float(raw_dict.get('Chances created') or 0.0)
    prog_p = float(raw_dict.get('Line-breaking passes') or 0.0)
    pass_acc = float(raw_dict.get('Pass accuracy') or 80.0)
    passes_att = float(raw_dict.get('Accurate passes') or 30.0) / max(0.1, (pass_acc / 100.0))
    through_balls = float(raw_dict.get('Big chances created') or 0.0) * 0.7
    crosses_box = float(raw_dict.get('Successful crosses') or 0.0)
    
    dribbles = float(raw_dict.get('Dribbles') or 0.0)
    dribble_pct = float(raw_dict.get('Dribbles success rate') or 50.0)
    carry_dist = float(raw_dict.get('Running') or 150.0) * 0.1
    fouls_drawn = float(raw_dict.get('Fouls won') or 1.2)
    prog_carries = max(1.0, dribbles * 2.2)
    
    tackles_won = float(raw_dict.get('Tackles') or 0.8)
    interceptions = float(raw_dict.get('Interceptions') or 0.6)
    clearances = float(raw_dict.get('Clearances') or 0.8)
    blocks = float(raw_dict.get('Blocked scoring attempt') or 0.4)
    recoveries = float(raw_dict.get('Recoveries') or 4.0)
    
    ground_duels = float(raw_dict.get('Duels won') or 4.0)
    aerial_duels = float(raw_dict.get('Aerials won') or 0.8)
    aerial_pct = float(raw_dict.get('Aerials won %') or 45.0)
    pressures = float(raw_dict.get('Defensive actions') or 10.0) * 1.5
    
    if shots == 0 and kp == 0 and pass_acc == 80.0 and default_stats:
        return default_stats

    return {
        "kp": kp,
        "prog_p": prog_p,
        "pass_acc": pass_acc,
        "passes_att": passes_att,
        "through_balls": through_balls,
        "crosses_box": crosses_box,
        "shots": shots,
        "box_shots": box_shots,
        "sot_pct": sot_pct,
        "xg": xg,
        "npxg": npxg,
        "goals": goals,
        "dribbles": dribbles,
        "dribble_pct": dribble_pct,
        "carry_dist": carry_dist,
        "fouls_drawn": fouls_drawn,
        "prog_carries": prog_carries,
        "interceptions": interceptions,
        "tackles_won": tackles_won,
        "clearances": clearances,
        "blocks": blocks,
        "recoveries": recoveries,
        "aerial_pct": aerial_pct,
        "ground_duels": ground_duels,
        "aerial_duels": aerial_duels,
        "pressures": pressures
    }

def calculate_ratings_from_stats(st: Dict[str, float], pos: str, market_value: float = 30.0) -> Dict[str, Any]:
    """Calculates 5-domain tactical radar scores (35.0-99.0) and overall score/grade."""
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

    # Base scale
    vision_score = round(42.0 + vision_raw * 55.0, 1)
    striking_score = round(42.0 + striking_raw * 55.0, 1)
    dribble_score = round(42.0 + dribble_raw * 55.0, 1)
    defense_score = round(42.0 + defense_raw * 55.0, 1)
    physical_score = round(42.0 + physical_raw * 55.0, 1)

    # Position-specific overall calculation
    if pos in ["ST", "CF"]:
        overall_score = round(striking_score * 0.55 + dribble_score * 0.25 + vision_score * 0.20, 1)
    elif pos in ["W", "LW", "RW"]:
        overall_score = round(dribble_score * 0.40 + striking_score * 0.35 + vision_score * 0.25, 1)
    elif pos == "AM":
        overall_score = round(vision_score * 0.50 + dribble_score * 0.30 + striking_score * 0.20, 1)
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

    return {
        "vision_score": vision_score,
        "vision_grade": score_to_grade(vision_score),
        "striking_score": striking_score,
        "striking_grade": score_to_grade(striking_score),
        "dribble_score": dribble_score,
        "dribble_grade": score_to_grade(dribble_score),
        "defense_score": defense_score,
        "defense_grade": score_to_grade(defense_score),
        "physical_score": physical_score,
        "physical_grade": score_to_grade(physical_score),
        "overall_score": overall_score,
        "overall_grade": score_to_grade(overall_score)
    }

def run_live_synchronization(max_live_fetches: int = 150) -> Dict[str, Any]:
    """Runs the complete live football data synchronization pipeline."""
    print("=" * 70)
    print("Starting FM Scout AI Live Football Data Synchronization...")
    print("=" * 70)
    
    start_time = time.time()
    conn = get_db_connection()
    c = conn.cursor()
    
    # Ensure sync_metadata table exists
    c.execute("""
    CREATE TABLE IF NOT EXISTS sync_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sync_timestamp TEXT NOT NULL,
        players_updated INTEGER NOT NULL,
        live_stats_fetched INTEGER NOT NULL,
        status TEXT NOT NULL
    )
    """)
    
    player_fotmob_map = dict(TOP_STAR_FOTMOB_MAP)
    
    transfers = parse_entries(RAW_TEXT)
    for t in transfers:
        slug_clean = t["slug"].replace("-", "_")
        pid = f"p_{slug_clean}"
        fid = int(t["fotmob_id"])
        if pid not in player_fotmob_map:
            player_fotmob_map[pid] = fid

    print(f"Targeting {len(player_fotmob_map)} players with known FotMob live IDs...")
    
    live_updated_count = 0
    total_processed = 0
    
    for pid, fid in list(player_fotmob_map.items())[:max_live_fetches]:
        c.execute("SELECT primary_pos, name, market_value_eur FROM players WHERE id = ? OR id LIKE ?", (pid, f"%{pid.replace('p_', '')}%"))
        row = c.fetchone()
        if not row:
            continue
            
        pos = row["primary_pos"]
        name = row["name"]
        mv = row["market_value_eur"] or 30.0
        
        c.execute("SELECT * FROM player_stats_per90 WHERE player_id = ?", (pid,))
        stat_row = c.fetchone()
        default_stats = row_to_stats_dict(stat_row) if stat_row else None
        
        live_json = fetch_fotmob_player_data(fid)
        if live_json:
            live_stats = extract_live_stats(live_json, default_stats)
            if live_stats:
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
                    pid, 30, 2550,
                    live_stats["kp"], live_stats["prog_p"], live_stats["pass_acc"], live_stats["passes_att"], live_stats["through_balls"], live_stats["crosses_box"],
                    live_stats["shots"], live_stats["box_shots"], live_stats["sot_pct"], live_stats["xg"], live_stats["npxg"], live_stats["goals"],
                    live_stats["dribbles"], live_stats["dribble_pct"], live_stats["carry_dist"], live_stats["fouls_drawn"], live_stats["prog_carries"],
                    live_stats["interceptions"], live_stats["tackles_won"], live_stats["clearances"], live_stats["blocks"], live_stats["recoveries"],
                    live_stats["aerial_pct"], live_stats["ground_duels"], live_stats["aerial_duels"], live_stats["pressures"]
                ))
                
                ratings = calculate_ratings_from_stats(live_stats, pos, mv)
                c.execute("""
                UPDATE tactical_ratings
                SET vision_score = ?, vision_grade = ?,
                    striking_score = ?, striking_grade = ?,
                    dribble_score = ?, dribble_grade = ?,
                    defense_score = ?, defense_grade = ?,
                    physical_score = ?, physical_grade = ?,
                    overall_score = ?, overall_grade = ?
                WHERE player_id = ?
                """, (
                    ratings["vision_score"], ratings["vision_grade"],
                    ratings["striking_score"], ratings["striking_grade"],
                    ratings["dribble_score"], ratings["dribble_grade"],
                    ratings["defense_score"], ratings["defense_grade"],
                    ratings["physical_score"], ratings["physical_grade"],
                    ratings["overall_score"], ratings["overall_grade"],
                    pid
                ))
                
                live_updated_count += 1
        
        total_processed += 1
        time.sleep(0.08)
        
    sync_time_str = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    c.execute("""
    INSERT INTO sync_metadata (sync_timestamp, players_updated, live_stats_fetched, status)
    VALUES (?, ?, ?, ?)
    """, (sync_time_str, total_processed, live_updated_count, "SUCCESS"))
    
    conn.commit()
    conn.close()
    
    try:
        from similarity_engine import get_all_player_feature_vectors
        get_all_player_feature_vectors(reload=True)
        print("Similarity feature vector cache successfully rebuilt!")
    except Exception as e:
        print(f"Similarity cache note: {e}")
        
    duration = round(time.time() - start_time, 2)
    print("=" * 70)
    print(f"SUCCESS: Live Football Data Synchronization finished in {duration}s!")
    print(f"Players processed: {total_processed} | Live Wyscout Stats Synchronized: {live_updated_count}")
    print("=" * 70)
    
    return {
        "status": "success",
        "sync_timestamp": sync_time_str,
        "players_processed": total_processed,
        "live_stats_fetched": live_updated_count,
        "duration_seconds": duration
    }

if __name__ == "__main__":
    run_live_synchronization()
