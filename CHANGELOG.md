# Changelog

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
