import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from similarity_engine import find_similar_players

print("=== 1. HYBRID ENSEMBLE (50% Style + 50% Volume) for Son Heung-min ===")
res1 = find_similar_players('p_son', algorithm='hybrid', hybrid_balance=0.5)
for r in res1['results'][:5]:
    p = r['player']
    print(f"  - {p['name']} ({p.get('korean_name')}) | {p['club']} | €{p['market_value_eur']}M -> 종합: {r['similarity_pct']}% (스타일: {r['cosine_pct']}%, 체급: {r['euclidean_pct']}%)")

print("\n=== 2. TWO-STAGE SEQUENTIAL (Cutoff 88% Style -> Rank by Volume) ===")
res2 = find_similar_players('p_son', algorithm='sequential', sequential_cutoff=88.0)
for r in res2['results'][:5]:
    p = r['player']
    print(f"  - {p['name']} ({p.get('korean_name')}) | {p['club']} | €{p['market_value_eur']}M -> 종합: {r['similarity_pct']}% (스타일: {r['cosine_pct']}%, 체급: {r['euclidean_pct']}%)")
