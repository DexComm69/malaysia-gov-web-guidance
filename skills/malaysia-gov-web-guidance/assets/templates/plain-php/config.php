<?php
/**
 * Site settings for the starter header/footer (plain PHP, no framework).
 * Every TODO needs a real value from the agency: never invent URLs or dates.
 */
declare(strict_types=1);

$SITE = [
    'name_ms'  => 'TODO Nama Agensi',              // e.g. Majlis Daerah Contoh Jaya
    'name_en'  => 'TODO Agency Name',
    // Languages that REALLY have content. Add 'en' only when the English pages exist:
    // splwpk-multilang is printed only when there is more than one language.
    'languages' => ['ms'],
    'mygov'    => 'https://www.malaysia.gov.my',   // exact URL required by SPLaSK
    // Path the site lives under: '' at the web root, '/mdcj' for http://localhost/mdcj/ on XAMPP.
    'base'     => rtrim((string) (getenv('SITE_BASE') ?: ''), '/'),
];

/**
 * Pages SPLaSK looks for. 'updated_at' must come from the CMS/database (the real date the
 * content last changed), e.g. SELECT updated_at FROM pages WHERE slug = 'tentang-kami'.
 * A page with url null is not printed (no placeholder links: they fail Active Link).
 */
$SPLASK_PAGES = [
    // tag                          url                 label (ms)          label (en)        updated_at (Y-m-d H:i:s) or null
    ['splwpk-about-us',          '/tentang-kami',   'Tentang Kami',      'About Us',       null],
    ['splwpk-news',              '/berita',         'Berita',            'News',           null],
    ['splwpk-faq',               '/soalan-lazim',   'Soalan Lazim',      'FAQ',            null],
    ['splwpk-contact-details',   '/hubungi-kami',   'Hubungi Kami',      'Contact Us',     null],
    ['splwpk-client-charter',    null,              'Piagam Pelanggan',  'Client Charter', null],   // TODO url
    ['splwpk-publicising',       null,              'Ketua Pegawai Digital', 'Chief Digital Officer', null],   // TODO url
];
$FOOTER_LINKS = [
    // tag                        url               label (ms)        label (en)
    ['splwpk-privacy-policy',  '/dasar-privasi', 'Dasar Privasi',  'Privacy Policy'],
    ['splwpk-sitemap',         '/peta-laman',    'Peta Laman',     'Sitemap'],
    ['splwpk-feedback-form',   '/maklum-balas',  'Maklum Balas',   'Feedback'],   // link only; the TAG goes on the <form> in maklum-balas.php
    ['splwpk-publication',     null,             'Penerbitan',     'Publications'],     // TODO url
    ['splwpk-electronic-archive', null,          'Arkib',          'Archive'],          // TODO url
    ['splwpk-procurement',     null,             'Tender dan Sebut Harga', 'Tenders and Quotations'],   // TODO url
    ['splwpk-freedom',         null,             'Kebebasan Maklumat', 'Freedom of Information'],   // TODO url
    ['splwpk-online-e-participation', null,      'e-Penyertaan',   'e-Participation'],  // TODO url (with its policy)
];

function lang(): string {
    global $SITE;
    $l = $_GET['lang'] ?? 'ms';
    return in_array($l, $SITE['languages'], true) ? $l : 'ms';
}

/** Site URL for a root-relative path, so the site also works in a sub-folder. */
function url(string $path): string {
    global $SITE;
    return $SITE['base'] . '/' . ltrim($path, '/');
}

function e(?string $s): string {
    return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8');
}

/** SPLaSK timestamp: always the full Y-m-d H:i:s of a real update, never the current time. */
function splask_ts(?string $updatedAt): string {
    if ($updatedAt === null) return '';
    $t = strtotime($updatedAt);
    return $t === false ? '' : date('Y-m-d H:i:s', $t);
}
