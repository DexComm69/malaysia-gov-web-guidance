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
2. **Pass SPLaSK**, JDN's automated website monitor. It scores portals against **24 criteria**, and its crawler finds most of them only through hidden HTML attributes such as `splwpk-search-function="splwpk-search-function"`. A site can have a perfect search box and still score zero if the attribute is missing or misspelled.

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
- **Check your templates** for CSS classes that the published MYDS stylesheet doesn't define.
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
├── scripts/mgwg.py              search / list / retrieve / check-classes (stdlib Python)
├── guides/gov/                  hand-written guides, English + Bahasa Melayu
│   ├── splask-overview.md         what SPLaSK is, who it covers, the 6 vs 7 dimensions
│   ├── splask-tagging.md          splwpk-* attributes, timestamps, pitfalls
│   ├── splask-criteria-checklist.md  the 24 criteria mapped to build tasks
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
```

## Accuracy and known limits

- **The SPLaSK tag list is evidence-based, not official.** It comes from the live HTML of government portals (including JDN's own), because JDN's *Manual Tagging SPLaSK 2.0* could not be obtained. If you have the manual, please [open an issue](https://github.com/DexComm69/malaysia-gov-web-guidance/issues) so the list can be checked.
- **The sources disagree on SPLaSK's dimensions.** malaysia.gov.my lists 7 (including Web Design); JDN's 2024 notice lists 6. The skill uses 6 and points out the difference.
- MYDS's own "SPLaSK Compliance" page, and most of its plain HTML/CSS components, are still *Work In Progress* at the source.
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

Senarai tag SPLaSK diambil daripada HTML portal kerajaan yang sedang beroperasi, kerana *Manual Tagging SPLaSK 2.0* tidak dapat diperoleh. Jika anda mempunyai manual tersebut, sila buka [*issue*](https://github.com/DexComm69/malaysia-gov-web-guidance/issues).

### Lesen

[MIT](LICENSE), bagi fail repositori ini sahaja. Kandungan MYDS dan SPLaSK tertakluk kepada syarat pemiliknya.
