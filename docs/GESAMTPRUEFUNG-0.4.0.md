# Gesamtprüfung des Konzepts (0.4.0, #71)

Stand 22.11.2026 · Grundlage: alle `docs/KONZEPT-*.md`, Modulübersicht, Modulregister, `spec/v1`, UEBERGABE und
PROJEKTSTAND, abgeglichen mit EduKSX-Glossary 0.18.0-beta.1 und dem Stand von Core und Ident laut PROJEKTSTAND.
Ergänzt die [Lückenanalyse](LUECKENANALYSE-0.4.0.md): Dort steht, was **fehlt**, hier, was sich **widerspricht** oder
**veraltet** ist.

Regel (AGENTS.md): Widersprüche werden einzeln entschieden und festgehalten, nicht stillschweigend überschrieben.
Abschnitt A braucht deshalb je Punkt einen Entscheid; Abschnitt B ist redaktionell und wird mit diesem PR
nachgeführt.

## A · Widersprüche (Entscheid nötig)

| Nr. | Widerspruch | Fundstellen | Empfehlung | Entscheid |
| --- | --- | --- | --- | --- |
| W1 | Drei Klassifizierungen: DB B2 (öffentlich, intern, personenbezogen, besonders schützenswert, geheim), Plattform §6 (öffentlich, intern, vertraulich, besonders schützenswert), Kanton Zürich (öffentlich, intern, vertraulich, geheim) | DB B2, Plattform §6, PROJEKTSTART | DB B2 bleibt Feldklasse (Datenschutz); **eine** Tabelle bildet sie auf die vier Stufen des Kantons ab; Plattform §6 verweist nur darauf | in #78 |
| W2 | RPO 1 Min. / PITR für PostgreSQL ↔ täglicher Dump in Operation, Ident (I11, P7 `pg_dumpall`) und Glossary | DB C2, Plattform §7.3a, Ident I11, Glossary D6 | entscheiden in #74 (WAL-Archivierung in Operation oder RPO anpassen) | BESCHLOSSEN 22.11. (#74): RPO/RTO bleiben, WAL-Archivierung in Operation, Restore-Test monatlich (DB-E18) |
| W3 | Werkzeuge doppelt und abweichend: Plattform 7.2/7.4/S5 nennen GitOps (Argo CD/Flux), Prometheus, Renovate, CloudNativePG, cert-manager, Ansible; 7.3a und Operation nennen Komodo, VictoriaLogs, Dependabot; Leitstand nennt zusätzlich Beszel | Plattform 7.2, 7.4, S5; 7.3a; Leitstand §1, §2 | Werkzeugnamen nur noch in 7.3a (Verweis auf Operation); 7.2/7.4 als «Stufe 2 (später)» kennzeichnen; `/metrics` als Format (Prometheus-Textformat), nicht als Werkzeug | BESCHLOSSEN 22.11.: Werkzeuge nur in 7.3a; 7.4 als Anforderungen, Stufe-2-Werkzeuge nur Kandidaten. Dazu übernommen: PITR für PostgreSQL (WAL-G/pgBackRest, #74), OpenTelemetry als Schnittstelle (#76), Renovate für Digests im Betrieb (Empfehlung an Operation), kein Kubernetes/GitOps vor §9.5; Folgeprojekte abgleichen (#83) |
| W4 | Core-Standardtabellen: C7 sagt «mit Ident (Core 0.2)», Fahrplan 4.1a legt sie in 0.3 | Core C7, 4.1a | C7 an 4.1a angleichen: Core 0.3 (nach PoC #36) | BESCHLOSSEN 22.11.: C7 → Core 0.3 |
| W5 | `@eduksx/ui` «erst wenn ein zweites Modul mit Inertia/React entsteht» – Glossary und Intranet sind beide React, Flow-Prototyp ebenfalls | Core C10, Plugins P5, Modulvorlage Nichtziele | Bedingung gilt als erfüllt; Start mit #75 | BESCHLOSSEN 22.11. (#75): Start `@eduksx/ui` im Repo EduKSX-UI nach KONZEPT-DESIGN |
| W6 | Core bindet DB 1.2.1/API 1.1.1 (C9), gültig sind DB 1.3/API 1.2 (bald 1.4/1.3) | Core C9, UEBERGABE 20.11. | kein Widerspruch im Konzept, aber Drift: Folge-Issue in EduKSX-Core «Standards 1.3/1.2 übernehmen» | bewusst offen gelassen (Entscheid 22.11.2026); wird mit der nächsten Core-Minor bzw. der Übernahme der Standards je Modul (E5) erledigt |
| W7 | Edulog-Rollen `pupil`, `legal_guardian` haben keinen Zugang – Portal (Eltern) und Stundenplan (SuS) brauchen sie | Ident 2.1, Modulübersicht `portal`, `timetable` | Regel bleibt, bis das Rollenkonzept Minderjährige und Eltern regelt; dort freischalten je Modul | in #77 |
| W8 | Löschregister muss ausserhalb der Datenbank liegen und vor dem Start erreichbar sein – Selbst-Hosting beschreibt keinen Ort dafür | DB B3, Selbst-Hosting 4.1, SH-E6 | eigenes restic-Repository bzw. Ordner ausserhalb `data/`, vom Installer angelegt; ohne Register startet das Modul nicht | BESCHLOSSEN 22.11.: eigener Ordner + restic (Selbst-Hosting 4.3a); Notfallkonzept [KONZEPT-NOTFALL.md](KONZEPT-NOTFALL.md) |
| W9 | Ident I8 «ZU PRÜFEN», obwohl P8 ergab: Zitadel liefert kein SCIM an Anwendungen → Brücke sendet SCIM | Ident I8, §4.3 P8 | I8 beschliessen: Brücke sendet SCIM, ausgelöst durch Ereignisse | BESCHLOSSEN 22.11.: zuerst Anlage beim ersten Login + S4; SCIM aus der Brücke erst bei Bedarf |
| W10 | Zitadel bietet kein DPoP (P8); I9/#35 offen; Plan B Keycloak kann DPoP | Ident I9, P8, Prüfauftrag DPoP/mTLS | Entscheid in #35 (z. B. `private_key_jwt` + kurze Tokens statt DPoP); kein Abbruchgrund (4.2) | in #35 |
| W11 | Prüfliste «Anmeldung nur über Ident, lokale Passwörter nur als Notfallkonto» ↔ Glossary (zentral) mit lokalem Admin, Community-Konten und Microsoft-Anmeldung | Plattform §6, Glossary KONZEPT-BENUTZER | Übergang bis Ident produktiv: Eintrag im Ausnahmeregister (API D8) mit Ablauf «Anschluss an Ident» | BESCHLOSSEN 22.11.: lokales Login als Standard, Ident/Entra/Google optional; bei aktivem Anbieter lokal nur Notfallkonten – [KONZEPT-ANMELDUNG.md](KONZEPT-ANMELDUNG.md) |
| W12 | API-First (Grundsatz 1) ↔ Glossary-Website über Inertia direkt auf den Services | API Grundsätze, Glossary | Begriff klären | BESCHLOSSEN 22.11. (#72): API-Standard G4 – Glossary übernimmt Stufe B ab der nächsten MINOR |
| W13 | Register ↔ Wirklichkeit: Repos EduKSX-Connect, EduKSX-Time, EduKSX-Shop vorhanden, im Register `geplant`; EduKSX-Connectors und EduKSX-Prototyp nicht erwähnt; Repo heisst EduKSX-Ident (Register: EdukSX-Ident); EduKSX-Portal laut #61 vorhanden, aber nicht auffindbar | Register, Modulübersicht, Issues #57–#64 | #57–#64 in 0.4.0 aufnehmen und freigeben; Connectors und Prototyp als «kein Modul» wie Suite eintragen; Portal prüfen | BESCHLOSSEN 22.11.: Connectors und Prototyp als «kein Modul»; offene PRs übernommen: Register/Texte (time, connect, shop aktiv, Repo EduKSX-Ident) in #82, Icons (connect, shop, portal, flow, Architektur) in einem eigenen PR nach den Icon-PRs markussxch #17–#21; `portal` bleibt `geplant`, bis das Repo EduKSX-Portal auffindbar ist |
| W14 | Neue Modul-Repos entstanden ohne Profil `eduksx-modul` (#37 offen) – ob sie der Modulvorlage folgen, ist nicht geprüft | Modulvorlage M1, Register | Abgleich je Repo als Teil von #37 bzw. eigenes Issue | BESCHLOSSEN 22.11.: Abgleich der Repos nach #37 (#83) |

## B · Veraltete Stellen (redaktionell, mit diesem PR nachgeführt)

| Nr. | Stelle | Korrektur |
| --- | --- | --- |
| R1 | Plattform, Kopf: «Nichts davon ist umgesetzt» | Hinweis auf Umsetzungsstand in PROJEKTSTAND |
| R2 | Plattform 7.1, Stufe 0 «1 VPS, Traefik, Deploy je Merge» | Stand heute: dev (Hostinger), test-01/prod-01 (Infomaniak, Operation) |
| R3 | Core §5: Fahrplan 0.2 «Release nach Freigabe» | 0.2.0 veröffentlicht (PROJEKTSTAND) |
| R4 | Register und Modulübersicht: Core «0.1.0» | 0.2.0 |
| R5 | Ident 4.1: in den Zeilen P1 und P5 stehen Ergebnisse statt Schritte; 4.3: P1 «teilweise», P5 «offen», obwohl der Verlauf beide als bestanden festhält | Schritte wiederhergestellt, 4.3 nach Verlauf nachgeführt |
| R6 | Ident: Abschnitte in der Reihenfolge 2.1, 2.3, 2.2 | Reihenfolge 2.1, 2.2, 2.3 |
| R7 | Core C7: «PoC #25» (Konzept-Issue), gemeint ist die Durchführung | #36 |
| R8 | UEBERGABE, Kopf: «Stand 13.11.2026 (21:30) – Release 0.2.0; nächster Meilenstein 0.3.0» | Stand 22.11.2026, 0.3.0 eingefroren, Erweiterungsrunde 0.4.0 |

**Nicht geändert, nur vermerkt:**
- Plattform §8: Tabelle der Glossary-Issues #185–#193 «Status `triage`» – Stand im Glossary nicht geprüft (kein API-Zugriff in dieser Sitzung).
- Begriff «Rechtssammlung» (Plattform 4.2, §8, DB B1) neben Modul `codex` – einheitlich «Codex (Rechtssammlung)», sobald die Dokumente ohnehin angepasst werden.
- PROJEKTSTAND: «P2–P4, P6–P9 bestanden» – laut Ident 4.3 ist P6 nur teilweise bestanden.
- Lizenz dieses Repos (GPL-3.0) ist im Lizenzmodell (Plattform §9.7) nicht erwähnt; `spec/` ist zusätzlich MIT.

## C · Querschnitt

- **Werkzeuge an einer Stelle:** Die meisten Abweichungen (W3, Leitstand, 7.4) entstehen, weil Werkzeugnamen in mehreren Dokumenten stehen. Regel für 0.4.0: Werkzeuge nur in 7.3a mit Verweis auf Operation.
- **Status-Angaben driften:** Issue-Tabellen in den Konzepten (Core §5, Ident §5, Plattform §8) veralten schnell. Vorschlag: Status nur in GitHub, die Tabellen nennen nur das Issue.
- **Präfixe und Begriffe:** Rechte (`x-eduksx-ability`), Rollen (`roles`), Scopes und Ereignisse folgen dem Modulschlüssel – ausser den Rechten ist alles festgelegt (→ #77).

## Verlauf

- 22.11.2026: Entscheide W3, W4, W8, W9, W11, W13, W14 (Chat); neue Konzepte Anmeldung und Notfall.
- 22.11.2026: Angelegt (#71); W1–W14 zur Entscheidung, R1–R8 nachgeführt.
