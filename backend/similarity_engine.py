"""
FM Scout AI (FC Finder) - Similarity Engine
Calculates multi-dimensional tactical similarity between football players using:
1. Cosine Similarity (Tactical playstyle ratio / pattern matching)
2. Euclidean Distance (Absolute performance volume & capacity matching)
Incorporates position-group pre-filtering and Min-Max feature normalization.
"""
import math
import numpy as np
from typing import List, Dict, Any, Optional
from database import get_db_connection

# Features used for tactical player similarity calculation
TACTICAL_FEATURE_KEYS = [
    # Passing & Vision
    "key_passes", "progressive_passes", "pass_completion_pct", "passes_attempted", "through_balls", "crosses_into_box",
    # Striking & Finishing
    "shots", "box_shots", "shots_on_target_pct", "xg", "goals",
    # Dribbling & Ball Carrying
    "dribbles_completed", "dribble_success_pct", "carrying_dist_prog", "fouls_drawn", "progressive_carries",
    # Defending
    "interceptions", "tackles_won", "clearances", "blocks", "ball_recoveries",
    # Physical & Duels
    "aerial_won_pct", "ground_duels_won", "aerial_duels_won", "pressures"
]

POSITION_GROUPS = {
    "FW": ["ST", "CF", "W", "LW", "RW"],
    "MF": ["AM", "CM", "DM", "LM", "RM"],
    "DF": ["CB", "FB", "LB", "RB", "LWB", "RWB"]
}

_CACHED_ALL_PLAYERS = None

def get_all_player_feature_vectors(reload: bool = False):
    """Fetches all player records, their per-90 stats, and tactical ratings with in-memory caching."""
    global _CACHED_ALL_PLAYERS
    if _CACHED_ALL_PLAYERS is not None and not reload:
        return _CACHED_ALL_PLAYERS

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        p.id, p.name, p.full_name, p.korean_name, p.age, p.nationality, p.nat_code, p.club, p.league, p.league_tier,
        p.primary_pos, p.secondary_pos, p.pos_group, p.foot, p.height_cm, p.market_value_eur, p.wage_eur_pw,
        p.contract_until, p.avatar_type,
        
        -- Per 90 stats
        s.matches_played, s.minutes_played,
        s.key_passes, s.progressive_passes, s.pass_completion_pct, s.passes_attempted, s.through_balls, s.crosses_into_box,
        s.shots, s.box_shots, s.shots_on_target_pct, s.xg, s.npxg, s.goals,
        s.dribbles_completed, s.dribble_success_pct, s.carrying_dist_prog, s.fouls_drawn, s.progressive_carries,
        s.interceptions, s.tackles_won, s.clearances, s.blocks, s.ball_recoveries,
        s.aerial_won_pct, s.ground_duels_won, s.aerial_duels_won, s.pressures,
        
        -- Tactical ratings
        r.vision_score, r.vision_grade,
        r.striking_score, r.striking_grade,
        r.dribble_score, r.dribble_grade,
        r.defense_score, r.defense_grade,
        r.physical_score, r.physical_grade,
        r.overall_score, r.overall_grade,
        r.tactical_role
    FROM players p
    JOIN player_stats_per90 s ON p.id = s.player_id
    JOIN tactical_ratings r ON p.id = r.player_id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    players = [dict(row) for row in rows]
    _CACHED_ALL_PLAYERS = players
    return players

def calculate_normalized_vectors(players: List[Dict[str, Any]], custom_weights: Optional[Dict[str, float]] = None):
    """
    Normalizes all player stats to [0, 100] percentile space
    and applies optional tactical pillar category weights.
    """
    if not players:
        return {}, {}, {}

    # Find min and max for each metric across the entire player pool
    min_vals = {k: min(p[k] for p in players) for k in TACTICAL_FEATURE_KEYS}
    max_vals = {k: max(p[k] for p in players) for k in TACTICAL_FEATURE_KEYS}

    # Category weight mapping
    weights = {
        "vision": 1.0,
        "striking": 1.0,
        "dribble": 1.0,
        "defense": 1.0,
        "physical": 1.0
    }
    if custom_weights:
        for k in weights:
            if k in custom_weights and custom_weights[k] is not None:
                weights[k] = float(custom_weights[k])

    metric_category = {
        "key_passes": "vision", "progressive_passes": "vision", "pass_completion_pct": "vision",
        "passes_attempted": "vision", "through_balls": "vision", "crosses_into_box": "vision",
        "shots": "striking", "box_shots": "striking", "shots_on_target_pct": "striking", "xg": "striking", "goals": "striking",
        "dribbles_completed": "dribble", "dribble_success_pct": "dribble", "carrying_dist_prog": "dribble",
        "fouls_drawn": "dribble", "progressive_carries": "dribble",
        "interceptions": "defense", "tackles_won": "defense", "clearances": "defense", "blocks": "defense", "ball_recoveries": "defense",
        "aerial_won_pct": "physical", "ground_duels_won": "physical", "aerial_duels_won": "physical", "pressures": "physical"
    }

    vectors = {}
    for p in players:
        vec = []
        for k in TACTICAL_FEATURE_KEYS:
            min_v = min_vals[k]
            max_v = max_vals[k]
            if max_v == min_v:
                norm_v = 50.0
            else:
                norm_v = ((p[k] - min_v) / (max_v - min_v)) * 100.0
            
            # Apply category weight
            cat = metric_category.get(k, "vision")
            w = weights.get(cat, 1.0)
            vec.append(norm_v * w)
        vectors[p["id"]] = np.array(vec, dtype=float)

    return vectors, min_vals, max_vals

