import json
import urllib.request
import time
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_api():
    print("Testing FastAPI server and all endpoints...")
    base_url = "http://127.0.0.1:8000"
    
    # 1. Health check
    req = urllib.request.urlopen(f"{base_url}/api/health")
    data = json.loads(req.read().decode('utf-8'))
    print("1. Health check:", data)
    assert data["status"] == "ok"

    # 2. Players list
    req = urllib.request.urlopen(f"{base_url}/api/players?limit=10")
    data = json.loads(req.read().decode('utf-8'))
    print(f"2. Players count: {len(data['players'])}")
    assert len(data["players"]) > 0

    # 3. Single player details
    req = urllib.request.urlopen(f"{base_url}/api/players/p_odegaard")
    data = json.loads(req.read().decode('utf-8'))
    print(f"3. Player p_odegaard: {data['player']['name']} | Overall Grade: {data['player']['overall_grade']}")
    assert "M. Ødegaard" in data["player"]["name"]
    assert len(data["radar_data"]) == 5

    # 4. Scout similar players (Cosine)
    req_body = json.dumps({
        "target_player_id": "p_odegaard",
        "algorithm": "cosine",
        "position_match": "group",
        "limit": 5
    }).encode('utf-8')
    req = urllib.request.Request(f"{base_url}/api/scout/similar", data=req_body, headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read().decode('utf-8'))
    print(f"4. Scout similar matches for Odegaard (Cosine): {len(data['results'])}")
    for r in data["results"][:3]:
        print(f"   - {r['player']['name']} ({r['player']['club']}): {r['similarity_pct']}% match | Gem Score: {r['gem_score']}")

    # 5. Scout similar players (Euclidean)
    req_body = json.dumps({
        "target_player_id": "p_odegaard",
        "algorithm": "euclidean",
        "position_match": "group",
        "limit": 5
    }).encode('utf-8')
    req = urllib.request.Request(f"{base_url}/api/scout/similar", data=req_body, headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read().decode('utf-8'))
    print(f"5. Euclidean distance matches for Odegaard: {len(data['results'])}")

    # 6. Compare two players
    req_body = json.dumps({
        "player_a_id": "p_odegaard",
        "player_b_id": "p_stengs"
    }).encode('utf-8')
    req = urllib.request.Request(f"{base_url}/api/scout/compare", data=req_body, headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read().decode('utf-8'))
    print(f"6. Compare Odegaard vs Stengs Cosine: {data['cosine_similarity']}% | Euclidean: {data['euclidean_similarity']}%")

    # 7. Archetypes
    req = urllib.request.urlopen(f"{base_url}/api/archetypes")
    data = json.loads(req.read().decode('utf-8'))
    print(f"7. Archetypes count: {len(data['archetypes'])}")

    # 8. Legal info
    req = urllib.request.urlopen(f"{base_url}/api/legal")
    data = json.loads(req.read().decode('utf-8'))
    print(f"8. Legal licenses count: {len(data['licenses'])}")
    print(f"   Attribution: {data['wyscout_attribution']}")

    print("\n✅ All 8 API Endpoints & Integration Tests Passed Successfully!")

if __name__ == "__main__":
    test_api()
