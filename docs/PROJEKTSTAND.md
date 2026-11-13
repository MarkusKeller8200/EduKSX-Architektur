# EduKSX-Architektur – Projektstand

> Stand 13.11.2026 (21:30): Release 0.2.0; Plattform-Entscheide §9.2–9.7 und Werkzeuge Betrieb Stufe 1 getroffen.
> Core 0.1.0 veröffentlicht, Core 0.2 (ohne Ident) geplant. Als Nächstes PoC Zitadel (#36) und Core 0.2.

## Umgesetzt

| Bereich | Stand | Seit Version | Konzept |
|---|---|---|---|
| Plattform: Bausteine, Schnittstellen S1–S8, Prüfliste, Infrastruktur | abgenommen, §9 vollständig entschieden | 0.1.0 | `docs/KONZEPT-PLATTFORM.md` |
| DB-Standard | 1.2.1 abgenommen | 0.1.0 | `docs/KONZEPT-DB-GUIDELINE.md` |
| API-Standard | 1.1.1 abgenommen | 0.1.0 | `docs/KONZEPT-API-GUIDELINE.md` |
| Modulregister (englische Schlüssel) | abgenommen | 0.1.0 | `docs/REGISTER-MODULE.md` |
| Identity-Provider Zitadel | entschieden, PoC offen (#25) | 0.1.0 | `docs/KONZEPT-PLATTFORM.md` 4.1, §9.1 |
| Konzept Core (`eduksx/core` 0.1) | abgenommen | 0.2.0 | `docs/KONZEPT-CORE.md` |
| Konzept Ident, PoC-Drehbuch | Drehbuch abgenommen, PoC offen (#36) | 0.2.0 | `docs/KONZEPT-IDENT.md` |
| Schemas S1, S4, S5, S6 | beschlossen, mit Tests | 0.2.0 | `spec/README.md` |
| Modulvorlage, Datenschutz-Vorlagen | beschlossen, Probe-Modul offen (#37) | 0.2.0 | `docs/KONZEPT-MODULVORLAGE.md` |
| Prüfaufträge RLS, DPoP/mTLS | Empfehlung, Entscheid nach Prototyp/PoC | 0.2.0 | `docs/PRUEFAUFTRAG-*.md` |

## Offen bzw. geplant

- Meilenstein «0.3.0 – Betrieb Stufe 1»: #29 Hosting und Geheimnisse, #30 Sicherung und Überwachung, #22 Datenschutz C9,
  #36 PoC Zitadel durchführen, #35 Entscheid DPoP/mTLS, #34 Entscheid RLS, #37 Blueprint-Profil und Probe-Modul

## Technik

- Reines Doku-Repository: Konzepte in `docs/`, kein Anwendungscode (bleibt in den Modul-Repos).
- Schemas der Schnittstellen in `spec/v1/` (JSON Schema 2020-12, OpenAPI 3.1) mit Beispielen.
- Prüfen: `python3 -m pip install -r requirements-pruefung.txt`, dann `python3 -m unittest discover -s tests`
  (Verweise, keine Geheimnisse, Pflichtdokumente, Schemas und Beispiele).
