#!/usr/bin/env python3
"""PoC P5: Anmeldung über den Edulog-Ersatz (SAML) bis zum Rücksprung ins Glossary. Aufruf: python3 edulog_login.py lehrperson"""
import json, pathlib, sys, http.server, threading, urllib.parse, secrets, hashlib, base64
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).parent
state = json.loads((ROOT / "state.json").read_text())
who = sys.argv[1] if len(sys.argv) > 1 else "lehrperson"
cb = {}
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        cb["url"] = "http://localhost:8000" + self.path; self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
    def log_message(self, *a): pass
srv = http.server.HTTPServer(("127.0.0.1", 8000), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
verifier = secrets.token_urlsafe(48)
challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
url = "http://localhost:8080/oauth/v2/authorize?" + urllib.parse.urlencode({
    "client_id": state["oidc_app"]["client_id"], "redirect_uri": "http://localhost:8000/auth/callback",
    "response_type": "code", "scope": f"openid profile email urn:zitadel:iam:org:project:id:{state['project']}:aud",
    "code_challenge": challenge, "code_challenge_method": "S256"})
shots = []
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-proxy-server"]); pg = b.new_page()
    def shot(name):
        f = ROOT / f"edulog-{who}-{len(shots)}-{name}.png"; pg.screenshot(path=str(f)); shots.append(f.name)
    pg.goto(url); pg.wait_for_load_state()
    pg.locator("a.lgn-idp:has-text('Edulog')").first.click(); pg.wait_for_load_state()
    pg.fill("input[name=username]", who); pg.fill("input[name=password]", "edulog-test")
    pg.keyboard.press("Enter"); pg.wait_for_load_state()
    for i in range(6):
        if "url" in cb: break
        pg.wait_for_timeout(1500)
        skip = pg.locator("button:has-text('Skip'), button:has-text('überspringen'), [name=skip]")
        if "mfa/prompt" in pg.url and skip.count() > 0:
            shot("mfa-angebot"); skip.first.click(); pg.wait_for_load_state(); continue
        btn = pg.locator("#submit-button, button[type=submit]:not([disabled])")
        if "url" not in cb and btn.count() > 0 and "localhost:8080" in pg.url:
            shot("zwischenschritt"); btn.first.click(); pg.wait_for_load_state()
    if "url" not in cb:
        shot("fehler"); print(json.dumps({"ok": False, "seite": pg.url, "bilder": shots})); sys.exit(1)
    b.close()
code = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(cb["url"]).query))["code"]
import requests
s = requests.Session(); s.trust_env = False
tok = s.post("http://localhost:8080/oauth/v2/token", data={"grant_type": "authorization_code", "code": code,
      "redirect_uri": "http://localhost:8000/auth/callback", "code_verifier": verifier},
      auth=(state["oidc_app"]["client_id"], state["oidc_app"]["client_secret"])).json()
part = tok["id_token"].split(".")[1]; c = json.loads(base64.urlsafe_b64decode(part + "=" * (-len(part) % 4)))
print(json.dumps({"ok": True, "sub": c["sub"], "name": c.get("name"), "email": c.get("email"), "locale": c.get("locale"),
      "eduksx_orgs": c.get("eduksx_orgs"), "eduksx_roles": c.get("eduksx_roles"), "zwischenschritte": shots}, ensure_ascii=False, indent=1))