def compute_cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """
    Computes Cosine Similarity between vector A and vector B.
    Cosine Similarity = (A . B) / (||A|| * ||B||)
    Rescales [0.60, 1.0] to [40%, 100%] to provide genuine tactical scouting nuance.
    """
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    cos_val = float(np.dot(vec_a, vec_b) / (norm_a * norm_b))
    # Rescale so nuances in shooting/passing/dribble styles are clearly reflected
    rescaled = 40.0 + max(0.0, min(1.0, (cos_val - 0.60) / 0.40)) * 60.0
    return round(rescaled, 1)

def compute_euclidean_similarity(vec_a: np.ndarray, vec_b: np.ndarray, max_possible_dist: float = 140.0) -> (float, float):
    """
    Computes Euclidean Distance and converts to normalized similarity percentage.
    Uses practical volume threshold (~140) to reflect performance capacity differences.
    """
    dist = float(np.linalg.norm(vec_a - vec_b))
    similarity_pct = max(0.0, min(100.0, (1.0 - (dist / 140.0)) * 100.0))
    return round(similarity_pct, 1), round(dist, 2)

def generate_ai_scout_briefing(target: Dict[str, Any], cand: Dict[str, Any], sim_pct: float, cos_pct: float, euc_pct: float, diff: Dict[str, float]) -> str:
    """Generates an insightful, human-readable Korean AI scouting briefing."""
    target_name = target.get("korean_name") or target.get("name")
    
    strengths = []
    if diff.get("dribbles_completed", 0) > 0.4:
        strengths.append("민첩한 온더볼 드리블 돌파력")
    elif diff.get("key_passes", 0) > 0.3 or diff.get("progressive_passes", 0) > 0.8:
        strengths.append("창의적인 찬스 메이킹 & 전진 패스")
    elif diff.get("shots", 0) > 0.3 or diff.get("box_shots", 0) > 0.3:
        strengths.append("과감한 박스 침투 및 슈팅 결정력")
    elif diff.get("ground_duels_won", 0) > 0.6 or diff.get("aerial_won_pct", 0) > 5.0:
        strengths.append("강인한 신체 경합 및 제공권 우위")
    elif (diff.get("tackles_won", 0) + diff.get("interceptions", 0)) > 0.5:
        strengths.append("적극적인 전방 압박 & 수비 기여도")
    
    val_note = ""
    if cand.get("market_value_eur", 0) < target.get("market_value_eur", 0) * 0.5:
        val_note = "이적료 대비 가성비가 극대화된"
    elif cand.get("age", 25) <= 23:
        val_note = "향후 폭발적 성장이 기대되는 U-23"
    else:
        val_note = "전술 스타일이 정밀하게 일치하는"

    if strengths:
        highlight = strengths[0]
        return f"{target_name} 대비 {highlight}을(를) 갖추고 전술 스타일 {int(cos_pct)}% 일치하는 {val_note} 자원"
    else:
        return f"{target_name}의 전술 롤과 퍼포먼스 체급을 종합 {int(sim_pct)}% 재현하는 {val_note} 대체 자원"

