---
id: splask-overview
title: "SPLaSK: what it is, who it applies to, how agencies are judged"
title_ms: "SPLaSK: apa itu, siapa terlibat, bagaimana agensi dinilai"
category: gov
keywords: "splask monitoring pemantauan dimensions dimensi criteria kriteria agency responsibilities tanggungjawab agensi jdn mampu pkpa probe muse gos e-rating osi egdi pbt"
description: "Background for any Malaysian public-sector website: SPLaSK (Sistem Pemantauan Laman Web dan Servis Kerajaan) automatically checks official agency portals against 24 criteria. Read before building or auditing a gov site."
description_ms: "Latar belakang bagi laman web sektor awam: SPLaSK memantau portal rasmi agensi secara automatik berdasarkan 24 kriteria."
sources: "https://www.malaysia.gov.my/my/my-initiative/whole-government-digital-services/pemantauan/sistem-pemantauan-laman-web-dan-perkhidmatan-dalam-talian-kerajaan-splask ; https://www.jdn.gov.my/hebahan-info-kerajaan-digital-siri-32-sistem-pemantauan-laman-web-dan-servis-kerajaan-splask/ ; JDN infographic 'Info Kerajaan Digital Siri 32' (attached to the JDN notice)"
authority: "Jabatan Digital Negara (JDN, formerly MAMPU), Kementerian Digital"
status: current
retrieved: 2026-11-25
---

# SPLaSK: what it is, who it applies to, how agencies are judged / SPLaSK: apa itu, siapa terlibat, bagaimana agensi dinilai

## English

**What it is.** SPLaSK (*Sistem Pemantauan Laman Web dan Servis Kerajaan*; malaysia.gov.my expands it as *... Perkhidmatan Dalam Talian Kerajaan*) is JDN's platform that monitors official public-sector portals and online services, automatically and continuously, against criteria set by JDN. The results appear on dashboards for top management, ministries / State Secretary offices, and their agencies. JDN also uses SPLaSK as a benchmark for how well a portal complies when it is built.

**Who it covers.** Every public-sector agency: Federal Public Service (PAP), State Public Service (PAN), federal and state statutory bodies (BBP, BBN) and **local authorities (PBT)**. Local council portals therefore fall under SPLaSK.

**Governing circular.** The JDN notice names *PKPA Bil. 2 Tahun 2015: Pengurusan Laman Web Agensi Sektor Awam* as the guidance for managing agency portals. It also tells agencies to follow whatever portal-management circulars and guidelines are currently in force.

**Criteria and dimensions.**
- There are 24 criteria, consolidated from 47 ProBE criteria and 24 MUSE criteria.
- **The sources disagree on the number of dimensions:**
  - malaysia.gov.my (updated 23 Sep 2025, but describing the 2019 design) lists **7**: Quality of Content, Ease of Use, Privacy/Security, Responsiveness, Reliability, Accessibility, Web Design.
  - The JDN notice (12 Sep 2024) and its infographic list **6**: Reliability, Accessibility, Quality of Content, Ease of Use, Privacy/Security, Responsiveness. Web Design is no longer a dimension.
  - Treat the **6-dimension model as current**, and mention the discrepancy if the user writes formal documents (URS/SRS).
- SPLaSK V2.0 (launched 25 Oct 2022) added website-monitoring functions and criteria. Its live tags (see `splask-tagging`) include items that are not in the older criteria diagram, such as procurement, mobile apps, multilang and e-participation.

**What the agency must do (infographic, four roles):**
1. *Pengurusan Pengguna*: appoint, register and manage SPLaSK users (supervisor, webmaster).
2. *Pengurusan Laman Web*: keep the site profile current: % SLA, URL tagging, downtime.
3. *Pematuhan Kriteria*: tag the site and carry out the assessment.
4. *Maklum Balas*: give feedback on using SPLaSK.

**Contact.** splask@jdn.gov.my (JDN notice, 2024). The older address splask@digital.gov.my still appears on malaysia.gov.my.

**What this means for a developer:** the criteria map onto concrete page features, and most of them are only detected if the right `splwpk-*` attribute is in the HTML. Retrieve `splask-criteria-checklist` and `splask-tagging` next.

**Scope caution:** SPLaSK targets *official portals/websites* and *government online services (GOS)*. An internal staff module behind a login (for example a module inside an agency's staff portal) is probably not crawled as a website. However, the portal that hosts it is, and the GOS criteria (e-rating, feedback auto-notification, online service security) may apply to public-facing services. Confirm scope with the agency webmaster or the SPLaSK supervisor rather than assuming.

## Bahasa Melayu

**Apa itu.** SPLaSK ialah platform JDN yang memantau portal/laman web rasmi dan perkhidmatan dalam talian agensi Kerajaan secara kendiri, automatik, masa nyata dan berterusan, berdasarkan kriteria yang ditetapkan oleh JDN. Laporan dipaparkan dalam bentuk *dashboard* mengikut peringkat Pengurusan Atasan, Kementerian/Pejabat SUK Negeri dan agensi di bawahnya. SPLaSK juga menjadi penanda aras pematuhan kriteria dalam pembangunan portal/laman web rasmi agensi sektor awam.

**Liputan.** PAP, PAN, BBP, BBN dan **Pihak Berkuasa Tempatan (PBT)**. Portal rasmi PBT juga tertakluk kepada SPLaSK.

**Pekeliling.** Hebahan JDN merujuk *PKPA Bil. 2 Tahun 2015: Pengurusan Laman Web Agensi Sektor Awam*. Agensi juga perlu merujuk pekeliling/garis panduan pengurusan portal/laman web yang sedang berkuat kuasa.

**Kriteria dan dimensi.**
- Terdapat 24 kriteria, dimurnikan daripada 47 kriteria ProBE dan 24 kriteria MUSE.
- **Bilangan dimensi berbeza mengikut sumber:**
  - malaysia.gov.my menyenaraikan **7** dimensi, termasuk *Web Design*.
  - Hebahan JDN (12 Sep 2024) dan infografiknya menyenaraikan **6** dimensi: *Reliability, Accessibility, Quality of Content, Ease of Use, Privacy/Security, Responsiveness*.
  - Gunakan model 6 dimensi sebagai terkini, dan nyatakan perbezaan ini dalam dokumen rasmi.
- SPLaSK V2.0 dilancarkan pada 25 Oktober 2022 dengan fungsi, modul dan kriteria pemantauan laman web tambahan.

**Tanggungjawab agensi (infografik):**
1. Pengurusan Pengguna: pelantikan, pendaftaran dan pengurusan pengguna (*supervisor, webmaster*).
2. Pengurusan Laman Web: kemas kini maklumat terkini (% SLA, *URL tagging, downtime*).
3. Pematuhan Kriteria: *tagging* dan melaksanakan penilaian.
4. Maklum Balas: memberi maklum balas terhadap penggunaan sistem SPLaSK.

**Hubungi.** splask@jdn.gov.my

**Skop:** SPLaSK menilai portal/laman web rasmi dan perkhidmatan dalam talian Kerajaan (GOS). Modul dalaman yang memerlukan log masuk mungkin tidak dinilai sebagai laman web, tetapi portal induknya dinilai. Sahkan skop dengan *webmaster* atau *supervisor* SPLaSK agensi.

Infografik rasmi / official infographic: https://www.jdn.gov.my/hebahan-info-kerajaan-digital-siri-32-sistem-pemantauan-laman-web-dan-servis-kerajaan-splask/
