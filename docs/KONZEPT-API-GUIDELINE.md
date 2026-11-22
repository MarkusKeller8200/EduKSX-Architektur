# Konzept: API-Standard der EduKSX-Plattform (#15, #18)

Stand: 22.11.2026 (Version 1.3) · Verantwortlich: Markus Keller · Status: **BESCHLOSSEN** – Version 1.3 (G4 API-First)
beschlossen am 22.11.2026 (Version 1.2 am 20.11.2026, Version 1.1 am 13.11.2026, Version 1.0 am 12.11.2026)

Verbindlicher Standard für **alle** Schnittstellen der EduKSX-Module (Glossary, Rechtssammlung, Intranet, Stundenplan,
Ident …) – für Menschen und KI-Agenten. Er enthält nur Regeln, die für jedes Modul gelten. Endpunkte, Felder und
modulspezifische Entscheide stehen im API-Konzept des jeweiligen Moduls, das auf diesen Standard verweist (für das
Glossary: `docs/KONZEPT-API.md`, für das Intranet: `App\Support\OpenApi` und `docs/KONZEPT-MCP.md`).

Er ergänzt den [DB-Standard](KONZEPT-DB-GUIDELINE.md) (Verweise A1 … D3) und konkretisiert die Schnittstellen S1–S8 aus
[KONZEPT-PLATTFORM.md](KONZEPT-PLATTFORM.md).

**Verbindlichkeit** (Stufen nach [KONZEPT-VORLAGE.md](KONZEPT-VORLAGE.md)): Alle Regeln sind **BESCHLOSSEN**
(12.11.2026, Abnahme Version 1.0) – auch die im Text als EMPFOHLEN bezeichneten –, ausser sie sind ausdrücklich als
**ZU PRÜFEN** gekennzeichnet. Quellen der übernommenen Regeln stehen in Klammern. Neu in 1.1 (Entscheide API-E18–API-E35 vom
13.11.2026, nach dem Architektur-Review): schlanke Umsetzung in **Stufen**, **Modulschlüssel** für die Suite,
Korrekturen K1–K3, Datenschutz nach DSGVO/IDG und nachweisbare Sicherheit.

