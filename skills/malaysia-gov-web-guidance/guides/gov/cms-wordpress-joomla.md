---
id: cms-wordpress-joomla
title: "SPLaSK tags and MYDS masthead on WordPress and Joomla sites"
title_ms: "Tag SPLaSK dan masthead MYDS pada laman WordPress dan Joomla"
category: gov
keywords: "wordpress joomla cms tema theme child template override elementor gutenberg block editor menu nav_menu_link_attributes get_search_form wp_body_open kses unfiltered_html timestamp modified date tinymce jce text filters mod_menu mod_finder smart search cassiopeia astra plugin seo yoast rank math tag hilang tag dibuang"
description: "Where splwpk-* tags and the masthead go in a WordPress or Joomla site so they survive editor filtering and theme updates: child themes/template overrides, menu-link attributes, search forms, real timestamps from modified dates, and why the content editor strips custom attributes. Most Malaysian agency portals run on one of these CMSs."
description_ms: "Di mana tag splwpk-* dan masthead diletakkan dalam laman WordPress atau Joomla supaya tidak dibuang oleh editor atau kemas kini tema."
sources: "JDN Manual Tagging SPLaSK V2.0 (tag rules) ; developer.wordpress.org (wp_body_open, nav_menu_link_attributes, get_search_form, get_the_modified_date, wp_kses_allowed_html, child themes) ; docs.joomla.org (template overrides, child templates, Global Configuration Text Filters)"
authority: "JDN (tag rules); WordPress and Joomla documentation (CMS hooks). CMS advice is general practice, not JDN guidance."
status: current
retrieved: 2026-11-26
---

# SPLaSK tags and MYDS masthead on WordPress and Joomla / Tag SPLaSK dan masthead MYDS pada WordPress dan Joomla

## English

**The rule that matters most:** put tags in **theme/template code**, not in page content. CMS editors strip unknown attributes such as `splwpk-news="splwpk-news"` when content is saved, often without warning. Tags typed in the editor may look right on the day and disappear at the next edit. Tag rules themselves (names, `<form>` placement, timestamps, no `<i>`) are in `splask-tagging`; this guide is only about *where* to put them.

After any change, check what the crawler sees with `python scripts/mgwg.py scan <home-url> --pages all`. The scan reads the server HTML, as SPLaSK does, so a tag added by a JavaScript page builder will show up as missing.

### WordPress

1. **Use a child theme** (or a small site plugin), never the parent theme's files: a theme update overwrites them. Header and footer markup goes in the child theme's `header.php` / `footer.php`, or in block-theme template parts (`parts/header.html`) edited as code.
2. **Masthead:** print it right after `<body>` with the `wp_body_open` hook (WordPress 5.2+; the theme must call `wp_body_open()`):
   ```php
   add_action('wp_body_open', function () { get_template_part('parts/masthead'); });  // markup: masthead-html
   ```
3. **Menu links** (About Us, News, FAQ, Contact, Sitemap, Privacy): WordPress menus only let editors set class, title and rel. Add the tag with the `nav_menu_link_attributes` filter, keyed on a CSS class the editor sets on the menu item (*Appearance → Menus → Screen Options → CSS Classes*):
   ```php
   add_filter('nav_menu_link_attributes', function ($atts, $item) {
       $map = ['splask-about' => 'splwpk-about-us', 'splask-news' => 'splwpk-news', 'splask-faq' => 'splwpk-faq',
               'splask-contact' => 'splwpk-contact-details', 'splask-sitemap' => 'splwpk-sitemap',
               'splask-privacy' => 'splwpk-privacy-policy'];
       foreach ($map as $class => $tag) {
           if (in_array($class, (array) $item->classes, true)) {
               $atts[$tag] = $tag;
               // timestamp tags: use the target page's real last-modified date
               if ($tag !== 'splwpk-sitemap' && $tag !== 'splwpk-privacy-policy' && $item->object === 'page') {
                   $atts['timestamp'] = get_the_modified_date('Y-m-d H:i:s', (int) $item->object_id);
               }
           }
       }
       return $atts;
   }, 10, 2);
   ```
   For **News** pointing at a post archive, use the newest post's date instead: `get_lastpostmodified('blog')` returns the newest modified time as `Y-m-d H:i:s`.
4. **Search:** the tag must be on the `<form>`. Override the form with the `get_search_form` filter or a `searchform.php` in the child theme:
   ```php
   add_filter('get_search_form', fn($form) => preg_replace('/<form\b/', '<form splwpk-search-function="splwpk-search-function"', $form, 1));
   ```
   If the site uses a search plugin, check its rendered `<form>` with `scan`; some plugins render the form with JavaScript.
