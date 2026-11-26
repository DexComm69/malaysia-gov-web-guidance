<?php defined('ABSPATH') || exit; ?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
  <meta charset="<?php bloginfo('charset'); ?>">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <?php wp_head(); /* title and description: set them in the SEO plugin, home title under 70 characters, description 1-159 */ ?>
</head>
<body <?php body_class('font-body'); ?>>
<?php wp_body_open(); /* skip link + masthead, from functions.php */ ?>
<header class="site-header">
  <a class="site-name" href="<?php echo esc_url(home_url('/')); ?>"><?php bloginfo('name'); ?></a>
  <?php /* one <h1> per page: the page title in the content, not the site name here */ ?>
  <?php get_search_form(); ?>

  <div role="group" aria-label="Saiz tulisan" splwpk-w3c="splwpk-w3c">
    <button type="button" data-fs="0.875" aria-label="Kecilkan tulisan" aria-pressed="false">A-</button><button type="button" data-fs="1" aria-label="Saiz tulisan biasa" aria-pressed="true">A</button><button type="button" data-fs="1.25" aria-label="Besarkan tulisan" aria-pressed="false">A+</button>
  </div>

  <?php if (count(splask_languages()) > 1 && function_exists('pll_the_languages')): ?>
    <div class="lang-switch" splwpk-multilang="splwpk-multilang">
      <?php pll_the_languages(['display_names_as' => 'slug']); ?>
    </div>
  <?php endif; ?>

  <nav aria-label="Menu utama"><?php wp_nav_menu(['theme_location' => 'primary', 'container' => false]); ?></nav>
</header>
<main id="kandungan">
