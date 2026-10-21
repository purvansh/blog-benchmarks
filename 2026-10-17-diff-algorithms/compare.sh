#!/usr/bin/env bash
# For each commit, hash the diff each algorithm produces. Commits where the
# hashes differ are the only ones where the choice of algorithm is visible.
cd "${REPO:?set REPO}"
N="${N:-800}"
differ=0; total=0
declare -A hunkdelta
: > /tmp/difflist.txt
for c in $(git log --no-merges --format=%H -"$N"); do
  m=$(git diff --diff-algorithm=myers     -U3 "$c^" "$c" 2>/dev/null)
  [ -z "$m" ] && continue
  total=$((total+1))
  hm=$(md5sum <<<"$m" | cut -d' ' -f1)
  hh=$(md5sum <<<"$(git diff --diff-algorithm=histogram -U3 "$c^" "$c" 2>/dev/null)" | cut -d' ' -f1)
  hp=$(md5sum <<<"$(git diff --diff-algorithm=patience  -U3 "$c^" "$c" 2>/dev/null)" | cut -d' ' -f1)
  hn=$(md5sum <<<"$(git diff --diff-algorithm=minimal   -U3 "$c^" "$c" 2>/dev/null)" | cut -d' ' -f1)
  if [ "$hm" != "$hh" ] || [ "$hm" != "$hp" ] || [ "$hm" != "$hn" ]; then
    differ=$((differ+1)); echo "$c" >> /tmp/difflist.txt
  fi
done
echo "commits with a non empty diff: $total"
echo "commits where the four algorithms disagree: $differ"
awk -v d=$differ -v t=$total 'BEGIN{printf "that is %.1f%%\n", (d/t)*100}'
