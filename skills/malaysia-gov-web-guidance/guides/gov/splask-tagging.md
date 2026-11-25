---
id: splask-tagging
title: "SPLaSK tagging: splwpk-* attributes and timestamps in HTML"
title_ms: "Tagging SPLaSK: atribut splwpk-* dan timestamp dalam HTML"
category: gov
keywords: "splask tagging penandaan splwpk attribute atribut timestamp crawler url tagging search-function feedback-form privacy-policy pdpa sitemap w3c multilang broadcast news about-us faq client-charter contact-details gov-policies open-data publication procurement electronic-archive e-participation online-services mobile-apps publicising seo-h1"
description: "Exact syntax for the splwpk-* attributes the SPLaSK crawler reads, the full observed tag list, which tags carry a timestamp, placement rules, and pitfalls (typos, JS-injected tags, aria-hidden links). Use whenever building a header, footer, search, feedback form or home page for a gov site."
description_ms: "Sintaks tepat atribut splwpk-* yang dibaca oleh crawler SPLaSK, senarai tag, tag yang memerlukan timestamp, dan perangkap biasa."
sources: "Live HTML of www.jdn.gov.my, www.digital.gov.my and a local-council portal (inspected 2026-11-25); ammaridris.my Joomla SPLaSK Tagging module page (third-party, 2019, updated 2021). The official 'Manual Tagging SPLaSK 2.0' PDF (melaka.gov.my mirror) could not be read: TLS certificate error."
authority: "Jabatan Digital Negara; syntax inferred from JDN's own portal"
status: current
retrieved: 2026-11-25
---

# SPLaSK tagging / Tagging SPLaSK

## English

SPLaSK's crawler finds most website criteria by looking for **custom HTML attributes named `splwpk-<criterion>`** on the page. If the feature exists but the attribute is missing, SPLaSK scores it as missing. This is what the infographic calls "URL tagging".

### Syntax (as used on JDN's own portal)

The attribute name and value are the same string. "Updated content" criteria also carry a `timestamp` attribute in `YYYY-MM-DD HH:MM:SS` (24-hour, local time):

```html
<!-- feature without freshness requirement -->
<form action="/carian" method="get" role="search"
      splwpk-search-function="splwpk-search-function"
      splwpk-advanced-search-function="splwpk-advanced-search-function">…</form>

<!-- freshness-tracked content: add timestamp = last real update of that content -->
<a href="/berita" splwpk-news="splwpk-news" timestamp="2026-11-24 09:15:00">Berita</a>
```

One portal also adds a per-tag twin, `splwpk-news-timestamp="2026-11-24 09:15:00"`, next to `timestamp`. Adding both is harmless and future-proof.

In PHP, render the timestamp from the content's real `updated_at`, never a hard-coded or `now()` value:

```php
<a href="/berita" splwpk-news="splwpk-news"
   timestamp="<?= htmlspecialchars(date('Y-m-d H:i:s', strtotime($latestNews['updated_at']))) ?>">Berita</a>
```

### Tag list (observed on live government portals, 2024–2026)

| Tag | Put it on | Timestamp seen |
|---|---|---|
| `splwpk-search-function` | the site search `<form>` | no |
| `splwpk-advanced-search-function` | same search form, or the advanced search | no |
| `splwpk-feedback-form` | the feedback form, or the link to it | no |
| `splwpk-privacy-policy` | the link to the privacy policy (usually footer) | no |
| `splwpk-pdpa` | link to the PDPA statement (community module; not seen on JDN) | no |
| `splwpk-sitemap` | link to the sitemap (`/sitemap.xml` or the HTML sitemap); digital.gov.my also uses `<meta name="splwpk-sitemap" content="splwpk-sitemap">` | no |
| `splwpk-w3c` | the accessibility toolbar or widget (font size, contrast) | no |
| `splwpk-multilang` | the language switcher (BM / EN) | no |
| `splwpk-broadcast` | announcements block or link | **yes** |
| `splwpk-news` | news block or link | **yes** |
| `splwpk-about-us` | About Us link | **yes** |
| `splwpk-contact-details` | contact details block or link | **yes** |
| `splwpk-faq` | FAQ link | **yes** |
| `splwpk-client-charter` | client charter (*Piagam Pelanggan*) link | **yes** |
| `splwpk-gov-policies` | government policies link | **yes** |
| `splwpk-online-e-participation` | e-participation (*e-Penyertaan*) link | **yes** |
| `splwpk-publicising` | page publicising the agency CIO/CDO or achievements | **yes** (a third-party guide says CIO/CDO info must be updated within 30 days; unverified) |
| `splwpk-electronic-archive` | media centre or archive link | sometimes |
| `splwpk-procurement` | tender or procurement listings | sometimes |
| `splwpk-publication` | publications page | community module only |
| `splwpk-open-data` | open data / datasets link (data.gov.my) | community module only |
| `splwpk-online-services` | links to the agency's online services | no |
| `splwpk-mobile-apps` | links to the agency's mobile apps (gamma.malaysia.gov.my listing) | no |
| `seo-h1` | the page's main `<h1>` (community module; not seen on JDN, so unverified) | no |

