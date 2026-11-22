# Modulregister der EduKSX-Plattform

Stand: 20.11.2026 · Verantwortlich: Markus Keller · Status: **BESCHLOSSEN** 13.11.2026

Einzige Quelle für die **Modulschlüssel**. DB-Standard (E1) und API-Standard (G2) verweisen hierher. Änderungen nur per
Pull Request.

## Regeln

- **Schlüssel intern, englisch, unveränderlich:** Kleinbuchstaben, ohne Bindestrich, englisch (DB A1). Der Schlüssel
  benennt Schema, Datenbankzugänge, Löschregister, Ereignisse (`<key>.<objekt>.<verb>`), Fehlertypen, Token-Präfixe,
  MCP-Werkzeuge und API-Pfade. Ist er einmal vergeben, ändert er sich nie.
- **Marketingname frei:** Wie ein Modul gegenüber Kundinnen und Kunden heisst, wird situativ festgelegt und darf sich
  ändern, ohne dass Code, Datenbank oder API angepasst werden. Die Spalte «Marketingname» ist nur ein Hinweis; sie folgt dem
  Entscheid M1 (EduKSX-UI `docs/KONZEPT-MARKE.md`, 22.11.2026): `EduKSX-<Begriff>`, deutsche Bezeichnung als Untertitel.
- **Status:** `aktiv` (Repo vorhanden), `geplant` (Schlüssel vergeben, noch kein Repo), `reserviert` (für die
  Produktfamilie freigehalten, noch kein Modul).

## Register

Beschreibung, Abgrenzung und Icons je Modul: [MODULE-UEBERSICHT.md](MODULE-UEBERSICHT.md).

| Schlüssel | Modul (intern) | Marketingname (Stand) | Repo | Betriebsart | Status |
| --- | --- | --- | --- | --- | --- |
| `core` | gemeinsame Bibliothek `eduksx/core` (kein Dienst, Plattform 4.3) | EduKSX-Core | EduKSX-Core | Paket | aktiv (0.2.0) |
| `ident` | Anmeldung, Konten, Organisationen, Rollen | EduKSX-Ident | EduKSX-Ident | zentral | aktiv (Brücke 0.1, unveröffentlicht) |
| `ops` | Leitstand: Kunden, Instanzen, Versionen, Updates, Zustand | EduKSX-Ops | – | intern | geplant |
| `glossary` | Glossar | EduKSX-Glossary | EduKSX-Glossary | zentral | aktiv |
| `codex` | Rechtssammlung | EduKSX-Codex | EduKSX-Codex | zentral | aktiv |
| `intranet` | Intranet einer Schule | EduKSX-Intranet | sek-intranet | isoliert | aktiv |
| `timetable` | Stundenplan | EduKSX-Timetable | – | isoliert | geplant |
| `connect` | Stammdaten und Sync mit Fremdsystemen (M365, ASM, Escola, CMI, LMVZ …) | EduKSX-Connect | EduKSX-Connect | offen | aktiv (Repo angelegt 16.11.2026; #43) |
| `licence` | Zuweisung von Softwarelizenzen und Plattformzugängen | EduKSX-Licence | – | offen | geplant (#43: eigenständig oder Teil von `connect`) |
| `portal` | Self-Service-Portal für Eltern, Ärztinnen, Zahnärzte und alle Externen der Schule | EduKSX-Portal | – | offen | geplant |
| `shop` | interner Shop für Mitarbeitende und Lehrpersonen (Hard- und Software, Klassenbestellungen) | EduKSX-Shop | EduKSX-Shop | offen | aktiv (Repo angelegt 16.11.2026) |
| `sign` | Dokumente unterschreiben über Anbieter (z. B. Deepsign, SwissSign) | EduKSX-Sign | – | offen | geplant |
| `time` | Zeiterfassung für Mitarbeitende und Lehrpersonen bzw. Anbindung externer Systeme | EduKSX-Time | EduKSX-Time | offen | aktiv (Repo angelegt 16.11.2026) |
| `staffing` | Einsatzplanung von Mitarbeitenden und vor allem Lehrpersonen | EduKSX-Staffing | – | offen | geplant |
| `flow` | Abläufe und Termine: Schritte, die Vorgänge in den anderen Modulen aufrufen; Jahreskalender | EduKSX-Flow | EduKSX-Flow | offen | aktiv (Repo angelegt, Prototyp in EduKSX-Prototyp) |
| `planner` | Jahresplanung (Abgrenzung zu `flow` OFFEN) | EduKSX-Planner | – | offen | geplant (neu 22.11.2026) |
| `services` | Produktfamilie | – | – | – | reserviert (noch nicht definiert) |

**Kein Modul:** Repo **EduKSX-Suite** (angelegt 13.11.2026, leer) ist das Verteilpaket für das Selbst-Hosting (Installer, Update-Dienst,
VM-Vorlage; [KONZEPT-SELBSTHOSTING.md](KONZEPT-SELBSTHOSTING.md)) und erhält keinen Modulschlüssel. Ebenso ohne Schlüssel
(22.11.2026, Gesamtprüfung W13): **EduKSX-Connectors** (Sammlung der Anbindungen an Fremd-APIs, Grundlage für `connect`)
und **EduKSX-Prototyp** (Prototypen und Umsetzungsgrundlagen, kein produktives Modul). Ebenso ohne Schlüssel das Repo
**EduKSX-UI** (npm-Paket `@eduksx/ui`, Design-System, [KONZEPT-DESIGN.md](KONZEPT-DESIGN.md); Repo angelegt 22.11.2026, öffentlich).

## Umbenennungen

| Datum | bisher | neu | Grund |
| --- | --- | --- | --- |
| 13.11.2026 | `recht` (DB-Standard) | `codex` | Widerspruch DB/API bereinigt; englisch (API-E35) |
| 13.11.2026 | `stundenplan` | `timetable` | interne Bezeichnungen englisch |
| 13.11.2026 | `leitstand` | `ops` | interne Bezeichnungen englisch |

Alle drei Module hatten noch kein Repo und keine Daten; die Umbenennung war ohne Migration möglich.
