#!/usr/bin/env bash
# Only the commits where the algorithms disagree. How much do they disagree by?
cd "${REPO:?}"
printf "%-12s %7s %7s %7s\n" algorithm hunks added removed
for alg in myers minimal patience histogram; do
  h=0; a=0; d=0
  while read -r c; do
    out=$(git diff --diff-algorithm=$alg -U3 "$c^" "$c" 2>/dev/null)
    h=$((h + $(grep -c '^@@' <<<"$out")))
    a=$((a + $(grep -c '^+[^+]' <<<"$out")))
    d=$((d + $(grep -c '^-[^-]' <<<"$out")))
  done < "$LIST"
  printf "%-12s %7s %7s %7s\n" "$alg" "$h" "$a" "$d"
done
