---
name: malaysia-gov-web-guidance
description: "Unofficial guide to Malaysian government web standards: MYDS (Malaysia Government Design System) components, tokens, grid, typography, accessibility and page patterns, plus JDN's SPLaSK website-monitoring criteria and the exact splwpk-* HTML tags its crawler reads. English + Bahasa Melayu. Use it FIRST whenever building, reviewing, auditing or fixing a Malaysian public-sector website, portal, online service or internal system: anything for a kementerian, jabatan, agensi, badan berkanun, PBT/majlis, state government or .gov.my site, or when the user mentions MYDS, SPLaSK, JDN, MAMPU, PKPA, GovTech Malaysia, masthead or 'portal rasmi'. This includes short reviews of pasted HTML/PHP ('check this footer', 'why did we fail SPLaSK', 'accessibility review'): SPLaSK tag names and criteria are not reliably known from memory, so consult the skill instead of answering directly. Do NOT use for non-government projects, other countries' design systems, or backend-only work (SQL, APIs, deployment)."
---

# Malaysia Government Web Guidance

> **Unofficial.** This skill is not made, endorsed or maintained by Jabatan Digital Negara (JDN), GovTech Malaysia or any government agency. It points to the official sources and summarises them. When the official source and this skill disagree, the official source wins. Tell the user so whenever it matters.

Malaysian public-sector sites are judged against two things a model's training data covers poorly:

1. **MYDS** (Malaysia Government Design System): the official look, tokens and components from GovTech Malaysia / JDN, documented at design.digital.gov.my.
2. **SPLaSK**: JDN's automated monitor, which scores every official agency portal (ministries, departments, statutory bodies, state governments and local councils) against 25 criteria. Most criteria are detected only through custom `splwpk-*` HTML attributes. A page can have a perfect search box or feedback form and still score zero for it if the tag is missing.

The skill has two kinds of guides:
- **Hand-written guides** (`guides/gov/`): SPLaSK overview, tagging, criteria checklist, a plain-HTML masthead, MYDS without React, and WordPress/Joomla. Each has an English section and a Bahasa Melayu section.
- **MYDS documentation pages**, about 115 of them: the index holds only titles and links. `retrieve` reads each page **live from design.digital.gov.my**, in English and/or Malay, and caches it for 7 days. This needs internet access the first time.

## Step 1: Search

```sh
python "<this-skill-dir>/scripts/mgwg.py" search "<what you are building>"
```

Queries can be in English or Malay ("borang maklum balas", "log masuk", "footer with privacy policy"). Run 1–3 searches covering the distinct parts of the task, for example the page pattern, its components and the compliance rules. To browse: `python ".../mgwg.py" list` (or `list --category gov`).

Categories:
- `gov`: hand-written cross-source guides. **For any page on a gov website, also retrieve `splask-tagging` and `splask-criteria-checklist`**, because the crawler checks the header, footer and home page. **When a site is launching, or SPLaSK shows errors or no marks**, retrieve `splask-operations`. **For "we failed SPLaSK", "check our site" or any live URL or HTML file, run `python ".../mgwg.py" scan <url-or-file> --pages all` first.** It checks the official SPLaSK 2.0 rules against the HTML the server sends (tags, spelling, placement, timestamps, SEO limits) on the home page plus the pages it links to (privacy, sitemap, feedback, FAQ, ...), and gives a FAIL/WARN/PASS list with a suggested fix for each FAIL. If the user names pages, scan only those: `--list-pages` shows the numbered choices, then `--pages 1,3`, `--pages privacy,sitemap` or `--pages <url>,<url>`. A tag found only on another page is a WARN that tells you to register that page as a Criteria URL. `--format md` gives a Markdown table for reports; `--fail-on fail` returns exit code 1 for CI (the repository also ships a GitHub Action). Re-run it after fixing. **For WordPress or Joomla sites**, retrieve `cms-wordpress-joomla` (tags in theme code, menu-link filters, editors that strip attributes). **For any review, audit or "semak" request, also use `audit-checklist`.** It has the scope rules, a browser check script, the rules for internal staff systems and the report format. **For any form the public submits or uses to look something up** (permohonan, aduan, pendaftaran, semak status), retrieve `service-form-pattern`. **For React, Next.js, Vite or Inertia projects**, retrieve `myds-react-nextjs` (tags in JSX/TSX, BM/EN routing and language switch, known gaps in the MYDS docs).
- `myds-foundation`: grid, colour, typography, icons, motion, radius, shadow, spacing.
- `myds-component-design`: a component's design spec (anatomy, states, do's and don'ts).
- `myds-component-react` / `myds-react-hook`: a component's React API.
- `myds-html-css`: non-React components (only Button and Toggle are complete; the rest are stubs at the source).
- `myds-pattern`: login, registration, forgot password, landing page, standard page, contact us.
- `myds-setup`, `accessibility`, `splask`.

## Step 2: Retrieve

```sh
python ".../mgwg.py" retrieve <id>[,<id>...] --lang en     # English only, to save context
python ".../mgwg.py" retrieve <id> --lang ms               # official Malay wording
```

