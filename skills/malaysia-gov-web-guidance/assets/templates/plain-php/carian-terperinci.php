<?php
/** Advanced search: the splwpk-advanced-search-function tag is on this page's <form>.
 *  Register this page as the Criteria URL for that tag in the SPLaSK site profile. */
$PAGE = ['title' => 'Carian Terperinci', 'description' => 'Carian terperinci mengikut kata kunci, jenis kandungan dan tarikh.'];
require __DIR__ . '/header.php';
$en = lang() === 'en';
?>
<h1><?= $en ? 'Advanced search' : 'Carian terperinci' ?></h1>
<form action="<?= e(url('/carian')) ?>" method="get" splwpk-advanced-search-function="splwpk-advanced-search-function">
  <label for="as-q"><?= $en ? 'Keywords' : 'Kata kunci' ?></label>
  <input id="as-q" name="q" type="search" value="<?= e($_GET['q'] ?? '') ?>">

  <label for="as-type"><?= $en ? 'Content type' : 'Jenis kandungan' ?></label>
  <select id="as-type" name="jenis">
    <option value=""><?= $en ? 'All' : 'Semua' ?></option>
    <option value="halaman"><?= $en ? 'Pages' : 'Halaman' ?></option>
    <option value="berita"><?= $en ? 'News' : 'Berita' ?></option>
  </select>

  <label for="as-from"><?= $en ? 'From date' : 'Dari tarikh' ?></label>
  <input id="as-from" name="dari" type="date">
  <label for="as-to"><?= $en ? 'To date' : 'Hingga tarikh' ?></label>
  <input id="as-to" name="hingga" type="date">

  <button type="submit"><?= $en ? 'Search' : 'Cari' ?></button>
</form>
<?php require __DIR__ . '/footer.php'; ?>
