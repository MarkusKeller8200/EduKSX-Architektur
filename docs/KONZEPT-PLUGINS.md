# Konzept: Plugins – Module in Intranet und Portal einbinden (#44)

Stand: 13.11.2026 (Meilenstein 0.3.0) · Verantwortlich: Markus Keller · Status: **IN ARBEIT** – P1, P2 BESCHLOSSEN im
Chat 13.11.2026; übrige Punkte EMPFOHLEN.

Grundlagen: [Modulübersicht](MODULE-UEBERSICHT.md) §4, [Plattform](KONZEPT-PLATTFORM.md) S1, S2, S5, S7, S8,
[Steckbrief-Schema](../spec/v1/module-manifest.schema.json).

## 1. Ziel

Das Intranet (für Mitarbeitende) und später das Portal (für Externe) zeigen Inhalte und Funktionen der übrigen Module
– Begriffe aus dem Glossary, Erlasse aus dem Codex, «meine Lizenzen», «mein Stundenplan» –, **ohne deren Daten zu
kopieren und ohne fremden Code im Gastgeber auszuführen**. Ein Modul wird angebunden, indem der Gastgeber seinen
Steckbrief liest.

**Nichtziele:**
- keine Plugins Dritter in der ersten Stufe
- keine Anbindung von Fremdsystemen (M365, Apple School Manager, Escola …) als Plugin – das ist Aufgabe von `connect`
- kein Datenbankzugriff über Modulgrenzen

## 2. Ablauf

```text
Intranet (Gastgeber)                         Modul (z. B. Glossary)
  │ 1. liest /.well-known/eduksx-module.json ─►│ Steckbrief mit Abschnitt «ui»
  │ 2. zeigt Menüeintrag, Kachel, Suchtreffer   │
  │ 3. lädt Web-Komponente  ────────────────────►│ /ui/v1/elements.js (vom Modul ausgeliefert)
  │ 4. Komponente ruft die API des Moduls ──────►│ /api/v1/… (öffentlich bzw. mit Token, S2/S1)
```

1. **Anmelden eines Moduls im Gastgeber:** Administratorin gibt die Adresse des Moduls ein (bei zentralen Modulen
   vorausgefüllt). Der Gastgeber liest den Steckbrief, zeigt die angebotenen Kacheln, Menüeinträge und die Suche zur
   Auswahl.
2. **Anzeige:** Kacheln sind Web-Komponenten des Moduls (wie heute `<glossary-term>`, Plattform S8), eingebettet im
   Gastgeber; Menüeinträge sind Links mit Permalinks; die gemeinsame Suche fragt die Such-API jedes Moduls an.
3. **Daten der Person (Stufe 2):** Die Komponente erhält ein kurzlebiges Token für **dieses** Modul (Zielgruppe `aud`
   = Modul) aus Ident; der Gastgeber reicht nie sein eigenes Token weiter.

## 3. Entscheide

| Nr. | Frage | Optionen | Entscheid | Status |
|---|---|---|---|---|
| P1 | Form | Manifest + Web-Komponenten / Composer-Paket im Gastgeber | **Manifest im Steckbrief (S5) + Web-Komponenten des Moduls**; der Gastgeber installiert keinen fremden Code | BESCHLOSSEN 13.11.2026 |
| P2 | Umfang Stufe 1 | eigene Module / auch Dritte | **eigene Module**; Stufe 1 öffentliche Daten (Glossary, Codex) und Links; Stufe 2 Daten der Person über Ident; Fremdsysteme über `connect`; keine Plugins Dritter | BESCHLOSSEN 13.11.2026 |
| P3 | Beschreibung | eigenes Format / Abschnitt im Steckbrief | Abschnitt `ui` im Steckbrief (`spec/v1/module-manifest.schema.json`, abwärtskompatibel ergänzt) | EMPFOHLEN |
| P4 | Einbettung | Web-Komponente / iframe | Web-Komponente mit Shadow DOM; iframe nur für ganze Seiten mit eigener Anmeldung | EMPFOHLEN |
| P5 | Gestaltung | frei / gemeinsame Gestaltung | Komponenten übernehmen Farben und Schrift des Gastgebers über CSS-Variablen (`--eduksx-*`), später aus `@eduksx/ui` (Core C10); WCAG 2.1 AA | EMPFOHLEN |
| P6 | Sicherheit | – | Skripte nur vom Host des Moduls, mit Subresource Integrity bzw. fester Version im Pfad (`/ui/v1/`); CSP des Gastgebers listet erlaubte Module; Tokens nur mit `aud` des Moduls, höchstens 10 Min. | EMPFOHLEN |
| P7 | Selbst-Hosting | – | lokale Gastgeber dürfen zentrale Module (Glossary, Codex) einbinden – nur öffentliche Daten, ohne Anmeldung (SH-E12) | EMPFOHLEN |
| P8 | Versionierung | – | `ui` gehört zur Steckbrief-Version v1; Komponenten-Pfade tragen die Hauptversion (`/ui/v1/`); Brüche nur mit `/ui/v2/` parallel | EMPFOHLEN |

## 4. Umsetzung

### 4.1 Abschnitt `ui` im Steckbrief

```json
"ui": {
  "elements": "/ui/v1/elements.js",
  "widgets": [
    {"id": "term-search", "title": "Begriff nachschlagen", "element": "glossary-search", "audience": "public"},
    {"id": "my-proposals", "title": "Meine Vorschläge", "element": "glossary-my-proposals", "audience": "user",
     "scopes": ["glossary:proposals.read"]}
  ],
  "menu": [{"title": "Glossar", "url": "/"}],
  "search": {"url": "/api/v1/search?q={query}", "audience": "public"}
}
```

- `element` beginnt mit dem Modulschlüssel (`glossary-…`), damit sich Komponenten verschiedener Module nicht
  überschneiden (Namensraum nach API G2).
- `audience`: `public` (ohne Anmeldung) oder `user` (Token der Person, Stufe 2).

### 4.2 Was ein Modul liefert

- die Web-Komponenten unter `/ui/v1/` (gebaut mit dem Modul, CORS nur lesend, API C6)
- Such-Endpunkt mit einheitlicher Antwort (Titel, Kurztext, Permalink, Modul) – Schema folgt in `spec/` mit dem
  ersten Abnehmer
- Permalinks für alle Treffer (S8)

### 4.3 Was der Gastgeber (Intranet, Portal) liefert

- Verwaltung der angebundenen Module (Adresse, Auswahl der Kacheln, Rechte je Rolle)
- Rahmen für Kacheln, gemeinsame Suche über alle angebundenen Module, Menü (S7)
- in Stufe 2 die Token-Beschaffung je Modul über Ident

### 4.4 Tests

- Steckbrief mit `ui` besteht das Schema (`tests/test_spec.py`)
- Probe: Glossary-Kachel und Glossary-Suche im Intranet nur über Steckbrief und API (Testliste #44)

## 5. Issues

| Issue | Inhalt | Status |
|---|---|---|
| #44 | Dieses Konzept | `_2 in Arbeit` |
| (folgt, Glossary) | Steckbrief mit `ui`, Web-Komponenten unter `/ui/v1/`, Such-API | nach Abnahme |
| (folgt, Intranet) | Gastgeber: Module anbinden, Kacheln, Suche | nach Abnahme |

## 6. Verlauf

- 13.11.2026: Konzept angelegt; P1, P2 im Chat beschlossen.
