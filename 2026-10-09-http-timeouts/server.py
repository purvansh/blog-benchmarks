# Two deliberately broken servers.
#   :8099  accepts the connection and never sends a single byte
#   :8100  sends a complete set of headers, then stalls forever mid body
import socket, threading
def serve(port, preamble):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", port)); s.listen(64)
    held = []
    while True:
        c, _ = s.accept()
        try: c.recv(65535)
        except OSError: pass
        if preamble:
            try: c.sendall(preamble)
            except OSError: pass
        held.append(c)          # never closed, never written to again
threading.Thread(target=serve, args=(8099, b""), daemon=True).start()
serve(8100, b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 100\r\n\r\n")
