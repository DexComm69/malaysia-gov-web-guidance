<?php
$PAGE = ['title' => 'Carian', 'description' => 'Carian kandungan laman.'];
require __DIR__ . '/header.php';
$q = trim((string) ($_GET['q'] ?? ''));
?>
<h1><?= lang() === 'en' ? 'Search' : 'Carian' ?></h1>
<?php if ($q === ''): ?>
  <p><?= lang() === 'en' ? 'Enter a word in the search box above.' : 'Masukkan perkataan dalam kotak carian di atas.' ?></p>
<?php else: ?>
  <p><?= lang() === 'en' ? 'Results for' : 'Hasil carian untuk' ?> "<?= e($q) ?>":</p>
  <?php
  // TODO: search your own content, e.g. SELECT slug, title FROM pages WHERE title LIKE :q OR body LIKE :q
  // (bind the parameter; never put $q into SQL directly).
  $results = [];
  ?>
  <?php if (!$results): ?><p><?= lang() === 'en' ? 'Nothing found.' : 'Tiada hasil dijumpai.' ?></p><?php endif; ?>
<?php endif; ?>
<p><a href="<?= e(url('/carian-terperinci')) ?>"><?= lang() === 'en' ? 'Advanced search' : 'Carian terperinci' ?></a></p>
<?php require __DIR__ . '/footer.php'; ?>
