# Five type checkers against ten planted bugs

`store-annotated.py` carries ten planted type errors with `# BUG n:` markers.
The harness derives the line numbers from those markers and writes a stripped
copy, so the file the checkers read has no markers in it.

## Run

```bash
# derive expected.txt and write the marker-free copy
python3 -c "<see the post rig>"
docker run --rm -v "$PWD":/w python:3.12-slim bash -c '
  apt-get update -qq && apt-get install -y -qq nodejs npm
  pip install -q mypy pyright pyrefly ty pytype
  python /w/score.py'
python3 rescore.py    # score per bug, from the saved raw output
```

## Results

Defaults, no configuration file for any of them.

| checker | found | false positives | time |
|---|---|---|---|
| ty 0.0.90 | **10/10** | 0 | **89 ms** |
| mypy 2.4.0 | **10/10** | 0 | 240 ms |
| pyright | 9/10 | 0 | 1,938 ms |
| pytype 2024.10.11 | 8/10 | 0 | 9,767 ms |
| pyrefly 1.4.0 | **0/10** | 0 | 260 ms |

pyrefly's zero is not a failure to run. It prints:

```
INFO 0 errors
No `pyrefly.toml` found — using preset `basic`.
```

The same file under `preset = "strict"` produces 10 errors.

## Two scoring bugs worth recording

1. The first pass used **hand-written line numbers**, and five of the ten were
   wrong. `expected.txt` is now derived from the markers in the source.
2. Scoring by exact line undercounted every tool at once. A checker reports a
   missing return at the `def` line and a missing await at the *use* site, both
   correctly. `rescore.py` scores per bug, with an accepted line set each.

Before those fixes mypy scored 8/10 and pyright 7/10. Both actually find more
than that.
