<?php
/**
 * PoC P5 mit Login V2 (#36): Ident-Brücke für die Antwort von RetrieveIdentityProviderIntent (Actions v2, Response).
 * Bildet die Edulog-Attribute (Leitfaden 1.2.1) auf das neue Konto ab und verweigert Lernende und leere Rolle.
 * Start: SIGNING_KEY=… php -S 0.0.0.0:8096 bridge_intent.php
 */
$body = file_get_contents('php://input');
parse_str(str_replace(',', '&', $_SERVER['HTTP_ZITADEL_SIGNATURE'] ?? ''), $sig);
$ok = isset($sig['v1'], $sig['t']) && abs(time() - (int) $sig['t']) <= 300
    && hash_equals(hash_hmac('sha256', $sig['t'].'.'.$body, (string) getenv('SIGNING_KEY')), $sig['v1']);
if (! $ok) { http_response_code(401); exit; }
$in = json_decode($body, true);
file_put_contents(__DIR__.'/bridge-intent-request.json', json_encode($in, JSON_PRETTY_PRINT));
$resp = $in['response'] ?? [];
$attrs = $resp['idpInformation']['rawInformation']['attributes'] ?? $resp['idpInformation']['rawInformation'] ?? [];
$werte = function (string $n) use ($attrs): array {
    $v = $attrs[$n] ?? [];
    $v = is_array($v) ? $v : [$v];
    $out = [];
    foreach ($v as $x) { foreach (explode('##', (string) $x) as $y) { if (trim($y) !== '') { $out[] = trim($y); } } }
    return $out;
};
$eins = fn (string $n): string => $werte($n)[0] ?? '';
$rollen = $werte('EdulogPersonRole');
if (! array_intersect($rollen, ['teacher', 'administration', 'principal', 'technician'])) {
    http_response_code(403);   // Zitadel bricht ab (interruptOnError): kein Konto für Lernende und unbekannte Rolle
    exit;
}
// Antwort als Objekte weiterreichen (leere Objekte bleiben {} – sonst lehnt Zitadel das Protobuf-JSON ab)
$out = json_decode($body)->response;
$profil = (object) ['givenName' => $eins('givenName'), 'familyName' => $eins('sn'),
    'displayName' => $eins('givenName').' '.$eins('sn'), 'preferredLanguage' => substr($eins('preferredLanguage') ?: 'de', 0, 2)];
$mail = (object) ['email' => $eins('mail'), 'isVerified' => true];
$meta = array_map(fn ($k, $v) => (object) ['key' => $k, 'value' => base64_encode(json_encode($v))],
    ['edulog_techid', 'edulog_roles', 'edulog_orgs', 'edulog_canton'],
    [$eins('EdulogPersonTechID'), $rollen, $werte('o'), $eins('EdulogPersonCanton')]);
// Anzeigename der Verknüpfung (Pflichtfeld): die Kennung im Kantons-IdP (uid), sonst die E-Mail
foreach ([$out->addHumanUser->idpLinks ?? [], $out->createUser->human->idpLinks ?? []] as $links) {
    foreach ($links as $link) { $link->userName = $eins('uid') ?: $eins('mail'); }
}
if (isset($out->addHumanUser)) {
    $out->addHumanUser->username = $eins('mail');
    $out->addHumanUser->profile = $profil;
    $out->addHumanUser->email = $mail;
    $out->addHumanUser->metadata = $meta;
}
if (isset($out->createUser->human)) {
    $out->createUser->username = $eins('mail');
    $out->createUser->human->profile = $profil;
    $out->createUser->human->email = $mail;
    $out->createUser->human->metadata = $meta;
}
header('Content-Type: application/json');
echo json_encode($out);
