<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo('charset'); ?>">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<header class="site-header">
  <img src="<?php echo get_stylesheet_directory_uri(); ?>/logo-mdcj.png">
  <h1 class="site-title"><?php bloginfo('name'); ?></h1>
  <?php get_search_form(); ?>
  <nav><?php wp_nav_menu(['theme_location' => 'primary']); ?></nav>
  <div class="ticker"><a href="/berita/" splwpk-news="splwpk-news" timestamp="2025-12-01 09:00:00">Berita Terkini</a></div>
</header>
