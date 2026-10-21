import json
with open("data.json") as f: d = json.load(f)
print(round(sum(r["amount"] for r in d), 2))
