# Konzept: Design-System und Themes (`@eduksx/ui`, 0.4.0, #75)

Stand: 22.11.2026 · Verantwortlich: Markus Keller · Status: **BESCHLOSSEN** 22.11.2026 (Entscheide im Chat), Punkte mit
**ZU PRÜFEN** sind Vorschläge.

Konkretisiert [Plattform 4.3 und §6 «Oberfläche»](KONZEPT-PLATTFORM.md), [Core C10](KONZEPT-CORE.md) und
[Plugins P5](KONZEPT-PLUGINS.md). Grundlagen: CI-Manual v1.0 und Markenfortschreibungen (Repo markussxch,
`docs/brand/`), EduKSX-Produktfamilie (`docs/products/`), Intranet (`docs/KONZEPT-THEMES.md`, `docs/GUI-KOMPONENTEN.md`,
`docs/KONZEPT-DESIGN.md`), Glossary (`docs/KONZEPT-DESIGN.md`, DEC-015, DEC-023). Verbindlichkeit: Stufen nach
[KONZEPT-VORLAGE.md](KONZEPT-VORLAGE.md).

## 1. Ziel

Alle EduKSX-Module sehen gleich aus und bedienen sich gleich – mit **einer** Quelle für Farben, Schrift und Abstände
und **einem** Satz Bausteine. Organisationen können ihr eigenes Theme haben, ohne dass Barrierefreiheit oder Marke
leiden.

**Nichtziele:**
- keine Gestaltung am Code vorbei (Entwurfswerkzeuge liefern Vorschläge, der Code bleibt verbindlich)
- kein Code automatisch aus Entwürfen
- kein eigenes Aussehen je Modul (Module unterscheiden sich über ihr Icon)

## 2. Zwei Quellen, eine Regel (BESCHLOSSEN)

| Was | Quelle |
| --- | --- |
| Wortmarke, Markenfarben, Schrift, Signets, Schreibweisen | CI von MarKusSXCH (markussxch `docs/brand/`) |
| Bausteine, Verhalten, Theme-Technik | Intranet (GUI-Prototypen), weitergeführt in `@eduksx/ui` |

Bei Widerspruch gilt für Farbe und Marke das CI, für Bedienung das Intranet bzw. `@eduksx/ui`. **Barrierefreiheit geht
immer vor** (WCAG 2.1 AA, eCH-0059).

## 3. Design-Tokens (BESCHLOSSEN)

- **Eine Quelle:** `tokens.json` im Format der W3C Design Tokens Community Group (DTCG) im Repo EduKSX-UI.
- **Build** (z. B. Style Dictionary) erzeugt daraus:
  - CSS-Variablen für hell und dunkel mit den Namen der Bausteine (`--background`, `--foreground`, `--primary`,
    `--muted-foreground`, `--link`, `--ring`, `--term-underline`, Status, Seitenleiste, Diagramme …) und die
    Markenwerte `--brand-*` des CI,
  - das Theme für Tailwind 4,
  - die Variablen `--eduksx-*` für Web-Komponenten der Plugins (P5),
  - die Liste der bekannten Tokens für Themes (5).
- **Standardwerte «EduKSX»** wie im Glossary (DEC-015): Orange `#FF8A00` als Fläche mit dunkler Schrift, Link und Fokus
  `#0272AD` (dunkel `#32B8F2`), Sekundärtext `#5A6678`, Schrift **Inter** selbst gehostet; Status-Farben wie im
  Intranet.
- **Kontrastprüfung** in der CI: Text ≥ 4,5 : 1, Linien und Fokus ≥ 3 : 1, hell und dunkel (Paare aus dem
  Kontrasttest des Glossary).
- **Penpot** (Intranet-Konzept Stufe 2/3) darf `tokens.json` lesen und schreiben; Änderungen kommen als Pull Request.
  Nicht Pflicht.

## 4. Bausteine in `@eduksx/ui` (BESCHLOSSEN)