Retrieve the 3–6 guides that matter most for the task, not every hit. **The exception is React:** also retrieve the `develop-<component>` page for every MYDS component you import, to confirm its import path and props. Each guide costs context, and extra ones rarely change the result. Fetch another one later if a specific question comes up. Use `--lang ms` or `both` when the user is writing Malay UI text or formal documents (URS/SRS).

Fetches retry 3 times, and fall back to an older cached copy (marked `STALE`) if the site can't be reached. If a fetch still fails, the script prints the page's section outline. Tell the user, give them the page URL, and continue with the hand-written guides. Don't fill the gap from memory as if it were MYDS. On a slow or filtered network, or before working offline, run `python ".../mgwg.py" prefetch all` (or a category or a list of ids) once to fill the cache. The cache lives in the system temp folder under `mgwg-cache`; `prefetch` prints the exact path. To list token names with their values, run `python ".../mgwg.py" tokens [--filter otl]`.

**MYDS pages can be incomplete or contradict themselves** (for example, undocumented props, or enum values that aren't listed). When one affects the task, tell the user and mark the choice as unconfirmed instead of guessing quietly.

**Match the guides to the project's stack.** MYDS components are React. If the project is plain PHP/HTML/Blade (no React), retrieve `myds-plain-html-php` and `masthead-html`, and use each component's `design-*` page for its anatomy rather than copying React code.

## Step 3: Build and verify against the guides

- Use MYDS tokens (`rgb(var(--txt-black-900))`), not hand-picked hex values. Use the 12-8-4 grid, Poppins for headings and Inter for body text.
- Render `splwpk-*` attributes server-side, with the exact spelling from `splask-tagging`, and give "updated content" tags a real `timestamp`.
- Meet the accessibility rules in `develop-accessibility` (WCAG 2.2: labels, keyboard support, focus, semantics).
- For non-React projects, run `python ".../mgwg.py" check-classes <changed templates> --css <project css>` to catch utility classes that the purged MYDS stylesheet doesn't define.
- Confirm the result does what the user asked. Don't add features they didn't request just because a guide mentions them; list relevant compliance gaps at the end instead.

## Conflicts: always ask, before building

When a government guide disagrees with another source of guidance, **don't pick one yourself**. The other source might be modern-web-guidance, the project's own conventions (CLAUDE.md, an existing design system, the agency's branding) or the user's request. Examples: MYDS primary blue vs an agency's own colours, Poppins/Inter vs the project's fonts, a React-only MYDS component vs a PHP stack, a hidden SPLaSK marker vs an accessibility rule.

1. Do the parts that don't conflict.
2. Ask the user (AskUserQuestion when available). Give both rules, each with its source (guide id and URL), what each choice means for this task, and your recommendation.
3. Ask before building anything that depends on the answer, every time. Don't build your recommended option and ask afterwards, and don't reuse an answer from a different project or an earlier task.
4. If you truly cannot ask (a non-interactive run), use the MYDS default. Put the question at the top of your reply and say which option you assumed.

The same applies when the official sources disagree with each other (for example an older malaysia.gov.my page describing 7 SPLaSK dimensions where JDN's v2.0 manual has 6): state the discrepancy rather than smoothing it over.

## Language of reports and documents

Before writing a report, audit, checklist or other document *file* (not your chat reply, and not UI text), ask which language the user wants: Bahasa Melayu, English, or both. Don't infer it from the language of the request. UI strings follow the site's own languages (BM default, with an EN switch on gov sites).

## Never invent facts the rules depend on

SPLaSK rules often need real-world facts: dataset URLs and titles on data.gov.my, an app's GAMMA page, real `updated_at` dates, privacy and CIO page URLs. If you don't have them, **don't make them up.** Leave a clear `TODO` in the code (for example `<!-- TODO: data.gov.my dataset URL + exact title -->`), and list each one under **Open compliance items** with exactly what the user must supply. A fake date or a guessed link fails SPLaSK anyway, and it also hides the problem.

## How much to trust each guide

- Hand-written guides carry `sources`, `status` and `retrieved` in their frontmatter. MYDS pages are always the live official text.
- `status: stub`: the source page is a placeholder. Say so, and fall back to the design page or general best practice.
- The SPLaSK guides (`splask-tagging`, `splask-criteria-checklist`, `splask-operations`) follow JDN's official *Manual Tagging SPLaSK V2.0* and SPLaSK user manuals. Tags the manual doesn't list (`splwpk-pdpa`, `seo-h1`) are marked as such. If the user has a newer manual, it wins.
- If the user reports a newer MYDS release or SPLaSK change, trust them and say the hand-written guide may be out of date.

## Step 4: Disclose

In the response where you deliver work shaped by these guides, end with a section headed `### Panduan Web Kerajaan`:
- One bullet per guide that actually changed what you built: `- **\`<id>\`**: <the non-obvious choice it drove and the mistake it prevented> ("<short verbatim quote of the rule>")`. Keep each bullet to 2 sentences or fewer.
- Then, if any apply: **Open compliance items:** things this page still needs for SPLaSK or MYDS that you didn't build.
- Only cite guides you retrieved in this turn. Never quote from memory after context compaction; re-run `retrieve` instead.

If you searched but no guide applied, say in one sentence what you checked.
