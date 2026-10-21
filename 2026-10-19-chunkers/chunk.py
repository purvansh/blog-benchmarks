# Six ways to split one technical document, scored on what they break.
#
# The usual chunker comparison counts chunks and stops. The things that
# actually cost you at retrieval time are structural: a fenced code block cut
# in half is two chunks that are each wrong, and a chunk that begins mid
# sentence has lost the subject of its own first clause.
import re, statistics, tiktoken
from langchain_text_splitters import (
    CharacterTextSplitter, RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter, TokenTextSplitter,
)

doc = open("/w/doc.md", encoding="utf8").read()
enc = tiktoken.get_encoding("cl100k_base")
SIZE, OVER = 1000, 200

def ntok(s): return len(enc.encode(s, disallowed_special=()))

def score(name, chunks):
    chunks = [c for c in chunks if c.strip()]
    toks = [ntok(c) for c in chunks]
    # a chunk with an odd number of fence markers starts or ends inside a code block
    broken_code = sum(1 for c in chunks if c.count("```") % 2 == 1)
    # ends mid sentence: last non space char is not . ! ? : ) ` | # or end of a list item
    mid_sent = sum(1 for c in chunks if c.rstrip() and c.rstrip()[-1] not in ".!?:`|)]}>-*")
    # a table row split from its header row
    broken_table = sum(1 for c in chunks if c.lstrip().startswith("|") and "---" not in c.split("\n")[0])
    over = sum(1 for t in toks if t > SIZE)
    print(f"{name:26s} {len(chunks):5d} {statistics.median(toks):7.0f} {max(toks):7d} "
          f"{broken_code:7d} {mid_sent*100//max(1,len(chunks)):6d}% {broken_table:7d} {over:5d}")

print(f"document: {len(doc):,} chars, {ntok(doc):,} tokens, {doc.count('```')//2} code blocks\n")
print(f"{'splitter':26s} {'chunks':>5s} {'median':>7s} {'max':>7s} {'codecut':>7s} {'midsent':>7s} {'tblcut':>7s} {'over':>5s}")

score("fixed chars, no overlap",
      CharacterTextSplitter(separator="", chunk_size=SIZE, chunk_overlap=0).split_text(doc))
score("fixed chars, 200 overlap",
      CharacterTextSplitter(separator="", chunk_size=SIZE, chunk_overlap=OVER).split_text(doc))
score("recursive, 200 overlap",
      RecursiveCharacterTextSplitter(chunk_size=SIZE, chunk_overlap=OVER).split_text(doc))
score("recursive, markdown-aware",
      RecursiveCharacterTextSplitter.from_language("markdown", chunk_size=SIZE, chunk_overlap=OVER).split_text(doc))
score("token window (cl100k)",
      TokenTextSplitter(chunk_size=250, chunk_overlap=50).split_text(doc))
hdr = MarkdownHeaderTextSplitter([("#", "h1"), ("##", "h2"), ("###", "h3")])
score("markdown headers", [d.page_content for d in hdr.split_text(doc)])
