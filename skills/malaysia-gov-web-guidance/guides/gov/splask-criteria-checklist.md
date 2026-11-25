---
id: splask-criteria-checklist
title: "SPLaSK criteria checklist: the 25 website criteria (SPLaSK 2.0) and GOS criteria, mapped to build tasks"
title_ms: "Senarai semak kriteria SPLaSK: 25 kriteria laman web (SPLaSK 2.0) dan kriteria GOS, dipetakan kepada tugasan pembangunan"
category: gov
keywords: "splask criteria kriteria checklist senarai semak website gos online service quality content ease of use privacy security responsiveness reliability accessibility loading time downtime active link device responsiveness seo search engine google top 10 serpapi mygov portal datasets publication feedback form privacy policy https freedom of information procurement e-participation title meta description h1 alt viewport deprecated"
description: "All SPLaSK 2.0 website criteria in 6 dimensions, from JDN's tagging manual, each with what to build, its tag, and the untagged rules the crawler measures itself (SEO limits, viewport, Google top-10, HTTPS, uptime formula, 5-second load). Plus the GOS online-service criteria. Use when planning, building or auditing any Malaysian public-sector site."
description_ms: "Semua kriteria laman web SPLaSK 2.0 dalam 6 dimensi, mengikut manual tagging JDN, serta kriteria GOS."
sources: "Manual Tagging SPLaSK V2.0, Jabatan Digital Negara; Manual Penggunaan SPLaSK (Webmaster / Supervisor) for downtime and SerpAPI; malaysia.gov.my SPLaSK page, Rajah 1, for the GOS criteria"
authority: "Jabatan Digital Negara (official manuals)"
status: current
retrieved: 2026-11-25
---

# SPLaSK criteria checklist / Senarai semak kriteria SPLaSK

## English

*Manual Tagging SPLaSK V2.0* lists **25 website criteria in 6 dimensions**. Older notices say "24 criteria"; the v2.0 manual adds *Freedom of Information*. For tags and their exact conditions, see `splask-tagging`.

### Accessibility (7)

| Criterion | What to build | Tag |
|---|---|---|
| Active Link | No broken links (pages deleted, moved or renamed) | crawler |
| Device Responsiveness | All content and functions work on mobile, **and** `<meta name="viewport" content="width=device-width, initial-scale=1">` | crawler |
| Search Engine Optimization | On the **home page**: `<title>` **under 70 characters**, `<meta name="description">` **under 160 characters**, `alt` on **every** `<img>`, **no deprecated HTML tags**, **exactly one `<h1>`** | crawler |
| Mobile Apps | A link to the app's GAMMA page, with the link text matching the app's name in GAMMA | `splwpk-mobile-apps` |
| Multi-Language for Content | BM and English content | `splwpk-multilang` |
| Sitemap | A sitemap page or file, linked | `splwpk-sitemap` |
| Find Website Using Search Tool | The site appears in **Google's top 10** for its **full official name**. SPLaSK checks this through **SerpAPI**: the webmaster adds a SerpAPI token in the SPLaSK profile. The scheduled check runs nightly at 11:15 p.m., and the search test runs on the 1st, 10th and 20th of each month | crawler |

### Ease of Use (4)

| Criterion | What to build | Tag |
|---|---|---|
| Link to MyGov Portal | A link to exactly `https://www.malaysia.gov.my` | crawler |
| Search Function | Site search as a real `<form>` | `splwpk-search-function` |
| W3C Disability Accessibility | At least one of: change text size, change font, change background colour | `splwpk-w3c` |
| Advanced Search Option | Advanced search as a `<form>` | `splwpk-advanced-search-function` |

### Quality of Content (9)

| Criterion | What to build | Tag |
|---|---|---|
| Presence of Datasets | At least one link to a dataset that exists on data.gov.my, with the link text matching its title | `splwpk-open-data` |
| Publication | Publications as an eBook or a download | `splwpk-publication` |
| Updated Content | Broadcast, About Us, News/Government policies, FAQ, Client Charter with achievement, Contact Details, each with a real timestamp inside its window (30 days; 60 days for the charter achievement) | 6 tags + `timestamp` |
| Number of Online Services | Online services linked **on the home page** | `splwpk-online-services` |
| Electronic Archive | Archive of policies, budgets, laws and past events (URL must work) | `splwpk-electronic-archive` |
| Publicising Agency CIO/CDO | CIO/CDO information, updated within 30 days | `splwpk-publicising` + `timestamp` |
| Freedom of Information | Information on freedom-of-information law | `splwpk-freedom` |
| Online Procurement Announcement | Tender and procurement announcements | `splwpk-procurement` |
| Online E-Participation | E-participation programmes, **plus an e-participation policy or guideline** | `splwpk-online-e-participation` |

### Privacy / Security (2)

| Criterion | What to build | Tag |
|---|---|---|
| Privacy Policy | A link on every page, **and** a dedicated page with a heading containing *privasi*/*privacy* | `splwpk-privacy-policy` (both) |
| HTTPS Availability | The site is reachable over HTTPS | crawler |

### Responsiveness (1)

| Criterion | What to build | Tag |
|---|---|---|
| Feedback Form | A feedback `<form>` on the site | `splwpk-feedback-form` |

### Reliability (2)

| Criterion | Rule | Tag |
|---|---|---|
| Downtime | Meet the SLA set in the SPLaSK site profile. Uptime is checked **every minute**. Score = `100 − (total_downtime_minutes / 1440 × 100)`. **Scheduled maintenance registered in the profile beforehand doesn't count.** Announce outages on another official channel (GOS Gateway or the agency's social media) | crawler |
| Loading Time | The page loads in **5 seconds or less**, as measured by SPLaSK; **at most 5 redirects** | crawler |

### GOS (government online service) criteria

From the SPLaSK criteria diagram on malaysia.gov.my. Not covered by the tagging manual.

Understandable and accurate content · look and feel · quick link · responsiveness to enquiries · **availability of GOS e-Rating** · aid, tools and help resources · **feedback auto-notification** · online service security. See `service-form-pattern`.

### Also expected on every gov portal (MYDS)

The official masthead (`masthead-html`), a standard footer, and light mode by default.

## Bahasa Melayu

*Manual Tagging SPLaSK V2.0* menyenaraikan **25 kriteria dalam 6 dimensi**:
- **Accessibility (7):** pautan aktif; responsif peranti (`meta viewport`); SEO; aplikasi mudah alih (GAMMA); pelbagai bahasa; peta laman; carian Google (10 teratas, melalui SerpAPI).
  - Syarat SEO di halaman utama: tajuk kurang 70 aksara, *meta description* kurang 160 aksara, `alt` pada semua imej, tiada tag HTML lapuk, satu `<h1>` sahaja.
- **Ease of Use (4):** pautan ke `https://www.malaysia.gov.my`, fungsi carian (`<form>`), kemudahan W3C, carian terperinci.
- **Quality of Content (9):** set data (data.gov.my), penerbitan, kandungan dikemas kini (30/60 hari), perkhidmatan dalam talian di halaman utama, arkib elektronik, CIO/CDO, *Freedom of Information*, perolehan, e-penyertaan (dengan polisi).
- **Privacy/Security (2):** dasar privasi (pautan di semua halaman + halaman khas), HTTPS.
- **Responsiveness (1):** borang maklum balas.
- **Reliability (2):**
  - *Downtime*: diperiksa setiap minit; markah 100 − (minit downtime / 1440 × 100); penyelenggaraan yang didaftarkan lebih awal dalam profil tidak dikira.
  - Masa muat: 5 saat atau kurang, maksimum 5 *redirect*.
