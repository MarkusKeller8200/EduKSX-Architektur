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
- **GUI-Prototypen** bleiben die Musterseite; sie wandern mit den Bausteinen in EduKSX-UI (Storybook o. Ä., ZU PRÜFEN).

## 5. Themes (BESCHLOSSEN)

| Theme | Wer | Regel |
| --- | --- | --- |
| **EduKSX (Standard)** | alle | aus `tokens.json`, nicht änderbar ausser im Code |
| **Hoher Kontrast** | alle | Vorlage, wählbar |
| **Theme der Organisation** | Admin der Organisation | ganzes Theme (alle bekannten Tokens, hell und dunkel); gespeichert werden nur Abweichungen |

- Nur **bekannte Tokens** und nur `#rrggbb` werden gespeichert und ausgegeben (Technik Intranet `Themes::GROUPS`).
- Ein Theme der Organisation lässt sich erst **aktivieren, wenn die Kontrastprüfung bestanden ist** (strenger als heute im
  Intranet, wo sie nur warnt).
- Es gilt im **Kontext der Organisation** (isolierte Instanz; in zentralen Modulen bei angemeldeten Personen der
  Organisation bzw. in ihrer Organisations-Darstellung). Öffentliche Seiten zentraler Module ohne Organisationskontext
  bleiben im Standard.
- **Unverändert bleiben:** EduKSX-Wortmarke und Signets (Farben nach CI), Fokus-Sichtbarkeit, Statusbedeutung
  (Erfolg, Warnung, Fehler immer mit Symbol und Text). Ein Logo der Organisation kommt **zusätzlich** in die Kopfzeile.
- Hell, dunkel oder System wählt die Person.

**Intranet (BESCHLOSSEN):** Das Intranet stellt auf `@eduksx/ui` und den Standard «EduKSX» um; das heutige Aussehen
(Farben der Sekundarschule Bülach, Open Sans) bleibt als **Theme der Instanz** erhalten. Umsetzung als Issue im
Intranet (#83), nicht rückwirkend.

## 6. Seiten und Texte (BESCHLOSSEN, aus dem Glossary)

- Breiten: darstellungsoptimiert 1152 px, breit 1536 px, voll; Fliesstext auf Lesebreite (`max-w-prose`) (Glossary
  DEC-023).
- Kopfzeile auf Website und Administration gleich: Wortmarke, Modulwechsel, Suche, Ansicht, Farbschema, Person.
- Schweizer Schreibweise, Datum `DD.MM.YYYY`, Zeit `HH:MM:SS` (DB D2); keine Entscheidnummern in Anzeigetexten.

## 7. Prüfung (BESCHLOSSEN)

- Kontrasttest der Tokens und jedes Themes (CI und beim Aktivieren).
- **axe-core** auf den Hauptseiten jedes Moduls in der CI (z. B. über Playwright); Befunde «serious» und «critical»
  lassen die CI scheitern (ZU PRÜFEN: zuerst als Warnung).
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
| DS7 | axe-core sofort als Fehler oder zuerst als Warnung; Musterseite (Storybook o. Ä.) | – | ZU PRÜFEN |

## 9. Verlauf

- 22.11.2026: Angelegt (#75); Entscheide DS1–DS6 im Chat.
