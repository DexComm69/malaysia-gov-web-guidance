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
document.querySelectorAll('[splwpk-w3c] [data-size]').forEach(function (b) {
  b.addEventListener('click', function () {
    var s = parseInt(b.dataset.size, 10);
    document.documentElement.style.fontSize = s === 0 ? '' : (100 + s * 12.5) + '%';
  });
});
</script>
<?php wp_footer(); ?>
</body>
</html>
