# How many inotify watches a recursive watcher needs for a tree, and what the
# kernel will actually give you. The limit is per user, not per process, which
# is the part that turns this into an outage rather than an error.
import os, sys, subprocess
root = sys.argv[1]
dirs = files = 0
for d, dn, fn in os.walk(root):
    dirs += 1; files += len(fn)
def sysctl(k):
    return int(open(f"/proc/sys/fs/inotify/{k}").read().strip())
used = 0
for p in os.listdir("/proc"):
    if not p.isdigit(): continue
    fd = f"/proc/{p}/fd"
    try: names = os.listdir(fd)
    except OSError: continue
    for n in names:
        try:
            if "inotify" in os.readlink(os.path.join(fd, n)):
                try:
                    used += sum(1 for l in open(f"/proc/{p}/fdinfo/{n}") if l.startswith("inotify"))
                except OSError: pass
        except OSError: pass
print(f"tree            {root}")
print(f"directories     {dirs:,}")
print(f"files           {files:,}")
print(f"max_user_watches  {sysctl('max_user_watches'):,}")
print(f"max_user_instances {sysctl('max_user_instances'):,}")
print(f"max_queued_events  {sysctl('max_queued_events'):,}")
print(f"watches in use right now (all processes, this user): {used:,}")
