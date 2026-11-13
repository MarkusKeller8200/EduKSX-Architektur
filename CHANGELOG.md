# Changelog – EduKSX-Architektur

Format angelehnt an [Keep a Changelog](https://keepachangelog.com/de/), Versionen nach
[Semantic Versioning](https://semver.org/lang/de/) (MAJOR.MINOR.PATCH). Neue Einträge kommen laufend unter
**Unveröffentlicht**; `python3 .github/blueprint/release.py set X.Y.Z --commit` macht daraus eine Version.

## [Unveröffentlicht]

### Neu

- **Ident mit Zitadel:** Identity-Provider entschieden (Plattform 4.1, §9.1), vorbehaltlich Proof of Concept (#25); Plan B Keycloak.
- **Modulregister:** `docs/REGISTER-MODULE.md` als einzige Quelle der Modulschlüssel für DB- und API-Standard; interne Schlüssel englisch (`recht` → `codex`, `stundenplan` → `timetable`, `leitstand` → `ops`), Marketingnamen frei. DB-Standard 1.2.1, API-Standard 1.1.1 (redaktionell), Entscheide als `DB-E<n>` bzw. `API-E<n>`.
- **Core als Bibliothek:** Plattform 4.3 – `eduksx/core` ist kein Dienst; bringt Standardtabellen je Modul-Schema mit, Stammdaten in Ident (DB-E12).
- **API-Standard 1.1 (#18):** nach Architektur-Review – Stufen für schlanke Umsetzung, Modulschlüssel als Namensraum der Suite, gemeinsame Bausteine, korrigierte ETag-, Lösch- und Sync-Regeln, Datenschutz nach DSGVO/IDG, Sicherheitsnachweis mit ASVS, Scan und Pentest, Konformitätstest.
- **API-Standard (#15):** Regeln für die Schnittstellen aller Module (`docs/KONZEPT-API-GUIDELINE.md`) – Entwurf, Fehler, Pagination, Idempotenz, Sicherheit und Datenschutz, Versionierung, OpenAPI und Tests; abgeglichen mit gängigen Richtlinien und den Empfehlungen des Bundes, verlinkt aus der Prüfliste der Plattform.
- **DB-Standard (#9, #11, #20):** Regeln für Datenbank, Migrationen und Modelle aller Module (`docs/KONZEPT-DB-GUIDELINE.md`), verlinkt aus der Prüfliste der Plattform; Version 1.1 gegliedert in Grundregeln, Sicherheit und Datenschutz, Betrieb und Sprachen; Version 1.2 mit Teil «Modularität und Zusammenführbarkeit» und Datenschutzregeln nach IDG, DSG und DSGVO.
