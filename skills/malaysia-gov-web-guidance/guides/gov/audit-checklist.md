---
id: audit-checklist
title: "Auditing a gov site or system for MYDS and SPLaSK: steps, checks and report format"
title_ms: "Mengaudit laman web atau sistem kerajaan untuk MYDS dan SPLaSK: langkah, semakan dan format laporan"
category: gov
keywords: "audit review semak semakan pematuhan compliance checklist senarai semak report laporan check verify assess internal system dashboard staff back-office target size contrast overflow h1 labels splwpk masthead"
description: "How to review an existing Malaysian government site or system: decide SPLaSK scope, run the automated browser checks (snippet included), check MYDS identity and SPLaSK tags, judge internal staff tools fairly, and write the report. Use for any 'review / audit / semak / check compliance' request."
description_ms: "Cara menyemak laman web atau sistem kerajaan sedia ada: skop SPLaSK, semakan automatik, identiti MYDS, tag SPLaSK, sistem dalaman, dan format laporan."
sources: "Compiled from this skill's guides (splask-overview, splask-criteria-checklist, splask-tagging, masthead-html, myds-plain-html-php), MYDS develop/accessibility (WCAG 2.2) and design/text-input, design/table; WCAG 2.2 success criteria 1.3.1, 1.4.3, 2.4.1, 2.5.8, 3.3.1, 4.1.2. Workflow tested on a 7-role staff system in November 2026."
authority: "Unofficial synthesis of MYDS (GovTech Malaysia / JDN), SPLaSK (JDN) and W3C WCAG 2.2"
status: current
retrieved: 2026-11-25
---

# Auditing for MYDS and SPLaSK / Mengaudit untuk MYDS dan SPLaSK

## English

### 1. Before you start: ask, don't assume

- **Report language:** BM, English, or both (see SKILL.md).
- **Scope:** public pages only, or every screen and role? For role-based systems, ask which roles exist and how to switch between them.
- **What is being judged:** the agency's *portal* (SPLaSK applies in full), a *government online service* (online-service criteria apply), or an *internal staff tool* (MYDS and accessibility apply; SPLaSK website criteria mostly don't). Retrieve `splask-overview` for the scope rules. If unsure, report SPLaSK items as "applies if this becomes public-facing" rather than as failures.

### 2. Automated checks (run in the browser on every page and role)

Run this in the page console, or through a browser-automation tool, once per route. For single-page apps, switch the role and route, wait for rendering, then run it again.

```js
(() => {
  const m = document.querySelector('main') || document.body;
  const named = el => (el.getAttribute('aria-label') || el.getAttribute('aria-labelledby') || el.textContent || el.title || '').trim();
  const fields = [...m.querySelectorAll('input,select,textarea')].filter(i => i.type !== 'hidden');
  const tables = [...m.querySelectorAll('table')];
  const small = [...document.querySelectorAll('button,a[href],input[type=checkbox],input[type=radio]')]
    .filter(e => { const r = e.getBoundingClientRect(); return r.width && (r.width < 24 || r.height < 24) && !e.closest('p,li,td'); });
  return {
    url: location.href, lang: document.documentElement.lang, title: document.title,
    h1: m.querySelectorAll('h1').length,
    unlabelledFields: fields.filter(i => !(i.labels && i.labels.length) && !i.getAttribute('aria-label') && !i.getAttribute('aria-labelledby')).map(i => i.id || i.name),
    unnamedControls: [...m.querySelectorAll('button,a[href],[role=button]')].filter(b => !named(b)).length,
    imgNoAlt: [...m.querySelectorAll('img')].filter(i => !i.hasAttribute('alt')).length,
    tablesWithoutHeaders: tables.filter(t => !t.querySelector('th')).length,
    tablesWithoutCaption: tables.filter(t => !t.querySelector('caption') && !t.getAttribute('aria-label') && !t.getAttribute('aria-labelledby')).length,
    smallTargets: small.slice(0, 5).map(e => (e.textContent || e.className).trim().slice(0, 30)),
    // SPLaSK 2.0 crawler rules (Manual Tagging SPLaSK V2.0): run these on the HOME page
    titleLength: document.title.length,                                   // must be < 70
    metaDescriptionLength: (document.querySelector('meta[name=description]')?.content || '').length, // must be 1-159
    viewport: !!document.querySelector('meta[name=viewport][content*="width=device-width"]'),
    h1OnWholePage: document.querySelectorAll('h1').length,                // must be exactly 1
    imgWithoutAltOnPage: [...document.querySelectorAll('img')].filter(i => !i.hasAttribute('alt')).length,
    deprecatedTags: [...new Set([...document.querySelectorAll('acronym,applet,basefont,bgsound,big,blink,center,dir,font,frame,frameset,isindex,keygen,listing,marquee,menuitem,multicol,nextid,nobr,noembed,noframes,plaintext,spacer,strike,tt,xmp')].map(e => e.tagName.toLowerCase()))],
    splwpkOnIcon: [...document.querySelectorAll('i')].filter(i => [...i.attributes].some(a => a.name.startsWith('splwpk-'))).map(i => [...i.attributes].find(a => a.name.startsWith('splwpk-')).name),
    myGovLinks: [...new Set([...document.querySelectorAll('a[href*="malaysia.gov.my"]')].map(a => a.href))].slice(0, 5), // manual: link to https://www.malaysia.gov.my
    masthead: !!document.querySelector('#masthead, .masthead'),
    splwpk: [...new Set((document.documentElement.outerHTML.match(/splwpk-[a-z0-9-]+/g) || []))],
    searchForm: !!document.querySelector('form[role=search], input[type=search]'),
    myGovLink: [...document.querySelectorAll('a[href]')].some(a => /malaysia\.gov\.my/.test(a.href)),
    metaDescription: !!document.querySelector('meta[name=description]'),
    headingFont: getComputedStyle(m.querySelector('h1') || m).fontFamily,
    bodyFont: getComputedStyle(document.body).fontFamily,
    horizontalOverflow: document.documentElement.scrollWidth > innerWidth + 1,
  };
})()
```

