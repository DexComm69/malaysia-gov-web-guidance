# Eval baseline

The cases in this folder come from stress-test rounds 4 to 7. Their graders were applied to the outputs those rounds produced, one run per arm, with and without the skill.

| Case | With the skill | Without the skill |
|---|---|---|
| `fix-seeded-faults-home-page` (6 checks) | **6 / 6** | 2 / 6: invented `splwpk-security-policy` and `splwpk-disclaimer`, feedback tag on a link instead of the `<form>`, 94-character title, no MyGov link |
| `fix-wordpress-child-theme` (7 checks) | **7 / 7** | 3 / 7: invented `splwpk-security-policy`, `splwpk-disclaimer` and `splwpk-mygov`, kept the `splwpk-sitemaps` typo, search and feedback tags off the `<form>`, no Criteria URL step |
| `fix-joomla-child-template` (7 checks) | **7 / 7** | 2 / 7: invented `splwpk-multi-language`, kept the `splwpk-electronic-archieve` typo, date-only timestamps, search and feedback tags off the `<form>`, no tag on the language switcher |
| `fix-laravel-blade-app` (7 checks) | **7 / 7** | 5 / 7: search and feedback tags off the `<form>`, 78-character title, MyGov link without `www` (no invented tags this time; it also honestly hid the EN switch) |
| **Total** | **27 / 27** | **12 / 27** |
| `fix-laravel-blade-app-bm` (8 checks: the same task asked and reported in Bahasa Melayu) | **8 / 8** (same scan result as the English run) | not run |

Checks that both arms passed: in the first two cases, real timestamps kept instead of invented dates, no "always now" timestamp, the language switcher printed by PHP, viewport and one `<h1>`; in the Joomla case, removing the "always now" timestamp and the administrator steps; in the Laravel case, real full-format timestamps, the typo and Blade-comment fixes, official tags only and an honest note on the missing English content.

**How this was measured (26 November 2026).** The checks that a script can decide were checked with a script; "no invented dates" and the `splwpk-x` example inside a PHP comment were judged by reading the files. The outputs came from skill versions 1.4 (round 4), 1.5.0 (round 5), 1.6.0 (round 6) and 1.6.1 (round 7), with prompts close to, but not word for word, the ones in `prompt.md`. Treat this as a baseline, not a statistically solid score.

**Running the suite with the CLI.** From this skill's folder:

```sh
claude plugin eval . --scaffold --allow-tools Write,Edit,Bash
```

The CLI only grants a shell tool when it can sandbox it. On Windows without the sandbox feature the runs are refused, so run it on macOS or Linux (or WSL) with the sandbox backend installed. Each case runs 3 times per arm by default; these are billed model runs.
