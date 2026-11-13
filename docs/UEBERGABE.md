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

**Konzept eingefroren (ab 0.3.0)** – Änderungen nur über Issue mit Label `konzept-anpassung` und Freigabe
(README). Weiterarbeit in den Modul-Repos (Core, Glossary, Intranet, Codex, Suite, Operation).

**Offene Issues** (Meilenstein «Anpassungen aus der Umsetzung», alle von der Umsetzung abhängig)

| Issue | Inhalt | wartet auf |
|---|---|---|
| #36 | PoC Zitadel (`_2 in Arbeit`, eigene Sitzung) | Durchführung; danach I1-Vorbehalt, I8, I9, I13, I14 |
| #35 | Entscheid DPoP/mTLS (API C1) | PoC P8 |
| #34 | Entscheid RLS (DB-E5) | Prototyp (Glossary PostgreSQL) |
| #43 | Konzept connect (UUID-Hoheit, IDA, licence) | Core so weit (Entscheid 13.11.2026) |
| #37 | Blueprint-Profil und Probe-Modul | my-github-blueprint |
| #51 | Repo EduKSX-Suite: Installer, Update-Dienst, VM-Vorlage | Repo anlegen |
| #52 | Probe Glossary-Plugin im Intranet | Glossary, Intranet |
| #22 | Datenschutz C9 gegenlesen | Fachperson |

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

### Sitzung 14.11.2026 (00:00) – Merge Ident, Prüfung der Umsetzung

- EdukSX-Ident PR #7 (Brücke 0.1) und PR #46 (Login V2 mit EduKSX-Gestaltung) gemergt; Ident #2–#6 im Beta-Test.
- Umsetzung gegen die Konzepte geprüft; redaktionell nachgeführt: Register, Modulübersicht, Issue-Tabellen Core/Ident.
- Nächste Schritte: Core 0.2 (#13–#16), Glossary #335 mergen, Ident 0.2 (S4-Zustellung, Prüfung gegen spec/), PoC #36 abschliessen.

### Sitzung 13.11.2026 (23:17–23:50) – Konzeptabschluss

- Konzepte Leitstand, Selbst-Hosting, Plugins; Icons freigegeben (markussxch #13); Operation #27 freigegeben.
- Alle nicht PoC-abhängigen Empfehlungen beschlossen; Meilenstein «Anpassungen aus der Umsetzung»; Release 0.3.0.

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

- Entscheid 13.11.2026 (23:45): **Konzept abgeschlossen und eingefroren** mit Release 0.3.0; Empfehlungen einzeln
  übernommen (L3–L6, SH-E9–SH-E12, P3–P8, I2–I4, I6, I7, I11); #29/#30 geschlossen (Operation zuständig).

- Entscheid 13.11.2026 (23:25): ops = Kunden und Kundeninstanzen (L1), Updates beim Kunden über eigenen Update-Dienst
  (L2); Selbst-Hosting SH-E1–SH-E8 (u. a. Repo EduKSX-Suite, SQLite je Modul, nur Korrekturen automatisch, tägliche
  Sicherung); Plugins als Manifest + Web-Komponenten, Stufe 1 eigene Module (P1, P2). PoC und connect warten auf Core.

- Entscheid 13.11.2026 (23:06): **MarKusSX-Operation ist die Quelle für den Betrieb** (Komodo, Caddy, 1Password,
  VictoriaLogs, Backrest/restic, Headscale, Cloudflare Access). Plattform §7.3a verweist nur noch darauf; die um 21:30
  beschlossenen Werkzeuge (SOPS/age, pgBackRest, Litestream, Prometheus/Grafana/Loki) sind aufgehoben. Widerspruch
  DB-Standard C2 (PITR, RPO 1 bzw. 15 Min.) ↔ Operation (täglicher Dump) als Prüfauftrag an Operation (MarKusSX-Operation #27).

- Entscheid 13.11.2026 (22:52): Zweck aller Module festgelegt (MODULE-UEBERSICHT.md); Einsatzplanung = `staffing`,
  Stundenplan bleibt `timetable`; Icon-Entwürfe für intranet, timetable, staffing, ops (markussxch PR #13, Freigabe offen).

- Entscheid 13.11.2026 (22:24): Selbst-Hosting ohne Ident – lokale Konten mit eigenem zweitem Faktor, optional
  Entra/Google per OIDC; kein Zitadel vor Ort, kein Edulog (auch nicht über das zentrale Ident, 22:27). Installation per Befehl und als VM-Vorlage (#40).

- Entscheid 13.11.2026 (21:30): Plattform §9.2–9.7 (siehe Konzept), Betrieb Stufe 1 mit Infomaniak (Werkzeuge
  am 13.11. 23:06 durch MarKusSX-Operation ersetzt, siehe unten); Core 0.2 ohne Ident, Ident-Teile in Core 0.3;
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
