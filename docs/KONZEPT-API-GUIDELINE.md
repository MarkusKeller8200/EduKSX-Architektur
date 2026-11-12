# Konzept: API-Standard der EduKSX-Plattform (#15)

Stand: 12.11.2026 (Version 0.3) · Verantwortlich: Markus Keller · Status: **ENTWURF** – zur Abnahme (alle Entscheide getroffen)

Verbindlicher Standard für **alle** Schnittstellen der EduKSX-Module (Glossary, Rechtssammlung, Intranet, Stundenplan,
Ident …) – für Menschen und KI-Agenten. Er enthält nur Regeln, die für jedes Modul gelten. Endpunkte, Felder und
modulspezifische Entscheide stehen im API-Konzept des jeweiligen Moduls, das auf diesen Standard verweist (für das
Glossary: `docs/KONZEPT-API.md`, für das Intranet: `App\Support\OpenApi` und `docs/KONZEPT-MCP.md`).

Er ergänzt den [DB-Standard](KONZEPT-DB-GUIDELINE.md) (Verweise A1 … D3) und konkretisiert die Schnittstellen S1–S8 aus
[KONZEPT-PLATTFORM.md](KONZEPT-PLATTFORM.md).

**Verbindlichkeit** (Stufen nach [KONZEPT-VORLAGE.md](KONZEPT-VORLAGE.md)): **BESCHLOSSEN** = bereits in Plattform,
DB-Standard oder Glossary entschieden (Quelle in Klammern) · **EMPFOHLEN** = neu in diesem Entwurf · **ZU PRÜFEN** = technisch zu klären (Liste
am Schluss).

