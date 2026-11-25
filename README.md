# Malaysia Gov Web Guidance

**An unofficial Claude skill for building Malaysian government websites that follow MYDS and pass SPLaSK.**
English · [Bahasa Melayu](#bahasa-melayu)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Claude skill](https://img.shields.io/badge/Claude-skill-d97757)
![Languages](https://img.shields.io/badge/lang-EN%20%7C%20BM-green)

> [!IMPORTANT]
> **Unofficial.** This project is not made, endorsed or maintained by Jabatan Digital Negara (JDN), GovTech Malaysia or any Malaysian government agency. It links to and summarises the official sources. When they disagree with this skill, **the official source wins**: [design.digital.gov.my](https://design.digital.gov.my) and your agency's SPLaSK supervisor or webmaster.

---

## Why this exists

Every official Malaysian public-sector website (ministries, departments, statutory bodies, state governments and local councils) is expected to:

1. **Look and behave like a government site.** That means following **MYDS**, the Malaysia Government Design System: the official masthead, colour tokens, Poppins/Inter typography, the 12-8-4 grid and accessible components.
2. **Pass SPLaSK**, JDN's automated website monitor. It scores portals against **25 criteria** (SPLaSK 2.0), and its crawler finds most of them only through hidden HTML attributes such as `splwpk-search-function="splwpk-search-function"`. A site can have a perfect search box and still score zero if the attribute is missing or misspelled.

AI assistants know very little about either. In testing, Claude without this skill **made up SPLaSK tag names** (`splwpk-search`, `splwpk-multilingual`) that the crawler would never match, and **wrote the wrong masthead wording**. With the skill, both came out right.

## What it does

When you ask Claude to build or review something for a Malaysian government site, the skill makes Claude:

- **Search** about 120 guides (MYDS docs plus hand-written SPLaSK guides) in English or Malay, for example "borang maklum balas" or "login page".
- **Read the official MYDS page live** from design.digital.gov.my, in English and/or Bahasa Melayu.
- **Build to the rules:**
  - MYDS tokens (`rgb(var(--txt-black-900))`), fonts and grid;
  - the official masthead text ("Portal Rasmi Kerajaan Malaysia" / "Official Malaysia Government Website");
  - correctly spelled, server-rendered `splwpk-*` tags with real timestamps.
- **Work without React.** MYDS components are React-only, so the skill includes guides for plain **PHP / HTML / Blade** projects. This matters because many agencies run PHP on XAMPP or Laravel.
- **Pre-check a live site for SPLaSK** with `scan`, using the official SPLaSK 2.0 rules: missing, misspelled or misplaced tags, stale timestamps, tags hidden in HTML comments or only added by JavaScript, home-page SEO limits, viewport, HTTPS and redirects. It reads the page the way the crawler does.
- **Check your templates** for CSS classes that the published MYDS stylesheet doesn't define. Works with PHP, Blade and JavaScript-built HTML.
- **Review existing sites:** a step-by-step audit checklist with a browser check script and a report format.
- **Build public service forms** the government way: an error summary, a PDPA notice, a reference number on the acknowledgement, and e-Rating.
- **Ask before deciding.** If MYDS conflicts with your agency's branding or your project's conventions (for example MYDS blue vs your council's colours), it stops and asks you.
- **Ask which language** (BM, English or both) before writing a report or audit.
- **Show its work.** Answers end with a *Panduan Web Kerajaan* section listing the rules applied and any compliance items still open.

## Install

### Claude app (claude.ai, desktop, mobile)

1. Download **`malaysia-gov-web-guidance.skill`** from the [latest release](https://github.com/DexComm69/malaysia-gov-web-guidance/releases/latest).
2. Open it in Claude and click **Save skill**, or upload it under **Settings → Capabilities → Skills**.

Code execution must be on, because the skill runs a small Python script.

### Claude Code: as a plugin (recommended)

```text
/plugin marketplace add DexComm69/malaysia-gov-web-guidance
/plugin install malaysia-gov-web-guidance@malaysia-gov-web-guidance
```

### Claude Code: manual

Copy `skills/malaysia-gov-web-guidance/` into `~/.claude/skills/` (all projects) or `.claude/skills/` (one project).

**Requirements:** Python 3.8+ (standard library only), and internet access the first time each MYDS page is read. Pages are then cached for 7 days.

## Try it

Ask Claude things like:

- *"Build a staff login page in plain PHP for our council's portal, following government design rules."*
- *"Make header.php and footer.php for our agency site. It must pass SPLaSK, with BM by default and an EN switch."*
- *"Semak index.html ni untuk pematuhan MYDS dan SPLaSK."*
- *"Which SPLaSK criteria does our feedback page need to meet?"*

The skill turns on automatically for government work. You can also name it: *"use malaysia-gov-web-guidance"*.

## What's inside

```text
skills/malaysia-gov-web-guidance/
├── SKILL.md                     instructions Claude follows
├── scripts/mgwg.py              search / list / retrieve / prefetch / tokens / scan / check-classes (stdlib Python)
├── scripts/splask_scan.py       the SPLaSK 2.0 pre-check used by `scan`
├── guides/gov/                  hand-written guides, English + Bahasa Melayu
│   ├── splask-overview.md         what SPLaSK is, who it covers, its 6 dimensions
│   ├── splask-tagging.md          splwpk-* attributes, timestamps, pitfalls
│   ├── splask-criteria-checklist.md  the 25 criteria and their crawler rules, mapped to build tasks
│   ├── splask-operations.md       crawler whitelist, site profile, Criteria URL, assessments, errors
│   ├── service-form-pattern.md    public forms: validation, PDPA notice, reference number, e-Rating
│   ├── audit-checklist.md         how to review a site: scope, browser checks, report format
│   ├── myds-react-nextjs.md       React/Next.js: imports, tags in JSX, BM/EN routing, doc gaps
│   ├── masthead-html.md           official masthead in plain HTML/PHP, exact BM/EN wording
│   └── myds-plain-html-php.md     MYDS without React: stylesheet, tokens, grid, fonts
└── references/
    ├── myds-index.json            titles + links of ~115 MYDS pages (content fetched live)
    └── sources.md                 every source, known gaps and discrepancies
```

The script can also be used on its own:

```sh
python scripts/mgwg.py search "footer privacy policy sitemap"
python scripts/mgwg.py retrieve splask-tagging,design-12-8-4-grid --lang en
python scripts/mgwg.py check-classes templates/*.php --css assets/app.css
python scripts/mgwg.py scan https://www.example.gov.my --follow   # SPLaSK 2.0 pre-check of a live site
python scripts/mgwg.py tokens --filter otl          # MYDS token names with light/dark values
python scripts/mgwg.py prefetch all                 # cache every MYDS page for slow or offline use
```

## Accuracy and known limits

- **Tested before release:** three rounds of stress tests (a full review of a 7-role system, a PHP public form, a Next.js page) and a trigger test with 16 real prompts in English, BM and Manglish. The skill turned on for all 8 government tasks and stayed off for all 8 near-misses (a bakery site, Singapore's SGDS, SQL, deployment, generic React and others). Details in `CHANGELOG.md`.

- **The SPLaSK rules follow JDN's official *Manual Tagging SPLaSK V2.0* and the SPLaSK user manuals** (checked November 2026). If JDN publishes a newer version, please [open an issue](https://github.com/DexComm69/malaysia-gov-web-guidance/issues).
- **SPLaSK's dimensions:** the v2.0 manual confirms 6. malaysia.gov.my still describes the older model with 7, including Web Design.
- MYDS's own "SPLaSK Compliance" page, and most of its plain HTML/CSS components, are still *Work In Progress* at the source.
- **Known conflict:** MYDS's input border colour (1.27:1) is below WCAG's 3:1 for form controls. The skill raises this instead of deciding it.
- Content was reviewed on 25 November 2026. MYDS pages are always read live, but the hand-written guides can go out of date. Check `references/sources.md`.

## Contributing

Corrections are welcome, especially:
- tag names or rules confirmed against the official SPLaSK tagging manual;
- changes to MYDS (new pages, renamed tokens);
- better Malay wording in the guides.

Keep both language sections in `guides/gov/*.md`, cite an official source, and update `retrieved:`.

## Licence

[MIT](LICENSE), covering this repository's own files only (see [NOTICE](NOTICE)). MYDS documentation, code and assets belong to GovTech Malaysia / JDN, and SPLaSK material belongs to JDN. This repository doesn't copy them: it links to them or reads them from the official websites when it runs. "MYDS", "SPLaSK", "JDN" and "GovTech Malaysia" are named only to identify the official sources.

---

## Bahasa Melayu

**Skill Claude tidak rasmi untuk membina laman web kerajaan Malaysia yang mematuhi MYDS dan lulus penilaian SPLaSK.**

> [!IMPORTANT]
> **Tidak rasmi.** Projek ini tidak dibangunkan, disahkan atau diselenggara oleh Jabatan Digital Negara (JDN), GovTech Malaysia atau mana-mana agensi kerajaan. Jika berbeza dengan sumber rasmi, **sumber rasmi diutamakan**: [design.digital.gov.my](https://design.digital.gov.my) serta *supervisor* atau *webmaster* SPLaSK agensi anda.

### Mengapa

Portal rasmi sektor awam (kementerian, jabatan, badan berkanun, kerajaan negeri dan PBT) perlu:
1. Mengikut **MYDS**: *masthead* rasmi, token warna, fon Poppins/Inter, grid 12-8-4 dan komponen yang mesra OKU.
2. Lulus **SPLaSK**: 24 kriteria. Kebanyakannya dikesan melalui atribut HTML `splwpk-*`. Ciri yang wujud tanpa tag yang betul dikira **tiada**.

Tanpa skill ini, Claude mereka nama tag SPLaSK yang salah dan menulis teks *masthead* yang tidak rasmi.

### Apa yang dilakukan

- Mencari kira-kira 120 panduan dalam BM atau BI, dan membaca halaman MYDS terus daripada laman rasmi.
- Membina mengikut peraturan: token dan fon MYDS, teks *masthead* rasmi, dan tag `splwpk-*` dengan ejaan tepat serta *timestamp* sebenar.
- Menyokong projek **PHP / HTML / Blade** tanpa React.
- **Bertanya dahulu** jika MYDS bercanggah dengan jenama agensi atau konvensyen projek anda.
- **Bertanya bahasa** laporan (BM, BI atau kedua-duanya) sebelum menulis.
- Menyenaraikan peraturan yang digunakan dan perkara pematuhan yang belum selesai dalam bahagian *Panduan Web Kerajaan*.

### Pemasangan

- **Aplikasi Claude:** muat turun `malaysia-gov-web-guidance.skill` daripada [*release* terkini](https://github.com/DexComm69/malaysia-gov-web-guidance/releases/latest), buka dalam Claude, dan klik **Save skill**.
- **Claude Code:**
  ```text
  /plugin marketplace add DexComm69/malaysia-gov-web-guidance
  /plugin install malaysia-gov-web-guidance@malaysia-gov-web-guidance
  ```
- Memerlukan Python 3.8+ dan akses internet kali pertama setiap halaman MYDS dibaca.

### Had

Peraturan SPLaSK mengikut *Manual Tagging SPLaSK V2.0* dan manual pengguna SPLaSK rasmi (JDN). Jika versi baharu diterbitkan, sila buka [*issue*](https://github.com/DexComm69/malaysia-gov-web-guidance/issues).

### Lesen

[MIT](LICENSE), bagi fail repositori ini sahaja. Kandungan MYDS dan SPLaSK tertakluk kepada syarat pemiliknya.
