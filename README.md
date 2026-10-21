# blog-benchmarks

The rigs behind the measurement posts on [purvansh.site/blog](https://purvansh.site/blog).

Every post on that blog has to contain a number that was actually measured rather
than quoted. This repository is where those measurements come from: one directory
per post, holding the scripts that produced the figures, the exact commands, and
the raw output they printed.

Nothing here is a library. These are single purpose rigs, written to answer one
question each, and kept exactly as they were when the numbers were taken.

## The machine

Unless a directory's README says otherwise, every figure was measured here:

| | |
|---|---|
| CPU | Intel Core i5-1135G7, 4 cores / 8 threads, up to 4.2 GHz |
| Memory | 31 GiB |
| OS | Ubuntu 22.04.5 LTS, kernel 6.8.0-138-generic |
| Node | v22.22.0 |
| Python | 3.10.12 (host), 3.12.15 (containers) |
| Docker | 29.9.0, overlay2 |

Absolute numbers move with hardware. The ratios between entries are the part
that should reproduce on yours.

## Running them

Each directory has its own README with the commands. Where a rig walks a file
tree it reads `$TREE`, so point that at whatever you want measured:

```bash
TREE=/path/to/some/repo ./final.sh
```

## Index

| Date | Post | Rig |
|---|---|---|
| 2026-10-07 | [Seven JSON parsers on one 621 MiB file](https://purvansh.site/blog/seven-json-parsers-one-big-file) | [`2026-10-07-json-parsers`](./2026-10-07-json-parsers) |
| 2026-10-08 | [One million rows, seven primary keys](https://purvansh.site/blog/primary-keys-and-the-wal-they-cost) | [`2026-10-08-primary-keys`](./2026-10-08-primary-keys) |
| 2026-10-09 | [Eight HTTP clients against a server that never answers](https://purvansh.site/blog/http-clients-that-wait-forever) | [`2026-10-09-http-timeouts`](./2026-10-09-http-timeouts) |
| 2026-10-10 | [Five Python installers, nineteen packages](https://purvansh.site/blog/python-installers-cold-and-warm) | [`2026-10-10-python-installers`](./2026-10-10-python-installers) |
| 2026-10-14 | [One repo, four file watchers](https://purvansh.site/blog/four-file-watchers-one-kernel-budget) | [`2026-10-14-file-watchers`](./2026-10-14-file-watchers) |
| 2026-10-11 | [A hundred thousand vectors, six HNSW settings](https://purvansh.site/blog/hnsw-settings-and-the-biggest-index) | [`2026-10-11-hnsw-settings`](./2026-10-11-hnsw-settings) |
| 2026-10-12 | [Four load generators, one stalling server](https://purvansh.site/blog/load-generators-and-the-p99-that-lies) | [`2026-10-12-load-generators`](./2026-10-12-load-generators) |
| 2026-10-13 | [One SQLite database, seven durability settings](https://purvansh.site/blog/sqlite-durability-and-the-149x) | [`2026-10-13-sqlite-durability`](./2026-10-13-sqlite-durability) |
| 2026-10-15 | [Five schedulers, one missed window](https://purvansh.site/blog/schedulers-and-the-missed-window) | [`2026-10-15-schedulers`](./2026-10-15-schedulers) |
| 2026-10-16 | [Eight ways to checksum 2 GiB](https://purvansh.site/blog/checksum-2gib-and-the-same-algorithm-twice) | [`2026-10-16-hash-throughput`](./2026-10-16-hash-throughput) |
| 2026-10-17 | [Four diff algorithms over 800 commits](https://purvansh.site/blog/diff-algorithms-over-800-commits) | [`2026-10-17-diff-algorithms`](./2026-10-17-diff-algorithms) |
| 2026-10-18 | [Five Python type checkers against ten planted bugs](https://purvansh.site/blog/five-type-checkers-ten-planted-bugs) | [`2026-10-18-type-checkers`](./2026-10-18-type-checkers) |
| 2026-10-19 | [Six ways to chunk one document](https://purvansh.site/blog/six-chunkers-one-document) | [`2026-10-19-chunkers`](./2026-10-19-chunkers) |
| 2026-10-20 | [Four Node package managers](https://purvansh.site/blog/node-package-managers-second-project) | [`2026-10-20-node-package-managers`](./2026-10-20-node-package-managers) |
| 2026-10-21 | [Five popular MCP servers, read for their defaults](https://purvansh.site/blog/mcp-server-defaults-read-closely) | [`2026-10-21-mcp-defaults`](./2026-10-21-mcp-defaults) |

## A note on the numbers that changed

Two figures in these rigs were wrong before they were right, and the corrections
are in the history rather than quietly overwritten:

- The file watcher counts were first taken per process from `/proc/<pid>/fdinfo`,
  which undercounts Node's recursive watcher by roughly 4x. The rig now measures
  the delta in the user's total watch count across every process, which is what
  the kernel actually charges the uid for.
- An attempt to measure what chokidar reports at the watch ceiling used
  `getWatched()`, which returns an empty object even on a healthy 100 directory
  tree. That measurement was dropped rather than published.
- The SQLite default configuration first measured at 6.29 s and reproduces at
  41.7 s on an idle disk. The fast figure was discarded.
- The type checker scores were first computed from hand-written line numbers,
  five of which were wrong, and then by exact line match, which undercounts
  every checker. See that directory's README.
- A broken-table metric in the chunker rig rewarded splitters for never
  starting a chunk at a line boundary. Removed rather than reported.
