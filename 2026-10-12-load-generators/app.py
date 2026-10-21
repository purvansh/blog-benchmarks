# A server that stops the world. Every 10 seconds it takes a global lock and
# holds it for one second, so every request in flight and every request that
# arrives during that second is blocked. This is the shape of a GC pause, a
# cache rebuild or a lock convoy, and it is the case that separates load
# generators measuring service time from ones measuring what a user felt.
import http.server, socketserver, threading, time

STALL_EVERY, STALL_FOR = 10.0, 1.0
lock = threading.Lock()

def stall_loop():
    start = time.time()
    while True:
        time.sleep(max(0, STALL_EVERY - ((time.time() - start) % STALL_EVERY)))
        with lock:
            time.sleep(STALL_FOR)

class H(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    def do_GET(self):
        with lock:
            pass
        body = b"ok"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a): pass

class S(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

threading.Thread(target=stall_loop, daemon=True).start()
S(("0.0.0.0", 8111), H).serve_forever()
