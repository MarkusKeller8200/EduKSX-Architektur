# Changelog – EduKSX-Architektur

Format angelehnt an [Keep a Changelog](https://keepachangelog.com/de/), Versionen nach
[Semantic Versioning](https://semver.org/lang/de/) (MAJOR.MINOR.PATCH). Neue Einträge kommen laufend unter
**Unveröffentlicht**; `python3 .github/blueprint/release.py set X.Y.Z --commit` macht daraus eine Version.

## [Unveröffentlicht]

### Geändert

- **Lizenz `spec/`:** zusätzlich MIT (Doppellizenz `GPL-3.0-or-later OR MIT`, `spec/LICENSE`), damit `eduksx/core` (MIT) die Schemas ausliefern kann.

### Geändert

- **Redaktionell:** Repo EdukSX-Ident im Register und in der Modulübersicht; Issue-Tabellen in KONZEPT-CORE und KONZEPT-IDENT nachgeführt; Name des Konformitätstests in KONZEPT-CORE korrigiert (`AssertsConformance`).
- **Repo:** Python-Cache (`tests/__pycache__/`) nicht mehr eingecheckt, `.gitignore` ergänzt.
- **Modulregister:** `time` aktiv mit Repo EduKSX-Time (angelegt 16.11.2026); Modulübersicht angeglichen.

## [0.3.0] – 2026-11-13

### Neu

- **Konzept abgeschlossen und eingefroren:** Leitstand L3–L6, Selbst-Hosting SH-E9–SH-E12, Plugins P3–P8, Ident I2–I4, I6, I7, I11 beschlossen; Änderungen ab jetzt nur über Issues mit Label `konzept-anpassung` und Freigabe (README, CONTRIBUTING). Offene Punkte aus der Umsetzung im Meilenstein «Anpassungen aus der Umsetzung» (#22, #34–#37, #43, #51, #52); #29/#30 an MarKusSX-Operation übergeben.

### Neu

- **PoC Ident mit Zitadel, Durchgang 1 (#36):** Werkzeuge in `poc/ident-zitadel/`, Ergebnisse in KONZEPT-IDENT §4.3.

### Geändert

- **Plattform §9.2–9.7 entschieden:** Ident zentral mit Trennung auf Wunsch, Leitstand als eigene Anwendung, zuerst zentral, Kubernetes ab > 30 isolierten Instanzen, Unterdomain mit optionaler eigener Domain, Lizenz «Bibliotheken MIT, Module AGPL-3.0» (Glossary wechselt, Glossary #336).
- **Betrieb Stufe 1 (§7.3a, #29, #30):** Quelle ist das Repo MarKusSX-Operation (Komodo, Caddy, 1Password, VictoriaLogs, Backrest); Widerspruch zum DB-Standard C2 (PITR, RPO) als Prüfauftrag festgehalten.
- **Core-Fahrplan (KONZEPT-CORE 4.1a):** 0.2 ohne Ident (Steckbrief/`/health`, S4-Empfang, `data_changes`, Schemas), 0.3 nach dem PoC (OIDC, JWT, Standardtabellen); Issues EduKSX-Core #13–#16.
- **Modulregister:** `core` aktiv (0.1.0), `codex` aktiv (Repo EduKSX-Codex).
- **Konzepte Leitstand (#48), Selbst-Hosting (#40), Plugins (#44):** ops = Kunden und Kundeninstanzen, Technik bei MarKusSX-Operation; Suite-Paket in neuem Repo EduKSX-Suite (SQLite je Modul, Update-Dienst mit «nur Korrekturen automatisch», tägliche Sicherung, VM-Vorlage); Plugins als Manifest im Steckbrief plus Web-Komponenten. Schema: Abschnitt `ui` im Steckbrief, Instanz-Token in S6 (abwärtskompatibel).
- **Modulübersicht:** `docs/MODULE-UEBERSICHT.md` – Zweck, Kurzbeschreibung, Systemgrenzen und Icons aller Module, Gruppen, Integration über Plugins (Entwurf); Register mit `connect`, `licence`, `portal`, `shop`, `sign`, `time` und neu `staffing` (Einsatzplanung) als geplant.
- **Selbst-Hosting (#40):** Anmeldung ohne Ident – lokale Konten mit zweitem Faktor, optional Entra/Google per OIDC; Ausnahme in Plattform S1, Baustein im Core-Fahrplan.

## [0.2.0] – 2026-11-13

### Neu

- **Konzept Core abgenommen (#27):** `docs/KONZEPT-CORE.md` – Umfang `eduksx/core` 0.1, Herauslöse-Plan aus dem Glossary, Entscheide C1–C11 beschlossen (C11: Schemas aus `spec/`).
- **Schnittstellen als Schemas (#3):** `spec/v1/` – JSON Schemas für Claims (S1), Ereignisse und Signatur (S4), Steckbrief und `/health` (S5), OpenAPI 3.1 für Heartbeat und Aufträge (S6), je mit gültigen und ungültigen Beispielen; Versionierung in `spec/README.md`. Festlegungen SP1–SP8 beschlossen: Ereignisarten von Ident mit Modulschlüssel (`ident.user.deleted`), Feld `role` in `eduksx_orgs`, Signaturformat `t=…,v1=…`; Plattform S1/S4 angeglichen.
- **Konzept Ident (#25):** `docs/KONZEPT-IDENT.md` – Aufbau mit Zitadel und Ident-Brücke, Anbindung Edulog (SAML, Attribute, Rollen), Entscheide I1–I11, Drehbuch für den Proof of Concept mit Abbruchkriterien; als Drehbuch abgenommen, Durchführung in #36.
- **Konzept Modulvorlage (#28):** `docs/KONZEPT-MODULVORLAGE.md` – Ablauf «neues Modul anlegen», Inhalt eines neuen Moduls; Vorlagen für Verzeichnis der Bearbeitungen und Datenschutz-Folgenabschätzung unter `docs/vorlagen/`; M1–M5 beschlossen, Probe-Modul in #37.
- **Prüfaufträge (#13, #16):** `docs/PRUEFAUFTRAG-RLS.md` (Vorgehen und Prototyp für Row-Level Security) und `docs/PRUEFAUFTRAG-DPOP-MTLS.md` (Variantenvergleich, Empfehlung: kurze JWT mit `private_key_jwt`, DPoP vor mTLS); Entscheide bleiben ZU PRÜFEN.

### Geändert

- **Prüfungen:** Tests prüfen die Schemas unter `spec/` (neue Prüf-Abhängigkeit `jsonschema`, MIT, `requirements-pruefung.txt`, in `docs/third-party.json`); CI installiert sie und ruft `python` statt `python3` auf (Windows-Runner).

## [0.1.0] – 2026-11-13

### Neu

- **Plattform-Konzept abgenommen (#2, #4):** Bausteine, Schnittstellen S1–S8, Prüfliste für Module; offene Entscheide §9.2–9.7 bleiben offen.
- **Ident mit Zitadel:** Identity-Provider entschieden (Plattform 4.1, §9.1), vorbehaltlich Proof of Concept (#25); Plan B Keycloak.
- **Modulregister:** `docs/REGISTER-MODULE.md` als einzige Quelle der Modulschlüssel für DB- und API-Standard; interne Schlüssel englisch (`recht` → `codex`, `stundenplan` → `timetable`, `leitstand` → `ops`), Marketingnamen frei. DB-Standard 1.2.1, API-Standard 1.1.1 (redaktionell), Entscheide als `DB-E<n>` bzw. `API-E<n>`.
- **Core als Bibliothek:** Plattform 4.3 – `eduksx/core` ist kein Dienst; bringt Standardtabellen je Modul-Schema mit, Stammdaten in Ident (DB-E12).
- **API-Standard 1.1 (#18):** nach Architektur-Review – Stufen für schlanke Umsetzung, Modulschlüssel als Namensraum der Suite, gemeinsame Bausteine, korrigierte ETag-, Lösch- und Sync-Regeln, Datenschutz nach DSGVO/IDG, Sicherheitsnachweis mit ASVS, Scan und Pentest, Konformitätstest.
- **API-Standard (#15):** Regeln für die Schnittstellen aller Module (`docs/KONZEPT-API-GUIDELINE.md`) – Entwurf, Fehler, Pagination, Idempotenz, Sicherheit und Datenschutz, Versionierung, OpenAPI und Tests; abgeglichen mit gängigen Richtlinien und den Empfehlungen des Bundes, verlinkt aus der Prüfliste der Plattform.
- **DB-Standard (#9, #11, #20):** Regeln für Datenbank, Migrationen und Modelle aller Module (`docs/KONZEPT-DB-GUIDELINE.md`), verlinkt aus der Prüfliste der Plattform; Version 1.1 gegliedert in Grundregeln, Sicherheit und Datenschutz, Betrieb und Sprachen; Version 1.2 mit Teil «Modularität und Zusammenführbarkeit» und Datenschutzregeln nach IDG, DSG und DSGVO.
