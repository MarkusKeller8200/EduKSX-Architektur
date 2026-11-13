# Übergabe an einen neuen Chat – EduKSX-Architektur

Stand: **13.11.2026 (21:30)** – Release 0.2.0; Plattform §9 vollständig entschieden; nächster Meilenstein «0.3.0 – Betrieb Stufe 1».
[PROJEKTSTAND.md](PROJEKTSTAND.md) (aktuell), [PROJEKTSTAND-ARCHIV.md](PROJEKTSTAND-ARCHIV.md) (Verlauf), Konzepte in
`docs/KONZEPT-*.md`. Bei jeder Übergabe nachführen.

## Start nächster Chat (Übergabe 13.11.2026, 20:45)

**Zuerst lesen:** CLAUDE.md → AGENTS.md → dieser Abschnitt → PROJEKTSTAND.md → passende KONZEPT-*.md.

**Stand Code und CI**
- Letztes Release **v0.2.0** (13.11.2026) mit allen Konzepten aus Meilenstein 0.2.0 (PR #33). Nächstes nur auf
  ausdrückliche Freigabe.
- Tests laufen auf Windows/macOS/Linux (`python -m unittest`, Abhängigkeit `jsonschema` über `requirements-pruefung.txt`).
- Workflow `pages` schlägt seit 12.11.2026 fehl (vermutlich GitHub Pages nicht eingerichtet) – nicht untersucht.
- Branch `konzepte-0.2.0` ist gemergt; Löschen nur nach Rückfrage.
- Prüfen: `python3 -m pip install -r requirements-pruefung.txt`, dann `python3 -m unittest discover -s tests`.

**Offene Issues und ihr Status** (Meilenstein «0.3.0 – Betrieb Stufe 1», alle `triage`)

| Issue | Inhalt |
|---|---|
| #29, #30 | Hosting und Geheimnisse, Sicherung und Überwachung – Werkzeuge entschieden (Plattform §7.3a), Umsetzung offen |
| #22 | Datenschutz C9 rechtlich gegenlesen (Fachperson) |
| #40 | Konzept Selbst-Hosting: Suite-Paket, Installer + VM-Vorlage, Anmeldung ohne Ident, Mindestanforderungen |
| #36 | PoC Zitadel durchführen – **auf dem Rechner von Projektverantwortliche:r** (Docker Desktop, Steuerung über die Verbindung zum Rechner); Edulog-Testzugang anfragen |
| #35 | Entscheid DPoP/mTLS nach PoC P8 (API C1) |
| #34 | Entscheid RLS nach Prototyp (DB-E5) |
| #37 | Blueprint-Profil `eduksx-modul` und Probe-Modul |

**Hinweise für die Arbeit**
- Modulschlüssel nur aus `docs/REGISTER-MODULE.md`; Entscheide heissen `DB-E<n>` bzw. `API-E<n>`, in Konzepten
  `C<n>` (Core), `I<n>` (Ident), `M<n>` (Modulvorlage), `SP<n>` (Schemas).
- Noch EMPFOHLEN bzw. ZU PRÜFEN: Ident I2–I11 (Entscheid mit #36). Beschlossen 13.11.2026: Core C1–C11, Schemas
  SP1–SP8, Modulvorlage M1–M5.
- Core: 0.1.0 veröffentlicht; Meilenstein «0.2.0 – Plattform-Schnittstellen» mit EduKSX-Core #13–#16 (`triage`), Fahrplan
  in KONZEPT-CORE 4.1a. Ident-Teile erst in Core 0.3 nach #36.
- Glossary #336: Lizenzwechsel MIT → AGPL-3.0 (`triage`).
- Glossary-Guideline zitiert noch «Plattform-Entscheid E4» (gemeint DB-E4) – im Glossary korrigieren.

**Arbeitsregeln** (siehe AGENTS.md)
- Jedes Thema aus dem Chat → Issue mit Testliste; Status `_1 bereit` → `_2 in Arbeit` → `_3 Beta-Test`.
- Releases nur nach ausdrücklicher Freigabe; Löschen nur nach Rückfrage.

## Sitzungen

### Sitzung 13.11.2026 (21:08–21:30) – Offene Entscheide

- Plattform §9.2–9.7, Betrieb Stufe 1 (§7.3a) und Core-Fahrplan entschieden; Register nachgeführt (core, codex aktiv).
- Core-Issues #13–#16 (Meilenstein 0.2.0) und Glossary #336 (Lizenz) angelegt.

### Sitzung 13.11.2026 (20:25–21:00) – Konzepte Meilenstein 0.2.0 und Verbesserungen

- Auftrag im Chat: «Konzepte fertig stellen, Meilenstein 0.2.0 und Verbesserungen» (gilt als Freigabe für #3, #13,
  #16, #25, #28).
- Core C5–C10 beschlossen, Konzept abgenommen (#27); Schemas `spec/v1/` mit Tests (#3); KONZEPT-IDENT.md mit
  PoC-Drehbuch nach Recherche Zitadel/Edulog/Keycloak (#25); Modulvorlage und Datenschutz-Vorlagen (#28);
  Prüfaufträge RLS (#13) und DPoP/mTLS (#16) mit Empfehlung.
- #13 und #16 auf Wunsch in den Meilenstein 0.2.0 verschoben (vorher Sammlung «Verbesserungen»); abgenommen wird dort
  die Empfehlung, die Entscheide nach Prototyp bzw. PoC sind als #34 und #35 in 0.3.0 abgespalten.
- Abnahme-Runde im Chat: SP1–SP8, C11, M1–M5 beschlossen; I2–I11 bleiben empfohlen; Durchführung PoC (#36) und
  Probe-Modul (#37) nach 0.3.0 abgespalten.
- Testlisten abgehakt, PR #33 gemergt, Issues #3, #13, #16, #25, #27, #28 geschlossen, Release 0.2.0 freigegeben.

### Sitzung 13.11.2026 (15:05–16:55) – Register, Core, Ident, Meilensteine

- Modulregister mit englischen Schlüsseln (`codex`, `timetable`, `ops`), Entscheid-Nummern `DB-E`/`API-E` (#23, PR #24).
- Zitadel als Identity-Provider vorbehaltlich PoC (#25, PR #26).
- Meilensteine 0.2.0 und 0.3.0 angelegt, #27–#30 erfasst; 0.1.0 abgenommen und released.

## Entscheide

- Entscheid 13.11.2026 (22:24): Selbst-Hosting ohne Ident – lokale Konten mit eigenem zweitem Faktor, optional
  Entra/Google per OIDC; kein Zitadel vor Ort, kein Edulog. Installation per Befehl und als VM-Vorlage (#40).

- Entscheid 13.11.2026 (21:30): Plattform §9.2–9.7 (siehe Konzept), Betrieb Stufe 1 mit Infomaniak, SOPS/age,
  pgBackRest, Litestream, Prometheus/Grafana/Loki, Uptime Kuma; Core 0.2 ohne Ident, Ident-Teile in Core 0.3;
  PoC #36 auf dem Rechner von Projektverantwortliche:r; Module AGPL-3.0, Glossary wechselt.

- Entscheid 13.11.2026: Core C5–C10 übernommen (Packagist, `EduKSX\Core`, Standardtabellen mit Ident in Core 0.2,
  Übernahme-Migration, Standards in `composer.json`, UI-Paket später).
- Entscheid 13.11.2026: Prüf-Abhängigkeit `jsonschema` (MIT) für die Schema-Tests.
- Entscheid 13.11.2026: Schemas SP1–SP8 (u. a. Ereignisse `ident.*`, Feld `role`, Signatur `t=…,v1=…`), Core C11 und
  Modulvorlage M1–M5 beschlossen.

- Entscheid 13.11.2026: Interne Bezeichnungen englisch, Marketingnamen situativ (REGISTER-MODULE.md).
- Entscheid 13.11.2026: `eduksx/core` ist eine Bibliothek, kein Dienst; Standardtabellen je Modul-Schema, Stammdaten in Ident (DB-E12).
- Entscheid 13.11.2026: Identity-Provider Zitadel, vorbehaltlich PoC; Plan B Keycloak.
- Entscheid 13.11.2026: Core in eigenem Repo EduKSX-Core, Lizenz MIT, Core 0.1 nur PHP 8.4 / Laravel 13.