5. **Feedback form:** form plugins (Contact Form 7, WPForms, Gravity Forms, Fluent Forms, Elementor Pro Form) each render their own `<form>`. Use the plugin's own attribute or HTML-output filter, or wrap the shortcode in a template where you control the `<form>`. For an Elementor Pro Form widget, the `elementor/widget/render_content` filter receives the widget's HTML, so you can add the tag to its `<form` for the widget named as the feedback form (check `$widget->get_name() === 'form'` and the form name setting). Confirm the tag lands on the `<form>` element, not a wrapper `<div>`, and clear Elementor's cache before checking.
6. **Why tags vanish from content:** post content is filtered by KSES. Users without the `unfiltered_html` capability (Authors, Editors on multisite, and every user on multisite except Super Admins) lose unknown attributes on save. Don't hand out `unfiltered_html` to fix this; either move the tag into theme code (preferred) or allow just the `splwpk-*` attributes with the `wp_kses_allowed_html` filter for the elements you need.
7. **Page builders:** Elementor Pro has *Advanced → Attributes* (`key|value`, one per line, e.g. `splwpk-faq|splwpk-faq`). It puts attributes on the widget wrapper, which is fine for link-type tags only if the wrapper contains the link; for search and feedback the attribute must reach the `<form>` itself. Run `scan` to confirm. Free Elementor and the block editor don't offer custom attributes on most blocks.
8. **SEO plugins** (Yoast, Rank Math) set the `<title>` and meta description. SPLaSK's home-page limits are stricter than the plugins' green lights: title under 70 characters, description 1–159 characters, exactly one `<h1>`. Many themes print the site name as `<h1>` in the header *and* the page title as another `<h1>`. Make the header's site name a `<p>` or `<a>` on every page, so each page's own title is its one `<h1>`; on the home page, consider titling the front page with the agency name so that `<h1>` names the agency.
9. **Language switcher:** `splwpk-multilang` only counts if the other language really exists. Without a translation plugin (Polylang, WPML, TranslatePress) or separate English pages, `?lang=en` usually shows the same Malay page. Print the switcher from the theme, and point it at real URLs.
10. **Fake timestamps:** some themes set `timestamp` to the current time (`date('Y-m-d H:i:s')`, `current_time()`) "so SPLaSK passes". Remove it: the date must be when the content really changed. `scan` warns when a timestamp equals the time of the scan.
11. **Caching:** after changing tags, purge the page cache (plugin, host or Cloudflare) before scanning; SPLaSK sees the cached HTML.

### Joomla (4 and 5)

1. **Use a child template** (Joomla 4.1+, *System → Site Templates → Create Child Template*) or template overrides. Never edit core module or component files; Joomla updates replace them.
2. **Masthead:** in the child template's `index.php`, right after `<body>`, or in a *Custom* module assigned to a position at the very top (only if the editor keeps the markup; see point 5).
3. **Menu links:** menu items offer only a link class, title and rel. Override the menu layout (*Templates → your template → Create Overrides → Modules → mod_menu*), then in `html/mod_menu/default_component.php` and `default_url.php` add the tag based on the link class the editor sets (*Menu item → Link Type → Link Class*):
   ```php
   $map = ['splask-about' => 'splwpk-about-us', 'splask-news' => 'splwpk-news', 'splask-faq' => 'splwpk-faq',
           'splask-contact' => 'splwpk-contact-details', 'splask-sitemap' => 'splwpk-sitemap', 'splask-privacy' => 'splwpk-privacy-policy'];
   $cls = $item->getParams()->get('menu-anchor_css', '');
   foreach ($map as $c => $tag) { if (str_contains(" $cls ", " $c ")) { $attributes[$tag] = $tag; } }
   ```
   For timestamp tags, take the date from the linked article's `modified` column and format it in the site time zone: `HTMLHelper::_('date', $article->modified, 'Y-m-d H:i:s')`.
4. **Search:** Smart Search (`com_finder` / `mod_finder`) renders the form. Override `html/mod_finder/default.php` and put `splwpk-search-function="splwpk-search-function"` on the `<form>`. The advanced search form (`com_finder` with *Show Advanced Search*) gets `splwpk-advanced-search-function` the same way, in an override of the component's search layout.
5. **Why tags vanish from articles and Custom modules:** *Global Configuration → Text Filters* strips attributes for most groups, and TinyMCE or JCE may also clean the HTML. Prefer template code. If an editor must add a tag in content, set *No Filtering* only for a small trusted group (such as Super Users) and allow custom attributes in the editor's settings, then re-check with `scan`.
6. **SEO:** *Global Configuration → Site → Site Meta Description* and the menu item's *Page Display → Browser Page Title* control the home page. The same SPLaSK limits apply. Joomla's *Site Name in Page Titles* option adds characters, so count the final `<title>`.
7. **Caching:** clear *System → Clear Cache* (and any CDN) before scanning.

### Both CMSs: checklist

