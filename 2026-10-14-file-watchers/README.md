# One repo, four file watchers, one kernel budget

Measures how many inotify watches each recursive file watcher takes for the same
tree, and what happens at the ceiling.

`max_user_watches` is per UID, not per process, so every watcher running as you
draws from one budget.

## Run

```bash
TREE=/path/to/repo ./final.sh        # watches and RSS per watcher
TREE=/path/to/repo ./contention.sh   # what the second watcher does
```

`final.sh` measures the delta in the user's total watch count across every
process. Do not use `/proc/<pid>/fdinfo` for this: it undercounts Node's
recursive watcher by roughly 4x, which is the error the first version of this
rig made.

The ceiling test runs in a container as a uid nothing else uses, so the only
inotify quota it exhausts is its own:

```bash
docker run --rm -u 12345 -v "$PWD":/w:ro python:3.12-slim bash -c '
  mkdir -p /tmp/t && cd /tmp/t && for i in $(seq 0 69999); do mkdir -p d$i; done
  python3 /w/enospc.py'
```

## Results

Tree: 5,006 directories, 46,197 files, 51,203 total. Ceiling: 65,536.

| watcher | watches | RSS |
|---|---|---|
| raw inotify, one per directory | 5,006 | 10 MB |
| @parcel/watcher | 5,006 | 72 MB |
| node fs.watch recursive | 51,105 | 163 MB |
| chokidar 3.6.0 | 51,104 | 338 MB |

chokidar and Node's recursive watcher both take a watch per file, not per
directory, which is 78% of the entire user budget for one watcher on one repo.

The ceiling is exact:

```
refused after 65536 watches: errno 28 (No space left on device)
```

Contention, from a clean baseline of 550 watches in use:

- chokidar alone on this repo: fine, reaches `ready`.
- node fs.watch started first, taking the total to 51,655, then chokidar:
  `Error: ENOSPC: System limit for number of file watchers reached`

The second watcher to start is the one that dies.
