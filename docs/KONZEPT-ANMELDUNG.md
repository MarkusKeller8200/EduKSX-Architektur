# Konzept: Anmeldung – lokales Login als Standard, föderiert optional (0.4.0, #71 W11)

Stand: 22.11.2026 · Verantwortlich: Markus Keller · Status: **BESCHLOSSEN** 22.11.2026 (Entscheid W11 der
[Gesamtprüfung](GESAMTPRUEFUNG-0.4.0.md)), Werte mit **ZU PRÜFEN** sind Vorschläge.

Ändert [Plattform S1 und §6](KONZEPT-PLATTFORM.md) («Anmeldung nur über Ident» → lokales Login als Standard, Ident
optional) und verallgemeinert [Selbst-Hosting SH-E1](KONZEPT-SELBSTHOSTING.md). Grundlage ist die erprobte Anmeldung im
EduKSX-Glossary (`docs/KONZEPT-BENUTZER.md`, `App\Support\Totp`). Verbindlichkeit: Stufen nach
[KONZEPT-VORLAGE.md](KONZEPT-VORLAGE.md).

## 1. Ziel

Jedes Modul kann sich **ohne fremden Dienst** sicher anmelden lassen. Eine föderierte Anmeldung – EduKSX-Ident,
Microsoft Entra ID oder Google – ist eine **Option**. Ist sie eingeschaltet und geprüft, ersetzt sie das lokale Login
für die normalen Konten.

**Nichtziele:**
- kein eigener Identity-Provider in jedem Modul (Konten, Rollen und Organisationen über Module hinweg bleiben Aufgabe von Ident)
- keine Verknüpfung von Konten allein über die gleiche E-Mail-Adresse
- keine Passwortregeln mit Zeichenklassen, kein erzwungener Passwortwechsel

## 2. Anmeldearten und Umschalten

| Modus (`auth.mode`) | Wer meldet sich wie an | Wann |
| --- | --- | --- |
| `local` (Standard) | alle lokal (Passwort + zweiter Faktor nach Recht, Passkey) | ohne föderierten Anbieter |
| `federated` | normale Konten nur über den Anbieter; lokal nur die **Notfallkonten** | nach Einschalten und erfolgreicher Prüfung eines Anbieters |
| `mixed` (Ausnahme) | Organisationskonten über den Anbieter, **Externe mit Selbstregistrierung** lokal | nur Module mit öffentlicher Selbstregistrierung (z. B. Glossary-Community); im Datenmodell des Moduls begründet |

**Umschalten auf `federated`** (BESCHLOSSEN):

1. Admin trägt den Anbieter ein (Ident, Entra ID oder Google; OIDC, Code + PKCE, vertraulicher Client).
2. **Probeanmeldung:** Mindestens ein Konto mit Admin-Recht meldet sich erfolgreich über den Anbieter an und ist
   verknüpft. Ohne diesen Nachweis lässt sich der Modus nicht umschalten – Schutz vor Aussperren.
3. Ab dem Umschalten ist das lokale Login für normale Konten **gesperrt** (nicht gelöscht). Bestehende Konten werden bei
   der nächsten Anmeldung verknüpft: zuerst über den Anbieter, dann einmalig mit dem lokalen Passwort bestätigt;
   Schlüssel ist `issuer` + `subject` (DB B4).
4. Nach einer Übergangsfrist (Vorschlag 30 Tage, ZU PRÜFEN) werden nicht verknüpfte Konten deaktiviert und die
   Admin benachrichtigt.
5. Zurück auf `local` jederzeit durch eine Admin mit frischem zweitem Faktor; protokolliert.

**Notfallkonten (Break-Glass, BESCHLOSSEN):** Auch im Modus `federated` bleiben **zwei** lokale Notfallkonten, damit ein
Ausfall des Anbieters das Modul nicht sperrt. Sie verlangen Passkey oder TOTP, sind nicht für den Alltag gedacht, jede
Anmeldung erzeugt einen Eintrag im Sicherheitsprotokoll und eine Meldung an die Verantwortlichen. Angelegt bzw.
zurückgesetzt werden sie nur per Befehl auf dem Server.

## 3. Regeln für das lokale Login (BESCHLOSSEN, aus dem Glossary übernommen und ergänzt)