- [ ] Tags live in child theme/template code, not in page content.
- [ ] The language switcher points at real pages in the other language.
- [ ] Every timestamp comes from the CMS's real modified date, never a hard-coded or "today" value (a fake date is a compliance problem, and the content must actually be updated within the window).
- [ ] Search, advanced search and feedback tags are on the `<form>`.
- [ ] No tag on an icon `<i>` inside a menu item.
- [ ] Pages tagged outside the home page are registered as Criteria URLs in the SPLaSK site profile (`splask-operations`). `scan --pages all` reports these.
- [ ] One `<h1>` on the home page; title and description within the limits.
- [ ] Cache purged, then `python scripts/mgwg.py scan <home> --pages all` has no FAIL.

## Bahasa Melayu

**Peraturan paling penting:** letakkan tag dalam **kod tema/templat**, bukan dalam kandungan halaman. Editor CMS membuang atribut yang tidak dikenali seperti `splwpk-news="splwpk-news"` semasa kandungan disimpan, selalunya tanpa amaran. Peraturan tag (nama, letak pada `<form>`, *timestamp*, bukan pada `<i>`) ada dalam `splask-tagging`.

Selepas setiap perubahan, semak apa yang dilihat oleh perangkak dengan `python scripts/mgwg.py scan <url-utama> --pages all`.

### WordPress
1. Gunakan **tema anak** (*child theme*) atau plugin kecil, bukan fail tema induk, kerana kemas kini tema akan menulis ganti fail itu.
2. **Masthead:** cetak selepas `<body>` melalui *hook* `wp_body_open`.
3. **Pautan menu:** tambah tag melalui penapis `nav_menu_link_attributes`, berdasarkan kelas CSS yang ditetapkan pada item menu. *Timestamp* diambil daripada `get_the_modified_date('Y-m-d H:i:s', $id)` halaman sasaran, atau `get_lastpostmodified('blog')` untuk berita.
4. **Carian:** tag mesti pada `<form>`; gunakan penapis `get_search_form` atau `searchform.php` dalam tema anak.
5. **Borang maklum balas:** pastikan tag berada pada elemen `<form>` yang dijana oleh plugin borang, bukan pada `<div>` pembalut.
6. **Tag hilang daripada kandungan:** KSES membuang atribut bagi pengguna tanpa keupayaan `unfiltered_html`. Jangan beri keupayaan itu secara meluas; pindahkan tag ke kod tema, atau benarkan atribut `splwpk-*` sahaja melalui penapis `wp_kses_allowed_html`.
7. **Pembina halaman:** Elementor Pro (*Advanced → Attributes*, `kunci|nilai`) meletakkan atribut pada pembalut widget. Untuk carian dan maklum balas, atribut mesti sampai ke `<form>` (contohnya melalui penapis `elementor/widget/render_content`). Sahkan dengan `scan`.
8. **Plugin SEO:** had SPLaSK lebih ketat: tajuk kurang daripada 70 aksara, penerangan 1–159 aksara, satu `<h1>` sahaja di halaman utama. Jadikan nama laman dalam pengepala `<p>` atau `<a>`, bukan `<h1>`.
9. **Penukar bahasa:** `splwpk-multilang` hanya bermakna jika versi bahasa lain benar-benar wujud (plugin terjemahan atau halaman BI berasingan).
10. **Timestamp palsu:** buang kod yang menetapkan `timestamp` kepada masa semasa. Tarikh mesti tarikh kandungan sebenar dikemas kini.
11. Kosongkan *cache* sebelum mengimbas.

### Joomla (4 dan 5)
1. Gunakan **templat anak** atau *template override*; jangan ubah fail teras.
2. **Masthead:** dalam `index.php` templat anak, terus selepas `<body>`.
3. **Pautan menu:** buat *override* `mod_menu` dan tambah tag berdasarkan *Link Class* item menu. *Timestamp* daripada lajur `modified` artikel: `HTMLHelper::_('date', $article->modified, 'Y-m-d H:i:s')`.
4. **Carian:** *override* `mod_finder` dan letakkan tag pada `<form>`.
5. **Tag hilang:** *Global Configuration → Text Filters* dan editor (TinyMCE/JCE) membuang atribut. Utamakan kod templat; jika perlu, benarkan *No Filtering* untuk kumpulan kecil yang dipercayai sahaja.
6. **SEO:** kira panjang `<title>` akhir, termasuk nama laman jika pilihan *Site Name in Page Titles* dihidupkan.
7. Kosongkan *cache* sebelum mengimbas.

### Senarai semak
- [ ] Tag dalam kod tema/templat, bukan kandungan.
- [ ] *Timestamp* daripada tarikh kemas kini sebenar CMS, bukan nilai tetap atau "hari ini".
- [ ] Tag carian, carian terperinci dan maklum balas pada `<form>`.
- [ ] Tiada tag pada ikon `<i>`.
- [ ] Halaman bertag selain halaman utama didaftarkan sebagai *Criteria URL* dalam profil SPLaSK.
- [ ] Satu `<h1>`; tajuk dan penerangan dalam had.
- [ ] `scan --pages all` tiada FAIL.