def find_similar_players(
    target_player_id: str,
    algorithm: str = "hybrid", # "hybrid", "sequential", "cosine", "euclidean"
    hybrid_balance: float = 0.5, # 0.0 (100% Volume/Euclidean) to 1.0 (100% Style/Cosine)
    sequential_cutoff: float = 80.0, # 1st stage style cutoff %
    position_match: str = "group", # "strict", "group", "all"
    max_age: Optional[int] = None,
    max_market_value: Optional[float] = None,
    league_tier: Optional[int] = None,
    leagues: Optional[List[str]] = None,
    limit: int = 15,
    custom_weights: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Executes player scouting similarity search based on target player profile.
    """
    all_players = get_all_player_feature_vectors()
    player_dict = {p["id"]: p for p in all_players}

    if target_player_id not in player_dict:
        return {"error": f"Target player with ID '{target_player_id}' not found.", "results": []}

    target = player_dict[target_player_id]
    vectors, _, _ = calculate_normalized_vectors(all_players, custom_weights)
    target_vec = vectors[target_player_id]

    # Candidate filtering
    candidates = []
    for p in all_players:
        if p["id"] == target_player_id:
            continue

        # Position filtering
        if position_match == "strict":
            if p["primary_pos"] != target["primary_pos"] and p["secondary_pos"] != target["primary_pos"]:
                continue
        elif position_match == "group":
            target_group = target["pos_group"]
            if p["pos_group"] != target_group:
                # Also check cross-group versatility (e.g. AM in MF vs W in FW)
                if not (target["primary_pos"] in ["AM", "W"] and p["primary_pos"] in ["AM", "W"]):
                    continue

        # Age filter
        if max_age is not None and p["age"] > max_age:
            continue

        # Market value filter
        if max_market_value is not None and p["market_value_eur"] > max_market_value:
            continue

        # League tier filter
        if league_tier is not None and p["league_tier"] != league_tier:
            continue

        # Specific league filter
        if leagues and len(leagues) > 0 and p["league"] not in leagues:
            continue

        cand_vec = vectors[p["id"]]

        # Calculate both similarity dimensions
        cos_sim = compute_cosine_similarity(target_vec, cand_vec)
        euc_sim, raw_dist = compute_euclidean_similarity(target_vec, cand_vec)

        algo_lower = algorithm.lower()
        if algo_lower == "hybrid":
            # Weighted Ensemble Hybrid
            w_cos = float(np.clip(hybrid_balance, 0.0, 1.0))
            w_euc = 1.0 - w_cos
            sim_pct = round((w_cos * cos_sim) + (w_euc * euc_sim), 2)
            metric_label = f"하이브리드 앙상블 (스타일 {int(w_cos*100)}% + 체급 {int(w_euc*100)}%)"
            metric_val = sim_pct
        elif algo_lower == "sequential":
            # 2-Stage Sequential: Must pass Cosine style threshold first
            if cos_sim < sequential_cutoff:
                continue
            sim_pct = round((0.4 * cos_sim) + (0.6 * euc_sim), 2)
            metric_label = f"2단계 순차 스카우팅 (스타일 {cos_sim}% 통과 → 체급 {euc_sim}%)"
            metric_val = sim_pct
        elif algo_lower == "euclidean":
            sim_pct = euc_sim
            metric_label = "유클리드 거리 (절대 볼륨)"
            metric_val = raw_dist
        else: # cosine default
            sim_pct = cos_sim
            metric_label = "코사인 유사도 (스타일 비율)"
            metric_val = round(cos_sim / 100.0, 4)

        # Tactical diff breakdown against target
        stat_diff = {
            "key_passes": round(p["key_passes"] - target["key_passes"], 2),
            "progressive_passes": round(p["progressive_passes"] - target["progressive_passes"], 2),
            "pass_completion_pct": round(p["pass_completion_pct"] - target["pass_completion_pct"], 1),
            "shots": round(p["shots"] - target["shots"], 2),
            "box_shots": round(p["box_shots"] - target["box_shots"], 2),
            "dribbles_completed": round(p["dribbles_completed"] - target["dribbles_completed"], 2),
            "tackles_won": round(p["tackles_won"] - target["tackles_won"], 2),
            "interceptions": round(p["interceptions"] - target["interceptions"], 2),
            "ground_duels_won": round(p["ground_duels_won"] - target["ground_duels_won"], 2),
            "aerial_won_pct": round(p["aerial_won_pct"] - target["aerial_won_pct"], 1)
        }

        # Value-for-Money Gem Index calculation
        value_score = 0.0
        if p["market_value_eur"] > 0:
            value_ratio = min(1.0, (target["market_value_eur"] + 10) / (p["market_value_eur"] + 10))
            age_bonus = max(0, (26 - p["age"]) * 2.0)
            value_score = round(sim_pct * 0.7 + value_ratio * 20.0 + age_bonus, 1)

        ai_briefing = generate_ai_scout_briefing(target, p, sim_pct, cos_sim, euc_sim, stat_diff)

        candidates.append({
            "player": p,
            "similarity_pct": sim_pct,
            "cosine_pct": cos_sim,
            "euclidean_pct": euc_sim,
            "euclidean_dist": raw_dist,
            "metric_type": metric_label,
            "metric_raw": metric_val,
            "gem_score": value_score,
            "stat_diff": stat_diff,
            "ai_briefing": ai_briefing
        })

    # Sort results by similarity percentage descending
    candidates.sort(key=lambda x: x["similarity_pct"], reverse=True)

    return {
        "target_player": target,
        "algorithm": algorithm,
        "hybrid_balance": hybrid_balance,
        "sequential_cutoff": sequential_cutoff,
        "total_matches": len(candidates),
        "results": candidates[:limit]
    }

def compare_two_players(player_a_id: str, player_b_id: str) -> Dict[str, Any]:
    """Generates direct head-to-head tactical comparison between two players."""
    all_players = get_all_player_feature_vectors()
    player_dict = {p["id"]: p for p in all_players}

    if player_a_id not in player_dict or player_b_id not in player_dict:
        return {"error": "One or both players not found."}

    pa = player_dict[player_a_id]
    pb = player_dict[player_b_id]

    vectors, _, _ = calculate_normalized_vectors(all_players)
    vec_a = vectors[player_a_id]
    vec_b = vectors[player_b_id]

    dim = len(TACTICAL_FEATURE_KEYS)
    max_possible_dist = math.sqrt(dim * (100.0 ** 2))

    cos_sim = compute_cosine_similarity(vec_a, vec_b)
    euc_sim, euc_dist = compute_euclidean_similarity(vec_a, vec_b, max_possible_dist)

    radar_comparison = [
        {"metric": "창의성 (Vision)", "playerA": pa["vision_score"], "playerB": pb["vision_score"], "gradeA": pa["vision_grade"], "gradeB": pb["vision_grade"]},
        {"metric": "슈팅 (Striking)", "playerA": pa["striking_score"], "playerB": pb["striking_score"], "gradeA": pa["striking_grade"], "gradeB": pb["striking_grade"]},
        {"metric": "드리블 (Dribble)", "playerA": pa["dribble_score"], "playerB": pb["dribble_score"], "gradeA": pa["dribble_grade"], "gradeB": pb["dribble_grade"]},
        {"metric": "수비력 (Defense)", "playerA": pa["defense_score"], "playerB": pb["defense_score"], "gradeA": pa["defense_grade"], "gradeB": pb["defense_grade"]},
        {"metric": "경합력 (Physical)", "playerA": pa["physical_score"], "playerB": pb["physical_score"], "gradeA": pa["physical_grade"], "gradeB": pb["physical_grade"]},
    ]

    detailed_stats = [
        {"name": "Key Passes / 90", "a": pa["key_passes"], "b": pb["key_passes"], "unit": ""},
        {"name": "Progressive Passes / 90", "a": pa["progressive_passes"], "b": pb["progressive_passes"], "unit": ""},
        {"name": "Pass Completion %", "a": pa["pass_completion_pct"], "b": pb["pass_completion_pct"], "unit": "%"},
        {"name": "Shots / 90", "a": pa["shots"], "b": pb["shots"], "unit": ""},
        {"name": "Expected Goals (xG) / 90", "a": pa["xg"], "b": pb["xg"], "unit": ""},
        {"name": "Dribbles Completed / 90", "a": pa["dribbles_completed"], "b": pb["dribbles_completed"], "unit": ""},
        {"name": "Carrying Distance (Prog m)", "a": pa["carrying_dist_prog"], "b": pb["carrying_dist_prog"], "unit": "m"},
        {"name": "Tackles Won / 90", "a": pa["tackles_won"], "b": pb["tackles_won"], "unit": ""},
        {"name": "Interceptions / 90", "a": pa["interceptions"], "b": pb["interceptions"], "unit": ""},
        {"name": "Aerial Won %", "a": pa["aerial_won_pct"], "b": pb["aerial_won_pct"], "unit": "%"},
        {"name": "Ground Duels Won / 90", "a": pa["ground_duels_won"], "b": pb["ground_duels_won"], "unit": ""},
    ]

    return {
        "player_a": pa,
        "player_b": pb,
        "cosine_similarity": cos_sim,
        "euclidean_similarity": euc_sim,
        "euclidean_distance": euc_dist,
        "radar_data": radar_comparison,
        "detailed_stats": detailed_stats
    }
