# EduKSX-Architektur – Projektstand

> Stand 13.11.2026 (16:55): Release 0.1.0 «Grundgerüst» – Plattform-Konzept, DB-Standard 1.2.1, API-Standard 1.1.1 und
> Modulregister abgenommen; Identity-Provider Zitadel (vorbehaltlich PoC). Als Nächstes Meilenstein 0.2.0 «Core und
> Ident», beginnend mit dem Konzept Core 0.1 (#27).

## Umgesetzt

| Bereich | Stand | Seit Version | Konzept |
|---|---|---|---|
| Plattform: Bausteine, Schnittstellen S1–S8, Prüfliste, Infrastruktur | abgenommen | 0.1.0 | `docs/KONZEPT-PLATTFORM.md` |
| DB-Standard | 1.2.1 abgenommen | 0.1.0 | `docs/KONZEPT-DB-GUIDELINE.md` |
| API-Standard | 1.1.1 abgenommen | 0.1.0 | `docs/KONZEPT-API-GUIDELINE.md` |
| Modulregister (englische Schlüssel) | abgenommen | 0.1.0 | `docs/REGISTER-MODULE.md` |
| Identity-Provider Zitadel | entschieden, PoC offen (#25) | 0.1.0 | `docs/KONZEPT-PLATTFORM.md` 4.1, §9.1 |

## Offen bzw. geplant

- Meilenstein «0.2.0 – Core und Ident»: #27 Konzept Core 0.1, #25 PoC Zitadel, #3 Schnittstellen als Schemas,
  #28 Vorlage für neue Module (alle `triage`)
- Meilenstein «0.3.0 – Betrieb Stufe 1»: #29 Hosting und Geheimnisse, #30 Sicherung und Überwachung, #22 Datenschutz C9
- Sammlung Verbesserungen: #13 RLS, #16 DPoP/mTLS (Prüfaufträge)

## Technik

- Reines Doku-Repository: Konzepte in `docs/`, kein Anwendungscode (bleibt in den Modul-Repos).
- Prüfen: `python3 -m unittest discover -s tests` (Verweise, keine Geheimnisse).
