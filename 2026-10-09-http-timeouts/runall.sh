#!/usr/bin/env bash
# Every client, same URL, all at once. 420 second ceiling: anything that hits
# it is reported as "still waiting", because that is the honest result.
URL="$1"; TAG="$2"; CAP=420
run() {
  local name="$1"; shift
  ( local t0 t1 out rc
    t0=$(date +%s.%N)
    out=$(timeout -s KILL $CAP "$@" 2>&1 | tr '\n' ' ' | cut -c1-90); rc=$?
    t1=$(date +%s.%N)
    if [ $rc -eq 137 ]; then out="STILL WAITING at ${CAP}s (killed)"; fi
    printf "%-14s %8.1fs  rc=%-3s %s\n" "$name" "$(echo "$t1-$t0"|bc -l)" "$rc" "$out" >> "results.$TAG"
  ) &
}
: > "results.$TAG"
run curl         curl -sS "$URL"
run wget         wget -qO- "$URL"
run python-urllib python3 -I c_urllib.py "$URL"
run python-requests python3 c_requests.py "$URL"
run node-fetch-global node c_fetch.mjs "$URL"
run node-http    node c_http.js "$URL"
run node-fetch-pkg node c_nodefetch.mjs "$URL"
run bun-fetch    bun c_fetch.mjs "$URL"
wait
sort -k2 -n "results.$TAG"