Not tagged; measured by SPLaSK itself: loading time, downtime, browser compatibility, device responsiveness, active links, search-engine findability. See `splask-criteria-checklist`.

### Rules of thumb

1. **Render tags server-side.** JDN and digital.gov.my emit them in the HTML response. At least one local-council portal injects some with jQuery after load. Nothing reviewed confirms that the crawler runs JavaScript, so in PHP, echo the attributes into the markup.
2. **Tag the real element** (the visible search form, the footer link) wherever possible. Then the tag stays true even if the page is redesigned.
3. If you need an invisible marker, take it out of the tab order and the accessibility tree: `<a href="/faq" splwpk-faq="splwpk-faq" timestamp="…" hidden></a>`. JDN uses `style="display:none"` on an `<a>`. Some portals put links inside `class="sr-only" aria-hidden="true"`, but a focusable link under `aria-hidden` is a WCAG failure, so don't copy that.
4. **Spell tags exactly.** Live sites have typos the crawler will not match, for example `splwpk-elecronic-archive` and `splwpk-advanced-search-funtion`. Copy names from the table above.
5. **Where tags go.** The crawler reads the **home page**, which is where all three reference portals put their tags.
   - **Shared header and footer** (search, multilang, w3c, privacy-policy, pdpa, sitemap, feedback-form): render them in the shared layout, so they appear on the home page and, harmlessly, on every inner page too.
   - **Timestamped "updated content" tags** (news, broadcast, about-us, contact-details, faq and so on) belong on the home page, where the links to that content live. Fill each timestamp from the real `updated_at` of that content.
   - **An inner service page** (a form, a listing) needs only the shared layout tags. Don't add timestamped tags there just to have them. If a real date isn't available, leave the tag out rather than inventing one.
6. A timestamp must reflect a **real content update**. A fake or auto-refreshed timestamp defeats the purpose of the "Updated Content" criterion, and auditors can compare it with the actual content.
7. After deploying, check with *View Source* or `curl -s https://site | grep -o 'splwpk-[a-z-]*' | sort -u`.

**Open question to raise with the user:** the authoritative tag list is JDN's *Manual Tagging SPLaSK 2.0*, which was not readable during research. If the user has the PDF, verify this table against it.

## Bahasa Melayu

SPLaSK mengesan kebanyakan kriteria laman web melalui **atribut HTML tersuai `splwpk-<kriteria>`**. Jika ciri wujud tetapi atribut tiada, SPLaSK menganggap ciri itu tiada. Inilah yang disebut sebagai "URL tagging" dalam infografik.

**Sintaks:** nilai atribut sama dengan namanya. Kriteria *Updated Content* memerlukan atribut `timestamp="YYYY-MM-DD HH:MM:SS"`, iaitu tarikh sebenar kandungan dikemas kini:

```html
<a href="/berita" splwpk-news="splwpk-news" timestamp="2026-11-24 09:15:00">Berita</a>
```

**Panduan:**
1. Jana atribut di pelayan (PHP), bukan disuntik dengan JavaScript.
2. Letakkan pada elemen sebenar (borang carian, pautan di *footer*).
3. Penanda tersembunyi mesti dikeluarkan daripada turutan tab: gunakan `hidden` atau `display:none`, bukan `aria-hidden` pada pautan yang boleh difokus.
4. Eja nama tag dengan tepat. Ejaan salah seperti `splwpk-elecronic-archive` tidak akan dikesan.
5. Letakkan di halaman utama.
6. *Timestamp* mesti mencerminkan kemas kini kandungan yang sebenar.
7. Semak dengan *View Source* selepas pelaksanaan.

Senarai tag rasmi terdapat dalam *Manual Tagging SPLaSK 2.0* (JDN). Sahkan jadual di atas dengan manual tersebut jika ada.
