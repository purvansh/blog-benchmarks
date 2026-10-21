#!/usr/bin/env bash
# The six that outlasted 420s, given 960s. rc is captured from timeout itself,
# not from the end of a pipe, so 137 really means it was killed at the cap.
URL="http://127.0.0.1:8099/"; CAP=960
run() {
  local name="$1"; shift
  ( local t0 t1 rc
    t0=$(date +%s.%N)
    timeout -s KILL $CAP "$@" > "out.$name" 2>&1; rc=$?
    t1=$(date +%s.%N)
    local msg; msg=$(tr '\n' ' ' < "out.$name" | cut -c1-80)
    [ $rc -eq 137 ] && msg="STILL WAITING at ${CAP}s"
    printf "%-18s %7.1fs  rc=%-4s %s\n" "$name" "$(echo "$t1-$t0"|bc -l)" "$rc" "$msg" >> results.LONG
  ) &
}
: > results.LONG
run curl             curl -sS "$URL"
run wget             wget -qO- "$URL"
run python-urllib    python3 -I c_urllib.py "$URL"
run python-requests  python3 c_requests.py "$URL"
run node-http        node c_http.js "$URL"
run node-fetch-pkg   node c_nodefetch.mjs "$URL"
wait
sort -k2 -n results.LONG
