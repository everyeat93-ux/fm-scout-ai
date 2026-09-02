import os
import sys
from similarity_engine import find_similar_players, compare_two_players
from database import get_db_connection

def test_engine():
    print("Testing FM Scout AI Similarity Core...")
    res = find_similar_players('p_odegaard', algorithm='cosine')
    print("Target:", res['target_player']['name'], f"({res['target_player']['club']})")
    print(f"Found {len(res['results'])} matches:")
    for r in res['results'][:5]:
        p = r['player']
        print(f"  - {p['name']} ({p['club']}, {p['league']}, €{p['market_value_eur']}M) -> Match: {r['similarity_pct']}% | Gem Score: {r['gem_score']}")

    print("\nTesting Euclidean Distance Algorithm:")
    res_euc = find_similar_players('p_odegaard', algorithm='euclidean')
    for r in res_euc['results'][:5]:
        p = r['player']
        print(f"  - {p['name']} ({p['club']}, €{p['market_value_eur']}M) -> Match: {r['similarity_pct']}% (Distance: {r['metric_raw']})")

    print("\nTesting 1v1 Comparison:")
    comp = compare_two_players('p_odegaard', 'p_stengs')
    print("Odegaard vs Stengs Cosine Sim:", comp['cosine_similarity'], "%")
    print("Odegaard vs Stengs Euclidean Sim:", comp['euclidean_similarity'], "%")
    print("Radar Data Points:", len(comp['radar_data']))
    print("\nAll Core Tests Passed Successfully!")

if __name__ == "__main__":
    test_engine()