- **Repo EduKSX-UI** (angelegt 22.11.2026, öffentlich), npm-Paket `@eduksx/ui`, Lizenz MIT (Plattform §9.7), eigene Versionen und Frontend-CI; Core
  bleibt PHP (Core C10, geändert 22.11.2026).
- **Start (0.1):** Tokens und Build, Kontrasttest, `BrandWordmark` nach dem Komponentenkontrakt des CI (Markenschlüssel
  `education` plus Produktzusatz, `aria-label`, nur Tokens), **Kopfzeile mit Modulwechsel** (S7), **Verlauf** (Anzeige
  von `data_changes` bzw. Revisionen, DB A7, #73).
- **Danach:** die Bausteine, die das Glossary bereits aus dem Intranet übernommen hat (`ui/*` auf Basis shadcn/Radix,
  Data-Grid, Begriff, Theme-Bereich, Layouts), in der Reihenfolge, in der ein zweites Modul sie braucht.
- **Übernahme mit Herkunft:** Kopfkommentar `Übernommen aus sek-intranet <Pfad> @ <Commit>`, Liste im Repo; keine
  Namen, Texte, Pfade, Rechte oder das Branding der Schule; Lizenz der übernommenen Teile geprüft (das Intranet ist
  privat, das Paket öffentlich).
- **Farbneutral:** Bausteine nutzen nur Tokens (`bg-primary`, `text-muted-foreground` …), nie feste Farbwerte.
- **Musterseite:** Die GUI-Prototypen wandern mit den Bausteinen in EduKSX-UI, als eigene Testseite (Vite + React,
  GitHub Pages, kein Storybook; DS7). Jeder UI-Entscheid wird dort hell und dunkel in allen Pflicht-Ansichten (DS9)
  sichtbar gemacht.

## 5. Themes (BESCHLOSSEN)

| Theme | Wer | Regel |
| --- | --- | --- |
| **EduKSX (Standard)** | alle | aus `tokens.json`, nicht änderbar ausser im Code |
| **Hoher Kontrast** | alle | mitgeliefert (DS11), hell und dunkel, wählbar |
| **Violett** | alle | mitgeliefert (DS11), hell und dunkel, wählbar |
| **Theme der Organisation** | Admin der Organisation | ganzes Theme (alle bekannten Tokens, hell und dunkel); gespeichert werden nur Abweichungen |

- **Mitgeliefert (DS11, Idee EduKSX-UI #18):** immer EduKSX plus die zwei Alternativen Hoher Kontrast und Violett,
  definiert in `tokens.json` von EduKSX-UI und dort durch die Kontrastprüfung abgesichert. Weitere Themes legt die
  Organisation an; der Admin der Organisation gibt frei, welche Themes zur Wahl stehen, die Person wählt aus dieser
  Liste.
- Nur **bekannte Tokens** und nur `#rrggbb` werden gespeichert und ausgegeben (Technik Intranet `Themes::GROUPS`).
- Ein Theme der Organisation lässt sich erst **aktivieren, wenn die Kontrastprüfung bestanden ist** (strenger als heute im
  Intranet, wo sie nur warnt).
- Es gilt im **Kontext der Organisation** (isolierte Instanz; in zentralen Modulen bei angemeldeten Personen der
  Organisation bzw. in ihrer Organisations-Darstellung). Öffentliche Seiten zentraler Module ohne Organisationskontext
  bleiben im Standard.
- **Unverändert bleiben:** EduKSX-Wortmarke und Signets (Farben nach CI), Fokus-Sichtbarkeit, Statusbedeutung
  (Erfolg, Warnung, Fehler immer mit Symbol und Text). **Marke links oben** (KONZEPT-MARKE M3, EduKSX-UI): entweder die
  EduKSX-Wortmarke des Moduls oder ein **eigenes Logo der Instanz** (White-Label); MarKusSXCH nur in der Signatur.
- Hell, dunkel oder System wählt die Person (DS8).
- **Ausnahme Codex-Einbettung (DS14):** Für die auf der Homepage einer Gemeinde eingebettete Rechtssammlung darf die
  Gemeinde eigenes CSS hinterlegen (geprüft beim Speichern, wirkt nur im Baustein, Kontrastprüfung warnt). Codex selbst
  und seine Administration bleiben bei DS4 ([KONZEPT-CODEX.md](KONZEPT-CODEX.md) §4.2).

**Intranet (BESCHLOSSEN):** Das Intranet stellt auf `@eduksx/ui` und den Standard «EduKSX» um; das heutige Aussehen
(Farben der Sekundarschule Bülach, Open Sans) bleibt als **Theme der Instanz** erhalten. Umsetzung als Issue im
Intranet (#83), nicht rückwirkend.

## 6. Seiten und Texte (BESCHLOSSEN, aus dem Glossary)

- Breiten: darstellungsoptimiert 1152 px, breit 1536 px, voll; Fliesstext auf Lesebreite (`max-w-prose`) (Glossary
  DEC-023).
- Kopfzeile auf Website und Administration gleich: Wortmarke, Modulwechsel, Suche, Ansicht, Farbschema, Person.
- **Farbschema (DS8, Idee EduKSX-UI #17):** Jedes Modul bietet in der Kopfzeile rechts den Umschalter Hell / Dunkel /
  Wie System mit den Symbolen Sonne, Mond und Sonne-Mond an (Baustein `ColorSchemeToggle`, Hook `useColorScheme`).
  Vorgabe «Wie System», gespeichert je Browser.
- **Ansichten (DS9, Idee EduKSX-UI #19):** Jedes Modul bietet auf dem Desktop die Ansichten Darstellungsoptimiert,
  Breit und Voll sowie Vollbild an (Bausteine `ViewWidthToggle`, `FullscreenButton`), Vorgabe Darstellungsoptimiert.
  Jede Oberfläche wird in den **Pflicht-Ansichten** geprüft: Handy hoch und quer, Tablet hoch und quer,
  Darstellungsoptimiert, Breit, Voll, jeweils hell und dunkel. Die Testseite von EduKSX-UI schaltet sie direkt um.
- **Symbole (DS10, Idee EduKSX-UI #20):** Bediensymbole aus Lucide (ISC), Modul-Icons aus dem EduKSX-Set; Symbol-Knöpfe
  immer mit `aria-label`, gleichlautendem Tooltip und bei Umschaltern `aria-pressed`; jede Option eines Umschalters
  mit eigenem Symbol; Warnung, Fehler und Erfolg immer mit Symbol und Text. Feste Zuordnungen und Grössen regelt
  KONZEPT-MARKE §6 in EduKSX-UI.
- **GUI-Profile (DS12, Idee EduKSX-UI #23):** Nicht jede Oberfläche braucht dasselbe. Unterschieden wird nach Art des
  Moduls (intern für eine Organisation, öffentlich, reine Mobilnutzung) und nach Art der Ansicht (Webseite, Anwendung,
  Administration; in der Administration ist eine dichtere, komplexere Oberfläche erlaubt). Die Regeln je Profil stehen
  als Tabelle im Guideline-Text von EduKSX-UI; keine eigene Technik (kein Profil-Attribut, keine eigenen Tokens).
- Schweizer Schreibweise, Datum `DD.MM.YYYY`, Zeit `HH:MM:SS` (DB D2); keine Entscheidnummern in Anzeigetexten.

## 7. Prüfung (BESCHLOSSEN)

- Kontrasttest der Tokens und jedes Themes (CI und beim Aktivieren).
- **axe-core** auf den Hauptseiten jedes Moduls in der CI (z. B. über Playwright); Befunde «serious» und «critical»
  lassen die CI sofort scheitern, «moderate» und «minor» erscheinen als Warnung (DS7). In EduKSX-UI prüft axe-core
  jede Seite der Testseite (EduKSX-UI #14).
- Abnahmecheckliste des CI-Manuals (§ 13) in der PR-Vorlage jedes Moduls.

## 8. Entscheide

| Nr. | Frage | Entscheid | Status |
| --- | --- | --- | --- |
| DS1 | Quelle für Aussehen und Bedienung | CI für Aussehen, Intranet/`@eduksx/ui` für Bedienung; Barrierefreiheit vor | BESCHLOSSEN 22.11.2026 |
| DS2 | Token-Quelle | `tokens.json` (DTCG) mit Build | BESCHLOSSEN 22.11.2026 |
| DS3 | Ort von `@eduksx/ui` | eigenes Repo EduKSX-UI, MIT | BESCHLOSSEN 22.11.2026 |
| DS4 | Anpassung durch Organisationen | ganzes Theme, nur bekannte Tokens, aktivierbar erst nach bestandener Kontrastprüfung; Wortmarke unverändert | BESCHLOSSEN 22.11.2026 |
| DS5 | Intranet | EduKSX-Standard, SekBülach als Theme der Instanz | BESCHLOSSEN 22.11.2026 |
| DS6 | Farbe je Modul | keine; Unterscheidung über Icons | BESCHLOSSEN 22.11.2026 |
| DS7 | axe-core sofort als Fehler oder zuerst als Warnung; Musterseite (Storybook o. Ä.) | «serious»/«critical» sofort Fehler, Rest Warnung; Musterseite als eigene Testseite in EduKSX-UI (kein Storybook) | BESCHLOSSEN 22.11.2026 |
| DS8 | Farbschema-Umschalter in allen Modulen (Idee EduKSX-UI #17) | Pflicht, Hell / Dunkel / Wie System mit Symbolen, Baustein `ColorSchemeToggle` | BESCHLOSSEN 22.11.2026 |
| DS9 | Ansichten und Testumgebung (Idee EduKSX-UI #19) | Desktop-Ansichten Darstellungsoptimiert, Breit, Voll und Vollbild Pflicht; Pflicht-Ansichten zum Prüfen Handy/Tablet hoch und quer plus Desktop | BESCHLOSSEN 22.11.2026 |
| DS10 | Icon-Konzept (Idee EduKSX-UI #20) | Lucide für Bedienung, EduKSX-Set für Module, Regeln aus Glossary; Einzelheiten KONZEPT-MARKE §6 | BESCHLOSSEN 22.11.2026 |
| DS11 | Mitgelieferte Themes (Idee EduKSX-UI #18) | EduKSX plus Hoher Kontrast und Violett; weitere je Organisation, Auswahl durch die Person aus den vom Org-Admin freigegebenen | BESCHLOSSEN 22.11.2026 |
| DS12 | GUI-Profile nach Modul- und Ansichtsart (Idee EduKSX-UI #23) | Regeltabelle im Guideline-Text von EduKSX-UI, ohne eigene Technik | BESCHLOSSEN 22.11.2026 |
| DS13 | GUI-Tester (Idee EduKSX-UI #21) | Testseite von EduKSX-UI wird zum GUI-Tester ausgebaut: Erscheinungsbild, Themes in der Vorschau, je Baustein Beispiele, Versionen und Status, Überarbeitung, Wünsche (Regeln aus dem Intranet übernommen, nicht verlinkt) | BESCHLOSSEN 22.11.2026 |
| DS14 | Eigenes CSS für eingebettete Inhalte bei Dritten | Ausnahme zu DS4 nur für die Codex-Einbettung auf Gemeinde-Homepages; CSS geprüft, im Baustein gekapselt, Kontrastprüfung warnt; Verantwortung bei der Gemeinde ([Codex](KONZEPT-CODEX.md) CX4) | BESCHLOSSEN 26.11.2026 |

## 9. Verlauf

- 22.11.2026: Angelegt (#75); Entscheide DS1–DS6 im Chat.
- 22.11.2026: DS7 entschieden (Review EduKSX-UI PR #8); Ideen EduKSX-UI #17, #19, #20, #18, #23, #21 angenommen als DS8–DS13;
  Marke links oben nach KONZEPT-MARKE M3 (DS4-Abschnitt in §5).
- 26.11.2026: DS14 Ausnahme für die Codex-Einbettung (#119).
