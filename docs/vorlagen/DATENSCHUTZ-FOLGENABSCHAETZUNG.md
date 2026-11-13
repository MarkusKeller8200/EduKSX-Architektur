# Datenschutz-Folgenabschätzung – Modul `<schlüssel>`

Vorlage aus EduKSX-Architektur ([Modulvorlage](../KONZEPT-MODULVORLAGE.md) 4.3) – kopieren als
`docs/DATENSCHUTZ-FOLGENABSCHAETZUNG.md` im Modul. Pflicht nach DB-Standard B10, wenn das Modul Daten der Klasse
«besonders schützenswert» bearbeitet oder Personendaten online für viele Personen zugänglich macht. Für Kunden im Kanton
Zürich gilt **zusätzlich** die Vorlage des Kantons; bei besonderen Risiken legt der Kunde das Vorhaben der bzw. dem
Datenschutzbeauftragten zur **Vorabkontrolle** vor. Arbeitshilfe, keine Rechtsberatung; nur erfundene Beispiele.

Stand: JJJJ-MM-TT · Modulversion: X.Y.Z · Erstellt von: … · Geprüft durch Fachperson: … am …

## 1. Vorhaben

- Was macht das Modul, für wen, warum? (zwei bis drei Sätze)
- Verweis auf das [Verzeichnis der Bearbeitungen](DATENSCHUTZ-VERZEICHNIS.md) (Zwecke, Daten, Empfänger)
- Neu gegenüber der letzten Fassung: …

## 2. Notwendigkeit und Verhältnismässigkeit

| Frage | Antwort |
|---|---|
| Ist jede Datenkategorie für den Zweck nötig? Was wurde weggelassen? | |
| Gibt es eine mildere Lösung (weniger Daten, Pseudonyme, kürzere Fristen)? | |
| Wie lange werden die Daten aufbewahrt, und warum so lange? | |
| Werden Daten Minderjähriger bearbeitet? Welche Schutzmassnahmen gelten? | |

## 3. Risiken für die Betroffenen

Eintrittswahrscheinlichkeit und Schwere je Risiko: tief / mittel / hoch.

| Risiko | Betroffene | Wahrscheinlichkeit | Schwere | Massnahmen | Restrisiko |
|---|---|---|---|---|---|
| Unbefugter Zugriff einer anderen Organisation | | | | Mandantentrennung (DB B1), Test mit zwei Organisationen | |
| Zugriff mit gestohlenem Konto | | | | MFA für privilegierte Rechte, kurze Tokens (API C1) | |
| Datenabfluss über Protokolle oder Exporte | | | | Maskierung (API C7), Export nur mit Recht (DB B8) | |
| Verlust oder Verfälschung | | | | Sicherung, Wiederherstellungstest (DB C2), Historie (DB A7) | |
| Bekanntgabe an Dritte ohne Grundlage | | | | Positivlisten (API C4), keine Personendaten in Ereignissen (API B7) | |

## 4. Massnahmen und Nachweise

- Sicherheitsnachweis: ASVS Level 2, Scan, Penetrationstest (API C10) – Datum, Ergebnis
- Protokoll der Lesezugriffe auf «besonders schützenswert» (DB B11)
- Schulung bzw. Anleitung der Organisations-Admins
- Ablauf bei Datenschutzverletzungen (DB B13)

## 5. Ergebnis

- Restrisiko: tragbar / nicht tragbar – Begründung
- Vorabkontrolle nötig: ja / nein – eingereicht am …, Stellungnahme vom …
- Freigabe durch die verantwortliche Stelle (Kunde): Name, Funktion, Datum

## 6. Verlauf

- JJJJ-MM-TT: angelegt.
