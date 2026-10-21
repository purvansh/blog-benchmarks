#!/usr/bin/env bash
# Four diff algorithms over the same real commits. The question is not speed,
# it is how much of a change each one claims happened: hunks a reviewer must
# read, and lines it says were added or removed.
cd "${REPO:-.}"
commits=$(git log --no-merges --format=%H -40)
printf "%-12s %8s %8s %8s\n" algorithm hunks added removed
for alg in myers minimal patience histogram; do
  h=0; a=0; d=0
  for c in $commits; do
    out=$(git diff --diff-algorithm=$alg --unified=3 "$c^" "$c" -- '*.ts' '*.tsx' '*.js' '*.mjs' '*.json' 2>/dev/null)
    h=$((h + $(grep -c '^@@' <<<"$out")))
    a=$((a + $(grep -c '^+[^+]' <<<"$out")))
    d=$((d + $(grep -c '^-[^-]' <<<"$out")))
  done
  printf "%-12s %8s %8s %8s\n" "$alg" "$h" "$a" "$d"
done
