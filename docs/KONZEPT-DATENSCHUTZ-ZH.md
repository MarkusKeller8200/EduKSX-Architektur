# Konzept: Datenschutz nach Vorgaben des Kantons Zürich (0.4.0, #78)

Stand: 25.11.2026 · Verantwortlich: Markus Keller · Status: **BESCHLOSSEN** 25.11.2026 (Chat, Entscheide DZ1–DZ5);
Punkte mit **ZU PRÜFEN** klärt die Fachperson (#22). Keine Rechtsberatung.

Ergänzt den [DB-Standard](KONZEPT-DB-GUIDELINE.md) (B2, B3, B7–B14), den [API-Standard](KONZEPT-API-GUIDELINE.md)
(C9) und die Vorlagen in [docs/vorlagen/](vorlagen/). Grundlage: [Lückenanalyse](LUECKENANALYSE-0.4.0.md) 2.9 und
Widerspruch W1 der [Gesamtprüfung](GESAMTPRUEFUNG-0.4.0.md). Verbindlichkeit: Stufen nach [KONZEPT-VORLAGE.md](KONZEPT-VORLAGE.md).

## 1. Ziel

Eine Schule im Kanton Zürich kann EduKSX einsetzen, ohne die Vorgaben der Datenschutzbeauftragten (DSB) und des
Kantons selbst übersetzen zu müssen: gleiche Klassifizierung, fertige Vertragsunterlagen, geklärte Anbieter, Regel für
das Archiv und ein Nachweis je Modul für ihr ISMS.

**Nichtziele:**
- keine Rechtsberatung; die Unterlagen sind Arbeitshilfen
- keine Informationen der Stufe «geheim» des Kantons in EduKSX
- kein eigenes Archivsystem (das Archiv bleibt bei Gemeinde bzw. Staatsarchiv)

## 2. Klassifizierung (BESCHLOSSEN, DZ1 – löst W1)

Der Kanton unterscheidet **öffentlich, intern, vertraulich, geheim**. Nach der Informationsklassifizierung des
Mittelschul- und Berufsbildungsamts (MBA) gelten Personendaten als «intern» (§ 3 Abs. 3 IDG) und besondere
Personendaten als «vertraulich» (§ 3 Abs. 4 IDG). Die Datenklassen des DB-Standards (B2, je Feld) bleiben; diese
Tabelle ist die **einzige** Zuordnung:

| Datenklasse DB B2 (je Feld) | Stufe Kanton Zürich | Hinweis |
| --- | --- | --- |
| öffentlich | **öffentlich** | |
| intern | **intern** | |
| personenbezogen | **intern** | Personendaten, § 3 Abs. 3 IDG |
| besonders schützenswert | **vertraulich** | besondere Personendaten, § 3 Abs. 4 IDG |
| geheim (Passwort-Hash, Token, 2FA-Geheimnis) | **vertraulich** | technische Geheimnisse; die Stufe «geheim» des Kantons wird in EduKSX nicht bearbeitet |

- **Je Modul** gilt die höchste Stufe seiner Felder; sie steht im Steckbrief (S5) und bestimmt die Betriebsart
  (Plattform §6, 4.2): «vertraulich» → isoliert oder zentral nur mit Folgenabschätzung (DB B10).
- Plattform §6 nennt nur noch diese vier Stufen und verweist hierher.

## 3. Bearbeiten im Auftrag (BESCHLOSSEN, DZ2)

Betreibt EduKSX ein Modul für eine Schule, ist das ein **Bearbeiten im Auftrag** (§ 6 IDG, § 25 IDV); nach § 25 IDV
braucht es dafür einen **schriftlichen Vertrag**.

- Grundlage sind die **«Allgemeinen datenschutzrechtlichen Geschäftsbedingungen bei der Datenbearbeitung durch
  Dritte»** des Regierungsrats (AGB Datenbearbeitung durch Dritte); EduKSX übernimmt sie unverändert.
- Die Vorlage [vorlagen/AUFTRAGSBEARBEITUNG-ZH.md](vorlagen/AUFTRAGSBEARBEITUNG-ZH.md) ergänzt nur, was je Modul und
  Kunde verschieden ist: Module, Datenklassen und Stufen, Betriebsart, Standort, Unterauftragnehmer, Fristen,
  Sicherung, Meldewege.
- Sie enthält den **Abgleich mit den Checklisten** des DSB-Leitfadens «Bearbeiten im Auftrag» (Anhang 2
  «Informationssicherheitsmassnahmen», Anhang 3 «Kriterien für die Vertragsprüfung»), damit die Schule ihn nicht selbst
  erarbeiten muss.
- ZU PRÜFEN (#22): ob die AGB für Gemeinden und Schulgemeinden unverändert gelten oder eine Gemeindefassung nötig ist.

## 4. Anbieter und Cloud (BESCHLOSSEN, DZ3)

Nach dem Merkblatt Cloud Computing der DSB ist auch die Nutzung von Cloud-Diensten ein Bearbeiten im Auftrag.

| Anbieter | Zweck | Personendaten | Regel |
| --- | --- | --- | --- |
| **Infomaniak** (Schweiz) | test und prod, Sicherungen | ja | Risikoanalyse nach Merkblatt Cloud Computing in der Vorlage; Datenort Schweiz |
| **Hostinger** | dev | **nein** | nur erfundene bzw. anonymisierte Daten (DB B12) |
| **Cloudflare** (US-Unternehmen) | DNS, öffentliche Seiten | **nein** | **nur öffentliche Inhalte** (z. B. Glossary, Codex, GitHub Pages); Personendaten laufen nie über Cloudflare – damit entfällt die Frage CLOUD Act für Personendaten |
| GitHub (US-Unternehmen) | Quellcode, Issues | nein | keine echten Daten in Issues, Commits oder Bildschirmfotos (AGENTS.md) |

- Neue Anbieter nur mit Eintrag in dieser Tabelle und, wenn Personendaten betroffen sind, mit Risikoanalyse.
- Verschlüsselung der Ablage und Schlüssel getrennt vom Anbieter nach DB C2 und dem Leitfaden «Verschlüsselung der
  Daten im Rahmen der Auslagerung» (ZU PRÜFEN #22: Abgleich im Detail).
- Prüfliste Plattform §6: Modul nennt seine Anbieter; ein Modul mit Personendaten hinter Cloudflare besteht nicht.

## 5. Archivierung (BESCHLOSSEN, DZ4)

Öffentliche Organe bieten Unterlagen vor dem Vernichten dem zuständigen Archiv an. Neue Regel im DB-Standard B3:

1. **Anbieten, dann löschen:** Module mit Geschäftsunterlagen (Codex, Intranet, Sign, Staffing; weitere nach Steckbrief)
   löschen nach Ablauf der Frist nicht direkt, sondern legen die betroffenen Unterlagen zuerst als **Archivangebot** an.
2. Das Archivangebot ist ein **Export als PDF/A** (Dokumente, Ansichten) **plus CSV** (Metadaten und Tabellen, UTF-8,
   Spalten mit deutscher Beschreibung nach DB A8), mit Prüfsummen und einem Verzeichnis.
3. Die Schule bestätigt «übernommen» oder «nicht archivwürdig»; erst dann wird gelöscht (Eintrag im Löschregister).
   Ohne Antwort nach einer Frist [90 Tage] erinnert das Modul; es löscht nie stillschweigend.
4. Ein Format nach eCH-0160 (Ablieferungspaket) folgt, wenn ein Archiv es verlangt.
- ZU PRÜFEN (#22): Fristen und Zuständigkeit (Gemeindearchiv bzw. Staatsarchiv) je Unterlagenart.

## 6. Nachweis für das ISMS der Schule (BESCHLOSSEN, DZ5)

Schulen im Kanton Zürich führen ein ISMS (Leitfaden Informationssicherheit in Volksschulen). Jedes Modul liefert dazu
einen **Nachweis**: welche Anforderungen das Modul erfüllt, welche beim Betrieb (EduKSX bzw. Kunde) liegen und welche
die Schule selbst erfüllen muss. Vorlage: Abschnitt «Nachweis ISMS» in
[vorlagen/AUFTRAGSBEARBEITUNG-ZH.md](vorlagen/AUFTRAGSBEARBEITUNG-ZH.md); je Modul als `docs/NACHWEIS-ISMS.md`
(Modulvorlage).

## 7. Fachperson (#22)

Die Prüfung durch eine Fachperson bleibt Voraussetzung vor dem ersten Kunden. Sie prüft API C9, DB B3, diese Zuordnung
und die Vorlage. ZU PRÜFEN: wer (z. B. Datenschutzberatung der Schulgemeinde oder externe Fachperson) und bis wann.

## 8. Entscheide

| Nr. | Frage | Optionen | Entscheid | Status |
| --- | --- | --- | --- | --- |
| DZ1 | Zuordnung DB B2 → Stufen des Kantons | nach MBA / strenger / B2 ersetzen | nach MBA: personenbezogen → intern, besonders schützenswert und Geheimnisse → vertraulich; «geheim» nicht in EduKSX | BESCHLOSSEN 25.11.2026 |
| DZ2 | Grundlage Vertrag | AGB des Kantons / eigener Vertrag | AGB Datenbearbeitung durch Dritte + Vorlage mit Checklisten-Abgleich | BESCHLOSSEN 25.11.2026 |
| DZ3 | Cloudflare | nur öffentliche Inhalte / mit Risikoanalyse / gar nicht | nur öffentliche Inhalte, keine Personendaten | BESCHLOSSEN 25.11.2026 |
| DZ4 | Format Archivexport | eCH-0160 / PDF/A + CSV / offen | PDF/A + CSV; eCH-0160 bei Bedarf | BESCHLOSSEN 25.11.2026 |
| DZ5 | Nachweis für das ISMS | je Modul | `docs/NACHWEIS-ISMS.md` je Modul nach Vorlage | BESCHLOSSEN 25.11.2026 |

## 9. Quellen

- MBA Kanton Zürich: Informationsklassifizierung (IKT-Grundversorgung Sek II)
- DSB Kanton Zürich: Leitfaden Bearbeiten im Auftrag; Merkblatt Cloud Computing; Merkblatt Nutzung der
  Cloud-Produkte von US-Unternehmen; Leitfaden Verschlüsselung der Daten im Rahmen der Auslagerung; Leitfaden
  Informationssicherheit in Volksschulen
- Regierungsrat Kanton Zürich: AGB Datenbearbeitung durch Dritte (24.06.2015)
- Staatsarchiv Kanton Zürich: Leitfaden Informationsverwaltung und Archivierung für Gemeinden

## 10. Verlauf

- 25.11.2026: Konzept angelegt (#78), DZ1–DZ5 im Chat entschieden.
