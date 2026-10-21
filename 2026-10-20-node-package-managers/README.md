# What the second project costs

Installs the same package.json into two separate project directories and
measures disk with the shared store counted once, which is the marginal cost of
the next repo you clone.

## Run

```bash
docker run --rm -v "$PWD":/src:ro -v "$PWD/run.sh":/run.sh:ro node:22-slim bash -c '
  apt-get update -qq && apt-get install -y -qq curl unzip
  npm i -g pnpm && curl -fsSL https://bun.sh/install | bash
  export PATH="/root/.bun/bin:$PATH" && corepack enable
  bash /run.sh'
```

## Results

| manager | one project | two projects | second costs | files | dirs |
|---|---|---|---|---|---|
| pnpm 12.14.0 | 106 MB | 138 MB | **32 MB** | 9,415 | 1,267 |
| bun 1.4.3 | 107 MB | 155 MB | 48 MB | 9,472 | 783 |
| npm 10.9.9 | 118 MB | 290 MB | 172 MB | 9,470 | 774 |
| yarn 1.22.22 | 132 MB | 320 MB | 188 MB | 9,510 | 811 |
| Yarn PnP 4.18.1 | 1 MB + 133 MB cache | 184 MB | 50 MB | **5 + 242** | 0 |

Every layout that builds a `node_modules` writes between 9,415 and 9,510 files,
within 1% of each other. Yarn Plug'n'Play is the only one that changes that
number, because the packages stay zipped: 242 archives instead of ~9,470 loose
files, and no `node_modules` at all.

`du` is run across the project directories and the store in a single
invocation, so a hardlinked file is counted once rather than twice.
