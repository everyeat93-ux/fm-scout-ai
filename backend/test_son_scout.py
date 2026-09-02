import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from similarity_engine import find_similar_players, compare_two_players
from main import list_players

print("1. Testing Korean Search for '손흥민':")
search_res = list_players(q="손흥민")
print(f"Found {search_res['count']} players matching '손흥민':")
for p in search_res["players"]:
    print(f"  - {p['name']} ({p['korean_name']}) | {p['club']} | {p['primary_pos']} | €{p['market_value_eur']}M")

print("\n2. Testing Scouting Matches for Son Heung-min (p_son):")
res = find_similar_players('p_son', algorithm='cosine', position_match='group')
target = res['target_player']
print(f"Target Player: {target['name']} ({target['korean_name']}) - {target['club']} ({target['tactical_role']})")
print(f"Total Matches Found: {len(res['results'])}")
for r in res['results'][:5]:
    p = r['player']
    print(f"  - {p['name']} ({p.get('korean_name')}) | {p['club']} ({p['league']}) | €{p['market_value_eur']}M -> 유사도: {r['similarity_pct']}% | 진주지수: {r['gem_score']}")

print("\n3. Testing 1v1 Compare: Son Heung-min vs Hwang Hee-chan:")
comp = compare_two_players('p_son', 'p_hwang_heechan')
print(f"Cosine Similarity: {comp['cosine_similarity']}% | Euclidean: {comp['euclidean_similarity']}%")
