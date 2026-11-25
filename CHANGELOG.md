# Changelog

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
