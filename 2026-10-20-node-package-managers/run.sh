#!/usr/bin/env bash
# Inside the container: install the same package.json four ways, in two
# separate projects each, and measure what lands on disk.
set -uo pipefail
measure() {
  local name="$1" p1="$2" p2="$3" store="$4"
  local s1 f1 d1 total
  s1=$(du -sm --apparent-size "$p1" 2>/dev/null | cut -f1)
  f1=$(find "$p1" -type f 2>/dev/null | wc -l)
  d1=$(find "$p1" -type d 2>/dev/null | wc -l)
  total=$(du -sm --total "$p1" "$p2" $store 2>/dev/null | tail -1 | cut -f1)
  printf "%-8s | one project %5s MB | files %6s | dirs %5s | two projects + store %5s MB\n" \
    "$name" "$s1" "$f1" "$d1" "$total"
}

prep() { rm -rf /w2 && mkdir -p /w2 && cp /src/package.json /w2/; }

# npm
mkdir -p /a && cp /src/package.json /a/ && (cd /a && npm install --silent --no-fund --no-audit >/dev/null 2>&1)
prep && (cd /w2 && npm install --silent --no-fund --no-audit >/dev/null 2>&1)
measure npm /a/node_modules /w2/node_modules ""

# yarn classic
corepack enable >/dev/null 2>&1
mkdir -p /b && cp /src/package.json /b/ && (cd /b && yarn install --silent >/dev/null 2>&1)
prep && (cd /w2 && yarn install --silent >/dev/null 2>&1)
measure yarn /b/node_modules /w2/node_modules ""

# pnpm
mkdir -p /c && cp /src/package.json /c/ && (cd /c && pnpm install --silent >/dev/null 2>&1)
prep && (cd /w2 && pnpm install --silent >/dev/null 2>&1)
measure pnpm /c/node_modules /w2/node_modules "$(pnpm store path 2>/dev/null)"

# bun
mkdir -p /d && cp /src/package.json /d/ && (cd /d && bun install --silent >/dev/null 2>&1)
prep && (cd /w2 && bun install --silent >/dev/null 2>&1)
measure bun /d/node_modules /w2/node_modules "/root/.bun/install/cache"

# yarn berry with node-modules linker is the same as classic for layout, so the
# interesting berry case is Plug'n'Play, which writes no node_modules at all.
mkdir -p /e && cp /src/package.json /e/
(cd /e && yarn set version berry >/dev/null 2>&1 && yarn config set nodeLinker pnp >/dev/null 2>&1 && yarn install >/dev/null 2>&1)
if [ -d /e/.yarn/cache ]; then
  sz=$(du -sm --apparent-size /e/.yarn/cache | cut -f1)
  files=$(find /e/.yarn/cache -type f | wc -l)
  nm=$([ -d /e/node_modules ] && echo yes || echo "none")
  printf "%-8s | one project %5s MB | files %6s | dirs %5s | node_modules: %s\n" "yarn-pnp" "$sz" "$files" "0" "$nm"
fi
