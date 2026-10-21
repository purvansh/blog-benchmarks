# Does lowering synchronous really make rollback journal mode slower?
# Five alternating runs each, to rule out thermal drift and ordering effects.
import os, sqlite3, time
N, BATCH = 100_000, 20
DB = "/tmp/sqlite-rig/v.db"
os.makedirs("/tmp/sqlite-rig", exist_ok=True)
rows = [(i, f"user-{i%9973}", i*1.5) for i in range(N)]
def clean():
    for s in ("", "-wal", "-shm", "-journal"):
        try: os.unlink(DB+s)
        except FileNotFoundError: pass
def run(sync):
    clean(); c = sqlite3.connect(DB)
    c.execute("pragma journal_mode=delete;"); c.execute(f"pragma synchronous={sync};")
    c.execute("create table t (id integer primary key, usr text, amt real);")
    t0 = time.perf_counter()
    for i in range(0, N, BATCH):
        c.execute("begin"); c.executemany("insert into t values (?,?,?)", rows[i:i+BATCH]); c.execute("commit")
    el = time.perf_counter()-t0; c.close(); return el
full, norm = [], []
for i in range(5):
    full.append(run("FULL")); norm.append(run("NORMAL"))
    print(f"round {i+1}: FULL {full[-1]:6.2f}s   NORMAL {norm[-1]:6.2f}s", flush=True)
clean()
print(f"\nFULL   best {min(full):.2f}s  median {sorted(full)[2]:.2f}s  -> {N/BATCH/min(full):,.0f} commits/sec")
print(f"NORMAL best {min(norm):.2f}s  median {sorted(norm)[2]:.2f}s  -> {N/BATCH/min(norm):,.0f} commits/sec")
