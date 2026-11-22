# Konzept: Notfall – Wiederinbetriebnahme bei fehlendem Schlüssel oder fehlender Sicherung (0.4.0, #71 W8)

Stand: 22.11.2026 · Verantwortlich: Markus Keller · Status: **BESCHLOSSEN** 22.11.2026 (Entscheid W8 der
[Gesamtprüfung](GESAMTPRUEFUNG-0.4.0.md)), Werte mit **ZU PRÜFEN** sind Vorschläge.

Ergänzt [DB-Standard B3 und C2](KONZEPT-DB-GUIDELINE.md) und [Selbst-Hosting](KONZEPT-SELBSTHOSTING.md). Für unseren
eigenen Betrieb gilt dieselbe Logik; Werkzeuge und Abläufe dort legt MarKusSX-Operation fest (Plattform §7.3a).

## 1. Ziel

Fehlt ein Schlüssel, eine Sicherung oder das Löschregister, soll ein Modul **mit vertretbarem Aufwand** wieder laufen –
ohne dass gelöschte Personendaten zurückkommen und ohne dass jemand an der Datenbank von Hand arbeiten muss.

**Grundsätze:**
1. **Vorbeugen vor Reparieren:** Jeder Schlüssel liegt an zwei Orten (Tresor bzw. Geheimnisspeicher **und** ausgedrucktes Wiederherstellungsblatt).
2. **Lieber Daten verwerfen als Gelöschtes zurückholen:** Kann das Löschregister nicht angewendet werden, werden ältere Sicherungen gesperrt, nicht eingespielt.
3. **Jeder Notfallweg ist protokolliert** und meldet sich bei den Verantwortlichen.

## 2. Was es gibt (Selbst-Hosting)

| Teil | Ort | Gesichert | Schlüssel |
| --- | --- | --- | --- |
| Daten je Modul | `/opt/eduksx/data/<modul>/` | täglich und vor Updates, restic (SH-E6) | Sicherungsschlüssel |
| Löschregister je Modul | `/opt/eduksx/loeschregister/<modul>/` (ausserhalb `data/`), nur anhängend, verschlüsselt | **eigenes** restic-Repository, nach jeder Löschung, längere Aufbewahrung als die Datensicherung | Registerschlüssel |
| Anwendungsschlüssel | `.env` (`APP_KEY` u. a.) | mit dem Wiederherstellungsblatt | – |
| Wiederherstellungsblatt | Ausdruck/PDF vom Installer, Ablage offline (Tresor der Schule) | – | enthält Sicherungs-, Register- und Anwendungsschlüssel |

Der Installer erzeugt alle Schlüssel, zeigt das Wiederherstellungsblatt **einmal** an und verlangt die Bestätigung, dass
es abgelegt ist. Die Startseite «System» erinnert jährlich an die Prüfung des Blatts.

## 3. Notfälle und Wege

| Nr. | Fall | Weg | Folge |
| --- | --- | --- | --- |
| N1 | Löschregister fehlt oder ist beschädigt, Sicherung des Registers vorhanden | `eduksx notfall register-holen <modul>`: neuestes Register aus seinem restic-Repository, Prüfsumme, Start | keine |
| N2 | Registerschlüssel fehlt, Blatt vorhanden | Schlüssel vom Wiederherstellungsblatt eintragen | keine |
| N3 | Registerschlüssel **und** Blatt fehlen, Datenbank aktuell und intakt | `eduksx notfall register-neu <modul>` (Admin mit zweitem Faktor auf dem Server): neues, leeres Register ab Stichtag; **alle Sicherungen vor dem Stichtag werden gesperrt** (nicht mehr einspielbar, löschen nach Frist); neues Blatt | Rückgriff auf alte Stände entfällt; laufender Betrieb unverändert |
| N4 | Datensicherung fehlt oder ist unbrauchbar, Datenbank verloren | Neuinstallation des Moduls; Inhalte aus Exporten bzw. Quellen (Glossary: Abgleich mit dem zentralen Glossary, Module mit Stammdaten: `connect`/Import); Register bleibt gültig und wird beim ersten Start angewendet | Datenverlust seit dem letzten Export; dokumentiert als Vorfall |
| N5 | Sicherungsschlüssel fehlt, Blatt fehlt | Sicherungen sind nicht lesbar → wie N4; neue Sicherung mit neuem Schlüssel sofort | wie N4 |
| N6 | Anwendungsschlüssel (`APP_KEY`) fehlt | vom Blatt; ohne Blatt: neuer Schlüssel, verschlüsselte Felder (2FA-Geheimnisse, Zugangsdaten) sind verloren → alle Personen richten den zweiten Faktor neu ein, Zugangsdaten zu Fremdsystemen neu eintragen | Aufwand für die Personen, keine Datenlücke |

**«Ohne Register kein Start» (DB B3, Regel 3) bleibt.** Einziger Ausweg ist N3 – bewusst, protokolliert und mit Sperre
der älteren Sicherungen. So kommt kein gelöschter Datensatz zurück.

## 4. Pflichten

- **Befehle** `eduksx notfall …` gehören zur Suite (Update-Dienst) bzw. zu `eduksx/core`; sie laufen nur auf dem Server, verlangen eine Admin mit zweitem Faktor und schreiben ins Sicherheitsprotokoll.
- **Übung:** Die CI der Suite spielt N1, N3 und N4 auf einer frischen VM durch; beim Kunden empfohlen einmal jährlich (ZU PRÜFEN: geführte Übung auf der Seite «System»).
- **Unser Betrieb:** dieselben Fälle in MarKusSX-Operation abbilden (Schlüssel in 1Password plus Notfallkopie offline, DB C2); als Folge-Issue dort.
- **Meldung:** Jeder Notfallweg erzeugt einen Vorfall-Eintrag; bei Personendaten prüft die verantwortliche Stelle die Meldepflicht (DB B13).

## 5. Entscheide

| Nr. | Frage | Entscheid | Status |
| --- | --- | --- | --- |
| NF1 | Ort des Löschregisters beim Selbst-Hosting | eigener Ordner ausserhalb `data/`, eigenes restic-Repository | BESCHLOSSEN 22.11.2026 (W8) |
| NF2 | Schlüsselablage | Tresor + Wiederherstellungsblatt vom Installer | BESCHLOSSEN 22.11.2026 |
| NF3 | Register und Schlüssel verloren | neues Register ab Stichtag, ältere Sicherungen gesperrt (N3) | BESCHLOSSEN 22.11.2026 |
| NF4 | Übungen beim Kunden | jährlich empfohlen, geführte Übung | ZU PRÜFEN |

## 6. Verlauf

- 22.11.2026: Angelegt nach Entscheid W8 (Gesamtprüfung 0.4.0).
