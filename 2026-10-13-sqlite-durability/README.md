# SQLite durability settings, per row and per commit

`bench.py` writes 100,000 rows in ONE transaction under seven pragma
combinations. Every configuration finishes in about 0.1 s and they are
indistinguishable, which is the point: the settings cost nothing per row.

`bench2.py` writes the same rows in 5,000 transactions of 20. That is where
they separate.

## Run

```bash
python3 bench.py     # one transaction: all settings look identical
python3 bench2.py    # 5,000 transactions: best of 5
python3 verify.py    # isolates the delete+FULL vs delete+NORMAL pair
```

## Results

SQLite 3.37.2, ext4 on NVMe, machine idle, best of 5.

| configuration | 1 txn | 5,000 txns | commits/sec | vs default |
|---|---|---|---|---|
| WAL + OFF | 0.09 s | 0.14 s | 35,903 | 299x |
| journal OFF + OFF | 0.09 s | 0.15 s | 32,369 | 270x |
| **WAL + NORMAL** | 0.10 s | **0.28 s** | **17,861** | **149x** |
| MEMORY + NORMAL | 0.10 s | 11.43 s | 438 | 3.7x |
| WAL + FULL | 0.10 s | 11.69 s | 428 | 3.6x |
| delete + NORMAL | 0.11 s | 31.35 s | 159 | 1.3x |
| defaults (delete + FULL) | 0.12 s | 41.73 s | 120 | baseline |

On this build, `pragma journal_mode=WAL` leaves `synchronous` at 2 (FULL):

```
fresh db   journal_mode = delete | synchronous = 2
after WAL  journal_mode = wal    | synchronous = 2
```

So turning on WAL alone buys 3.6x of an available 149x.

## A number that was wrong first

An earlier run with other work on the machine reported the default
configuration at 6.29 s, seven times faster than it reproduces when the disk is
otherwise idle. `verify.py` exists because that figure looked wrong: it runs
the suspicious pair five times alternating, which showed 41.7 s and 32.2 s
consistently. The 6.29 s figure was discarded, not published.
