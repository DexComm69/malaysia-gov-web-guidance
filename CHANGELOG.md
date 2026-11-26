# Changelog

## 1.9.0 (26 November 2026)

- **`scan` reports freshness due dates and the Criteria URLs to register.** Each dated item (news, about us, contact, client charter, CIO) shows its last update and the day it goes stale; `--due-within N` turns anything due within N days into a WARN (also an input of the GitHub Action, for weekly reminders).
- **`scan --myds`**: official masthead wording, its "Kenal pasti begini" toggle and its position; Poppins/Inter (another font is reported as a conflict to raise); light mode by default.
- **`scan --a11y`**: form fields without labels, links/buttons with no accessible name, skipped heading levels, duplicate ids, and a skip link on the home page.
- **`scan --fix`**: writes `<page>.fixed.html` with safe mechanical fixes for static HTML: misspelled tags and tag values, tags moved off `<i>` icons and wrapper `<div>`s onto the right `<a>`/`<form>`, the exact MyGov URL, viewport and `lang`. Dates, text and other links are never changed.
- **`scan --render`**: compares the server HTML with the page after JavaScript runs (Playwright, using the system Edge or Chrome) and fails tags that only JavaScript adds.
- **`scan --lang ms`**: the text and Markdown reports in Bahasa Melayu (JSON stays English).
- **Starter templates** (`assets/templates/`): header/footer for plain PHP, WordPress, Joomla, Laravel and Next.js with the masthead, correctly placed tags, real-date timestamps, a W3C control, a skip link, one `<h1>`, and a language switcher shown only when a second language exists. The rendered example has no MYDS or accessibility warnings; PHP files pass `php -l`; tests check every template against the rules.
- **New guide `mydigital-id`**: sign-in with MyDigital ID (MyID Access, standard OpenID Connect) and identity checks with MyID Verify, summarised from MyDigital ID Sdn. Bhd.'s developer portal, with the decisions to raise (data kept, hashing the IC number, Static vs Live).
- **New guide `bm-ui-glossary`**: standard BM wording for masthead, navigation, SPLaSK page names, buttons, forms and dates, from MYDS's own Malay strings; notes where MYDS differs from Dewan Bahasa spelling (*kemas kini*, *e-mel*) and its *Modul* mislabel for Modal.
- 77 unit tests (32 new).

## 1.8.0 (26 November 2026)

- **New `update-index` command** (`scripts/myds_index.py`): compares `references/myds-index.json` with the live MYDS documentation navigation and reports new, renamed and removed pages. `--write` adds new pages (English and Malay titles, section headings, stub status, and a category taken from the nearest page in the navigation), fixes renamed titles and drops pages only when their URL really returns 404; a page missing from the navigation but still online is reported and kept. `--refresh` re-reads every page; `--fail-on-change` exits 1 for CI. Against the live site: 115 pages, up to date; a full refresh reproduced every title, Malay title and stub status in the index.
- **Weekly CI check** (`.github/workflows/myds-index.yml`): fails when MYDS has changed, so the index never silently ages.
- 45 unit tests (5 new, with a stand-in MYDS site).

## 1.7.1 (26 November 2026)

- **`scan` fixes:**
  - An open-data link to data.gov.my that isn't a dataset page (the home page, a dashboard) is now a clear FAIL ("not a dataset page") instead of a confusing title mismatch.
  - A tag missing from the home page is only softened to the "register a Criteria URL" WARN when the tag on the other page is itself correct. A misplaced tag there (for example on an `<i>`) keeps the home-page FAIL.
  - The "this may be a splash page" warning now appears only when the page links on to a separate home page (`/utama`, `/home`), not on every home page with few tags.
- **GitHub Action:** a moving `v1` tag always points at the latest 1.x release, so workflows can use `@v1`.
- **Trigger test** rerun on 1.7.1: 18/18 on the first pass (9 government prompts, 9 near-misses).
- 40 unit tests (4 new).

## 1.7.0 (26 November 2026)

- **`scan --check-links` checks the data.gov.my and GAMMA links:** for every link tagged `splwpk-open-data`, it opens the dataset on data.gov.my and compares the link text with the dataset's English and Malay titles; for every `splwpk-mobile-apps` link, it reads the app's name from its GAMMA page. A wrong title is a FAIL whose fix gives the exact title; a dataset or app that doesn't exist is a FAIL; a site that can't be reached is a WARN. Matching ignores case, spacing and punctuation. Tested live: jdn.gov.my's GAMMA link matches ("GAMMA.my"); a real dataset passes with either its English or Malay title and fails with a paraphrase.
- 36 unit tests (5 new, offline, with stand-in pages).

