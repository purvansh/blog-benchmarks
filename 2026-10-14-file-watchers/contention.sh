#!/usr/bin/env bash
# Two watchers, one kernel budget. The question is what the second one does
# when the first has already taken most of it.
cd "$(dirname "$0")"
TREE=${TREE:-.}
echo "baseline watches in use: $(python3 -I count_watches.py $TREE | tail -1 | grep -oE '[0-9,]+$')"
echo
echo "=== A: chokidar alone ==="
timeout 40 node chok.js "$TREE" 2>&1 | head -3
echo "(exit $? -- 124 means it was still running happily at 40s)"
echo
echo "=== B: node fs.watch first, then chokidar ==="
node nodewatch.js "$TREE" >/dev/null 2>&1 &
first=$!
timeout 8 cat </dev/zero >/dev/null 2>&1
echo "after first watcher: $(python3 -I count_watches.py $TREE | tail -1 | grep -oE '[0-9,]+$') watches in use"
timeout 40 node chok.js "$TREE" 2>&1 | head -3
echo "(exit $?)"
kill -9 $first 2>/dev/null
