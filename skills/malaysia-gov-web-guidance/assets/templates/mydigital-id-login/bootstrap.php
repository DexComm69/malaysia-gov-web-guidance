<?php
declare(strict_types=1);

$secure = ($_SERVER['HTTPS'] ?? '') === 'on' || getenv('MYID_ALLOW_HTTP_FOR_TESTS') !== '1';
session_set_cookie_params(['lifetime' => 0, 'path' => '/', 'secure' => $secure, 'httponly' => true, 'samesite' => 'Lax']);
session_start();

require __DIR__ . '/oidc.php';
$CONFIG = require __DIR__ . '/config.php';
$OIDC = new MyIdOidc($CONFIG);

function e(?string $s): string { return htmlspecialchars((string) $s, ENT_QUOTES, 'UTF-8'); }

/** For display only: ******-**-1234 */
function mask_nric(string $nric): string {
    $d = preg_replace('/\D/', '', $nric);
    return strlen($d) >= 4 ? '******-**-' . substr($d, -4) : '****';
}

/** What to store: a keyed hash if a pepper is configured, otherwise the digits (agency decision). */
function nric_for_storage(string $nric, string $pepper): string {
    $d = preg_replace('/\D/', '', $nric);
    return $pepper !== '' ? hash_hmac('sha256', $d, $pepper) : $d;
}
