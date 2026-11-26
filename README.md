# EduKSX-Architektur

Architektur, Schnittstellen und Betriebskonzept der EduKSX-Plattform (Ident, Module, Leitstand) für Projektverantwortliche und Entwickler der Module.

## Inhalt

| Bereich | Dokument |
| --- | --- |
| Plattform: Bausteine, Schnittstellen S1–S8, Prüfliste | [docs/KONZEPT-PLATTFORM.md](docs/KONZEPT-PLATTFORM.md) |
| Technologie-Stack, Versionen, Prüfbefehl, Feature-Schalter | [docs/KONZEPT-STACK.md](docs/KONZEPT-STACK.md) |
| Codex: Öffentlichkeit, Anmeldung, Einbindung bei Gemeinden, CSS, Mustersystematik | [docs/KONZEPT-CODEX.md](docs/KONZEPT-CODEX.md) |
| Qualitätsziele: Antwortzeiten, Verfügbarkeit, Wartbarkeit | [docs/KONZEPT-QUALITAET.md](docs/KONZEPT-QUALITAET.md) |
| Protokollierung und Fehlersuche: Arten, Fristen, Debug, Maskierung, Support | [docs/KONZEPT-PROTOKOLLIERUNG.md](docs/KONZEPT-PROTOKOLLIERUNG.md) |
| Rollen und Rechte: Standardrollen, Namensschema, Datenebene, Minderjährige | [docs/KONZEPT-ROLLEN.md](docs/KONZEPT-ROLLEN.md) |
| Datenschutz Kanton Zürich: Klassifizierung, Auftragsbearbeitung, Anbieter, Archiv | [docs/KONZEPT-DATENSCHUTZ-ZH.md](docs/KONZEPT-DATENSCHUTZ-ZH.md), [Vorlage](docs/vorlagen/AUFTRAGSBEARBEITUNG-ZH.md) |
| DB- und API-Standard | [docs/KONZEPT-DB-GUIDELINE.md](docs/KONZEPT-DB-GUIDELINE.md), [docs/KONZEPT-API-GUIDELINE.md](docs/KONZEPT-API-GUIDELINE.md) |
| Gemeinsame Bibliothek `eduksx/core` | [docs/KONZEPT-CORE.md](docs/KONZEPT-CORE.md) |
| Ident mit Zitadel, Proof of Concept | [docs/KONZEPT-IDENT.md](docs/KONZEPT-IDENT.md) |
| Vorlage für neue Module, Datenschutz-Vorlagen | [docs/KONZEPT-MODULVORLAGE.md](docs/KONZEPT-MODULVORLAGE.md), [docs/vorlagen/](docs/vorlagen/DATENSCHUTZ-VERZEICHNIS.md) |
| Leitstand, Selbst-Hosting, Plugins | [docs/KONZEPT-LEITSTAND.md](docs/KONZEPT-LEITSTAND.md), [docs/KONZEPT-SELBSTHOSTING.md](docs/KONZEPT-SELBSTHOSTING.md), [docs/KONZEPT-PLUGINS.md](docs/KONZEPT-PLUGINS.md) |
| Module, Systemgrenzen, Icons | [docs/MODULE-UEBERSICHT.md](docs/MODULE-UEBERSICHT.md) |
| Schnittstellen als Schemas | [spec/README.md](spec/README.md) |
| Prüfaufträge | [RLS](docs/PRUEFAUFTRAG-RLS.md), [DPoP/mTLS](docs/PRUEFAUFTRAG-DPOP-MTLS.md) |
| Modulschlüssel | [docs/REGISTER-MODULE.md](docs/REGISTER-MODULE.md) |

Prüfen: `python3 -m pip install -r requirements-pruefung.txt`, dann `python3 -m unittest discover -s tests`.

## Konzept eingefroren (ab 0.3.0)

Seit Release 0.3.0 «Konzept abgeschlossen» (13.11.2026) gilt das Konzept als **eingefroren**. Die Module arbeiten
danach. Geändert wird es nur noch,

1. wenn die **Umsetzung ein Problem zeigt** (PoC, Prototyp, Modul) – als Issue mit Label **`konzept-anpassung`**,
   Begründung aus der Umsetzung und betroffenem Abschnitt, und
2. nach **ausdrücklicher Freigabe** durch Projektverantwortliche:r (`_1 bereit`).

Offene Punkte, die erst die Umsetzung entscheidet (Ident-PoC, RLS, DPoP/mTLS, `connect`, Proben), stehen im
Meilenstein «Anpassungen aus der Umsetzung»; ihre Ergebnisse fliessen auf demselben Weg ein. Redaktionelle
Korrekturen (Tippfehler, Verweise) brauchen kein eigenes Issue.

**Erweiterungsrunde 0.4.0 (beschlossen 22.11.2026, #70):** Neue Themen, die im Konzept fehlen, sind keine Anpassung,
sondern eine **Erweiterung** – Label **`konzept-erweiterung`**, Meilenstein «0.4.0 – Konzept erweitert»:

- Erlaubt sind nur **neue** Abschnitte oder Dokumente und **Präzisierungen** als neue Unterversion eines Standards
  (z. B. DB-Standard 1.4). Beschlossenes wird nicht geändert; ein Widerspruch wird als eigener Entscheid vorgelegt.
- Jedes Issue braucht die Freigabe durch Projektverantwortliche:r; jedes Thema kommt als Konzept-PR.
- **Nicht rückwirkend:** Ein Modul übernimmt neue Regeln mit einem Issue im Modul ab seinem nächsten MINOR-Release
  (DB E5, API D8).
- Mit Release 0.4.0 endet die Runde; danach gilt der Freeze wieder wie oben. Grundlage:
  [Lückenanalyse](docs/LUECKENANALYSE-0.4.0.md).

## Mitmachen

Fehler, Verbesserungen und Ideen bitte über die Issue-Formulare melden. Wie Meldungen freigegeben und umgesetzt
werden, steht in [CONTRIBUTING.md](CONTRIBUTING.md) und [docs/GITHUB-ABLAUF.md](docs/GITHUB-ABLAUF.md).
Sicherheitslücken bitte nicht öffentlich melden, sondern wie in [SECURITY.md](SECURITY.md) beschrieben.

## Versionen

Änderungen stehen im [CHANGELOG.md](CHANGELOG.md). Releases entstehen nach Freigabe automatisch (`version.py`,
Workflow `release.yml`).
