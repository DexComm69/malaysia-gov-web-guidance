---
id: splask-criteria-checklist
title: "SPLaSK criteria checklist: what a gov website and online service must have"
title_ms: "Senarai semak kriteria SPLaSK: keperluan laman web dan perkhidmatan dalam talian kerajaan"
category: gov
keywords: "splask criteria kriteria checklist senarai semak website gos online service quality content ease of use privacy security responsiveness reliability accessibility loading time downtime browser compatibility active link device responsiveness seo search engine mygov portal datasets publication feedback form privacy policy e-rating quick link help"
description: "The 24 SPLaSK criteria (15 website and 15 GOS, of which 6 are shared) mapped to concrete implementation tasks, tags and checks. Use when planning, building or auditing any Malaysian public-sector site or online service."
description_ms: "24 kriteria SPLaSK dipetakan kepada tugasan pelaksanaan, tag dan semakan."
sources: "malaysia.gov.my SPLaSK page, Rajah 1 'Kriteria SPLaSK'; JDN Info Kerajaan Digital Siri 32; MYDS docs (design.digital.gov.my) for implementation"
authority: "Jabatan Digital Negara"
status: current
retrieved: 2026-11-25
---

# SPLaSK criteria checklist / Senarai semak kriteria SPLaSK

## English

The criteria diagram (Rajah 1, malaysia.gov.my) splits the 24 criteria into **Website (15)** and **GOS, Government Online Service (15)**, with 6 criteria shared between them. The diagram predates SPLaSK V2.0 (2022). V2.0 tags seen on live portals add items such as procurement, mobile apps, multilang and e-participation; see `splask-tagging`.

### Website-only criteria (9)

| Dimension | Criterion | Build it like this | Tag |
|---|---|---|---|
| Quality of Content | Updated content | News, announcements, About Us, contact details, FAQ and client charter are kept current, and the home page shows their last-updated date | `splwpk-news`, `splwpk-broadcast`, `splwpk-about-us`, `splwpk-contact-details`, `splwpk-faq`, `splwpk-client-charter` + `timestamp` |
| Quality of Content | Presence of datasets | Link to the agency's open datasets (data.gov.my) | `splwpk-open-data` |
| Quality of Content | Publication | A publications page (reports, circulars, brochures) | `splwpk-publication` |
| Ease of Use | Search function | A working site search on every page, in the header | `splwpk-search-function` (+ `splwpk-advanced-search-function`) |
| Ease of Use | Link to MyGov portal | A visible link to www.malaysia.gov.my (usually footer) | (no tag seen; JDN's link is tagged `splwpk-online-services`) |
| Ease of Use | Find website using search tool | The site appears in search-engine results for the agency name: unique `<title>`, meta description, one `<h1>`, `sitemap.xml`, crawlable `robots.txt` | `splwpk-sitemap` |
| Ease of Use | W3C disability accessibility | WCAG-conformant pages plus an accessibility tool (text size, contrast). MYDS targets WCAG 2.2 | `splwpk-w3c` |
| Privacy/Security | Privacy policy | A privacy policy page (and a PDPA statement) linked from the footer | `splwpk-privacy-policy`, `splwpk-pdpa` |
| Responsiveness | Feedback form | An online feedback form (not only an email address) | `splwpk-feedback-form` |

### Shared criteria (6), measured by SPLaSK itself without tags

| Dimension | Criterion | Build it like this |
|---|---|---|
| Reliability | Loading time | Keep pages light: compress images, defer non-critical JS, cache static assets. Check with PageSpeed Insights |
| Reliability | Downtime | Monitor uptime and report the SLA % in the SPLaSK profile. Plan maintenance windows |
| Accessibility | Browser compatibility | Test current Chrome, Edge, Firefox and Safari. Don't depend on one browser (many gov sites still say "best viewed in Chrome/Edge"; avoid that) |
| Accessibility | Active link | No broken links: run a link checker before release and periodically |
| Accessibility | Device responsiveness | Responsive layout on the MYDS 12-8-4 grid (desktop ≥1024px 12 columns; tablet 768–1023px 8 columns; mobile ≤767px 4 columns) |
| Accessibility | Search engine optimisation | Semantic HTML, a descriptive `<title>` and meta description, a single `<h1>`, `lang="ms"` / `lang="en"` set correctly, an XML sitemap |

### GOS-only criteria (9), for online services

Quality of Content: understandable content, accuracy of content · Web Design: look and feel · Ease of Use: quick link · Responsiveness: responsiveness to enquiries, **availability of GOS e-Rating**, aid/tools/help resources, **feedback auto-notification** (acknowledge every submission automatically) · Privacy/Security: online service security (HTTPS, secure login, session handling).

### Also expected on every gov portal (MYDS)

- The official **masthead** ("Official Malaysia Government Website" / "Portal Rasmi Kerajaan Malaysia") at the very top. See `masthead-html`.
- A standard footer containing the agency logo, address, contact details, social links, privacy policy, disclaimer and sitemap. See `develop-footer` and `design-intro`.
- Light mode supported by default (MYDS style configuration). Dark mode is optional.

## Bahasa Melayu

Rajah 1 (malaysia.gov.my) membahagikan 24 kriteria kepada **Laman Web (15)** dan **GOS, Perkhidmatan Dalam Talian Kerajaan (15)**; 6 kriteria dikongsi oleh kedua-duanya.

**Laman web sahaja:**
- *Quality of Content*: kandungan dikemas kini (dengan *timestamp*), kehadiran set data, penerbitan.
- *Ease of Use*: fungsi carian, pautan ke portal MyGov (www.malaysia.gov.my), laman web boleh ditemui melalui enjin carian, kebolehcapaian W3C untuk OKU.
- *Privacy/Security*: dasar privasi.
- *Responsiveness*: borang maklum balas.

**Dikongsi (diukur sendiri oleh SPLaSK, tanpa tag):** masa muat (*loading time*), *downtime*, keserasian pelayar, pautan aktif, responsif pada peranti, SEO.

**GOS sahaja:** kandungan mudah difahami, ketepatan kandungan, rupa dan rasa (*look and feel*), pautan pantas, respons kepada pertanyaan, ketersediaan GOS e-Rating, bantuan dan sumber rujukan, notifikasi automatik maklum balas, keselamatan perkhidmatan dalam talian.

**Turut dijangka (MYDS):** *masthead* rasmi di bahagian paling atas, *footer* standard, dan mod cerah sebagai lalai.

Rajah 1 (rasmi / official): https://www.malaysia.gov.my/my/my-initiative/whole-government-digital-services/pemantauan/sistem-pemantauan-laman-web-dan-perkhidmatan-dalam-talian-kerajaan-splask
