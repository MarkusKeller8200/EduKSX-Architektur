# <img src="docs/assets/icons/eduksx-architektur-color.svg" width="32" alt=""> EduKSX-Architektur

Architektur, Schnittstellen und Betriebskonzept der EduKSX-Plattform (Ident, Module, Leitstand) für Projektverantwortliche und Entwickler der Module.

## Inhalt

| Bereich | Dokument |
| --- | --- |
| Plattform: Bausteine, Schnittstellen S1–S8, Prüfliste | [docs/KONZEPT-PLATTFORM.md](docs/KONZEPT-PLATTFORM.md) |
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

## Mitmachen

Fehler, Verbesserungen und Ideen bitte über die Issue-Formulare melden. Wie Meldungen freigegeben und umgesetzt
werden, steht in [CONTRIBUTING.md](CONTRIBUTING.md) und [docs/GITHUB-ABLAUF.md](docs/GITHUB-ABLAUF.md).
Sicherheitslücken bitte nicht öffentlich melden, sondern wie in [SECURITY.md](SECURITY.md) beschrieben.

## Versionen

Änderungen stehen im [CHANGELOG.md](CHANGELOG.md). Releases entstehen nach Freigabe automatisch (`version.py`,
Workflow `release.yml`).
