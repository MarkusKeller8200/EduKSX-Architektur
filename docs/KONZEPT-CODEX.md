# Konzept: Codex – systematische Rechtssammlung (#119)

Stand: 26.11.2026 · Verantwortlich: Markus Keller · Status: **BESCHLOSSEN** 26.11.2026 (CX1–CX8), **ZU PRÜFEN**:
Funktionsliste §2 · Verbindlichkeit: Stufen nach [KONZEPT-VORLAGE.md](KONZEPT-VORLAGE.md).

Ergänzt den Abschnitt `codex` der [Modulübersicht](MODULE-UEBERSICHT.md). Grundlagen:
[Anmeldung](KONZEPT-ANMELDUNG.md), [Design](KONZEPT-DESIGN.md) (DS4, Ausnahme DS14), [Plugins](KONZEPT-PLUGINS.md) (P2, P7),
[Datenschutz ZH](KONZEPT-DATENSCHUTZ-ZH.md) (Cloudflare nur öffentliche Inhalte, «anbieten, dann löschen»).

## 1. Ziel

Codex ist die **systematische Rechtssammlung** von Schul- und politischen Gemeinden: Erlasse und Reglemente mit
Systematik, Versionen und Gültigkeit, öffentlich publiziert. Jede Gemeinde kann Codex als **ihre eigene Rechtssammlung**
nutzen und auf ihrer Homepage einbinden. Später erlaubt Codex die **Gegenüberstellung** mehrerer Gemeinden.

**Mandant** ist die einzelne Schul- oder politische Gemeinde (Organisation nach [Rollen](KONZEPT-ROLLEN.md)).

**Nichtziele:** keine Unterschriften (→ `sign`), keine allgemeine Dokumentablage (→ `intranet`), keine
Vernehmlassungs- oder Genehmigungsabläufe (→ `flow`).

## 2. Öffentlichkeit (CX1 BESCHLOSSEN, Funktionsliste ZU PRÜFEN)

Codex ist **öffentlich wie das Glossary**: Lesen braucht keine Anmeldung. Welche Funktion öffentlich ist, wird vor der
Umsetzung im Repo EduKSX-Codex noch einmal geprüft. Vorschlag (**EMPFOHLEN**):

| Öffentlich, ohne Anmeldung | Mit Anmeldung (Rolle nach [Rollen](KONZEPT-ROLLEN.md)) |
| --- | --- |
| Rechtssammlung einer Gemeinde lesen, durchsuchen, nach Systematik blättern | Erlasse erfassen, bearbeiten, Versionen anlegen (`editor`) |
| aktuelle und frühere Fassungen, Gültigkeit, Änderungsverlauf | Fassung freigeben und publizieren (`admin` der Gemeinde) |
| Gegenüberstellung mehrerer Gemeinden | Muster-Einträge zuordnen oder deaktivieren (§5) |
| Einbettung auf der Gemeinde-Homepage, lesende API (§4) | CSS und Template für die Einbettung pflegen (§4.2) |
| PDF/Druck einer Fassung | Mandanten, Rollen, Einstellungen (`admin`) |

Öffentliche Inhalte dürfen über Cloudflare ausgeliefert werden ([Datenschutz ZH](KONZEPT-DATENSCHUTZ-ZH.md)); Konten
und Entwürfe nicht.

## 3. Anmeldung (CX2 BESCHLOSSEN)

**Identisch wie Glossary:** lokales Login als Standard (Passwort plus zweiter Faktor bzw. Passkey), Anbindung an
EduKSX-Ident optional; Entra ID und Google wie in allen Modulen ebenfalls optional. Regeln, Notfallkonten und
Umschalten nach [KONZEPT-ANMELDUNG.md](KONZEPT-ANMELDUNG.md) (AN1–AN5), umgesetzt mit dem Baustein «Anmeldung» aus
`eduksx/core`. Eine öffentliche Selbstregistrierung gibt es in Codex nicht (kein Modus `mixed`).

## 4. Einbindung bei der Gemeinde

### 4.1 Drei Wege (CX3 BESCHLOSSEN)

| Weg | Für wen | Eigenschaften |
| --- | --- | --- |
| **JS-Baustein** (Standard) | Homepages, die ein Script erlauben | ein `<script>`-Tag plus Element `<eduksx-codex gemeinde="…">` (Web Component mit Shadow DOM, wie im [Plugin-Konzept](KONZEPT-PLUGINS.md)); Tiefenlinks auf einzelne Erlasse über die Adresse der Homepage; Inhalte für Suchmaschinen über die öffentliche Codex-Seite mit `canonical` |
| **iFrame** (Rückfall) | CMS ohne eigene Scripts | eine Adresse je Gemeinde, Höhe passt sich per `postMessage` an; Optik über das CSS der Gemeinde (§4.2) |
| **Öffentliche API** | Gemeinden bzw. Webdienstleister, die selbst darstellen | lesend, ohne Anmeldung, nach [API-Guideline](KONZEPT-API-GUIDELINE.md) (`/codex/v1`, OpenAPI); Ratenbegrenzung; nur publizierte Fassungen |

Für den JS-Baustein gelten die Sicherheitsregeln aus [Plugins](KONZEPT-PLUGINS.md) P6 sinngemäss (Script nur vom
Codex-Host, feste Version im Pfad bzw. Subresource Integrity). Der iFrame ist hier – anders als bei Plugins in
unseren Modulen (P4) – als Rückfall für fremde Homepages erlaubt, weil er nur öffentliche Inhalte ohne Anmeldung zeigt.

