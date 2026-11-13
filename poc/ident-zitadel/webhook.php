<?php
/**
 * PoC Ident (#25): Empfänger für Zitadel Actions v2 (Ereignis an ein Modul, Plattform S4).
 * Prüft die Signatur «ZITADEL-Signature: t=<Zeit>,v1=<HMAC-SHA256(Schlüssel, t.Body)>», höchstens 5 Minuten alt.
 * Start: SIGNING_KEY=… php -S 0.0.0.0:8099 webhook.php
 */
$body = file_get_contents('php://input');
$header = $_SERVER['HTTP_ZITADEL_SIGNATURE'] ?? '';
parse_str(str_replace(',', '&', $header), $parts);
$expected = hash_hmac('sha256', ($parts['t'] ?? '').'.'.$body, (string) getenv('SIGNING_KEY'));
$fresh = abs(time() - (int) ($parts['t'] ?? 0)) <= 300;
$valid = isset($parts['v1']) && hash_equals($expected, $parts['v1']) && $fresh;
$event = json_decode($body, true) ?? [];
file_put_contents(__DIR__.'/webhook.log', json_encode([
    'gueltig' => $valid,
    'ereignis' => $event['event_type'] ?? null,
    'aggregate' => $event['aggregateID'] ?? null,
    'organisation' => $event['resourceOwner'] ?? null,
]).PHP_EOL, FILE_APPEND);
http_response_code($valid ? 200 : 401);
