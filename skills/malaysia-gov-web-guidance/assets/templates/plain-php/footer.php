<?php
/** Starter footer: privacy link on every page, sitemap, MyGov, and the other SPLaSK links that have real URLs. */
$L = lang();
?>
</main>
<footer class="site-footer">
  <nav aria-label="<?= $L === 'en' ? 'Footer' : 'Pautan kaki' ?>">
    <?php foreach ($FOOTER_LINKS as [$tag, $url, $ms, $en]): if ($url === null) continue;
          // the feedback TAG belongs on the <form> of the feedback page, not on this link
          $attr = $tag === 'splwpk-feedback-form' ? '' : ' ' . $tag . '="' . $tag . '"'; ?>
      <a href="<?= e($url) ?>"<?= $attr ?>><?= e($L === 'en' ? $en : $ms) ?></a>
    <?php endforeach; ?>
    <a href="<?= e($SITE['mygov']) ?>">MyGov</a>
  </nav>
  <p>&copy; <?= date('Y') ?> <?= e($SITE[$L === 'en' ? 'name_en' : 'name_ms']) ?>. <?= $L === 'en' ? 'All Rights Reserved' : 'Hak Cipta Terpelihara' ?>.</p>
</footer>
<script>
/* Text-size control for splwpk-w3c: the tag is in the server HTML; this only adds the behaviour. */
document.querySelectorAll('[splwpk-w3c] [data-size]').forEach(function (b) {
  b.addEventListener('click', function () {
    var step = parseInt(b.dataset.size, 10);
    document.documentElement.style.fontSize = step === 0 ? '' : (100 + step * 12.5) + '%';
  });
});
</script>
</body>
</html>
