# Konzept: EduKSX-Plattform – Architektur, Schnittstellen, Betrieb

Stand: Entwurf 08.11.2026 zur Abnahme durch Projektverantwortliche:r. Grundlage: Gespräche zum EduKSX-Glossary
(Organisationen, Einbindung, Updates). Nichts davon ist umgesetzt; Mengen und Preise sind Schätzungen.

## 1. Zweck

Mehrere Anwendungen für Schulen, Schulgemeinden und Gemeinden – heute das **Glossary**, später z. B.
**Rechtssammlung**, **Intranet**, **Stundenplan** – teilen Anmeldung, Konten, Organisationen, Gestaltung und Betrieb.
Dieses Papier legt fest:

- die **Bausteine** der Plattform und ihre Aufgaben,
- die **Schnittstellen** zwischen ihnen (verbindlich für alle Module),
- die **Anforderungen** an jeden weiteren Dienst,
- **Infrastruktur, Updates und Skalierung** in Stufen.

## 2. Begriffe

| Begriff | Bedeutung |
| --- | --- |
| Plattform | Gesamtheit aus Ident, Modulen, gemeinsamem Unterbau und Leitstand |
| Modul | eigenständige Anwendung mit eigenem Repository, Image und eigener Version (Glossary, Rechtssammlung …) |
| Organisation (Mandant) | Schule, Schulgemeinde, Gemeinde oder Team; Kunde der Plattform |
| Zentraler Dienst | eine Instanz für alle Organisationen; Trennung logisch über die Organisation |
| Isolierte Instanz | eigene Instanz je Organisation mit eigener Datenbank, Dateien, Sicherungen und Schlüsseln |
| Leitstand | interne Steuerung: Kunden, Module je Kunde, Versionen, Updates, Zustand |

## 3. Übersicht

```text
                  ┌──────────────────────────────────────────────┐
                  │ EduKSX-Ident  ident.eduksx.ch                │
                  │ Login · MFA · Konten · Organisationen ·      │
                  │ Rollen je Modul · Brücken (Edulog, Entra) ·  │
                  │ OIDC/OAuth2 · SCIM · Ereignisse              │
                  └──────────────────────┬───────────────────────┘
                                         │ S1 Anmeldung · S2 Dienst-Token · S3 Konten · S4 Ereignisse
      ┌──────────────────────────────────┼─────────────────────────────────────┐
┌─────┴──────────────┐  ┌────────────────┴───┐                 ┌───────────────┴──────────────┐
│ Glossary (zentral) │  │ Rechtssammlung     │                 │ Intranet, Stundenplan …      │
│ öffentlich lesbar  │  │ (zentral, öffentl.)│                 │ isolierte Instanz je Kunde   │
└─────────┬──────────┘  └─────────┬──────────┘                 └───────────────┬──────────────┘
          └──── gemeinsamer Unterbau «eduksx/core» (Paket, kein Dienst) ────────┘
                                         │ S5 Steckbrief/Zustand · S6 Heartbeat/Aufträge
                  ┌──────────────────────┴───────────────────────┐
                  │ Leitstand (intern): Kunden, Module, Versionen,│
                  │ Update-Ringe, Wartungsfenster, Zustand        │
                  └──────────────────────────────────────────────┘
```

## 4. Bausteine

### 4.1 EduKSX-Ident

- **Aufgabe:** einzige Stelle für Anmeldung, zweiten Faktor, Konten, Organisationen, Mitgliedschaften und Rollen je
  Modul; Einladungen und Freigaben in einem eigenen Portal im EduKSX-Design.
- **Nicht selbst schreiben:** Basis ist ein bewährter Identity-Provider (Kandidaten: Keycloak, Zitadel – Auswahl
  mit Bewertung von Lizenz, Mandantenfähigkeit, Betrieb, Updates). Darum ein dünnes Portal.
- **Brücken:** Edulog, Microsoft Entra ID, Google Workspace als vorgeschaltete Anmeldedienste; MFA zentral.
- **Datenminimierung:** Ident hält Identität (Name, E-Mail, Mitgliedschaften, Rollen), nie Inhalte der Module.
- **Trennung bei strengen Kunden:** eigener Bereich (Realm/Instanz) je Kunde oder direkte Anbindung an das Entra der
  Gemeinde. Für Module unsichtbar – sie sprechen nur OIDC.

