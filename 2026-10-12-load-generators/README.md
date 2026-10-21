# Load generators against a stop-the-world server

`app.py` takes a global lock for one second out of every ten. Every handler
acquires that lock, so during that second everything in flight blocks and
everything arriving queues. That is the shape of a GC pause.

## Run

```bash
python3 app.py &
ab -c 10 -t 30 -n 500000 -q http://127.0.0.1:8111/
npx autocannon -c 10 -d 30 -j http://127.0.0.1:8111/
docker run --rm --network host -i peterevans/vegeta sh -c \
  "echo 'GET http://127.0.0.1:8111/' | vegeta attack -rate=400 -duration=30s | vegeta report"
docker run --rm --network host -v "$PWD":/w:ro grafana/k6 run \
  --summary-trend-stats "avg,p(50),p(90),p(95),p(99),max" /w/k6.js
```

## Results

| tool | model | p50 | p99 | max |
|---|---|---|---|---|
| ApacheBench | closed loop | 1 ms | **3 ms** | 2,296 ms |
| autocannon | closed loop | 41 ms | 43 ms | 1,036 ms |
| k6 constant-arrival-rate | open loop | 0.23 ms | **906 ms** | 1,000 ms |
| vegeta | open loop | 41 ms | **907 ms** | 1,043 ms |

Same server, same stalls. The reported p99 differs by 302x depending on
whether the generator keeps sending during the pause.

k6 also reported 268 dropped iterations, meaning it could not start that many
on schedule. A closed-loop tool has no way to produce that signal.

autocannon's flat 41 ms floor is the classic delayed-ACK signature and is a
property of this client/server pair, not of the stall.
