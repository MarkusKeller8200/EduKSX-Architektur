# Prüfauftrag: An den Absender gebundene Tokens – DPoP oder mTLS (#16)

Stand: 13.11.2026 · Verantwortlich: Markus Keller · Status: **ZU PRÜFEN** – Recherche abgeschlossen, Empfehlung
liegt vor; entschieden wird nach Schritt P8 des Ident-PoC ([KONZEPT-IDENT.md](KONZEPT-IDENT.md) §4).

Betrifft [API-Standard C1](KONZEPT-API-GUIDELINE.md) («DPoP/mTLS für Dienst-zu-Dienst: ZU PRÜFEN») und Plattform S2/S6.

## 1. Frage

Sollen Zugriffstokens für Dienst-zu-Dienst-Aufrufe mit Personendaten (S2, z. B. Intranet → Glossary, Leitstand →
Instanz) an den Absender gebunden sein, damit ein abgefangenes Token allein nichts nützt (RFC 9700, Security
Guideline des Bundes 3.1)? Wenn ja: DPoP (RFC 9449) oder mTLS (RFC 8705)?

## 2. Varianten

| | A · Bearer, kurz und eng | B · DPoP (RFC 9449) | C · mTLS (RFC 8705) |
|---|---|---|---|
| Schutz bei gestohlenem Token | bis Ablauf nutzbar (≤ 10 Min.), nur für ein `aud` und wenige Scopes | ohne privaten Schlüssel wertlos | ohne Zertifikat und Schlüssel wertlos |
| Anmeldung des Clients | `private_key_jwt` statt Secret | dazu Schlüsselpaar je Client für Proofs | Zertifikat je Client, PKI nötig |
| Infrastruktur | keine | keine; Replay-Speicher (`jti`) im Modul, z. B. Redis | TLS muss bis zum Modul durchgehen bzw. der Proxy reicht das Zertifikat sicher weiter; schwierig hinter einem CDN (Plattform 7.3) |
| Ident: Zitadel | unterstützt | in der Dokumentation nicht gefunden – **ZU PRÜFEN** im PoC | nicht gefunden – **ZU PRÜFEN** |
| Ident: Keycloak (Plan B) | unterstützt | seit 26.4 offiziell unterstützt, alle Grants | unterstützt |
| Laravel (Modul als Empfänger) | Core 0.2: JWT-Prüfung über JWKS | eigener Baustein in Core; Pakete der Gemeinschaft vorhanden, aber jung (Pflege und Lizenz prüfen) | Proxy-Konfiguration plus Prüfung des Fingerabdrucks `x5t#S256` |
| Aufwand für Abnehmer (Intranet, Leitstand) | klein | mittel: Proof je Aufruf signieren | mittel bis hoch: Zertifikate ausrollen und erneuern |

## 3. Empfehlung

1. **Ab Stufe 1 Pflicht (Variante A):** JWT-Zugriffstokens höchstens 10 Minuten, `aud` = Ziel-Modul, enge Scopes,
   Client-Anmeldung mit `private_key_jwt`; keine statischen Secrets für S2. Das steht bereits in API C1 und wird nur
   um `private_key_jwt` ergänzt. EMPFOHLEN.
2. **DPoP vor mTLS:** DPoP braucht keine PKI und funktioniert hinter Proxy und CDN. Pflicht für Servicekonten mit
   Daten der Klasse «personenbezogen» oder höher, **sobald Ident es anbietet**; der Prüf-Baustein kommt dann in
   `eduksx/core` (Gruppe «Integration», API G3). EMPFOHLEN.
3. **mTLS nur für S6** (Leitstand ↔ isolierte Instanz) als Option, wo eine Instanz beim Kunden läuft und ein
   Zertifikat ohnehin ausgerollt wird (Plattform S6 nennt mTLS bereits). EMPFOHLEN.
4. **Bietet Zitadel kein DPoP:** Variante A bleibt; DPoP wird als Anforderung an Ident festgehalten und mit jeder neuen
   Zitadel-Hauptversion geprüft. Kein Grund für Plan B allein deswegen (KONZEPT-IDENT §4.2).

## 4. Offene Prüfpunkte

- [ ] PoC P8: Zitadel-Version auf DPoP und `private_key_jwt` für Client Credentials prüfen
- [ ] DPoP-Baustein: Paket wählen oder selbst auf `web-token/jwt-library` aufbauen; Lizenz, Pflege, Prüfung von
      `htm`, `htu`, `iat`, `jti`, `ath` und Nonce
- [ ] Entscheid in API C1 und in der Entscheidtabelle des API-Standards nachführen

## 5. Quellen (Stand 13.11.2026)

- RFC 9449 (DPoP) <https://datatracker.ietf.org/doc/rfc9449/>, RFC 8705 (mTLS), RFC 9700 (OAuth 2.0 Security BCP)
- Keycloak 26.4: DPoP offiziell unterstützt <https://www.keycloak.org/2025/10/dpop-support-26-4>
- Zitadel empfiehlt gebundene Tokens selbst, ohne eigene Unterstützung zu nennen <https://zitadel.com/blog/ai-agent-impersonation>
- Laravel-Pakete (zu prüfen): <https://packagist.org/packages/labrodev/laravel-dpop>,
  <https://packagist.org/packages/guillaumetissier/resource-guard>

## 6. Verlauf

- 13.11.2026: Recherche und Empfehlung; Entscheid nach PoC P8.
