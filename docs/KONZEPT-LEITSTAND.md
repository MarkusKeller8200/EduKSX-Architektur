# Konzept: Leitstand `ops` – Kunden, Kundeninstanzen und Updates (#48)

Stand: 13.11.2026 (Meilenstein 0.3.0) · Verantwortlich: Markus Keller · Status: **BESCHLOSSEN** 13.11.2026 (eingefroren mit 0.3.0; Änderungen nur über `konzept-anpassung`).

Konkretisiert [Plattform 4.4 und S6](KONZEPT-PLATTFORM.md). Modulschlüssel `ops` laut [Modulregister](REGISTER-MODULE.md).
Betrieb der eigenen Server: Repo **MarKusSX-Operation** (Plattform §7.3a).

**Verbindlichkeit:** Stufen nach [KONZEPT-VORLAGE.md](KONZEPT-VORLAGE.md).

## 1. Ziel

Eine Stelle, die weiss, **welcher Kunde was hat**: welche Module, in welcher Version, wo sie laufen (bei uns zentral,
als Instanz bei uns oder beim Kunden selbst gehostet) und ob sie gesund sind. Für selbst gehostete Instanzen plant der
Leitstand Updates in Ringen – ohne Zugriff ins Netz des Kunden.

**Nichtziele:**
- keine Technik unserer Server: Ausrollen, Container, Betriebssystem, Sicherung, Alarme bleiben in MarKusSX-Operation
  (Komodo, Beszel, Uptime Kuma, Backrest) – ops liest dort nur
- keine Inhalte und keine Personendaten der Kunden (nur Kontakt der Verantwortlichen beim Kunden)
- kein Ersatz für Lagekarte oder Operation Center

## 2. Abgrenzung

| Frage | MarKusSX-Operation | Leitstand `ops` |
|---|---|---|
| Wofür? | Technik **unserer** Server | **Kunden** und ihre Instanzen |
| Server, Container, Stacks, Updates bei uns | Komodo, Wartungsfenster So 03:00 | zeigt Version und Zustand (liest Komodo-API) |
| Zustand, Messwerte, Alarme bei uns | Beszel, Uptime Kuma, ntfy, Lagekarte | – |
| Kunden, Verträge, Kontakte, Module je Kunde | – (Nichtziel «keine Business-Logik») | ja |
| Selbst gehostete Instanzen beim Kunden | – | Heartbeat (S6), Version, Update-Ringe, Wartungsfenster des Kunden |
| Neuer Kunde zentral | – | Organisation in Ident, Module freischalten |
| Neue Instanz bei uns | Komodo legt Stack an (Prozedur) | löst die Prozedur aus bzw. dokumentiert sie, hält die Zuordnung |
| Abrechnung | – | später |

**Grundsatz:** Was Root auf einem Server braucht, gehört zu Operation. ops braucht nie Root und nie den Docker-Socket.

## 3. Ablauf

### 3.1 Kunde und Instanzen

```text
Kunde «Schule Beispiel»
 ├─ zentral:   glossary, codex          (Organisation in Ident, kein eigener Server)
 ├─ bei uns:   intranet 2.4.1           (Instanz auf prod-01, Stack in Komodo)
 └─ vor Ort:   timetable 1.0.3          (selbst gehostet, Suite 2026.11, Heartbeat zuletzt 03:15)
```

### 3.2 Updates selbst gehosteter Instanzen (BESCHLOSSEN 13.11.2026)

Beim Kunden führt der **Update-Dienst des Suite-Pakets** die Updates aus ([KONZEPT-SELBSTHOSTING.md](KONZEPT-SELBSTHOSTING.md));
das Muster stammt aus dem Glossary (DEC-027, U3–U19). Der Leitstand gibt nur vor, **wann** welche Version erlaubt ist:

1. Release eines Moduls → läuft zuerst bei uns (**Ring 0**: test-01, dann prod-01 über Komodo, Operation).
2. ops gibt die Version für **Ring 1** frei (Pilotinstanzen, ~5 %), nach Beobachtung für **Ring 2** (alle).
3. Instanzen, die sich angemeldet haben (Heartbeat freiwillig), holen den Auftrag über S6 und führen ihn im eigenen
   Zeitfenster aus; Ergebnis kommt mit dem nächsten Heartbeat zurück.
