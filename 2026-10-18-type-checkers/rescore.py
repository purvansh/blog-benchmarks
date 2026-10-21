# Score per BUG, not per line. A checker legitimately attributes a missing
# return to the `def` line and a missing await to the use site, so each bug
# carries the set of lines where a correct diagnostic may land.
import re, glob, os
ACCEPT = {
    "BUG1 optional not narrowed":   {35},
    "BUG2 int += str":              {39},
    "BUG3 unknown attribute":       {44},
    "BUG4 missing return":          {46, 51},   # 46 is `def total`
    "BUG5 dict returned as list":   {58},
    "BUG6 wrong arity":             {62},
    "BUG7 dict value type":         {65, 66},   # comprehension spans two lines
    "BUG8 missing await":           {75, 76},   # 76 is the use site
    "BUG9 join of non-str":         {83},
    "BUG10 str for int param":      {91},
}
ALL = set().union(*ACCEPT.values())
LINE_RE = re.compile(r"store_clean\.py[\"']?(?::(\d+)|,\s*line\s+(\d+))")
print(f"{'checker':9s} {'found':>7s} {'false positives':>16s}   missed")
for f in sorted(glob.glob("out-*.txt")):
    name = os.path.basename(f)[4:-4]
    out = open(f, errors="replace").read()
    lines = {int(a or b) for a, b in LINE_RE.findall(out)}
    hits = [b for b, acc in ACCEPT.items() if acc & lines]
    missed = [b.split()[0] for b in ACCEPT if not (ACCEPT[b] & lines)]
    fp = sorted(lines - ALL)
    print(f"{name:9s} {len(hits):5d}/10 {len(fp):16d}   {missed if missed else 'none'}   fp lines {fp}")
