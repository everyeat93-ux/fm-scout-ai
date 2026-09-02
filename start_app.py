"""
FM Scout AI (FC Finder) - Single Launcher Script
Runs the FastAPI server serving both the REST API and the built React Dashboard on http://localhost:8000
"""
import os
import sys
import webbrowser

# Add backend directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from pipeline.build_db import build_database
from database import DB_PATH

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        print("Scout database not found. Building scout_hub.sqlite...")
        build_database()

    print("=" * 65)
    print(" ⚽ FM Scout AI (FC Finder) - Wyscout Tactical Analyst Dashboard")
    print("=" * 65)
    print(" Server running at: http://localhost:8000")
    print(" API Documentation: http://localhost:8000/docs")
    print(" Zero-cost static architecture with SQLite & client-side Canvas")
    print("=" * 65)

    import uvicorn
    # Open default browser automatically
    try:
        webbrowser.open("http://localhost:8000")
    except Exception:
        pass

    uvicorn.run("main:app", app_dir=os.path.join(os.path.dirname(__file__), "backend"), host="0.0.0.0", port=8000, reload=True)
