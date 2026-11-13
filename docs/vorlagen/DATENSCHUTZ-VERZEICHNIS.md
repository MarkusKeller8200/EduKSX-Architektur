# Verzeichnis der Bearbeitungen – Modul `<schlüssel>`

Vorlage aus EduKSX-Architektur ([Modulvorlage](../KONZEPT-MODULVORLAGE.md) 4.3) – kopieren als
`docs/DATENSCHUTZ-VERZEICHNIS.md` im Modul. Grundlage: DB-Standard B7–B9, API-Standard C9. Arbeitshilfe, keine
Rechtsberatung. Nur erfundene Beispiele, keine echten Personen- oder Organisationsnamen.

Stand: JJJJ-MM-TT · Modulversion: X.Y.Z · Verantwortlich (Modul): … · Geprüft durch Fachperson: … am …

## 1. Angaben zum Modul

| Feld | Inhalt |
|---|---|
| Modul (Schlüssel, Marketingname) | |
| Betriebsart | zentral / isoliert |
| Verantwortliche (Datenherrschaft) | die Schule bzw. Gemeinde als öffentliches Organ; Plattform als Auftragsbearbeiterin |
| Auftragsbearbeitungsvertrag | Verweis, Datum |
| Anwendbares Recht | IDG ZH / DSG / DSGVO (strengstes gilt, DB B7) |
| Höchste Datenklasse | öffentlich / intern / vertraulich / besonders schützenswert |
| Folgenabschätzung nötig? | ja / nein – Begründung (DB B10) |
| Datenort | Hosting, Sicherungen, Protokolle: Schweiz (Anbieter, Standort) |

## 2. Bearbeitungen

Eine Zeile je Zweck. Spalten «Tabellen» und «Operationen» werden aus dem Code erzeugt (DB B9, API C9), der Rest von
Hand gepflegt.

| Zweck | Rechtsgrundlage / Auftrag | Betroffene | Datenkategorien (Klassen) | Tabellen | Operationen (`operationId`) | Empfänger (Scopes, Module, Dritte) | Löschfrist |
|---|---|---|---|---|---|---|---|
| | | Lehrpersonen / Schüler:innen / Eltern / Verwaltung | | | | | |

## 3. Bekanntgaben und Unterauftragnehmer

| Empfänger | Zweck | Daten | Ort | Grundlage / Vertrag |
|---|---|---|---|---|
| EduKSX-Ident | Anmeldung, Konten | Kennung, Name, E-Mail, Rollen | Schweiz | Plattform S1 |

## 4. Technische und organisatorische Massnahmen

- Mandantentrennung (DB B1), Datenklassen je Feld (DB B2), Löschregister (DB B3)
- Zugriff nur über Ident mit Rechten je Objekt; zweiter Faktor für privilegierte Rechte (API C1, C2)
- Protokolle: Änderungen (DB A7), Lesezugriffe auf «besonders schützenswert» (DB B11), Aufbewahrung …
- Sicherung und Wiederherstellung mit RPO … / RTO … (DB C2)
- Kopien für Entwicklung und Test nur anonymisiert (DB B12)

## 5. Rechte der Betroffenen

| Recht | Umsetzung im Modul |
|---|---|
| Auskunft, Datenherausgabe | `GET /api/v1/me/data-export` bzw. «Meine Daten» (DB B8, API C9) |
| Berichtigung | |
| Löschung | über `ident.user.deleted` (S4) und Löschregister |
| Einschränkung | `is_processing_restricted` (DB B13) |

## 6. Verlauf

- JJJJ-MM-TT: angelegt.