### 4.2 Module

| Betriebsart | Beispiele | Instanzen | Datenbank | Öffentlich |
| --- | --- | --- | --- | --- |
| zentral | Glossary, Rechtssammlung | eine für alle | PostgreSQL | Lesen ohne Login |
| isoliert | Intranet, Stundenplan | je Kunde | SQLite (klein) bzw. PostgreSQL | nie |

Gleicher Quellcode und gleiches Image für alle Kunden; Unterschiede nur über Konfiguration und Einstellungen.

### 4.3 Gemeinsamer Unterbau «eduksx/core»

Composer- und npm-Paket, von jedem Modul eingebunden (Herkunft: heutiges Glossary):

- Anmeldung als OIDC-Client, Abmelden, Rollen aus Ident plus feine Rechte im Modul, zweiter Faktor über `acr`
- Protokoll, Einstellungen, Gesundheit (`/up`, `/health`), Steckbrief, Metriken, strukturierte Protokolle
- Update-Dienst und Meldung an den Leitstand
- Oberfläche: Kopfzeile mit Modulwechsel, Design-System, Tabellen, Dialoge, Hilfe nach Rolle, Barrierefreiheit
- gemeinsame Regeln für CI, Releases, Dockerfile (my-github-blueprint)

### 4.4 Leitstand

Interne Anwendung (nicht Teil eines Moduls): Kunden und ihre Module, Versionen je Instanz, Update-Ringe,
Wartungsfenster, Zustand, Meldungen; später Verträge und Abrechnung. Richtet neue Kunden automatisch ein
(Namespace bzw. VM, Datenbank, Speicher, DNS, Zertifikat, Client in Ident, erstes Admin-Konto).

## 5. Schnittstellen (verbindlich)

Alle Schnittstellen sind versioniert (`v1`), mit JSON-Schema bzw. OpenAPI beschrieben und abwärtskompatibel;
Brüche nur in einer neuen Version mit Übergangszeit.

### S1 · Anmeldung (Ident → Module)

- **Verfahren:** OpenID Connect, Authorization Code mit PKCE; nur vertrauliche Clients (Server-seitig).
- **Scopes:** `openid profile email eduksx.org` (+ modulspezifisch, z. B. `glossary`).
- **Claims im ID-Token:**

  | Claim | Inhalt |
  | --- | --- |
  | `sub` | stabile, pseudonyme Kennung (nie die E-Mail) |
  | `email`, `email_verified` | Adresse und Bestätigung |
  | `given_name`, `family_name`, `name`, `locale` | Anzeige |
  | `acr`, `amr` | Stärke der Anmeldung (z. B. `mfa`) |
  | `eduksx_orgs` | Liste `{id, name, rolle}` der Organisationen (`admin`, `member`) |
  | `eduksx_roles` | Rollen je Modul, z. B. `{"glossary": ["moderator"]}` |

- **Lebensdauer:** ID/Access-Token 5–10 Minuten, Refresh nur serverseitig; Sitzung im Modul höchstens so lange wie
  in Ident.
- **Abmelden:** RP-initiated Logout und **Back-Channel-Logout** an alle Module.
- **Zweiter Faktor:** Module verlangen für privilegierte Rollen `acr=mfa`; fehlt er, Weiterleitung zu Ident mit
  `acr_values`.
- **Rückfall:** je Modul ein lokales Notfallkonto (Break-Glass) für den Betrieb, protokolliert.

### S2 · Dienst zu Dienst

- OAuth2 **Client Credentials**, JWT-Zugriffstoken, Prüfung über **JWKS**, `aud` = Ziel-Modul, Scopes je Endpunkt
  (z. B. `glossary:read-org`, `glossary:propose`).
- Ersetzt mittelfristig die modul-eigenen Servicekonten; diese bleiben bis dahin gültig.

### S3 · Konten in isolierte Instanzen

- **SCIM 2.0** (Users, Groups) von Ident in die Instanz, oder Anlage beim ersten Login (Just-in-Time).
- Sperren/Löschen in Ident wird per SCIM bzw. Ereignis (S4) in der Instanz umgesetzt.
- Nur die für die Instanz freigegebenen Personen werden übertragen.

