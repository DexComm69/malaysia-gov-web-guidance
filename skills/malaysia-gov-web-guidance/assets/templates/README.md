# Starter templates: MYDS masthead + SPLaSK tags

Ready-made header and footer code for five setups. Each one gives the same result, shown in `example.html` (rendered from the plain-PHP template with demo data for a fictional council):

- the official MYDS masthead (wording from the MYDS locale files), a skip link, MYDS stylesheet and Poppins/Inter;
- the search tag on the search `<form>`, a W3C text-size control (`splwpk-w3c`) rendered on the server;
- menu links tagged by **code**, with `timestamp` taken from the content's **real** last-updated date (never the current time);
- the language switcher (`splwpk-multilang`) printed **only when a second language really has content**;
- footer links for privacy (on every page), sitemap and MyGov (`https://www.malaysia.gov.my`), and the other SPLaSK pages once they have real URLs;
- one `<h1>` per page: the page's own heading (the site name in the header is a link).

| Folder | For | Start with |
|---|---|---|
| `plain-php/` | Plain PHP / HTML (e.g. XAMPP) | `config.php` (site name, page URLs, where the dates come from, `base` for sub-folders), then `header.php` / `footer.php`; see **Plain PHP: before you start** below |
| `wordpress/` | WordPress child theme | `functions.php`; set CSS classes `splask-about`, `splask-news`, `splask-faq`, `splask-contact`, `splask-sitemap`, `splask-privacy` on menu items |
| `joomla/` | Joomla 4/5 child template | `index.php`, `helper/splask.php`; set the same values as menu items' **Link Class** |
| `laravel/` | Laravel + Blade | `config/splask.php`, register `SplaskComposer` for `partials.header` and `partials.footer` |
| `mydigital-id-login/` | Sign-in with MyDigital ID (plain PHP, no Composer) | its own README; tested against a mock OpenID Connect provider |
| `nextjs/` | Next.js App Router | `lib/splask.ts`, `app/[lang]/layout.tsx`, `proxy.ts` (`middleware.ts` before Next.js 16: BM by default, `x-pathname` for the language switch); add `types/splask.d.ts` |

### Plain PHP: before you start

1. **Flag image:** save the official MYDS flag as `assets/img/malaysia-flag.svg`, from https://github.com/govtechmy/myds/blob/main/packages/react/src/svg/icons/malaysia-flag.svg (it isn't bundled: the MYDS repository has no licence). Don't draw a different flag.
2. **Sub-folder installs** (`http://localhost/mdcj/` on XAMPP): set `SITE_BASE=/mdcj` (environment or `config.php`) and `RewriteBase /mdcj/` in `.htaccess`. All links go through `url()`.
3. **Pages included:** `index.php`, `carian.php` (search results), `carian-terperinci.php` (advanced search, tagged `<form>`), `maklum-balas.php` (feedback: tagged `<form>`, validation, CSRF, reference number), `dasar-privasi.php` (tagged privacy heading), `peta-laman.php` (built from `config.php`), `404.php`. **You write** the content pages the menu links to (`tentang-kami.php`, `berita.php`, `soalan-lazim.php`, `hubungi-kami.php`, ...) the same way: set `$PAGE`, include `header.php`, one `<h1>`, include `footer.php`.
4. **Local testing:** `php -S 127.0.0.1:8080 -t . router.php`. The built-in server ignores `.htaccess`; the router gives the same pretty URLs and blocks settings and data files. **Keep databases outside the web root** in production.
5. `assets/site.css` hides the skip link until focused, tidies the masthead, sets the 12-8-4 container and uses a darker input border than MYDS's (MYDS's is below WCAG's 3:1; a choice to confirm with the agency).

**Everything marked TODO needs a real value from the agency** (URLs, the source of each date, agency name, description). Pages without a real URL are simply not printed: a placeholder link would fail Active Link.

After adapting a template, check the result with:

```sh
python scripts/mgwg.py scan <your-home-page-url> --pages all --check-links --myds --a11y
```

`example.html` scores no warnings on the MYDS and accessibility checks; its remaining SPLaSK fails are the pages a real agency still has to supply (archive, open data, mobile app, and so on). The PHP files pass `php -l`; the Blade and TSX files are checked for the rules above by the skill's tests but are not compiled.
