# Entwurf: Datenmodell Kontakt, Verwendung, Verbund (#124)

**Status: ENTWURF, nicht freigegeben.** Stand 28.11.2026, entstanden im Chat. Kein Punkt dieses Dokuments ist
beschlossen. Es wurde **nicht** vollständig mit den beschlossenen Konzepten abgeglichen; die bekannten Widersprüche
und die Richtungsentscheide vom 28.11.2026 stehen in §6. Umgesetzt wird erst über die dort genannten Issues.

Datei: [`datenmodell/kontakt-kern.dbml`](datenmodell/kontakt-kern.dbml), Arbeitsweise:
[`datenmodell/README.md`](datenmodell/README.md).

## 1. Idee

Ein Kontakt hat keine feste Rolle. Was er ist, ergibt sich aus der Verwendung.

| Baustein | Bedeutung | Beispiele |
| --- | --- | --- |
| Kontakt | Person oder Organisation | Schülerin, Mutter, Fachstelle, Firma |
| Verwendung | Funktion des Kontakts, mit Zeitraum; mehrere gleichzeitig | Lernende, Erziehungsberechtigte, Mitarbeitende, Behördenmitglied |
| Verbund | Gruppe von Kontakten | Haushalt, Klasse, Schulhaus, Gremium |
| Zugehörigkeit | Kontakt in einem Verbund, mit Funktion und Zeitraum | Klassenlehrperson der Klasse, Mitglied der Behörde |
| Beziehung | Kontakt zu Kontakt, mit Zeitraum | erziehungsberechtigt, Notfallkontakt, arbeitet bei |

Regeln des Entwurfs:

- Ein Modul erhält nur Kontakte mit einer Verwendung, die für das Modul zugelassen ist (`module_usage_types`).
- Rechte gelten je Verwendung und werden nicht zusammengezählt (Elternteil und Lehrperson in einer Person).
- Kommunikationswege können an einer Verwendung hängen (schulische und private Adresse getrennt).
- Ein Kontakt ohne Verwendung hat keinen Zweck mehr und wird zur Löschung vorgeschlagen.
- Gesundheitsdaten und andere besondere Personendaten liegen nie am Kontakt, sondern im Fachmodul.

## 2. Schnitt

| Bereich | Inhalt |
| --- | --- |
| Kontakt-Kern | Kontakt, Person, Organisation, Verwendung, Kommunikationsweg, Verbund, Zugehörigkeit, Beziehung, Kennung im Fremdsystem, Sperrvermerk |
| People | Stammdaten der Person, Sprachen, Heimatort, Adressen, Sorge- und Auskunftsrecht, Notfallkontakte, Einwilligungen, Notizen, Zusatzfelder |
| Referenzdaten | Länder, Gemeinden, Ortschaften mit PLZ, Stand der Lieferung |

## 3. Datenarten

Unabhängig von der Datenklasse: Die Datenklasse sagt, wie stark etwas geschützt wird; die Datenart sagt, wo es liegt,
wer es abgleicht und wie lange es lebt.

| Datenart | Wem gehören die Daten | Wer pflegt sie | Beispiele |
| --- | --- | --- | --- |
| Stammdaten | der Schule | die Schule, teils über `connect` | Kontakte, Adressen, Klassen, Verwendungen |
| Betriebsdaten | der Schule | entstehen im Betrieb | Absenzen, Noten, Zeiteinträge, Buchungen |
| Referenzdaten | einer amtlichen oder normgebenden Stelle | EduKSX, über Updates | Länder, Gemeinden, Ortschaften |
| Systemkatalog | Teil der Programmlogik | EduKSX | Verwendungsarten, Beziehungsarten (Enums nach A4) |
| Schulkatalog | der Schule | die Schule | Funktionen im Verbund, Zusatzfelder |

Folgen: Stammdaten werden laufend abgeglichen, Betriebsdaten nicht. Wird ein Fremdprodukt abgelöst, sind die Stammdaten
schon da; für die Betriebsdaten braucht es je Modul einen Entscheid (übernehmen oder im Altsystem archivieren).

## 4. Datenklassen

Massgebend sind die Datenklassen nach [KONZEPT-DB-GUIDELINE.md](KONZEPT-DB-GUIDELINE.md) B2 und die Zuordnung in
[KONZEPT-DATENSCHUTZ-ZH.md](KONZEPT-DATENSCHUTZ-ZH.md) §2. Im Entwurf gilt:

- Der Kontakt-Kern und People enthalten **kein** Feld der Klasse «besonders schützenswert».
- Grenzfälle sind in der DBML-Datei als «personenbezogen, erhöhter Schutz (Vorschlag)» markiert: Sperrvermerke, Sorge-
  und Auskunftsrecht, Nationalität, Sprachen, Dolmetschbedarf, AHV-Nummer, Freitext der Notizen. Diese Stufe gibt es in
  B2 nicht (Widerspruch W4).
- Zusatzfelder tragen ihre Datenklasse an der Definition (`data_class`).

## 5. Gegenprobe

Die Felder der heute eingesetzten Schulverwaltung wurden dem Entwurf zugeordnet (227 Exportfelder): 54 liegen im
Entwurf, 77 sind Angaben von Bezugspersonen (dieselben Tabellen über die Beziehung), 33 sind berechnet, 63 gehören in
Fachmodule (Schullaufbahn und Statistik, Gesundheit, sonderpädagogische Massnahmen, Konto, Abgleich, Nachrichten,
Finanzen).

