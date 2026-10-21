# Same uuid v7 layout, three different insert rates, to isolate what the
# random tail costs. rate = ids generated inside one millisecond.
import csv, os, random, secrets, uuid, time
N = 1_000_000
random.seed(8)
PAYLOAD = [(f"user-{random.randint(1,99999)}", round(random.uniform(0,500),2)) for _ in range(N)]
base_ms = int(time.time()*1000)

def v7(ms, tail):
    b = bytearray(16)
    b[0:6] = ms.to_bytes(6,"big")
    b[6] = 0x70 | (tail[0] & 0x0F); b[7] = tail[1]
    b[8] = 0x80 | (tail[2] & 0x3F); b[9:16] = bytes(tail[3:10])
    return str(uuid.UUID(bytes=bytes(b)))

def write(name, keys):
    with open(f"{name}.csv","w",newline="") as f:
        w = csv.writer(f)
        for k,(u,a) in zip(keys,PAYLOAD): w.writerow([k,u,a])
    print(f"{name:12s} {os.path.getsize(name+'.csv')/1e6:6.1f} MB  first {keys[0]}  last {keys[-1]}")

# strictly monotonic: counter in the tail, no randomness at all
write("uuid7mono", [v7(base_ms + i//1000, list((i % 1000).to_bytes(10,"big"))) for i in range(N)])
# 10 ids per millisecond, which is a busy but ordinary service
write("uuid7slow", [v7(base_ms + i//10, [secrets.randbits(8) for _ in range(10)]) for i in range(N)])
