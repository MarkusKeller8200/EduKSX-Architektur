# Konzept: Selbst-Hosting mit dem Suite-Paket (#40)

Stand: 13.11.2026 (Meilenstein 0.3.0) · Verantwortlich: Markus Keller · Status: **IN ARBEIT** – Grundsätze SH-E1–SH-E9
BESCHLOSSEN im Chat 13.11.2026; Details EMPFOHLEN.

**Leitsatz (Chat 13.11.2026):** Selbst-Hosting darf nicht kompliziert sein, sonst nutzt es niemand.

Grundlagen: [Plattform](KONZEPT-PLATTFORM.md) §2, §6, S1 (Ausnahme Selbst-Hosting), [Leitstand](KONZEPT-LEITSTAND.md),
Selbst-Hosting des Glossary (EduKSX-Glossary `docs/KONZEPT-UPDATES.md` DEC-027, `docs/SELBST-HOSTEN.md`) – dessen
bewährtes Muster wird für alle Module verallgemeinert.

## 1. Ziel

Eine Schule oder Gemeinde betreibt die gewünschten EduKSX-Module auf **einem eigenen Server**, installiert in unter
15 Minuten von einer Person ohne Docker-Kenntnisse, und hält sie mit wenig Aufwand aktuell und gesichert.

**Nichtziele:**
- keine Betriebswerkzeuge von MarKusSX-Operation beim Kunden (Komodo, Headscale, 1Password …)
- kein Ident vor Ort, kein Edulog (Plattform S1, Ausnahme)
- keine Variante ohne Docker (Glossary DEC-027, Entscheid 4)
- kein Kubernetes

## 2. Ablauf aus Sicht der Schule

1. **Server bereitstellen:** Linux-VM mit Docker (Ubuntu 24.04/26.04, Debian 12/13; amd64, arm64 ZU PRÜFEN) **oder**
   die fertige **VM-Vorlage** importieren (VMware, Hyper-V, Proxmox).
2. **Installieren:** `curl -fsSLO …/install.sh && less install.sh && sudo sh install.sh` bzw. in der VM-Vorlage
   automatisch beim ersten Start. Der Installer fragt nur: Adresse (Domain), Admin-E-Mail, Module, optional
   Proxy des Schulnetzes und Sicherungsziel. Geheimnisse erzeugt er selbst.
3. **Erster Login:** im Browser, zweiten Faktor einrichten; optional M365/Entra oder Google anbinden.
4. **Fertig:** Startseite «System» zeigt Module, Versionen, Zustand (`/health` aller Module), Sicherung und Updates.

## 3. Entscheide

| Nr. | Frage | Entscheid | Status |
|---|---|---|---|
| SH-E1 | Anmeldung | im Modul: lokale Konten mit zweitem Faktor (TOTP/Passkey), optional Entra/Google per OIDC; kein Ident, kein Edulog | BESCHLOSSEN 13.11.2026 |
| SH-E2 | Installation | Installer mit einem Befehl **und** VM-Vorlage | BESCHLOSSEN 13.11.2026 |
| SH-E3 | Ort des Pakets | neues Repo **EduKSX-Suite**: Installer, Compose-Grundgerüst, Update-Dienst, VM-Vorlage; Module liefern Image und Compose-Baustein | BESCHLOSSEN 13.11.2026 |
| SH-E4 | Datenbank | **SQLite je Modul** als Standard (eine Schule); **PostgreSQL optional** (ein Container, Schema je Modul) für Schulgemeinden | BESCHLOSSEN 13.11.2026 |
| SH-E5 | Updates | eigener **Update-Dienst** (Glossary U3–U9); **nur Korrekturen automatisch** im Zeitfenster, neue Funktionen auf Knopfdruck, nie automatisch über eine Hauptversion | BESCHLOSSEN 13.11.2026 |
| SH-E6 | Sicherung | **täglich und vor jedem Update**, verschlüsselt mit restic (lokal, NAS oder S3 in der Schweiz), monatlicher Wiederherstellungstest; laufende Sicherung (Litestream bzw. WAL) als Schalter | BESCHLOSSEN 13.11.2026 |
| SH-E7 | Verantwortung für RPO/RTO | beim Kunden; die Werte des DB-Standards C2 gelten für unseren Betrieb, beim Selbst-Hosting sind sie Empfehlung | BESCHLOSSEN 13.11.2026 |
| SH-E8 | Meldung an den Leitstand | Heartbeat freiwillig (Opt-in beim Installieren), ohne Personendaten (S6) | BESCHLOSSEN 13.11.2026 (L2) |
| SH-E9 | Reverse Proxy | Caddy mit automatischem HTTPS (wie Glossary und Operation); Alternative «hinter vorhandenem Proxy» | EMPFOHLEN |
| SH-E10 | Suite-Version | eine Versionsnummer je Paket (z. B. `2026.11`), die alle Module mit Digest festlegt; Module einzeln aktualisierbar nur innerhalb der Korrekturen | EMPFOHLEN |
| SH-E11 | VM-Vorlage | Ubuntu LTS, gebaut mit Packer in der CI; Formate OVA (VMware), VHDX (Hyper-V), qcow2 (Proxmox); erster Start fragt im Browser statt in der Konsole | EMPFOHLEN |
| SH-E12 | Inhalte zentraler Module | Glossary und Codex müssen nicht selbst gehostet werden: lokale Module binden sie über Plugins aus dem zentralen Dienst ein ([Plugins](KONZEPT-PLUGINS.md)); ein selbst gehostetes Glossary gleicht Begriffe ab (Glossary U11) | EMPFOHLEN |

