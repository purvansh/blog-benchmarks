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
