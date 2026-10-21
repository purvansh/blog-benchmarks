# The same 100,000 rows, written two ways: in one transaction, and in 5,000
# separate transactions of 20 rows. The durability settings cost nothing in
# the first case and everything in the second, because the unit they are
# charged per is the commit, not the row.
import os, sqlite3, time

N, BATCH = 100_000, 20
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
]

def clean():
    for suf in ("", "-wal", "-shm", "-journal"):
        try: os.unlink(DB + suf)
        except FileNotFoundError: pass

def run(pragmas, many):
    clean()
    c = sqlite3.connect(DB)
    for p in pragmas: c.execute(f"pragma {p};")
    c.execute("create table t (id integer primary key, usr text not null, amt real not null);")
    t0 = time.perf_counter()
    if many:
        for i in range(0, N, BATCH):
            c.execute("begin")
            c.executemany("insert into t values (?,?,?)", rows[i:i+BATCH])
            c.execute("commit")
    else:
        c.execute("begin"); c.executemany("insert into t values (?,?,?)", rows); c.execute("commit")
    el = time.perf_counter() - t0
    c.close()
    return el

print(f"sqlite {sqlite3.sqlite_version}, {N:,} rows, /tmp on NVMe, best of 5\n")
print(f"{'configuration':28s} {'1 txn':>9s} {'5,000 txns':>12s} {'commits/sec':>13s} {'ratio':>7s}")
for name, pragmas in CONFIGS:
    one = min(run(pragmas, False) for _ in range(5))
    many = min(run(pragmas, True) for _ in range(5))
    print(f"{name:28s} {one:8.2f}s {many:11.2f}s {N/BATCH/many:13,.0f} {many/one:6.1f}x")
clean()
