# Projektstart – EduKSX-Architektur

Stand: 2026-11-08 · Status: **OFFEN** – Grundgerüst erst nach Bestätigung durch Projektverantwortliche:r

Steckbrief aus der Start-Checkliste (`start.py --ziel …` im GitHub-Blueprint). Er ist die Grundlage für das Grundgerüst
und für die Konfiguration in `.github/blueprint.toml`. Änderungen hier festhalten und `start.py` erneut ausführen.

## Ziel

Architektur, Schnittstellen und Betriebskonzept der EduKSX-Plattform (Ident, Module, Leitstand) für Projektverantwortliche und Entwickler der Module.

**Nichtziele:**

- kein Anwendungscode (bleibt in den Repositories der Module)
- keine Kundendaten, Zugangsdaten oder Geheimnisse
- keine Betriebsanleitung je Kunde (gehört in den Leitstand)

## Datenschutz

- Zielgruppe: öffentliche Organe, Unternehmen
- Anwendbares Recht: IDG (Kanton Zürich) bzw. DSG
- Daten: besonders schützenswert · Schutzbedarf: **vertraulich**

Die Zuordnung ist eine Arbeitshilfe, keine Rechtsberatung; bei öffentlichen Organen die zuständige
Datenschutzstelle einbeziehen (z. B. Vorabkontrolle bzw. Datenschutz-Folgenabschätzung).

## Antworten

| Frage | Antwort |
|---|---|
| Wie heisst das Projekt (voller Name)? | EduKSX-Architektur |
| Was soll das Projekt leisten, und für wen? (ein bis zwei Sätze) | Architektur, Schnittstellen und Betriebskonzept der EduKSX-Plattform (Ident, Module, Leitstand) für Projektverantwortliche und Entwickler der Module. |
| Was gehört ausdrücklich nicht dazu (Nichtziele)? | kein Anwendungscode (bleibt in den Repositories der Module), keine Kundendaten, Zugangsdaten oder Geheimnisse, keine Betriebsanleitung je Kunde (gehört in den Leitstand) |
| Welcher Kurzname soll in den Release-Titeln stehen? | EduKSX-Architektur |
| Ist es eine Web-Anwendung, eine Desktop-Anwendung oder beides? | beides |
| Wer nutzt die Anwendung? | öffentliche Organe, Unternehmen |
| Welche öffentlichen Organe? | Kanton Zürich |
| Ist das Repository neu oder gibt es es schon? | neu |
| Wer gibt Issues und Releases frei (Rolle genügt)? | Projektverantwortliche:r |
| Arbeitest du allein oder im Team? | allein |
| Ist das Repository öffentlich oder privat? | privat |
| Unter welcher Lizenz steht der Code? | GPL-3.0-or-later |
| Auf wen lautet die Lizenz? | Markus Keller |
| In welchen Programmiersprachen wird entwickelt? | Python, JavaScript / TypeScript, PHP |
| Welcher Grundsatz gilt für Abhängigkeiten? | geprüfte Pakete |
| Für welche Betriebssysteme? | Windows, macOS, Linux |
| Wo läuft die Web-Anwendung? | eigener Server / VPS |
| Wie kommt die Anwendung zu den Nutzer:innen? | Server, GitHub Pages |
| Welches Framework bzw. welche Grundlage? | Laravel + Inertia/React |
| Welche Daten verarbeitet die Anwendung? | besonders schützenswert |
| Welcher Schutzbedarf gilt für die Daten (Klassifizierung)? | vertraulich |
| Welche Anmeldungen und Zugänge braucht es? | eigene Benutzerkonten, Entra ID / SSO, externe Dienste (API) |
| In welchen Sprachen wird die Oberfläche ausgeliefert? | de-CH |
| Gibt es Plugins oder Module mit eigener Version? | nein |
| Mit welchem Befehl laufen alle Prüfungen? | python3 -m unittest discover -s tests |
| In welcher Datei steht die Versionsnummer? | version.py |
| Mit welcher Version startet das Projekt? | 0.1.0 |
| Mit welchen KI-Agenten wird gearbeitet? | Claude |
| Wie heisst der erste Meilenstein? | 0.1.0 – Grundgerüst |
| Übergabe und Projektstand auch als Kopie im Claude-Projekt führen? | nein |
| Welche ersten Funktionen gehören in diesen Meilenstein? | Plattform-Konzept ablegen (Entwurf zur Abnahme), Schnittstellen-Spezifikation (OIDC-Claims, Webhooks, Heartbeat, Modul-Steckbrief als Schemas), Anforderungen an Module (Prüfliste für jedes neue Modul), Auswahl Identity-Provider (Keycloak oder Zitadel bewerten) |

## Grundgerüst

Vorschlag für Aufbau, Ordner und erste Dateien – wird vor dem Anlegen mit Projektverantwortliche:r
abgestimmt (Status je Punkt: BESCHLOSSEN, EMPFOHLEN, OFFEN, ZU PRÜFEN):

| Punkt | Vorschlag | Status |
|---|---|---|
| Technik | Python, JavaScript / TypeScript, PHP · Laravel + Inertia/React | OFFEN |
| Ordner | Quellcode, `tests/`, `docs/` | OFFEN |
| Prüfungen | `python3 -m unittest discover -s tests` (Workflow «pruefungen») | OFFEN |
| Version | `version.py` mit 0.1.0 | OFFEN |
| Auslieferung | Server, GitHub Pages | OFFEN |

## Erster Meilenstein: 0.1.0 – Grundgerüst

- [ ] Plattform-Konzept ablegen (Entwurf zur Abnahme)
- [ ] Schnittstellen-Spezifikation (OIDC-Claims, Webhooks, Heartbeat, Modul-Steckbrief als Schemas)
- [ ] Anforderungen an Module (Prüfliste für jedes neue Modul)
- [ ] Auswahl Identity-Provider (Keycloak oder Zitadel bewerten)

Diese Punkte werden nach Bestätigung als Issues mit Testliste angelegt.
