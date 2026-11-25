# Vorlage: Bearbeiten im Auftrag für Schulen im Kanton Zürich

Vorlage nach [KONZEPT-DATENSCHUTZ-ZH.md](../KONZEPT-DATENSCHUTZ-ZH.md) §3 und §6 (#78). Arbeitshilfe, keine
Rechtsberatung; vor dem ersten Einsatz durch eine Fachperson geprüft (#22). Felder in `[eckigen Klammern]` je Kunde
ausfüllen.

## Teil A · Vereinbarung

**Grundlage:** Es gelten die «Allgemeinen datenschutzrechtlichen Geschäftsbedingungen bei der Datenbearbeitung durch
Dritte» des Regierungsrats des Kantons Zürich (AGB Datenbearbeitung durch Dritte) in der jeweils gültigen Fassung.
Diese Vereinbarung ergänzt sie; bei Widerspruch gehen die AGB vor.

| Punkt | Angabe |
| --- | --- |
| Auftraggeberin (öffentliches Organ) | [Schule, Adresse, verantwortliche Stelle] |
| Auftragnehmerin | [Betreiberin EduKSX, Adresse, Kontakt Datenschutz] |
| Module | [z. B. Intranet, Glossary] |
| Betriebsart je Modul | [zentral / isoliert / selbst gehostet] (Plattform 4.2) |
| Höchste Stufe je Modul | [öffentlich / intern / vertraulich] (KONZEPT-DATENSCHUTZ-ZH §2) |
| Kategorien betroffener Personen | [Lehrpersonen, Mitarbeitende, Schülerinnen und Schüler, Eltern …] |
| Zweck und Rechtsgrundlage | aus dem Verzeichnis der Bearbeitungen je Modul ([DATENSCHUTZ-VERZEICHNIS.md](DATENSCHUTZ-VERZEICHNIS.md)) |
| Datenort | Schweiz (Infomaniak); keine Personendaten über Cloudflare oder in dev (KONZEPT-DATENSCHUTZ-ZH §4) |
| Unterauftragnehmer | [Infomaniak … – nur mit Zustimmung der Auftraggeberin ändern] |
| Sicherung und Wiederherstellung | RPO/RTO nach DB-Standard C2; monatlicher Restore-Test mit Protokoll |
| Fristen, Löschung, Archiv | Fristen je Tabelle (DB B9); «anbieten, dann löschen» mit Export PDF/A + CSV (DB B3) |
| Meldung von Verletzungen | [Frist, Kontakt] nach DB B13 |
| Auskunft und Export | Export «alle Daten einer Person» (DB B8, API C9) |
| Ende der Zusammenarbeit | vollständiger Export, danach Löschung mit Bestätigung |
| Unterschriften | [Ort, Datum, Unterschrift beider Parteien; Genehmigung der vorgesetzten Stelle, falls nötig] |

## Teil B · Abgleich mit dem Leitfaden «Bearbeiten im Auftrag» der DSB

Je Punkt aus **Anhang 2** (Informationssicherheitsmassnahmen) und **Anhang 3** (Kriterien für die Vertragsprüfung)
des Leitfadens eine Zeile: wie EduKSX ihn erfüllt und wo der Nachweis steht. Die Punkte werden aus der jeweils gültigen
Fassung des Leitfadens übernommen (nicht hier abgeschrieben, damit die Vorlage nicht veraltet).

| Leitfaden (Anhang, Punkt) | Umsetzung in EduKSX | Nachweis | Offen |
| --- | --- | --- | --- |
| [Anhang 2, …] | z. B. Mandantentrennung `organization_id` (DB B1), Verschlüsselung (DB C2), ASVS L2 (API C10) | [Konzept, Testprotokoll] | |
| [Anhang 3, …] | z. B. Unterauftragnehmer, Datenort, Löschung (Teil A) | [Abschnitt] | |

## Teil C · Risikoanalyse je Anbieter (Merkblatt Cloud Computing)

| Anbieter | Daten | Risiken | Massnahmen | Restrisiko akzeptiert von |
| --- | --- | --- | --- | --- |
| Infomaniak | Fachdaten, Sicherungen | [z. B. Zugriff des Anbieters, Ausfall] | [Verschlüsselung, Schlüssel getrennt, Sicherung an zweitem Ort] | [Stelle, Datum] |

## Teil D · Nachweis ISMS je Modul

Für das ISMS der Schule (Leitfaden Informationssicherheit in Volksschulen). Je Modul als `docs/NACHWEIS-ISMS.md`.

| Anforderung | Erfüllt durch das Modul | Erfüllt durch den Betrieb | Aufgabe der Schule |
| --- | --- | --- | --- |
| Zugriffsschutz | Rollen und Rechte, MFA für privilegierte Rollen | Härtung, Zugriff nur über VPN | Rollen zuweisen, Austritte melden |
| Protokollierung | Sicherheitsprotokoll, Lesezugriffe (DB B11) | Aufbewahrung, Auswertung | Kontrolle der Protokolle |
| Datensicherung | Export, Löschregister | Sicherung, Restore-Test | – |
| [weitere] | | | |