### S4 · Ereignisse (Ident → Module)

- **Webhooks**, signiert (HMAC-SHA256 über Zeitstempel + Inhalt, Kopfzeile `EduKSX-Signature`), Format
  **CloudEvents 1.0** JSON, Zustellung mit Wiederholung und Ausgangswarteschlange.
- Arten: `user.updated`, `user.disabled`, `user.deleted`, `org.created`, `org.updated`, `org.deleted`,
  `membership.added`, `membership.removed`, `role.changed`.
- Module verarbeiten idempotent (Ereignis-ID), weisen Ereignisse älter als 5 Minuten ab.

### S5 · Modul-Steckbrief und Zustand (Modul → Leitstand, Plattform)

- `GET /.well-known/eduksx-module.json`: Name, Version, API-Versionen, benötigte Scopes, Rechte des Moduls,
  Betriebsart, URLs für Zustand und Metriken.
- `GET /up` (Lebenszeichen, ohne Inhalt) und `GET /health` (JSON: Version, Datenbank, Migrationen, Warteschlange,
  Speicher, Ident erreichbar).
- `GET /metrics` (Prometheus, nur mit Berechtigung).

### S6 · Leitstand ↔ Instanz (Update-Dienst)

- **Nur ausgehend** von der Instanz: `POST /api/v1/instances/{id}/heartbeat` alle 15 Minuten (Version, Zustand,
  Ergebnis des letzten Auftrags – keine Inhalte, keine Personendaten); `GET /api/v1/instances/{id}/jobs` holt
  Aufträge (Update auf Version X mit Digest, Wartungsfenster).
- Anmeldung der Instanz mit eigenem Client (Client Credentials) oder mTLS; Aufträge signiert.
- Images nur signiert aus der offiziellen Registry; Update mit Sicherung, Prüfung, Rücksprung.

### S7 · Modulwechsel und Navigation

- `GET /api/v1/me/modules` in Ident: Module, auf die die Person Zugriff hat (Name, URL, Symbol) – Grundlage für die
  gemeinsame Kopfzeile in allen Modulen.

### S8 · Öffentliche Daten-APIs der Module

- REST unter `/api/v1`, OpenAPI 3.1, ETag/304, Abruflimits, CORS nur lesend, Swagger-Seite und Postman-Sammlung,
  Daten unter klarer Lizenz (Glossary: CC BY 4.0).
- Module verweisen aufeinander über Permalinks (z. B. Glossary `/g/{code}`) und die Einbindung
  (`<glossary-term>`), nicht über Datenbankzugriffe.

## 6. Anforderungen an jeden Dienst (Prüfliste)

### Betrieb

- [ ] Signiertes Docker-Image je Release (Registry, Tags `X.Y.Z`, `X.Y`, `latest`), SBOM
- [ ] Zustandslos: Sitzungen, Cache, Warteschlange in Redis bzw. Datenbank; Dateien in Object Storage
- [ ] Konfiguration nur über Umgebung und Einstellungen; Geheimnisse aus dem Geheimnisspeicher, nie im Image
- [ ] Getrennte Rollen web / worker / scheduler im selben Image
- [ ] `/up`, `/health`, `/metrics`, Steckbrief (S5); Protokolle als JSON auf stdout mit Anfrage-ID
- [ ] Migrationen vorwärts, automatisch, **abwärtskompatibel** (erweitern → umstellen → aufräumen über zwei Versionen)
- [ ] Sicherung vor Update, Wiederherstellung dokumentiert und getestet; Update-Dienst-tauglich (S6)
- [ ] Sauberes Herunterfahren (laufende Anfragen und Aufträge beenden)

### Identität und Rechte

- [ ] Anmeldung nur über Ident (S1) via `eduksx/core`; lokale Passwörter nur als Notfallkonto
- [ ] Rechte im Modul über Rechte, nicht Rollennamen; Rollen aus Ident abgebildet
- [ ] Zweiter Faktor für privilegierte Rechte (`acr`)
- [ ] Back-Channel-Logout und Ereignisse (S4) verarbeitet; Kontolöschung pseudonymisiert Inhalte nach Löschkonzept
- [ ] Dienst-zu-Dienst nur mit S2

### Mandanten und Datenschutz

