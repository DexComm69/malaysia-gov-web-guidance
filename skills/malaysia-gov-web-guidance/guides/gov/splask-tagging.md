---
id: splask-tagging
title: "SPLaSK tagging: every splwpk-* tag, its rules and timestamps (per the official SPLaSK 2.0 tagging manual)"
title_ms: "Tagging SPLaSK: setiap tag splwpk-*, syarat dan timestamp (mengikut Manual Tagging SPLaSK 2.0 rasmi)"
category: gov
keywords: "splask tagging penandaan splwpk attribute atribut timestamp crawler url tagging search-function advanced-search-function feedback-form privacy-policy sitemap w3c multilang mobile-apps broadcast news gov-policies about-us faq client-charter contact-details open-data publication online-services electronic-archive publicising freedom procurement online-e-participation criteria url icon i element"
description: "Exact syntax and conditions for every splwpk-* tag the SPLaSK crawler reads, taken from JDN's Manual Tagging SPLaSK V2.0: which element, which extra conditions (form, link text, freshness window, no <i>), timestamps, Criteria URL, and common mistakes. Use whenever building a header, footer, home page, search, feedback form or content listing for a gov site."
description_ms: "Sintaks dan syarat setiap tag splwpk-* yang dibaca oleh crawler SPLaSK, mengikut Manual Tagging SPLaSK V2.0 (JDN)."
sources: "Manual Tagging Sistem Pemantauan Laman Web dan Perkhidmatan Dalam Talian (SPLaSK) V2.0, Jabatan Digital Negara (32 slides; criteria definitions and code examples); Manual Penggunaan SPLaSK for Webmaster / Supervisor (Criteria URL); live HTML of www.jdn.gov.my and www.digital.gov.my"
authority: "Jabatan Digital Negara (official manual)"
status: current
retrieved: 2026-11-25
---

# SPLaSK tagging / Tagging SPLaSK

## English

SPLaSK's crawler finds most criteria by looking for **custom HTML attributes named `splwpk-<criterion>`**. If a feature exists but its tag is missing or misspelled, SPLaSK scores the criterion as failed. Everything below follows JDN's *Manual Tagging SPLaSK V2.0*.

### Syntax

The attribute's value repeats its name. Updated-content criteria add a separate `timestamp` attribute, `YYYY-MM-DD HH:MM:SS` (24-hour):

```html
<form action="/carian" role="search" splwpk-search-function="splwpk-search-function">…</form>
<li splwpk-news="splwpk-news" timestamp="2026-11-24 09:15:00">…</li>
<a href="/peta-laman" splwpk-sitemap="splwpk-sitemap">Peta Laman</a>
```

The manual's own examples put tags on `<a>`, `<li>`, `<ul>`, `<div>`, `<small>`, `<form>` and headings. Some live portals also add a `splwpk-<tag>-timestamp` twin. The manual doesn't use it, so it isn't needed (though it's harmless).

Render the timestamp from the content's real `updated_at`, never a hard-coded value or `now()`:

```php
<li splwpk-news="splwpk-news" timestamp="<?= htmlspecialchars(date('Y-m-d H:i:s', strtotime($n['updated_at']))) ?>">…</li>
```

### Tags and their conditions (Manual Tagging SPLaSK V2.0)

