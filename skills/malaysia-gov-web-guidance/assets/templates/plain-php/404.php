<?php
http_response_code(404);
$PAGE = ['title' => 'Halaman tidak dijumpai', 'description' => 'Halaman yang anda cari tidak wujud.'];
require __DIR__ . '/header.php';
?>
<h1><?= lang() === 'en' ? 'Page not found' : 'Halaman tidak dijumpai' ?></h1>
<p><?= lang() === 'en' ? 'The page you are looking for does not exist.' : 'Halaman yang anda cari tidak wujud.' ?>
   <a href="<?= e(url('/')) ?>"><?= lang() === 'en' ? 'Back to Home' : 'Kembali ke Laman Utama' ?></a></p>
<?php require __DIR__ . '/footer.php'; ?>
