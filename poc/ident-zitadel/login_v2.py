#!/usr/bin/env python3
"""PoC: Anmeldung über Login V2 (Passwort oder Edulog). Aufruf: python3 login_v2.py redaktion | python3 login_v2.py edulog lehrperson"""
import json, pathlib, sys, http.server, threading, urllib.parse, secrets, hashlib, base64, requests
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).parent
state = json.loads((ROOT / "state.json").read_text())
mode = sys.argv[1]; who = sys.argv[2] if len(sys.argv) > 2 else None
login = {"redaktion": "redaktion@beispielthal.example", "lehrperson": "lehrperson@musterhausen.example"}.get(mode)
cb = {}
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        cb["url"] = "http://localhost:8000" + self.path; self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
    def log_message(self, *a): pass
srv = http.server.HTTPServer(("127.0.0.1", 8000), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
ver = secrets.token_urlsafe(48); ch = base64.urlsafe_b64encode(hashlib.sha256(ver.encode()).digest()).rstrip(b"=").decode()
url = "http://localhost:8090/oauth/v2/authorize?" + urllib.parse.urlencode({"client_id": state["oidc_app"]["client_id"],
      "redirect_uri": "http://localhost:8000/auth/callback", "response_type": "code",
      "scope": f"openid profile email urn:zitadel:iam:org:project:id:{state['project']}:aud", "code_challenge": ch, "code_challenge_method": "S256"})
tag = who or mode; n = [0]
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-proxy-server"]); pg = b.new_page(locale="de-CH")
    def shot(name):
        pg.screenshot(path=str(ROOT / f"v2-{tag}-{n[0]}-{name}.png")); n[0] += 1
    pg.goto(url); pg.wait_for_load_state("networkidle"); shot("start")
    if mode == "edulog":
        pg.locator("button:has-text('Edulog'), a:has-text('Edulog')").first.click(); pg.wait_for_load_state()
        pg.fill("input[name=username]", who); pg.fill("input[name=password]", "edulog-test"); pg.keyboard.press("Enter")
    else:
        pg.fill("input[name=loginName]", login); pg.keyboard.press("Enter"); pg.wait_for_load_state("networkidle")
        pg.wait_for_selector("input[type=password]", timeout=15000); shot("passwort")
        pg.fill("input[type=password]", "Poc-Test-2026!"); pg.keyboard.press("Enter")
    for _ in range(10):
        pg.wait_for_timeout(1500)
        if "url" in cb: break
        skip = pg.locator("button:has-text('Überspringen'), button:has-text('Skip'), button:has-text('überspringen')")
        if skip.count() > 0: shot("angebot"); skip.first.click()
    if "url" not in cb:
        shot("halt"); print(json.dumps({"ok": False, "seite": pg.url[:160], "text": pg.inner_text("body")[:300]}, ensure_ascii=False)); sys.exit(1)
    b.close()
code = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(cb["url"]).query))["code"]
s = requests.Session(); s.trust_env = False
tok = s.post("http://localhost:8090/oauth/v2/token", data={"grant_type": "authorization_code", "code": code,
      "redirect_uri": "http://localhost:8000/auth/callback", "code_verifier": ver},
      auth=(state["oidc_app"]["client_id"], state["oidc_app"]["client_secret"])).json()
part = tok["id_token"].split(".")[1]; c = json.loads(base64.urlsafe_b64decode(part + "=" * (-len(part) % 4)))
print(json.dumps({"ok": True, "name": c.get("name"), "eduksx_orgs": c.get("eduksx_orgs"), "eduksx_roles": c.get("eduksx_roles")}, ensure_ascii=False))
