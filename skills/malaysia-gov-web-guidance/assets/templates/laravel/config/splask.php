<?php
/*
 | SPLaSK links for the starter header/footer. Tagged links live here and in the Blade partials,
 | never in admin-editable HTML. A url of null is not printed (no placeholder links).
 | 'model'/'slug' say where the real updated_at comes from (see SplaskComposer).
 */
return [
    'languages' => ['ms'],   // add 'en' only when the English pages really exist
    'mygov' => 'https://www.malaysia.gov.my',
    'menu' => [
        ['tag' => 'splwpk-about-us',        'url' => '/tentang-kami', 'ms' => 'Tentang Kami', 'en' => 'About Us',   'source' => ['page', 'tentang-kami']],
        ['tag' => 'splwpk-news',            'url' => '/berita',       'ms' => 'Berita',       'en' => 'News',       'source' => ['news', null]],
        ['tag' => 'splwpk-faq',             'url' => '/soalan-lazim', 'ms' => 'Soalan Lazim', 'en' => 'FAQ',        'source' => ['page', 'soalan-lazim']],
        ['tag' => 'splwpk-contact-details', 'url' => '/hubungi-kami', 'ms' => 'Hubungi Kami', 'en' => 'Contact Us', 'source' => ['page', 'hubungi-kami']],
    ],
    'footer' => [
        ['tag' => 'splwpk-privacy-policy', 'url' => '/dasar-privasi', 'ms' => 'Dasar Privasi', 'en' => 'Privacy Policy'],
        ['tag' => 'splwpk-sitemap',        'url' => '/peta-laman',    'ms' => 'Peta Laman',    'en' => 'Sitemap'],
        ['tag' => null,                    'url' => '/maklum-balas',  'ms' => 'Maklum Balas',  'en' => 'Feedback'],   // the tag goes on the feedback page's <form>
        ['tag' => 'splwpk-publication',    'url' => null, 'ms' => 'Penerbitan', 'en' => 'Publications'],   // TODO real url
        ['tag' => 'splwpk-electronic-archive', 'url' => null, 'ms' => 'Arkib', 'en' => 'Archive'],        // TODO real url
        ['tag' => 'splwpk-procurement',    'url' => null, 'ms' => 'Tender dan Sebut Harga', 'en' => 'Tenders and Quotations'],   // TODO
        ['tag' => 'splwpk-freedom',        'url' => null, 'ms' => 'Kebebasan Maklumat', 'en' => 'Freedom of Information'],      // TODO
    ],
];
