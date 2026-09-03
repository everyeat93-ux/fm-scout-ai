"""
FM Scout AI (FC Finder) - Backend API
FastAPI REST API providing player search, similarity calculation, head-to-head comparison,
and Wyscout/StatsBomb legal compliance data.
"""
import os
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from database import get_db_connection, init_db
from similarity_engine import find_similar_players, compare_two_players, get_all_player_feature_vectors, calculate_manager_tactical_fit

app = FastAPI(
    title="FM Scout AI (FC Finder) API",
    description="Wyscout Tactical Analyst Themed Player Scouting & Similarity Calculation Service",
    version="1.0.0"
)

# Enable GZip compression for fast payload delivery
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Enable CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class SimilarPlayerRequest(BaseModel):
    target_player_id: str
    algorithm: str = "hybrid" # "hybrid", "sequential", "cosine", "euclidean"
    hybrid_balance: float = 0.5 # 0.0 (100% Euclidean) to 1.0 (100% Cosine)
    sequential_cutoff: float = 80.0 # 1st stage style cutoff %
    position_match: str = "group" # "strict", "group", "all"
    max_age: Optional[int] = None
    max_market_value: Optional[float] = None
    league_tier: Optional[int] = None
    leagues: Optional[List[str]] = None
    limit: int = 15
    custom_weights: Optional[Dict[str, float]] = None

class CompareRequest(BaseModel):
    player_a_id: str
    player_b_id: str

@app.on_event("startup")
def on_startup():
    init_db()
    try:
        from pipeline.run_real_db_build import build_100pct_real_database
        from similarity_engine import get_all_player_feature_vectors
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT count(*) FROM players WHERE id LIKE 'p_db_%'")
        fake_count = c.fetchone()[0]
        c.execute("SELECT count(*) FROM players")
        total_count = c.fetchone()[0]
        c.execute("SELECT club FROM players WHERE id = 'p_lee_kangin'")
        row = c.fetchone()
        
        # If database has fake synthetic players or is missing latest FotMob transfers, rebuild!
        if fake_count > 0 or total_count < 100 or not row or "Atl" not in str(row[0]):
            print("Synchronizing 100% authentic real player database with latest FotMob transfers...")
            build_100pct_real_database()
            get_all_player_feature_vectors(reload=True)
            print("100% Real Player Database successfully loaded!")
        conn.close()
    except Exception as e:
        print(f"Startup DB check error: {e}")

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "FM Scout AI (FC Finder)", "database": "scout_hub.sqlite"}