| Criterion (dimension) | Tag | Conditions in the manual |
|---|---|---|
| Search Function (Ease of Use) | `splwpk-search-function` | **On the `<form>` element itself** (manual example: `<form splwpk-search-function="…">`) |
| Advanced Search Option (Ease of Use) | `splwpk-advanced-search-function` | On the advanced-search `<form>` element |
| W3C Disability Accessibility (Ease of Use) | `splwpk-w3c` | On the wrapper of the accessibility controls. Offer at least one of: change text size, change font, change background colour (snippet below) |
| Multi-Language for Content (Accessibility) | `splwpk-multilang` | On the language switcher (manual example: a `<div>` wrapping the BM/EN links). Content available in BM and English |
| Sitemap (Accessibility) | `splwpk-sitemap` | Tag not on an `<i>` element |
| Mobile Apps (Accessibility) | `splwpk-mobile-apps` | On a link to the app's page in **GAMMA** (gamma.malaysia.gov.my). Link text = the app's name in GAMMA. At least one app |
| Presence of Datasets (Quality of Content) | `splwpk-open-data` | At least one link to a dataset that **exists on data.gov.my**. Link text = the dataset's **exact title** there |
| Publication (Quality of Content) | `splwpk-publication` | Publications offered as an eBook or a download |
| Updated Content: Broadcast | `splwpk-broadcast` + `timestamp` | Announcements updated within the last **30 days** |
| Updated Content: About Us | `splwpk-about-us` + `timestamp` | Within **30 days**; changes to the Minister, Deputy Minister or senior management must be updated **immediately** |
| Updated Content: News / Government policies | `splwpk-news` and/or `splwpk-gov-policies` + `timestamp` | Updated within **30 days** of the announcement |
| Updated Content: FAQ | `splwpk-faq` + `timestamp` | An FAQ exists |
| Updated Content: Client Charter | `splwpk-client-charter` + `timestamp` | The charter shown **with its achievement for the previous 60 days** |
| Updated Content: Contact Details | `splwpk-contact-details` + `timestamp` | Updated within **30 days** |
| Number of Online Services (Quality of Content) | `splwpk-online-services` | On links with an `href`, **shown on the home page** (the URL isn't checked for working) |
| Electronic Archive (Quality of Content) | `splwpk-electronic-archive` | URL must work; tag not on `<i>` |
| Publicising Agency CIO/CDO (Quality of Content) | `splwpk-publicising` + `timestamp` | Updated within **30 days**; URL must work; tag not on `<i>` |
| Freedom of Information (Quality of Content) | `splwpk-freedom` | Information on freedom-of-information law. URL must work |
| Online Procurement Announcement (Quality of Content) | `splwpk-procurement` | Tag not on `<i>` |
| Online E-Participation (Quality of Content) | `splwpk-online-e-participation` | An e-participation policy or guideline must be provided there; tag not on `<i>` |
| Privacy Policy (Privacy/Security) | `splwpk-privacy-policy` | **Two parts:** (1) on the privacy-policy *link*, on every page and especially the home page; (2) a dedicated privacy page whose heading (H1–H6) contains the keyword *privasi* or *privacy*, with that heading tagged too |
| Feedback Form (Responsiveness) | `splwpk-feedback-form` | **On the feedback `<form>` element itself** (manual example). A tagged *link* to a form doesn't count. If the form lives on another page, tag the `<form>` there and register that page as a **Criteria URL** |

**Not tagged; the crawler measures these itself:** Active Link, Device Responsiveness, SEO, Find Website Using Search Tool, Link to MyGov Portal, HTTPS Availability, Downtime and Loading Time. See `splask-criteria-checklist` for their rules.

**Not in the official manual:** `splwpk-pdpa` and `seo-h1` come from a third-party Joomla module. They're harmless, but they don't score anything.

### Ready-made W3C control (plain HTML)

```html
<div class="a11y-tools" role="group" aria-label="Saiz tulisan" splwpk-w3c="splwpk-w3c">
  <button type="button" data-fs="0.875">A-</button>
  <button type="button" data-fs="1">A</button>
  <button type="button" data-fs="1.25">A+</button>
</div>
<script>
  document.querySelectorAll('[data-fs]').forEach(b => b.addEventListener('click', () => {
    document.documentElement.style.fontSize = (16 * b.dataset.fs) + 'px';
    localStorage.setItem('fs', b.dataset.fs);
  }));
  if (localStorage.getItem('fs')) document.documentElement.style.fontSize = (16 * localStorage.getItem('fs')) + 'px';
</script>
```

Size text in `rem` so it scales. A contrast or background toggle (adding a class on `<html>`) also satisfies the criterion.

### Rules of thumb

1. **Don't put tags on `<i>` icon elements.** The manual rules this out for several criteria, and some live portals get it wrong (for example a feedback tag on an icon). Search, advanced search and feedback go on their `<form>`; link-type criteria go on the `<a>`.
2. **Render tags on the server** (PHP, or server-side React). Tags added later by JavaScript may not be seen by the crawler.
3. **Where tags go:** by default the crawler reads the home page. Global items (search, multilang, w3c, privacy-policy link, sitemap, feedback) belong in the shared header and footer. If a criterion's tag lives on another page, the SPLaSK webmaster registers that page as a **Criteria URL** in the site profile (SPLaSK user manual).
4. A timestamp must show a **real** update, and that update must fall inside the window above. A fake or auto-refreshed date defeats the criterion.
5. **Spell tags exactly** as in the table. Live portals have typos the crawler won't match (`splwpk-elecronic-archive`, `splwpk-advanced-search-funtion`).
6. Invisible markers must be out of the tab order and the accessibility tree: use `hidden` or `display:none`, not `aria-hidden` on a focusable link.
7. **Verify** with View Source, or `curl -s https://site | grep -o 'splwpk-[a-z0-9-]*' | sort -u`. Then run an **On-Demand Assessment** in SPLaSK (see `splask-operations`).

## Bahasa Melayu

Crawler SPLaSK mengesan kebanyakan kriteria melalui **atribut HTML `splwpk-<kriteria>`**. Ciri tanpa tag yang betul dikira gagal. Kandungan di atas mengikut *Manual Tagging SPLaSK V2.0* (JDN).

**Sintaks:** nilai atribut sama dengan namanya. Kriteria *Updated Content* memerlukan atribut berasingan `timestamp="YYYY-MM-DD HH:MM:SS"`.

**Syarat utama:**
- Carian, carian terperinci dan maklum balas mesti menggunakan `<form>`.
- W3C: sekurang-kurangnya satu kemudahan, iaitu tukar saiz tulisan, jenis tulisan atau warna latar.
- Set data: pautan ke set data yang wujud di data.gov.my, dengan teks pautan sama dengan tajuk set data.
- Aplikasi mudah alih: pautan ke GAMMA, dengan teks sama dengan nama aplikasi.
- *Broadcast*, *About Us*, berita/dasar kerajaan, *Contact Details* dan CIO: dikemas kini dalam **30 hari**. Perubahan menteri dan pengurusan atasan: **serta-merta**.
- Piagam pelanggan: dipaparkan bersama pencapaian **60 hari** sebelumnya.
- Perkhidmatan dalam talian: dipaparkan di halaman utama, dengan `href`.
- Arkib elektronik, CIO dan *Freedom of Information* (`splwpk-freedom`): URL mesti berfungsi.
- **Jangan letak tag pada elemen `<i>`** (ikon).
- Dasar privasi: tag pada pautan di semua halaman, **dan** halaman khas dengan tajuk (H1–H6) mengandungi perkataan *privasi*/*privacy* yang turut ditag.
- Tag di halaman lain selain halaman utama perlu didaftarkan sebagai **Criteria URL** dalam profil laman web SPLaSK.
- `splwpk-pdpa` dan `seo-h1` tiada dalam manual rasmi.
