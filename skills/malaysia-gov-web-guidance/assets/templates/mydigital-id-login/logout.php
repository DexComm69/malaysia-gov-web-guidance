<?php
declare(strict_types=1);
require __DIR__ . '/bootstrap.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST' || !hash_equals($_SESSION['csrf'] ?? '', (string) ($_POST['csrf'] ?? ''))) {
    http_response_code(405);
    exit;
}
try {
    $url = $OIDC->logoutUrl($CONFIG['after_logout']);                 // ends the MyDigital ID session too
} catch (Throwable $ex) {
    $url = $CONFIG['after_logout'];
}
$_SESSION = [];
session_destroy();
header('Location: ' . $url, true, 303);
