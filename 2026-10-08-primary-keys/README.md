# One million rows, seven primary keys

Loads the identical million row payload into Postgres 17 seven times, changing
only the primary key, and measures COPY time, heap size, primary key index size,
WAL bytes, and B-tree leaf density.

## Run

```bash
docker run -d --name pgbench -e POSTGRES_PASSWORD=bench -p 55432:5432 \
  postgres:17-alpine -c full_page_writes=on -c wal_compression=off
psql -h 127.0.0.1 -p 55432 -U postgres -c "create extension if not exists pgstattuple;"

python3 genids.py     # one CSV per scheme, keys generated outside the database
./bench.sh            # COPY time, sizes, WAL delta from pg_current_wal_lsn()
./dens.sh             # B-tree leaf density from pgstatindex

python3 genv7.py      # uuid v7 at three different generation rates
./v7bench.sh
```

Each run issues `CHECKPOINT` before loading so full page write behaviour starts
from the same place.

## Results

| scheme | COPY | heap | PK index | WAL | leaf density |
|---|---|---|---|---|---|
| bigint identity | 1.65 s | 58 MB | 21 MB | 96 MB | 90.1% |
| Snowflake bigint | 1.65 s | 58 MB | 24 MB | 98 MB | 80.8% |
| UUID v7 (uuid) | 2.76 s | 66 MB | 41 MB | 124 MB | 67.0% |
| UUID v4 (uuid) | 3.54 s | 66 MB | 38 MB | 126 MB | 71.6% |
| ULID (text) | 3.24 s | 73 MB | 63 MB | 162 MB | 67.5% |
| nanoid (text) | 4.06 s | 66 MB | 51 MB | 146 MB | 69.0% |
| UUID v4 (text) | 4.57 s | 81 MB | 73 MB | 189 MB | 69.9% |

The UUID v7 row above is generated at 1000 ids per millisecond. The rate is the
whole story:

| v7 variant | COPY | PK index | leaf density | WAL |
|---|---|---|---|---|
| monotonic, no random tail | 2.09 s | 30 MB | 90.0% | 113 MB |
| 10 ids per ms | 2.21 s | 30 MB | 90.0% | 113 MB |
| 1000 ids per ms | 2.75 s | 41 MB | 67.0% | 124 MB |
| v4 random, for comparison | 3.55 s | 38 MB | 71.6% | 126 MB |

At ten ids per millisecond, v7 indexes exactly like a counter. At a thousand,
the random tail scatters keys within each millisecond and the index comes out
larger than random v4's.
