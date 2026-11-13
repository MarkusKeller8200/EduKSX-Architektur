<?php
/**
 * PoC Ident (#25/#36, P4): Stub der Ident-Brücke. Zitadel ruft sie vor Userinfo und Access-Token auf (Actions v2,
 * restCall). Sie prüft ZITADEL-Signature und antwortet mit den Plattform-Claims eduksx_orgs und eduksx_roles
 * (spec/v1/oidc-claims.schema.json), damit Module keine Zitadel-Claims auswerten müssen.
 * Start: SIGNING_KEY=… php -S 0.0.0.0:8098 bridge.php
 */
$body = file_get_contents('php://input');
parse_str(str_replace(',', '&', $_SERVER['HTTP_ZITADEL_SIGNATURE'] ?? ''), $sig);
$valid = isset($sig['v1'], $sig['t']) && abs(time() - (int) $sig['t']) <= 300
    && hash_equals(hash_hmac('sha256', $sig['t'].'.'.$body, (string) getenv('SIGNING_KEY')), $sig['v1']);
if (! $valid) {
    http_response_code(401);
    exit;
}
$in = json_decode($body, true);
file_put_contents(__DIR__.'/bridge-request.json', json_encode($in, JSON_PRETTY_PRINT));
$state = json_decode(file_get_contents(__DIR__.'/state.json'), true);
// Projekt → Modulschlüssel (in der echten Brücke aus dem Modulregister bzw. Steckbrief)
$modules = [$state['project'] => 'glossary', $state['platform_project'] => 'platform'];
// Plattform-ID (UUID) je Organisation: im Stub als UUID v5 aus der Zitadel-ID, in der Brücke aus ihrer Datenbank
$uuid = function (string $id): string {
    $h = sha1('eduksx-org:'.$id);
    return sprintf('%s-%s-5%s-%s%s-%s', substr($h, 0, 8), substr($h, 8, 4), substr($h, 13, 3),
        dechex(8 | (hexdec($h[16]) & 3)), substr($h, 17, 3), substr($h, 20, 12));
};
$roles = [];
foreach ($in['user_grants'] ?? [] as $grant) {
    $module = $modules[$grant['project_id'] ?? ''] ?? null;
    if ($module === null) {
        continue;
    }
    foreach ($grant['roles'] ?? [] as $role) {
        $roles[$module][] = preg_replace('/^'.$module.'\./', '', $role);
    }
}
$roles = array_map(fn ($r) => array_values(array_unique($r)), $roles);
$org = $in['org'] ?? [];
$orgs = isset($org['id']) ? [['id' => $uuid((string) $org['id']), 'name' => (string) ($org['name'] ?? ''), 'role' => 'member']] : [];
header('Content-Type: application/json');
echo json_encode(['append_claims' => [
    ['key' => 'eduksx_orgs', 'value' => $orgs],
    ['key' => 'eduksx_roles', 'value' => (object) $roles],
]]);
