# One CSV per id scheme, same 1,000,000 payload rows, only the key differs.
# Keys are generated here so the database is never timed on generating them.
import csv, os, random, secrets, time, uuid

N = 1_000_000
random.seed(8)
PAYLOAD = [(f"user-{random.randint(1,99999)}", round(random.uniform(0,500),2)) for _ in range(N)]

B32 = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"          # Crockford, as ULID uses
NANO = "_-0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def ulid(ms, rnd):
    out = []
    v = ms
    for _ in range(10):
        out.append(B32[v & 31]); v >>= 5
    t = "".join(reversed(out))
    r = "".join(B32[x & 31] for x in rnd)
    return t + r

def uuid7(ms, rnd):
    # unix_ts_ms | ver 7 | rand_a | var | rand_b   (RFC 9562 layout)
    b = bytearray(16)
    b[0:6] = ms.to_bytes(6, "big")
    b[6] = 0x70 | (rnd[0] & 0x0F)
    b[7] = rnd[1]
    b[8] = 0x80 | (rnd[2] & 0x3F)
    b[9:16] = bytes(rnd[3:10])
    return str(uuid.UUID(bytes=bytes(b)))

base_ms = int(time.time() * 1000)
EPOCH = 1735689600000      # 2025-01-01, a snowflake epoch

def write(name, keys):
    with open(f"{name}.csv", "w", newline="") as f:
        w = csv.writer(f)
        for k, (u, a) in zip(keys, PAYLOAD):
            w.writerow([k, u, a])
    print(f"{name:12s} {os.path.getsize(name+'.csv')/1e6:7.1f} MB  e.g. {keys[0]}")

write("seq",      [i+1 for i in range(N)])
write("uuid4",    [str(uuid.uuid4()) for _ in range(N)])
write("uuid4text",[str(uuid.uuid4()) for _ in range(N)])
write("uuid7",    [uuid7(base_ms + i//1000, [secrets.randbits(8) for _ in range(10)]) for i in range(N)])
write("ulid",     [ulid(base_ms + i//1000, [secrets.randbits(8) for _ in range(16)]) for i in range(N)])
write("nanoid",   ["".join(NANO[secrets.randbits(6)] for _ in range(21)) for _ in range(N)])
write("snowflake",[((base_ms - EPOCH + i//1000) << 22) | (7 << 12) | (i % 4096) for i in range(N)])