Then:
- **Forms:** submit each form empty. Expect `aria-invalid="true"` on bad fields, an error message linked through `aria-describedby`, and an error summary with `role="alert"` that receives focus (MYDS `design-text-input`: hint text, error state).
- **Mobile:** repeat at 375px width. Check for horizontal overflow and stacked layout (SPLaSK "device responsiveness").
- **Keyboard:** Tab through one page. Focus must be visible, follow a logical order, and never get trapped.
- **Contrast:** body text needs at least 4.5:1, large text and UI parts at least 3:1.
- **SPLaSK tags from the server:** `curl -s <url> | grep -o 'splwpk-[a-z0-9-]*' | sort -u`. Tags injected by JavaScript may not be seen by the crawler.
- **CSS classes (non-React projects):** `python scripts/mgwg.py check-classes <templates> --css <project.css>`.

Automated checks give evidence, not verdicts. Look at the pages too.

### 3. What to check, and where it comes from

| Area | Check | Guide |
|---|---|---|
| Government identity | Official masthead, exact wording | `masthead-html` |
| SPLaSK tagging | Correct `splwpk-*` names, server-rendered, real timestamps | `splask-tagging` |
| SPLaSK features | Search form, feedback form, privacy policy (link on every page + dedicated page), sitemap, contact details, exact MyGov link, real "last updated" date; home-page SEO (title < 70, description < 160, one `<h1>`, all `alt`, viewport, no deprecated tags); no `splwpk-*` on `<i>` | `splask-criteria-checklist`, `splask-tagging` |
| SPLaSK operations | The crawler's IP is whitelisted, Criteria URLs are registered, the SerpAPI token is set, Matomo tracking is on every page | `splask-operations` |
| Accessibility | Labels, one `<h1>`, landmarks, skip link, errors, table headers, focus, contrast, target size ≥ 24×24px (WCAG 2.5.8; inline text links are exempt) | `develop-accessibility` |
| MYDS look | Poppins/Inter, tokens, 12-8-4 grid, light mode default | `myds-plain-html-php`, `design-typography`, `design-color` |

### 4. Internal staff systems: what must hold, what can bend

MYDS was written mainly for public sites. For back-office tools (dashboards, data entry, approval workflows):
- **Must hold:** accessibility (WCAG 2.2: labels, keyboard, focus, contrast, errors), bilingual interface, light mode default, government identity on any page that can be reached without login.
- **Can bend, but report as a deviation:** heading sizes (dense tools often use smaller headings than MYDS's 36px `<h1>`), full-width layouts instead of the 1280px max, and compact tables.
- **Decision, not a finding:** agency branding versus MYDS fonts and colours. Raise it as a question (SKILL.md "Conflicts"). Don't mark it as a failure.

### 5. Report format

1. **Scope and method:** pages, roles and viewports checked; guides used; tools.
2. **Does SPLaSK apply?** Portal, online service, or internal, with the reason.
3. **What already meets the standard:** a table with evidence. Credit good work; it tells the team what to keep.
4. **Gaps:** separate tables for SPLaSK and MYDS. Each row has an ID, the gap, the **evidence** (element, URL or measured value) and the fix.
5. **Decisions for the user:** conflicts and scope questions, with options. Not decided by the reviewer.
6. **Priority order.**
7. **`### Panduan Web Kerajaan`:** the guides that shaped the review, plus open compliance items.

## Bahasa Melayu

### 1. Sebelum mula: tanya, jangan andaikan
- **Bahasa laporan:** BM, BI, atau kedua-duanya.
- **Skop:** halaman awam sahaja, atau semua skrin dan peranan?
- **Jenis sistem:** *portal* agensi (SPLaSK terpakai sepenuhnya), *perkhidmatan dalam talian kerajaan* (kriteria GOS terpakai), atau *sistem dalaman staf* (MYDS dan kebolehcapaian terpakai; kriteria laman web SPLaSK kebanyakannya tidak). Jika tidak pasti, laporkan item SPLaSK sebagai "terpakai jika dibuka kepada awam", bukan sebagai kegagalan.

### 2. Semakan automatik
Jalankan skrip di atas pada setiap halaman dan peranan. Kemudian:
- hantar borang kosong (semak `aria-invalid`, mesej ralat dan ringkasan ralat);
- uji pada lebar 375px;
- uji navigasi papan kekunci;
- semak kontras;
- semak tag `splwpk-*` dalam HTML daripada pelayan;
- jalankan `check-classes`.

### 3. Sistem dalaman
- **Wajib:** kebolehcapaian WCAG 2.2, dwibahasa, mod cerah sebagai lalai, identiti kerajaan pada halaman yang boleh dicapai tanpa log masuk.
- **Boleh dilonggarkan, tetapi dilaporkan:** saiz tajuk, susun atur lebar penuh, jadual padat.
- **Keputusan pengguna, bukan dapatan:** jenama agensi berbanding fon dan warna MYDS.

### 4. Format laporan
Skop dan kaedah → Adakah SPLaSK terpakai → Yang sudah mematuhi → Jurang (SPLaSK, MYDS) dengan bukti → Keputusan untuk pengguna → Keutamaan → `### Panduan Web Kerajaan`.
