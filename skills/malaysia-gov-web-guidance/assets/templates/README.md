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
| `plain-php/` | Plain PHP / HTML (e.g. XAMPP) | `config.php` (site name, page URLs, where the dates come from), then `header.php` / `footer.php` |
| `wordpress/` | WordPress child theme | `functions.php`; set CSS classes `splask-about`, `splask-news`, `splask-faq`, `splask-contact`, `splask-sitemap`, `splask-privacy` on menu items |
| `joomla/` | Joomla 4/5 child template | `index.php`, `helper/splask.php`; set the same values as menu items' **Link Class** |
| `laravel/` | Laravel + Blade | `config/splask.php`, register `SplaskComposer` for `partials.header` and `partials.footer` |
| `nextjs/` | Next.js App Router | `lib/splask.ts`, `app/[lang]/layout.tsx`; add `types/splask.d.ts`; middleware must set an `x-pathname` header (or pass the path another way) |

**Everything marked TODO needs a real value from the agency** (URLs, the source of each date, agency name, description). Pages without a real URL are simply not printed: a placeholder link would fail Active Link.

After adapting a template, check the result with:

```sh
python scripts/mgwg.py scan <your-home-page-url> --pages all --check-links --myds --a11y
```

`example.html` scores no warnings on the MYDS and accessibility checks; its remaining SPLaSK fails are the pages a real agency still has to supply (archive, open data, mobile app, and so on). The PHP files pass `php -l`; the Blade and TSX files are checked for the rules above by the skill's tests but are not compiled.
