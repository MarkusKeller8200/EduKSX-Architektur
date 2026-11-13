# Übergabe an einen neuen Chat – EduKSX-Architektur

Stand: **13.11.2026 (20:45)** – Release 0.1.0 «Grundgerüst»; laufender Meilenstein «0.2.0 – Core und Ident», Konzepte fertig.
[PROJEKTSTAND.md](PROJEKTSTAND.md) (aktuell), [PROJEKTSTAND-ARCHIV.md](PROJEKTSTAND-ARCHIV.md) (Verlauf), Konzepte in
`docs/KONZEPT-*.md`. Bei jeder Übergabe nachführen.

## Start nächster Chat (Übergabe 13.11.2026, 20:45)

**Zuerst lesen:** CLAUDE.md → AGENTS.md → dieser Abschnitt → PROJEKTSTAND.md → passende KONZEPT-*.md.

**Stand Code und CI**
- Letztes Release **v0.1.0** (13.11.2026). Nächstes nur auf ausdrückliche Freigabe.
- Branch `konzepte-0.2.0` mit Pull Request für alle Konzepte aus dieser Sitzung; CI-Lauf dort prüfen. Zum ersten Mal
  laufen die Tests wirklich auf Windows/macOS/Linux (bisher nur Doku-Änderungen) – `python` statt `python3`,
  Abhängigkeit `jsonschema` über `requirements-pruefung.txt`.
- Workflow `pages` schlägt seit 12.11.2026 fehl (vermutlich GitHub Pages nicht eingerichtet) – nicht untersucht.
- Prüfen: `python3 -m pip install -r requirements-pruefung.txt`, dann `python3 -m unittest discover -s tests`.

**Offene Issues und ihr Status**

| Issue | Meilenstein | Status | Inhalt |
|---|---|---|---|
| #27 | 0.2.0 – Core und Ident | `_3 Beta-Test` | Konzept Core abgenommen (C5–C10 beschlossen) – schliessen nach Test |
| #25 | 0.2.0 – Core und Ident | `_3 Beta-Test` | KONZEPT-IDENT.md als Drehbuch abgenommen |
| #3 | 0.2.0 – Core und Ident | `_3 Beta-Test` | Schemas unter `spec/v1/` mit Tests; SP1–SP8 beschlossen |
| #28 | 0.2.0 – Core und Ident | `_3 Beta-Test` | KONZEPT-MODULVORLAGE.md (M1–M5 beschlossen), Datenschutz-Vorlagen |
| #29, #30, #22 | 0.3.0 – Betrieb Stufe 1 | `triage` | Hosting, Sicherung/Überwachung, Datenschutz C9 |
| #13, #16 | 0.2.0 – Core und Ident | `_3 Beta-Test` | Prüfaufträge RLS, DPoP/mTLS – abgenommen wird die Empfehlung |
| #34, #35 | 0.3.0 – Betrieb Stufe 1 | `triage` | Entscheid RLS nach Prototyp (DB-E5), Entscheid DPoP/mTLS nach PoC P8 (API C1) |
| #36, #37 | 0.3.0 – Betrieb Stufe 1 | `triage` | PoC Zitadel durchführen (Edulog-Testzugang anfragen), Blueprint-Profil und Probe-Modul |

**Hinweise für die Arbeit**
- Modulschlüssel nur aus `docs/REGISTER-MODULE.md`; Entscheide heissen `DB-E<n>` bzw. `API-E<n>`, in Konzepten
  `C<n>` (Core), `I<n>` (Ident), `M<n>` (Modulvorlage), `SP<n>` (Schemas).
- Noch EMPFOHLEN bzw. ZU PRÜFEN: Ident I2–I11 (Entscheid mit #36). Beschlossen 13.11.2026: Core C1–C11, Schemas
  SP1–SP8, Modulvorlage M1–M5.
- 0.2.0 enthält nur noch Konzepte (#3, #13, #16, #25, #27, #28, alle `_3 Beta-Test`); sind sie abgenommen und PR #33
  gemergt, kann das Release 0.2.0 vorgeschlagen werden.
- Glossary-Guideline zitiert noch «Plattform-Entscheid E4» (gemeint DB-E4) – im Glossary korrigieren.

**Arbeitsregeln** (siehe AGENTS.md)
- Jedes Thema aus dem Chat → Issue mit Testliste; Status `_1 bereit` → `_2 in Arbeit` → `_3 Beta-Test`.
- Releases nur nach ausdrücklicher Freigabe; Löschen nur nach Rückfrage.

## Sitzungen

### Sitzung 13.11.2026 (20:25–20:45) – Konzepte Meilenstein 0.2.0 und Verbesserungen

- Auftrag im Chat: «Konzepte fertig stellen, Meilenstein 0.2.0 und Verbesserungen» (gilt als Freigabe für #3, #13,
  #16, #25, #28).
- Core C5–C10 beschlossen, Konzept abgenommen (#27); Schemas `spec/v1/` mit Tests (#3); KONZEPT-IDENT.md mit
  PoC-Drehbuch nach Recherche Zitadel/Edulog/Keycloak (#25); Modulvorlage und Datenschutz-Vorlagen (#28);
  Prüfaufträge RLS (#13) und DPoP/mTLS (#16) mit Empfehlung.
- #13 und #16 auf Wunsch in den Meilenstein 0.2.0 verschoben (vorher Sammlung «Verbesserungen»); abgenommen wird dort
  die Empfehlung, die Entscheide nach Prototyp bzw. PoC sind als #34 und #35 in 0.3.0 abgespalten.
- Abnahme-Runde im Chat: SP1–SP8, C11, M1–M5 beschlossen; I2–I11 bleiben empfohlen; Durchführung PoC (#36) und
  Probe-Modul (#37) nach 0.3.0 abgespalten.

### Sitzung 13.11.2026 (15:05–16:55) – Register, Core, Ident, Meilensteine

- Modulregister mit englischen Schlüsseln (`codex`, `timetable`, `ops`), Entscheid-Nummern `DB-E`/`API-E` (#23, PR #24).
- Zitadel als Identity-Provider vorbehaltlich PoC (#25, PR #26).
- Meilensteine 0.2.0 und 0.3.0 angelegt, #27–#30 erfasst; 0.1.0 abgenommen und released.

## Entscheide

- Entscheid 13.11.2026: Core C5–C10 übernommen (Packagist, `EduKSX\Core`, Standardtabellen mit Ident in Core 0.2,
  Übernahme-Migration, Standards in `composer.json`, UI-Paket später).
- Entscheid 13.11.2026: Prüf-Abhängigkeit `jsonschema` (MIT) für die Schema-Tests.
- Entscheid 13.11.2026: Schemas SP1–SP8 (u. a. Ereignisse `ident.*`, Feld `role`, Signatur `t=…,v1=…`), Core C11 und
  Modulvorlage M1–M5 beschlossen.

- Entscheid 13.11.2026: Interne Bezeichnungen englisch, Marketingnamen situativ (REGISTER-MODULE.md).
- Entscheid 13.11.2026: `eduksx/core` ist eine Bibliothek, kein Dienst; Standardtabellen je Modul-Schema, Stammdaten in Ident (DB-E12).
- Entscheid 13.11.2026: Identity-Provider Zitadel, vorbehaltlich PoC; Plan B Keycloak.
- Entscheid 13.11.2026: Core in eigenem Repo EduKSX-Core, Lizenz MIT, Core 0.1 nur PHP 8.4 / Laravel 13.
