# Run each checker at its default settings and score it against the planted
# lines. Output formats differ per tool, so the line extractor accepts both
# "file.py:LINE" and 'File "...", line LINE'.
import re, subprocess, sys, time

EXPECTED = {int(l.split()[0]) for l in open("/w/expected.txt") if l.strip()}
TARGET = "app/store_clean.py"
LINE_RE = re.compile(r"store_clean\.py[\"']?(?::(\d+)|,\s*line\s+(\d+))")

TOOLS = [
    ("mypy",    ["mypy", TARGET]),
    ("pyright", ["pyright", TARGET]),
    ("pyrefly", ["pyrefly", "check", TARGET]),
    ("ty",      ["ty", "check", TARGET]),
    ("pytype",  ["pytype", "-j", "4", TARGET]),
]

print(f"{'checker':9s} {'ms':>7s}  {'found':>7s}  {'extra':>5s}   missed")
for name, cmd in TOOLS:
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd="/w", capture_output=True, text=True, timeout=600)
        out = p.stdout + p.stderr
    except Exception as e:
        print(f"{name:9s} {'-':>7s}  FAILED {e}"); continue
    ms = int((time.time() - t0) * 1000)
    lines = {int(a or b) for a, b in LINE_RE.findall(out)}
    if not lines and "error" not in out.lower():
        status = "clean run, no diagnostics parsed"
    hit = sorted(EXPECTED & lines)
    extra = sorted(lines - EXPECTED)
    missed = sorted(EXPECTED - lines)
    print(f"{name:9s} {ms:7d}  {len(hit):5d}/10  {len(extra):5d}   {missed}")
    open(f"/w/out-{name}.txt", "w").write(out)