- [ ] Zentral: jede Tabelle mit Kundendaten trägt die Organisations-ID; Zugriffe immer darauf eingeschränkt
- [ ] Isoliert: keine Daten verlassen die Instanz ausser Heartbeat (S6)
- [ ] Klassifizierung je Modul (öffentlich / intern / vertraulich / besonders schützenswert) und daraus Betriebsart
- [ ] Datenminimierung, Löschfristen, Export für Betroffene, Protokolle; Hosting in der Schweiz; IDG/DSG
- [ ] Datenschutzerklärung und Verzeichnis der Bearbeitungen je Modul

### Sicherheit

- [ ] OWASP ASVS Stufe 2; CSP, sichere Kopfzeilen, Abruflimits
- [ ] Abhängigkeiten geprüft (Renovate/Dependabot), CodeQL, Geheimnis-Scan
- [ ] Keine Inhalte als HTML aus fremden Quellen; Ausgaben escapen
- [ ] Sicherheitsmeldungen über private Meldestelle

### Oberfläche

- [ ] Design-System und Kopfzeile mit Modulwechsel aus `eduksx/core`
- [ ] WCAG 2.1 AA (eCH-0059), de-CH, Schweizer Schreibweise
- [ ] Hilfe nach Rolle, keine internen Entscheidnummern in Anzeigetexten

### API

- [ ] S8: versioniert, OpenAPI, ETag, Abruflimits, Swagger, Postman

### Ablauf

- [ ] Repository mit my-github-blueprint: Issues mit Freigabe, Labels, Meilensteine, CHANGELOG, Konzepte als PR,
      Releases nur nach Freigabe

## 7. Infrastruktur

### 7.1 Stufen

| Stufe | Kunden | Infrastruktur | Betrieb |
| --- | --- | --- | --- |
| 0 – heute | Glossary allein | 1 VPS, Docker Compose, Traefik | Deploy je Merge |
| 1 – Start Ident | bis ~30 | 2–3 VPS (Zentral, Kunden), Object Storage | Compose + Update-Dienst, Leitstand |
| 2 – Wachstum | ~30–200+ | Kubernetes in der Schweiz, Knotengruppen «zentral» und «Kunden» | GitOps, Ringe, Autoscaling |

**Stufe 1:** VPS «Zentral» (4 vCPU, 8–16 GB, mit SLA und Snapshots): Ident, zentrale Module, Leitstand,
PostgreSQL, Redis. VPS «Kunden» (je 4 vCPU, 8–16 GB): isolierte Instanzen; Kunden mit hohen Anforderungen eigener VPS.
Sicherungen in Object Storage und an einem zweiten Standort.

**Stufe 2:** Cluster mit Knotengruppen; je Kunde ein Namespace mit eigener Datenbank, Speicher und Netzwerkregeln;
physisch getrennt (eigene Knoten/VM) auf Wunsch; beim Kunden selbst mit Update-Dienst.

### 7.2 Container

| Container | Zweck | zentral | isoliert |
| --- | --- | --- | --- |
| web | Website, API | ≥ 2 Kopien | 1 |
| worker | Warteschlange | ≥ 1 | 1 |
| scheduler | geplante Aufgaben | 1 | 1 |
| Datenbank | PostgreSQL | gemeinsam (mit Ersatz) | je Kunde (oder SQLite) |
| Update-Dienst | Aufträge ausführen | – (GitOps) | ausserhalb des Clusters |

Schätzung: zentral 15–25 Container plus Datenbank, Redis, Ingress, Monitoring; 200 isolierte Instanzen ≈ 600–800
Container, ≈ 60–100 GB RAM, 4–8 Knoten mit 16–32 GB.

### 7.3 Standorte

Schweiz (z. B. Infomaniak), Hauptstandort und zweiter Standort für Sicherungen und Notfall; öffentliche Dienste hinter
CDN (z. B. Cloudflare); isolierte Instanzen wahlweise bei uns oder beim Kunden.

### 7.4 Automatisch aktualisieren

