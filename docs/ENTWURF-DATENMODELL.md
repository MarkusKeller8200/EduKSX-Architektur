# Entwurf: Datenmodell Kontakt, Verwendung, Verbund (#124)

**Status: ENTWURF, nicht freigegeben.** Stand 28.11.2026, entstanden im Chat. Kein Punkt dieses Dokuments ist
beschlossen. Es wurde **nicht** vollständig mit den beschlossenen Konzepten abgeglichen; die bekannten Widersprüche
stehen in §6 und brauchen je einen Entscheid über `konzept-anpassung`, bevor etwas umgesetzt wird.

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

## 6. Widersprüche zu beschlossenen Konzepten (OFFEN)

| Nr. | Entwurf | Beschlossen | Zu entscheiden |
| --- | --- | --- | --- |
| W1 | Kontakt-Kern als gemeinsame Tabellen, auf die People und Fachmodule verweisen | DB-Standard E2: Schema je Modul, kein Zugriff auf das Schema eines anderen Moduls; E3: Personen über Modulgrenzen nur mit `issuer` + `subject` bzw. `platform_id` | Ist der Kontakt-Kern ein eigenes Modul mit API, Teil von `connect`, oder eine Bibliothek, deren Tabellen in jedem Modul liegen? |
| W2 | Klassen, Schulhäuser und Zuordnung von Personen als Verbund und Zugehörigkeit im Kontakt-Kern | DB-E17: Stammdaten einer Organisation führt `connect` und bietet sie über seine API an | Wer führt diese Stammdaten: `connect` oder der Kontakt-Kern? |
| W3 | Länder, Gemeinden und Ortschaften als mitgelieferte Tabellen | DB-E17: feste Codelisten liegen versioniert als Code in `eduksx/core`, keine Tabelle | Gilt DB-E17 auch für grosse Listen (mehrere tausend Einträge, mit Nachfolgern), oder werden diese als Tabellen-Paket geliefert? |
| W4 | Zusätzliche Stufe «erhöhter Schutz» für Grenzfälle | B2 kennt fünf Datenklassen | Sechste Klasse, Merkmal an der Klasse «personenbezogen», oder Grenzfälle als «besonders schützenswert» führen? |
| W5 | Massnahmen je Klasse (feldweise Verschlüsselung, Sperre in Export und Suche, zwingende Zwei-Faktor-Anmeldung) | B2, B6, B11 regeln Historie, Verschlüsselung und Leseprotokoll bereits | Abgleichen; nur Lücken als Anpassung beantragen |
| W6 | Katalog der Verwendungen und «Rechte je Verwendung» | KONZEPT-ROLLEN (#77) | Verhältnis von Verwendung zu Rolle und Geltungsbereich klären |
| W7 | Neue Bereiche People und Referenzdaten sowie weitere mögliche Module aus der Modul-Landkarte | Modulschlüssel nur aus `REGISTER-MODULE.md` | Aufnahme ins Register erst nach Entscheid |
| W8 | Pflichtspalten nach A3a nicht ausgeschrieben; Mandant (`organization_id`) nicht modelliert | A3a, B1 | Vor einer Umsetzung ergänzen |

Nicht abgeglichen wurden KONZEPT-CORE, KONZEPT-IDENT, KONZEPT-ROLLEN und KONZEPT-PROTOKOLLIERUNG.

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
