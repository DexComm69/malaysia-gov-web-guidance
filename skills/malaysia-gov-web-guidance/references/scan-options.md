# `scan` options

`python ".../mgwg.py" scan <home-url-or-file> [options]` (the same as `scripts/splask_scan.py`). It reads the HTML the server sends, as the SPLaSK crawler does, and checks the rules from JDN's *Manual Tagging SPLaSK V2.0*. Every FAIL has a suggested fix. It is a pre-check: the SPLaSK assessment is the authority.

## Which pages

| Option | Use |
|---|---|
| *(none)* | Home page only |
| `--pages all` | Home page plus every page it links to that SPLaSK cares about (privacy, sitemap, feedback, FAQ, contact, news, ...) |
| `--list-pages` | Show those pages, numbered, then stop |
| `--pages 1,3` / `--pages privacy,sitemap` / `--pages <url>,<url>` | Only the pages the user named |
| `--max-pages N` | Cap on extra pages (default 15) |

A tag found only on another page is a WARN telling you to register that page as a **Criteria URL** in the SPLaSK site profile; the report ends with the list of Criteria URLs to register. It also lists **freshness due dates**: when each dated item (news, about us, contact, client charter, CIO) goes stale.

## Extra checks

| Option | Checks |
|---|---|
| `--check-links` | Every same-site link on the scanned pages (Active Link); `--check-links all` adds external links. Also opens each tagged data.gov.my / GAMMA link and checks the link text is the exact dataset title or app name. Needs internet. |
| `--myds` | Official masthead wording, its "Kenal pasti begini" toggle and position; Poppins/Inter (another font is a conflict to raise with the user); light mode by default |
| `--a11y` | Form fields without labels, links/buttons without an accessible name, skipped heading levels, duplicate ids, skip link |
| `--render` | Compares with the page after JavaScript runs and fails tags only JavaScript adds. Needs Playwright (`pip install playwright`); uses the system Edge or Chrome |
| `--due-within N` | WARN for dated items that go stale within N days |
| `--today YYYY-MM-DD` | Date used for freshness (tests, reproducible reports) |

## Fixing

`--fix` writes `<page>.fixed.html` next to each scanned **local .html** file, with safe mechanical fixes only: misspelled tags and tag values, tags moved off `<i>` icons and wrapper `<div>`s onto the right `<a>`/`<form>`, the exact MyGov URL, viewport and `lang`. It never changes dates, text, titles, descriptions or other links. For a CMS or framework, fix the template that produces the page instead (see `cms-wordpress-joomla` and `assets/templates/`).

## Output

| Option | Output |
|---|---|
| *(default)* | Text report |
| `--format md` | Markdown table (for reports, issues, pull requests) |
| `--format json` (or `--json`) | Machine-readable (always English) |
| `--lang ms` | Text/Markdown report in Bahasa Melayu |
| `--md-out FILE` | Also append the Markdown report to FILE (e.g. `$GITHUB_STEP_SUMMARY`) |
| `--fail-on fail` / `warn` | Exit code 1 on FAIL (or WARN), for CI |

The repository's GitHub Action runs the same scan: inputs `url`, `pages`, `fail-on`, `due-within`, and `extra-args` (e.g. `--myds --a11y --check-links --lang ms`).
