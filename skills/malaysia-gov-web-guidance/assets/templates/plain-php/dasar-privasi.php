<?php
/** Dedicated privacy page: its heading contains "privasi" and carries the tag (SPLaSK Privacy Policy, part 2;
 *  part 1 is the tagged footer link on every page). The policy text is the agency's own: TODO. */
$PAGE = ['title' => 'Dasar Privasi', 'description' => 'Dasar privasi portal rasmi.'];
require __DIR__ . '/header.php';
?>
<h1 splwpk-privacy-policy="splwpk-privacy-policy"><?= lang() === 'en' ? 'Privacy Policy' : 'Dasar Privasi' ?></h1>
<p>TODO: <?= lang() === 'en' ? "the agency's privacy policy text." : 'teks dasar privasi agensi.' ?></p>
<?php require __DIR__ . '/footer.php'; ?>
