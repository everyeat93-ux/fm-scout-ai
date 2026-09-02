import urllib.request
import json
import re

url = "https://fm-scout-ai.onrender.com"
html = urllib.request.urlopen(url + "/").read().decode("utf-8")
print("HTML Title:", re.findall(r"<title>(.*?)</title>", html))
scripts = re.findall(r'src=["\'](.*?)["\']', html)
print("Scripts found in HTML:", scripts)

for s in scripts:
    res = urllib.request.urlopen(url + s)
    content = res.read()
    print(f"  Asset {s} -> HTTP {res.getcode()}, Size: {len(content)} bytes")

# Test API players
api_res = urllib.request.urlopen(url + "/api/players?limit=10")
data = json.loads(api_res.read().decode("utf-8"))
print(f"API /api/players test -> count: {data['count']}, players: {len(data['players'])}")
