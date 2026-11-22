# Entwickler-Stack EduKSX-Glossary

Stand 22.11.2026 (Glossary 0.18.0-beta.1 plus Merges bis #497). Reine Übersicht, keine Konzeptänderung; massgebend
sind die Dokumente im Repo [EduKSX-Glossary](https://github.com/MarkusKeller8200/EduKSX-Glossary) (`DEPLOY.md`,
`docs/KONZEPT-DEPLOYMENT.md`) und für den Betrieb [MarKusSX-Operation](https://github.com/MarkusKeller8200/markussx-operation).
Als bearbeitbares Whiteboard: [Entwickler-Stack EduKSX-Glossary](https://claude.ai/artifact/7rRR1wivpJYFbrAzQg1Bjw)
(claude.ai, privat bis zum Teilen).

## Anwendung

Fünf Zugänge greifen auf dieselbe Laravel-App zu.

```mermaid
flowchart TB
    subgraph Zugaenge["Zugänge"]
        direction LR
        WEB["Website<br/>Inertia React"]
        EXT["Browser-Erweiterung<br/>Chrome MV3"]
        EMB["Einbindung<br/>JS 1.1.1"]
        KI["KI-Assistent<br/>MCP /mcp"]
        API["API-Client<br/>REST /api/v1"]
    end

    subgraph App["Laravel 13 · PHP 8.4 · Docker"]
        direction LR
        R1["Web + Inertia<br/>Seiten, Administration"]
        R2["API v1 · Sync<br/>Token, Scopes"]
        R3["MCP-Server<br/>laravel/mcp"]
        CORE["eduksx/core<br/>Schema, Sicherheit"]
        S1["Glossary-Dienst<br/>Abbilder, Revisionen"]
        S2["Öffentlich<br/>Index, Cache, Export"]
        S3["Einstellungen<br/>Schalter, env-Sperre"]
        S4["Statistik<br/>Tageszähler ohne Cookies"]
    end

    DB[("SQLite / PostgreSQL<br/>Begriffe, Konten, Zähler")]
    BAK["Litestream / Backrest<br/>laufende Sicherung"]

    WEB --> R1
    EXT --> R2
    EMB --> R2
    KI --> R3
    API --> R2
    App --> DB
    DB --> BAK
```

| Teil              | Inhalt                                                                                         |
| ----------------- | ---------------------------------------------------------------------------------------------- |
| Website           | Inertia mit React und TypeScript, öffentliche Seiten und Administration                        |
| Erweiterung       | Browser-Erweiterung (Manifest V3), lädt den Index einmal täglich, Melden von Kandidaten         |
| Einbindung        | Paket `glossary-highlighter` (Einbindung und Web-Komponenten 1.1.1)                            |
| MCP               | `laravel/mcp` 1.2.1, Streamable HTTP unter `/mcp`, nur lesend (Phase 1)                         |
| API               | REST `/api/v1` (öffentlich, Servicekonten mit Scopes), interner Sync unter `/api/sync`          |
| eduksx/core       | gemeinsames Paket der Produktfamilie: Schema-Härtung, Fehlerformat, Sicherheits-Header         |
| Daten             | SQLite zu Beginn, PostgreSQL in der CI und später auf prod; Sicherung mit Litestream/Backrest  |

## Auslieferung

Jeder Merge erzeugt ein Image; welche Umgebung es übernimmt, entscheidet der Image-Tag.

```mermaid
flowchart LR
    GH["GitHub<br/>PR, Squash-Merge, Tags"] --> CI["CI<br/>phpunit (SQLite, PostgreSQL),<br/>phpstan, pint, vp, tsc"]
    CI --> IMG["GHCR<br/>Docker-Image"]

    IMG -- ":main" --> DEV["dev<br/>Hostinger<br/>glossary-dev.markussx.ch"]
    IMG -- ":beta" --> TEST["test<br/>test-01 (Infomaniak)<br/>glossary-test.eduksx.ch"]
    IMG -- ":stable" --> PROD["prod<br/>prod-01 (Infomaniak)<br/>glossary.eduksx.ch"]

    SSH["SSH aus GitHub<br/>jeder Merge"] -.-> DEV
    KOM["Komodo + Caddy (VPN)<br/>test stündlich<br/>prod So 03:05, wenn test grün"] -.-> TEST
    KOM -.-> PROD
```

- **Beta** (`X.Y.Z-beta.N`) setzt `:beta` → test. **Release** (`X.Y.Z`) setzt zusätzlich `:stable` → prod im
  nächsten Wartungsfenster.
- Der **Entwicklungs-Sync** (dev ↔ test/prod) läuft über die App selbst (`/api/sync`, Administration › System ›
  Sync), nicht über die Auslieferung.