## 1.6.2 (26 November 2026)

- **Stress test round 7** (Laravel 11 + Blade + Alpine.js, 5 pages, 15 seeded faults), run in English with and without the skill and once entirely in Bahasa Melayu: with the skill 27 → 11 scan fails in both languages (all 11 need real council URLs); without it 27 → 17. Two new eval cases, `fix-laravel-blade-app` and `fix-laravel-blade-app-bm` (with a check that the report is in formal BM). Eval baseline: 27/27 with the skill, 12/27 without; the BM case 8/8.
- **`scan` catches tags bound by JavaScript frameworks** (Alpine.js `x-bind:splwpk-*`, Vue `:splwpk-*`) as a FAIL, and no longer repeats a tag-on-`<i>` finding as a wrapper warning.
- **`splask-tagging`:** Alpine/Vue bindings and Blade `{{-- --}}` comments hide tags from the crawler; keep tags in templates rather than admin-editable HTML; add `splwpk-multilang` only when the site really has both languages (both with-skill runs showed an EN switch on a BM-only site, though they flagged it; the run without the skill hid it, which is better).
- 31 unit tests (3 new).

## 1.6.1 (26 November 2026)

- **Stress test round 6** (Joomla 5 Cassiopeia child template, 5 pages, 15 seeded faults): with the skill, 25 → 8 scan fails (7 of them date-only placeholders in its sample pages, 1 needing an admin switch); without it, 25 → 22, with an invented `splwpk-multi-language` tag and date-only timestamps. A third eval case, `fix-joomla-child-template`, joins the suite: 20/20 checks with the skill, 7/20 without.
- **Fixed a `scan` bug from 1.5.1:** PASS lines for timestamped tags said "no freshness limit" even where the limit is 30 days (stale dates were still caught). Found by the with-skill agent in round 6.
- **`scan` warns when search or feedback tags sit on a wrapper** (`<div>` around the form) instead of the `<form>` itself, as the manual requires. Age is never shown as negative.
- **`splask-tagging`:** a timestamp is always the full `YYYY-MM-DD HH:MM:SS`; in sample HTML use `00:00:00` when only the date is known, never `TODO` inside the attribute.
- **`cms-wordpress-joomla` (Joomla):** tag the language switcher through a `mod_languages` override, form extensions put "custom attributes" on the module wrapper, remove `Factory::getDate('now')` timestamps, one `<h1>`.
- 28 unit tests (4 new).

## 1.6.0 (26 November 2026)

- **`scan --check-links`:** tests every link on the scanned pages for SPLaSK's Active Link criterion (no broken links). Same-site links by default; `--check-links all` adds external links. A broken link is a FAIL naming the page and link text; a link that can't be reached right now is a WARN. Checks run 4 at a time, retry with GET when a server refuses HEAD, and retry unreachable links once more one by one. `--max-links` caps the run (default 150). On jdn.gov.my: 58 links, none broken.
- **Eval suite** (`skills/malaysia-gov-web-guidance/evals/`): stress-test rounds 4 and 5 as `claude plugin eval` cases, with their input files and 13 graders (official tag names only, form placement, no invented dates, no fake "now" timestamps, SEO limits, Criteria URL steps). Run with `claude plugin eval . --scaffold --allow-tools Write,Edit,Bash` from the skill folder.
- **One-source build** (`tools/build.py`): builds the `.skill` file from this repository, and can layer a private overlay (extra files plus exact text patches) for an internal edition. A patch whose text no longer matches stops the build, so editions can't drift apart. CI runs `python tools/build.py --check`.
- **`mgwg.py`:** uses MYDS pages and the MYDS stylesheet bundled with the skill when they are present, before fetching them.
- 24 unit tests (3 new for links).

## 1.5.1 (26 November 2026)

