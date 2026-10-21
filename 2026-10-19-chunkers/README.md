# Six ways to chunk one document

Scores each splitter on what it *breaks*, not on how many pieces it makes.

Document: the Playwright MCP README, 66,827 chars, 16,494 cl100k tokens, 30
fenced code blocks.

## Run

```bash
curl -sSL -o doc.md https://raw.githubusercontent.com/microsoft/playwright-mcp/main/README.md
docker run --rm -v "$PWD":/w:ro python:3.12-slim bash -c \
  'pip install -q langchain-text-splitters tiktoken && python /w/chunk.py'
```

## Results

| splitter | chunks | median tok | max tok | code cut | mid-sentence |
|---|---|---|---|---|---|
| recursive, generic | 89 | 208 | 379 | **5** | 11% |
| markdown headers | 12 | 339 | **7,447** | **0** | 0% |
| token window (cl100k) | 103 | 206 | 230 | 9 | 73% |
| recursive, markdown preset | 100 | 196 | 349 | **18** | 14% |
| fixed chars | 67 | 238 | 386 | 6 | 83% |
| fixed chars + overlap | 84 | 238 | 375 | 7 | 89% |

The markdown preset cut 3.6x more code blocks than the generic splitter. The
reason is its separator list:

```
'\n#{1,6} '      <- headings, highest priority
'```\n'          <- the code fence, SECOND priority
...
```

It is configured to prefer cutting at a code fence, which leaves chunks holding
an unbalanced number of fence markers.

## A metric that was dropped

An earlier version also counted broken markdown tables, as "chunk starts with a
`|` row that is not a header separator". That rewards any splitter which never
starts a chunk at a line boundary, so the fixed-character splitters scored 0 on
it for the wrong reason. It was removed rather than reported.