## 4. Umsetzung

### 4.1 Aufbau einer Installation

```text
/opt/eduksx
 ├─ .env                 Adresse, Module, Zeitfenster, Sicherungsziel (Geheimnisse vom Installer erzeugt)
 ├─ compose.yaml         Grundgerüst: Caddy, Update-Dienst, Sicherung
 ├─ modules/<modul>.yaml Baustein je Modul (aus dem Modul-Repo, Image mit Digest)
 └─ data/<modul>/        Daten, SQLite-Datei bzw. Speicher je Modul
```

- Module per Schalter (`EDUKSX_MODULES=intranet,timetable`); dazuschalten = Installer erneut, nichts geht verloren.
- Jedes Modul: Rollen web/worker/scheduler im selben Image (Plattform §6), `/up`, `/health`, Steckbrief (S5).

### 4.2 Update-Dienst

Verallgemeinert aus dem Glossary (DEC-027): eigener Container mit eingeschränktem Docker-Zugriff (nur eigene
Container), Aufträge über Dateien im gemeinsamen Volume bzw. über den Leitstand (S6). Ablauf: Image mit Digest und
Signatur prüfen → Wartungsmodus → Sicherung → Austausch → `/health` → bei Fehler zurück samt Datenbank → Protokoll und
Mail. Die Module selbst haben nie Docker-Zugriff.

### 4.3 Anmeldung (SH-E1)

Baustein in `eduksx/core` (Core-Fahrplan «mit #40»): lokale Konten, TOTP/Passkey, Wiederherstellungscodes,
Notfallkonto; OIDC-Client für Entra und Google mit Zuordnung über Gruppen bzw. Domäne. Bei mehreren Modulen gibt es
mit lokalen Konten **ein Konto je Modul**; eine gemeinsame Anmeldung nur über Entra/Google (ZU PRÜFEN: gemeinsames
Konto über ein kleines «Konto-Modul» der Suite – erst bei Bedarf).

### 4.4 Mindestanforderungen (Schätzung, in der Probe messen)

| Fall | Server (VM) | Speicher |
|---|---|---|
| eine Schule, 1–2 Module, SQLite | 2 vCPU, 4 GB RAM | 50 GB SSD |
| Schulgemeinde, alle Module, ~2000 Personen, PostgreSQL | 4–8 vCPU, 16 GB RAM | 200 GB SSD |

Rundherum: DNS-Name und Port 443 (für Zugriff von zuhause: DMZ bzw. Reverse Proxy der Gemeinde), Port 80 für das
Zertifikat oder eigenes Zertifikat, ausgehend HTTPS (Registry, optional Leitstand) und SMTP, Sicherungsziel ausserhalb
der VM.

### 4.5 Tests

- CI im Repo EduKSX-Suite: frische VM, Installer mit Antwortdatei, alle Module grün; Update auf die nächste Version
  und Rücksprung; Wiederherstellung aus der Sicherung.
- Probe mit einer Person ohne Docker-Kenntnisse (Testliste #40).

## 5. Issues

| Issue | Inhalt | Status |
|---|---|---|
| #40 | Dieses Konzept | `_2 in Arbeit` |
| #48 | Leitstand, Update-Ringe, Heartbeat | `_2 in Arbeit` |
| (folgt) | Repo EduKSX-Suite anlegen (Projektverantwortliche:r), Installer und Update-Dienst aus dem Glossary übernehmen | nach Abnahme |
| (folgt, EduKSX-Core) | lokale Anmeldung mit zweitem Faktor, OIDC Entra/Google | mit dem ersten Modul, das selbst gehostet wird |

## 6. Verlauf

- 13.11.2026: Konzept angelegt; SH-E1–SH-E8 im Chat beschlossen.
