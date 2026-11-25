# Konzept: Protokollierung und Fehlersuche (0.4.0, #76)

Stand: 25.11.2026 · Verantwortlich: Markus Keller · Status: **BESCHLOSSEN** 25.11.2026 (Chat, Entscheide PR1–PR4);
Abschnitte mit **EMPFOHLEN** gelten, bis das erste Modul sie umsetzt.

Hebt [API-Standard C7](KONZEPT-API-GUIDELINE.md) auf BESCHLOSSEN und baut ihn aus. Ergänzt Plattform §6 «Betrieb»
und S5 (OpenTelemetry als Schnittstelle, W3). **Werkzeuge** des Betriebs (Protokollspeicher, Überwachung, Alarmkanäle)
stehen nur in [Plattform 7.3a](KONZEPT-PLATTFORM.md) bzw. MarKusSX-Operation; dieses Konzept legt fest, **was** ein
Modul liefert. Grundlage: [Lückenanalyse](LUECKENANALYSE-0.4.0.md) 2.7. Verbindlichkeit: Stufen nach
[KONZEPT-VORLAGE.md](KONZEPT-VORLAGE.md).

## 1. Ziel

Jeder Fehler lässt sich über eine ID von der Meldung bis in alle beteiligten Module verfolgen – ohne Personendaten in
den Protokollen und ohne Debug-Modus in prod.

**Nichtziele:**
- kein eigenes Fehler-Tracking-Werkzeug (PR1)
- keine Auswertung von Nutzungsverhalten; Statistik bleibt ohne Cookies und ohne Personenbezug

## 2. Abgrenzung zu MarKusSX-Operation (BESCHLOSSEN)

| Aufgabe | Modul (dieses Konzept) | Betrieb (Operation, Plattform 7.3a) |
| --- | --- | --- |
| Inhalt, Aufbau und Stufen der Protokolle | ✓ | |
| Maskierung von Personendaten | ✓ (Baustein in Core) | |
| Ausgabe: JSON auf stdout, OpenTelemetry (OTLP) | ✓ | |
| Sammeln, Speichern, Fristen durchsetzen | | ✓ |
| Alarme und Benachrichtigung | Ereignisse und Schwellwerte benennen | ✓ Werkzeug und Kanal |
| Zugriff für Support | Rechte, Protokollpaket (§7) | Zugang zum Protokollspeicher |

## 3. Protokollarten (BESCHLOSSEN, PR3)

| Art | Inhalt | Ort | Frist | Zugriff |
| --- | --- | --- | --- | --- |
| **Anwendung** | Fehler, Warnungen, Abläufe | stdout/OTLP → Protokollspeicher | **30 Tage** | Betrieb, Support |
| **Zugriff** | Anfragen nach C7 (Methode, Pfad ohne Query-Werte, Status, Dauer, Token-Präfix, Organisation) | stdout/OTLP → Protokollspeicher | **90 Tage** (wie API C9) | Betrieb, Sicherheit |
| **Job** | Aufträge der Warteschlange, Zeitpläne, Sync | stdout/OTLP → Protokollspeicher | **30 Tage** | Betrieb, Support |
| **Sicherheit** | Anmeldung, Rechteänderung, Debug ein/aus, Exporte, Lesezugriffe auf besonders schützenswerte Daten (DB B11) | Datenbank, hash-verkettet (DB A7) + Kopie im Protokollspeicher | **1 Jahr** (DB-E15) | Sicherheit, `admin` der Organisation für eigene Einträge |
| **Historie (Audit)** | fachliche Änderungen `data_changes` | Datenbank (DB A7) | nach DB-E15 | nach Rollen des Moduls |

