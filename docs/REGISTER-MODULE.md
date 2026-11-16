# Modulregister der EduKSX-Plattform

Stand: 13.11.2026 · Verantwortlich: Markus Keller · Status: **BESCHLOSSEN** 13.11.2026

Einzige Quelle für die **Modulschlüssel**. DB-Standard (E1) und API-Standard (G2) verweisen hierher. Änderungen nur per
Pull Request.

## Regeln

- **Schlüssel intern, englisch, unveränderlich:** Kleinbuchstaben, ohne Bindestrich, englisch (DB A1). Der Schlüssel
  benennt Schema, Datenbankzugänge, Löschregister, Ereignisse (`<key>.<objekt>.<verb>`), Fehlertypen, Token-Präfixe,
  MCP-Werkzeuge und API-Pfade. Ist er einmal vergeben, ändert er sich nie.
- **Marketingname frei:** Wie ein Modul gegenüber Kundinnen und Kunden heisst, wird situativ festgelegt und darf sich
  ändern, ohne dass Code, Datenbank oder API angepasst werden. Die Spalte «Marketingname» ist nur ein Hinweis.
- **Status:** `aktiv` (Repo vorhanden), `geplant` (Schlüssel vergeben, noch kein Repo), `reserviert` (für die
  Produktfamilie freigehalten, noch kein Modul).

## Register

Beschreibung, Abgrenzung und Icons je Modul: [MODULE-UEBERSICHT.md](MODULE-UEBERSICHT.md).

| Schlüssel | Modul (intern) | Marketingname (Stand) | Repo | Betriebsart | Status |
| --- | --- | --- | --- | --- | --- |
| `core` | gemeinsame Bibliothek `eduksx/core` (kein Dienst, Plattform 4.3) | Teil von «EduKSX-Core» | EduKSX-Core | Paket | aktiv (0.1.0) |
| `ident` | Anmeldung, Konten, Organisationen, Rollen | Teil von «EduKSX-Core» | EdukSX-Ident | zentral | aktiv (Brücke 0.1, unveröffentlicht) |
| `ops` | Leitstand: Kunden, Instanzen, Versionen, Updates, Zustand | Teil von «EduKSX-Core» | – | intern | geplant |
| `glossary` | Glossar | EduKSX-Glossary | EduKSX-Glossary | zentral | aktiv |
| `codex` | Rechtssammlung | EduKSX-Codex | EduKSX-Codex | zentral | aktiv |
| `intranet` | Intranet einer Schule | Intranet | sek-intranet | isoliert | aktiv |
| `timetable` | Stundenplan | Stundenplan | – | isoliert | geplant |
| `connect` | Stammdaten und Sync mit Fremdsystemen (M365, ASM, Escola, CMI, LMVZ …) | EduKSX-Connect | – | offen | geplant (#43) |
| `licence` | Zuweisung von Softwarelizenzen und Plattformzugängen | EduKSX-Licence | – | offen | geplant (#43: eigenständig oder Teil von `connect`) |
| `portal` | Self-Service-Portal für Eltern, Ärztinnen, Zahnärzte und alle Externen der Schule | EduKSX-Portal | EduKSX-Portal | offen | aktiv (Repo angelegt 16.11.2026) |
| `shop` | interner Shop für Mitarbeitende und Lehrpersonen (Hard- und Software, Klassenbestellungen) | EduKSX-Shop | – | offen | geplant |
| `sign` | Dokumente unterschreiben über Anbieter (z. B. Deepsign, SwissSign) | EduKSX-Sign | – | offen | geplant |
| `time` | Zeiterfassung für Mitarbeitende und Lehrpersonen bzw. Anbindung externer Systeme | EduKSX-Time | – | offen | geplant |
| `staffing` | Einsatzplanung von Mitarbeitenden und vor allem Lehrpersonen | EduKSX-Staffing | – | offen | geplant |
| `services` | Produktfamilie | – | – | – | reserviert (noch nicht definiert) |

**Kein Modul:** Repo **EduKSX-Suite** (angelegt 13.11.2026, leer) ist das Verteilpaket für das Selbst-Hosting (Installer, Update-Dienst,
VM-Vorlage; [KONZEPT-SELBSTHOSTING.md](KONZEPT-SELBSTHOSTING.md)) und erhält keinen Modulschlüssel.

## Umbenennungen

| Datum | bisher | neu | Grund |
| --- | --- | --- | --- |
| 13.11.2026 | `recht` (DB-Standard) | `codex` | Widerspruch DB/API bereinigt; englisch (API-E35) |
| 13.11.2026 | `stundenplan` | `timetable` | interne Bezeichnungen englisch |
| 13.11.2026 | `leitstand` | `ops` | interne Bezeichnungen englisch |

Alle drei Module hatten noch kein Repo und keine Daten; die Umbenennung war ohne Migration möglich.
