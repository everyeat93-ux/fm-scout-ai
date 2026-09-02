"""
FM Scout AI (FC Finder) - Database Engine
Provides SQLite connection management and table creation for scout_hub.sqlite
"""
import os
import sqlite3
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "scout_hub.sqlite")

def get_db_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Players table (Metainfo)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        full_name TEXT,
        korean_name TEXT,
        age INTEGER NOT NULL,
        nationality TEXT NOT NULL,
        nat_code TEXT NOT NULL,
        club TEXT NOT NULL,
        league TEXT NOT NULL,
        league_tier INTEGER NOT NULL,
        primary_pos TEXT NOT NULL,
        secondary_pos TEXT,
        pos_group TEXT NOT NULL,
        foot TEXT NOT NULL,
        height_cm INTEGER,
        market_value_eur REAL NOT NULL,
        wage_eur_pw REAL NOT NULL,
        contract_until INTEGER,
        avatar_type TEXT DEFAULT 'silhouette_generic'
    );
    """)

    # Per-90 Factual Event Metrics (Wyscout / FBref 9 domains)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS player_stats_per90 (
        player_id TEXT PRIMARY KEY,
        matches_played INTEGER NOT NULL,
        minutes_played INTEGER NOT NULL,
        
        -- Passing & Playmaking (Vision)
        key_passes REAL NOT NULL,
        progressive_passes REAL NOT NULL,
        pass_completion_pct REAL NOT NULL,
        passes_attempted REAL NOT NULL,
        through_balls REAL NOT NULL,
        crosses_into_box REAL NOT NULL,
        
        -- Striking & Threat (Striking)
        shots REAL NOT NULL,
        box_shots REAL NOT NULL,
        shots_on_target_pct REAL NOT NULL,
        xg REAL NOT NULL,
        npxg REAL NOT NULL,
        goals REAL NOT NULL,
        
        -- On-ball & Carrying (Dribble)
        dribbles_completed REAL NOT NULL,
        dribble_success_pct REAL NOT NULL,
        carrying_dist_prog REAL NOT NULL,
        fouls_drawn REAL NOT NULL,
        progressive_carries REAL NOT NULL,
        
        -- Defending (Defense)
        interceptions REAL NOT NULL,
        tackles_won REAL NOT NULL,
        clearances REAL NOT NULL,
        blocks REAL NOT NULL,
        ball_recoveries REAL NOT NULL,
        
        -- Physical & Duels (Physical)
        aerial_won_pct REAL NOT NULL,
        ground_duels_won REAL NOT NULL,
        aerial_duels_won REAL NOT NULL,
        pressures REAL NOT NULL,
        
        FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE
    );
    """)

    # Normalized 0-100 Tactical Ratings and Custom Tiers (F to SSS)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tactical_ratings (
        player_id TEXT PRIMARY KEY,
        
        -- 5 Core Tactical Pillars (0 - 100 Score)
        vision_score REAL NOT NULL,
        vision_grade TEXT NOT NULL,
        
        striking_score REAL NOT NULL,
        striking_grade TEXT NOT NULL,
        
        dribble_score REAL NOT NULL,
        dribble_grade TEXT NOT NULL,
        
        defense_score REAL NOT NULL,
        defense_grade TEXT NOT NULL,
        
        physical_score REAL NOT NULL,
        physical_grade TEXT NOT NULL,
        
        -- Overall Tactical Index
        overall_score REAL NOT NULL,
        overall_grade TEXT NOT NULL,
        
        -- Tactical Archetype
        tactical_role TEXT NOT NULL,
        
        FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE
    );
    """)

    # Leagues metadata
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leagues (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        country TEXT NOT NULL,
        country_code TEXT NOT NULL,
        tier INTEGER NOT NULL,
        reputation INTEGER NOT NULL
    );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_PATH)
