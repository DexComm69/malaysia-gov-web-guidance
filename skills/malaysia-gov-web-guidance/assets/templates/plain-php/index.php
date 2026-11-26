<?php
$PAGE = [
    'title'       => 'Laman Utama',
    'description' => 'TODO One-sentence summary of the agency site, under 160 characters.',
];
require __DIR__ . '/header.php';
?>
<h1><?= e($SITE[lang() === 'en' ? 'name_en' : 'name_ms']) ?></h1>
<p>TODO kandungan laman utama.</p>
<?php require __DIR__ . '/footer.php'; ?>
