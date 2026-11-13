# Übergabe an einen neuen Chat – EduKSX-Architektur

Stand: **13.11.2026 (16:55)** – Release 0.1.0 «Grundgerüst»; laufender Meilenstein «0.2.0 – Core und Ident».
[PROJEKTSTAND.md](PROJEKTSTAND.md) (aktuell), [PROJEKTSTAND-ARCHIV.md](PROJEKTSTAND-ARCHIV.md) (Verlauf), Konzepte in
`docs/KONZEPT-*.md`. Bei jeder Übergabe nachführen.

## Start nächster Chat (Übergabe 13.11.2026, 16:55)

**Zuerst lesen:** CLAUDE.md → AGENTS.md → dieser Abschnitt → PROJEKTSTAND.md → passende KONZEPT-*.md.

**Stand Code und CI**
- Letztes Release **v0.1.0** (13.11.2026). Nächstes nur auf ausdrückliche Freigabe.
- Workflow `pages` schlägt seit 12.11.2026 fehl (vermutlich GitHub Pages nicht eingerichtet) – nicht untersucht.
- Prüfen: `python3 -m unittest discover -s tests`.

**Offene Issues und ihr Status**

| Issue | Meilenstein | Status | Inhalt |
|---|---|---|---|
| #27 | 0.2.0 – Core und Ident | `triage` | Konzept Core 0.1 (KONZEPT-CORE.md) |
| #25 | 0.2.0 – Core und Ident | `triage` | PoC Zitadel inkl. Edulog-Testzugang |
| #3 | 0.2.0 – Core und Ident | – | Schnittstellen als Schemas |
| #28 | 0.2.0 – Core und Ident | `triage` | Vorlage für neue Module |
| #29, #30, #22 | 0.3.0 – Betrieb Stufe 1 | `triage` | Hosting, Sicherung/Überwachung, Datenschutz C9 |
| #13, #16 | Verbesserungen | `triage` | Prüfaufträge RLS, DPoP/mTLS |

**Hinweise für die Arbeit**
- Modulschlüssel nur aus `docs/REGISTER-MODULE.md`; Entscheide heissen `DB-E<n>` bzw. `API-E<n>`.
- Glossary-Guideline zitiert noch «Plattform-Entscheid E4» (gemeint DB-E4) – im Glossary korrigieren.

**Arbeitsregeln** (siehe AGENTS.md)
- Jedes Thema aus dem Chat → Issue mit Testliste; Status `_1 bereit` → `_2 in Arbeit` → `_3 Beta-Test`.
- Releases nur nach ausdrücklicher Freigabe; Löschen nur nach Rückfrage.

## Sitzungen

### Sitzung 13.11.2026 (15:05–16:55) – Register, Core, Ident, Meilensteine

- Modulregister mit englischen Schlüsseln (`codex`, `timetable`, `ops`), Entscheid-Nummern `DB-E`/`API-E` (#23, PR #24).
- Zitadel als Identity-Provider vorbehaltlich PoC (#25, PR #26).
- Meilensteine 0.2.0 und 0.3.0 angelegt, #27–#30 erfasst; 0.1.0 abgenommen und released.

## Entscheide

- Entscheid 13.11.2026: Interne Bezeichnungen englisch, Marketingnamen situativ (REGISTER-MODULE.md).
- Entscheid 13.11.2026: `eduksx/core` ist eine Bibliothek, kein Dienst; Standardtabellen je Modul-Schema, Stammdaten in Ident (DB-E12).
- Entscheid 13.11.2026: Identity-Provider Zitadel, vorbehaltlich PoC; Plan B Keycloak.
- Entscheid 13.11.2026: Core in eigenem Repo EduKSX-Core, Lizenz MIT, Core 0.1 nur PHP 8.4 / Laravel 13.