- **Stress test round 5** (WordPress child theme, 5 pages, 15 seeded faults): with the skill, 27 → 11 fails, all 11 needing real council URLs; without it, 27 → 22 and three invented tag names. The trigger test, rerun with 18 prompts, scored 18/18.
- **`scan` warns about generated timestamps:** a timestamp equal to the scan date/time usually means the theme prints the current time instead of the real update date.
- **`scan`:** no "very little server HTML" warning on small pages that carry tags; Windows paths shown with forward slashes.
- **One `<h1>` rule made consistent** across the guides and the scanner: a site name repeated in the header should be a `<p>` or `<a>`, so each page's title is its one `<h1>`.
- **`cms-wordpress-joomla`:** tagging an Elementor Pro form with `elementor/widget/render_content`, multilang needs a real second language, and removing fake "now" timestamps.

## 1.5.0 (26 November 2026)

- **Multi-page `scan`:** choose which pages to check, or check them all.
  - `--list-pages` lists the pages linked from the home page that a SPLaSK review needs (privacy, sitemap, feedback, search, contact, FAQ, about, news, client charter, publication, archive, procurement, e-participation, CIO, freedom of information). It finds them from tagged links first, then from link text in BM or English.
  - `--pages all`, `--pages 1,3` (numbers from the list), `--pages privacy,sitemap` (names) or `--pages <url>,<url>`; `--max-pages` caps the run. `--follow` still works and means `--pages privacy`.
  - Each page gets the tag checks (spelling, placement, timestamps, freshness, link targets). Findings that repeat the home page word for word (shared header and footer) are shown once.
  - The dedicated privacy page is checked for a tagged H1–H6 containing "privasi"/"privacy".
  - A tag missing from the home page but found on a scanned page becomes a WARN that says to register that page as a Criteria URL in the SPLaSK profile.
- **A suggested fix for every FAIL**, as ready-to-paste markup where possible.
- **`--format text|json|md`, `--md-out FILE` and `--fail-on never|fail|warn`** for reports and CI.
- **GitHub Action** (`action.yml`): `uses: DexComm69/malaysia-gov-web-guidance@v1.5.0` with `url`, `pages` and `fail-on`. It writes the Markdown report to the job summary.
- **Automated tests** (`tests/`, standard-library `unittest`): a 15-fault page and a 4-page fixture site, run by a self-test workflow on Linux and Windows, Python 3.8 and 3.13.
- **New guide `cms-wordpress-joomla`** (EN/BM): tags in child-theme or template code, menu-link filters and overrides, search forms, real timestamps from modified dates, and why editors strip `splwpk-*` attributes.
- **SKILL.md and `audit-checklist`:** start site checks with `scan --pages all`, or the pages the user named.

## 1.4.0 (25 November 2026)

- **New `scan` command:** a SPLaSK 2.0 pre-check of a live site or HTML file, built from JDN's tagging manual. Like the crawler, it reads the server HTML without running JavaScript. It reports:
  - missing, misspelled or misplaced tags (on `<i>`, not on the `<form>`, privacy tag not on a link);
  - tags that exist only in HTML comments or only in JavaScript;
  - missing or badly formatted timestamps, and freshness against each criterion's window;
  - data.gov.my and GAMMA link targets, the dedicated privacy page (`--follow`), and the MyGov link;
  - home-page SEO limits, viewport, HTTPS, redirects and fetch time;
  - the MYDS masthead (info only), and a hint when the URL looks like a splash page.
- **Stress test round 4:** the scanner was run on 5 live federal, state and local-government portals, and its false alarms were fixed. Real issues it found include a misspelled tag value, tags inside HTML comments, a curly quote inside a tag value, and stale timestamps. Fixing a page with 15 seeded faults took it from 25 fails to 12 with the skill, against 17 without it; the run without the skill also invented two tag names.
- **Placement rules clarified from the manual's examples:** search, advanced search and feedback tags go on the `<form>` element itself; multilang goes on the language switcher; w3c goes on the controls' wrapper (ready-made snippet added); keep one `<h1>` for the page's main subject.
- **SKILL.md:**
  - start "we failed SPLaSK" requests with `scan`;
  - never invent URLs or dates that the rules depend on; leave TODOs instead;
  - the report-language question applies to document files, not chat replies.
- **`splask-operations`:** logins with a one-time code, dashboard refresh times, and the fact that assessment reports are kept 6 months only.

## 1.3.0 (25 November 2026)

**SPLaSK guides now follow JDN's official manuals:** *Manual Tagging SPLaSK V2.0* and the SPLaSK user manuals for Webmaster and Supervisor. Before this, the tag list came from live portal HTML.

