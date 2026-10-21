# Six HNSW settings against exact search

100,000 clustered vectors at 384 dimensions in faiss. Every index is scored
against exact inner product ground truth at five search widths.

The vectors are clustered (200 centroids plus noise) rather than uniform
random. Uniform random vectors are a worst case for any ANN index and would
understate recall for every configuration at once.

## Run

```bash
docker run --rm -v "$PWD":/w:ro -v "$PWD":/out python:3.12-slim bash -c '
  pip install -q numpy faiss-cpu
  python /w/hnsw.py'
```

## Results

Exact brute force: **2.53 ms per query**, 154 MB of vectors, recall 1.0.

| config | build | size | best recall | ms at that recall |
|---|---|---|---|---|
| M 8, efC 100 | 7.6 s | 161.7 MB | 0.9958 | 0.261 |
| M 16, efC 100 | 8.3 s | 168.0 MB | 0.9996 | 0.194 |
| M 16, efC 200 | 16.8 s | 168.0 MB | 1.0 | 0.291 |
| M 32, efC 200 | 20.2 s | 180.8 MB | 1.0 | 0.249 |
| M 48, efC 200 | 21.6 s | 193.6 MB | 1.0 | 0.286 |
| M 64, efC 400 | 55.2 s | 206.4 MB | 1.0 | 0.364 |

M 64 costs 6.6x the build time of M 16 and is 1.9x slower per query, for
0.0004 more recall. On one index (M 16, efC 100), raising ef from 16 to 128
moves recall from 0.84 to 0.9996 with no rebuild.
