# Five Python installers, cold and warm

Installs the same 19 pinned packages into a clean `python:3.12-slim` container
five ways. Each installer gets its own empty Docker named volume for the cold
run, then the same volume again for the warm run, which is the shape of a CI job
with a restored cache.

Only the install command is timed. Installing the installer is not.

## Run

```bash
./bench.sh
```

Timing is integer nanosecond arithmetic in bash, because the slim image has no
`bc`. An earlier version of this rig used `bc` and silently reported every
duration as 0.0 s.

## Results

| installer | cold | warm | warm vs pip |
|---|---|---|---|
| uv 0.13.4 | 48.2 s | 0.34 s | 125x faster |
| Poetry 2.5.1 | 72.3 s | 4.5 s | 9.4x faster |
| Pipenv 2026.10.2 | 88.4 s | 24.3 s | 1.7x faster |
| pip 25.0.1 | 105.1 s | 42.2 s | baseline |
| PDM 2.29.3 | 93.4 s | 45.9 s | 9% slower |

The warm uv number was verified rather than trusted: a repeat run took 321 ms
and the resulting venv imports pandas 2.2.3, numpy 2.2.1, boto3, fastapi,
sqlalchemy and celery.
