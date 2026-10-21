# Allocate inotify watches until the kernel refuses, as a uid nothing else on
# the machine runs as, so the only quota exhausted is this test's own.
import ctypes, os
lib = ctypes.CDLL("libc.so.6", use_errno=True)
fd = lib.inotify_init()
n = 0
while True:
    d = f"/tmp/t/d{n}"
    wd = lib.inotify_add_watch(fd, d.encode(), 0x00000FFF)
    if wd < 0:
        e = ctypes.get_errno()
        print(f"refused after {n} watches: errno {e} ({os.strerror(e)})")
        break
    n += 1
    if n > 70000:
        print("no refusal by", n); break
print("limit file says:", open("/proc/sys/fs/inotify/max_user_watches").read().strip())
