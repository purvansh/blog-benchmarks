# Four diff algorithms over 800 commits

Runs every `git diff --diff-algorithm` over the same commits and compares the
output by hash rather than by eye.

## Run

```bash
git clone --filter=blob:none https://github.com/expressjs/express.git
REPO=$PWD/express N=800 ./compare.sh    # how often they disagree at all
REPO=$PWD/express LIST=$PWD/differing-commits.txt ./detail.sh   # by how much
```

## Results

800 non-merge commits of expressjs/express, git 2.34.1.

| pair | commits that differ |
|---|---|
| myers vs minimal | **0 of 800** |
| myers vs patience | 16 of 800 |
| myers vs histogram | 18 of 800 |
| patience vs histogram | 11 of 800 |
| indent heuristic on vs off | 11 of 800 |

Any disagreement at all: 20 of 800, or 2.5%.

On those 20 commits:

| algorithm | hunks | added | removed |
|---|---|---|---|
| myers | 299 | 2,575 | 1,561 |
| minimal | 299 | 2,575 | 1,561 |
| patience | 292 | 2,582 | 1,568 |
| histogram | 292 | 2,577 | 1,563 |

`minimal` is documented as spending extra time to find a smaller diff. It
produced byte-identical output to the default on every commit in the sample.
