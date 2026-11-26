<?php
/** Privacy page (selected in Settings > Privacy): one <h1>, tagged for SPLaSK, containing "privasi". */
defined('ABSPATH') || exit;
get_header();
while (have_posts()): the_post(); ?>
  <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
    <h1 class="entry-title" splwpk-privacy-policy="splwpk-privacy-policy"><?php the_title(); ?></h1>
    <div class="entry-content"><?php the_content(); ?></div>
  </article>
<?php endwhile;
get_footer();
