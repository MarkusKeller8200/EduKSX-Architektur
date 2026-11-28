# EduKSX-Architektur – Projektstand

> Stand 13.11.2026 (23:50): Release 0.3.0 «Konzept abgeschlossen» – Konzept eingefroren; Änderungen nur über
> `konzept-anpassung`. Offen nur, was die Umsetzung entscheidet (Meilenstein «Anpassungen aus der Umsetzung»).

## Umgesetzt

| Bereich | Stand | Seit Version | Konzept |
|---|---|---|---|
| Plattform: Bausteine, Schnittstellen S1–S8, Prüfliste, Infrastruktur | abgenommen, §9 vollständig entschieden | 0.1.0 | `docs/KONZEPT-PLATTFORM.md` |
| DB-Standard | 1.3 abgenommen (A8 deutsche Beschreibungen, #65) | 0.1.0 | `docs/KONZEPT-DB-GUIDELINE.md` |
| API-Standard | 1.2 abgenommen (A8 deutsche Beschreibungen, #65) | 0.1.0 | `docs/KONZEPT-API-GUIDELINE.md` |
| Modulregister (englische Schlüssel) | abgenommen | 0.1.0 | `docs/REGISTER-MODULE.md` |
| Identity-Provider Zitadel | entschieden, PoC läuft (#36): P2–P4, P6–P9 bestanden, P5 mit Edulog-Ersatz; offen Admin-MFA, echter Edulog-Anschluss, P10 | 0.1.0 | `docs/KONZEPT-PLATTFORM.md` 4.1, §9.1 |
| Konzept Core (`eduksx/core` 0.1) | abgenommen | 0.2.0 | `docs/KONZEPT-CORE.md` |
| Konzept Ident, PoC-Drehbuch | beschlossen bis auf PoC-Punkte (#36) | 0.2.0 | `docs/KONZEPT-IDENT.md` |
| Schemas S1, S4, S5, S6 | beschlossen, mit Tests | 0.2.0 | `spec/README.md` |
| Modulvorlage, Datenschutz-Vorlagen | beschlossen, Probe-Modul offen (#37) | 0.2.0 | `docs/KONZEPT-MODULVORLAGE.md` |
| Prüfaufträge RLS, DPoP/mTLS | Empfehlung, Entscheid nach Prototyp/PoC | 0.2.0 | `docs/PRUEFAUFTRAG-*.md` |
| Konzepte Leitstand, Selbst-Hosting, Plugins, Modulübersicht | beschlossen, eingefroren | 0.3.0 | `docs/KONZEPT-*.md`, `docs/MODULE-UEBERSICHT.md` |
| Qualitätsziele (#80) | beschlossen 25.11.2026, Messung im Betrieb offen | unveröffentlicht | `docs/KONZEPT-QUALITAET.md` |
| Protokollierung und Fehlersuche, API C7 (#76) | beschlossen 25.11.2026, Core-Bausteine offen (#83) | unveröffentlicht | `docs/KONZEPT-PROTOKOLLIERUNG.md` |
| Rollen und Rechte, Steckbrief `abilities` (#77) | beschlossen 25.11.2026, Core-Baustein und Glossary-Umstellung offen (#83) | unveröffentlicht | `docs/KONZEPT-ROLLEN.md` |
| Datenschutz Kanton Zürich, DB-Standard 1.5 (#78) | beschlossen 25.11.2026, Prüfung durch Fachperson offen (#22) | unveröffentlicht | `docs/KONZEPT-DATENSCHUTZ-ZH.md` |
| Technologie-Stack, Versionen, `ci:check`, Feature-Schalter (#79) | beschlossen 25.11.2026, Umstellung der Module bis 31.12.2026 offen (#83) | unveröffentlicht | `docs/KONZEPT-STACK.md` |
| Entwurf Datenmodell Kontakt-Kern (#124) | **ENTWURF**, nicht freigegeben; Widersprüche W1–W8 offen | unveröffentlicht | `docs/ENTWURF-DATENMODELL.md`, `docs/datenmodell/` |

## Umsetzung in den Modul-Repos (Stand 14.11.2026)

- EduKSX-Core 0.1.1 veröffentlicht; 0.2 (#13–#16) veröffentlicht als 0.2.0. `spec/` zusätzlich unter MIT (Core liefert die Schemas aus).
- EduKSX-Ident: Brücke 0.1 gemergt (#2–#6 im Beta-Test), unveröffentlicht.
- EduKSX-Glossary: Umstellung auf Core 0.1 als PR #335 bereit (#334).

## Offen bzw. geplant

- Meilenstein «Anpassungen aus der Umsetzung»: #36 PoC, #35 DPoP/mTLS, #34 RLS, #43 connect, #37 Probe-Modul,
  #51 Suite (Projektstart 14.11.2026 erledigt, Umsetzung in EduKSX-Suite #2–#8), #52 Plugin-Probe, #22 Datenschutz

## Technik

- Reines Doku-Repository: Konzepte in `docs/`, kein Anwendungscode (bleibt in den Modul-Repos).
- Schemas der Schnittstellen in `spec/v1/` (JSON Schema 2020-12, OpenAPI 3.1) mit Beispielen.
- Prüfen: `python3 -m pip install -r requirements-pruefung.txt`, dann `python3 -m unittest discover -s tests`
  (Verweise, keine Geheimnisse, Pflichtdokumente, Schemas und Beispiele).
