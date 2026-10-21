import ctypes, os, sys
lib = ctypes.CDLL("libc.so.6", use_errno=True)
fd = lib.inotify_init()
IN_ALL = 0x00000FFF
n = 0
for d, _, _ in os.walk(sys.argv[1]):
    if lib.inotify_add_watch(fd, d.encode(), IN_ALL) >= 0: n += 1
    else:
        print("ENOSPC at", n, flush=True); break
print("watches added:", n, flush=True)
while True: os.read(fd, 4096)