4. Springen Instanzen zurück oder melden Fehler, stoppt ops die Freigabe automatisch.
5. Instanzen ohne Heartbeat aktualisieren nach ihrer eigenen Regel (Vorgabe «nur Korrekturen», Selbst-Hosting
   SH-E5) und sehen neue Versionen über den öffentlichen Release-Hinweis.

### 3.3 Anmeldung einer Instanz (S6)

Selbst gehostete Instanzen haben kein Ident (Plattform S1, Ausnahme). Darum meldet sich eine Instanz mit einem
**Instanz-Token** an, das ops bei der Registrierung ausstellt (einmaliger Einladungscode im Installer → Token;
gespeichert nur als Hash; widerrufbar; Präfix `ops_inst_`). Instanzen bei uns können zusätzlich Client Credentials
über Ident verwenden. Aufträge sind signiert (JWS, [ops-instances.openapi.json](../spec/v1/ops-instances.openapi.json)).

## 4. Entscheide

| Nr. | Frage | Optionen | Entscheid | Status |
|---|---|---|---|---|
| L1 | Aufteilung ops ↔ Operation | ops = Kunden + Kundeninstanzen / ops entfällt / ops = alles | ops = Kunden und Kundeninstanzen; Technik unserer Server in Operation | BESCHLOSSEN 13.11.2026 |
| L2 | Updates bei Kunden | eigener Update-Dienst / Komodo-Agent beim Kunden | eigener Update-Dienst im Suite-Paket, Heartbeat freiwillig | BESCHLOSSEN 13.11.2026 |
| L3 | Zustand unserer Server in ops | eigene Messung / Komodo-API lesen | Komodo-API nur lesend (Konto ohne Schreibrechte) | BESCHLOSSEN 13.11.2026 |
| L4 | Anmeldung der Instanz | nur Ident / Instanz-Token | Instanz-Token von ops; Ident optional für Instanzen bei uns | BESCHLOSSEN 13.11.2026 |
| L5 | Ringe | 2 / 3 Ringe | Ring 0 (wir), Ring 1 (Pilot ~5 %), Ring 2 (alle) | BESCHLOSSEN 13.11.2026 |
| L6 | Wann bauen? | jetzt / mit dem ersten selbst gehosteten Kunden | erst wenn es selbst gehostete Instanzen gibt; bis dahin genügt eine Kundenliste in Operation bzw. eine Tabelle | BESCHLOSSEN 13.11.2026 |

## 5. Umsetzung (Skizze)

- Laravel-Modul `ops` mit `eduksx/core`, Betriebsart `internal`, Anmeldung über Ident mit Rolle `ops:admin`, zweiter Faktor.
- Tabellen (Schema `ops`): `customers`, `contacts`, `contracts`, `installations` (Kunde, Modul, Ort: central /
  hosted / self_hosted, Version, Ring, Zeitfenster), `instance_tokens`, `heartbeats` (nur letzte 30 Tage), `jobs`,
  `releases` (Version, Freigabe je Ring).
- API S6 nach [spec/v1/ops-instances.openapi.json](../spec/v1/ops-instances.openapi.json).
- Datenschutz: nur Kontaktdaten der Verantwortlichen beim Kunden; Heartbeats ohne Personendaten (SP7).

## 6. Issues

| Issue | Inhalt | Status |
|---|---|---|
| #48 | Dieses Konzept | abgenommen 13.11.2026 |
| #40 | Selbst-Hosting mit Update-Dienst | abgenommen 13.11.2026 |
| (folgt) | Repo EduKSX-Ops | mit dem ersten selbst gehosteten Kunden (L6) |

## 7. Verlauf

- 13.11.2026: Konzeptabschluss – alle Entscheide ausser den vom PoC abhängigen beschlossen; eingefroren mit 0.3.0.
- 13.11.2026: Konzept angelegt; L1, L2 im Chat beschlossen.
