#!/usr/bin/env python3
"""PoC (#36): EduKSX-Gestaltung für Login V2 – nur über Einstellungen und API, Zitadel bleibt unverändert (I10).
Farben aus dem EduKSX-Icon-Set (Orange #FF8A00, Neutral #222222 / #F2F5F8), Logo und Icon aus
EduKSX-UI icons/png (eduksx-tile-light/-dark; einzige Quelle des Icon-Sets, auch im Paket @eduksx/ui). Aufruf: python3 branding.py <png-ordner>
"""
import pathlib, sys, requests

BASE, HOST = "http://localhost:8080", "localhost:8090"
ROOT = pathlib.Path(__file__).parent
s = requests.Session(); s.trust_env = False
s.headers.update({"Authorization": "Bearer " + (ROOT / "pat" / "admin.pat").read_text().strip(), "Host": HOST})
json_h = {"Content-Type": "application/json"}

# Farben, kein Zitadel-Wasserzeichen, Hell/Dunkel nach System
s.put(f"{BASE}/admin/v1/policies/label", headers=json_h, json={
    "primaryColor": "#FF8A00", "backgroundColor": "#FFFFFF", "warnColor": "#C62828", "fontColor": "#222222",
    "primaryColorDark": "#FF8A00", "backgroundColorDark": "#1B1F24", "warnColorDark": "#FF6B6B", "fontColorDark": "#F2F5F8",
    "hideLoginNameSuffix": True, "disableWatermark": True, "themeMode": "THEME_MODE_AUTO"}).raise_for_status()
png = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None
if png:
    for ep, f in [("logo", "512/eduksx-tile-light.png"), ("logo/dark", "512/eduksx-tile-dark.png"),
                  ("icon", "192/eduksx-tile-light.png"), ("icon/dark", "192/eduksx-tile-dark.png")]:
        p = png / f if (png / f).exists() else png / "512" / pathlib.Path(f).name
        s.post(f"{BASE}/assets/v1/instance/policy/label/{ep}", files={"file": p.open("rb")}).raise_for_status()
s.post(f"{BASE}/admin/v1/policies/label/_activate", headers=json_h, json={}).raise_for_status()

# Keine Selbstregistrierung: Konten kommen über Edulog oder Einladung
lp = s.get(f"{BASE}/admin/v1/policies/login").json()["policy"]
lp = {k: v for k, v in lp.items() if k not in ("details", "isDefault", "idps", "secondFactors", "multiFactors")}
lp["allowRegister"] = False
s.put(f"{BASE}/admin/v1/policies/login", headers=json_h, json=lp).raise_for_status()

# Eigene Texte (Login V2), je Sprache
texte = {"de": {"loginname": {"title": "Anmelden bei EduKSX",
                              "description": "Mit Ihrem Schulkonto über Edulog oder mit Ihrem EduKSX-Login."}}}
for loc, t in texte.items():
    s.put(f"{BASE}/v2/settings/hosted_login_translation", headers=json_h,
          json={"instance": True, "locale": loc, "translations": t}).raise_for_status()
print("Gestaltung gesetzt; Login-Container neu starten, damit er die Einstellungen neu lädt.")
