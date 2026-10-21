#!/usr/bin/env bash
one() {
  local name="$1"; shift
  local m out
  out=$("$@" 2>&1 | tail -1)
  m=$(/usr/bin/time -f "%e %M" "$@" 2>&1 >/dev/null | tail -1)
  printf "%-16s %-9s peak %8s KB (%.0f MiB)  -> %s\n" "$name" "${m%% *}s" "${m##* }" "$(echo "${m##* }/1024"|bc -l)" "$out"
}
one bun          bun big_node.js
one python-json  python3 big_p_json.py
one orjson       python3 big_p_orjson.py
one ijson        python3 big_p_ijson.py