| Thema | Regel | Herkunft |
| --- | --- | --- |
| Passwortlänge | **mind. 15 Zeichen** für Konten ohne zweiten Faktor, **mind. 12 Zeichen** mit zweitem Faktor; höchstens ≥ 64 Zeichen zulassen; Unicode zählt je Zeichen | NIST SP 800-63B-4; Glossary (12) |
| Passwortinhalt | keine Zeichenklassen-Regeln, kein periodischer Wechsel; Abgleich mit einer Liste bekannter bzw. kompromittierter Passwörter (Liste offline in `eduksx/core`; Abfrage bei einem externen Dienst nur per Schalter, ZU PRÜFEN) | NIST SP 800-63B-4 |
| Speicherung | nur Hash (Argon2id, sonst bcrypt nach Laravel-Standard) | Glossary, DB B6 |
| Zweiter Faktor | TOTP nach RFC 6238, Geheimnis verschlüsselt; **Passkeys (WebAuthn)** zusätzlich; 8 einmalige Wiederherstellungscodes nur als Hash | Glossary; NIST (phishing-resistente Option) |
| Pflicht zum zweiten Faktor | nach **effektiven Rechten** (privilegiert = Pflicht), nicht abschaltbar über Rollen; vor der Bestätigung sind privilegierte Funktionen gesperrt | Glossary DEC-017, DB B4 |
| Schutz vor Angriffen | Begrenzung der Versuche je Konto und Adresse, generische Fehlertexte (kein Hinweis, ob ein Konto existiert), neue Sitzungs-ID nach Anmeldung, Cookies `Secure`, `HttpOnly`, `SameSite`, nur HTTPS | Glossary |
| Sitzung | Leerlauf höchstens 30 Min. in der Administration, 8 Std. sonst; absolut 12 Std. (ZU PRÜFEN) | neu |
| Heikle Aktionen | frischer zweiter Faktor (höchstens 15 Min. alt) für Rechte, Export, Löschen, Sicherheitseinstellungen | API C1 |
| Zurücksetzen | einmaliger, kurzlebiger Link (60 Min.), verrät nicht, ob ein Konto existiert; Zurücksetzen des zweiten Faktors nur per Befehl auf dem Server mit Audit-Eintrag | Glossary |
| Erste Admin | per Befehl auf dem Server, nie über die Website | Glossary |
| Selbstregistrierung | nur, wo das Modul sie braucht: Double-Opt-in, Spam-Schutz, Schalter «Registrierung offen» (Vorgabe aus) | Glossary |
| Protokoll | Anmeldung, Fehlversuche, Sperre, Zurücksetzen, Moduswechsel und Notfallkonto im Sicherheitsprotokoll (DB A7, Hash-Kette) | DB A7 |

## 4. Föderierte Anmeldung (BESCHLOSSEN)

- OIDC, Authorization Code mit PKCE, Prüfung von `state`, `nonce`, Signatur, Aussteller, Audience, Ablauf und Redirect-URI.
- Schlüssel des Kontos: `issuer` + `subject`; für Entra ergänzend `tid`/`oid`. Eine gleiche E-Mail-Adresse allein verknüpft nie.
- Einen zweiten Faktor des Anbieters erkennt das Modul nur an, wenn `acr`/`amr` ihn belegen und die Anerkennung für diesen Anbieter freigegeben ist; sonst verlangt das Modul seinen eigenen.
- **Ident** liefert zusätzlich Organisationen und Rollen (Claims S1); **Entra/Google** liefern nur die Identität – Rollen vergibt das Modul (bzw. Zuordnung über Gruppen oder Domäne).
- Abmelden: RP-initiated Logout; Back-Channel-Logout, wo der Anbieter ihn bietet (Ident: ja).

## 5. Umsetzung

- Baustein **«Anmeldung»** in `eduksx/core` (Core-Fahrplan, neu: nächste Minor nach 0.2; Quelle Glossary): lokale
  Konten, TOTP, Passkeys, Wiederherstellungscodes, Notfallkonten, Modusschalter, OIDC-Client für Ident/Entra/Google.
- Einstellungen `auth.mode`, `auth.providers`, `auth.registration`; Umschalten nur mit Probeanmeldung (2).
- Mehrere Module ohne föderierten Anbieter: ein Konto je Modul (Selbst-Hosting 4.3); gemeinsames Konto über einen Anbieter.
- Tests: Aussperr-Schutz (Umschalten ohne Probeanmeldung scheitert), Notfallkonto bei Ausfall des Anbieters, keine
  Verknüpfung über E-Mail, Passwortregeln, MFA-Pflicht nach Recht.

## 6. Entscheide

| Nr. | Frage | Entscheid | Status |
| --- | --- | --- | --- |
| AN1 | Standard-Anmeldung | lokales Login in jedem Modul; Ident, Entra ID, Google optional | BESCHLOSSEN 22.11.2026 |
| AN2 | Lokales Login bei aktivem Anbieter | für normale Konten gesperrt nach erfolgreicher Probeanmeldung; zwei Notfallkonten bleiben | BESCHLOSSEN 22.11.2026 |
| AN3 | Regeln lokales Login | Tabelle 3 (Glossary plus NIST SP 800-63B-4) | BESCHLOSSEN 22.11.2026 |
| AN4 | Externe mit Selbstregistrierung | Modus `mixed` als begründete Ausnahme je Modul | BESCHLOSSEN 22.11.2026 |
| AN5 | Übergangsfrist, Sitzungsdauer, externe Passwortprüfung | Werte in 2 und 3 | ZU PRÜFEN |

## 7. Quellen

- NIST SP 800-63B-4 (Juli 2025), Passwörter und Authentifikatoren: <https://pages.nist.gov/800-63-4/sp800-63b/authenticators>
- EduKSX-Glossary: `docs/KONZEPT-BENUTZER.md` (DEC-017), `docs/KONZEPT-STACK.md`

## 8. Verlauf

- 22.11.2026: Angelegt nach Entscheid W11 (Gesamtprüfung 0.4.0).
