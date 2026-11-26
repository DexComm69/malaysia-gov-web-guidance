<?php
declare(strict_types=1);
require __DIR__ . '/bootstrap.php';

try {
    header('Location: ' . $OIDC->loginUrl(), true, 302);
} catch (Throwable $ex) {
    error_log('MyDigital ID login start failed: ' . $ex->getMessage());
    http_response_code(503);
    echo '<!DOCTYPE html><html lang="ms"><meta charset="utf-8"><title>Log masuk</title>'
       . '<p>Log masuk dengan MyDigital ID tidak dapat dimulakan sekarang. Sila cuba lagi sebentar lagi.</p>'
       . '<p lang="en">MyDigital ID login could not be started. Please try again shortly.</p></html>';
}
