# Konzept: Technologie-Stack und gemeinsame Muster (0.4.0, #79)

Stand: 25.11.2026 · Verantwortlich: Markus Keller · Status: **BESCHLOSSEN** 25.11.2026 (Chat, Entscheide ST1–ST5);
Punkte mit **ZU PRÜFEN** sind Vorschläge.

Schliesst die Lücke «Einheitlicher Stack» der [Lückenanalyse](LUECKENANALYSE-0.4.0.md) (Bereich 6): Bisher war nur
das Backend über die [Modulvorlage](KONZEPT-MODULVORLAGE.md) festgelegt. Ergänzt [Plattform §6](KONZEPT-PLATTFORM.md)
und die Modulvorlage. Werkzeuge des Betriebs stehen weiterhin nur in Plattform 7.3a bzw. MarKusSX-Operation.
Verbindlichkeit: Stufen nach [KONZEPT-VORLAGE.md](KONZEPT-VORLAGE.md).

## 1. Ziel

Alle Module bauen auf demselben Stack, in Versionen, die noch Fehlerkorrekturen erhalten. Wer ein Modul kennt, findet
sich in jedem anderen zurecht; Bausteine aus `eduksx/core` und `@eduksx/ui` passen überall.

**Nichtziele:**
- keine Vorgabe für Werkzeuge des Betriebs (→ Plattform 7.3a, MarKusSX-Operation)
- keine Vorgabe für Bibliotheken innerhalb eines Moduls, solange sie Lizenz- und Pflegeprüfung bestehen (`third-party.json`)
- keine Vorgabe für Prototypen (EduKSX-Prototyp) und reine Konzept-Repos

## 2. Plattformvorgabe (BESCHLOSSEN, ST1)

| Bereich | Vorgabe | Begründung |
| --- | --- | --- |
| Backend | **Laravel** mit PHP | Modulvorlage und `eduksx/core` sind Laravel-Pakete; Mandanten, Warteschlangen, Tests eingebaut; erprobt in Glossary, Intranet, Ident |
| Oberfläche | **Inertia** mit **React** und **TypeScript** | eine Anwendung statt getrennter Frontend-App; `@eduksx/ui` liefert React-Bausteine; Glossary und Intranet nutzen es schon |
| Gestaltung | **Tailwind CSS** mit **`@eduksx/ui`** (Tokens, Themes, Bausteine) | [KONZEPT-DESIGN.md](KONZEPT-DESIGN.md); Farben nur über Tokens |
| Build | **Vite** (auch Vite+) | Standard von Laravel und Inertia |
| Datenbank | **SQLite** (isoliert, klein) oder **PostgreSQL** (zentral) | [DB-Standard](KONZEPT-DB-GUIDELINE.md), Tests auf beiden |
| Auslieferung | **Docker-Image** je Modul | Plattform §6 «Betrieb» |

Gilt für jedes Modul mit eigener Oberfläche. Module ohne Oberfläche (z. B. reine Dienste) brauchen nur Backend,
Datenbank und Auslieferung. Abweichungen nur mit Eintrag im **Ausnahmeregister** ([API-Standard D8](KONZEPT-API-GUIDELINE.md))
mit Grund und Ablaufdatum.

## 3. Versionen (BESCHLOSSEN, ST2)

Mindestversionen für alle Module ab **31.12.2026**:

| Komponente | Mindestversion | Fehlerkorrekturen bis | Nächster Wechsel spätestens |
| --- | --- | --- | --- |
| PHP | **8.5** | 31.12.2027 | PHP 8.6 bis 31.12.2027 |
| Laravel | **13** | Q3 2027 | Laravel 14 bis Q3 2027 (verlangt PHP 8.4, erfüllt) |
| Node.js (Build, Tests) | **26 LTS** | 27.10.2027 (Ende aktive LTS-Phase) | Node 28 bis 27.10.2027 |
| PostgreSQL | **18** | 14.11.2030 | – (neue Major erst nach eigenem Entscheid) |
| React, Inertia, TypeScript, Tailwind | jeweils aktuelle Major (heute React 19, Inertia 3, TypeScript 7, Tailwind 4) | je Projekt | Regel ST3 |

Quellen der Daten: php.net «Supported Versions», Laravel «Support Policy», Node.js «Releases», PostgreSQL «Versioning
Policy» (Stand 25.11.2026). Die Tabelle wird bei jedem Wechsel nachgeführt.

## 4. Wechselregel (BESCHLOSSEN, ST3)

- Ein Modul läuft **immer auf Versionen, die noch Fehlerkorrekturen erhalten** – nicht nur Sicherheitsupdates.
  - PHP: «Active Support» (2 Jahre ab Erscheinen)
  - Laravel: «Bug Fixes Until» (18 Monate)
  - Node.js: Phase «Active LTS»; die Phase «Maintenance» genügt nicht
  - PostgreSQL: unterstützte Major (Fehlerkorrekturen über die Minor-Releases bis zum Ende)
  - Bibliotheken: unterstützte Major laut Projekt
- **Spätestens am letzten Tag** der Fehlerkorrekturen ist das Modul umgestellt und als Release auf prod.
- **Übergang (BESCHLOSSEN, ST2):** Alle bestehenden Module wechseln bis **31.12.2026** auf PHP 8.5, Node 26 und
  PostgreSQL 18 (bestehende PostgreSQL-Datenbanken und die CI). Danach gilt die Regel ohne Übergang.
- **Überwachung:** Workflow «Fremdkomponenten prüfen» (Blueprint, monatlich) und Dependabot melden neue Versionen;
  der Leitstand zeigt je Instanz die Versionen (S5). ZU PRÜFEN: eine Prüfung in `ci:check`, die bei einer Version
  ohne Fehlerkorrekturen scheitert.
