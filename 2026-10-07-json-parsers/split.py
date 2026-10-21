# Separate the parse from the walk. Same file, same two phases, timed apart.
import json, orjson, time, resource, sys
which = sys.argv[1]
raw = open("data.json","rb").read()
t0 = time.perf_counter()
d = orjson.loads(raw) if which == "orjson" else json.loads(raw.decode())
t1 = time.perf_counter()
t = 0.0
for r in d: t += r["amount"]
t2 = time.perf_counter()
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
print(f"{which:12s} parse {t1-t0:5.2f}s   walk {t2-t1:5.2f}s   peak {peak:7.0f} MiB   sum {t:.2f}")