@app.get("/api/players")
def list_players(
    q: Optional[str] = None,
    pos: Optional[str] = None,
    pos_group: Optional[str] = None,
    league: Optional[str] = None,
    max_age: Optional[int] = None,
    max_value: Optional[float] = None,
    sort_by: str = "overall_score",
    limit: int = 100
):
    """Lists players with optional searching and filtering."""
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        p.id, p.name, p.full_name, p.korean_name, p.age, p.nationality, p.nat_code, p.club, p.league, p.league_tier,
        p.primary_pos, p.secondary_pos, p.pos_group, p.foot, p.height_cm, p.market_value_eur, p.wage_eur_pw,
        p.contract_until, p.avatar_type,
        r.vision_score, r.vision_grade,
        r.striking_score, r.striking_grade,
        r.dribble_score, r.dribble_grade,
        r.defense_score, r.defense_grade,
        r.physical_score, r.physical_grade,
        r.overall_score, r.overall_grade,
        r.tactical_role
    FROM players p
    JOIN tactical_ratings r ON p.id = r.player_id
    WHERE 1=1
    """
    params = []

    if q:
        query += " AND (p.name LIKE ? OR p.full_name LIKE ? OR p.korean_name LIKE ? OR p.club LIKE ?)"
        term = f"%{q}%"
        params.extend([term, term, term, term])

    if pos:
        query += " AND (p.primary_pos = ? OR p.secondary_pos = ?)"
        params.extend([pos, pos])

    if pos_group:
        query += " AND p.pos_group = ?"
        params.append(pos_group)

    if league:
        query += " AND p.league = ?"
        params.append(league)

    if max_age:
        query += " AND p.age <= ?"
        params.append(max_age)

    if max_value:
        query += " AND p.market_value_eur <= ?"
        params.append(max_value)

    # Sort order
    valid_sorts = {
        "overall_score": "r.overall_score DESC",
        "market_value_eur": "p.market_value_eur DESC",
        "age": "p.age ASC",
        "name": "p.name ASC",
        "vision_score": "r.vision_score DESC",
        "striking_score": "r.striking_score DESC",
        "dribble_score": "r.dribble_score DESC",
        "defense_score": "r.defense_score DESC",
        "physical_score": "r.physical_score DESC"
    }
    order_clause = valid_sorts.get(sort_by, "r.overall_score DESC")
    query += f" ORDER BY {order_clause} LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return {"players": [dict(r) for r in rows], "count": len(rows)}

@app.get("/api/players/{player_id}")
def get_player(player_id: str):
    """Returns detailed profile, factual per-90 metrics, and tactical ratings for a single player."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        p.*,
        s.*,
        r.*
    FROM players p
    JOIN player_stats_per90 s ON p.id = s.player_id
    JOIN tactical_ratings r ON p.id = r.player_id
    WHERE p.id = ?
    """, (player_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail=f"Player with ID '{player_id}' not found.")

    p_dict = dict(row)
    manager_fit = calculate_manager_tactical_fit(p_dict)
    
    # Structure radar metrics
    radar_data = [
        {"metric": "창의성 (Vision)", "score": p_dict["vision_score"], "grade": p_dict["vision_grade"], "fullMark": 100},
        {"metric": "슈팅 (Striking)", "score": p_dict["striking_score"], "grade": p_dict["striking_grade"], "fullMark": 100},
        {"metric": "드리블 (Dribble)", "score": p_dict["dribble_score"], "grade": p_dict["dribble_grade"], "fullMark": 100},
        {"metric": "수비력 (Defense)", "score": p_dict["defense_score"], "grade": p_dict["defense_grade"], "fullMark": 100},
        {"metric": "경합력 (Physical)", "score": p_dict["physical_score"], "grade": p_dict["physical_grade"], "fullMark": 100},
    ]

    return {
        "player": p_dict,
        "radar_data": radar_data,
        "manager_fit": manager_fit
    }

@app.post("/api/scout/similar")
def scout_similar_players(req: SimilarPlayerRequest):
    """Calculates tactical similarity matches based on target player ID and algorithm settings."""
    result = find_similar_players(
        target_player_id=req.target_player_id,
        algorithm=req.algorithm,
        hybrid_balance=req.hybrid_balance,
        sequential_cutoff=req.sequential_cutoff,
        position_match=req.position_match,
        max_age=req.max_age,
        max_market_value=req.max_market_value,
        league_tier=req.league_tier,
        leagues=req.leagues,
        limit=req.limit,
        custom_weights=req.custom_weights
    )
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.post("/api/scout/compare")
def compare_players_endpoint(req: CompareRequest):
    """Generates direct head-to-head tactical comparison between two players."""
    result = compare_two_players(req.player_a_id, req.player_b_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.get("/api/archetypes")
def get_archetypes():
    """Returns curated tactical presets (e.g. Deep-Lying Playmaker, Inverted Winger, Box-to-Box, etc.)."""
    presets = [
        {
            "id": "advanced_playmaker",
            "title": "Advanced Playmaker / Pocket 10",
            "description": "High creative vision, progressive passing volume, key pass creator.",
            "benchmark_player_id": "p_odegaard",
            "benchmark_name": "Martin Ødegaard",
            "pos_group": "MF",
            "primary_pillar": "Vision & Pass"
        },
        {
            "id": "box_to_box",
            "title": "Box-to-Box Engine",
            "description": "High stamina, ground duel wins, all-round carry and disruption.",
            "benchmark_player_id": "p_valverde",
            "benchmark_name": "Federico Valverde",
            "pos_group": "MF",
            "primary_pillar": "Physical & All-Round"
        },
        {
            "id": "deep_controller",
            "title": "Deep Controller / Anchor 6",
            "description": "Elite passing volume, high pass completion %, defensive screen.",
            "benchmark_player_id": "p_rodri",
            "benchmark_name": "Rodri",
            "pos_group": "MF",
            "primary_pillar": "Vision & Defense"
        },
        {
            "id": "inverted_winger",
            "title": "Inverted Goalscoring Winger",
            "description": "Explosive carries, high shots inside box, creative cut-backs.",
            "benchmark_player_id": "p_saka",
            "benchmark_name": "Bukayo Saka",
            "pos_group": "FW",
            "primary_pillar": "Dribble & Striking"
        },
        {
            "id": "lethal_poacher",
            "title": "Box Poacher / Target Forward",
            "description": "Massive xG accumulation, box presence, clinical conversion.",
            "benchmark_player_id": "p_haaland",
            "benchmark_name": "Erling Haaland",
            "pos_group": "FW",
            "primary_pillar": "Striking & xG"
        },
        {
            "id": "ball_playing_cb",
            "title": "Ball-Playing Central Defender",
            "description": "Dominant aerial presence, clean defensive actions, progressive distribution.",
            "benchmark_player_id": "p_saliba",
            "benchmark_name": "William Saliba",
            "pos_group": "DF",
            "primary_pillar": "Defense & Physical"
        }
    ]
    return {"archetypes": presets}

@app.get("/api/legal")
def get_legal_info():
    """Returns license compliance, open data attributions, and legal disclaimers."""
    return {
        "wyscout_attribution": "경기 전술 이벤트 통계는 Luca Pappalardo 등이 Nature Scientific Data(2019) 저널에 배포한 Wyscout Open Dataset(CC BY 4.0)을 기반으로 역산되었습니다.",
        "statsbomb_attribution": "Certain tactical metrics and event models are derived in accordance with the StatsBomb Open Data user guidelines.",
        "licenses": [
            {
                "dataset": "Wyscout Open Dataset (Luca Pappalardo et al.)",
                "license": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
                "doi": "10.1038/s41597-019-0247-7"
            },
            {
                "dataset": "European Soccer Database (Hugo Mathien)",
                "license": "Open Database License (ODbL)"
            },
            {
                "dataset": "European Leagues Database (Kamran Gayibov)",
                "license": "Community Data License Agreement (CDLA) - Sharing - Version 1.0"
            }
        ],
        "disclaimer": "FM Scout AI (FC Finder)는 비영리 전술 데이터 분석 시뮬레이터입니다. 본 서비스는 선수의 실제 사진(초상권 보호) 대신 국기 아이콘 및 실루엣 아바타를 사용하며, 지적재산권과 오픈 라이선스 규정을 엄격히 준수합니다."
    }

# Mount static frontend build if it exists
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
