# Konzept: Qualitätsziele (0.4.0, #80)

Stand: 25.11.2026 · Verantwortlich: Markus Keller · Status: **BESCHLOSSEN** 25.11.2026 (Chat, Entscheide QZ1–QZ4);
Abschnitte mit **EMPFOHLEN** gelten, bis das erste Modul sie umsetzt.

Ergänzt die bereits festgelegten Ziele – Sicherheit (ASVS L2, API C10), Barrierefreiheit (WCAG 2.1 AA, KONZEPT-DESIGN),
RPO/RTO (DB C2), Einfachheit beim Selbst-Hosting – um Performance, Verfügbarkeit und Wartbarkeit. Grundlage:
[Lückenanalyse](LUECKENANALYSE-0.4.0.md) Bereich 9. Werkzeuge der Messung stehen nur in Plattform 7.3a bzw.
MarKusSX-Operation. Verbindlichkeit: Stufen nach [KONZEPT-VORLAGE.md](KONZEPT-VORLAGE.md).

## 1. Übersicht

| Ziel | Wert | Quelle |
| --- | --- | --- |
| Sicherheit | OWASP ASVS Stufe 2, Scan, Pentest | API C10 |
| Barrierefreiheit | WCAG 2.1 AA (eCH-0059), axe-core in der CI | KONZEPT-DESIGN DS7 |
| Datenverlust, Ausfallzeit | RPO/RTO je Dienstart | DB C2 |
| Selbst-Hosting | Installation unter 15 Minuten ohne Docker-Kenntnisse | KONZEPT-SELBSTHOSTING |
| **Antwortzeiten** | §2 | dieses Konzept (QZ1) |
| **Verfügbarkeit** | §3 | dieses Konzept (QZ2) |
| **Wartbarkeit** | §4 | dieses Konzept (QZ3) |

## 2. Antwortzeiten und Last (BESCHLOSSEN, QZ1)

**Antwortzeit p95**, gemessen am Server (ohne Netz zum Client), je Monat:

| Art der Anfrage | p95 | Beispiele |
| --- | --- | --- |
| Lesen öffentlich | **300 ms** | Glossary-Index, Codex-Erlass, Einbindung |
| Lesen angemeldet, Schreiben | **800 ms** | Listen der Administration, Speichern, Freigeben |
| Export, Suche über grosse Mengen | **5 s** | wer länger braucht, läuft als **Auftrag** (Warteschlange) mit Statusmeldung |

**Lastannahmen** (Grundlage für Tests und Grösse der Server):

| Dienstart | Organisationen | Personen | Spitzenlast |
| --- | --- | --- | --- |
| zentral | 50 | 20 000 | 50 Anfragen/s |
| isoliert | 1 | 2 000 | 10 Anfragen/s |
| Ident | alle | alle Konten | Anmeldespitze Schulbeginn: wie zentral, ZU PRÜFEN im PoC (#36) |

## 3. Verfügbarkeit (BESCHLOSSEN, QZ2)

| Dienstart | Ziel je Monat | entspricht höchstens |
| --- | --- | --- |
| zentral | **99,5 %** | ca. 3,6 Stunden Ausfall |
| isoliert | **99 %** | ca. 7,3 Stunden Ausfall |
| Ident | **99,9 %** | ca. 44 Minuten Ausfall |

- **Wartungsfenster:** Sonntag 03:00–05:00 (Schweizer Zeit), angekündigt; zählt nicht als Ausfall. Updates auf prod
  laufen in diesem Fenster (heute So 03:05, wenn test grün).
- Verfügbar heisst: `/up` antwortet mit `200` von ausserhalb des Rechenzentrums.
- Ident braucht für 99,9 % Redundanz; das folgt mit dem Betrieb von Ident (Plattform 4.1, §7.5).

## 4. Wartbarkeit (BESCHLOSSEN, QZ3)

| Ziel | Wert |
| --- | --- |
| Statische Analyse | **PHPStan Stufe 7** in bestehenden Modulen, **Stufe 8** in neuen; TypeScript `strict` |
| Testabdeckung | **80 %** der Zeilen in Services und Policies (Fachlogik und Rechte) |
| Abhängigkeiten | **Sicherheitsupdates innert 7 Tagen**, übrige monatlich (Dependabot, Workflow «Fremdkomponenten prüfen») |
| Laufzeiten und Frameworks | nur Versionen mit Fehlerkorrekturen ([KONZEPT-STACK.md](KONZEPT-STACK.md) ST3) |

Alle Werte prüft `composer ci:check` (KONZEPT-STACK §5); eine Unterschreitung lässt die CI scheitern.

## 5. Messung (EMPFOHLEN)

- **Antwortzeiten:** `/metrics` im Prometheus-Textformat mit einem Histogramm der Dauer je Art der Anfrage (Label
  `class` = `read_public`, `read`, `write`, `export`; aus `x-eduksx-operation` bzw. der Route). Keine Personendaten
  in Labels.
- **Verfügbarkeit:** Prüfung von `/up` jede Minute von ausserhalb (Werkzeug nach Plattform 7.3a).
- **Last:** Lasttest mit den Annahmen aus §2 vor jedem MINOR-Release eines zentralen Moduls auf test (ZU PRÜFEN:
  Werkzeug im Betrieb).
- **Wartbarkeit:** Ergebnis von `ci:check` (Stufe, Abdeckung) im Release-Bericht.
- **Bericht:** Der Leitstand (S5, KONZEPT-LEITSTAND) zeigt je Modul und Monat p95, Verfügbarkeit und Stand der
  Abhängigkeiten.

## 6. Wenn ein Ziel verfehlt wird (BESCHLOSSEN, QZ4)

- Die Ziele sind **interne Ziele**, keine Zusage an Kunden. Eine vertragliche Zusage (SLA) braucht einen eigenen
  Entscheid und steht dann in Teil A der Vorlage [AUFTRAGSBEARBEITUNG-ZH.md](vorlagen/AUFTRAGSBEARBEITUNG-ZH.md).
- Ein verfehltes Monatsziel erzeugt ein **Issue mit Label `fehler`** im Modul-Repo, mit Messwert und Ursache.
- Zwei Monate hintereinander verfehlt: Massnahme im nächsten Release-Meilenstein (z. B. Abfrage optimieren, Auftrag
  statt direkter Antwort, mehr Ressourcen).

## 7. Entscheide

| Nr. | Frage | Optionen | Entscheid | Status |
| --- | --- | --- | --- | --- |
| QZ1 | Antwortzeiten und Last | 300 ms/800 ms/5 s / strenger / lockerer | 300 ms / 800 ms / 5 s; Last zentral 50 Org., 20 000 Personen, 50/s; isoliert 2 000 Personen, 10/s | BESCHLOSSEN 25.11.2026 |
| QZ2 | Verfügbarkeit | 99,5/99/99,9 % / überall 99,9 % / überall 99 % | zentral 99,5 %, isoliert 99 %, Ident 99,9 %; Wartungsfenster So 03:00–05:00 | BESCHLOSSEN 25.11.2026 |
| QZ3 | Wartbarkeit | Stufe 7, 80 %, 7 Tage / max, 90 % / ohne Abdeckung | PHPStan 7 (neu 8), 80 % Services/Policies, Sicherheitsupdates 7 Tage | BESCHLOSSEN 25.11.2026 |
| QZ4 | Verfehlen | interne Ziele / Zusage an Kunden | interne Ziele, Issue `fehler`, Monatsbericht | BESCHLOSSEN 25.11.2026 |

## 8. Verlauf

- 25.11.2026: Konzept angelegt (#80), QZ1–QZ4 im Chat entschieden.
