<div align="center">

# Malaysia Government Web Guidance

**A Claude skill for building and auditing Malaysian public-sector websites against MYDS and SPLaSK 2.0**

<p>
  <a href="https://github.com/DexComm69/malaysia-gov-web-guidance/releases/latest"><img alt="Release" src="https://img.shields.io/github/v/release/DexComm69/malaysia-gov-web-guidance?style=for-the-badge&logo=github&label=release&color=2ea043"></a>
  <a href="https://github.com/DexComm69/malaysia-gov-web-guidance/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/DexComm69/malaysia-gov-web-guidance?style=for-the-badge&logo=github&color=e3b341"></a>
  <a href="https://github.com/DexComm69/malaysia-gov-web-guidance/commits/main"><img alt="Last commit" src="https://img.shields.io/github/last-commit/DexComm69/malaysia-gov-web-guidance?style=for-the-badge&logo=git&logoColor=white&color=0969da"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/github/license/DexComm69/malaysia-gov-web-guidance?style=for-the-badge&logo=opensourceinitiative&logoColor=white&color=8250df"></a>
</p>
<p>
  <img alt="SPLaSK 2.0" src="https://img.shields.io/badge/SPLaSK-2.0-c8102e?style=for-the-badge">
  <img alt="MYDS" src="https://img.shields.io/badge/MYDS-1.0-2563eb?style=for-the-badge">
  <img alt="Claude skill and plugin" src="https://img.shields.io/badge/Claude-Skill%20%26%20Plugin-D97757?style=for-the-badge&logo=claude&logoColor=white">
  <img alt="Python 3.8+" src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img alt="Docs in BM and English" src="https://img.shields.io/badge/Docs-BM%20%7C%20EN-010066?style=for-the-badge">
</p>

