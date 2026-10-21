# Eight HTTP clients against a server that never answers

Two deliberately broken servers and eight HTTP clients at their default
settings, timing how long each waits before giving up.

- `:8099` accepts the connection, reads the request, and never sends a byte.
- `:8100` sends a complete, valid set of response headers including a
  `Content-Length`, then stalls before any body.

Both hold the socket open rather than closing it. A close is an event the client
can see, and that case already works.

## Run

```bash
python3 server.py &            # both ports
./runall.sh http://127.0.0.1:8099/ A      # 420 s ceiling
./runall.sh http://127.0.0.1:8100/ B
./runlong.sh                   # the six that outlasted 420 s, given 960 s
./runB.sh                      # scenario B at 960 s
```

## Results

No timeout argument anywhere. "Still waiting" means the harness killed it.

| client | silent server | headers then stall |
|---|---|---|
| Node 22 global fetch | 300.9 s, HeadersTimeoutError | 300.9 s, BodyTimeoutError |
| Bun 1.3.14 fetch | 300.1 s, DOMException code 23 | 300.1 s |
| curl 7.81.0 | still waiting at 960 s | still waiting at 960 s |
| GNU Wget 1.21.2 | still waiting at 960 s | still waiting at 960 s |
| Python requests 2.34.2 | still waiting at 960 s | still waiting at 960 s |
| Python urllib | still waiting at 960 s | still waiting at 420 s |
| Node 22 http.get | still waiting at 960 s | still waiting at 420 s |
| node-fetch 3 | still waiting at 960 s | still waiting at 420 s |

Sending valid headers changed nothing for any client.

## wget is the interesting one

Its manual says "The only timeout enabled by default is a 900-second read
timeout", and `--tries` defaults to 20. The timeout does fire. wget's response
is to open a fresh connection and try again:

```
$ wget --read-timeout=5 --tries=3 -O- http://127.0.0.1:8099/
HTTP request sent, awaiting response... Read error (Connection timed out) in headers.
Retrying.

--2026-10-21 15:01:29--  (try: 2)  http://127.0.0.1:8099/
Connecting to 127.0.0.1:8099... connected.
HTTP request sent, awaiting response... Read error (Connection timed out) in headers.
Retrying.
```

So the documented 900 second bound is on one attempt. Twenty attempts is five
hours.
