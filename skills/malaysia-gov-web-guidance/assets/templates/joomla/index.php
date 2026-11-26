<?php
/**
 * Child template index.php (Joomla 4/5, child of Cassiopeia or similar): skip link, masthead,
 * one <h1> (the page's own heading from the component), W3C text-size control, footer links.
 * Set the home page's Browser Page Title so the final <title> is under 70 characters
 * (Global Configuration > Include Site Name in Page Titles adds to it), and fill in Site Meta Description.
 */
defined('_JEXEC') or die;

use Joomla\CMS\Factory;

$app = Factory::getApplication();
$sitename = htmlspecialchars($app->get('sitename'), ENT_QUOTES, 'UTF-8');
$en = str_starts_with($this->language, 'en');
?>
<!DOCTYPE html>
<html lang="<?php echo $this->language; ?>" dir="<?php echo $this->direction; ?>">
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <jdoc:include type="metas" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@govtechmy/myds-style@1.0.0/dist/index.css">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600&family=Inter:wght@400;500;600&display=swap">
  <jdoc:include type="styles" />
  <jdoc:include type="scripts" />
</head>
<body class="site font-body">
  <a class="skip-link" href="#kandungan"><?php echo $en ? 'Skip to main content' : 'Langkau ke kandungan utama'; ?></a>
  <?php include __DIR__ . '/masthead.php'; ?>
  <header class="site-header">
    <a class="site-name" href="<?php echo $this->baseurl; ?>/"><?php echo $sitename; ?></a>
    <jdoc:include type="modules" name="search" style="none" />
    <div role="group" aria-label="<?php echo $en ? 'Text size' : 'Saiz tulisan'; ?>" splwpk-w3c="splwpk-w3c">
      <button type="button" data-fs="0.875" aria-label="Kecilkan tulisan" aria-pressed="false">A-</button><button type="button" data-fs="1" aria-label="Saiz tulisan biasa" aria-pressed="true">A</button><button type="button" data-fs="1.25" aria-label="Besarkan tulisan" aria-pressed="false">A+</button>
    </div>
    <jdoc:include type="modules" name="topbar" style="none" />   <!-- the Language Switcher module (override in html/mod_languages) -->
    <nav aria-label="<?php echo $en ? 'Main menu' : 'Menu utama'; ?>"><jdoc:include type="modules" name="menu" style="none" /></nav>
  </header>
  <main id="kandungan"><jdoc:include type="message" /><jdoc:include type="component" /></main>
  <footer class="site-footer">
    <nav aria-label="<?php echo $en ? 'Footer' : 'Pautan kaki'; ?>">
      <jdoc:include type="modules" name="footer" style="none" />   <!-- footer menu: Link Classes splask-privacy, splask-sitemap, ... -->
      <a href="https://www.malaysia.gov.my">MyGov</a>
    </nav>
    <p>&copy; <?php echo Factory::getDate()->format('Y'); ?> <?php echo $sitename; ?>. <?php echo $en ? 'All Rights Reserved' : 'Hak Cipta Terpelihara'; ?>.</p>
  </footer>
  <script>
  (function () {
  /* Text-size control for splwpk-w3c: the tag is in the server HTML; this adds the behaviour and remembers the choice. */
  var buttons = document.querySelectorAll('[splwpk-w3c] [data-fs]');
  function set(v) {
    document.documentElement.style.fontSize = (16 * parseFloat(v)) + 'px';
    buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.fs === String(v))); });
  }
  buttons.forEach(function (b) {
    b.addEventListener('click', function () { set(b.dataset.fs); try { localStorage.setItem('fs', b.dataset.fs); } catch (e) {} });
  });
  try { var saved = localStorage.getItem('fs'); if (saved) set(saved); } catch (e) {}
})();
  </script>
</body>
</html>
