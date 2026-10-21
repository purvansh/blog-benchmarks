#!/usr/bin/env bash
# 3 runs per parser, median wall clock, max peak RSS. Same job every time:
# sum the "amount" field over 900,000 records in one 164 MiB file.
run3() {
  local name="$1"; shift
  local times=() rss=() out=""
  for i in 1 2 3; do
    local m
    m=$(/usr/bin/time -f "%e %M" "$@" 2>&1 >/dev/null | tail -1)
    times+=("${m%% *}"); rss+=("${m##* }")
  done
  out=$("$@" 2>/dev/null | tail -1)
  local med
  med=$(printf '%s\n' "${times[@]}" | sort -n | sed -n 2p)
  local peak
  peak=$(printf '%s\n' "${rss[@]}" | sort -n | tail -1)
  printf "%-18s median %6ss   peakRSS %8s KB (%.0f MiB)   sum=%s\n" \
    "$name" "$med" "$peak" "$(echo "$peak/1024" | bc -l)" "$out"
}
run3 python-json   python3 -I p_json.py
run3 orjson        python3 p_orjson.py
run3 ijson-stream  python3 p_ijson.py
run3 node-22       node p_node.js
run3 bun           bun p_node.js
run3 jq-1.6-dom    jq 'map(.amount)|add' data.json
run3 jq-1.6-stream jq -n --stream 'reduce (inputs|select(length==2 and (.[0]|length)==2 and .[0][1]=="amount")|.[1]) as $x (0; .+$x)' data.json
