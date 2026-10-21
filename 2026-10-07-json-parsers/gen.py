import json, random, sys
random.seed(7)
n = int(sys.argv[1])
words = ["alpha","bravo","charlie","delta","echo","foxtrot","golf","hotel"]
with open("data.json","w") as f:
    f.write("[")
    for i in range(n):
        if i: f.write(",")
        rec = {
            "id": i,
            "user": f"user-{random.randint(1,99999)}",
            "amount": round(random.uniform(0, 500), 2),
            "tags": random.sample(words, 3),
            "note": " ".join(random.choice(words) for _ in range(12)),
            "ok": random.random() > 0.3,
        }
        f.write(json.dumps(rec))
    f.write("]")
