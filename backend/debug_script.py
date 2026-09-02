import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from database import get_db_connection
from similarity_engine import get_all_player_feature_vectors, find_similar_players, compare_two_players

conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT id, name FROM players")
rows = cursor.fetchall()
print(f"Total players in DB: {len(rows)}")
for r in rows:
    print(r['id'], "->", r['name'])

all_p = get_all_player_feature_vectors()
print(f"Total feature vectors fetched: {len(all_p)}")

res = find_similar_players('p_odegaard', algorithm='cosine')
print("\nScouting Result for Odegaard:")
print(res)