Fristen gelten im Protokollspeicher des Betriebs und bei Selbst-Hosting in der Instanz. Sie sind **Höchstfristen**
(BESCHLOSSEN 25.11.2026): Ein Modul darf kürzer aufbewahren, wenn sein Löschkonzept es verlangt (z. B. Glossary:
Protokolle mit IP-Adressen höchstens 14 Tage, MarKusSX-Operation #19); länger nur mit Eintrag im Ausnahmeregister.

## 4. Stufen (EMPFOHLEN)

| Stufe | Wofür | prod | test | dev |
| --- | --- | --- | --- | --- |
| `error` | Fehler, die eine Anfrage oder einen Auftrag abbrechen | ✓ | ✓ | ✓ |
| `warning` | erwartete Störungen, Wiederholungen, Muster nach C7 | ✓ | ✓ | ✓ |
| `info` | Start/Ende von Aufträgen, Zustandswechsel | ✓ (Standard) | ✓ | ✓ |
| `debug` | Einzelheiten für die Fehlersuche | nur nach §5 | ✓ (Standard) | ✓ (Standard) |

## 5. Fehlersuche in prod (BESCHLOSSEN, PR2)

- `APP_DEBUG` ist in test und prod **immer aus**; Fehler an Clients ohne Stacktrace (API A6).
- Zusätzliches Debug nur **je Organisation**, **höchstens 60 Minuten**, nur durch den **Super-Admin**; danach schaltet
  es sich selbst aus.
- Ein- und Ausschalten mit Grund im **Sicherheitsprotokoll**; der `admin` der Organisation sieht den Eintrag.
- Auch im Debug gilt die Maskierung (§6); Bodies, Tokens und Geheimnisse werden nie protokolliert.

## 6. Maskierung von Personendaten (BESCHLOSSEN)

- Baustein in **`eduksx/core`**: ein Prozessor für den Logger, der Felder nach Datenklasse (DB B2) und bekannte Muster
  (E-Mail, Telefonnummer, AHV-Nummer, IBAN, Token) ersetzt.
- Module protokollieren IDs (`user_id`, `organization_id`, `request_id`), nie Namen oder Inhalte.
- **Test aus Core:** schreibt Protokolle mit Beispiel-Personendaten und prüft, dass keine davon in der Ausgabe stehen
  (Teil des Konformitätstests, API D8).

## 7. Korrelation (BESCHLOSSEN)

- Jede Anfrage hat eine `request_id` (C7) und einen W3C-**`traceparent`**; beide werden übernommen oder erzeugt.
- Weitergabe an andere Module bei Dienst-zu-Dienst-Aufrufen (S2), in Ereignissen (S4, CloudEvents-Erweiterung
  `traceparent`) und an Aufträge der Warteschlange; der Auftrag protokolliert dieselben IDs.
- Fehlermeldungen an Nutzerinnen und Nutzer zeigen die `request_id` («Fehlernummer»), damit der Support sie findet.

## 8. Alarme (BESCHLOSSEN, PR1)

Kein eigenes Fehler-Tracking. Fehler sind strukturierte Protokolle mit `request_id`; Alarme laufen über den Betrieb.
Jedes Modul benennt in seinem Betriebsteil mindestens:

- Anteil `5xx` über einem Schwellwert, `/health` nicht «ok»
- Muster nach C7 (viele `401`/`403`, viele verschiedene IDs, grosse Exporte)
- fehlgeschlagene Aufträge nach der letzten Wiederholung, Sicherung oder Restore-Test fehlgeschlagen
- Debug länger als erlaubt (sollte nie vorkommen)

## 9. Support-Zugriff (BESCHLOSSEN, PR4)

- **Zentral betrieben:** Support liest im Protokollspeicher des Betriebs nur mit eigenem Recht; jeder Zugriff auf
  Protokolle einer Organisation steht im Sicherheitsprotokoll.
- **Selbst gehostet:** kein Fernzugriff. Die Instanz erzeugt ein **Protokollpaket** für einen Zeitraum (Befehl bzw.
  Administration › System): maskiert, mit Version, Steckbrief und `/health`, verschlüsselt für den Support. Der Kunde
  sendet es selbst; die Erzeugung steht im Sicherheitsprotokoll.
- Protokollpakete gelten als «intern» (KONZEPT-DATENSCHUTZ-ZH §2) und werden nach dem Fall gelöscht, spätestens nach
  30 Tagen.

## 10. Bausteine für Core (Folgeauftrag)

Logger-Format (JSON, OTLP), Maskierungs-Prozessor mit Test, Middleware für `request_id` und `traceparent`, Weitergabe
an Aufträge und Ereignisse, befristetes Debug je Organisation, Befehl «Protokollpaket». Erfasst in #83 (Abgleich der
Folgeprojekte) für das Repo EduKSX-Core.

## 11. Entscheide

| Nr. | Frage | Optionen | Entscheid | Status |
| --- | --- | --- | --- | --- |
| PR1 | Fehler-Tracking | nur Logs + Alarme / eigenes Werkzeug / später | nur strukturierte Logs und Alarme über den Betrieb | BESCHLOSSEN 25.11.2026 |
| PR2 | Debug in prod | je Organisation befristet / je Anfrage / gar nicht | je Organisation, höchstens 60 Minuten, nur Super-Admin, protokolliert | BESCHLOSSEN 25.11.2026 |
| PR3 | Fristen | nach Art / einheitlich 90 Tage / einheitlich 1 Jahr | Anwendung und Jobs 30 Tage, Zugriff 90 Tage, Sicherheit 1 Jahr, Historie nach DB-E15 | BESCHLOSSEN 25.11.2026 |
| PR4 | Support bei Selbst-Hosting | Protokollpaket / Fernzugriff / beides | Protokollpaket, kein Fernzugriff | BESCHLOSSEN 25.11.2026 |

## 12. Verlauf

- 25.11.2026: Fristen als Höchstfristen festgelegt (Abgleich mit MarKusSX-Operation #19).
- 25.11.2026: Konzept angelegt (#76), PR1–PR4 im Chat entschieden; API C7 auf BESCHLOSSEN.
