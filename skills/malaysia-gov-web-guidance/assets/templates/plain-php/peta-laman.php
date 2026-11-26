<?php
/** Sitemap page, built from config.php so it never misses a page. The footer link to it carries splwpk-sitemap. */
$PAGE = ['title' => 'Peta Laman', 'description' => 'Senarai semua halaman portal.'];
require __DIR__ . '/header.php';
$L = lang();
$extra = [['/', 'Laman Utama', 'Home'], ['/carian-terperinci', 'Carian Terperinci', 'Advanced search']];
?>
<h1><?= $L === 'en' ? 'Sitemap' : 'Peta Laman' ?></h1>
<ul>
  <?php foreach ($extra as [$u, $labelMs, $labelEn]): ?>
    <li><a href="<?= e(url($u)) ?>"><?= e($L === 'en' ? $labelEn : $labelMs) ?></a></li>
  <?php endforeach; ?>
  <?php foreach (array_merge($SPLASK_PAGES, $FOOTER_LINKS) as $row): if ($row[1] === null || $row[1] === '/peta-laman') continue; ?>
    <li><a href="<?= e(url($row[1])) ?>"><?= e($L === 'en' ? $row[3] : $row[2]) ?></a></li>
  <?php endforeach; ?>
</ul>
<?php require __DIR__ . '/footer.php'; ?>