| Was | Wie |
| --- | --- |
| Module | Release → signiertes Image → Leitstand setzt Zielversion → GitOps (Argo CD/Flux) bzw. Update-Dienst; Ringe: unser Server → Pilot (~5 %) → alle; blau/grün; Rücksprung; Stopp bei Fehlern |
| Abhängigkeiten, Basis-Images | Renovate/Dependabot als PR, CI, nächstes Release |
| Betriebssystem | automatische Sicherheitsupdates; Cluster-Knoten durch den Anbieter nacheinander |
| PostgreSQL | Operator (z. B. CloudNativePG), kleine Updates automatisch |
| Zertifikate | automatisch (Traefik / cert-manager) |
| Infrastruktur | als Code (OpenTofu/Terraform, Ansible) |

### 7.5 Vorkehrungen für Skalierung

1. Zustandslose Container (Redis, Object Storage)
2. PostgreSQL für alles Zentrale, mit Verbindungspool und Lesekopien
3. Arbeit getrennt (worker, scheduler)
4. Organisations-ID überall in zentralen Diensten
5. Abwärtskompatible Migrationen (Updates ohne Ausfall)
6. Grenzen je Kunde (Abrufe, Speicher, Konten)
7. Beobachtung von Anfang an (Prometheus, Grafana, Loki, Uptime-Überwachung)
8. Sicherungen mit regelmässigem Wiederherstellungstest
9. Geheimnisse zentral (SOPS/Vault), keine handgepflegten `.env` je Instanz

## 8. Fahrplan

1. **Ident** (Produktwahl, Portal, Brücken) – Plattform-Rollen und Organisationen
2. **Glossary als erster Client** (vorbereitende Issues im Glossary, siehe unten)
3. **`eduksx/core`** aus dem Glossary herauslösen
4. **Rechtssammlung** als zweiter zentraler Dienst
5. **Leitstand und Update-Dienst**, dann **Intranet** als erste isolierte Instanz
6. Stufe 2 (Kubernetes), wenn der Aufwand mit einzelnen VPS spürbar wird

### Vorbereitende Arbeiten im EduKSX-Glossary (Issues, Status `triage`)

| Issue | Inhalt | Schnittstelle |
| --- | --- | --- |
| [#185](https://github.com/MarkusKeller8200/EduKSX-Glossary/issues/185) | Anmeldung über OpenID Connect | S1 |
| [#186](https://github.com/MarkusKeller8200/EduKSX-Glossary/issues/186) | Rollen und Organisation aus Ident | S1 |
| [#187](https://github.com/MarkusKeller8200/EduKSX-Glossary/issues/187) | Back-Channel-Logout und Ereignisse | S1, S4 |
| [#188](https://github.com/MarkusKeller8200/EduKSX-Glossary/issues/188) | OAuth2 Client Credentials zwischen Diensten | S2 |
| [#189](https://github.com/MarkusKeller8200/EduKSX-Glossary/issues/189) | Modul-Steckbrief und `/health` | S5 |
| [#190](https://github.com/MarkusKeller8200/EduKSX-Glossary/issues/190) | zustandslos mit Redis und Object Storage | 7.5 |
| [#191](https://github.com/MarkusKeller8200/EduKSX-Glossary/issues/191) | PostgreSQL unterstützen | 7.5 |
| [#192](https://github.com/MarkusKeller8200/EduKSX-Glossary/issues/192) | strukturierte Protokolle und Metriken | S5, 7.5 |
| [#193](https://github.com/MarkusKeller8200/EduKSX-Glossary/issues/193) | Bausteine für `eduksx/core` abgrenzen | 4.3 |

Dazu im Glossary bereits geplant: Selbst hosten und Updates (Konzept DEC-027, #174–#184).

## 9. Offene Entscheide

1. Identity-Provider: Keycloak oder Zitadel (Bewertung)?
2. Ident zentral für alle oder getrennte Bereiche je Kunde ab einer bestimmten Klassifizierung?
3. Leitstand als eigene interne Anwendung (Vorschlag) oder Teil von Ident?
4. Zuerst zentral mit Organisationen, isolierte Instanzen nur auf Wunsch (Vorschlag)?
5. Zeitpunkt für Stufe 2 (Kubernetes) – Kriterium z. B. > 30 isolierte Instanzen?
6. Domains: Unterdomain je Kunde (`schule-x.intranet.eduksx.ch`) und/oder eigene Domain des Kunden?
7. Lizenzmodell der Plattform-Module (offen wie das Glossary oder teilweise geschlossen)?
