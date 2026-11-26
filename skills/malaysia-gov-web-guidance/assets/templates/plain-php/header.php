<?php
/**
 * Starter header. Usage at the top of a page:
 *   <?php $PAGE = ['title' => 'Tentang Kami', 'description' => '...']; require __DIR__.'/header.php'; ?>
 * then the page prints its own single <h1>. The site name in the header is a link, not a heading.
 */
require_once __DIR__ . '/config.php';
$L = lang();
$name = $SITE[$L === 'en' ? 'name_en' : 'name_ms'];
$title = trim(($PAGE['title'] ?? '') . ' | ' . $name, ' |');          // keep the home page title under 70 characters
?>
<!DOCTYPE html>
<html lang="<?= e($L) ?>">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title><?= e($title) ?></title>
  <meta name="description" content="<?= e($PAGE['description'] ?? '') ?>">   <!-- 1-159 characters on the home page -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@govtechmy/myds-style@1.0.0/dist/index.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600&family=Inter:wght@400;500;600&display=swap">
  <link rel="stylesheet" href="<?= e(url('/assets/site.css')) ?>">
</head>
<body class="font-body">
<a class="skip-link" href="#kandungan"><?= $L === 'en' ? 'Skip to main content' : 'Langkau ke kandungan utama' ?></a>
<?php require __DIR__ . '/masthead.php'; ?>
<header class="site-header">
  <a class="site-name" href="<?= e(url('/')) ?>"><?= e($name) ?></a>

  <form action="<?= e(url('/carian')) ?>" method="get" role="search" splwpk-search-function="splwpk-search-function">
    <label for="carian"><?= $L === 'en' ? 'Search' : 'Carian' ?></label>
    <input id="carian" name="q" type="search">
    <button type="submit"><?= $L === 'en' ? 'Search' : 'Cari' ?></button>
  </form>
  <a href="<?= e(url('/carian-terperinci')) ?>"><?= $L === 'en' ? 'Advanced search' : 'Carian terperinci' ?></a>
  <!-- The advanced-search page's <form> carries splwpk-advanced-search-function; register that page as a Criteria URL. -->

  <div role="group" aria-label="<?= $L === 'en' ? 'Text size' : 'Saiz tulisan' ?>" splwpk-w3c="splwpk-w3c">
    <?php if ($L === 'en'): ?><button type="button" data-fs="0.875" aria-label="Smaller text" aria-pressed="false">A-</button><button type="button" data-fs="1" aria-label="Normal text size" aria-pressed="true">A</button><button type="button" data-fs="1.25" aria-label="Larger text" aria-pressed="false">A+</button><?php else: ?><button type="button" data-fs="0.875" aria-label="Kecilkan tulisan" aria-pressed="false">A-</button><button type="button" data-fs="1" aria-label="Saiz tulisan biasa" aria-pressed="true">A</button><button type="button" data-fs="1.25" aria-label="Besarkan tulisan" aria-pressed="false">A+</button><?php endif; ?>
  </div>

  <?php if (count($SITE['languages']) > 1): ?>
  <div class="lang-switch" splwpk-multilang="splwpk-multilang">
    <?php foreach ($SITE['languages'] as $code): ?>
      <a href="?lang=<?= e($code) ?>" lang="<?= e($code) ?>" hreflang="<?= e($code) ?>"<?= $code === $L ? ' aria-current="true"' : '' ?>><?= $code === 'ms' ? 'BM' : 'EN' ?></a>
    <?php endforeach; ?>
  </div>
  <?php endif; ?>

  <nav aria-label="<?= $L === 'en' ? 'Main menu' : 'Menu utama' ?>">
    <?php foreach ($SPLASK_PAGES as [$tag, $url, $labelMs, $labelEn, $updated]): if ($url === null) continue;
          $ts = splask_ts($updated); ?>
      <a href="<?= e(url($url)) ?>" <?= $tag ?>="<?= $tag ?>"<?= $ts !== '' ? ' timestamp="' . e($ts) . '"' : '' ?>><?= e($L === 'en' ? $labelEn : $labelMs) ?></a>
    <?php endforeach; ?>
  </nav>
</header>
<main id="kandungan">
