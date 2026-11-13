import http.server, urllib.parse, json, pathlib
class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get('Content-Length', 0))).decode()
        tok = urllib.parse.parse_qs(body).get('logout_token', [''])[0]
        pathlib.Path('/home/claude/poc-zitadel/logout-token.txt').write_text(tok)
        self.send_response(200); self.end_headers()
    def log_message(self, *a): pass
http.server.HTTPServer(('0.0.0.0', 8097), H).serve_forever()