- **Selbst-Hosting:** Das Image bringt PHP und Node mit; Kundinnen und Kunden betreiben nur PostgreSQL selbst. Die
  Installationsanleitung nennt die Mindestversion; ältere Versionen meldet `/health` als Warnung.

## 5. Gemeinsamer Prüfbefehl (BESCHLOSSEN, ST4)

Jedes Modul hat **`composer ci:check`** – derselbe Befehl lokal und in der CI (Workflow `pruefungen`). Vorbild ist das
Glossary:

| Schritt | Inhalt |
| --- | --- |
| PHP-Stil und Analyse | Pint, PHPStan (Stufe nach den Qualitätszielen, #80) |
| Oberfläche | Linter und Format (`npm run check`), Typprüfung (`tsc`), JavaScript-Tests |
| Tests | PHPUnit auf SQLite **und** PostgreSQL, inkl. Konformitätstest aus `eduksx/core` (API D8) |
| Schnittstelle | Spectral-Regelsatz `eduksx`, `oasdiff` gegen die letzte Version (API D3) |
| Barrierefreiheit | axe-core («serious»/«critical» als Fehler, DS7) |

Die Modulvorlage trägt den Befehl ein ([KONZEPT-MODULVORLAGE.md §4.1](KONZEPT-MODULVORLAGE.md)).

## 6. Feature-Schalter und Einstellungen (BESCHLOSSEN, ST5)

Muster aus dem Glossary (`App\Support\Settings`, #106, #366), als Baustein in **`eduksx/core`**:

- **Definition im Code:** je Einstellung Schlüssel, Gruppe, Bezeichnung, Hinweis, Typ (`bool`, `int`, `choice`,
  `text`, `url`, `email`, `secret`) und optional eine **Umgebungsvariable**.
- **Vorrang:** Umgebungsvariable gesetzt → Wert gilt und die Einstellung ist in der Administration **gesperrt**
  (mit Hinweis auf die Variable). Sonst gilt der Wert aus der Administration, sonst die Vorgabe aus der Konfiguration.
- **Speicherung:** nur Abweichungen von der Vorgabe (Tabelle `settings`); Geheimnisse verschlüsselt, nie angezeigt.
- **Rechte und Nachweis:** Ändern nur mit einem systemkritischen Recht, jede Änderung im Protokoll (DB A7).
- **Herkunft sichtbar:** Die Administration zeigt je Wert «Umgebung», «Administration» oder «Vorgabe».
- **Feature-Schalter** sind Einstellungen vom Typ `bool`; ein Schalter ohne Wirkung wird mit dem nächsten MINOR entfernt.
- Kommt in Core, sobald das zweite Modul es braucht (Core 4.1) – Glossary und Intranet erfüllen das; Fahrplan in
  [KONZEPT-CORE.md](KONZEPT-CORE.md) ZU PRÜFEN (Core-Minor nach 0.3).

## 7. Stand der Module und Übergang

| Modul | Heute | Bis 31.12.2026 umzustellen |
| --- | --- | --- |
| Glossary | PHP ^8.4 (Image 8.4), Laravel 13, Inertia 3, React 19; CI mit Node 22 und PostgreSQL 16 | PHP 8.5, Node 26, PostgreSQL 18 in der CI |
| Intranet (sek-intranet) | PHP ^8.3 (Image 8.4), Laravel 13, Inertia 3, React 19; CI mit Node 22 | PHP 8.5, Node 26 |
| Core | PHP ^8.4, Laravel 13 | PHP-Anforderung auf 8.5 |
| Ident (Brücke) | PHP ^8.4, Laravel 13 | PHP 8.5, Node 26 |
| übrige Module | noch ohne Code | starten direkt mit diesem Stand |

Die Umstellung ist ein Folgeauftrag je Modul-Repo (#83). Bis dahin ist keine Ausnahme nötig; ein Modul, das den
31.12.2026 nicht schafft, braucht einen Eintrag im Ausnahmeregister.

## 8. Entscheide

| Nr. | Frage | Optionen | Entscheid | Status |
| --- | --- | --- | --- | --- |
| ST1 | Frontend als Plattformvorgabe? | Vorgabe mit Ausnahmeregister / nur Empfehlung / offen lassen | Inertia, React, TypeScript, Tailwind und `@eduksx/ui` als Vorgabe; Abweichung nur mit Ausnahmeregister | BESCHLOSSEN 25.11.2026 |
| ST2 | Mindestversionen | 8.4·13·Node 24·PG 18 / 8.4·13·Node 26·PG 18 / heutiger Stand | zuerst 8.4·13·Node 24·PG 18; wegen ST3 **sofort umgestellt** auf PHP 8.5, Laravel 13, Node 26, PostgreSQL 18, Übergang bis 31.12.2026 | BESCHLOSSEN 25.11.2026 |
| ST3 | Wann wechseln? | 6 Monate vor Ende Sicherheit / bei Ende der Fehlerkorrekturen / bei Ende Sicherheit | **bei Ende der Fehlerkorrekturen** | BESCHLOSSEN 25.11.2026 |
| ST4 | Gemeinsamer Prüfbefehl | aus Glossary übernehmen / je Modul | `composer ci:check` nach Glossary in der Modulvorlage | BESCHLOSSEN 25.11.2026 |
| ST5 | Feature-Schalter | Baustein in Core / je Modul / nur beschreiben | Muster aus Glossary als Baustein in `eduksx/core` | BESCHLOSSEN 25.11.2026 |

## 9. Verlauf

- 25.11.2026: Konzept angelegt (#79), ST1–ST5 im Chat entschieden.
