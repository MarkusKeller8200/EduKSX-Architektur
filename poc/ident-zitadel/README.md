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
| `edulog-mock/` | Edulog-Ersatz (SimpleSAMLphp-Testbild) mit Testkonten im Format des Leitfadens 1.2.1: Lehrperson, Schulleitung mit `##`, Schülerin, unbekannte Rolle | P5 |
| `edulog-mapping.js` | Zitadel-Action: Edulog-Attribute auf das Konto abbilden, `##` trennen, Metadaten `edulog_*`, kein Konto für Lernende und leere Rolle | P5 |
| `edulog_login.py` | Anmeldung über den Edulog-Ersatz bis zum Rücksprung ins Glossary | P5 |
| `proxy.conf` | nginx: eine Adresse (Port 8090) für Zitadel und Login V2, wie Traefik im Betrieb | P1 |
| `login_v2.py` | Anmeldung über Login V2 mit Passwort oder Edulog | P1, P5 |
| `bridge_intent.php` | Brücke für Login V2: Antwort von `RetrieveIdentityProviderIntent` (Actions v2) – Edulog-Attribute abbilden, Lernende abweisen | P5 |
| `branding.py` | EduKSX-Gestaltung für Login V2 über Einstellungen: Farben, Logo, Texte, keine Selbstregistrierung (Bilder in `bilder/`) | P1 |
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

Edulog-Ersatz starten (ACS für Login V1, Werte aus den SP-Metadaten von Zitadel):

```bash
docker run -d --name edulog-mock -p 8081:8080 \
  -e SIMPLESAMLPHP_SP_ENTITY_ID="http://localhost:8080/idps/<idp-id>/saml/metadata" \
  -e SIMPLESAMLPHP_SP_ASSERTION_CONSUMER_SERVICE="http://localhost:8080/ui/login/login/externalidp/saml/acs" \
  -v $PWD/edulog-mock/authsources.php:/var/www/simplesamlphp/config/authsources.php:ro \
  -v $PWD/edulog-mock/saml20-idp-hosted.php:/var/www/simplesamlphp/metadata/saml20-idp-hosted.php:ro \
  kristophjunge/test-saml-idp:1.15
```

Login V2 (eigener Container, braucht ein Dienstkonto mit `IAM_LOGIN_CLIENT` und dessen Token):

```bash
docker run -d --name poc-proxy --network host -v $PWD/proxy.conf:/etc/nginx/conf.d/default.conf:ro nginx:1.29-alpine
docker run -d --name zitadel-login --network host -e HOSTNAME=0.0.0.0 -e ZITADEL_API_URL=http://localhost:8080 \
  -e NEXT_PUBLIC_BASE_PATH=/ui/v2/login -e ZITADEL_SERVICE_USER_TOKEN="$(cat pat/login-client.pat)" \
  -e CUSTOM_REQUEST_HEADERS="Host:localhost:8090" ghcr.io/zitadel/zitadel-login:v4.20.3
```
