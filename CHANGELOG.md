# Changelog

## 1.2.0 (unreleased)

From stress-test round 3: a Next.js 14 App Router build using the official MYDS React components. All 11 imports were checked against the published `@govtechmy/myds-react` 1.0.2 exports.

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
