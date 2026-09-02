import io
import sys
import json
import urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

res = json.loads(urllib.request.urlopen('http://127.0.0.1:8000/api/players?limit=500').read().decode('utf-8'))
print(f"Total Players Loaded in Live App: {res['count']}")
for p in res['players'][:12]:
    print(f"  - {p['name']} ({p.get('korean_name')}) | {p['club']} | {p['primary_pos']} | €{p['market_value_eur']}M")

# Test searching various Korean names
for name in ["손흥민", "이강인", "김민재", "황희찬", "음바페", "하베르츠", "비르츠", "메시"]:
    q = urllib.parse.quote(name)
    r = json.loads(urllib.request.urlopen(f'http://127.0.0.1:8000/api/players?q={q}').read().decode('utf-8'))
    matched = [f"{x['name']}({x.get('korean_name')})" for x in r['players']]
    print(f"Search '{name}' -> Matched {len(r['players'])}: {', '.join(matched)}")
