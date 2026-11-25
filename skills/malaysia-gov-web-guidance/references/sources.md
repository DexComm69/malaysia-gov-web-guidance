# Sources

Every guide was checked against these sources on **2026-11-25**. This skill doesn't copy any of the official documents: MYDS pages are read live from the official site, and the hand-written guides summarise the official sources in their own words.

## Official sources

| Source | Used for |
|---|---|
| MYDS documentation: https://design.digital.gov.my/en/docs/design and /en/docs/develop (Malay: /ms/docs/...) | All `design-*` and `develop-*` guides (fetched live); `myds-plain-html-php`, `masthead-html` |
| MYDS source: https://github.com/govtechmy/myds (token CSS, HTML/CSS components, masthead locale strings, flag icon) | `myds-plain-html-php`, `masthead-html` (short official strings quoted for exact wording) |
| npm `@govtechmy/myds-style@1.0.0` (`dist/index.css`, via jsDelivr) | `check-classes` (downloaded at run time) |
| SPLaSK page on malaysia.gov.my: https://www.malaysia.gov.my/my/my-initiative/whole-government-digital-services/pemantauan/sistem-pemantauan-laman-web-dan-perkhidmatan-dalam-talian-kerajaan-splask | `splask-overview`, `splask-criteria-checklist` (Rajah 1) |
| JDN notice *Info Kerajaan Digital Siri 32: SPLaSK* (12 Sep 2024) and its infographic: https://www.jdn.gov.my/hebahan-info-kerajaan-digital-siri-32-sistem-pemantauan-laman-web-dan-servis-kerajaan-splask/ | `splask-overview` |

## Supporting evidence

- Live HTML of www.jdn.gov.my, www.digital.gov.my and a local-council portal, inspected for `splwpk-*` attributes.
- A third-party Joomla "SPLaSK Tagging" module page (ammaridris.my, 2019; updated 2021), for tag names not seen on the portals above (`splwpk-pdpa`, `splwpk-publication`, `splwpk-open-data`, `seo-h1`).

## Known gaps

- **The official tagging manual was not read.** *Manual Tagging SPLaSK 2.0* could not be obtained (a mirrored copy failed with a TLS certificate error). The tag table in `splask-tagging` is evidence-based but unofficial.
- **6 vs 7 dimensions.** malaysia.gov.my lists 7 (including Web Design); JDN's 2024 notice and infographic list 6. The guides treat 6 as current and say so.
- **Contact email.** splask@jdn.gov.my (2024) vs splask@digital.gov.my (malaysia.gov.my).
- MYDS's own "SPLaSK Compliance" page and 15 of the 17 HTML/CSS component pages are "Work In Progress" at the source.
- PKPA Bil. 2/2015 is referred to but not summarised. It may have been replaced; check the agency's current circulars.

## Updating

- MYDS pages need no update, because they are always read live. If MYDS adds or renames pages, regenerate `references/myds-index.json` (id, category, EN/MS titles, URLs, section headings) from the docs navigation.
- Hand-written guides: edit `guides/gov/*.md`, keep both language sections, and bump `retrieved`.
