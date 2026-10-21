#!/usr/bin/env bash
# Same 19 pinned packages into a fresh environment, five installers.
# Cold = empty cache volume. Warm = same volume, second run.
# Integer nanosecond arithmetic in bash, because the slim image has no bc.
set -uo pipefail
IMG=python:3.12-slim
REQ=/w/req.txt
here="$(cd "$(dirname "$0")" && pwd)"

run() { docker run --rm -v "$here":/w:ro -v "$2":/root/.cache "$IMG" bash -c "$3" 2>&1 | tail -1; }

bench() {
  local name="$1" setup="$2" cmd="$3"
  local vol="pyvol${name}"
  docker volume rm -f "$vol" >/dev/null 2>&1; docker volume create "$vol" >/dev/null
  local body="{ $setup ; } >/dev/null 2>&1; s=\$(date +%s%N); { $cmd ; } >/dev/null 2>&1; rc=\$?; e=\$(date +%s%N); echo \$(( (e-s)/1000000 )) \$rc"
  local cold warm
  cold=$(run "$name" "$vol" "$body")
  warm=$(run "$name" "$vol" "$body")
  printf "%-8s cold %7s ms rc=%-3s   warm %7s ms rc=%s\n" \
    "$name" "${cold%% *}" "${cold##* }" "${warm%% *}" "${warm##* }"
  docker volume rm -f "$vol" >/dev/null 2>&1
}

bench pip    "true" "python -m venv /v && /v/bin/pip install -q -r $REQ"
bench uv     "pip install -q uv" "uv venv /v && VIRTUAL_ENV=/v uv pip install -q -r $REQ"
bench poetry "pip install -q poetry && mkdir -p /p && cd /p && poetry init -n --name bench && poetry config virtualenvs.in-project true" \
             "cd /p && poetry add -n -q \$(sed 's/==/@/' $REQ | tr '\n' ' ')"
bench pdm    "pip install -q pdm && mkdir -p /p && cd /p && pdm init -n --python 3.12" \
             "cd /p && pdm add -q \$(tr '\n' ' ' < $REQ)"
bench pipenv "pip install -q pipenv && mkdir -p /p" "cd /p && pipenv install -q -r $REQ"
