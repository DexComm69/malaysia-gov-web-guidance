---
id: splask-operations
title: "Running SPLaSK: crawler access, site profile, Criteria URL, assessments, errors, analytics"
title_ms: "Mengendalikan SPLaSK: akses crawler, profil laman web, Criteria URL, penilaian, ralat, analitik"
category: gov
keywords: "splask operations webmaster supervisor whitelist ip firewall crawler error status 404 curl error 28 timeout port 80 443 pdsa mygovcloud gitn mygovosf profile profil laman web criteria url serpapi token tracking code matomo piwik api token on-demand assessment scheduler marks markah downtime sla maintenance production mode go-live launch"
description: "The operational side of SPLaSK for webmasters and developers: whitelisting the crawler, registering the site profile and Criteria URLs, the SerpAPI token, the Matomo tracking code, on-demand vs scheduled assessments, reading error statuses, and registering planned downtime. Use when launching a gov site, when SPLaSK shows errors or no marks, or when tags are correct but the score doesn't change."
description_ms: "Sisi operasi SPLaSK untuk webmaster: whitelist IP crawler, profil laman web, Criteria URL, SerpAPI, kod penjejakan Matomo, penilaian, ralat dan downtime berjadual."
sources: "Manual Penggunaan SPLaSK for Webmaster, Supervisor (Agensi) and Supervisor (HQ), Jabatan Digital Negara; Manual Tagging SPLaSK V2.0"
authority: "Jabatan Digital Negara (official manuals)"
status: current
retrieved: 2026-11-25
---

# Running SPLaSK / Mengendalikan SPLaSK

## English

Correct tags are only half of SPLaSK. The other half is set up by the agency's SPLaSK **webmaster** and **supervisor** in the SPLaSK system (https://splask.jdn.gov.my). A developer should know these steps, because "the tags are right but the score is zero" is usually one of them.

### 1. Let the crawler in (mandatory)
- SPLaSK's crawler must be **allowed through the firewall on ports 80 and 443**. Sites hosted in the public-sector data centre (PDSA) request this through MyGovCloud; sites on the government network (GITN/MyGovNet) request it through MyGovOSF.
- **The crawler's IP addresses are listed in the SPLaSK user manual** (slide 4) that JDN gives to registered webmasters. Get them from your agency's SPLaSK supervisor. Don't guess.
- If the crawler can't reach the site, **no assessment happens at all**. The common error statuses:

| Error shown in SPLaSK | Likely cause |
|---|---|
| `HTTP request returned status code 404` | The URL is dead or the document root is misconfigured, **or** the crawler's IP isn't whitelisted |
| `cURL error 28 … Connection timed out` | The crawler's IP isn't whitelisted |
| `Failed to connect … port 80: No route to host` | The web server isn't listening on port 80, or the IP isn't whitelisted |

### 2. The site profile
- **Official Website URL.** The name is read from the page `<title>` (another reason it should be under 70 characters).
- **CMS type.**
- **SerpAPI token:** needed for *Find Website Using Search Tool*. SPLaSK uses a free SerpAPI account (100 searches a month) to check that the site ranks in Google's top 10 for its full name.
- **Criteria URL:** if a criterion's tag isn't on the home page, register the page that has it (choose the tag, enter the URL). Otherwise the crawler won't find it.
- **Mode:** the tracking code and API token appear only when the profile is in **Production** mode. Changing the mode changes the tracking ID.

### 3. Analytics: the tracking code
SPLaSK's web analytics use **Matomo**. Paste the tracking code from the profile on **every page**, just before `</head>`. If the site already uses Matomo, follow Matomo's guide for multiple trackers so the two don't conflict.

### 4. Assessments
- **Scheduled:** automatic crawling at times SPLaSK sets.
- **On-Demand:** run by the webmaster at any time to check fixes. Statuses are Queue, Running and Completed. A site page shows its Current and Previous marks.
- After changing tags, **deploy first, then run an on-demand assessment** and open the detailed results to see which conditions failed.

### 5. Planned downtime
Register scheduled maintenance in the site profile **before** it starts, for example 48 hours. That period then isn't counted in the downtime score (`100 − downtime_minutes / 1440 × 100`). Announce it on another official channel too.

### 6. Integration
The profile's **API token** lets other systems read the site's SPLaSK marks, for example to show them on the agency's own site.

## Bahasa Melayu

1. **Whitelist IP crawler SPLaSK** pada port 80 dan 443 (wajib). Hosting di PDSA: mohon melalui MyGovCloud. Persekitaran GITN: mohon melalui MyGovOSF. Senarai IP terdapat dalam manual pengguna SPLaSK (slaid 4), yang boleh diperoleh daripada *supervisor* SPLaSK agensi. Tanpa akses, tiada penilaian dibuat (ralat 404, cURL 28 atau *No route to host*).
2. **Profil laman web:** URL rasmi, jenis CMS, token SerpAPI (untuk kriteria carian Google), **Criteria URL** bagi tag yang tiada di halaman utama, dan mod *Production*.
3. **Kod penjejakan Matomo** pada setiap halaman, sebelum `</head>`.
4. **Penilaian:** *Scheduler* (automatik) atau *On-Demand* (bila-bila masa). Selepas membetulkan tag, buat *deploy* dahulu, kemudian jalankan *On-Demand*.
5. **Downtime berjadual:** daftarkan dalam profil sebelum penyelenggaraan supaya tidak dikira.
6. **Token API:** untuk memaparkan markah SPLaSK di sistem lain.
