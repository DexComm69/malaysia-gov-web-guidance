<?php
/**
 * Renders index.php with demo data (fictional council, made-up dates), to produce example.html:
 *   php demo.php > ../example.html
 * Real sites read the dates from the database instead (see config.php).
 */
require __DIR__ . '/config.php';
$SITE['name_ms'] = 'Majlis Daerah Contoh Jaya';
$SITE['name_en'] = 'Contoh Jaya District Council';
$SITE['languages'] = ['ms', 'en'];   // demo assumes the English pages exist
$demoDates = ['splwpk-about-us' => '2026-11-03 09:12:44', 'splwpk-news' => '2026-11-20 08:05:31',
              'splwpk-faq' => '2026-10-01 15:02:10', 'splwpk-contact-details' => '2026-11-12 11:30:05'];
foreach ($SPLASK_PAGES as &$p) { $p[4] = $demoDates[$p[0]] ?? null; }
unset($p);
foreach ($FOOTER_LINKS as &$f) { if ($f[0] === 'splwpk-feedback-form') $f[1] = '/maklum-balas'; }
unset($f);
$_GET['lang'] = 'ms';
ob_start();
$PAGE = ['title' => 'Laman Utama', 'description' => 'Portal rasmi Majlis Daerah Contoh Jaya: perkhidmatan, berita dan maklumat untuk penduduk.'];
require __DIR__ . '/header.php';
echo '<h1>' . e($SITE['name_ms']) . "</h1>\n<p>Selamat datang.</p>\n";
require __DIR__ . '/footer.php';
echo ob_get_clean();
