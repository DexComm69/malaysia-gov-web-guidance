<?php
declare(strict_types=1);
require __DIR__ . '/bootstrap.php';

try {
    $claims = $OIDC->handleCallback($_GET);
} catch (Throwable $ex) {
    error_log('MyDigital ID login failed: ' . $ex->getMessage());   // never log tokens or IC numbers
    http_response_code(401);
    echo '<!DOCTYPE html><html lang="ms"><meta charset="utf-8"><title>Log masuk gagal</title>'
       . '<h1>Log masuk gagal</h1><p>Sila <a href="login.php">cuba log masuk semula</a>.</p>'
       . '<p lang="en">Login failed. Please <a href="login.php">try again</a>.</p></html>';
    exit;
}

$name = (string) ($claims[$CONFIG['claim_name']] ?? '');
$nric = (string) ($claims[$CONFIG['claim_nric']] ?? '');
if ($nric === '') {
    error_log('MyDigital ID login: IC number claim missing (check claim_nric in config.php)');
    http_response_code(401);
    exit('Log masuk gagal.');
}

session_regenerate_id(true);                                         // new session id after login
$_SESSION['user'] = [
    'sub'  => (string) $claims['sub'],
    'name' => $name,
    'nric_key' => nric_for_storage($nric, $CONFIG['nric_pepper']),   // TODO: look up / create the local account with this
    'nric_masked' => mask_nric($nric),
    'login_at' => time(),
];
header('Location: index.php', true, 303);