**Grundlagen:** Der Standard folgt in den meisten Punkten den Zalando RESTful API Guidelines (auch Vorbild für OTTO,
SBB und die REST-Guidelines des Bundes), den Empfehlungen der API-Architektur Bund (Security Guideline 1.0, 08/2025;
Idempotenz AP10, 01/2025), den OWASP API Security Top 10 (2023) und den IETF-Standards. Bewusste Abweichungen stehen in
[Abweichungen von Zalando](#bewusste-abweichungen-von-zalando), Quellen am Schluss. Er schliesst die offenen Punkte
API-01 und SEC-01 (externe Clients) im WebApplicationProgrammingGuide.

| Teil | Inhalt |
| --- | --- |
| [A · Entwurf](#a--entwurf) | Grundsätze, URLs, JSON, Felder, Datum, Sprache, Listen, Filter, Fehler, Statuscodes |
| [B · Verhalten](#b--verhalten) | Schreiben, Sperren, Idempotenz, Löschen, Caching, Synchronisation, Ereignisse |
| [C · Sicherheit und Datenschutz](#c--sicherheit-und-datenschutz) | Anmeldung, Tokens, Scopes, Mandanten, Datenklassen, Grenzen, CORS |
| [D · Lebenszyklus](#d--lebenszyklus) | Versionierung, Stabilität, OpenAPI, Doku, MCP, Betrieb, Tests |

## Grundsätze

1. **API first** – jede Funktion, die ein anderes System braucht, gibt es zuerst als API; Website, Intranet und MCP
   nutzen dieselben Services. BESCHLOSSEN (IDA-Vorgehen, Glossary «API gehört zum Kern»)
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
  Sprache als `<feld>_label` (`"status": "current", "status_label": "aktuell"`) – BESCHLOSSEN 12.11.2026, E9.
- Auf oberster Ebene steht immer ein JSON-Objekt, nie eine Liste oder ein Wert (Zalando #110).
- Fehlende Werte als `null`, nie als leerer String; `null` und fehlendes Feld bedeuten dasselbe (ausser bei `PATCH`,
  B1). Leere Listen als `[]`, nie `null`; Ja/Nein-Felder sind nie `null` – wo es drei Zustände gibt, ist es eine
  Aufzählung (Zalando #122–#124).
- Unbekannte Felder in Anfragen werden mit `422` abgelehnt, unbekannte Felder in Antworten ignorieren Abnehmer (D2).
- Aufzählungen sind **erweiterbar**: In OpenAPI als `type: string` mit `x-extensible-enum` (bzw. `examples`), damit
  neue Werte keine brechende Änderung sind. Ein geschlossenes `enum` nur für Eingaben, die der Dienst selbst prüft.
- Jede Zahl hat in der Beschreibung ein `format` (`int32`, `int64`, `decimal`); Fliesskommazahlen nur für Messwerte.
- Geldbeträge als ganze Zahl in Rappen mit Feld `currency` (DB A4); Zahlen nie als String, IDs immer als String.
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

### A6 Fehler (BESCHLOSSEN 12.11.2026, E5)

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
| `301` | Objekt dauerhaft verschoben (z. B. zusammengeführter Begriff, Glossary #16) |
| `304` | Unverändert (ETag) |
| `400` | Anfrage nicht lesbar (kaputtes JSON); `Idempotency-Key` fehlt, wo er Pflicht ist (B3) |
| `401` | Nicht angemeldet, Token ungültig/abgelaufen (mit `WWW-Authenticate`) |
| `403` | Angemeldet, aber kein Recht bzw. Scope |
| `404` | Gibt es nicht **oder** darf nicht gesehen werden (fremde Organisation → immer `404`, nie `403`) |
| `409` | Konflikt mit dem Zustand (Doppelanlage, `lock_version` veraltet, DB A6); Anfrage mit gleichem `Idempotency-Key` läuft noch |
| `410` | Endgültig gelöscht oder zurückgezogen, wo das Modul es so festlegt |
| `412` | `If-Match` passt nicht (siehe B2) |
| `415` | Falscher Content-Type |
| `422` | Inhaltlich ungültig (Validierung, unbekannte Felder oder Parameter); `Idempotency-Key` mit anderem Inhalt wiederverwendet |
| `428` | `If-Match` fehlt, wo es Pflicht ist |
| `429` | Abruflimit überschritten, mit `Retry-After` |
| `500`/`503` | Fehler im Dienst bzw. Wartung, mit `Retry-After` bei `503` |

---

## B · Verhalten

### B1 Schreiben (EMPFOHLEN)

- `POST` legt an, `PATCH` ändert einzelne Felder (JSON Merge Patch, RFC 7396: fehlendes Feld = unverändert,
  `null` = leeren), `PUT` nur, wo ein Objekt bewusst als Ganzes ersetzt wird, `DELETE` löscht.
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

### B2 Konkurrierende Änderungen (BESCHLOSSEN 12.11.2026, E6; Grundlage DB A6)

- Änderbare Objekte liefern `lock_version` im Body und als `ETag` (`W/"<id>-<lock_version>"`) in der Kopfzeile.
- `PATCH`, `PUT` und `DELETE` verlangen `If-Match` mit dem ETag (fehlt er: `428`); passt er nicht: `412` mit dem
  aktuellen Stand in `detail`. Nichts wird überschrieben.
- Wer kein `If-Match` senden kann (einfache Integrationen), darf `lock_version` im Body mitgeben; veraltet ergibt
  `409`.

### B3 Idempotenz und Wiederholung (EMPFOHLEN)

Nach Bund AP10 und dem IETF-Entwurf «Idempotency-Key» (noch kein RFC, ZU PRÜFEN bei dessen Veröffentlichung):

- `GET`, `HEAD`, `PUT`, `DELETE` sind idempotent; `POST` und `PATCH` nicht.
- Für `POST`, der etwas anlegt oder auslöst, akzeptiert die API die Kopfzeile `Idempotency-Key` (UUID v4, als
  String). Der Dienst speichert Schlüssel, Prüfsumme des Bodys, Besitz (Token) und Antwort **24 Stunden**:

  | Fall | Antwort |
  | --- | --- |
  | Schlüssel neu | normal ausführen, Antwort speichern |
  | Schlüssel bekannt, gleicher Body, abgeschlossen | gespeicherte Antwort erneut, Kopfzeile `Idempotent-Replayed: true` |
  | Schlüssel bekannt, Erstanfrage läuft noch | `409` |
  | Schlüssel bekannt, anderer Body | `422` |
  | Schlüssel fehlt, wo das Modul ihn verlangt | `400` |

- Schlüssel gelten je Token; ein fremder Schlüssel liefert nie die Antwort einer anderen Identität.
- Synchronisation, Importe, Bestellungen und MCP-Werkzeuge senden immer einen `Idempotency-Key`; für diese Endpunkte
  ist er Pflicht.
- Abnehmer wiederholen nur bei `429`, `503` und Netzfehlern – mit `Retry-After` bzw. exponentiellem Abstand und Zufall,
  höchstens fünfmal.

### B4 Löschen (EMPFOHLEN, Grundlage DB B3)

- `DELETE` auf ein Hauptobjekt löscht vorläufig (Papierkorb); die Antwort ist `204`. **Ein wiederholtes `DELETE`
  auf ein bereits gelöschtes Objekt antwortet ebenfalls `204`** (idempotent, BESCHLOSSEN 12.11.2026 nach Bund AP10) –
  sofern die Identität das Objekt sehen durfte; sonst `404`. `GET` liefert danach `404` bzw. `410`, wo das Modul es
  festlegt.
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
- Datenstand als Kopfzeile `EduKSX-Release`, wo ein Modul Veröffentlichungen kennt.
- **Eigene Kopfzeilen der Plattform** heissen `EduKSX-<Name>` ohne `X-`-Präfix (RFC 6648): `EduKSX-Release`,
  `EduKSX-Organization`, `EduKSX-Signature`. Modul-eigene Kopfzeilen gibt es nicht; das Glossary sendet
  `X-Glossary-Release` bis 1.0 parallel (BESCHLOSSEN 12.11.2026, E7).

### B6 Synchronisationsvertrag (BESCHLOSSEN im Glossary, für alle Module mit Abnehmern EMPFOHLEN)

Jedes Modul, dessen Daten andere Systeme regelmässig übernehmen, bietet:

1. **Vollstand** `GET /api/v1/exports` mit `cursor` (letztes Ereignis) und Lizenz.
2. **Änderungen** `GET /api/v1/changes?since=<cursor>` – jede Änderung ein Ereignis mit unveränderlicher `id`
   (= Cursor), `event_type`, `occurred_at` und dem Objekt im veröffentlichten Stand; Rückzüge als Tombstone.
3. Stabile `id`, `revision`, `updated_at` je Objekt; Reihenfolge reproduzierbar; wiederholte Abrufe idempotent.
4. Abnehmer halten einen lokalen Stand, laufen bei Ausfall weiter und ziehen danach lückenlos nach (Referenz:
   Intranet ↔ Glossary, `SYNC-INTRANET.md`).

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
| Person über Oberfläche oder KI-Client | OIDC über Ident (S1); MCP mit OAuth 2.1 + PKCE + dynamischer Registrierung | BESCHLOSSEN (Ziel) |
| Dienst zu Dienst | OAuth2 Client Credentials, JWT, Prüfung über JWKS, `aud` = Modul (S2) | BESCHLOSSEN (Ziel) |
| Übergang: Servicekonto des Moduls | eigenes Token (`Bearer`) mit Scopes | BESCHLOSSEN bis S2 steht |
| Übergang: persönliches Token (Intranet) | Token handelt im Namen der Person, mit Ablauf (E3) und feinen Scopes statt `read`/`write`; läuft aus, sobald Ident steht | BESCHLOSSEN 12.11.2026, E8 |

- Tokens nur im Kopf `Authorization: Bearer …`, nie in URL, Query oder Cookie für die API.
- **Lesbare Präfixe** je Modul und Art, damit Geheimnis-Scanner sie finden: `<modul>_<art>_<zufall>`
  (z. B. `glsx_sa_…`, `sbi_pat_…`); gespeichert wird nur der Hash, angezeigt nur das Präfix (DB B6).
- **Laufzeiten (BESCHLOSSEN 12.11.2026):**

  | Art | Laufzeit |
  | --- | --- |
  | Zugriffstoken aus OIDC/OAuth (S1, S2), JWT, signiert, mit `aud` | höchstens 10 Minuten, Erneuerung serverseitig |
  | Statisches Token eines Servicekontos, das automatisch erneuert wird | höchstens 90 Tage, Rotation mit Überlappung |
  | Persönliches Token, das automatisch erneuert wird | höchstens 30 Tage |
  | Statisches Token für Abnehmer, die **nicht** automatisch erneuern können (feste Konfiguration, Fremdsystem) | höchstens 12 Monate, Vorgabe 90 Tage; Warnung an die Besitzer 30 und 7 Tage vor Ablauf |

- Jedes Token hat Name, Besitz, Scopes, Ablaufdatum, letzten Gebrauch (als Datum) und ist jederzeit widerrufbar.
  Anlegen, Ändern, Widerrufen schreibt ins Sicherheitsprotokoll (DB A7).
- Nach RFC 9700 und der Security Guideline des Bundes: nur Authorization Code mit PKCE bzw. Client Credentials, keine
  Implicit- und Password-Grants; Tokens mit Zielgruppe (`aud`) und Prüfung von Signatur, Gültigkeit und Zweck.
  An den Absender gebundene Tokens (DPoP, RFC 9449, oder mTLS, RFC 8705) für Dienst-zu-Dienst-Zugriffe mit
  Personendaten: ZU PRÜFEN mit Ident (Entscheid beim Bau von Ident, #16).
- Ein statisches Token allein reicht nicht für privilegierte Vorgänge (Konten, Rollen, Löschen nach Datenschutzrecht);
  dafür gilt C2 (`acr=mfa`) bzw. ein ausdrücklich freigegebenes Servicekonto.
- Servicekonten sind eigene Identitäten, nie Benutzerkonten (DB B4).

### C2 Rechte und Scopes (EMPFOHLEN, Grundlage DB B4 und Plattform S2)

- Scopes heissen `<modul>:<recht>` (`glossary:read-org`, `glossary:propose`, `intranet:people.write`); `read` und
  `write` allein sind zu grob für neue Module.
- Geprüft wird **Scope des Tokens UND Recht der Identität** auf das konkrete Objekt (Policy) – der Scope begrenzt,
  er gewährt nie mehr. Rechte, nie Rollennamen (DB B4). Jeder Zugriff auf ein Objekt über eine ID prüft das Recht auf
  **dieses** Objekt (OWASP API1, BOLA), jede Funktion das Recht auf die Funktion (API5, BFLA).
- Rollen und Organisation kommen aus der Anmeldung bzw. dem Token, nie aus Angaben des Clients im Body oder in
  Kopfzeilen ohne Prüfung (Bund Security Guideline 3.2).
- Jeder Endpunkt nennt in der OpenAPI-Beschreibung seine Scopes (`security`) und das nötige Recht
  (`x-eduksx-ability`).
- Ein Token berechtigt nie zur Veröffentlichung oder zu Rechteänderungen, ausser das Modul hat dafür einen eigenen,
  eng begrenzten Scope beschlossen (Glossary DEC-017). KI-Werkzeuge veröffentlichen nie ohne Prüfung durch Menschen.
- Privilegierte Vorgänge über die API (Konten, Rollen, Löschen nach Datenschutzrecht) nur mit Anmeldung, die
  `acr=mfa` trägt, bzw. mit Servicekonto, das dafür ausdrücklich freigegeben ist.

### C3 Mandanten (BESCHLOSSEN, DB B1; API-Regeln EMPFOHLEN)

- Die Organisation kommt **aus dem Token** (Servicekonto der Organisation bzw. gewählte Organisation der Person mit
  Kopfzeile `EduKSX-Organization`, geprüft gegen die Mitgliedschaft) – nie aus einer frei wählbaren ID im Pfad oder
  Body.
- Ohne Mandantenkontext liefern Endpunkte für Organisationsdaten `403`, nie alles. Objekte fremder Organisationen
  ergeben `404`.
- Öffentliche Endpunkte enthalten nie Organisations- oder persönliche Anpassungen (Glossary DEC-018).
- Plattform-Administration über einen eigenen, protokollierten Weg (`/api/v1/admin/…`), nicht über Parameter.

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
- Personendaten nie in URLs (keine E-Mail als Pfad oder Filter in Logs): Suche nach Personen per `POST /people/search`
  oder `q` mit Protokollmaskierung.
- Personendaten über MCP an externe KI-Anbieter nur mit Vertrag zur Auftragsbearbeitung (Intranet KONZEPT-MCP, IDG ZH).

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

Unbekannte Felder und Aufzählungswerte ignorieren, Weiterleitungen (`301`) folgen, `Retry-After` beachten, ETag
nutzen, einen lokalen Stand halten und bei Ausfall weiterlaufen. Das steht in jeder API-Doku unter «Nutzung und
Stabilität».

### D3 OpenAPI-Beschreibung (BESCHLOSSEN, Glossary/Intranet/Plattform S8; Details EMPFOHLEN)

- **OpenAPI 3.1**, ausgeliefert unter `/api/openapi.json` (JSON ist gültiges YAML), als **eine** eigenständige Datei
  ohne externe Verweise (Zalando #101).
- **Vertrag zuerst** (BESCHLOSSEN 12.11.2026, E11): Neue Module schreiben die Beschreibung als Datei
  (`openapi/<modul>-v1.json` bzw. `.yaml`) vor dem Code und prüfen den Code dagegen. Das Intranet erzeugt sie bis zu
  einem Umbau weiter aus `App\Support\OpenApi`. In beiden Fällen gelten die Prüfung Route ↔ Beschreibung und der
  Linter.
- Jede Operation hat `operationId` (englisch, `camelCase`, Verb + Objekt: `listTerms`, `createPerson`) – daraus
  entstehen MCP-Werkzeugnamen (`list_terms`) und Postman-Einträge.
- Jeder Parameter hat ein `example`, jeder schreibende Endpunkt einen Beispiel-Body, nur mit erfundenen Werten
  (`…@sekbuelach.example`, BESCHLOSSEN Intranet 04.11.2026). Beschreibungen und Beispiele ohne Entscheidnummern und
  ohne echte Personen- oder Organisationsnamen.
- Schemas wiederverwenden (`components`); `Problem` gemeinsam für alle Fehler; `security` und `x-eduksx-ability` je
  Operation; Lizenz in `info.license`.
- **Tests:** jede Route unter `/api/v1` steht in der Beschreibung und umgekehrt; Antworten der Feature-Tests werden
  gegen das Schema geprüft; die Beschreibung ist gültiges OpenAPI 3.1.
- **Linter in der CI:** Spectral (bzw. Redocly CLI) mit einem gemeinsamen Regelsatz `eduksx` in `eduksx/core`, der
  diesen Standard prüft (Namen, `operationId`, Beispiele, `security`, `format`, Problem-Antworten). Ausgangspunkt:
  offene Regelsätze nach Zalando/OTTO, angepasst an die Abweichungen unten. Zuerst als Warnung, ab dem folgenden
  Release als Fehler. Neue Abhängigkeit → Eintrag in `third-party.json` (BESCHLOSSEN 12.11.2026, E12).
- **Brechende Änderungen automatisch erkennen:** die Beschreibung jedes Pull Requests wird mit `main` verglichen
  mit `oasdiff breaking`; ein Bruch in einer bestehenden Version lässt die CI scheitern, während der Vorschau nur
  Warnung. Vor dem Einsatz Lizenz und Pflege prüfen und in `third-party.json` eintragen (BESCHLOSSEN 12.11.2026, E13).
- **Client:** Für eigene Oberflächen wird aus der Beschreibung ein TypeScript-Client erzeugt
  (WebApplicationProgrammingGuide); Vertrag und Client werden im selben Pull Request geprüft.
- Gemeinsame Schemas (Problem, Pagination, Ereignis, Lizenz) liegen zentral in `eduksx/core` und werden nicht je Modul
  neu erfunden.

### D4 Doku und Werkzeuge (BESCHLOSSEN, Plattform S8)

- `/api/docs` mit **Scalar** (ohne Telemetrie, ohne fremde Schriften), `/api/swagger` mit «Try it out»,
  `/api/postman.json` (Postman v2.1, aus der Beschreibung erzeugt, Prüfung in der CI).
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

### D6 Betrieb (BESCHLOSSEN, Plattform S5/§6)

`/up`, `/health`, `/metrics` (nur mit Berechtigung), Steckbrief `/.well-known/eduksx-module.json` mit API-Versionen
und Scopes; JSON-Protokolle mit `request_id`; sauberes Herunterfahren; Wartung mit `503` und `Retry-After`.

### D7 Tests (EMPFOHLEN)

Jedes Modul hat mindestens: Route ↔ Beschreibung vollständig; Antworten gegen Schema; Fehlerformat für 401, 403, 404,
409/412, 422, 429; Scope **und** Recht (Token mit zu wenig Scope, Person ohne Recht); **Mandantentrennung** mit zwei
Organisationen über alle Endpunkte, Exporte und Feeds (DB B1); Veröffentlichungsgrenze mit privaten Testdaten (C4);
ETag/304 und `If-Match`/412; Idempotency-Key (alle fünf Fälle aus B3); wiederholtes `DELETE` → `204`;
**Mass Assignment** (geschützte Felder im Body werden abgelehnt); SSRF-Prüfung für Webhook-URLs; Cursor stabil über
Seiten; Synchronisation mit Rückzug und
Wiederaufnahme nach Ausfall; Historie mit `source = api`; Abruflimit; keine Tokens und Personendaten im Protokoll.

---

## Checkliste für Pull Requests mit API-Änderung

- [ ] Standard deckt die Änderung ab – sonst zuerst Konzept-PR
- [ ] URL, Felder und Werte englisch `snake_case` (A1, A2), Werte identisch zur Datenbank
- [ ] Datum ISO 8601 UTC, Sprache über `locale`, Rückfall erkennbar (A3, A4)
- [ ] Liste begrenzt, Cursor als Standard, Reihenfolge stabil, `total` nur auf Anfrage (A5)
- [ ] Aufzählungen erweiterbar, Zahlen mit `format`, keine `null`-Listen oder -Booleans (A2)
- [ ] Fehler als `problem+json` mit `code`; richtige Statuscodes (A6, A7)
- [ ] Schreiben im Service, eine Transaktion, Historie mit `source = api`, `If-Match` bzw. `lock_version` (B1, B2)
- [ ] `Idempotency-Key` für anlegende `POST`; Löschen über Papierkorb, Tombstone im Feed (B3, B4)
- [ ] Scope und Recht geprüft, Organisation aus dem Token, fremde Objekte `404` (C2, C3)
- [ ] Presenter mit Positivliste, schreibbare Felder als Positivliste, Datenklassen beachtet (C4)
- [ ] OWASP-Abgleich für neue Endpunkte (C8), insbesondere externe URLs (SSRF) und fremde Antworten
- [ ] Abruflimit, CORS, keine Personendaten in URL oder Protokoll (C5–C7)
- [ ] Nichts entfernt oder umbenannt in einer bestehenden Version; sonst `v2` mit Deprecation (D1)
- [ ] OpenAPI nachgeführt: `operationId`, Beispiele, `security`, Recht; Linter grün, kein Bruch; Postman neu erzeugt (D3, D4)
- [ ] MCP-Werkzeug mit Annotations, falls die Operation freigegeben ist (D5)
- [ ] Tests nach D7; CHANGELOG «API» nachgeführt

## Entscheide

Alle Punkte entschieden am 12.11.2026 (Chat mit Projektverantwortliche:r).

| Nr. | Frage | Entscheid | Abschnitt |
| --- | --- | --- | --- |
| E1 | Pagination | Cursor Standard, Seiten für kleine Admin-Listen, `total` nur auf Anfrage | A5 |
| E2 | Wiederholtes `DELETE` | `204` (idempotent, Bund AP10) | B4 |
| E3 | Laufzeit von Tokens | kurz (10 Min. / 30 / 90 Tage); bis 12 Monate nur, wenn der Abnehmer nicht automatisch erneuern kann | C1 |
| E4 | Umstellung Pagination | Intranet und Glossary `/terms` auf Cursor; Intranet sofort, Glossary in der Vorschau vor 1.0 | A5 |
| E5 | Fehlerformat | `problem+json` überall, Intranet stellt um (ohne v2, Prototyp) | A6 |
| E6 | Gleichzeitige Änderungen | `If-Match` Standard (412/428), `lock_version` im Body erlaubt (409) | B2 |
| E7 | Kopfzeilen | einheitlich `EduKSX-*`; `X-Glossary-Release` bis 1.0 parallel | B5 |
| E8 | Persönliche Tokens | bleiben bis Ident steht, mit Ablauf und feinen Scopes | C1 |
| E9 | Statuswerte | englischer Wert wie in der Datenbank, dazu `<feld>_label`; Glossary passt Beispiel und API an | A2 |
| E10 | Ablage | EduKSX-Architektur `docs/KONZEPT-API-GUIDELINE.md` (Quelle); Verweise aus Glossary, Intranet und WebApplicationProgrammingGuide (schliesst dort API-01, SEC-01 für externe Clients); Kopie im claude.ai-Projekt | – |
| E11 | Entstehung der Beschreibung | Vertrag zuerst für neue Module; Intranet bis zum Umbau aus dem Code | D3 |
| E12 | Linter | eigener Spectral-Regelsatz `eduksx` in `eduksx/core`, zuerst Warnung, dann Fehler | D3 |
| E13 | Brüche erkennen | `oasdiff` in der CI nach Lizenzprüfung; während der Vorschau Warnung | D3 |
| – | DPoP/mTLS für Dienst-zu-Dienst | mit Ident prüfen (#16) | C1 – ZU PRÜFEN |

## Abweichungen heute (Ist-Stand 12.11.2026)

| Thema | Glossary | Intranet | Standard |
| --- | --- | --- | --- |
| Fehler | `problem+json` ✓ | `{"message": …}` | `problem+json` (E5) |
| Hülle | `{"data": …}` ✓ (Beispiel im Konzept veraltet) | `{"data": …}` ✓ | `{"data": …}` |
| Pagination | `page`/`per_page` mit `total`; Cursor im Feed ✓ | `limit`/`offset`, `meta.total` | Cursor (E1, E4) |
| Statuswerte | Beispiel zeigt `"aktuell"` | – | englisch + `_label` (E9) |
| Kopfzeilen | `X-Glossary-Release` | – | `EduKSX-Release` (E7) |
| Konflikte | – | – | `If-Match` (E6) |
| Wiederholtes `DELETE` | – | `404` | `204` (E2) |
| Token-Laufzeit | Servicekonten mit Ablauf | persönliche Tokens | C1 (E3) |
| ETag/304 | ✓ | – | öffentliche Lese-Endpunkte |
| Anmeldung | anonym lesen, Servicekonten mit Scope ✓ | persönliche Tokens `sbi_`, `read`/`write` | C1/C2 |
| Abruflimit | 120/Min. ✓ | 120/Min. ✓ | C5 |
| Doku | Scalar, Swagger, Postman ✓ | API-Tester, Scalar | D4 |
| Beispiele | – | je Parameter ✓ | D3 |
| `If-Match` / Idempotency-Key | – | – | B2/B3 |

## Bewusste Abweichungen von Zalando

| Thema | Zalando | EduKSX | Grund |
| --- | --- | --- | --- |
| Version | Media-Type, keine Version im Pfad (#113–#115) | `/api/v1` im Pfad | beschlossen (Plattform §5, Glossary DEC-016); einfacher für Schulen, Tester und Postman |
| Aufzählungswerte | `UPPER_SNAKE_CASE` (#240) | klein `snake_case` | identisch mit Datenbank und Exporten (DB A1) |
| Scopes | `<app>.<mode>` (#225) | `<modul>:<recht>` | beschlossen (Plattform S2) |
| `ETag`/`If-Match`, `Idempotency-Key` | freiwillig (#182, #230) | Pflicht für Änderungen bzw. Sync, Importe, Bestellungen | Datenverlust vermeiden (DB A6), Bund AP10 |
| Mehrfachänderungen | `207` je Eintrag (#152) | alles oder nichts | eine Transaktion (DB A6); `207` nur nach eigenem Entscheid |

## Quellen

- Zalando RESTful API and Event Guidelines – opensource.zalando.com/restful-api-guidelines
- Microsoft REST API Guidelines (Azure, Graph) – github.com/microsoft/api-guidelines
- SBB API Principles – schweizerischebundesbahnen.github.io/api-principles
- API-Architektur Bund, REST-API-Guidelines, Security Guideline 1.0 (11.08.2025), Idempotenz AP10 1.0 (17.01.2025) –
  bk.admin.ch/en/api-architecture-bund
- OWASP API Security Top 10 (2023) – owasp.org/API-Security
- RFC 9457 (Problem Details), RFC 9745 (Deprecation), RFC 8594 (Sunset), RFC 7396 (JSON Merge Patch), RFC 9700 (OAuth
  2.0 Security BCP), RFC 9449 (DPoP), RFC 8705 (mTLS), RFC 3339 (Datum)
- IETF-Entwürfe: draft-ietf-httpapi-ratelimit-headers-11, draft-ietf-httpapi-idempotency-key-header-07
- Eigene Grundlagen: KONZEPT-PLATTFORM (S1–S8), DB-Standard 1.1, Glossary KONZEPT-API/-MCP/-ORGANISATION, Intranet
  AGENTS.md und KONZEPT-MCP, WebApplicationProgrammingGuide (API-01, SEC-01)

## Verlauf

- 12.11.2026: Entwurf 0.1 aus Plattform-Konzept (S1–S8), DB-Standard 1.1, Glossary (KONZEPT-API, -MCP, -ORGANISATION)
  und Intranet (REST-API v1, KONZEPT-MCP) erstellt.
- 12.11.2026: Version 0.2 – Abgleich mit Zalando, Bund (Security Guideline, AP10), OWASP API Top 10, RFC 9700/9745 und
  IETF-Entwürfen. Entscheide E1–E3 (Pagination, `DELETE`, Token-Laufzeiten); RateLimit-Kopfzeilen korrigiert;
  OWASP-Abgleich, Linter, Mass Assignment, SSRF, Abweichungen und Quellen ergänzt.
- 12.11.2026: Version 0.3 – offene Punkte entschieden (E4–E13); DPoP/mTLS bleibt ZU PRÜFEN mit Ident.
