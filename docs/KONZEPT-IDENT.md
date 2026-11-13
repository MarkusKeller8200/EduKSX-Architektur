# Konzept: EduKSX-Ident mit Zitadel und Proof of Concept (#25)

Stand: 13.11.2026 (Meilenstein 0.2.0) · Verantwortlich: Markus Keller · Status: **BESCHLOSSEN als Drehbuch** (#25, 13.11.2026) –
I2–I11 bleiben Empfehlungen bzw. Prüfpunkte, bis der Proof of Concept (#36) sie bestätigt.

Konkretisiert [Plattform 4.1, §5 S1–S4, S7 und §9.1](KONZEPT-PLATTFORM.md). Modulschlüssel `ident` laut
[Modulregister](REGISTER-MODULE.md). Schemas der Schnittstellen: [spec/](../spec/README.md).

**Verbindlichkeit:** Stufen nach [KONZEPT-VORLAGE.md](KONZEPT-VORLAGE.md). Recherche-Ergebnisse (Stand 13.11.2026) sind
als ZU PRÜFEN markiert, bis der PoC sie bestätigt.

## 1. Ziel

Ident ist die einzige Stelle für Anmeldung, zweiten Faktor, Konten, Organisationen und Rollen je Modul. Basis ist
**Zitadel** (BESCHLOSSEN 13.11.2026, vorbehaltlich PoC; Plan B Keycloak). Dieses Konzept legt fest, wie Ident aus Zitadel
und einer schlanken eigenen Brücke entsteht, und beschreibt den PoC so, dass er ohne weitere Klärung durchgeführt
werden kann.

**Nichtziele:**
- kein eigener Identity-Provider, keine Änderungen am Quellcode von Zitadel
- keine Zitadel-Eigenheiten in den Modulen – Module sprechen nur OIDC (S1), OAuth2 (S2), SCIM (S3) und S4-Ereignisse
- keine echten Personendaten im PoC; keine Anbindung produktiver Edulog-Identitäten vor Vertrag und Datenschutzprüfung

## 2. Aufbau

```text
 Edulog (SAML 2.0) ─┐   Entra ID / Google (OIDC) ─┐
                    ▼                              ▼
        ┌────────────────────────────────────────────────┐
        │ Zitadel (unverändert, AGPL)  + Login V2         │  OIDC/OAuth2 (S1, S2) ──► Module
        │ Organisationen · Projekte je Modul · Rollen      │
        │ Actions v2 ──(ZITADEL-Signature)──┐              │
        └───────────────────────────────────┼─────────────┘
                     ▲ API                   ▼
        ┌────────────┴───────────────────────────────────┐
        │ Ident-Brücke (Laravel, Modul `ident`)           │  S4 Ereignisse (EduKSX-Signature) ──► Module
        │ Rollen aus Edulog · Claims eduksx_* · Portal     │  S3 SCIM ──► isolierte Instanzen
        │ Einladungen · S7 /api/v1/me/modules              │  S7 ──► Kopfzeile der Module
        └────────────────────────────────────────────────┘
```

- **Zitadel** führt Konten, Organisationen, Anmeldung, MFA und die OIDC-Endpunkte. Je Modul ein **Projekt** mit den
  Rollen aus dem Steckbrief des Moduls (`roles`, S5); Organisationen erhalten Zugriff über Projekt-Grants.
- **Ident-Brücke** ist eine kleine Laravel-Anwendung (nutzt `eduksx/core`). Sie spricht Zitadel nur über dessen API und
  über Actions v2, übersetzt Zitadel-Ereignisse in S4-Ereignisse und ist die Stelle, an der Plattform-Regeln leben
  (Rollen-Abbildung, Einladungen, Freigaben). Fällt Zitadel weg, wird nur die Brücke angepasst.
- **Claims** `eduksx_orgs` und `eduksx_roles` (S1, [Schema](../spec/v1/oidc-claims.schema.json)) setzt eine
  Action vor der Ausgabe von Token und Userinfo, die die Brücke aufruft.

### 2.1 Anmeldung über Edulog

Edulog ist eine Föderation nach SAML 2.0; ein Dienstleistungsanbieter erhält höchstens 13 festgelegte Attribute, darunter
`EdulogPersonRole`, `EdulogPersonTechID` (stabile Kennung, NameID), `o` (Institution), `EdulogPersonCanton`,
`EdulogPersonLevel`, `EdulogPersonCycle` und `EdulogPersonAgeCategory`. Welche davon ein Dienst erhält, regelt der
Föderationsvertrag mit der Geschäftsstelle Edulog je Zweck.

| Edulog | Ident | Regel |
| --- | --- | --- |
| `EdulogPersonTechID` | externe Kennung des Kontos | stabil; nie `mail` als Schlüssel |
| `givenName`, `sn`, `mail`, `preferredLanguage` | Profil | nur wenn vertraglich freigegeben |
| `o`, `EdulogPersonCanton` | Vorschlag Organisation | Zuordnung bestätigt ein:e Organisations-Admin (keine automatische Aufnahme) |
| `EdulogPersonRole` = `principal`, `administration` | Vorschlag Org-Rolle `admin` | erst nach Bestätigung |
| `EdulogPersonRole` = `teacher`, `technician` | Org-Rolle `member` | Modulrollen vergibt die Organisation |
| `EdulogPersonRole` = `pupil`, `legal_guardian`, `other`, leer | kein Zugang | bis ein Modul für diese Gruppe freigegeben ist (Datenschutz, Minderjährige) |

**Formate nach dem Leitfaden für Identitätsanbieter** (Edulog, Version 1.2.1 vom 10.09.2020) – gelten für das, was
Ident von Edulog erhält, und für die Testkonten im PoC (P5):

| Attribut | Werte | Regel für Ident |
| --- | --- | --- |
| alle | SAML-Profil «basic», Namen mit genauer Gross- und Kleinschreibung | Abbildung in Zitadel exakt auf diese Namen |
| mehrwertige (`EdulogPersonRole`, `o`, `EdulogPersonLevel`, `EdulogPersonCycle`) | je Wert ein `AttributeValue` **oder** ein Wert mit `##` getrennt (z. B. Entra: `teacher##principal`) | die Brücke liest beide Formen und trennt an `##` |
| `EdulogPersonTechID` | von der Föderation erzeugt, bis 36 Zeichen (UUID-Form), nie leer, nie geändert | einziger Schlüssel des externen Kontos |
| `uid` | Kennung im Kantons-IdP, kann einer E-Mail-Adresse gleichen; ändert sich bei Neu-Föderation | nie als Schlüssel; höchstens zur Anzeige |
| `EdulogPersonRole` | `pupil`, `teacher`, `administration`, `principal`, `legal_guardian`, `technician`, `other`, leer; `pupil`, `legal_guardian`, `other` und leer stehen allein; `administration` und `principal` schliessen sich aus | wie Tabelle oben; leer = unbekannt = kein Zugang |
| `o` | Name(n) der Institution, oft Kürzel, bei Lehrpersonen häufig mehrere | ein Vorschlag je Wert; Abgleich über Namen **und** Kürzel der Organisation (Alias-Liste in Ident) |
| `EdulogPersonCanton` | Kürzel nach Art. 84 VZV, dazu `FL` (Liechtenstein) und `XX` (Ausland), leer | Hilfe beim Abgleich der Organisation |
| `preferredLanguage` | `de-CH`, `fr-CH`, `it-CH`, `rm-CH`, `en`; fehlt er, setzt die Föderation die Kantonssprache | Vorgabe für `locale`; Sprachen ohne Übersetzung fallen auf `de-CH` zurück |
| `EdulogPersonLevel` | `primary`, `secondary1`, `secondary2`, `tertiary`, leer | nur Information für Module, kein Recht |
| `EdulogPersonCycle` | `0` (nicht zutreffend), `1`–`3`, leer | nur Information für Module, kein Recht |
| `title` | frei gewählte Funktion, nur Nicht-Lernende | nicht anfordern (frei, kantonal verschieden) |
| `EdulogPersonBirthDate` | `JJJJMMTT`; an Dienste geht statt dessen die Altersklasse; fehlt sie bei Lernenden, gilt die jüngste Altersklasse | nicht anfordern; Minderjährige sind über `pupil` ohnehin ausgeschlossen |

**Umgebungen:** Edulog betreibt eine Integrationsumgebung (`go.int.edulog.ch`) getrennt von der Produktion
(`go.edulog.ch`); die Integration kann jederzeit neue Versionen erhalten und Daten löschen. Ident wird zuerst dort als
Dienstleistungsanbieter angeschlossen (dev), Produktion erst nach dem Go (Edulog-API-Referenz 1.4, 17.01.2022).

### 2.3 Sicherheitsanforderungen von Edulog an Ident

Nach «Sicherheitsanforderungen für IdP und SP für die Integration in Edulog» (Version 1.2, 5.2023) prüft die
Geschäftsstelle vor dem Anschluss. Abgleich mit dem PoC (Zitadel v4.20.3 als Dienstleistungsanbieter, Stand 13.11.2026):

| Anforderung | Edulog | Ident / Zitadel | Massnahme |
| --- | --- | --- | --- |
| TLS | nur TLS 1.2/1.3, Mozilla «Intermediate» | Sache des vorgeschalteten Proxys (Caddy nach MarKusSX-Operation) | Proxy so konfigurieren |
| Website-Zertifikat | kommerzielle CA, CN und SAN = FQDN, höchstens 2 Jahre, möglichst kein Wildcard | Proxy | ZU PRÜFEN: genügt Let's Encrypt? |
| Sicherheitskopfzeilen | CSP, X-Frame-Options, nosniff, HSTS, Permissions-Policy, Referrer-Policy, `X-Powered-By` entfernen; zusätzlich `X-XSS-Protection` empfohlen | Module über `eduksx/core`; Login-Seiten über den Proxy | `X-XSS-Protection` gilt heute als überholt (OWASP) – nur setzen, falls die Prüfung es verlangt |
| SAML: AuthnRequest signiert | Pflicht | `AuthnRequestsSigned="true"`, SHA-256 | erfüllt |
| SAML: Signaturzertifikat | eigenes Zertifikat (nicht TLS), höchstens 3 Jahre, RSA 2048/3072, SHA-2, **CN und SAN = FQDN, kein Wildcard** | von Zitadel je Anbieter erzeugt: RSA 4096, rund 1 Jahr, **CN «ZITADEL SP <id>»** (kein FQDN) | **Abweichung** – mit der Geschäftsstelle klären oder OIDC nutzen (I13) |
| SAML: Metadaten | `Extensions` mit zulässigen Digest- und Signaturverfahren; nur HTTP-POST und HTTP-Redirect | ohne `Extensions`; ACS zusätzlich mit HTTP-Artifact | Metadaten für Edulog von Hand ergänzen bzw. kürzen (werden ohnehin per Datei ausgetauscht) |
| OIDC (seit 1.2) | etablierte, zertifizierte Software statt Eigenbau | Zitadel als Client | erfüllt, falls Edulog OIDC für Dienstleistungsanbieter anbietet |

### 2.2 Ereignisse

Zitadel signiert Aufrufe aus Actions v2 mit der Kopfzeile `ZITADEL-Signature` (HMAC über Inhalt und Zeitstempel). Die
Brücke prüft diese Signatur, schreibt das Ereignis in ihre Ausgangswarteschlange und stellt es den Modulen als
CloudEvent mit `EduKSX-Signature` zu ([event.schema.json](../spec/v1/event.schema.json)). Module sehen das
Zitadel-Format nie.

## 3. Entscheide

| Nr. | Frage | Optionen | Entscheid | Status |
|---|---|---|---|---|
| I1 | Identity-Provider | Zitadel / Keycloak | Zitadel, Plan B Keycloak | BESCHLOSSEN 13.11.2026 vorbehaltlich PoC |
| I2 | Version | v3 / v4 | aktuelle Hauptversion 4 (Actions v2 und Login V2 dort Standard), genaue Version im Compose fixiert, Updates über Renovate | EMPFOHLEN |
| I3 | Anmeldeseite | Login V2 von Zitadel mit EduKSX-Gestaltung / eigene Seite über die Session-API | Login V2 mit Gestaltung; eigene Seite erst bei Bedarf | EMPFOHLEN |
| I4 | Eigene Logik | in Zitadel (Actions) / in einer Brücke | Ident-Brücke als Laravel-App (Modul `ident`), Actions nur als Aufruf der Brücke | EMPFOHLEN |
| I5 | Mandanten | eine Instanz mit Organisationen / Instanz je Kunde | eine Instanz, Organisation = Kunde; eigene Instanz nur auf Wunsch bzw. bei «besonders schützenswert» | BESCHLOSSEN 13.11.2026 (Plattform §9.2) |
| I6 | Anschluss Edulog | je Modul / einmal für die Plattform | einmal: Ident ist der Dienstleistungsanbieter gegenüber Edulog | EMPFOHLEN; Vertrag ZU PRÜFEN |
| I7 | Rollen aus Edulog | automatisch / Vorschlag mit Bestätigung | Vorschlag, Bestätigung durch Organisations-Admin (2.1) | EMPFOHLEN |
| I8 | Konten in isolierte Instanzen (S3) | SCIM aus Zitadel / SCIM aus der Brücke / nur beim ersten Login | ZU PRÜFEN im PoC, ob Zitadel SCIM an Anwendungen ausliefert; sonst sendet die Brücke SCIM, ausgelöst durch Ereignisse | ZU PRÜFEN |
| I9 | An den Absender gebundene Tokens (#16) | DPoP / mTLS / keine | siehe [Prüfauftrag DPoP/mTLS](PRUEFAUFTRAG-DPOP-MTLS.md) | ZU PRÜFEN |
| I10 | Lizenz AGPL-3.0 | unverändert betreiben / ändern | unverändert betreiben; eigene Teile (Brücke, Portal, Gestaltung) nur über API und Konfiguration – nach Auslegung von Zitadel löst das keine Pflicht zur Offenlegung aus; Restrisiko akzeptiert, Rückfall: Komponente ersetzen | BESCHLOSSEN 13.11.2026 |
| I12 | Edulog-API (Föderieren von Identitäten) | Ident nur als Dienstleistungsanbieter / zusätzlich als Identitätsanbieter gegenüber Edulog | nur Dienstleistungsanbieter: Die Edulog-API (Version 1.4) richtet sich an Identitätsanbieter und verlangt je Person die AHV-Nummer (AHVN13); deren systematische Verwendung braucht eine gesetzliche Grundlage und wäre «besonders schützenswert». Konten bringen die Kantone bzw. Schulen über ihren eigenen Identitätsanbieter | BESCHLOSSEN 13.11.2026 |
| I13 | Protokoll zwischen Edulog und Ident | SAML 2.0 / OpenID Connect | OpenID Connect, falls Edulog es Dienstleistungsanbietern anbietet (seit Sicherheitsanforderungen 1.2 vorgesehen): vermeidet die Abweichungen beim SAML-Signaturzertifikat (2.3); sonst SAML mit von Hand ergänzten Metadaten und geklärtem Zertifikat | EMPFOHLEN; bei der Geschäftsstelle ZU PRÜFEN |
| I14 | Wo Edulog-Konten und Schulzugehörigkeit leben | Konto in der Organisation der Schule / ein Plattform-Bereich, Zugehörigkeit in der Brücke | PoC: Konten aus Edulog entstehen in der Organisation des Anmeldekontexts (Plattform); Zitadel kann Konten nicht verschieben, und eine Lehrperson gehört oft mehreren Schulen. Daher Konten im Plattform-Bereich, Schulzugehörigkeit und Bestätigung in der Brücke (Quelle für `eduksx_orgs`); Zitadel nur für Anmeldung. Abbildung der Attribute mit Login V2 in der Brücke (Actions v2, im PoC bestätigt); das JavaScript für Login V1 entfällt | BESCHLOSSEN 13.11.2026 |
| I11 | Sicherung | Datenbank allein / mit Masterkey | PostgreSQL-Sicherung **und** Masterkey (getrennt im Geheimnisspeicher); ohne Masterkey ist die Sicherung wertlos | EMPFOHLEN |

## 4. Proof of Concept (#25)

**Rahmen:** lokal bzw. auf einem Test-Server mit Docker Compose; nur erfundene Konten (`…@schule-beispiel.example`);
Zeitbedarf geschätzt 3–5 Arbeitstage ohne Wartezeit auf Edulog. Ergebnis je Schritt in §4.3 eintragen.

### 4.1 Schritte

| # | Schritt | Abnahme | Testliste #25 |
|---|---|---|---|
| P1 | 13.11.2026 | **bestanden** (bis auf Admin-MFA) | Compose mit fixierter v4.20.3 und PostgreSQL (je ~80 MB RAM, Image 237 MB); Masterkey aus Datei. **Login V2** (Container `zitadel-login` v4.20.3) läuft hinter einem Proxy unter **derselben Adresse** wie die API – getrennte Ports scheitern bei SAML (Zitadel nennt Edulog sonst die Adresse des Login-Containers). Login V2 braucht ein Dienstkonto mit `IAM_LOGIN_CLIENT` (Token als Geheimnis) und sollte `ZITADEL_SESSION_COOKIE_SECRET` erhalten. Offen: Admin mit MFA, EduKSX-Gestaltung |
| P2 | Organisation «Schule Beispiel», Projekt `glossary` mit Rollen aus dem Steckbrief, Client für das Glossary (Code + PKCE, vertraulich) | Grant für die Organisation vorhanden | – |
| P3 | Glossary meldet sich an (Glossary #185) und wieder ab (RP-initiated und Back-Channel-Logout, #187) | Anmelden/Abmelden ok; Back-Channel-Logout beendet die Sitzung im Glossary | «Anmeldung Glossary … inkl. Abmelden» |
| P4 | Action vor Token/Userinfo ruft die Brücke (Stub) und setzt `eduksx_orgs`, `eduksx_roles` (#186) | ID-Token besteht [oidc-claims.schema.json](../spec/v1/oidc-claims.schema.json) | – |
| P5 | 13.11.2026 | **mit Ersatz bestanden** | Edulog-Ersatz (SAML, Testkonten im Format des Leitfadens 1.2.1): signierte Anfrage, Binding **HTTP-Redirect** (POST scheiterte mit Login V1), NameID persistent = `EdulogPersonTechID` als externe Kennung; Abbildung über eine Zitadel-Action (`edulog-mapping.js`): Profil, Sprache (`fr-CH` → `fr`), Mehrfachwerte in beiden Formen (`##`), Metadaten `edulog_roles`/`edulog_orgs`; **kein Konto** für `pupil` und leere Rolle; ohne bestätigte Rolle kein Zugang (I7), nach Bestätigung Anmeldung mit `eduksx_roles`. Echter Anschluss offen (4.1a). Befunde siehe I14. **Mit Login V2:** Abbildung durch die Brücke über Actions v2 (Antwort von `RetrieveIdentityProviderIntent`, `bridge_intent.php`) statt Zitadel-JavaScript – bestehende und neue Konten, Lernende abgewiesen (I4 erfüllt). Login V2 zeigt fehlende Rollenbestätigung nur als «Unknown error occurred» → eigener Hinweistext nötig |
| P6 | Actions v2: Ereignis bei neuem Konto und bei Löschung an einen Laravel-Endpunkt; Signatur `ZITADEL-Signature` prüfen, falsche Signatur und alter Zeitstempel werden abgewiesen; Brücke sendet S4 an einen Test-Empfänger | Ereignis besteht [event.schema.json](../spec/v1/event.schema.json) und [signature.schema.json](../spec/v1/signature.schema.json) | «Webhook … signiert/geprüft» |
| P7 | Sicherung: `pg_dump` + Masterkey; Wiederherstellung in eine **leere** Umgebung; Anmeldung P3 erneut | Anmeldung nach Wiederherstellung ok, Dauer notiert (RTO) | «Sicherung und Wiederherstellung» |
| P8 | Prüfpunkte I8 (SCIM) und I9 (DPoP, `private_key_jwt`) gegen die laufende Version | Ergebnis in §4.3 | – |
| P9 | Lizenz: Auslegung I10 mit Fachperson bzw. schriftlicher Auskunft von Zitadel festhalten | Notiz mit Datum | «Lizenzfrage dokumentiert» |
| P10 | Ergebnis in Plattform §9.1 eintragen: Vorbehalt aufgehoben oder Plan B | Pull Request | «Ergebnis … nachgetragen» |

### 4.1a Fragen an die Geschäftsstelle Edulog (vorbereitet, noch nicht gestellt)

Entscheid 13.11.2026: Ident wird so weit wie möglich integriert und gegen einen Edulog-Ersatz getestet; die Fragen werden
gestellt, wenn der Anschluss ansteht.

1. Anschluss als Dienstleistungsanbieter zuerst an die Integrationsumgebung (`go.int.edulog.ch`)?
2. OpenID Connect für Dienstleistungsanbieter möglich (I13)? Kommen die Edulog-Attribute dann als Claims?
3. Falls nur SAML: Wird ein Signaturzertifikat ohne FQDN im CN (von Zitadel erzeugt) und mit RSA 4096 akzeptiert (2.3)?
4. Genügt ein Website-Zertifikat von Let's Encrypt?
5. Anforderungskatalog für Dienstleistungsanbieter und Föderationsvertrag (Ablauf, Fristen, Kosten).
6. Attribute (Datensparsamkeit): `EdulogPersonTechID`, `EdulogPersonRole`, `o`, `EdulogPersonCanton`, `givenName`, `sn`,
   `mail`, `preferredLanguage`; `EdulogPersonLevel` und `EdulogPersonCycle` nur bei Bedarf eines Moduls.

### 4.2 Abbruch und Plan B

Der PoC gilt als **nicht bestanden**, wenn eines davon eintritt; dann wird Keycloak mit denselben Schritten geprüft:
- Edulog-Attribute lassen sich nicht zuverlässig auf Organisation und Rolle abbilden (P5);
- Ereignisse für Konto-Änderung und -Löschung sind nicht zuverlässig oder nicht signiert erhältlich (P6);
- Wiederherstellung gelingt nicht ohne Handarbeit an der Datenbank (P7);
- die Lizenzauslegung verlangt die Offenlegung eigener Teile (P9).

Fehlt nur DPoP (P8), ist das **kein** Abbruchgrund; Entscheid im Prüfauftrag #16.

### 4.3 Ergebnisse

Durchgang 1 am 13.11.2026 in der Cloud-Umgebung von Claude (Docker, Zitadel v4.20.3, PostgreSQL 17), Werkzeuge in
[`poc/ident-zitadel/`](../poc/ident-zitadel/README.md). Ein OIDC-Client simuliert das Glossary; die Anbindung im
Glossary selbst (#185–#187) folgt.

| # | Datum | Ergebnis | Bemerkung |
|---|---|---|---|
| P1 | 13.11.2026 | **teilweise** | Compose mit fixierter v4.20.3 und PostgreSQL läuft (je ~80 MB RAM, Image 237 MB); Masterkey aus Datei. Offen: **Login V2** (eigener Container, im Durchgang Login V1), Admin mit MFA |
| P2 | 13.11.2026 | **bestanden** | zwei Organisationen (Schule, Schulgemeinde), Projekte `glossary` (Rollen reader/editor/admin) und `platform` (Super-Admin), Projekt-Grants an die Organisationen, vertraulicher Web-Client (Code + PKCE), Dienstkonto für S2 – alles per API (`setup.py`) |
| P3 | 13.11.2026 | **bestanden** (mit Test-Client) | Anmelden mit Code + PKCE; ID-/Access-Token als JWT, Prüfung in PHP ohne Zusatzpaket (`verify.php`: Signatur über JWKS, iss, aud, exp; verändertes Token abgelehnt). RP-initiiertes Abmelden und **Back-Channel-Logout** mit passender `sid`. Client Credentials für das Dienstkonto. Befund: Token-Laufzeit ab Werk 12 h → auf 15 Min. gesetzt (API C1) |
| P4 | 13.11.2026 | **bestanden** (Stub) | Actions v2 `preuserinfo`/`preaccesstoken` rufen die Brücke (`bridge.php`), die `eduksx_orgs` und `eduksx_roles` setzt; ID-Token besteht `oidc-claims.schema.json` bis auf `iss` mit http (nur lokal). Befund: Mit `interruptOnError` hängt jede Anmeldung an der Brücke → Brücke hochverfügbar betreiben oder Ausfallverhalten festlegen |
| P5 | – | offen | Kein direkter Zugang: Edulog ist eine SAML-Föderation, Anschluss über Föderationsvertrag mit der Geschäftsstelle (Educa) und deren Anforderungskatalog. Bis dahin MockSAML mit den Edulog-Attributnamen. Entscheid 13.11.2026: alles vorbereiten; auf dev ausliefern und testen, produktiv erst nach dem Go (Schalter je Umgebung) |
| P6 | 13.11.2026 | **teilweise** | Ereignisse `user.human.added` und `user.removed` kommen signiert an; falsche Signatur und über 5 Min. alter Zeitstempel werden abgewiesen. Offen: Empfänger in Laravel und Umsetzung in S4/CloudEvent (`event.schema.json`) in der Brücke. Befund: Zitadel sperrt Ziele im privaten Netz ab Werk (`ZITADEL_HTTPCLIENT_DENYLIST`) – im PoC gelockert, im Betrieb so lassen |
| P7 | 13.11.2026 | **bestanden** | `pg_dumpall` in eine leere Umgebung zurückgespielt: Zitadel nach **8 s** bereit, Anmeldung ok, Signaturschlüssel unverändert (ausgestellte Tokens bleiben gültig). Mit falschem Masterkey startet Zitadel, stellt aber keine Tokens aus → I11 bestätigt |
| P8 | 13.11.2026 | **festgehalten** | `private_key_jwt` angeboten; **DPoP nicht** angeboten (Discovery); SCIM nur als Server (eingehend), kein ausgehendes Provisioning an Anwendungen gefunden → I8: Brücke sendet SCIM |
| P9 | 13.11.2026 | **angenommen** | Entscheid Projektverantwortliche:r: Auslegung I10 gilt als positiv (unveränderter Betrieb, eigene Teile über API; Module ohnehin AGPL, Plattform §9.7). Restrisiko akzeptiert – im schlimmsten Fall wird Zitadel ersetzt (Plan B Keycloak); deshalb sprechen Module Ident nur über Standards an. Schriftliche Anfrage an Zitadel optional |
| P10 | – | offen | nach dem echten Edulog-Anschluss (Integrationsumgebung) |

Weitere Befunde: Zwei-Faktor-Pflicht lässt sich je Organisation per Richtlinie setzen (API angenommen; Wirkung im
Durchgang nicht abschliessend geprüft). Back-Channel-Logout-Adressen auf `localhost` lehnt Zitadel ab der
Sperrliste ab (Schutz vor SSRF). Bisher kein Abbruchgrund nach 4.2.

## 5. Issues

| Issue | Inhalt | Status |
|---|---|---|
| #25 | Konzept und Drehbuch | `_3 Beta-Test` |
| #36 (0.3.0) | Durchführung des PoC nach §4 | `triage` |
| #16, #35 | Prüfauftrag DPoP/mTLS (I9); Entscheid nach P8 in #35 | Empfehlung im Beta-Test, #35 `triage` |
| #3 | Schemas S1, S4, S5, S6 | `_3 Beta-Test` |
| Glossary #185–#189 | Anmeldung, Rollen, Logout/Ereignisse, Client Credentials, Steckbrief | `triage` |
| (folgt) | Repo EduKSX-Ident mit der Brücke | nach bestandenem PoC |
| (Projektverantwortliche:r) | Testzugang Edulog bei der Geschäftsstelle anfragen | offen |

## 6. Quellen (Stand 13.11.2026)

- Zitadel: Lizenzwechsel auf AGPL-3.0 und nur noch PostgreSQL ab v3 – <https://zitadel.com/blog/zitadel-v3-announcement>,
  Lizenz-FAQ <https://help.zitadel.com/zitadel-licensing-faqs>, Auslegung zur API-Nutzung <https://zitadel.com/blog/apache-to-agpl>
- Zitadel Actions v2 und Signatur – <https://zitadel.com/docs/guides/integrate/actions/usage>,
  Umstieg von v1 <https://zitadel.com/docs/guides/integrate/actions/migrate-from-v1>
- Zitadel mit SAML-Anbieter und Attribut-Abbildung – <https://zitadel.com/docs/guides/integrate/identity-providers/mocksaml>
- Edulog: Sicherheitsanforderungen für IdP und SP 1.2 (5.2023); Leitfaden Hybrid-Infrastruktur AD/Azure AD für IdP 1.0
  (22.3.2021) – beide von Projektverantwortliche:r bereitgestellt; API-Referenz 1.4 (ELCA, 17.01.2022, von Projektverantwortliche:r bereitgestellt) – Föderieren für
  Identitätsanbieter, Integrations- und Produktionsumgebung; Leitfaden zu den Attributen für Identitätsanbieter, Version 1.2.1 (10.09.2020, von Projektverantwortliche:r
  bereitgestellt); Attribute für Dienstleistungsanbieter – <https://www.edulog.ch/sites/default/files/2021-07/Leitfaden_Attribute_Dienstleistungsanbieter_0.pdf>,
  Datenschutz <https://www.edulog.ch/de/was-ist-edulog/umgang-mit-daten-und-datenschutz>
- Keycloak (Plan B): Organisationen ab 26.0 <https://www.keycloak.org/2024/10/keycloak-2600-released.html>, DPoP ab 26.4
  unterstützt <https://www.keycloak.org/2025/10/dpop-support-26-4>

## 7. Verlauf

- 13.11.2026: I12 und I14 beschlossen; weiter mit Gestaltung Login V2 und Brücke als Laravel-App.
- 13.11.2026: Login V2 hinter gemeinsamem Proxy getestet: Passwort und Edulog-Ersatz, Abbildung über die Brücke (Actions v2); P1 bestanden.
- 13.11.2026: P5 mit Edulog-Ersatz bestanden; I14 (Konten im Plattform-Bereich, Zugehörigkeit in der Brücke) empfohlen.
- 13.11.2026: Sicherheitsanforderungen Edulog 1.2 mit Zitadel abgeglichen (2.3): Signaturzertifikat und Metadaten weichen ab; I13 (OIDC bevorzugt) empfohlen.
- 13.11.2026: Edulog-API-Referenz 1.4 ausgewertet: Integrationsumgebung für dev; I12 (Ident nicht als Identitätsanbieter) empfohlen.
- 13.11.2026: Edulog-Formate nach dem Leitfaden für Identitätsanbieter 1.2.1 ergänzt (2.1).
- 13.11.2026: Edulog vorbereiten, auf dev testen, produktiv erst nach Go (Schalter je Umgebung).
- 13.11.2026: P9 als positiv angenommen, I10 beschlossen (Restrisiko akzeptiert, Rückfall: Komponente ersetzen).
- 13.11.2026: PoC Durchgang 1 (Cloud-Umgebung): P2, P3, P4, P7 bestanden, P1 und P6 teilweise, P8 festgehalten; offen P5, P9, P10 (#36).
- 13.11.2026: Als Drehbuch abgenommen; I2–I11 bleiben empfohlen, Durchführung in #36.
- 13.11.2026: Konzept und PoC-Drehbuch angelegt (Recherche Zitadel, Edulog, Keycloak).