Die Einbettung zeigt nur **publizierte** Inhalte. Die Bearbeitung findet immer in Codex selbst statt, nie in der
Einbettung.

### 4.2 Eigenes CSS je Gemeinde (CX4 BESCHLOSSEN, Ausnahme zu DS4)

- Jede Gemeinde kann für **die eingebettete Rechtssammlung** eigenes CSS hinterlegen, damit sie wie ihre Homepage aussieht.
- Für weniger Versierte erstellen wir ein **CSS-Template nach dem Vorbild der Homepage** der Gemeinde (Farben,
  Schrift, Abstände); die Gemeinde übernimmt es oder passt es an.
- **Geltungsbereich:** nur die Einbettung (JS-Baustein im Shadow DOM, iFrame). Codex selbst, seine öffentliche Seite
  und die Administration folgen weiterhin **DS4** (ganzes Theme über bekannte Tokens, Kontrastprüfung) – festgehalten
  als **DS14** im [Design-Konzept](KONZEPT-DESIGN.md).
- **Prüfung beim Speichern (Pflicht):** kein `@import`, keine `url()` auf fremde Adressen (Schriften und Bilder nur
  von der Homepage-Domain der Gemeinde oder aus Codex), kein `expression`/`behavior`, Grössenbeschränkung; das CSS
  wirkt nur innerhalb des Bausteins.
- **Barrierefreiheit:** Codex führt beim Speichern eine Kontrastprüfung durch und **warnt**; die Verantwortung für das
  eigene CSS liegt bei der Gemeinde. Struktur, Überschriften und Tastaturbedienung liefert der Baustein unverändert.

## 5. Mustersystematik (CX5–CX8 BESCHLOSSEN)

- **Vorschlag (CX5):** Sind alle Gemeinden aufgenommen, stellen wir einen **Vorschlag für Nummerierung und Namen** der
  Dokumente vor (Mustersystematik). Gepflegt wird er zentral von EduKSX. Die Nutzung ist **optional**.
- **Liste je Gemeinde (CX6):** Die Gemeinde geht die Liste der Muster-Einträge durch und entscheidet je Eintrag, ob sie
  das Dokument hat. Hat sie es nicht, **deaktiviert** sie den Eintrag.
- **Zuordnen statt umbenennen (CX7):** Die Gemeinde ordnet ihre Erlasse den Muster-Einträgen zu. Ihre **eigene Nummer
  und Bezeichnung bleiben** – oder sie übernimmt die des Musters. Die Zuordnung ist die Grundlage für die
  Gegenüberstellung.
- **Deaktiviert im Vergleich (CX8):** In der eigenen Rechtssammlung ist ein deaktivierter Eintrag unsichtbar. In der
  Gegenüberstellung erscheint die Gemeinde mit **«kein Erlass»** – das ist selbst eine Aussage.
- Ändert sich die Mustersystematik, bleibt jede Zuordnung erhalten; neue Einträge erscheinen der Gemeinde als
  «noch nicht entschieden».

## 6. Daten und Aufbewahrung

- Personendaten: wenig (Konten der Bearbeitenden, Namen in Erlassen nur, wo sie zum Rechtstext gehören).
- Fassungen werden nicht gelöscht, sondern ausser Kraft gesetzt; der Verlauf bleibt öffentlich.
- Beim Vertragsende gilt «anbieten, dann löschen» mit Export PDF/A plus CSV ([Datenschutz ZH](KONZEPT-DATENSCHUTZ-ZH.md)).

## 7. Entscheide

| Nr. | Frage | Entscheid | Status |
| --- | --- | --- | --- |
| CX1 | Öffentlichkeit | öffentlich lesbar wie Glossary; Funktionsliste §2 vor der Umsetzung prüfen | BESCHLOSSEN 26.11.2026, Liste ZU PRÜFEN |
| CX2 | Anmeldung | wie Glossary: lokales Login Standard, Ident optional (AN1–AN5), keine Selbstregistrierung | BESCHLOSSEN 26.11.2026 |
| CX3 | Einbindung | JS-Baustein (Standard), iFrame (Rückfall) und öffentliche lesende API | BESCHLOSSEN 26.11.2026 |
| CX4 | Eigenes CSS | je Gemeinde, nur für die Einbettung, geprüft beim Speichern; Template nach Homepage; Ausnahme DS14 zu DS4 | BESCHLOSSEN 26.11.2026 |
| CX5 | Mustersystematik | Vorschlag für Nummerierung und Namen, sobald alle Gemeinden aufgenommen sind; optional | BESCHLOSSEN 26.11.2026 |
| CX6 | Liste je Gemeinde | Gemeinde entscheidet je Muster-Eintrag; nicht vorhanden → deaktivieren | BESCHLOSSEN 26.11.2026 |
| CX7 | Eigene Dokumente | Zuordnung zum Muster; eigene Nummer und Bezeichnung bleiben oder Muster übernehmen | BESCHLOSSEN 26.11.2026 |
| CX8 | Deaktiviert im Vergleich | eigene Sammlung: unsichtbar; Gegenüberstellung: «kein Erlass» | BESCHLOSSEN 26.11.2026 |

## 8. Verlauf

- 26.11.2026: Angelegt (#119) mit den Vorgaben von Markus Keller; CX1–CX8 im Chat entschieden.
