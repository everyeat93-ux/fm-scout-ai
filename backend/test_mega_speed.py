import time
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from similarity_engine import find_similar_players

t0 = time.time()
res = find_similar_players('p_son', algorithm='hybrid', hybrid_balance=0.5, limit=10)
t1 = time.time()

print(f"Scouted {res['total_matches']} valid candidate players in {(t1-t0)*1000:.1f}ms!")
print("\nTop 10 Hybrid Scouting Doppelgangers for Son Heung-min (손흥민):")
for i, r in enumerate(res['results']):
    p = r['player']
    print(f" #{i+1:02d} {p['name']} ({p.get('korean_name')}) | {p['club']} ({p['league']}) | €{p['market_value_eur']}M | 종합:{r['similarity_pct']}% (스타일:{r['cosine_pct']}%, 체급:{r['euclidean_pct']}%) | Gem:{r['gem_score']}")
