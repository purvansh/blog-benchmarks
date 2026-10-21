#!/usr/bin/env bash
# Scenario B at 960s: does wget's documented 900 second read timeout fire once
# the response headers have actually arrived?
URL="http://127.0.0.1:8100/"; CAP=960
run() { local n="$1"; shift
  ( t0=$(date +%s.%N); timeout -s KILL $CAP "$@" > "outB.$n" 2>&1; rc=$?
    t1=$(date +%s.%N); msg=$(tr '\n' ' ' < "outB.$n" | cut -c1-70)
    [ $rc -eq 137 ] && msg="STILL WAITING at ${CAP}s"
    printf "%-18s %7.1fs rc=%-4s %s\n" "$n" "$(echo "$t1-$t0"|bc -l)" "$rc" "$msg" >> results.B960 ) & }
: > results.B960
run wget            wget -qO- "$URL"
run curl            curl -sS "$URL"
run python-requests python3 c_requests.py "$URL"
wait
sort -k2 -n results.B960
