#!/usr/bin/env python3
"""PoC Ident (#25): Anmeldung im Browser mit OIDC-Code-Flow und PKCE, danach Token tauschen und Claims prüfen.

Aufruf: python3 login.py [lehrperson|redaktion]   – braucht state.json aus setup.py.
"""

import base64
import hashlib
import http.server
import json
import pathlib
import secrets
import sys
import threading
import urllib.parse

import requests
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8080"
ROOT = pathlib.Path(__file__).parent
state = json.loads((ROOT / "state.json").read_text())
who = sys.argv[1] if len(sys.argv) > 1 else "lehrperson"
login = {"lehrperson": "lehrperson@musterhausen.example", "redaktion": "redaktion@beispielthal.example"}[who]
client_id = state["oidc_app"]["client_id"]
redirect = "http://localhost:8000/auth/callback"

verifier = secrets.token_urlsafe(48)
challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
st = secrets.token_urlsafe(16)
scope = " ".join([
    "openid", "profile", "email", "offline_access",
    f"urn:zitadel:iam:org:project:id:{state['project']}:aud",  # Token für das Projekt glossary
    "urn:zitadel:iam:user:resourceowner",                         # Organisation (Mandant) im Token
])
auth_url = f"{BASE}/oauth/v2/authorize?" + urllib.parse.urlencode({
    "client_id": client_id, "redirect_uri": redirect, "response_type": "code", "scope": scope,
    "state": st, "code_challenge": challenge, "code_challenge_method": "S256",
})

callback = {}


class Callback(http.server.BaseHTTPRequestHandler):
    # Rücksprungadresse des Glossary (localhost:8000) – nimmt nur den Code entgegen
    def do_GET(self):
        callback["url"] = "http://localhost:8000" + self.path
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, *args):
        pass


server = http.server.HTTPServer(("127.0.0.1", 8000), Callback)
threading.Thread(target=server.serve_forever, daemon=True).start()

with sync_playwright() as p:
    browser = p.chromium.launch(args=["--no-proxy-server"])
    page = browser.new_page()

    page.goto(auth_url)
    page.fill("#loginName", login)
    page.click("#submit-button")
    page.fill("#password", "Poc-Test-2026!")
    page.click("#submit-button")
    # Zweiter Faktor einrichten: im PoC überspringen (Richtlinie MFA folgt im Bericht)
    for _ in range(3):
        if "url" in callback:
            break
        skip = page.locator("button:has-text('überspringen'), button:has-text('skip'), #mfa-init-skip, [name='skip']")
        if skip.count() > 0:
            skip.first.click()
        page.wait_for_timeout(1500)
    if "url" not in callback:
        page.screenshot(path=str(ROOT / "login-fehler.png"))
        sys.exit("Kein Rücksprung – siehe login-fehler.png, Seite: " + page.url)
    q = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(callback["url"]).query))
    assert q.get("state") == st, "state stimmt nicht"
    s = requests.Session()
    s.trust_env = False
    tok = s.post(f"{BASE}/oauth/v2/token", data={
        "grant_type": "authorization_code", "code": q["code"], "redirect_uri": redirect, "code_verifier": verifier,
    }, auth=(client_id, state["oidc_app"]["client_secret"])).json()


    def claims(jwt: str) -> dict:
        part = jwt.split(".")[1]
        return json.loads(base64.urlsafe_b64decode(part + "=" * (-len(part) % 4)))


    idc = claims(tok["id_token"])
    acc = claims(tok["access_token"])
    out = {
        "anmeldung": who,
        "sid": idc.get("sid"),
        "id_token": {k: idc.get(k) for k in ["iss", "sub", "aud", "email", "preferred_username", "locale",
                                              "urn:zitadel:iam:user:resourceowner:id",
                                              "urn:zitadel:iam:user:resourceowner:name",
                                              f"urn:zitadel:iam:org:project:{state['project']}:roles"]},
        "access_token_jwt": {"aud": acc.get("aud"), "exp_minus_iat_s": acc["exp"] - acc["iat"],
                             "roles": acc.get(f"urn:zitadel:iam:org:project:{state['project']}:roles")},
        "refresh_token": "refresh_token" in tok,
    }
    (ROOT / f"tokens-{who}.json").write_text(json.dumps({"id_token": tok["id_token"], "access_token": tok["access_token"]}))
    print(json.dumps(out, indent=2, ensure_ascii=False))
    if "--abmelden" in sys.argv:
        # RP-initiiertes Abmelden (P3); Zitadel benachrichtigt das Glossary per Back-Channel-Logout
        page.goto(f"{BASE}/oidc/v1/end_session?" + urllib.parse.urlencode({
            "id_token_hint": tok["id_token"], "post_logout_redirect_uri": "http://localhost:8000/", "state": "abgemeldet",
        }))
        page.wait_for_timeout(4000)
        lt = ROOT / "logout-token.txt"
        if lt.exists():
            lc = claims(lt.read_text())
            print("Back-Channel-Logout:", json.dumps({"sub": lc.get("sub"), "sid": lc.get("sid"),
                  "events": list(lc.get("events", {}).keys()), "sid_wie_id_token": lc.get("sid") == idc.get("sid")}))
        else:
            print("Back-Channel-Logout: nicht empfangen")
        print("Rücksprung nach Abmelden:", callback.get("url"))
    browser.close()