English · [Bahasa Melayu](#bahasa-melayu)

</div>

> [!IMPORTANT]
> **Unofficial project.** This skill is not developed, endorsed or maintained by Jabatan Digital Negara (JDN), GovTech Malaysia or any government agency. It summarises and links to the official sources, and **the official sources take precedence** wherever they differ: [design.digital.gov.my](https://design.digital.gov.my) for MYDS, and your agency's SPLaSK supervisor for SPLaSK.

## Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Coverage](#coverage)
- [Sources and accuracy](#sources-and-accuracy)
- [Validation](#validation)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Licence](#licence)
- [Bahasa Melayu](#bahasa-melayu)

## Overview

Official Malaysian public-sector websites, from ministries to local councils, are expected to meet two standards:

| Standard | Owner | What it requires |
|---|---|---|
| **MYDS**: Malaysia Government Design System | GovTech Malaysia / JDN | Official masthead, colour tokens, Poppins/Inter typography, the 12-8-4 grid, accessible components |
| **SPLaSK 2.0**: Sistem Pemantauan Laman Web dan Servis Kerajaan | JDN | 25 criteria across 6 dimensions, assessed by an automated crawler that detects most criteria through `splwpk-*` HTML attributes |

Neither standard is well represented in general-purpose AI models. Without guidance, models invent SPLaSK tag names that the crawler will never match, and paraphrase the official masthead text. This skill gives Claude the official rules, the MYDS documentation and tools to check its own output.

## Features

<table>
  <tr>
    <td align="center" width="20%"><h3>25</h3>SPLaSK 2.0 criteria</td>
    <td align="center" width="20%"><h3>~115</h3>MYDS pages, read live</td>
    <td align="center" width="20%"><h3>9</h3>hand-written guides</td>
    <td align="center" width="20%"><h3>16 / 16</h3>trigger tests passed</td>
    <td align="center" width="20%"><h3>BM · EN</h3>bilingual throughout</td>
  </tr>
</table>

<table>
  <tr>
    <td valign="top" width="33%">

### Guidance <img src="assets/icons/guidance.svg" width="24" height="24" align="top" alt="">

- **Official SPLaSK 2.0 rules** from JDN's tagging manual and user manuals: placement, timestamps, freshness windows, SEO limits, crawler access.
- **MYDS documentation**, searchable in English and Malay and fetched live from design.digital.gov.my.
- **Ready-made patterns:** masthead, BM/EN switch, public forms with PDPA notice, status lookups, audits.
- **Works with any stack:** plain PHP / HTML / Blade, or React / Next.js.

</td>
    <td valign="top" width="33%">

### Tooling <img src="assets/icons/tooling.svg" width="24" height="24" align="top" alt="">

- **`scan`:** a SPLaSK 2.0 pre-check of a live site, reading the server HTML the way the crawler does.
- **`check-classes`:** catches CSS classes that MYDS doesn't define, in PHP, Blade or JS-built markup.
- **`tokens`:** every MYDS colour token with its light and dark value.
- **`search` / `retrieve` / `prefetch`**, with retries and an offline cache.
- Python 3.8+, standard library only.

</td>
    <td valign="top" width="33%">

### Behaviour <img src="assets/icons/behaviour.svg" width="24" height="24" align="top" alt="">

- **Asks before deciding** conflicts, such as agency branding versus MYDS colours.
- **Never invents facts** the rules depend on, like URLs or dates; it leaves TODOs instead.
- **Asks the report language** (BM, English or both) before writing one.
- **Shows its work:** every answer ends with a *Panduan Web Kerajaan* section listing the rules applied and any open items.

</td>
  </tr>
</table>

## Installation

| Environment | Steps |
|---|---|
| **Claude app** (claude.ai, desktop, mobile) | Download `malaysia-gov-web-guidance.skill` from the [latest release](https://github.com/DexComm69/malaysia-gov-web-guidance/releases/latest), open it in Claude and select **Save skill**. Code execution must be enabled. |
| **Claude Code**: plugin (recommended) | `/plugin marketplace add DexComm69/malaysia-gov-web-guidance`<br>`/plugin install malaysia-gov-web-guidance@malaysia-gov-web-guidance` |
| **Claude Code**: manual | Copy `skills/malaysia-gov-web-guidance/` to `~/.claude/skills/` (all projects) or `.claude/skills/` (one project). |

**Requirements:** Python 3.8 or later. Network access the first time each MYDS page is read; pages are then cached for 7 days. Run `prefetch all` before working offline.

## Usage

### With Claude

The skill activates automatically for Malaysian public-sector work. Example requests:

- "Build a staff login page in plain PHP for our council portal, following government design rules."
- "Create header.php and footer.php for our agency site. It must pass SPLaSK, with BM by default and an EN switch."
- "Our portal failed SPLaSK last month. Fix index.html."
- "Semak index.html ini untuk pematuhan MYDS dan SPLaSK."

### Command line

```sh
cd skills/malaysia-gov-web-guidance
python scripts/mgwg.py scan https://www.example.gov.my --follow
```

| Command | Purpose |
|---|---|
| `scan <url-or-file> [--follow] [--json]` | SPLaSK 2.0 pre-check of a page (`--follow` also checks the privacy page) |
| `search "<query>"` | Rank guides for a task (English or Malay) |
| `retrieve <id>[,<id>] [--lang en\|ms\|both]` | Print guides; MYDS pages are fetched live |
| `list [--category <name>]` | List all guides |
| `check-classes <files> [--css <file>]` | Find CSS classes not defined by MYDS 1.0.0 |
| `tokens [--filter <prefix>]` | List MYDS theme tokens with light and dark values |
| `prefetch all\|<category>\|<ids>` | Cache MYDS pages for slow or offline use |

Example `scan` output (abridged):

```text
FAIL  Tag spelling            `splwpk-search-funtion` is not an official tag; did you mean `splwpk-search-function`?
FAIL  Feedback Form           `splwpk-feedback-form` is on an <i> element (1x); tag the link/element itself
FAIL  Commented-out tags      tags that exist only inside HTML comments <!-- --> (switched off): splwpk-sitemap
FAIL  Updated Content: News   newest timestamp 2024-11-02 is 752 days old (limit 30)
FAIL  SEO                     <title> is 94 characters (must be under 70)
PASS  Updated Content: About Us  `splwpk-about-us` found (1x); newest timestamp 2026-11-10, 14 days old (limit 30)
```

## Coverage

| Guide | Scope |
|---|---|
| `splask-overview` | What SPLaSK is, who it applies to, the 6 dimensions |
| `splask-tagging` | Every `splwpk-*` tag: placement, conditions, timestamps |
| `splask-criteria-checklist` | All 25 criteria, including the rules the crawler measures directly |
| `splask-operations` | Crawler whitelisting, site profile, Criteria URL, assessments, error statuses |
| `audit-checklist` | Reviewing an existing site: scope, automated checks, report format |
| `service-form-pattern` | Public submission and lookup forms: validation, PDPA notice, acknowledgement |
| `masthead-html` | The official masthead in HTML/PHP with the exact BM/EN wording |
| `myds-plain-html-php` | Using MYDS without React: stylesheet, tokens, grid, typography |
| `myds-react-nextjs` | MYDS React components, tags in JSX/TSX, BM/EN routing |
| `design-*`, `develop-*` | About 115 MYDS documentation pages, read live from the official site |

## Sources and accuracy

| Source | Used for |
|---|---|
| *Manual Tagging SPLaSK V2.0*, JDN | Tags, criteria, conditions and crawler rules |
| *Manual Penggunaan SPLaSK* (Webmaster, Supervisor), JDN | Operations: access, site profile, assessments |
| [design.digital.gov.my](https://design.digital.gov.my) and [github.com/govtechmy/myds](https://github.com/govtechmy/myds) | MYDS documentation, tokens, components |
| SPLaSK pages on malaysia.gov.my and jdn.gov.my | Background and the GOS criteria |

The official manuals are summarised in this project's own words and are not redistributed; ask your agency's SPLaSK supervisor or JDN for copies. The full source list and known discrepancies are in [`references/sources.md`](skills/malaysia-gov-web-guidance/references/sources.md).

## Validation

Each release is tested by having Claude complete realistic tasks with and without the skill.

| Test | Result |
|---|---|
| Review of a 7-role staff system (63 page and role combinations) | Report produced; skill issues fixed in 1.1.0 |
| Public PHP application form, built from scratch | Exact masthead wording, correct tags, accessible validation |
| Next.js page with MYDS React components | All 11 imports matched the published `@govtechmy/myds-react` exports |
| Trigger test: 16 prompts in English, BM and Manglish | 16/16: the skill activated for all 8 government tasks and none of the 8 near-misses |
| `scan` on 5 live government portals | Real issues found (misspelled tags, tags inside HTML comments, stale timestamps); false alarms fixed |
| Fixing a page with 15 seeded faults | 25 fails reduced to 12 with the skill, against 17 without it; the run without the skill also invented two tag names |

See [`CHANGELOG.md`](CHANGELOG.md) for details.

## Limitations

- `scan` is a **pre-check**. It hasn't yet been calibrated against an official SPLaSK on-demand assessment, which remains the only authoritative score.
- `scan` checks one page at a time and doesn't run JavaScript. It doesn't yet check broken links, data.gov.my dataset titles or GAMMA app names.
- The GOS (online service) criteria are taken from the older criteria diagram on malaysia.gov.my, not from the v2.0 tagging manual.
- The MYDS page index reflects the documentation as of November 2026.
- A few manual rules are terse and have been interpreted conservatively (for example "under 70 characters" for titles).

## Roadmap

```mermaid
flowchart TB
    subgraph shipped ["Released"]
        direction LR
        v10["<b>v1.0</b><br/>MYDS + SPLaSK<br/>guides, EN / BM"]
        v11["<b>v1.1</b><br/>Audit checklist,<br/>service forms"]
        v12["<b>v1.2</b><br/>React / Next.js,<br/>trigger-tested 16/16"]
        v13["<b>v1.3</b><br/>Official SPLaSK 2.0<br/>manual rules"]
        v14["<b>v1.4</b><br/>scan command"]
        v10 --> v11 --> v12 --> v13 --> v14
    end

    subgraph next ["Next"]
        direction LR
        cal["Calibrate scan against<br/>an official SPLaSK assessment"]
        ci["Automated regression<br/>tests in CI"]
        cal ~~~ ci
    end

    subgraph later ["Later"]
        direction LR
        scanplus["scan: broken links,<br/>data.gov.my titles,<br/>GAMMA app names"]
        upd["update-index for<br/>new MYDS pages"]
        cms["WordPress &<br/>Joomla guides"]
        idm["MyDigital ID<br/>sign-in"]
        bm["BM interface<br/>glossary"]
        scanplus ~~~ upd ~~~ cms ~~~ idm ~~~ bm
    end

    shipped --> next --> later

    classDef done fill:#dcfce7,stroke:#16a34a,color:#14532d,stroke-width:2px
    classDef nxt fill:#fef9c3,stroke:#ca8a04,color:#713f12,stroke-width:2px
    classDef plan fill:#e0e7ff,stroke:#4f46e5,color:#1e1b4b,stroke-width:1px,stroke-dasharray:4 3
    class v10,v11,v12,v13,v14 done
    class cal,ci nxt
    class scanplus,upd,cms,idm,bm plan
    style shipped fill:transparent,stroke:#16a34a,stroke-width:2px
    style next fill:transparent,stroke:#ca8a04,stroke-width:2px
    style later fill:transparent,stroke:#4f46e5,stroke-width:1px,stroke-dasharray:4 3
```

<sub><b>Green</b>: released · <b>Amber</b>: next up · <b>Blue, dashed</b>: planned. Full history in [CHANGELOG.md](CHANGELOG.md). Suggestions are welcome as [issues](https://github.com/DexComm69/malaysia-gov-web-guidance/issues).</sub>

## Contributing

Issues and pull requests are welcome, especially:
- corrections confirmed against an official JDN or GovTech source;
- changes in MYDS (new pages, renamed tokens) or a newer SPLaSK manual;
- improvements to the Malay wording.

Guides in `guides/gov/` keep an English and a Bahasa Melayu section, cite an official source, and record a `retrieved:` date.

## Licence

Released under the [MIT Licence](LICENSE). The licence covers this repository's own files only; see [NOTICE](NOTICE). MYDS and SPLaSK materials belong to GovTech Malaysia and JDN and are not included. "MYDS", "SPLaSK", "JDN" and "GovTech Malaysia" are used only to identify the official sources.

---

## Bahasa Melayu

**Skill Claude untuk membina dan mengaudit laman web sektor awam Malaysia mengikut MYDS dan SPLaSK 2.0.**

> [!IMPORTANT]
> **Projek tidak rasmi.** Skill ini tidak dibangunkan, disahkan atau diselenggara oleh Jabatan Digital Negara (JDN), GovTech Malaysia atau mana-mana agensi kerajaan. **Sumber rasmi diutamakan** sekiranya terdapat perbezaan: [design.digital.gov.my](https://design.digital.gov.my) bagi MYDS, dan *supervisor* SPLaSK agensi anda bagi SPLaSK.

### Gambaran keseluruhan

Laman web rasmi sektor awam perlu mematuhi **MYDS** (*masthead* rasmi, token warna, fon Poppins/Inter, grid 12-8-4, komponen mesra OKU) dan **SPLaSK 2.0** (25 kriteria dalam 6 dimensi, dinilai oleh *crawler* yang mengesan kebanyakan kriteria melalui atribut HTML `splwpk-*`). Skill ini membekalkan Claude dengan peraturan rasmi, dokumentasi MYDS dan alat semakan.

### Ciri utama

- Panduan dalam BM dan BI: kira-kira 115 halaman MYDS (dibaca terus dari laman rasmi) dan 9 panduan SPLaSK serta corak laman kerajaan.
- Peraturan SPLaSK berdasarkan *Manual Tagging SPLaSK V2.0* dan manual pengguna SPLaSK (JDN).
- Arahan `scan`: semakan awal SPLaSK 2.0 bagi laman web atau fail HTML.
- Sokongan PHP / HTML / Blade dan React / Next.js.
- Bertanya dahulu apabila berlaku konflik, tidak mereka maklumat, dan menyenaraikan perkara pematuhan yang belum selesai dalam bahagian *Panduan Web Kerajaan*.

### Pemasangan

- **Aplikasi Claude:** muat turun `malaysia-gov-web-guidance.skill` daripada [*release* terkini](https://github.com/DexComm69/malaysia-gov-web-guidance/releases/latest), buka dalam Claude dan pilih **Save skill**.
- **Claude Code:**
  ```text
  /plugin marketplace add DexComm69/malaysia-gov-web-guidance
  /plugin install malaysia-gov-web-guidance@malaysia-gov-web-guidance
  ```
- Memerlukan Python 3.8 ke atas, dan akses internet kali pertama setiap halaman MYDS dibaca.

### Had

- `scan` ialah semakan awal dan belum dikalibrasi dengan penilaian *On-Demand* SPLaSK yang rasmi.
- Kriteria GOS diambil daripada rajah kriteria lama di malaysia.gov.my.

### Lesen

[MIT](LICENSE), bagi fail repositori ini sahaja. Bahan MYDS dan SPLaSK adalah milik GovTech Malaysia dan JDN.
