# What SQLite's durability settings actually cost, on one disk, same rows.
#
# Every configuration inserts the identical 100,000 rows inside a single
# transaction, so the thing being measured is the journal and fsync behaviour
# rather than transaction overhead. Each run starts from a deleted database.
import os, sqlite3, time, sys

N = 100_000
DB = "/tmp/sqlite-rig/bench.db"
os.makedirs("/tmp/sqlite-rig", exist_ok=True)
rows = [(i, f"user-{i%9973}", i * 1.5) for i in range(N)]

CONFIGS = [
    ("defaults (delete + FULL)",   ["journal_mode=delete", "synchronous=FULL"]),
    ("delete + NORMAL",            ["journal_mode=delete", "synchronous=NORMAL"]),
    ("WAL + FULL",                 ["journal_mode=WAL", "synchronous=FULL"]),
    ("WAL + NORMAL",               ["journal_mode=WAL", "synchronous=NORMAL"]),
    ("WAL + OFF",                  ["journal_mode=WAL", "synchronous=OFF"]),
    ("MEMORY journal + NORMAL",    ["journal_mode=MEMORY", "synchronous=NORMAL"]),
    ("journal OFF + OFF",          ["journal_mode=OFF", "synchronous=OFF"]),
    ("WAL + NORMAL, 16 KiB pages", ["page_size=16384", "journal_mode=WAL", "synchronous=NORMAL"]),
]

def clean():
    for suf in ("", "-wal", "-shm", "-journal"):
        try: os.unlink(DB + suf)
        except FileNotFoundError: pass

print(f"sqlite {sqlite3.sqlite_version}, {N:,} rows per run, one transaction, /tmp on NVMe\n")
print(f"{'configuration':30s} {'wall':>8s} {'rows/sec':>11s} {'db size':>10s}")
for name, pragmas in CONFIGS:
    best = None
    for _ in range(3):
        clean()
        c = sqlite3.connect(DB)
        for p in pragmas: c.execute(f"pragma {p};")
        c.execute("create table t (id integer primary key, usr text not null, amt real not null);")
        t0 = time.perf_counter()
        c.execute("begin")
        c.executemany("insert into t values (?,?,?)", rows)
        c.execute("commit")
        c.close()
        el = time.perf_counter() - t0
        best = el if best is None else min(best, el)
    size = sum(os.path.getsize(DB + s) for s in ("", "-wal") if os.path.exists(DB + s))
    print(f"{name:30s} {best:7.2f}s {N/best:11,.0f} {size/1e6:9.1f} MB")
clean()
