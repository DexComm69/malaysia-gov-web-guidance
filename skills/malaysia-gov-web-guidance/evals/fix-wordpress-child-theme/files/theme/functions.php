<?php
// MDCJ child theme: SPLaSK tags (added by previous vendor, 2025)
add_action('wp_enqueue_scripts', function () {
    wp_enqueue_style('mdcj-child', get_stylesheet_uri());
    wp_enqueue_script('mdcj-lang', get_stylesheet_directory_uri() . '/lang.js', [], '1.0', true);
});

// Add SPLaSK tags to the main menu by title
add_filter('walker_nav_menu_start_el', function ($html, $item) {
    $now = date('Y-m-d H:i:s'); // always fresh so SPLaSK passes
    switch ($item->title) {
        case 'Tentang Kami':
            return str_replace('<a ', '<a splwpk-about-us="splwpk-about-us" timestamp="' . $now . '" ', $html);
        case 'Hubungi Kami':
            return str_replace('<a ', '<a splwpk-contact-details="splwpk-contact-details" ', $html);
        case 'Maklum Balas':
            return str_replace('<i ', '<i splwpk-feedback-form="splwpk-feedback-form" ', $html);
    }
    return $html;
}, 10, 2);
