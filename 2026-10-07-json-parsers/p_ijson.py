import ijson
t = 0.0
with open("data.json","rb") as f:
    for v in ijson.items(f, "item.amount"): t += float(v)
print(round(t,2))
