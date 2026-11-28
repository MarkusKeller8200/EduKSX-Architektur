# Datenmodell als Text (DBML)

**Status:** ENTWURF, nicht freigegeben (#124). Beschreibung und offene Widersprüche:
[ENTWURF-DATENMODELL.md](../ENTWURF-DATENMODELL.md).

| Datei | Inhalt |
| --- | --- |
| [`kontakt-kern.dbml`](kontakt-kern.dbml) | Kontakt, Verwendung, Verbund, Beziehung; Stammdaten der Person (People); Referenzdaten. 29 Tabellen, 15 Enums. |

## Arbeitsweise

1. **Die DBML-Datei in diesem Ordner ist die Quelle.** Geändert wird hier, per Branch und Pull Request.
2. **drawDB ist Ansicht und Editor:** Datei über «Import › DBML» öffnen, zeichnen, wieder als DBML exportieren und die
   Datei hier ersetzen. Ein Stand, der nur im Browser liegt, gilt nicht.
3. **Ansichten ausserhalb des Repositories** (Whiteboards, Bildschirmfotos) sind Abbilder. Weichen sie ab, gilt die Datei.
4. **Sobald ein Modul gebaut ist, gelten dessen Migrationen.** Die DBML-Datei wird dann nachgeführt.

## Prüfen

```bash
npx --package=@dbml/cli dbml2sql docs/datenmodell/kontakt-kern.dbml --postgres
```

Der Befehl meldet Syntaxfehler und erzeugt zur Kontrolle ein SQL-Skript. Er ist nicht Teil der CI.

## Regeln

- Namen, Schlüssel, Datentypen und Enums nach [KONZEPT-DB-GUIDELINE.md](../KONZEPT-DB-GUIDELINE.md) (A1, A3, A4).
- Jedes Feld trägt in der Notiz seine Datenklasse nach B2, jede Tabelle Bereich und Datenart.
- Die Pflichtspalten nach A3a sind in der Datei nicht ausgeschrieben; sie gelten für jede Tabelle.
- Nur erfundene Beispiele; keine echten Personendaten.

## Werkzeug

drawDB (im Browser, selbst betreibbar; Lizenz laut Hersteller-Repository AGPL-3.0, vor dem Einsatz dort prüfen). Es läuft
nur beim Entwerfen und wird nicht Teil von EduKSX; sein Quellcode gehört nicht in dieses Repository.
