<?php
declare(strict_types=1);
require __DIR__ . '/bootstrap.php';
$_SESSION['csrf'] ??= MyIdOidc::random(32);
$u = $_SESSION['user'] ?? null;
?>
<!DOCTYPE html>
<html lang="ms">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Akaun saya</title>
</head>
<body>
<main>
<?php if ($u): ?>
  <h1>Selamat datang, <?= e($u['name']) ?></h1>
  <p>No. kad pengenalan: <?= e($u['nric_masked']) ?></p>
  <form method="post" action="logout.php">
    <input type="hidden" name="csrf" value="<?= e($_SESSION['csrf']) ?>">
    <button type="submit">Log keluar</button>
  </form>
<?php else: ?>
  <h1>Log masuk</h1>
  <p>Anda memerlukan aplikasi MyDigital ID yang telah didaftarkan untuk log masuk.</p>
  <a class="btn" href="login.php">Log masuk dengan MyDigital ID</a>
<?php endif; ?>
</main>
</body>
</html>
