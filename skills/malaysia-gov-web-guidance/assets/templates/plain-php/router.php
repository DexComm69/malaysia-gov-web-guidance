<?php
/**
 * Router for PHP's built-in server (local testing), doing what .htaccess does on Apache:
 *   php -S 127.0.0.1:8080 -t . router.php
 * The built-in server ignores .htaccess, so without this router a database or settings file
 * in the site folder could be downloaded. In production keep databases OUTSIDE the web root anyway.
 */
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH) ?: '/');
$file = __DIR__ . $path;

if (preg_match('~/(config|header|footer|masthead|demo|router)\.php$|\.(sqlite|sqlite3|db|ini|log|env)$|/\.~i', $path)) {
    http_response_code(404); require __DIR__ . '/404.php'; return true;
}
if ($path === '/' ) { require __DIR__ . '/index.php'; return true; }
if (is_file($file) && !str_ends_with($file, '.php')) return false;           // static file: let the server send it
if (is_file($file)) { require $file; return true; }
$php = __DIR__ . rtrim($path, '/') . '.php';
if (preg_match('~^/[a-z0-9-]+/?$~', $path) && is_file($php)) { require $php; return true; }
http_response_code(404);
require __DIR__ . '/404.php';
return true;
