# EduKSX-Architektur

Architektur, Schnittstellen und Betriebskonzept der EduKSX-Plattform (Ident, Module, Leitstand) für Projektverantwortliche und Entwickler der Module.

## Inhalt

| Bereich | Dokument |
| --- | --- |
| Plattform: Bausteine, Schnittstellen S1–S8, Prüfliste | [docs/KONZEPT-PLATTFORM.md](docs/KONZEPT-PLATTFORM.md) |
| DB- und API-Standard | [docs/KONZEPT-DB-GUIDELINE.md](docs/KONZEPT-DB-GUIDELINE.md), [docs/KONZEPT-API-GUIDELINE.md](docs/KONZEPT-API-GUIDELINE.md) |
| Gemeinsame Bibliothek `eduksx/core` | [docs/KONZEPT-CORE.md](docs/KONZEPT-CORE.md) |
| Ident mit Zitadel, Proof of Concept | [docs/KONZEPT-IDENT.md](docs/KONZEPT-IDENT.md) |
| Vorlage für neue Module, Datenschutz-Vorlagen | [docs/KONZEPT-MODULVORLAGE.md](docs/KONZEPT-MODULVORLAGE.md), [docs/vorlagen/](docs/vorlagen/DATENSCHUTZ-VERZEICHNIS.md) |
| Schnittstellen als Schemas | [spec/README.md](spec/README.md) |
| Prüfaufträge | [RLS](docs/PRUEFAUFTRAG-RLS.md), [DPoP/mTLS](docs/PRUEFAUFTRAG-DPOP-MTLS.md) |
| Modulschlüssel | [docs/REGISTER-MODULE.md](docs/REGISTER-MODULE.md) |

Prüfen: `python3 -m pip install -r requirements-pruefung.txt`, dann `python3 -m unittest discover -s tests`.

## Mitmachen

Fehler, Verbesserungen und Ideen bitte über die Issue-Formulare melden. Wie Meldungen freigegeben und umgesetzt
werden, steht in [CONTRIBUTING.md](CONTRIBUTING.md) und [docs/GITHUB-ABLAUF.md](docs/GITHUB-ABLAUF.md).
Sicherheitslücken bitte nicht öffentlich melden, sondern wie in [SECURITY.md](SECURITY.md) beschrieben.

## Versionen

Änderungen stehen im [CHANGELOG.md](CHANGELOG.md). Releases entstehen nach Freigabe automatisch (`version.py`,
Workflow `release.yml`).
