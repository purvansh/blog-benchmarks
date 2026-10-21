#!/usr/bin/env bash
# Measure each watcher by the delta in the user's TOTAL inotify watch count,
# summed across every process, before and after it starts. Per process fdinfo
# undercounts Node's recursive watcher, so the system wide figure is the one
# that matches what the kernel is actually charging the uid for.
cd "$(dirname "$0")"
TREE=${TREE:-.}
total() { python3 -I count_watches.py "$TREE" | tail -1 | grep -oE '[0-9,]+$' | tr -d ,; }
one() {
  local name="$1"; shift
  local base after rss
  base=$(total)
  "$@" >/dev/null 2>&1 &
  local pid=$!
  timeout 12 cat </dev/zero >/dev/null 2>&1
  after=$(total)
  rss=$(grep VmRSS /proc/$pid/status 2>/dev/null | awk '{print $2}')
  kill -9 $pid 2>/dev/null
  timeout 3 cat </dev/zero >/dev/null 2>&1
  printf "%-24s watches %7s   rss %8s KB   (baseline %s, after %s)\n" \
    "$name" "$((after - base))" "${rss:-died}" "$base" "$after"
}
echo "tree: 5,006 directories, 46,197 files, dirs+files = 51,203"
echo "ceiling: $(cat /proc/sys/fs/inotify/max_user_watches)"
echo
one "raw inotify, 1 per dir" python3 -I raw_inotify.py "$TREE"
one "@parcel/watcher"        node parcelw.js "$TREE"
one "chokidar 3.6.0"         node chok.js "$TREE"
one "node fs.watch -r"       node nodewatch.js "$TREE"
