<?php
/** Starter footer: privacy link on every page, sitemap, MyGov, and the other SPLaSK links that have real URLs. */
$L = lang();
?>
</main>
<footer class="site-footer">
  <nav aria-label="<?= $L === 'en' ? 'Footer' : 'Pautan kaki' ?>">
    <?php foreach ($FOOTER_LINKS as [$tag, $url, $labelMs, $labelEn]): if ($url === null) continue;
          // the feedback TAG belongs on the <form> of the feedback page, not on this link
          $attr = $tag === 'splwpk-feedback-form' ? '' : ' ' . $tag . '="' . $tag . '"'; ?>
      <a href="<?= e(url($url)) ?>"<?= $attr ?>><?= e($L === 'en' ? $labelEn : $labelMs) ?></a>
    <?php endforeach; ?>
    <a href="<?= e($SITE['mygov']) ?>">MyGov</a>
  </nav>
  <p>&copy; <?= date('Y') ?> <?= e($SITE[$L === 'en' ? 'name_en' : 'name_ms']) ?>. <?= $L === 'en' ? 'All Rights Reserved' : 'Hak Cipta Terpelihara' ?>.</p>
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
