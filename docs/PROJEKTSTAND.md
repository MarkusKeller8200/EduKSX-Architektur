# EduKSX-Architektur – Projektstand

> Stand 13.11.2026 (20:45): Meilenstein 0.2.0 «Core und Ident» – Konzepte fertig: Core abgenommen (#27), Konzept Ident
> mit PoC-Drehbuch (#25), Schemas S1/S4/S5/S6 unter `spec/` (#3), Modulvorlage mit Datenschutz-Vorlagen (#28);
> Prüfaufträge RLS (#13) und DPoP/mTLS (#16) mit Empfehlung. Offen: Abnahme (Beta-Test) und Durchführung des PoC.

## Umgesetzt

| Bereich | Stand | Seit Version | Konzept |
|---|---|---|---|
| Plattform: Bausteine, Schnittstellen S1–S8, Prüfliste, Infrastruktur | abgenommen | 0.1.0 | `docs/KONZEPT-PLATTFORM.md` |
| DB-Standard | 1.2.1 abgenommen | 0.1.0 | `docs/KONZEPT-DB-GUIDELINE.md` |
| API-Standard | 1.1.1 abgenommen | 0.1.0 | `docs/KONZEPT-API-GUIDELINE.md` |
| Modulregister (englische Schlüssel) | abgenommen | 0.1.0 | `docs/REGISTER-MODULE.md` |
| Identity-Provider Zitadel | entschieden, PoC offen (#25) | 0.1.0 | `docs/KONZEPT-PLATTFORM.md` 4.1, §9.1 |
| Konzept Core (`eduksx/core` 0.1) | abgenommen | unveröffentlicht | `docs/KONZEPT-CORE.md` |
| Konzept Ident, PoC-Drehbuch | Entwurf, PoC offen | unveröffentlicht | `docs/KONZEPT-IDENT.md` |
| Schemas S1, S4, S5, S6 | Entwurf mit Tests | unveröffentlicht | `spec/README.md` |
| Modulvorlage, Datenschutz-Vorlagen | Entwurf | unveröffentlicht | `docs/KONZEPT-MODULVORLAGE.md` |
| Prüfaufträge RLS, DPoP/mTLS | Empfehlung, Entscheid nach Prototyp/PoC | unveröffentlicht | `docs/PRUEFAUFTRAG-*.md` |

## Offen bzw. geplant

- Meilenstein «0.2.0 – Core und Ident»: #27 im Beta-Test; #25, #3, #28 Konzepte im Beta-Test – Durchführung des PoC
  (#25) und Abnahme der Schemas (#3) stehen aus
- Meilenstein «0.3.0 – Betrieb Stufe 1»: #29 Hosting und Geheimnisse, #30 Sicherung und Überwachung, #22 Datenschutz C9
- Ebenfalls in 0.2.0 (seit 13.11.2026): #13 RLS (Prototyp offen), #16 DPoP/mTLS (Entscheid nach PoC P8)

## Technik

- Reines Doku-Repository: Konzepte in `docs/`, kein Anwendungscode (bleibt in den Modul-Repos).
- Schemas der Schnittstellen in `spec/v1/` (JSON Schema 2020-12, OpenAPI 3.1) mit Beispielen.
- Prüfen: `python3 -m pip install -r requirements-pruefung.txt`, dann `python3 -m unittest discover -s tests`
  (Verweise, keine Geheimnisse, Pflichtdokumente, Schemas und Beispiele).
