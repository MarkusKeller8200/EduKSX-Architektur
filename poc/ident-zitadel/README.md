# Proof of Concept: EduKSX-Ident mit Zitadel

Werkzeuge zum PoC nach [KONZEPT-IDENT.md](../../docs/KONZEPT-IDENT.md) §4 (#36). Nur lokal, nur erfundene Testdaten,
kein Betrieb. Ergebnisse stehen in KONZEPT-IDENT §4.3.

| Datei | Zweck | Schritt |
| --- | --- | --- |
| `docker-compose.yml` | Zitadel v4.20.3 und PostgreSQL 17; Masterkey aus `masterkey.txt` (nicht im Repository) | P1 |
| `setup.py` | Organisationen (Schulen), Projekte `glossary` und `platform` mit Rollen, Grants, Web-Client, Testkonten, Dienstkonto | P2 |
| `login.py` | Anmeldung im Browser (Code-Flow mit PKCE), Token tauschen, Claims zeigen; `--abmelden` für Abmelden | P3 |
| `logout_receiver.py` | Empfänger für Back-Channel-Logout (Port 8097) | P3 |
| `bridge.php` | Stub der Ident-Brücke: setzt `eduksx_orgs` und `eduksx_roles` vor Userinfo und Access-Token | P4 |
| `webhook.php` | Empfänger für Ereignisse aus Actions v2, prüft `ZITADEL-Signature` | P6 |
| `verify.php` | Prüft ein JWT ohne Zusatzpaket (JWKS, RS256, iss, aud, exp) – Vorlage für `eduksx/core` | P3 |

Ablauf (Python 3 mit `requests` und `playwright`, PHP 8.4, Docker):

```bash
head -c 24 /dev/urandom | base64 | head -c 32 > masterkey.txt
mkdir -m 777 pat && docker compose up -d          # Admin-Token entsteht in pat/admin.pat
python3 setup.py                                    # schreibt state.json (Zugangsdaten, nicht ins Repository)
python3 login.py lehrperson && python3 login.py redaktion --abmelden
php verify.php tokens-redaktion.json "$(python3 -c "import json;print(json.load(open('state.json'))['project'])")"
```

Für Actions v2 erlaubt die Compose-Datei Ziele im lokalen Netz (`ZITADEL_HTTPCLIENT_DENYLIST`). Im Betrieb bleibt die
Standard-Sperrliste (private Adressen gesperrt) aktiv.
