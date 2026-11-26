<?php defined('ABSPATH') || exit; ?>
</main>
<footer class="site-footer">
  <nav aria-label="Pautan kaki">
    <?php
    // Footer menu items use the same CSS classes as the main menu (splask-privacy, splask-sitemap, ...).
    wp_nav_menu(['theme_location' => 'footer', 'container' => false, 'fallback_cb' => false]);
    ?>
    <a href="https://www.malaysia.gov.my">MyGov</a>
  </nav>
  <p>&copy; <?php echo esc_html(wp_date('Y')); ?> <?php bloginfo('name'); ?>. Hak Cipta Terpelihara.</p>
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
<?php wp_footer(); ?>
</body>
</html>