- **`splask-tagging` rewritten:** every tag with its official conditions.
  - Search, advanced search and feedback must use `<form>`.
  - W3C needs text-size, font or background controls.
  - Datasets: link text must match the data.gov.my title. Mobile apps: link to GAMMA.
  - Freshness windows: 30 days, 60 days for client-charter achievement, and *immediately* for ministerial changes.
  - Online services must be on the home page.
  - Privacy policy is two-part: a link on every page, plus a dedicated page with a tagged heading.
  - **Tags must not sit on `<i>` icon elements.**
  - The `timestamp` format is confirmed.
- **New tag: `splwpk-freedom`** (Freedom of Information), the 25th criterion.
- **`splwpk-pdpa` and `seo-h1` are marked as not in the official manual.**
- **`splask-criteria-checklist` rewritten:** 25 criteria in 6 dimensions, with the crawler-only rules:
  - SEO: title under 70 characters, description under 160, all `alt`, no deprecated tags, exactly one `<h1>`;
  - viewport meta;
  - Google top 10 through SerpAPI;
  - an exact link to www.malaysia.gov.my;
  - HTTPS;
  - downtime formula and registered maintenance;
  - load in 5 seconds or less, with at most 5 redirects.
- **New guide `splask-operations`:**
  - crawler firewall whitelisting (ports 80/443);
  - the site profile, **Criteria URL** for tags not on the home page, SerpAPI token, Matomo tracking code;
  - on-demand vs scheduled assessments;
  - error statuses and their causes.
- **`audit-checklist` script:** checks the SPLaSK 2.0 SEO rules, deprecated tags, tags on `<i>`, and MyGov links.
- **Fixed:** the `splwpk-*` patterns used in the guides' checks didn't allow digits, so `splwpk-w3c` showed up as `splwpk-w`.
- 6 dimensions confirmed by the manual; the 7-dimension description on malaysia.gov.my is the older model.

## 1.2.0 (25 November 2026)

From stress-test round 3: a Next.js 14 App Router build using the official MYDS React components (all 11 imports checked against the published `@govtechmy/myds-react` 1.0.2 exports), and a trigger test with 16 real prompts (8 that should use the skill, 8 near-misses that shouldn't). **Final trigger score: 16/16.**

- **Description:** now says that short reviews of pasted HTML/PHP should consult the skill, because SPLaSK tag names aren't reliably known from memory.

- **New guide `myds-react-nextjs`:**
  - confirming imports and undocumented props;
  - SPLaSK tags in JSX/TSX (TypeScript declaration for `timestamp`, tags on native elements, check the server HTML);
  - BM/EN locale routing and the language switch;
  - known gaps in the MYDS React docs.
- **Language-switch pattern** added for plain PHP/HTML too.
- **Masthead wording:** documented that one MYDS demo says "Malaysian"; the locale files and malaysia.gov.my say "Malaysia".
- **Lookup services** (status checks) added to `service-form-pattern`: POST only, the same message for not-found and mismatch, rate limiting, never echo the MyKad number.
- **SKILL.md:** React projects retrieve one `develop-*` page per imported component; flag MYDS doc gaps instead of guessing.

## 1.1.0 (25 November 2026)

Fixes from two rounds of stress testing: a full review of a 7-role staff system, and building a public application form from scratch.

- **More reliable on slow networks:** MYDS page fetches retry 3 times, fall back to a cached copy (labelled `STALE`), and show the page outline if all else fails. New `prefetch` command to cache pages ahead of time.
- **Class checker:** understands HTML built by JavaScript string concatenation and template strings, and PHP/Blade expressions. It ignores array keys and function arguments, and reads `classList` calls. False alarms on a real 2,600-line app went from 42 to 0 (9 real findings kept).
- **New `tokens` command:** lists every MYDS theme token with its light and dark colour.
- **New guide `audit-checklist`:** how to review an existing site, with a browser check script, the rules for internal staff systems, and the report format.
- **New guide `service-form-pattern`:** public forms (fields, server-side validation and error summary, PDPA notice, CSRF and Post/Redirect/Get, acknowledgement with reference number, automatic notification, GOS e-Rating).
- **Better search** for form, validation and review queries, in English and Malay.
- **Known conflict documented:** MYDS input border contrast vs WCAG 1.4.11.
- Clearer rules: which SPLaSK tags belong on inner pages, and that React-only components are rebuilt with native HTML in non-React projects.

## 1.0.0 (25 November 2026)

First release.
