import orjson
with open("data.json","rb") as f: d = orjson.loads(f.read())
print(round(sum(r["amount"] for r in d), 2))
