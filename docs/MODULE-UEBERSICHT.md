# Module der EduKSX-Plattform – Übersicht und Systemgrenzen

Stand: 13.11.2026 · Verantwortlich: Markus Keller · Status: **BESCHLOSSEN** für Zweck und Kurzbeschreibung (Chat
13.11.2026); Abgrenzungen und Plugin-Integration **EMPFOHLEN**, bis das jeweilige Modul-Konzept sie bestätigt.

Schlüssel, Repos und Status führt allein das [Modulregister](REGISTER-MODULE.md). Icons aus dem EduKSX-Icon-Set, einzige Quelle
ist das Repo EduKSX-UI (`icons/`, Paket `@eduksx/ui`, Regeln in dessen `docs/KONZEPT-MARKE.md` §6). Die Bilder unten
verweisen direkt dorthin; dieses Repo hält keine Kopien mehr (seit 22.11.2026).

## 1. Auf einen Blick

| | Modul | Schlüssel | Kurzbeschreibung | Personendaten | Status |
|---|---|---|---|---|---|
| <img src="https://raw.githubusercontent.com/MarkusKeller8200/EduKSX-UI/main/icons/svg/eduksx-core-color.svg" width="32" alt=""> | EduKSX-Core | `core` | gemeinsam genutzte Bausteine aller Module (Bibliothek, kein Dienst) | keine | 0.2.0 |
| <img src="https://raw.githubusercontent.com/MarkusKeller8200/EduKSX-UI/main/icons/svg/eduksx-ident-color.svg" width="32" alt=""> | EduKSX-Ident | `ident` | eigener Identity-Provider (Zitadel) und Brücke zu Entra, Google, Edulog | Konten | Brücke 0.1 (Repo EduKSX-Ident), PoC #36 |
| <img src="https://raw.githubusercontent.com/MarkusKeller8200/EduKSX-UI/main/icons/svg/eduksx-ops-color.svg" width="32" alt=""> | EduKSX-Ops «Leitstand» | `ops` | Kunden, Instanzen, Versionen, Updates und Zustand – intern | keine | geplant |
| <img src="https://raw.githubusercontent.com/MarkusKeller8200/EduKSX-UI/main/icons/svg/eduksx-glossary-color.svg" width="32" alt=""> | EduKSX-Glossary | `glossary` | Verzeichnis von Begriffen und Abkürzungen | wenig | aktiv |
| <img src="https://raw.githubusercontent.com/MarkusKeller8200/EduKSX-UI/main/icons/svg/eduksx-codex-color.svg" width="32" alt=""> | EduKSX-Codex | `codex` | systematische Rechtssammlung jeder Gemeinde, später Gegenüberstellung mehrerer Gemeinden | wenig | aktiv |
| <img src="https://raw.githubusercontent.com/MarkusKeller8200/EduKSX-UI/main/icons/svg/eduksx-connect-color.svg" width="32" alt=""> | EduKSX-Connect | `connect` | verbinden und synchronisieren verschiedener Systeme; Stammdaten und ID-Zuordnung | viele | aktiv (Repo EduKSX-Connect) |
| <img src="https://raw.githubusercontent.com/MarkusKeller8200/EduKSX-UI/main/icons/svg/eduksx-licence-color.svg" width="32" alt=""> | EduKSX-Licence | `licence` | Zuweisung von Softwarelizenzen und Plattformzugängen | viele | geplant |
| <img src="https://raw.githubusercontent.com/MarkusKeller8200/EduKSX-UI/main/icons/svg/eduksx-timetable-color.svg" width="32" alt=""> | EduKSX-Timetable «Stundenplan» | `timetable` | Planen von Stundenplänen: SuS, LP, Räume und Lektionen | viele | geplant |
| <img src="https://raw.githubusercontent.com/MarkusKeller8200/EduKSX-UI/main/icons/svg/eduksx-staffing-color.svg" width="32" alt=""> | EduKSX-Staffing «Einsatzplanung» | `staffing` | Planen von Mitarbeitenden und vor allem Lehrpersonen | viele | geplant |
| <img src="https://raw.githubusercontent.com/MarkusKeller8200/EduKSX-UI/main/icons/svg/eduksx-planner-color.svg" width="32" alt=""> | EduKSX-Planner «Jahresplanung» | `planner` | Jahreskalender und Jahresplanung: Ferien, unterrichtsfreie Tage, Anlässe, Spezialwochen, Organisationsplanung (Icon EduKSX-UI #49) | offen | aktiv (Repo EduKSX-Planner, leer) |
| <img src="https://raw.githubusercontent.com/MarkusKeller8200/EduKSX-UI/main/icons/svg/eduksx-flow-color.svg" width="32" alt=""> | EduKSX-Flow | `flow` | fachliche Abläufe: Schritte, Zuständigkeiten und Fristen, die Vorgänge in den anderen Modulen aufrufen | viele | aktiv |
| <img src="https://raw.githubusercontent.com/MarkusKeller8200/EduKSX-UI/main/icons/svg/eduksx-time-color.svg" width="32" alt=""> | EduKSX-Time | `time` | Zeiterfassung für Mitarbeitende und Lehrpersonen bzw. Anbindung externer Systeme | viele | aktiv (Repo EduKSX-Time) |
| <img src="https://raw.githubusercontent.com/MarkusKeller8200/EduKSX-UI/main/icons/svg/eduksx-shop-color.svg" width="32" alt=""> | EduKSX-Shop | `shop` | interner Shop für Hard- und Software, Schwerpunkt Klassenbestellungen | mittel | aktiv (Repo EduKSX-Shop) |
| <img src="https://raw.githubusercontent.com/MarkusKeller8200/EduKSX-UI/main/icons/svg/eduksx-sign-color.svg" width="32" alt=""> | EduKSX-Sign | `sign` | Dokumente unterschreiben über Anbieter wie Deepsign oder SwissSign | mittel | geplant |
| <img src="https://raw.githubusercontent.com/MarkusKeller8200/EduKSX-UI/main/icons/svg/eduksx-portal-color.svg" width="32" alt=""> | EduKSX-Portal | `portal` | Self-Service-Portal für Eltern, Ärztinnen und Ärzte, Zahnärztinnen und Zahnärzte und alle Externen | viele | geplant |
| <img src="https://raw.githubusercontent.com/MarkusKeller8200/EduKSX-UI/main/icons/svg/eduksx-intranet-color.svg" width="32" alt=""> | EduKSX-Intranet | `intranet` | interne Plattform, die Module, Schnittstellen, Wissen und Links zusammenbringt | viele | aktiv |
| <img src="https://raw.githubusercontent.com/MarkusKeller8200/EduKSX-UI/main/icons/svg/eduksx-services-color.svg" width="32" alt=""> | EduKSX-Services | `services` | reserviert, noch nicht definiert | – | reserviert |

Leitlinie (Chat 13.11.2026): **Module mit wenig oder keinen Personendaten bleiben eigenständig** (Glossary, Codex) und
lassen sich auch ohne die übrige Plattform nutzen. Module, die von den schulischen Stammdaten leben, gruppieren sich
um `connect`.

## 2. Gruppen

```text
 Plattform-Grundlagen      core · ident · ops
 Eigenständig, offen       glossary · codex
 Schulische Stammdaten     connect ─┬─ licence
                                    ├─ timetable
                                    └─ staffing
 Dienste für Mitarbeitende time · shop · sign
 Planung und Abläufe       planner ── flow
 Zugänge                   intranet (intern) · portal (extern)
```

## 3. Module und Systemgrenzen

Je Modul: was es **macht**, was es **nicht macht** (gehört woanders hin) und mit wem es spricht. Austausch nur über
APIs und Ereignisse (Plattform §5, DB E2) – kein Modul greift auf die Datenbank eines anderen zu.

### core – gemeinsame Bausteine
- **Macht:** HTTP-Basis, Fehlerformat, Listen, DB-Helfer, Konformitätstest, Steckbrief, Ereignisempfang, später
  OIDC-Client ([KONZEPT-CORE.md](KONZEPT-CORE.md)).
- **Nicht:** keine Daten, keine Oberfläche, kein Fachcode, keine Personen-Stammdaten.

### ident – Identity-Provider und Brücke
- **Macht:** Anmeldung, zweiter Faktor, Konten, Organisationen, Rollen je Modul; Brücke zu Entra, Google, Edulog
  ([KONZEPT-IDENT.md](KONZEPT-IDENT.md)).
- **Nicht:** keine Schülerdaten ohne Login, keine Klassen, keine Zuordnung zu Fremdsystemen (→ `connect`); keine
  Inhalte der Module. Beim Selbst-Hosting gibt es kein Ident (#40).

### ops – Leitstand
- **Macht:** Kunden, Verträge, Module und Versionen je Kunde, selbst gehostete Instanzen mit Heartbeat und
  Update-Ringen (S6) – [KONZEPT-LEITSTAND.md](KONZEPT-LEITSTAND.md).
- **Nicht:** keine Technik unserer Server (→ MarKusSX-Operation mit Komodo), keine Inhalte und keine Personendaten
  der Kunden.

### glossary – Begriffe und Abkürzungen
- **Macht:** zentrales Verzeichnis mit Erklärungen, Kategorien, Vorschlägen; öffentlich lesbar, Daten CC BY 4.0.
- **Nicht:** keine Rechtstexte (→ `codex`), keine Wissensseiten der Schule (→ `intranet`).
- **Stack:** Übersicht über Anwendung und Auslieferung in [STACK-GLOSSARY.md](STACK-GLOSSARY.md).

### codex – systematische Rechtssammlung
- **Macht:** Erlasse und Reglemente jeder Schul- und politischen Gemeinde mit Systematik, Versionen und Gültigkeit;
  öffentlich lesbar wie Glossary, Anmeldung wie Glossary (lokal, Ident optional). Jede Gemeinde nutzt Codex als eigene
  Rechtssammlung und bindet sie auf ihrer Homepage ein (JS-Baustein, iFrame oder öffentliche API) – mit eigenem CSS
  bzw. einem Template nach ihrer Homepage. Optionale Mustersystematik (Nummerierung, Namen), der die Gemeinde ihre
  Erlasse zuordnet oder Einträge deaktiviert; Einlieferung als PDF (optional MD als Grundlage für MCP) per Ziehen und
  Ablegen, E-Mail, OneDrive/SharePoint oder Dropbox mit Erkennung und Kategorievorschlag; später Gegenüberstellung
  mehrerer Gemeinden ([KONZEPT-CODEX.md](KONZEPT-CODEX.md), #119, #121).
- **Nicht:** keine Unterschriften (→ `sign`), keine allgemeinen Dokumentablagen (→ `intranet`), keine
  Genehmigungsabläufe (→ `flow`).

### connect – Stammdaten und Sync
- **Macht:** Personen (auch ohne Login), Klassen, Schuljahre mit Plattform-ID; Zuordnung der IDs in Fremdsystemen
  (M365/Entra, Google, Apple School Manager, Escola, CMI, LMVZ …); Abgleich mit Protokoll und Ereignissen (#43).
- **Nicht:** keine Anmeldung (→ `ident`, das für `connect` ein Zielsystem ist), keine Lizenzlogik (→ `licence`),
  keine Stundenpläne, keine Termine im Schuljahr (→ `planner`). `connect` ist führend für das Schuljahr (ID, Beginn,
  Ende; #115).

### licence – Lizenzen und Zugänge
- **Macht:** welche Person bzw. Klasse welche Software-Lizenz oder welchen Plattformzugang erhält; Zuweisung und
  Entzug beim Anbieter; Übersicht über Bestand.
- **Nicht:** keine Bestellung und kein Einkauf (→ `shop`), keine Personenstammdaten (→ `connect`). Eigenständig oder
  Teil von `connect`: OFFEN (#43).

### timetable – Stundenplan
- **Macht:** Lektionen, Klassen, SuS-Gruppen, LP und Räume zu einem Stundenplan; Änderungen und Ausfälle. Liest
  unterrichtsfreie Tage, Spezialwochen und Lager aus `planner` und lässt die Lektionen an diesen Tagen ausfallen oder
  ersetzt sie; zeigt bei betroffenen Lektionen die Stellvertretung aus `staffing` an (#115).
- **Nicht:** keine Arbeitszeit (→ `time`), keine Personaleinsatzplanung ausserhalb des Unterrichts (→ `staffing`),
  keine Stellvertretungen planen (→ `staffing`), keine Termine im Schuljahr (→ `planner`). Bezieht Personen und
  Klassen aus `connect`.

### staffing – Einsatzplanung
- **Macht:** Pensen und Einsätze von Mitarbeitenden und Lehrpersonen planen (wer arbeitet wann, wo, mit welchem
  Pensum); Stellvertretungen (wer vertritt wen, wann; beschlossen 26.11.2026, #115).
- **Nicht:** keine Lektionsplanung (→ `timetable`), keine erfasste Ist-Zeit (→ `time`).

### planner – Jahresplanung
- **Macht:** Jahreskalender und Jahresplanung je Schuljahr (beschlossen 26.11.2026, #112, #115):
  - Ferien und unterrichtsfreie Tage (Brückentage, schulfreie Halbtage, Weiterbildungstage der LP)
  - Anlässe und Spezialwochen (Projektwochen, Lager, Sporttage, Elternabende) mit Klassen bzw. Teilnehmenden
  - Organisationsplanung der Schulleitung: Fristen, Sitzungen, Konvente, Zuständigkeiten
  - Hängt die Termine an das Schuljahr aus `connect` und stellt sie über API und Ereignisse bereit – für `timetable`
    (Ausfall, Ersatz) und `flow` (Auslöser, Fristen).
- **Nicht:** kein eigenes Schuljahr als Stammdaten (→ `connect`), keine Abläufe (→ `flow`), keine Lektionen und
  keine Ersatzstundenpläne (→ `timetable`), keine Einsätze und Stellvertretungen (→ `staffing`), keine Stoff- oder
  Themenplanung des Unterrichts.

### flow – Abläufe
- **Macht:** fachliche Abläufe mit Menschen: Schritte, Zuständigkeiten, Aufgaben, Bewilligungen, Fristen und Status.
  Ruft für die einzelnen Schritte Vorgänge in den anderen Modulen über deren API auf (beschlossen 26.11.2026, #112).
  - Formulare von Externen: `portal` erfasst und nimmt entgegen, danach startet ein Ablauf in `flow`; `portal` zeigt
    nur den Status an.
  - Unterschriften: `flow` startet die Unterschrift in `sign` als Schritt und wartet auf das Ereignis «unterschrieben».
  - Termine: aus `planner` als Auslöser oder Frist (z. B. «4 Wochen vor Schuljahresbeginn»).
- **Nicht:** keine Formulare für Externe (→ `portal`), keine Signatur (→ `sign`), kein eigener Kalender
  (→ `planner`), keine technische Synchronisation (→ `connect`/EduKSX-Connectors: Daten abgleichen, Zeitplan,
  Wiederholen). `flow` darf einen Abgleich anstossen, steuert ihn aber nicht.

### time – Zeiterfassung
- **Macht:** geleistete Arbeitszeit erfassen oder aus externen Systemen übernehmen; Saldi und Auswertungen.
- **Nicht:** keine Planung (→ `staffing`, `timetable`), keine Lohnabrechnung.

### shop – interner Shop
- **Macht:** Mitarbeitende und Lehrpersonen bestellen Hard- und Software, besonders Klassenbestellungen; Freigaben
  und Budget.
- **Nicht:** keine Zuweisung der gekauften Lizenzen (→ `licence`), keine Geräteverwaltung (MDM wie Jamf/Intune
  bleibt extern, angebunden über `connect`).

### sign – Unterschriften
- **Macht:** Dokumente zur Unterschrift senden, Status verfolgen, signierte Dokumente zurückgeben – über Anbieter wie
  Deepsign oder SwissSign. Dienst für andere Module (z. B. `codex`, `portal`, `intranet`) über API.
- **Nicht:** keine eigene Dokumentablage, keine eigene Signatur-Infrastruktur, keine Abläufe über die Unterschrift
  hinaus (→ `flow` ruft `sign` als Schritt auf).

### portal – Self-Service für Externe
- **Macht:** Zugang für Eltern, Ärztinnen und Ärzte, Zahnärztinnen und Zahnärzte und weitere Externe: Formulare,
  Anmeldungen, Unterschriften, Mitteilungen.
- **Nicht:** nichts für Mitarbeitende (→ `intranet`); keine eigenen Stammdaten (Personen aus `connect`); keine
  Bearbeitung eingegangener Formulare (→ Ablauf in `flow`, `portal` zeigt den Status).

### intranet – interne Plattform
- **Macht:** Einstieg für Mitarbeitende und Lehrpersonen; bringt Module, Schnittstellen, Wissen und Links zusammen –
  über Plugins (§4).
- **Nicht:** übernimmt keine Fachdaten anderer Module; zeigt sie über deren API an.

## 4. Integration über Plugins (Konzept: [KONZEPT-PLUGINS.md](KONZEPT-PLUGINS.md))

Das Intranet – später auch das Portal – bindet Module und Fremdsysteme über **Plugins** an:

- Ein **Plugin** gehört zu genau einem Modul bzw. Fremdsystem (z. B. Glossary, Codex, M365) und spricht nur über
  dessen **API**: bei EduKSX-Modulen die Daten-API nach S8 mit Token nach S2, bei Fremdsystemen deren Schnittstelle.
- Ein Plugin liefert, was der Gastgeber anzeigt: Kacheln bzw. Widgets, Menüeinträge, Treffer für die gemeinsame
  Suche, Einstellungen; die Rechte kommen aus den Scopes im Steckbrief des Moduls (S5).
- Eingebettet wird bevorzugt über Web-Komponenten und Permalinks (wie heute `<glossary-term>`, Plattform S8) –
  keine Datenbankzugriffe, kein Kopieren von Fachdaten.
- Funktioniert auch beim Selbst-Hosting: Das Glossary oder der Codex können als öffentliche Dienste angebunden sein,
  ohne dass der Kunde sie selbst betreibt.

Offen für das Konzept (#44): Plugin als Composer-Paket im Gastgeber oder als reine Beschreibung (Manifest) mit
Web-Komponenten des Moduls; Versionierung der Plugin-Schnittstelle; Freigabe von Plugins Dritter.

## 5. Verlauf

- 13.11.2026: Übersicht angelegt – Zweck und Kurzbeschreibung aller Module aus dem Chat, Abgrenzungen, Gruppen,
  Plugin-Integration; `staffing` neu vergeben; Icon-Entwürfe für intranet, timetable, staffing, ops.
- 13.11.2026: Icons für intranet, timetable, staffing, ops freigegeben.
- 22.11.2026: Sichtbare Namen nach M1 (EduKSX-UI KONZEPT-MARKE): alle `EduKSX-<Begriff>` mit deutschem Untertitel.
  Neues Modul `planner` EduKSX-Planner «Jahresplanung».