**Grundlagen:** Der Standard folgt in den meisten Punkten den Zalando RESTful API Guidelines (auch Vorbild für OTTO,
SBB und die REST-Guidelines des Bundes), den Empfehlungen der API-Architektur Bund (Security Guideline 1.0, 08/2025;
Idempotenz AP10, 01/2025), den OWASP API Security Top 10 (2023) und den IETF-Standards. Bewusste Abweichungen stehen in
[Abweichungen von Zalando](#bewusste-abweichungen-von-zalando), Quellen am Schluss. Er schliesst die offenen Punkte
API-01 und SEC-01 (externe Clients) im WebApplicationProgrammingGuide.

| Teil | Inhalt |
| --- | --- |
| [Stufen und Suite](#stufen-und-suite) | Was ab Tag 1 gilt, was vor dem Betrieb, was nur bei Bedarf; Modulschlüssel; `eduksx/core` |
| [A · Entwurf](#a--entwurf) | Grundsätze, URLs, JSON, Felder, Datum, Sprache, Listen, Filter, Fehler, Statuscodes |
| [B · Verhalten](#b--verhalten) | Schreiben, Sperren, Idempotenz, Löschen, Caching, Synchronisation, Ereignisse |
| [C · Sicherheit und Datenschutz](#c--sicherheit-und-datenschutz) | Anmeldung, Tokens, Scopes, Mandanten, Datenklassen, Grenzen, CORS |
| [D · Lebenszyklus](#d--lebenszyklus) | Versionierung, Stabilität, OpenAPI, Doku, MCP, Betrieb, Tests, Konformität |

## Grundsätze

1. **API first** – jede Schnittstelle steht zuerst als Vertrag (OpenAPI) fest, und **jede fachliche Funktion** gibt es
   auch als API-Operation mit demselben Service und derselben Policy wie in der Oberfläche; Website, Intranet und MCP
   nutzen dieselben Services. Ausgeführt in [G4](#g4-api-first-beschlossen-22112026-api-e38). BESCHLOSSEN (IDA-Vorgehen,
   Glossary «API gehört zum Kern»; präzisiert 22.11.2026, API-E38)
2. **Kein Zugriff auf fremde Datenbanken** – Module tauschen Daten nur über APIs, Permalinks und Ereignisse aus.
   BESCHLOSSEN (DB B5, Plattform S8)
3. **Beschreibung vor Code** – jede Operation steht in der OpenAPI-Beschreibung; ein Test verhindert Routen ohne
   Beschreibung. BESCHLOSSEN (Glossary #25)
4. **Nichts bricht** – in einer Version wird nur hinzugefügt; Brüche nur in einer neuen Hauptversion mit
   Übergangszeit. BESCHLOSSEN (Plattform §5, Glossary DEC-016)
5. **Positivliste statt Filter** – eine Antwort enthält nur Felder, die für diesen Zweck ausdrücklich freigegeben sind.
   BESCHLOSSEN (Glossary DEC-018, `ApiPresenter::PUBLIC_TERM_FIELDS`)
6. **Gleiche Regeln überall** – API, Website, Import und MCP rufen dieselben Rechteprüfungen und Services auf; ein Token
   hat nie mehr Rechte als seine Besitzerin oder sein Besitzer. BESCHLOSSEN (Intranet KONZEPT-MCP, Glossary DEC-017)
7. **Schlank** – der Standard ist kein Aufwandgenerator: Regeln gelten nach **Stufen** (ab Tag 1, vor dem Betrieb,
   nur bei Bedarf), und was jede API gleich macht, kommt fertig aus `eduksx/core`; Module konfigurieren, statt zu
   bauen. BESCHLOSSEN 13.11.2026 (API-E18)
8. **Eine Suite, eigenständige Repos** – jedes Modul hat einen registrierten **Modulschlüssel**; daran ist überall
   erkennbar, woher eine API, ein Scope, ein Ereignis oder ein Fehler stammt, und Namen kollidieren nie.
   BESCHLOSSEN 13.11.2026 (API-E19)
9. **DSGVO und IDG** – Datenschutz ist eingebaut, nicht nachgerüstet: Datenklassen und Zweck je Operation, Auskunft,
   Fristen, Datenort Schweiz/EU (C9). BESCHLOSSEN 13.11.2026 (API-E26–API-E29)
10. **Sicherheit nachweisbar** – Prüfziel OWASP ASVS Level 2, automatischer Scan und Penetrationstest vor dem ersten
    produktiven Release; ein Pentest darf keine offenen Befunde ergeben (C10). BESCHLOSSEN 13.11.2026 (API-E30)

---

## Stufen und Suite

### G1 Stufen (BESCHLOSSEN 13.11.2026, API-E18, API-E31)

Jede Regel gehört zu einer Stufe. Ein Modul erfüllt **Stufe 1 ab der ersten API**, **Stufe 2 vor dem produktiven
Betrieb** und **Stufe 3 nur für die Funktionen, die es tatsächlich anbietet**.

| Stufe | Wann | Regeln |
| --- | --- | --- |
| **1 · Kern** | jede API ab Tag 1, auch Prototypen | Vertrag zuerst (G4 A), `/api/v1` und Namen (A1, A2), Modulschlüssel (G2), `problem+json` (A6), Statuscodes (A7), Cursor (A5), Anmeldung + Scope + Recht je Objekt (C1–C3), Positivlisten Lesen/Schreiben (C4), Abruflimit und Sicherheitskopfzeilen (C5, C6), `request_id` (C7), OpenAPI mit Linter (D3), Tests «Prototyp» (D7) |
| **2 · Betrieb** | vor dem ersten produktiven Release | jede Fachfunktion als API mit Prüfung (G4 B), `If-Match` (B2), Idempotenz wo Pflicht (B3), Papierkorb-Regeln (B4), Caching (B5), Datenklassen und Zweck je Operation, Auskunft/Export, Fristen (C9), ASVS L2, Scan, Pentest (C10), `oasdiff` und Versionierung (D1, D3), Doku (D4), Betrieb (D6), Tests «produktiv» (D7), Konformitätstest (D8) |
| **3 · Bei Bedarf** | nur wenn das Modul die Funktion anbietet | Synchronisation (B6), Ereignisse und Webhooks (B7), MCP (D5), Sammeländerungen und Aufträge (B1), alle Sprachen mit `?locale=*` (A4), Organisations-API (C3) |

### G2 Modulschlüssel und Namensräume (BESCHLOSSEN 13.11.2026, API-E19)

Jedes Modul hat einen **Modulschlüssel**: englisch, klein, ein Wort (`[a-z][a-z0-9]{1,15}`), einmalig in der Suite und
unveränderlich. Er steht im Register unten; ein neues Modul trägt sich per Pull Request ein. Der Schlüssel bildet den
Namensraum überall dort, wo Module zusammentreffen – innerhalb eines Moduls sind Namen frei.

| Wo | Muster | Beispiel |
| --- | --- | --- |
| Adresse | eigener Host je Modul bzw. Instanz, Pfad `/api/v1`; später optional Gateway `api.eduksx.ch/<modul>/v1` | `glossary.eduksx.ch/api/v1/terms` |
| Steckbrief und OpenAPI | `module` in `/.well-known/eduksx-module.json`, `info.x-eduksx-module` | `"module": "glossary"` |
| Scopes | `<modul>:<ressource>.<aktion>` (C2) | `glossary:terms.read` |
| Ereignisse | `<modul>.<objekt>.<verb>` (B7) | `glossary.term.published` |
| Fehler-Typen | gemeinsame: `https://docs.eduksx.ch/problems/<code>`; modul-eigene: `…/problems/<modul>/<code>` | `…/problems/glossary/term_merged` |
| Tokens | Präfix `<modul>_<art>_` (C1) | `glossary_sa_…`, `intranet_pat_…` |
| MCP-Werkzeuge | `<modul>_<operation>` | `glossary_list_terms` |
| Kopfzeilen | nur die Plattform: `EduKSX-<Name>` (B5); Module definieren keine eigenen | `EduKSX-Release` |

**Register:** Schlüssel, Repos und Status aller Module stehen nur noch im [Modulregister](REGISTER-MODULE.md)
(Änderungen nur per Pull Request). Schlüssel sind englisch und ändern nie; Marketingnamen sind frei.

### G3 Gemeinsame Bausteine in `eduksx/core` (BESCHLOSSEN 13.11.2026, API-E20)

Was jede API gleich macht, baut kein Modul selbst. `eduksx/core` liefert die Bausteine **in dieser Reihenfolge und erst,
wenn das erste Modul sie braucht** – nichts auf Vorrat:

1. **HTTP-Basis** (Stufe 1): `problem+json`-Handler, `request_id`, Sicherheitskopfzeilen, CORS, Abruflimits,
   Maskierung im Protokoll.
2. **Listen und Schreiben** (Stufe 1/2): Cursor-Pagination, starker ETag mit `If-Match`, Idempotenz-Speicher.
3. **Prüfungen** (Stufe 1/2): Spectral-Regelsatz `eduksx`, `oasdiff`-Aufruf, Konformitätstest (D8).
4. **Integration** (Stufe 3, mit Ident bzw. dem ersten Webhook): Prüfung von Tokens und Scopes (Servicekonten, später
   JWT), Signatur von Webhooks, HTTP-Client mit SSRF-Schutz.

Ein Modul darf einen Baustein nur ersetzen, wenn es dafür einen Eintrag im Ausnahmeregister (D8) hat.

### G4 API-First (BESCHLOSSEN 22.11.2026, API-E38)

API-First heisst bei EduKSX zwei verbindliche Stufen und eine erlaubte:

| Stufe | Regel | Status |
| --- | --- | --- |
| **A · Vertrag zuerst** | Jede Schnittstelle steht zuerst in der OpenAPI-Beschreibung, wird geprüft (Linter, `oasdiff`) und erst dann gebaut (D3). | verbindlich |
| **B · Jede Fachfunktion als API** | Was die Oberfläche fachlich kann – anlegen, ändern, freigeben, exportieren, löschen, wiederherstellen –, gibt es auch als API-Operation. Oberfläche und API rufen **denselben Service** und **dieselbe Policy** auf; keine Fachlogik nur im Controller der Oberfläche. | verbindlich |
| **C · Oberfläche über die eigene API** (headless) | Website und Administration rufen nur `/api/v1` auf. | erlaubt, nicht verlangt (Inertia bleibt möglich) |

**Prüfung (automatisch):** Jede schreibende Web-Route nennt die zugehörige API-Operation (`operationId`, z. B. als
Routen-Attribut `eduksx.operation`). Ein Test aus `eduksx/core` (Konformitätstest D8) schlägt fehl, wenn eine schreibende
Web-Route keine Operation nennt, die Operation in der Beschreibung fehlt oder Route und Operation einen anderen Service
bzw. eine andere Policy aufrufen. Reine Anzeige-Seiten brauchen keine Operation.

**Interne APIs** (z. B. `/api/sync`, Administration, Dienst zu Dienst) folgen denselben Regeln und stehen in der
OpenAPI-Beschreibung, markiert mit `x-eduksx-internal: true`. Die öffentliche Doku (D4) und Postman blenden sie aus; der
Linter und die Tests prüfen sie wie alle anderen.

**Ausnahmen** nur mit Eintrag im Ausnahmeregister (D8), z. B. Assistenten über mehrere Schritte, deren Zwischenschritte
keine eigene Fachfunktion sind.

**Stufe und Übergang:** Regel A gilt ab Stufe 1 (G1), Regel B und die Prüfung ab Stufe 2 (vor dem ersten produktiven
Release). Bestehende Module übernehmen B ab ihrem nächsten MINOR-Release mit einem Issue im Modul (nicht rückwirkend,
DB E5); fehlende Operationen werden dort erfasst.

---

## A · Entwurf

### A1 URLs und Ressourcen (EMPFOHLEN, Version im Pfad BESCHLOSSEN)

| Regel | Muster | Richtig | Falsch |
| --- | --- | --- | --- |
| U1 | Präfix mit Hauptversion | `/api/v1/…` | `/api/terms`, `?version=1` |
| U2 | Ressourcen englisch, Plural, `kebab-case` | `/api/v1/service-accounts` | `/api/v1/serviceAccount`, `/api/v1/begriffe` |
| U3 | Einzelobjekt über `id` (UUID v7), zusätzlich Slug/Code wo vorhanden | `/terms/{idOrSlug}` | `/terms?id=…` |
| U4 | Unterressource nur bei echter Zugehörigkeit, höchstens zwei Ebenen | `/proposals/{id}/events` | `/orgs/{id}/members/{id}/roles/{id}` |
| U5 | Aktion, die kein CRUD ist: Unterressource als Substantiv bzw. Verb mit `POST` | `POST /terms/{id}/publication`, `POST /people/{id}/restore` | `GET /terms/{id}/publish` |
| U6 | Organisationsdaten unter eigenem Präfix, Organisation aus dem Token | `/api/v1/org/terms` | `/api/v1/organizations/{orgId}/terms` für fremde IDs |
| U7 | Eigene Person | `/api/v1/me` | `/api/v1/users/current` |
| U8 | Abfrageparameter `snake_case` | `?per_page=50&updated_since=…` | `?perPage=50` |

Website-Routen bleiben deutsch (`/begriffe/{slug}`), API-Routen englisch (DB A1). Feste Plattform-Pfade (BESCHLOSSEN,
Plattform S5): `/up`, `/health`, `/metrics`, `/.well-known/eduksx-module.json`, `/api/openapi.json`, `/api/docs`.

### A2 JSON und Feldnamen (BESCHLOSSEN durch DB A1, Hülle EMPFOHLEN)

- HTTPS, `application/json; charset=utf-8`, Unicode NFC (DB D3), keine `null`-Bytes, keine HTML-Codierung.
- Feldnamen **englisch, `snake_case`**, gleich wie die Spalten der Datenbank (`short_description`, `published_at`,
  `is_active`, `responsible_user_id`). Werte von Status und Arten englisch `snake_case`, **identisch** in Datenbank,
  API und Exporten (DB A1) – nie deutsche Anzeigewerte wie `"aktuell"`; das deutsche Label liefert die API bei Bedarf
  zusätzlich als `status_label`.
- **Hülle (EMPFOHLEN – in Glossary und Intranet bereits so umgesetzt):**

  ```json
  { "data": { "id": "0193…", "name": "…" } }
  { "data": [ … ], "meta": { "page": 1, "per_page": 50, "total": 812, "last_page": 17 },
    "links": { "self": "…", "next": "…", "prev": null } }
  ```

  Einzelobjekt und Listen immer in `data`; Zusatzinformationen in `meta`, Navigation in `links`. Glossary und Intranet
  nutzen `data` bereits; das Antwortbeispiel in der KONZEPT-API des Glossary zeigt das Objekt noch ohne Hülle.
- Werte von Status und Arten kommen englisch wie in der Datenbank; für Menschen zusätzlich das Label in der gewählten
  Sprache als `<feld>_label` (`"status": "current", "status_label": "aktuell"`) – BESCHLOSSEN 12.11.2026, API-E9.
- Auf oberster Ebene steht immer ein JSON-Objekt, nie eine Liste oder ein Wert (Zalando #110).
- Fehlende Werte als `null`, nie als leerer String; `null` und fehlendes Feld bedeuten dasselbe (ausser bei `PATCH`,
  B1). Ein Feld ist entweder «darf leer sein» (dann heisst `null` leer) oder Pflicht (dann ergibt `null` `422`) –
  einen dritten Zustand «bewusst `null` gesetzt» gibt es nicht (API-E32). Leere Listen als `[]`, nie `null`; Ja/Nein-Felder sind nie `null` – wo es drei Zustände gibt, ist es eine
  Aufzählung (Zalando #122–#124).
- Unbekannte Felder in Anfragen werden mit `422` abgelehnt, unbekannte Felder in Antworten ignorieren Abnehmer (D2).
- Aufzählungen sind **erweiterbar**: In OpenAPI als `type: string` mit `x-extensible-enum` (bzw. `examples`), damit
  neue Werte keine brechende Änderung sind. Ein geschlossenes `enum` nur für Eingaben, die der Dienst selbst prüft.
  Ein **unbekannter Wert** wird bei Entscheiden über Zugriff, Freigabe oder Sichtbarkeit wie «verweigert» behandelt,
  nie wie «erlaubt» (API-E32).
- Jede Zahl hat in der Beschreibung ein `format` (`int32`, `int64`); Fliesskommazahlen (`double`) nur für Messwerte.
- Geldbeträge als ganze Zahl in Rappen mit Feld `currency` (DB A4). Andere exakte Dezimalzahlen (z. B. Pensen,
  Prozentsätze mit fester Stellenzahl) als **String** mit `format: decimal` und `pattern`
  (`^-?\d+(\.\d{1,4})?$`). Sonst Zahlen nie als String; IDs immer als String (API-E32).
- **Datensparsam:** Antworten enthalten die für den Zweck nötigen Felder. Mehr nur mit `?fields=` und nur aus der
  Positivliste mit Recht (C4, C9).
- Verweise als `<ziel>_id`; eingebettete Objekte nur auf Anfrage (`?include=categories`) oder wenn das Konzept des
  Moduls es festlegt.

### A3 Datum und Zeit (BESCHLOSSEN, DB D2)

- In der API **immer ISO 8601**: Zeitpunkt in UTC mit `Z` (`2026-11-12T20:53:07Z`, Feld `_at`), Datum ohne Zeit
  (`2026-11-12`, Feld `_on`), Zeitraum `valid_from` / `valid_until`.
- Die Anzeige `DD.MM.YYYY` / `HH:MM:SS` (Europe/Zurich) gibt es nur in Oberflächen, Excel und PDF – nie in JSON.
- Parameter mit Zeitpunkten (`updated_since`) nehmen ISO 8601 entgegen; ohne Zeitzone gelten sie als **ungültig**
  (`422`), nicht als Ortszeit.

### A4 Sprachen (EMPFOHLEN, Grundlage DB D1)

- Fachinhalte sind mehrsprachig. Die Sprache wählt `?locale=fr` oder die Kopfzeile `Accept-Language`; der Parameter
  gewinnt. Die Antwort nennt sie in `Content-Language` und je Objekt in `locale`.
- Fehlt eine Übersetzung, kommt die Grundsprache `de` mit `"locale": "de"` – Abnehmer erkennen so den Rückfall.
- Für Synchronisation und Redaktion: `?locale=*` liefert alle Sprachen als
  `"translations": { "fr": { "name": "…" }, "it": { … } }`.
- Antworten, die von der Sprache abhängen, senden `Vary: Accept-Language`; Caches trennen nach `locale` (API-E32).
- Persönliche Freitexte werden nie übersetzt (DB D1). Fehlermeldungen (`title`, `detail`) folgen der gewählten Sprache;
  `type` und `code` sind sprachneutral.

### A5 Listen, Pagination, Filter, Sortierung (EMPFOHLEN, Glossary umgesetzt)

**Cursor ist Standard, Seiten sind erlaubt** (BESCHLOSSEN 12.11.2026, nach Zalando #160, #254):

| Zweck | Verfahren | Parameter | Antwort |
| --- | --- | --- | --- |
| **Standard:** Listen, Suche, Synchronisation, Ereignisse | Cursor | `cursor` (undurchsichtig), `limit` (Vorgabe 50, höchstens 200); Feeds zusätzlich `since` | `meta.next_cursor`, `has_more`; `links.next` |
| Kleine Listen in der Administration (erwartet < 10 000 Einträge) | Seiten | `page` (ab 1), `per_page` (Vorgabe 50, höchstens 200) | `meta.page`, `per_page`; `links.next/prev` |

- Die **Gesamtzahl** (`meta.total`, `last_page`) kommt nur auf Anfrage mit `?with_total=1` und nur, wo sie günstig
  zu berechnen ist; sie ist nie Pflicht für Abnehmer.
- Der Cursor ist ein undurchsichtiger, URL-sicherer String (Base64 aus Sortierwert + `id`); Abnehmer bauen ihn nie
  selbst. Filter und Sortierung sind im Cursor enthalten – andere Filter mit altem Cursor ergeben `422`.
- Jede Liste ist begrenzt; ohne `limit` bzw. `per_page` gilt die Vorgabe, nie «alles». Vollstände nur über einen
  Export-Endpunkt (`/exports`).
- Reihenfolge ist **immer stabil** (zuletzt nach `id`), damit keine Einträge zwischen Seiten verloren gehen.
- Filter als einfache Parameter mit Feldnamen (`?status=published&category=…`), Mehrfachwerte kommagetrennt
  (`?status=draft,under_review`), Zeiträume mit `_since`/`_until`. Volltext mit `q` – gesucht wird in der normalisierten
  Suchspalte (DB D3).
- Sortierung mit `sort=name,-published_at` (Minus = absteigend), nur über freigegebene Felder; Sortierung für Menschen
  nach Schweizer Regeln (DB D3).
- Ungültige Werte (`per_page=0`, unbekanntes Sortierfeld) ergeben `422`, nicht stilles Korrigieren.

### A6 Fehler (BESCHLOSSEN 12.11.2026, API-E5)

Alle Fehler unter `/api/` als **`application/problem+json` nach RFC 9457**:

```json
{
  "type": "https://docs.eduksx.ch/problems/validation",
  "title": "Die Eingaben sind nicht gültig.",
  "status": 422,
  "detail": "2 Felder sind nicht gültig.",
  "code": "validation_failed",
  "instance": "/api/v1/people",
  "request_id": "01JCX…",
  "errors": { "email": ["Die E-Mail-Adresse ist bereits vergeben."] }
}
```

- `code` ist ein stabiler, englischer Fehlerschlüssel (gehört zum Vertrag, D2); `title`/`detail` sind für Menschen und
  übersetzt.
- `errors` je Feld (Feldname wie im Body, verschachtelt mit Punkt: `address.zip`).
- Fehler enthalten nie Stacktraces, SQL, Pfade, Tokens oder Personendaten anderer Personen.
- Auch `401`, `403`, `404`, `429` und Fehler aus Middleware und Framework kommen in diesem Format (ein zentraler
  Handler).

### A7 Statuscodes (EMPFOHLEN)

| Code | Wann |
| --- | --- |
| `200` | Lesen, Ändern mit Rückgabe |
| `201` | Angelegt, mit `Location` und Objekt in `data` |
| `202` | Angenommen, läuft als Auftrag (`Location` auf `/jobs/{id}`) |
| `204` | Gelöscht bzw. ausgeführt ohne Inhalt – auch beim wiederholten `DELETE` (B4) |
| `301` | Objekt dauerhaft verschoben (z. B. zusammengeführter Begriff, Glossary #16) – nur für `GET`/`HEAD` |
| `308` | Dauerhaft verschoben für schreibende Methoden (Methode und Body bleiben) – nur wo ein Modul es festlegt |
| `304` | Unverändert (ETag) |
| `400` | Anfrage nicht lesbar (kaputtes JSON); `Idempotency-Key` fehlt, wo er Pflicht ist (B3) |
| `401` | Nicht angemeldet, Token ungültig/abgelaufen (mit `WWW-Authenticate`) |
| `403` | Angemeldet, aber kein Recht bzw. Scope |
| `404` | Gibt es nicht **oder** darf nicht gesehen werden (fremde Organisation → immer `404`, nie `403`) |
| `409` | Konflikt mit dem Zustand (Doppelanlage, `lock_version` veraltet, DB A6); Anfrage mit gleichem `Idempotency-Key` läuft noch |
| `410` | Endgültig gelöscht oder zurückgezogen, wo das Modul es so festlegt |
| `412` | `If-Match` passt nicht (B2, B4) |
| `415` | Falscher Content-Type |
| `422` | Inhaltlich ungültig (Validierung, unbekannte Felder oder Parameter); `Idempotency-Key` mit anderem Inhalt wiederverwendet |
| `428` | `If-Match` fehlt, wo es Pflicht ist |
| `429` | Abruflimit überschritten, mit `Retry-After` |
| `500`/`503` | Fehler im Dienst bzw. Wartung, mit `Retry-After` bei `503` |

### A8 Deutsche Beschreibungen in der OpenAPI-Beschreibung (BESCHLOSSEN 20.11.2026, API-E37; Grundlage DB A8)

Pfade, Felder, Parameter und Werte bleiben englisch (A1, A2). Jeder englische Name trägt eine deutsche Beschreibung,
verbindlich für alle EduKSX-Projekte:

| Element | Pflicht | Beispiel |
| --- | --- | --- |
| **Schema** (Objekt) | `title` = deutscher Begriff, `description` = Kurzbeschreibung mit Herkunft bzw. Verwendung | `Class`: `title: Klasse`, `description: Klasse eines Schuljahrs; erfasst in «Klassen», Grundlage für VZE und Lektionen` |
| **Eigenschaft und Parameter** | `title` = deutscher Begriff, `description` = Herkunft bzw. Verwendung | `student_count`: `title: Schülerzahl`, `description: Eingabe in «Klassen»; für Klassengrösse und VZE` |
| **Aufzählung** (Status, Art) | `x-eduksx-labels` mit dem deutschen Label je Wert – dieselben Texte wie `<feld>_label` (A2) und das Enum | `x-eduksx-labels: { draft: Entwurf, submitted: eingereicht }` |
| **Operation** | `summary` und `description` deutsch | `summary: Klasse anlegen` |
| **Tag** | `name` englisch wie die Ressource, `description` deutsch | `classes` – «Klassen und Klassenlehrpersonen» |

- Entspricht ein Feld einer Spalte, sind Begriff und Beschreibung **identisch** mit dem Datenmodell (DB A8) – eine
  Quelle, kein zweiter Text. Berechnete Felder nennen, woraus sie berechnet werden.
- `title` ist kurz (ein Begriff, kein Satz); `description` eine Zeile, ohne Entscheidnummern und ohne echte
  Personen- oder Organisationsnamen (D3).
- Der Linter (D3) prüft `title` und `description` bei Schemas, Eigenschaften und Parametern sowie
  `x-eduksx-labels` bei jeder Aufzählung – zuerst als Warnung, ab dem folgenden Release als Fehler.

---

## B · Verhalten

### B1 Schreiben (EMPFOHLEN)

- `POST` legt an, `PATCH` ändert einzelne Felder (JSON Merge Patch, RFC 7396: fehlendes Feld = unverändert,
  `null` = leeren, für Pflichtfelder `422`), `PUT` nur, wo ein Objekt bewusst als Ganzes ersetzt wird, `DELETE` löscht.
  Komplexe Änderungen (Reihenfolge, Verschieben, Zusammenführen) sind eigene Operationen (U5), kein JSON Patch.
- `PATCH` akzeptiert `application/merge-patch+json` und `application/json` und behandelt beide gleich; andere Typen
  ergeben `415` (BESCHLOSSEN 12.11.2026, API-E14).
- Validierung im Service, nicht im Controller – dieselbe für Website, API, Import und MCP. Nicht beschreibbare Felder
  (`id`, `created_at`, berechnete Werte) im Body ergeben `422`, sie werden nicht still ignoriert.
- Jede Änderung läuft in **einer** Transaktion (DB A6); Mails, Webhooks und Aufträge erst nach dem Commit.
- Die Antwort enthält das gespeicherte Objekt (mit neuem `lock_version` bzw. `ETag`), damit Abnehmer nicht erneut lesen
  müssen.
- Jede Änderung schreibt die Historie mit `source = api` (bzw. `mcp`), `actor_*` aus dem Token und `request_id`
  (DB A7).
- Lang laufende Vorgänge (grosse Importe, Exporte > 5 s bzw. > 10 000 Zeilen, DB A6) laufen als Auftrag: `202` und
  `GET /api/v1/jobs/{id}` mit `status` (`queued`, `running`, `succeeded`, `failed`) und Ergebnis.
- Mehrfachänderungen (`POST /…/batch`) nur, wenn ein Modul sie braucht; dann **alles oder nichts** und höchstens
  1000 Einträge.

### B2 Konkurrierende Änderungen (BESCHLOSSEN 12.11.2026, API-E6; Grundlage DB A6)

- Änderbare Objekte liefern `lock_version` im Body und einen **starken** `ETag` in der Kopfzeile:
  `ETag: "<id>.<lock_version>"` – nie `W/…`, weil `If-Match` nach RFC 9110 nur starke ETags vergleicht (K1, API-E21).
- Der ETag steht für den **Stand des Objekts**, nicht für eine bestimmte Darstellung: Sprache, gewählte Felder oder
  Rechte ändern ihn nicht. Der Dienst vergleicht `If-Match` gegen `id` und `lock_version`.
- `PATCH`, `PUT` und `DELETE` verlangen `If-Match` mit dem ETag (fehlt er: `428`); passt er nicht: `412` mit dem
  aktuellen ETag in der Antwort. Nichts wird überschrieben.
- Öffentliche Lese-ETags (Prüfsumme des Inhalts, B5) sind davon getrennt und gelten nur für `If-None-Match`.
- Wer kein `If-Match` senden kann (einfache Integrationen), darf `lock_version` im Body mitgeben; veraltet ergibt
  `409`.

### B3 Idempotenz und Wiederholung (EMPFOHLEN)

Nach Bund AP10 und dem IETF-Entwurf «Idempotency-Key» (noch kein RFC, ZU PRÜFEN bei dessen Veröffentlichung):

- `GET`, `HEAD`, `PUT`, `DELETE` sind idempotent; `POST` und `PATCH` nicht.
- Für `POST`, der etwas anlegt oder auslöst, akzeptiert die API die Kopfzeile `Idempotency-Key` (UUID v4, als
  String). Der Dienst speichert Schlüssel, Fingerabdruck, Bereich und Antwort **24 Stunden**:

  | Fall | Antwort |
  | --- | --- |
  | Schlüssel neu | normal ausführen, Antwort speichern |
  | Schlüssel bekannt, gleicher Body, abgeschlossen | gespeicherte Antwort erneut, Kopfzeile `Idempotent-Replayed: true` |
  | Schlüssel bekannt, Erstanfrage läuft noch | `409` |
  | Schlüssel bekannt, anderer Body | `422` |
  | Schlüssel fehlt, wo das Modul ihn verlangt | `400` |

- **Bereich** eines Schlüssels (API-E22): Organisation + Identität (Person bzw. Servicekonto, nicht das Token) + Methode
  und Pfad-Vorlage. Ein erneuertes Token führt denselben Auftrag also nicht zweimal aus; ein fremder Schlüssel liefert
  nie die Antwort einer anderen Identität.
- **Fingerabdruck:** SHA-256 über Methode, Pfad und den normalisierten Body (JSON mit sortierten Schlüsseln, ohne
  Leerraum).
- Synchronisation, Importe, Bestellungen und MCP-Werkzeuge senden immer einen `Idempotency-Key`; für diese Endpunkte
  ist er Pflicht.
- Abnehmer wiederholen nur bei `429`, `503` und Netzfehlern – mit `Retry-After` bzw. exponentiellem Abstand und Zufall,
  höchstens fünfmal.

### B4 Löschen (EMPFOHLEN, Grundlage DB B3)

- `DELETE` auf ein Hauptobjekt löscht vorläufig (Papierkorb); die Antwort ist `204`. Der Papierkorb behält den ETag,
  mit dem gelöscht wurde. Damit gilt (K2, API-E23):

  | Fall | Antwort |
  | --- | --- |
  | erstes Löschen ohne `If-Match` | `428` |
  | erstes Löschen, `If-Match` passt | `204` |
  | erstes Löschen, `If-Match` veraltet | `412` |
  | Wiederholung auf gelöschtes Objekt mit **demselben** ETag wie beim Löschen | `204` (idempotent, Bund AP10) |
  | Wiederholung mit anderem ETag | `412` |
  | Identität durfte das Objekt nie sehen | `404` |

  `GET` liefert danach `404` bzw. `410`, wo das Modul es festlegt.
- Wiederherstellen: `POST /…/{id}/restore` – nur mit Recht (Vorgabe Super-Admin, DB B3).
- Endgültiges Löschen und Fristen laufen über den Dienst, nicht über die API (Ausnahme: sofortige Löschung nach
  Datenschutzrecht über einen eigenen, protokollierten Endpunkt bzw. Ident).
- Veröffentlichte, synchronisierte Daten werden nicht still entfernt: Abnehmer erhalten im Change-Feed ein
  Tombstone-Ereignis (`unpublished`, `deleted`, `merged`).

### B5 Caching und bedingte Abrufe (BESCHLOSSEN für öffentliche Lese-APIs, Glossary/Plattform S8)

- Öffentliche Lese-Endpunkte liefern `ETag` (Prüfsumme des Inhalts) und beantworten `If-None-Match` mit `304`;
  `Cache-Control: public, max-age=60`.
- Antworten mit Organisations- oder Personendaten: `Cache-Control: private, no-store`, kein öffentlicher ETag
  (Glossary DEC-018).
- Öffentliche Antworten, die von der Sprache abhängen, senden `Vary: Accept-Language`; der Cache-Schlüssel enthält
  `locale` (API-E32).
- Datenstand als Kopfzeile `EduKSX-Release`, wo ein Modul Veröffentlichungen kennt.
- **Eigene Kopfzeilen der Plattform** heissen `EduKSX-<Name>` ohne `X-`-Präfix (RFC 6648): `EduKSX-Release`,
  `EduKSX-Organization`, `EduKSX-Signature`. Modul-eigene Kopfzeilen gibt es nicht; das Glossary sendet
  `X-Glossary-Release` bis 1.0 parallel (BESCHLOSSEN 12.11.2026, API-E7).

### B6 Synchronisationsvertrag (BESCHLOSSEN im Glossary, für alle Module mit Abnehmern EMPFOHLEN)

Jedes Modul, dessen Daten andere Systeme regelmässig übernehmen, bietet:

1. **Vollstand** `GET /api/v1/exports` mit `cursor` (letztes Ereignis) und Lizenz.
2. **Änderungen** `GET /api/v1/changes?since=<cursor>` – jede Änderung ein Ereignis mit unveränderlicher `id`
   (= Cursor), `event_type`, `occurred_at` und dem Objekt im veröffentlichten Stand; Rückzüge als Tombstone.
3. Stabile `id`, `revision`, `updated_at` je Objekt; Reihenfolge reproduzierbar; wiederholte Abrufe idempotent.
4. Abnehmer halten einen lokalen Stand, laufen bei Ausfall weiter und ziehen danach lückenlos nach (Referenz:
   Intranet ↔ Glossary, `SYNC-INTRANET.md`).

**Ablauf ohne Lücken (K3, API-E24)** – kein Snapshot auf dem Server nötig, funktioniert auch mit SQLite:

1. **Grenze merken:** Der Abnehmer holt zuerst den aktuellen Cursor (`/releases/latest` bzw. erste Seite von
   `/exports`) und speichert ihn.
2. **Vollstand lesen:** alle Seiten von `/exports` in einen neuen lokalen Stand. Änderungen während des Lesens sind
   erlaubt.
3. **Nachziehen:** `/changes?since=<Grenze>` anwenden – **idempotent über `revision`**: ein Ereignis ersetzt den lokalen
   Eintrag nur, wenn seine `revision` neuer ist; Tombstones entfernen. Was während Schritt 2 geändert wurde, wird so
   sicher korrigiert.
4. **Umschalten:** den neuen Stand atomar aktivieren und den letzten Cursor dauerhaft speichern.

- Cursor sind **mindestens 30 Tage** gültig. Ein älterer Cursor ergibt `410` mit `code: cursor_expired`; der Abnehmer
  beginnt wieder bei Schritt 1.
- Ereignisse haben eine streng steigende `id` je Modul; die Reihenfolge im Feed folgt ihr.
- Organisationsdaten werden je Organisation synchronisiert; ein Cursor gilt nur für die Organisation, für die er
  ausgegeben wurde (W1).

### B7 Ereignisse und Webhooks (BESCHLOSSEN, Plattform S4)

- Ausgehende Ereignisse als **CloudEvents 1.0** JSON, Art `<modul>.<objekt>.<verb>` in Vergangenheitsform
  (`glossary.term.published`, `ident.user.deleted`).
- Signiert mit HMAC-SHA256 über Zeitstempel + Inhalt, Kopfzeile `EduKSX-Signature`; Empfänger weisen Ereignisse älter
  als 5 Minuten ab und verarbeiten idempotent über die Ereignis-`id`.
- Zustellung über eine Ausgangswarteschlange nach dem Commit, mit Wiederholung; Ereignisse enthalten IDs und
  öffentliche/interne Felder, **keine** personenbezogenen Werte (Abnehmer holen sie mit Recht über die API).
- Eingehende Webhooks (z. B. Unterschriften im Intranet) prüfen die Signatur je Anbieter, laufen ohne Token, aber mit
  Abruflimit und eigener Protokollierung.

---

## C · Sicherheit und Datenschutz

### C1 Anmeldung (BESCHLOSSEN, Plattform S1/S2; Übergang EMPFOHLEN)

| Wer ruft auf | Verfahren | Stand |
| --- | --- | --- |
| Öffentlich (veröffentlichte Daten) | ohne Anmeldung | BESCHLOSSEN (Glossary) |
| Person über Oberfläche oder KI-Client | OIDC über Ident (Plattform S1); MCP mit OAuth 2.1 + PKCE + dynamischer Registrierung | BESCHLOSSEN (Ziel) |
| Dienst zu Dienst | OAuth2 Client Credentials, JWT, Prüfung über JWKS, `aud` = Modul (Plattform S2) | BESCHLOSSEN (Ziel) |
| Übergang: Servicekonto des Moduls | eigenes Token (`Bearer`) mit Scopes | BESCHLOSSEN bis Plattform S2 steht |
| Übergang: persönliches Token (Intranet) | Token handelt im Namen der Person, mit Ablauf (API-E3) und feinen Scopes statt `read`/`write`; läuft aus, sobald Ident steht | BESCHLOSSEN 12.11.2026, API-E8 |

- Tokens nur im Kopf `Authorization: Bearer …`, nie in URL, Query oder Cookie für die API.
- **Lesbare Präfixe** je Modul und Art, damit Geheimnis-Scanner sie finden: `<modulschlüssel>_<art>_<zufall>`
  (`glossary_sa_…`, `intranet_pat_…`; Arten `sa` Servicekonto, `pat` persönlich); gespeichert wird nur der Hash,
  angezeigt nur das Präfix (DB B6). Bestehende Präfixe (`sbi_`) gelten bis zum Ablauf der Tokens weiter.
- **Laufzeiten (BESCHLOSSEN 12.11.2026):**

  | Art | Laufzeit |
  | --- | --- |
  | Zugriffstoken aus OIDC/OAuth (Plattform S1, S2), JWT, signiert, mit `aud` | höchstens 10 Minuten, Erneuerung serverseitig |
  | Statisches Token eines Servicekontos, das automatisch erneuert wird | höchstens 90 Tage, Rotation mit Überlappung |
  | Persönliches Token, das automatisch erneuert wird | höchstens 30 Tage |
  | Statisches Token für Abnehmer, die **nicht** automatisch erneuern können (feste Konfiguration, Fremdsystem) | höchstens 12 Monate, Vorgabe 90 Tage; Warnung an die Besitzer 30 und 7 Tage vor Ablauf |

- Jedes Token hat Name, Besitz, Scopes, Ablaufdatum, letzten Gebrauch (als Datum) und ist jederzeit widerrufbar.
  Anlegen, Ändern, Widerrufen schreibt ins Sicherheitsprotokoll (DB A7).
- Nach RFC 9700 und der Security Guideline des Bundes: nur Authorization Code mit PKCE bzw. Client Credentials, keine
  Implicit- und Password-Grants; Tokens mit Zielgruppe (`aud`) und Prüfung von Signatur, Gültigkeit und Zweck.
  An den Absender gebundene Tokens (DPoP, RFC 9449, oder mTLS, RFC 8705) für Dienst-zu-Dienst-Zugriffe mit
  Personendaten: ZU PRÜFEN mit Ident (Entscheid beim Bau von Ident, #16; Variantenvergleich und Empfehlung:
  [Prüfauftrag DPoP/mTLS](PRUEFAUFTRAG-DPOP-MTLS.md)).
- Ein statisches Token allein reicht nie für privilegierte Vorgänge (Konten, Rollen, Löschen nach Datenschutzrecht,
  Plattform-Administration). Dafür gilt (W4, API-E25):
  - **Menschen:** zweiter Faktor, der **höchstens 15 Minuten** alt ist (`auth_time`, sonst Neuanmeldung über Ident mit
    `max_age`/`acr_values` – Step-up).
  - **Servicekonten:** eine eigene technische Identität nur für diesen Zweck, eigener Scope, Laufzeit höchstens
    90 Tage, jeder Aufruf im Sicherheitsprotokoll. Vier-Augen-Freigabe legt das Modul fest, wo es nötig ist.
  - **Bis Ident steht:** privilegierte Vorgänge nur in der Oberfläche mit Anmeldung, **nicht per API-Token**
    (BESCHLOSSEN 13.11.2026, API-E34). Bestehende API-Endpunkte für Konten und Rollen werden bis dahin auf Recht und Scope
    beschränkt oder abgeschaltet.
- Servicekonten sind eigene Identitäten, nie Benutzerkonten (DB B4).

### C2 Rechte und Scopes (EMPFOHLEN, Grundlage DB B4 und Plattform S2)

- Scopes heissen **`<modul>:<ressource>.<aktion>`** (W6, API-E19): Modulschlüssel (G2), Ressource wie im Pfad (Plural,
  `kebab-case`), Aktion **nur** `read`, `write`, `delete` oder `admin`. Beispiele: `glossary:terms.read`,
  `glossary:proposals.write`, `intranet:people.delete`.
- Die **Organisation steckt nicht im Scope-Namen**: `glossary:terms.read` mit dem Token einer Organisation liefert deren
  Sicht (C3). Damit entfällt `read-org`; das Glossary stellt in der Vorschau um.
- Geprüft wird **Scope des Tokens UND Recht der Identität** auf das konkrete Objekt (Policy) – der Scope begrenzt,
  er gewährt nie mehr. Rechte, nie Rollennamen (DB B4). Jeder Zugriff auf ein Objekt über eine ID prüft das Recht auf
  **dieses** Objekt (OWASP API1, BOLA), jede Funktion das Recht auf die Funktion (API5, BFLA).
- Rollen und Organisation kommen aus der Anmeldung bzw. dem Token, nie aus Angaben des Clients im Body oder in
  Kopfzeilen ohne Prüfung (Bund Security Guideline 3.2).
- Jeder Endpunkt nennt in der OpenAPI-Beschreibung seine Scopes (`security`) und das nötige Recht
  (`x-eduksx-ability`).
- Ein Token berechtigt nie zur Veröffentlichung oder zu Rechteänderungen, ausser das Modul hat dafür einen eigenen,
  eng begrenzten Scope beschlossen (Glossary DEC-017). KI-Werkzeuge veröffentlichen nie ohne Prüfung durch Menschen.
- Privilegierte Vorgänge über die API nur mit frischem zweitem Faktor bzw. eigenem Servicekonto (C1).

### C3 Mandanten (BESCHLOSSEN, DB B1; API-Regeln EMPFOHLEN)

- Die Organisation kommt **aus dem Token** (Servicekonto der Organisation bzw. gewählte Organisation der Person mit
  Kopfzeile `EduKSX-Organization`, geprüft gegen die Mitgliedschaft) – nie aus einer frei wählbaren ID im Pfad oder
  Body.
- Ohne Mandantenkontext liefern Endpunkte für Organisationsdaten `403`, nie alles. Objekte fremder Organisationen
  ergeben `404`.
- Öffentliche Endpunkte enthalten nie Organisations- oder persönliche Anpassungen (Glossary DEC-018).
- Plattform-Administration über einen eigenen, protokollierten Weg (`/api/v1/admin/…`), nicht über Parameter.
- **Mandantenkontext** (W1, API-E32): Die Middleware leitet aus der geprüften Identität einen unveränderlichen Kontext ab
  (Organisation, Identität, Scopes); er gilt für die ganze Anfrage. Die Organisation gehört in **jeden** Schlüssel, der
  Daten trennt: Cache, Idempotenz (B3), Cursor (B6), Export und Audit. Aufträge tragen sie in ihrer Nutzlast;
  Datenbankzugriffe ohne Kontext werfen eine Exception (DB B1).

### C4 Datenklassen und Veröffentlichungsgrenze (BESCHLOSSEN, DB B2, Glossary DEC-018)

| Datenklasse | In der API |
| --- | --- |
| öffentlich | öffentliche Endpunkte, Exporte, Change-Feed |
| intern | nur angemeldet mit Recht |
| personenbezogen | nur angemeldet mit Recht auf die Person; nie in öffentlichen Ausgaben, Ereignissen, Logs, Beispielen |
| besonders schützenswert | nur eigene, ausdrücklich beschlossene Endpunkte; nie über MCP an externe KI-Anbieter |
| geheim | nie – auch nicht gehasht, auch nicht für Admins |

- Jede Ressource hat einen **Presenter mit Positivliste** je Zweck (öffentlich, Organisation, Admin). Neue Spalten
  erscheinen erst, wenn sie dort eingetragen sind.
- Ebenso gibt es je Operation eine **Positivliste der schreibbaren Felder** (Validierungsregeln, nie
  `$request->all()` ins Modell). Felder wie `role`, `organization_id`, `status`, `is_active` sind nur über eigene,
  berechtigte Operationen änderbar (OWASP API3, Mass Assignment).
- Ein Test füllt Testdaten mit privaten Werten und Geheimnissen und prüft, dass sie in keiner öffentlichen Antwort,
  keinem Export, keinem Feed, keinem Beispiel der Beschreibung und keinem Pages-Build erscheinen.
- Personendaten nie als Pfad (keine E-Mail als ID). Suche nach Personen mit `GET /people?q=` ist erlaubt; Protokolle,
  Fehlermeldungen und Weiterleitungen **maskieren** die Werte von `q`/`search` und Filtern mit Personendaten.
  Browser-Clients nutzen `POST /people/search`, damit Suchbegriffe nicht im Verlauf landen (BESCHLOSSEN 12.11.2026, API-E15).
- **Datenklassen je Operation** (W3, API-E26): Jede Operation nennt in der Beschreibung die Datenklassen, die sie liest
  oder schreibt (`x-eduksx-data-classes: [public, internal, personal]`). Der Linter verlangt die Angabe ab Stufe 2.
- **MCP und externe KI:** Ein MCP-Werkzeug übernimmt die Datenklassen seiner Operation. An externe KI-Anbieter dürfen
  `public` und `internal`; `personal` nur mit Vertrag zur Auftragsbearbeitung **und** Freigabe je Werkzeug;
  `sensitive` und `secret` nie – auch nicht zusammengefasst oder umschrieben (Intranet KONZEPT-MCP, IDG ZH).

### C5 Abruflimits und Missbrauch (BESCHLOSSEN 120/Min., Glossary; Rest EMPFOHLEN)

- Vorgabe **120 Abrufe pro Minute** je Adresse (öffentlich) bzw. je Token (angemeldet); Anmeldung und Token-Anlage
  enger (10/Min.). Darüber `429` mit `Retry-After`.
- Antworten tragen `Retry-After` bei `429`/`503` (Standard). Die Kopfzeilen `RateLimit` und `RateLimit-Policy`
  folgen dem IETF-Entwurf (draft-ietf-httpapi-ratelimit-headers-11, noch kein RFC) – EMPFOHLEN, sobald der Entwurf
  stabil ist; bis dahin nicht als Vertrag zusichern. Die älteren Felder `RateLimit-Limit/-Remaining/-Reset` (frühere
  Entwürfe, Laravel-Vorgabe `X-RateLimit-*`) werden nicht dokumentiert.
- Neben Abrufen pro Minute auch Grenzen für teure Vorgänge (Export, Suche, Import) und für sensible Abläufe
  (Anmeldung, Einladungen, Bestellungen, Vorschläge) – OWASP API4 und API6.
- Grösse: Body höchstens 1 MB (Uploads über eigene Endpunkte mit eigener Grenze), höchstens 200 Einträge je Seite.
- Sperren je Adresse oder Token möglich; Cloudflare-Regeln vor öffentlichen Endpunkten.

### C6 CORS und Browser (BESCHLOSSEN für Lesen, Glossary)

- Öffentliche `GET`-Endpunkte: `Access-Control-Allow-Origin: *`, ohne Cookies.
- Schreibende Endpunkte: nur Herkünfte aus einer Liste je Instanz, mit Preflight; nie `*` mit Anmeldedaten.
- Sicherheitskopfzeilen für alle Antworten: `X-Content-Type-Options: nosniff`, `Strict-Transport-Security`; die API
  setzt keine Sitzungscookies.

### C7 Protokollierung (EMPFOHLEN, Grundlage Plattform §6 und DB A7)

- Jede Anfrage bekommt eine `request_id` (eingehend `X-Request-Id` übernehmen, sonst erzeugen), zurück in der
  Kopfzeile und in Fehlern; dieselbe ID steht in Historie und Protokoll.
- Protokolle als JSON: Zeit (UTC, synchronisiert), Methode, Pfad **ohne Query-Werte**, Status, Dauer, Quell-Adresse,
  Token-Präfix bzw. Servicekonto, Organisation – keine Bodies, keine Tokens, keine Personendaten. Einheitlicher
  Aufbau für die Auswertung in einem SIEM (Bund Security Guideline 3.4).
- Warnungen bei Mustern: viele `401`/`403` je Token oder Adresse, Rechteänderungen, ungewöhnlich grosse Exporte,
  Zugriffe auf viele verschiedene IDs in kurzer Zeit (Hinweis auf BOLA-Versuche).
- Das Sicherheitsprotokoll ist manipulationsgeschützt (Hash-Verkettung, DB A7).

### C8 Abgleich OWASP API Security Top 10 (2023) (EMPFOHLEN)

| Risiko | Massnahme im Standard |
| --- | --- |
| API1 Zugriff auf fremde Objekte (BOLA) | Policy je Objekt, fremde Organisation → `404` (C2, C3); Test mit zwei Organisationen (D7) |
| API2 Fehlerhafte Anmeldung | OIDC/OAuth nach RFC 9700, Laufzeiten, Hash-Speicherung, Abruflimit auf Anmeldung (C1, C5) |
| API3 Zugriff auf Objekt-Eigenschaften (inkl. Mass Assignment) | Positivlisten für Lesen **und** Schreiben (C4) |
| API4 Unbegrenzter Ressourcenverbrauch | Limits je Minute, Seitengrösse, Body-Grösse, teure Vorgänge, Zeitlimits (A5, C5) |
| API5 Fehlende Prüfung auf Funktionen (BFLA) | Recht je Operation in der Beschreibung (`x-eduksx-ability`), Admin-Pfade getrennt (C2, C3) |
| API6 Missbrauch sensibler Abläufe | eigene Grenzen für Anmeldung, Einladungen, Bestellungen, Vorschläge (C5) |
| API7 SSRF | Webhook- und Import-URLs nur HTTPS, keine internen Adressen (privat, Loopback, Link-Local, Metadaten), Ziel nach Auflösung erneut prüfen, keine Weiterleitungen folgen |
| API8 Fehlkonfiguration | Sicherheitskopfzeilen, CORS-Liste, keine Debug-Ausgaben, einheitliche Fehler (A6, C6) |
| API9 Fehlende Übersicht über APIs | Steckbrief `/.well-known/eduksx-module.json`, OpenAPI je Version, Abschaltung alter Versionen mit Sunset und Nutzungsmessung (D1, D6) |
| API10 Unsicherer Umgang mit fremden APIs | Antworten fremder Systeme (Plugins, Sync) gegen Schema prüfen, Zeitlimits, keine Weiterleitungen über fremde Hosts, Daten als nicht vertrauenswürdig behandeln |

### C9 Datenschutz nach DSGVO und IDG (BESCHLOSSEN 13.11.2026, API-E26–API-E29)

Die API ist so gebaut, dass ein Modul die Pflichten nach DSGVO und IDG (Kanton Zürich) erfüllen kann, ohne sie nachzurüsten.
Vor dem ersten produktiven Release liest die bzw. der Datenschutzverantwortliche diese Regeln gegen (ZU PRÜFEN, #22).

| Pflicht | Regel |
| --- | --- |
| Zweckbindung, Datensparsamkeit | Jede Operation nennt ihren Zweck (`x-eduksx-purpose`, ein Satz) und ihre Datenklassen (C4); Antworten nur mit nötigen Feldern, mehr mit `?fields=` und Recht (A2) |
| Verzeichnis der Bearbeitungen (Art. 30 DSGVO; Verzeichnis nach IDG) | Ein Werkzeug in `eduksx/core` erzeugt aus der Beschreibung je Modul eine Übersicht: Operationen, Zweck, Datenklassen, Empfänger (Scopes, MCP). Sie ist Teil der Release-Unterlagen |
| Auskunft und Datenübertragbarkeit (Art. 15, 20 DSGVO; Auskunftsrecht nach IDG) | Jedes Modul mit Personendaten bietet `GET /api/v1/me/data-export`: alle Daten zur angemeldeten Person, maschinenlesbar (JSON), als Auftrag (`202`), Download höchstens 7 Tage |
| Löschung (Art. 17 DSGVO) | über Ident: Ereignis `ident.user.deleted` → Modul pseudonymisiert bzw. löscht nach DB B3 inkl. Löschregister; Bestätigung im Sicherheitsprotokoll |
| Fristen | API-Protokolle 90 Tage, Idempotenz-Speicher 24 Stunden, Datenexporte 7 Tage, Cursor 30 Tage (enthalten keine Personendaten) |
| Datenort | Betrieb, Sicherungen, Protokolle und Unterauftragnehmer nur in der Schweiz oder der EU; externe KI nur nach C4 |
| Datenschutz durch Technik | Positivlisten (C4), Maskierung im Protokoll (C7), keine Personendaten in Ereignissen (B7), Mandantentrennung (C3) |
| Folgenabschätzung | Für Operationen mit `sensitive` hält das Modul eine Datenschutz-Folgenabschätzung bzw. Vorabkontrolle (IDG) fest, bevor sie produktiv geht |

### C10 Sicherheitsnachweis und Penetrationstest (BESCHLOSSEN 13.11.2026, API-E30)

Ziel: Ein Penetrationstest ergibt **keine offenen Befunde**. Der Weg dorthin ist so gebaut, dass Befunde früh und
automatisch auffallen:

1. **Prüfziel OWASP ASVS 5.0, Level 2** für jedes Modul ab Stufe 2. Die Anforderungen, die die API betreffen, sind in
   diesem Standard abgebildet (A–D); der Konformitätstest (D8) prüft sie, soweit automatisierbar.
2. **Automatischer Scan:** ZAP-API-Scan gegen die Staging-Umgebung mit der OpenAPI-Beschreibung, in der CI vor jedem
   Release; Befunde «hoch» und «mittel» stoppen das Release.
3. **Externer Penetrationstest** vor dem ersten produktiven Release jedes Moduls und nach grossen Änderungen an
   Anmeldung, Rechten oder Mandantentrennung. Befunde «kritisch», «hoch» und «mittel» sind vor dem Go-live behoben und
   nachgetestet; «tief» mit Termin. Akzeptierte Restrisiken nur mit Eintrag im Ausnahmeregister (D8).
4. **Grundhärtung** (Stufe 1): nur TLS 1.2 oder höher, keine Versionsangaben in Kopfzeilen (`Server`, `X-Powered-By`),
   keine Debug-Ausgaben, gleiche Antwort für «gibt es nicht» und «darfst du nicht sehen» (A7), Abhängigkeiten mit
   Sicherheitsprüfung in der CI (CodeQL, Abhängigkeitswarnungen).

---

## D · Lebenszyklus

### D1 Versionierung (BESCHLOSSEN, Glossary DEC-016 und Plattform §5)

- Hauptversion im Pfad (`/api/v1`). In einer Version **dürfen dazukommen:** Endpunkte, optionale Parameter, Felder,
  neue Werte bei Aufzählungen. **Nicht erlaubt:** entfernen, umbenennen, Bedeutung oder Typ ändern, Pflichtfeld neu
  einführen, Vorgaben ändern, Fehlercodes (`code`) ändern.
- Brüche nur in `/api/v2`; die alte Version läuft **mindestens 12 Monate** parallel; Ankündigung im CHANGELOG, auf
  `/api/docs` und mit `Deprecation` (RFC 9745, Standard seit 03/2025) und `Sunset` (RFC 8594), dazu
  `Link: <…>; rel="deprecation"`. `Sunset` liegt nie vor `Deprecation`.
- Die Nutzung abgelöster Versionen und Endpunkte wird gemessen (je Servicekonto); abgeschaltet wird erst, wenn bekannte
  Abnehmer umgestellt haben oder informiert wurden (Zalando #185, #188).
- **Vorschau:** Bis zum ersten produktiven Betrieb eines Moduls ist seine API eine Vorschau und darf sich mit Eintrag
  im CHANGELOG ändern; das steht in `info.description` und auf `/api/docs`. Danach gilt die Zusage ohne Ausnahme
  (analog DB A5).
- `info.version` der Beschreibung folgt der App-Version; Erweiterungen erhöhen MINOR.

### D2 Pflichten der Abnehmer (BESCHLOSSEN, Glossary DEC-016)

Unbekannte Felder und Aufzählungswerte ignorieren (bei Sicherheitsentscheiden als «verweigert» werten, A2),
Weiterleitungen `301` nur bei `GET`/`HEAD` automatisch folgen, `Retry-After` beachten, ETag
nutzen, einen lokalen Stand halten und bei Ausfall weiterlaufen. Das steht in jeder API-Doku unter «Nutzung und
Stabilität».

### D3 OpenAPI-Beschreibung (BESCHLOSSEN, Glossary/Intranet/Plattform S8; Details EMPFOHLEN)

- **OpenAPI 3.1**, ausgeliefert unter `/api/openapi.json` (JSON ist gültiges YAML), als **eine** eigenständige Datei
  ohne externe Verweise (Zalando #101).
- **Vertrag zuerst** (BESCHLOSSEN 12.11.2026, API-E11): Neue Module schreiben die Beschreibung als Datei
  (`openapi/<modul>-v1.json` bzw. `.yaml`) vor dem Code und prüfen den Code dagegen. Das Intranet erzeugt sie bis zu
  einem Umbau weiter aus `App\Support\OpenApi`. In beiden Fällen gelten die Prüfung Route ↔ Beschreibung und der
  Linter.
- Deutsche Begriffe und Beschreibungen nach A8 (`title`, `description`, `x-eduksx-labels`).
- Jede Operation hat `operationId` (englisch, `camelCase`, Verb + Objekt: `listTerms`, `createPerson`), eindeutig im
  Modul – daraus entstehen MCP-Werkzeugnamen mit Modulschlüssel (`glossary_list_terms`, G2) und Postman-Einträge.
- `info.x-eduksx-module` nennt den Modulschlüssel, `info.x-eduksx-api-standard` die Version dieses Standards (`1.1`).
- Jeder Parameter hat ein `example`, jeder schreibende Endpunkt einen Beispiel-Body, nur mit erfundenen Werten
  (`…@sekbuelach.example`, BESCHLOSSEN Intranet 04.11.2026). Beschreibungen und Beispiele ohne Entscheidnummern und
  ohne echte Personen- oder Organisationsnamen.
- Schemas wiederverwenden (`components`); `Problem` gemeinsam für alle Fehler; je Operation `security`,
  `x-eduksx-ability`, ab Stufe 2 `x-eduksx-data-classes` und `x-eduksx-purpose` (C9); Lizenz in `info.license`.
- **Tests:** jede Route unter `/api/v1` steht in der Beschreibung und umgekehrt; Antworten der Feature-Tests werden
  gegen das Schema geprüft; die Beschreibung ist gültiges OpenAPI 3.1.
- **Linter in der CI:** Spectral (bzw. Redocly CLI) mit einem gemeinsamen Regelsatz `eduksx` in `eduksx/core`, der
  diesen Standard prüft (Namen, `operationId`, Beispiele, `security`, `format`, Problem-Antworten). Ausgangspunkt:
  offene Regelsätze nach Zalando/OTTO, angepasst an die Abweichungen unten. Zuerst als Warnung, ab dem folgenden
  Release als Fehler. Neue Abhängigkeit → Eintrag in `third-party.json` (BESCHLOSSEN 12.11.2026, API-E12).
- **Brechende Änderungen automatisch erkennen:** die Beschreibung jedes Pull Requests wird mit `main` verglichen
  mit `oasdiff breaking`; ein Bruch in einer bestehenden Version lässt die CI scheitern, während der Vorschau nur
  Warnung. Vor dem Einsatz Lizenz und Pflege prüfen und in `third-party.json` eintragen (BESCHLOSSEN 12.11.2026, API-E13).
- **Client:** Für eigene Oberflächen wird aus der Beschreibung ein TypeScript-Client erzeugt
  (WebApplicationProgrammingGuide); Vertrag und Client werden im selben Pull Request geprüft.
- Gemeinsame Schemas (Problem, Pagination, Ereignis, Lizenz) liegen zentral in `eduksx/core` und werden nicht je Modul
  neu erfunden. Die Schemas der Plattform-Schnittstellen (Ereignis, Steckbrief, `/health`, Claims) werden in
  [`spec/`](../spec/README.md) gepflegt; Core liefert sie aus (#3, Core C11).

### D4 Doku und Werkzeuge (BESCHLOSSEN, Plattform S8)

- **Pflicht:** `/api/docs` mit **Scalar** (ohne Telemetrie, ohne fremde Schriften, mit Ausprobieren) und
  `/api/postman.json` (Postman v2.1, aus der Beschreibung erzeugt, Prüfung in der CI). **Freiwillig:** `/api/swagger`
  (BESCHLOSSEN 12.11.2026, API-E16; ändert Plattform S8).
- Die Doku enthält: Anmeldung und Token-Anlage, Abruflimits, Nutzung und Stabilität, Lizenz der Daten,
  Synchronisationsablauf mit Beispiel, Fehlerschlüssel.
- Änderungen an der API stehen im CHANGELOG des Moduls unter «Unveröffentlicht» (Abschnitt «API»).

### D5 MCP (BESCHLOSSEN in Glossary und Intranet; Regeln EMPFOHLEN)

- Der MCP-Server ist ein **Adapter auf dieselben Services** wie die API, ohne eigenen Datenbankzugriff; Werkzeuge
  werden aus der OpenAPI-Beschreibung abgeleitet (Intranet `McpConcept`).
- Jedes Werkzeug trägt MCP-Annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint=false`)
  – Hinweise, keine Sicherheitsgrenze.
- Einführung in Phasen: lesen → lesen mit Personendaten → schreiben (als Vorschlag bzw. mit Bestätigung) → löschen.
  Jede Phase braucht einen eigenen Entscheid.
- Historie mit `source = mcp` und Client-Name.
- Werkzeugnamen tragen den Modulschlüssel (`glossary_list_terms`), damit mehrere EduKSX-Server in einem KI-Client
  nebeneinander laufen. Externe KI nur nach den Datenklassen (C4).

### D6 Betrieb (BESCHLOSSEN, Plattform S5/§6)

- `/up` = **lebt** (Liveness: Prozess antwortet, ohne Abhängigkeiten zu prüfen); `/health` = **bereit** (Readiness:
  Datenbank, Migrationen, Warteschlange, Speicher, Ident; erst dann nimmt der Dienst Anfragen an); `/metrics` nur mit
  Berechtigung (Plattform S5).
- Steckbrief `/.well-known/eduksx-module.json` mit Modulschlüssel, API-Versionen, Scopes und Version dieses Standards.
- JSON-Protokolle mit `request_id`; sauberes Herunterfahren (laufende Anfragen und Aufträge beenden); Wartung mit
  `503` und `Retry-After`.
- Wiederanlauf, Sicherung, RPO/RTO und Löschregister nach DB C2 und B3; nach einer Wiederherstellung meldet `/health`
  erst «bereit», wenn das Löschregister angewendet ist.

### D7 Tests (BESCHLOSSEN 12.11.2026, API-E17 – abgestuft)

**Prototypen und Stufe 1** (z. B. Intranet mit JSON-Speicher) haben mindestens: Route ↔ Beschreibung; Fehlerformat; Scope **und**
Recht; Veröffentlichungsgrenze mit privaten Testdaten (C4); Schutz der schreibbaren Felder (Mass Assignment).

**Vor dem produktiven Betrieb** hat jedes Modul zusätzlich: Route ↔ Beschreibung vollständig; Antworten gegen Schema; Fehlerformat für 401, 403, 404,
409/412, 422, 429; Scope **und** Recht (Token mit zu wenig Scope, Person ohne Recht); **Mandantentrennung** mit zwei
Organisationen über alle Endpunkte, Exporte und Feeds (DB B1); Veröffentlichungsgrenze mit privaten Testdaten (C4);
ETag/304, starker ETag und `If-Match`/412; Idempotency-Key (alle fünf Fälle aus B3, auch nach Token-Erneuerung);
alle Fälle von `DELETE` aus B4;
**Mass Assignment** (geschützte Felder im Body werden abgelehnt); SSRF-Prüfung für Webhook-URLs; Cursor stabil über
Seiten; Synchronisation mit Rückzug und
Wiederaufnahme nach Ausfall und abgelaufenem Cursor (B6); Historie mit `source = api`; Abruflimit; keine Tokens und
Personendaten im Protokoll; Auskunft `/me/data-export` vollständig; ZAP-Scan ohne Befunde «hoch»/«mittel» (C10).

### D8 Konformität und Governance (BESCHLOSSEN 13.11.2026, API-E33)

Schlank gehalten – keine Gremien, sondern Prüfungen, die automatisch laufen:

- **Konformitätstest** aus `eduksx/core`: ein Testpaket, das jedes Modul in seiner CI ausführt. Es prüft die
  Beschreibung (Linter), ruft die laufende API in Tests auf (Fehlerformat, Kopfzeilen, Cursor, ETag, Abruflimit,
  Sicherheitskopfzeilen) und meldet die erfüllte Stufe. Auch KI-Agenten führen ihn vor jedem Pull Request aus.
- **Register in diesem Dokument:** Modulschlüssel (G2) und **Ausnahmen**: Modul, Regel, Grund, Ablaufdatum,
  zuständige Person. Eine Ausnahme ohne Ablaufdatum gibt es nicht; abgelaufene Ausnahmen lassen den
  Konformitätstest scheitern.
- **Version im Steckbrief:** Jedes Modul nennt die Version dieses Standards, die es erfüllt; neue Versionen des
  Standards gelten ab dem nächsten MINOR-Release des Moduls.

**Ausnahmeregister**

| Modul | Regel | Grund | Bis | Zuständig |
| --- | --- | --- | --- | --- |
| `intranet` | D3 Vertrag zuerst | Beschreibung wird aus dem Code erzeugt (API-E11) | Umbau des Intranets | Projektverantwortliche:r |
| `glossary` | B5 Kopfzeilen | `X-Glossary-Release` parallel zu `EduKSX-Release` (API-E7) | Release 1.0 | Projektverantwortliche:r |

---

## Checkliste für Pull Requests mit API-Änderung

Was in einem PR geprüft wird, richtet sich nach der Stufe des Moduls (G1); der Konformitätstest (D8) deckt die
markierten Punkte (⚙) automatisch ab.

- [ ] Standard deckt die Änderung ab – sonst zuerst Konzept-PR; Ausnahme nur mit Eintrag im Register (D8)
- [ ] Neue Fachfunktion der Oberfläche hat eine API-Operation mit demselben Service und derselben Policy; Web-Route nennt die `operationId`; interne Operationen mit `x-eduksx-internal` (G4) ⚙
- [ ] Modulschlüssel in Scopes, Ereignissen, Fehler-Typen, Token-Präfix und MCP-Namen (G2) ⚙
- [ ] Gemeinsame Bausteine aus `eduksx/core` statt eigener Umsetzung (G3)
- [ ] URL, Felder und Werte englisch `snake_case` (A1, A2), Werte identisch zur Datenbank
- [ ] Deutscher Begriff und Beschreibung je Schema, Feld und Parameter, Labels je Aufzählungswert (A8), gleich wie im Datenmodell
- [ ] Datum ISO 8601 UTC, Sprache über `locale`, Rückfall erkennbar (A3, A4)
- [ ] Liste begrenzt, Cursor als Standard, Reihenfolge stabil, `total` nur auf Anfrage (A5)
- [ ] Aufzählungen erweiterbar, Zahlen mit `format`, keine `null`-Listen oder -Booleans (A2)
- [ ] Fehler als `problem+json` mit `code`; richtige Statuscodes (A6, A7)
- [ ] Schreiben im Service, eine Transaktion, Historie mit `source = api`, starker ETag mit `If-Match` (B1, B2) ⚙
- [ ] `Idempotency-Key` für anlegende `POST`; Löschen über Papierkorb, Tombstone im Feed (B3, B4)
- [ ] Scope und Recht geprüft, Organisation aus dem Token, fremde Objekte `404` (C2, C3)
- [ ] Presenter mit Positivliste, schreibbare Felder als Positivliste, Datenklassen und Zweck je Operation (C4, C9)
- [ ] OWASP-Abgleich für neue Endpunkte (C8), insbesondere externe URLs (SSRF) und fremde Antworten
- [ ] Abruflimit, CORS, keine Personendaten in URL oder Protokoll (C5–C7)
- [ ] Nichts entfernt oder umbenannt in einer bestehenden Version; sonst `v2` mit Deprecation (D1)
- [ ] OpenAPI nachgeführt: `operationId`, Beispiele, `security`, Recht; Linter grün, kein Bruch; Postman neu erzeugt (D3, D4)
- [ ] MCP-Werkzeug mit Annotations, falls die Operation freigegeben ist (D5)
- [ ] Tests nach D7, Konformitätstest grün; vor dem ersten Release: ZAP-Scan, Pentest (C10); CHANGELOG «API» nachgeführt

## Entscheide

API-E1–API-E17 entschieden am 12.11.2026, API-E18–API-E35 am 13.11.2026 nach dem Architektur-Review (Chat mit Projektverantwortliche:r).

| Nr. | Frage | Entscheid | Abschnitt |
| --- | --- | --- | --- |
| API-E1 | Pagination | Cursor Standard, Seiten für kleine Admin-Listen, `total` nur auf Anfrage | A5 |
| API-E2 | Wiederholtes `DELETE` | `204` (idempotent, Bund AP10) | B4 |
| API-E3 | Laufzeit von Tokens | kurz (10 Min. / 30 / 90 Tage); bis 12 Monate nur, wenn der Abnehmer nicht automatisch erneuern kann | C1 |
| API-E4 | Umstellung Pagination | Intranet und Glossary `/terms` auf Cursor; Intranet sofort, Glossary in der Vorschau vor 1.0 | A5 |
| API-E5 | Fehlerformat | `problem+json` überall, Intranet stellt um (ohne v2, Prototyp) | A6 |
| API-E6 | Gleichzeitige Änderungen | `If-Match` Standard (412/428), `lock_version` im Body erlaubt (409) | B2 |
| API-E7 | Kopfzeilen | einheitlich `EduKSX-*`; `X-Glossary-Release` bis 1.0 parallel | B5 |
| API-E8 | Persönliche Tokens | bleiben bis Ident steht, mit Ablauf und feinen Scopes | C1 |
| API-E9 | Statuswerte | englischer Wert wie in der Datenbank, dazu `<feld>_label`; Glossary passt Beispiel und API an | A2 |
| API-E10 | Ablage | EduKSX-Architektur `docs/KONZEPT-API-GUIDELINE.md` (Quelle); Verweise aus Glossary, Intranet und WebApplicationProgrammingGuide (schliesst dort API-01, SEC-01 für externe Clients); Kopie im claude.ai-Projekt | – |
| API-E11 | Entstehung der Beschreibung | Vertrag zuerst für neue Module; Intranet bis zum Umbau aus dem Code | D3 |
| API-E12 | Linter | eigener Spectral-Regelsatz `eduksx` in `eduksx/core`, zuerst Warnung, dann Fehler | D3 |
| API-E13 | Brüche erkennen | `oasdiff` in der CI nach Lizenzprüfung; während der Vorschau Warnung | D3 |
| API-E14 | Content-Type bei `PATCH` | `application/merge-patch+json` und `application/json` gleich | B1 |
| API-E15 | Personensuche | `GET ?q=` erlaubt, Protokoll maskiert; Browser nutzen `POST …/search` | C4 |
| API-E16 | Doku-Seiten | Scalar und Postman Pflicht, Swagger freiwillig (Plattform S8 angepasst) | D4 |
| API-E17 | Tests | abgestuft: Mindestumfang für Prototypen, volle Liste vor produktivem Betrieb | D7 |
| API-E18 | Schlanke Umsetzung | Stufen (Kern, Betrieb, bei Bedarf) und gemeinsame Bausteine | Grundsatz 7, G1 |
| API-E19 | Suite und Namen | registrierter Modulschlüssel als Namensraum; Scopes `<modul>:<ressource>.<aktion>` (ersetzt `read-org`) | G2, C2 |
| API-E20 | `eduksx/core` | vier Bausteingruppen, jeweils erst beim ersten Bedarf | G3 |
| API-E21 | ETag (K1) | starker ETag `"<id>.<lock_version>"` = Stand des Objekts | B2 |
| API-E22 | Idempotenz-Bereich (W2) | Organisation + Identität + Operation; Fingerabdruck SHA-256 | B3 |
| API-E23 | `DELETE` (K2) | Wiederholung mit gleichem ETag → `204`, anderer ETag → `412` | B4 |
| API-E24 | Sync (K3) | Grenze merken, Vollstand, idempotent nachziehen, atomar umschalten; Cursor 30 Tage | B6 |
| API-E25 | Privilegierte Zugriffe (W4) | zweiter Faktor höchstens 15 Min. alt; eigene Servicekonten; Vier-Augen je Modul | C1 |
| API-E26 | Datenklassen und MCP (W3) | `x-eduksx-data-classes` je Operation; extern nur `public`/`internal`, `personal` mit AVV und Freigabe | C4, C9 |
| API-E27 | Verzeichnis | aus OpenAPI erzeugt | C9 |
| API-E28 | Auskunft | `GET /api/v1/me/data-export` je Modul mit Personendaten | C9 |
| API-E29 | Fristen, Datenort, Sparsamkeit | Protokolle 90 Tage; CH/EU; `?fields=` | C9, A2 |
| API-E30 | Sicherheitsnachweis | ASVS 5.0 L2, ZAP-Scan in der CI, externer Pentest vor erstem Release | C10 |
| API-E31 | Stufen-Einteilung | wie Tabelle G1 | G1 |
| API-E32 | Kleine Korrekturen | Mandantenkontext, `null`/Aufzählungen, `Vary`, `301`/`308`, Dezimalzahlen, Betrieb | A2, A4, A7, B5, C3, D6 |
| API-E33 | Governance | Konformitätstest, Register für Module und Ausnahmen, Version im Steckbrief | D8 |
| API-E34 | Privilegierte Vorgänge vor Ident | nur in der Oberfläche, nicht per API-Token | C1 |
| API-E35 | Rechtssammlung | gehört zum Modul `codex` | G2 |
| API-E37 | Deutsche Beschreibungen zu englischen Namen | `title`/`description` je Schema, Feld, Parameter; `x-eduksx-labels` je Aufzählung; Texte gleich wie im Datenmodell (DB-E13) | A8 |
| API-E38 | API-First | Stufen A (Vertrag zuerst) und B (jede Fachfunktion als API, gleicher Service und gleiche Policy) verbindlich, C (headless) erlaubt; automatische Prüfung Route ↔ `operationId`; interne APIs mit `x-eduksx-internal` (22.11.2026, #72) | G4 |
| API-E36 | Ein Register für DB und API | [REGISTER-MODULE.md](REGISTER-MODULE.md); Schlüssel englisch, Marketingnamen frei; `timetable`, `ops` neu vergeben | G2 |
| – | Datenschutzregeln C9 rechtlich gegenlesen | vor dem ersten produktiven Release (#22) | C9 – ZU PRÜFEN |
| – | DPoP/mTLS für Dienst-zu-Dienst | mit Ident prüfen (#16); empfohlen: kurze JWT mit `private_key_jwt` ab Stufe 1, DPoP vor mTLS sobald Ident es kann ([Prüfauftrag](PRUEFAUFTRAG-DPOP-MTLS.md)); Entscheid #35 | C1 – ZU PRÜFEN |

## Abweichungen heute (Ist-Stand 13.11.2026)

| Thema | Glossary | Intranet | Standard |
| --- | --- | --- | --- |
| Fehler | `problem+json` ✓ | `{"message": …}` | `problem+json` (API-E5) |
| Hülle | `{"data": …}` ✓ (Beispiel im Konzept veraltet) | `{"data": …}` ✓ | `{"data": …}` |
| Pagination | `page`/`per_page` mit `total`; Cursor im Feed ✓ | `limit`/`offset`, `meta.total` | Cursor (API-E1, API-E4) |
| Statuswerte | Beispiel zeigt `"aktuell"` | – | englisch + `_label` (API-E9) |
| Kopfzeilen | `X-Glossary-Release` | – | `EduKSX-Release` (API-E7) |
| Konflikte | – | – | `If-Match` (API-E6) |
| Wiederholtes `DELETE` | – | `404` | `204` (API-E2) |
| Token-Laufzeit | Servicekonten mit Ablauf | persönliche Tokens | C1 (API-E3) |
| ETag/304 | ✓ | – | öffentliche Lese-Endpunkte |
| Anmeldung | anonym lesen, Servicekonten mit Scope ✓ | persönliche Tokens `sbi_`, `read`/`write` | C1/C2 |
| Abruflimit | 120/Min. ✓ | 120/Min. ✓ | C5 |
| Doku | Scalar, Swagger, Postman ✓ | API-Tester, Scalar | D4 |
| Beispiele | – | je Parameter ✓ | D3 |
| `If-Match` / Idempotency-Key | – | – | B2/B3 |
| Scopes | `read-org` | `read`/`write` | `<modul>:<ressource>.<aktion>` (API-E19) |
| Token-Präfix | eigenes | `sbi_` | `<modulschlüssel>_<art>_` (G2) |
| Datenklassen, Zweck, Auskunft | Datenklassen je Spalte (DB) | – | je Operation, `/me/data-export` (C9) |

## Bewusste Abweichungen von Zalando

| Thema | Zalando | EduKSX | Grund |
| --- | --- | --- | --- |
| Version | Media-Type, keine Version im Pfad (#113–#115) | `/api/v1` im Pfad | beschlossen (Plattform §5, Glossary DEC-016); einfacher für Schulen, Tester und Postman |
| Aufzählungswerte | `UPPER_SNAKE_CASE` (#240) | klein `snake_case` | identisch mit Datenbank und Exporten (DB A1) |
| Scopes | `<app>.<resource>.<mode>` (#225) | `<modul>:<ressource>.<aktion>` | gleiche Idee; Doppelpunkt nach Plattform S2 |
| `ETag`/`If-Match`, `Idempotency-Key` | freiwillig (#182, #230) | Pflicht für Änderungen bzw. Sync, Importe, Bestellungen | Datenverlust vermeiden (DB A6), Bund AP10 |
| Mehrfachänderungen | `207` je Eintrag (#152) | alles oder nichts | eine Transaktion (DB A6); `207` nur nach eigenem Entscheid |

## Quellen

- Zalando RESTful API and Event Guidelines – opensource.zalando.com/restful-api-guidelines
- Microsoft REST API Guidelines (Azure, Graph) – github.com/microsoft/api-guidelines
- SBB API Principles – schweizerischebundesbahnen.github.io/api-principles
- API-Architektur Bund, REST-API-Guidelines, Security Guideline 1.0 (11.08.2025), Idempotenz AP10 1.0 (17.01.2025) –
  bk.admin.ch/en/api-architecture-bund
- OWASP API Security Top 10 (2023) – owasp.org/API-Security; OWASP ASVS 5.0 – owasp.org/www-project-application-security-verification-standard; ZAP API-Scan – zaproxy.org
- DSGVO (Verordnung (EU) 2016/679); IDG Kanton Zürich (Gesetz über die Information und den Datenschutz)
- Architektur-Review des API-Standards 1.0 vom 13.11.2026 (Punkte K1–K3, W1–W6)
- RFC 9457 (Problem Details), RFC 9745 (Deprecation), RFC 8594 (Sunset), RFC 7396 (JSON Merge Patch), RFC 9700 (OAuth
  2.0 Security BCP), RFC 9449 (DPoP), RFC 8705 (mTLS), RFC 3339 (Datum)
- IETF-Entwürfe: draft-ietf-httpapi-ratelimit-headers-11, draft-ietf-httpapi-idempotency-key-header-07
- Eigene Grundlagen: KONZEPT-PLATTFORM (S1–S8), DB-Standard 1.1, Glossary KONZEPT-API/-MCP/-ORGANISATION, Intranet
  AGENTS.md und KONZEPT-MCP, WebApplicationProgrammingGuide (API-01, SEC-01)

## Verlauf

- 12.11.2026: Entwurf 0.1 aus Plattform-Konzept (S1–S8), DB-Standard 1.1, Glossary (KONZEPT-API, -MCP, -ORGANISATION)
  und Intranet (REST-API v1, KONZEPT-MCP) erstellt.
- 12.11.2026: Version 0.2 – Abgleich mit Zalando, Bund (Security Guideline, AP10), OWASP API Top 10, RFC 9700/9745 und
  IETF-Entwürfen. Entscheide API-E1–API-E3 (Pagination, `DELETE`, Token-Laufzeiten); RateLimit-Kopfzeilen korrigiert;
  OWASP-Abgleich, Linter, Mass Assignment, SSRF, Abweichungen und Quellen ergänzt.
- 12.11.2026: Version 0.3 – offene Punkte entschieden (API-E4–API-E13); DPoP/mTLS bleibt ZU PRÜFEN mit Ident.
- 12.11.2026: Version 0.4 – Durchsicht PR #17: API-E14–API-E17 (PATCH-Content-Type, Personensuche, Doku-Seiten, Tests abgestuft).
- 12.11.2026: Version 1.0 abgenommen (#15, PR #17).
- 13.11.2026: Entwurf 1.1 nach Architektur-Review (#18): Stufen, Modulschlüssel und Register, `eduksx/core`, starker
  ETag, `DELETE`-Fälle, Sync ohne Lücken, Idempotenz-Bereich, privilegierte Zugriffe, DSGVO/IDG (C9),
  Sicherheitsnachweis (C10), Konformität (D8); Entscheide API-E18–API-E35.
- 13.11.2026: Version 1.1 abgenommen (#18, PR #19).
- 13.11.2026: Version 1.1.1 redaktionell – Register nach [REGISTER-MODULE.md](REGISTER-MODULE.md) verschoben (API-E36),
  Entscheide als `API-E<n>` nummeriert.
- 20.11.2026: Version 1.2 abgenommen – A8 deutsche Beschreibungen in der OpenAPI-Beschreibung (API-E37), verbindlich für
  alle EduKSX-Projekte (#65).
- 22.11.2026: Version 1.3 beschlossen – G4 API-First mit Stufen A/B/C, automatische Prüfung, interne APIs (API-E38, #72).
