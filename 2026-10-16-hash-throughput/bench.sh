#!/usr/bin/env bash
# Throughput of each hash over the same 2 GiB file, read from page cache so the
# number is CPU work and not disk. Best of 3. The file is warmed first.
F=/tmp/hashfile.bin
SIZE=$(stat -c%s "$F")
cat "$F" > /dev/null   # warm the page cache
run() {
  local name="$1"; shift
  local best=""
  for i in 1 2 3; do
    local s e el
    s=$(date +%s%N); "$@" "$F" >/dev/null 2>&1; e=$(date +%s%N)
    el=$(( (e-s)/1000000 ))
    [ -z "$best" ] && best=$el || { [ "$el" -lt "$best" ] && best=$el; }
  done
  awk -v n="$name" -v ms="$best" -v sz="$SIZE" \
    'BEGIN{printf "%-22s %7s ms  %8.0f MB/s\n", n, ms, (sz/1048576)/(ms/1000)}'
}
run "md5sum"            md5sum
run "sha1sum"           sha1sum
run "sha256sum"         sha256sum
run "sha512sum"         sha512sum
run "b2sum (BLAKE2b)"   b2sum
run "cksum (CRC32)"     cksum
run "openssl sha256"    openssl dgst -sha256
run "openssl blake2b512" openssl dgst -blake2b512