## 6. Widersprüche zu beschlossenen Konzepten und Entscheide vom 28.11.2026

Die Projektverantwortliche hat am 28.11.2026 im Chat je Widerspruch die **Richtung** entschieden. Die beschlossenen
Konzepte sind damit noch **nicht** geändert; dafür gibt es je ein Issue `konzept-anpassung` (Status `triage`,
Umsetzung erst nach Freigabe).

| Nr. | Widerspruch | Entscheid 28.11.2026 | Issue |
| --- | --- | --- | --- |
| W1 | Entwurf: Kontakt-Kern als gemeinsame Tabellen. Beschlossen: Schema je Modul (E2), Personen über Modulgrenzen nur als Referenz (E3) | **`connect` führt die Kontaktdaten.** Andere Module halten nur die Personenreferenz aus Core (C7). Das Modell dieses Entwurfs wird Grundlage für das Konzept `connect` | #126, #43 |
| W2 | Entwurf: Klassen und Schulhäuser im Kontakt-Kern. Beschlossen: führt `connect` (DB-E17) | **`connect` bleibt führend;** Fachmodul `registry` (Klasseneinteilung, Schullaufbahn, Statistik) arbeitet damit | #127 |
| W3 | Entwurf: Referenzdaten als Tabellen. Beschlossen: Codelisten als Code in `eduksx/core` (DB-E17) | **Alle Listen als Tabellen,** aktualisiert über den Update-Dienst der Suite; die Schule kann eigene Einträge hinzufügen sowie Einträge aktivieren und deaktivieren | #128 |
| W4 | Entwurf: Stufe «erhöhter Schutz». Beschlossen: fünf Datenklassen (B2) | **Merkmal «erhöhter Schutz»** zur Klasse «personenbezogen»; B2 behält fünf Klassen | #129 |
| W5 | Entwurf: eigene Massnahmentabelle. Beschlossen: Verschlüsselung (B6), Leseprotokoll (B11), `read_sensitive` (RO3) | **Nur die Lücken:** heikle Felder standardmässig nicht in Export, Suche und Schnittstellen | #129 |
| W6 | Entwurf: Katalog «Verwendung» mit Rechten je Verwendung. Beschlossen: Personengruppen ohne Rechte, Rechte nur aus Rollen (KONZEPT-ROLLEN §2, RO3) | **Verwendung = Personengruppe.** Liste um Mitarbeitende und Behördenmitglied ergänzen; Mehrfachzugehörigkeit mit Zeitraum; Rechte nur aus Rollen | #130 |
| W7 | Entwurf: neue Module. Beschlossen: Schlüssel nur aus dem Register | **`registry` und `health` als «geplant» eintragen;** `people` entfällt (W1) | #127 |
| W8 | Pflichtspalten nach A3a und Mandant nicht ausgeschrieben | bleibt so, bis feststeht, in welchem Schema die Tabellen liegen (Hinweis im Kopf der DBML-Datei) | – |

Die DBML-Datei ist auf diese Entscheide angepasst: Personengruppen statt Verwendungen, alle Referenzlisten als Tabellen
mit Herkunft (`entry_source`) und `is_active`, Bereiche als Teil von `connect`. Wo in §1 bis §5 noch «Verwendung»,
«Kontakt-Kern» oder «People» steht, ist nach W1 und W6 `connect` bzw. die Personengruppe gemeint.

Nicht abgeglichen wurden KONZEPT-CORE, KONZEPT-IDENT, KONZEPT-ANMELDUNG und KONZEPT-PROTOKOLLIERUNG.

## 7. Weitere offene Punkte

- Geburtsdatum im Kern oder in People.
- Lehrperson als eigene Verwendung oder aus der Zugehörigkeit zu einer Klasse abgeleitet.
- Notizen am Kontakt beibehalten oder in die Fachmodule verlegen (Freitext umgeht den Schutz).
- Heimatort als Freitext ohne zuordenbare Gemeinde.
- Nutzungsbedingungen der Quellen für Referenzdaten prüfen.
- Einstufung der Grenzfälle durch die Fachperson Datenschutz (#22).

## 8. Ansichten ausserhalb des Repositories

Abbilder des Entwurfs; private Arbeitsflächen der Projektverantwortlichen. Massgebend ist die DBML-Datei.

| Ansicht | Inhalt |
| --- | --- |
| [Datenmodell Ident, Kontakt, Verwendung](https://claude.ai/artifact/1mCTyECjzUJdphWo1t929B) | Bausteine, Beispiel Mehrfachfunktion, Regeln |
| [Datenbankschema Kontakt-Kern](https://claude.ai/artifact/FiYJFWkpN2eBTzbFW1PFjy) | Tabellen mit Datenklasse und Datenart (Stand vor der Angleichung an A1) |
| [Modul-Landkarte V2](https://claude.ai/artifact/46kb8bPCWR7DUSfcrfy44J) | Bereiche, Module, Abhängigkeiten, Abdeckung durch Fremdprodukte |

## Verlauf

- 28.11.2026: Entwurf aus dem Chat abgelegt (#124).
- 28.11.2026: Richtungsentscheide W1–W8; DBML angepasst; Issues #126–#130 angelegt.
