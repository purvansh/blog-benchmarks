# Seven JSON parsers, one large file

Measures peak resident memory and wall clock for seven ways to sum one float
field across a large JSON array. Every parser does identical work, and all seven
agree on the sum, which is how a streaming parser is shown not to be skipping
records.

## Run

```bash
python3 gen.py 900000          # 164 MiB, 900k records -> data.json
./bench.sh                     # median of 3 runs each, peak RSS via /usr/bin/time

python3 gen.py 3400000         # 621 MiB, 3.4M records
mv data.json big.json
./bigbench.sh                  # the same parsers against the larger file

python3 split.py json          # separate parse time from the walk over the result
python3 split.py orjson
```

`ijson` and `orjson` must be importable. Note that `python3 -I` ignores user
site-packages, so the runners for those two deliberately do not use it.

## Results

164 MiB file, 900,000 records, median of 3:

| parser | wall | peak RSS |
|---|---|---|
| Bun 1.3.14 | 0.90 s | 453 MiB |
| Node 22 | 1.44 s | 515 MiB |
| ijson 3.6.0 | 2.00 s | 12 MiB |
| orjson 3.13.0 | 3.33 s | 1356 MiB |
| Python json | 3.37 s | 971 MiB |
| jq 1.6 | 4.30 s | 1021 MiB |
| jq 1.6 --stream | 15.22 s | 3 MiB |

621 MiB file, 3,400,000 records:

| parser | wall | peak RSS | multiple of file |
|---|---|---|---|
| Bun 1.3.14 | 3.21 s | 1596 MiB | 2.6x |
| ijson | 7.34 s | 12 MiB | 0.02x |
| orjson | 11.81 s | 5096 MiB | 8.2x |
| Python json | 13.46 s | 3643 MiB | 5.9x |
| jq 1.6 | 15.81 s | 3825 MiB | 6.2x |
| jq --stream | 57.40 s | 3 MiB | 0.005x |
| Node 22 | fails | n/a | n/a |

Node 22 cannot read the 621 MiB file at all:

```
Error: Cannot create a string longer than 0x1fffffe8 characters
```

That is `buffer.constants.MAX_STRING_LENGTH`, 536,870,888, about 512 MiB. The
machine had 27 GiB free at the time.

Parse separated from the walk, on the 164 MiB file:

| | parse | walk | peak |
|---|---|---|---|
| `json.loads` | 3.00 s | 0.08 s | 1137 MiB |
| `orjson.loads` | 2.66 s | 0.08 s | 1356 MiB |

orjson is 1.13x faster to parse and peaks 219 MiB higher, with bytes input,
which is the input type its README recommends for lower memory use.
