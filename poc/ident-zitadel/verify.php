<?php
/**
 * PoC Ident (#25): Access-Token (JWT) ohne Zusatzpaket prüfen – Signatur RS256 über JWKS, iss, aud, exp,
 * Rollen und Mandant auslesen. Vorlage für die Token-Prüfung in eduksx/core 0.2.
 * Aufruf: php verify.php <token-datei> <projekt-id> [feld]
 */
[$_, $file, $project] = $argv + [null, null, null];
$field = $argv[3] ?? 'access_token';
$data = json_decode(file_get_contents($file), true);
$jwt = $data[$field] ?? $data;
$issuer = 'http://localhost:8080';

$b64 = fn (string $s) => base64_decode(strtr($s, '-_', '+/').str_repeat('=', (4 - strlen($s) % 4) % 4));
[$h, $p, $sig] = explode('.', $jwt);
$header = json_decode($b64($h), true);
$claims = json_decode($b64($p), true);

$ctx = stream_context_create(['http' => ['proxy' => '', 'request_fulluri' => false]]);
$jwks = json_decode(file_get_contents("$issuer/oauth/v2/keys", false, $ctx), true);
$jwk = current(array_filter($jwks['keys'], fn ($k) => $k['kid'] === $header['kid']));
if (! $jwk || $header['alg'] !== 'RS256') {
    exit("Schlüssel oder Verfahren unbekannt\n");
}
// RSA-Schlüssel aus n/e als PEM (DER-Kodierung von SubjectPublicKeyInfo)
$len = fn (int $l) => $l < 128 ? chr($l) : (($b = ltrim(pack('N', $l), "\0")) ? chr(0x80 | strlen($b)).$b : '');
$int = fn (string $x) => "\x02".$len(strlen($x = (ord($x[0]) > 127 ? "\0".$x : $x))).$x;
$rsa = $int($b64($jwk['n'])).$int($b64($jwk['e']));
$rsa = "\x30".$len(strlen($rsa)).$rsa;
$bits = "\x03".$len(strlen($rsa) + 1)."\x00".$rsa;
$alg = "\x30\x0d\x06\x09\x2a\x86\x48\x86\xf7\x0d\x01\x01\x01\x05\x00";
$spki = "\x30".$len(strlen($alg.$bits)).$alg.$bits;
$pem = "-----BEGIN PUBLIC KEY-----\n".chunk_split(base64_encode($spki), 64)."-----END PUBLIC KEY-----\n";

$ok = openssl_verify("$h.$p", $b64($sig), $pem, OPENSSL_ALGO_SHA256) === 1;
$checks = [
    'Signatur' => $ok,
    'iss' => $claims['iss'] === $issuer,
    'aud enthält Projekt' => in_array($project, (array) $claims['aud'], true),
    'nicht abgelaufen' => $claims['exp'] > time(),
];
foreach ($checks as $name => $pass) {
    echo ($pass ? '✓ ' : '✗ ').$name."\n";
}
$roles = $claims["urn:zitadel:iam:org:project:$project:roles"] ?? [];
echo 'Rollen: '.implode(', ', array_keys($roles))."\n";
echo 'Mandant (Organisation): '.json_encode(array_values(array_map('array_keys', $roles)))."\n";
// Manipuliertes Token muss scheitern
$forged = $h.'.'.rtrim(strtr(base64_encode(json_encode(['sub' => 'x'] + $claims)), '+/', '-_'), '=').'.'.$sig;
[$fh, $fp] = explode('.', $forged);
echo (openssl_verify("$fh.$fp", $b64($sig), $pem, OPENSSL_ALGO_SHA256) === 1 ? '✗' : '✓').' verändertes Token abgelehnt'."\n";
exit(in_array(false, $checks, true) ? 1 : 0);
