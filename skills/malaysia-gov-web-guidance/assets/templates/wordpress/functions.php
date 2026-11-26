<?php
/**
 * Starter child theme functions for a government WordPress site (see guide cms-wordpress-joomla).
 * Tags are printed by theme code, so editors can't delete them by editing content.
 * Menu items get their SPLaSK tag from a CSS class set in Appearance > Menus (Screen Options > CSS Classes):
 *   splask-about, splask-news, splask-faq, splask-contact, splask-sitemap, splask-privacy, splask-charter, splask-cio
 * The menu item must be a Page (or the news category) so the theme can read its real modified date.
 */
defined('ABSPATH') || exit;

add_action('wp_enqueue_scripts', function () {
    wp_enqueue_style('myds-style', 'https://cdn.jsdelivr.net/npm/@govtechmy/myds-style@1.0.0/dist/index.css', [], null);
    wp_enqueue_style('myds-fonts', 'https://fonts.googleapis.com/css2?family=Poppins:wght@500;600&family=Inter:wght@400;500;600&display=swap', [], null);
    wp_enqueue_style('child', get_stylesheet_uri(), ['myds-style'], wp_get_theme()->get('Version'));
});

// Official masthead right after <body> (the theme's header.php must call wp_body_open()).
add_action('wp_body_open', function () {
    echo '<a class="skip-link" href="#kandungan">' . esc_html__('Langkau ke kandungan utama', 'mdcj') . '</a>';
    get_template_part('parts/masthead');
});

/** SPLaSK timestamp from a real WordPress date: never the current time. */
function splask_ts(?int $post_id): string {
    return $post_id ? (string) get_post_modified_time('Y-m-d H:i:s', false, $post_id) : '';
}

/** Newest news post's modified time (category slug 'berita'), for the news link. */
function splask_news_ts(): string {
    $q = new WP_Query(['post_type' => 'post', 'posts_per_page' => 1, 'orderby' => 'modified', 'category_name' => 'berita', 'no_found_rows' => true]);
    return $q->have_posts() ? splask_ts($q->posts[0]->ID) : '';
}

add_filter('nav_menu_link_attributes', function ($atts, $item) {
    $map = [
        'splask-about'   => ['splwpk-about-us', true],
        'splask-news'    => ['splwpk-news', true],
        'splask-faq'     => ['splwpk-faq', true],
        'splask-contact' => ['splwpk-contact-details', true],
        'splask-charter' => ['splwpk-client-charter', true],
        'splask-cio'     => ['splwpk-publicising', true],
        'splask-sitemap' => ['splwpk-sitemap', false],
        'splask-privacy' => ['splwpk-privacy-policy', false],
    ];
    foreach ($map as $class => [$tag, $needs_ts]) {
        if (!in_array($class, (array) $item->classes, true)) continue;
        $atts[$tag] = $tag;
        if ($needs_ts) {
            $ts = $tag === 'splwpk-news' ? splask_news_ts() : ($item->object === 'page' ? splask_ts((int) $item->object_id) : '');
            if ($ts !== '') $atts['timestamp'] = $ts;   // no real date -> no timestamp (scan will say so)
        }
    }
    return $atts;
}, 10, 2);

// The search tag goes on the <form> itself.
add_filter('get_search_form', fn($form) => preg_replace('/<form\b/', '<form splwpk-search-function="splwpk-search-function"', $form, 1));

/** Languages that really have content. Add 'en' only when English pages exist (e.g. with Polylang/WPML). */
function splask_languages(): array {
    return function_exists('pll_languages_list') ? (array) pll_languages_list() : ['ms'];
}
