# What an HNSW parameter actually buys, measured against exact search.
#
# 100,000 vectors at 384 dimensions, the shape a small RAG index really has.
# The vectors are clustered rather than uniform random: 200 centroids with
# noise around them. Uniform random vectors are a worst case for any ANN index
# and would understate recall for every configuration at once.
import json, os, tempfile, time
import numpy as np, faiss

N, DIM, NQ, K, NCLUST = 100_000, 384, 500, 10, 200
rng = np.random.default_rng(11)
cent = rng.normal(size=(NCLUST, DIM)).astype(np.float32)
assign = rng.integers(0, NCLUST, size=N)
data = (cent[assign] + rng.normal(scale=0.35, size=(N, DIM)).astype(np.float32)).astype(np.float32)
data /= np.linalg.norm(data, axis=1, keepdims=True)
qa = rng.integers(0, NCLUST, size=NQ)
q = (cent[qa] + rng.normal(scale=0.35, size=(NQ, DIM)).astype(np.float32)).astype(np.float32)
q /= np.linalg.norm(q, axis=1, keepdims=True)

t0 = time.perf_counter()
truth = np.argsort(-(q @ data.T), axis=1)[:, :K]
exact_s = time.perf_counter() - t0
print(f"EXACT  {N} x {DIM}  brute force {exact_s:.2f}s total, "
      f"{exact_s/NQ*1000:.2f} ms/query, raw vectors {data.nbytes/1e6:.0f} MB", flush=True)

def recall(got): return float(np.mean([len(set(a) & set(b))/K for a, b in zip(got, truth)]))

rows = []
for M, efC in [(8, 100), (16, 100), (16, 200), (32, 200), (48, 200), (64, 400)]:
    ix = faiss.IndexHNSWFlat(DIM, M, faiss.METRIC_INNER_PRODUCT)
    ix.hnsw.efConstruction = efC
    faiss.omp_set_num_threads(8)
    t0 = time.perf_counter(); ix.add(data); build = time.perf_counter() - t0
    p = tempfile.mktemp(); faiss.write_index(ix, p); size = os.path.getsize(p)/1e6; os.unlink(p)
    for ef in [16, 32, 64, 128, 256]:
        ix.hnsw.efSearch = ef
        faiss.omp_set_num_threads(1)
        t0 = time.perf_counter(); _, lbl = ix.search(q, K); qs = time.perf_counter() - t0
        r = {"M": M, "efC": efC, "ef": ef, "build_s": round(build, 1), "index_mb": round(size, 1),
             "recall": round(recall(lbl), 4), "ms_per_q": round(qs/NQ*1000, 3)}
        rows.append(r); print(r, flush=True)
json.dump({"exact_ms_per_q": exact_s/NQ*1000, "raw_mb": data.nbytes/1e6, "rows": rows},
          open("/out/hnsw.json", "w"), indent=1)
