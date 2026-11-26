---
id: bm-ui-glossary
title: "Bahasa Melayu interface glossary for government websites"
title_ms: "Glosari antara muka Bahasa Melayu untuk laman web kerajaan"
category: gov
keywords: "bahasa melayu bm glossary glosari terjemahan translation ui interface antara muka label butang button menu footer masthead log masuk daftar hantar carian peta laman dasar privasi soalan lazim hubungi kami maklum balas kemas kini e-mel dbp dewan bahasa ejaan spelling tarikh bulan month"
description: "Standard Bahasa Melayu wording for the parts of a government site that repeat everywhere: masthead, navigation, SPLaSK page names, buttons, form labels and messages, dates. Each term says where it comes from (MYDS's own Malay strings, the SPLaSK guides, or common government usage) and where MYDS differs from Dewan Bahasa dan Pustaka spelling."
description_ms: "Istilah Bahasa Melayu piawai untuk bahagian laman kerajaan yang berulang: masthead, navigasi, nama halaman SPLaSK, butang, label borang dan mesej, tarikh."
sources: "MYDS documentation site locale strings: github.com/govtechmy/myds apps/docs/locales/ms.ts and en.ts (retrieved 2026-11-26) ; this skill's splask-criteria-checklist and splask-tagging (page names) ; Dewan Bahasa dan Pustaka spelling (prpm.dbp.gov.my) for the spelling notes"
authority: "MYDS / GovTech Malaysia (terms marked MYDS); this skill (terms marked SPLaSK); common usage (terms marked Common: check against the agency's own style)"
status: current
retrieved: 2026-11-26
---

# Bahasa Melayu interface glossary / Glosari antara muka Bahasa Melayu

## English

Use these when writing UI text for a government site, so the same thing has the same name on every page and every agency site. The **Source** column says how firm each term is:
- **MYDS**: the Malay string MYDS itself uses on design.digital.gov.my. Use it as is.
- **SPLaSK**: the page names used throughout this skill's SPLaSK guides (and on most agency portals). Use these for the pages SPLaSK looks for.
- **Common**: wording widely used on Malaysian government sites, but not from an official list. Prefer the agency's own style guide if it has one.

BM is the default language of a government site, with an English switch (see `splask-tagging` for `splwpk-multilang`: only when the English content really exists).

**Spelling notes (Dewan Bahasa dan Pustaka).** Two MYDS strings differ from the standard DBP spelling; use the DBP form in new text unless the agency has decided otherwise:
- *kemas kini* (two words), not *kemaskini*: "Kemas Kini Terakhir".
- *e-mel*, not *emel*.

**MYDS error to avoid:** the MYDS site labels the Modal component *Modul*. In Malay *modul* means "module"; a modal dialog is a *dialog* or *tetingkap dialog*.

### Masthead and identity

| English | Bahasa Melayu | Source |
|---|---|---|
| Official Malaysia Government Website | Portal Rasmi Kerajaan Malaysia | MYDS |
| Here's how you know | Kenal pasti begini | MYDS |
| Official government websites end with .gov.my | Pautan portal rasmi berakhir dengan .gov.my | MYDS |
| Secure websites use HTTPS | Portal yang selamat menggunakan HTTPS | MYDS |
| Look for the lock icon | Periksa ikon kunci mangga | MYDS |

### Navigation and SPLaSK page names

| English | Bahasa Melayu | Source |
|---|---|---|
| Home | Laman Utama | MYDS |
| About Us | Tentang Kami | SPLaSK |
| News | Berita | SPLaSK |
| Announcements | Pengumuman / Hebahan | SPLaSK |
| Frequently Asked Questions | Soalan Lazim | SPLaSK |
| Contact Us | Hubungi Kami | SPLaSK |
| Feedback | Maklum Balas | SPLaSK |
| Sitemap | Peta Laman | SPLaSK |
| Privacy Policy | Dasar Privasi | MYDS |
| Disclaimer | Penafian | MYDS |
| Security Policy | Dasar Keselamatan | Common |
| Client Charter | Piagam Pelanggan | SPLaSK |
| Publications | Penerbitan | SPLaSK |
| Archive | Arkib | SPLaSK |
| Tenders and Quotations | Tender dan Sebut Harga | SPLaSK |
| e-Participation | e-Penyertaan | SPLaSK |
| Online Services | Perkhidmatan Dalam Talian | SPLaSK |
| Open Data | Data Terbuka | SPLaSK |
| Advanced Search | Carian Terperinci | SPLaSK |
| Search | Carian (field) / Cari (button) | Common |
| Skip to main content | Langkau ke kandungan utama | Common |

### Footer

| English | Bahasa Melayu | Source |
|---|---|---|
| All Rights Reserved | Hak Cipta Terpelihara | MYDS |
| Last Updated | Kemas Kini Terakhir (MYDS writes *Kemaskini Terakhir*) | MYDS, DBP spelling |
| Personal Data Protection | Perlindungan Data Peribadi | MYDS |
| Your Privacy | Privasi Anda | MYDS |
| Information Collected | Maklumat Yang Dikumpul | MYDS |
| Policy Change | Pindaan Dasar | MYDS |

### Actions and buttons

| English | Bahasa Melayu | Source |
|---|---|---|
| Submit | Hantar | MYDS |
| Send your feedback | Kirimkan maklum balas anda | MYDS |
| Continue | Teruskan | Common (MYDS uses *Tutup*, "Close", for its success modal) |
| Close | Tutup | MYDS |
| Cancel | Batal | Common |
| Save | Simpan | Common |
| Edit | Kemas Kini / Sunting | Common |
| Delete | Padam | Common |
| Back | Kembali | Common |
| Next / Previous | Seterusnya / Sebelumnya | Common (the MYDS docs use both) |
| Download | Muat Turun | Common |
| Upload | Muat Naik | Common |
| Print | Cetak | Common |
| Log in / Log out | Log Masuk / Log Keluar | Common |
| Register | Daftar | Common |
| Forgot password? | Lupa kata laluan? | Common |
| Copied | Disalin | MYDS |

### Forms and messages

| English | Bahasa Melayu | Source |
|---|---|---|
| Name | Nama | MYDS |
| Email | E-mel (MYDS writes *Emel*) | MYDS, DBP spelling |
| Phone number | Nombor telefon | Common |
| IC number (MyKad) | Nombor kad pengenalan (MyKad) | Common |
| Address | Alamat | Common |
| Message | Mesej | Common |
| Required | Wajib diisi | Common |
| Optional | Pilihan | Common |
| Name can only contain letters and spaces. | Nama hanya boleh mengandungi huruf dan ruang. | MYDS |
| This email has already been registered. | E-mel ini telah didaftarkan. | MYDS (DBP spelling) |
| Failed to submit. Please try again later. | Gagal menghantar. Sila cuba lagi nanti. | MYDS |
| Successfully sent! | Berjaya dihantar! | MYDS |
| Thank you | Terima kasih | MYDS |
| We'll contact you soon | Kami akan hubungi anda | MYDS |
| Page not found | Halaman tidak dijumpai | MYDS |
| The page you are looking for does not exist. | Halaman yang anda cari tidak wujud. | MYDS |
| Search by name | Cari mengikut nama | MYDS |
| All | Semua | MYDS |

### Dates

Write dates as *19 Februari 2024* (day, full month name, year), as MYDS does. Short month names in BM: Jan, Feb, **Mac**, Apr, **Mei**, Jun, Jul, **Ogo**, Sep, **Okt**, Nov, **Dis** (bold: different from English). MYDS uses *DIS 2024* and *MAC 2025*. This is for the text people read; SPLaSK `timestamp` attributes always use `YYYY-MM-DD HH:MM:SS`.

## Bahasa Melayu

Gunakan glosari ini semasa menulis teks antara muka laman kerajaan supaya perkara yang sama mempunyai nama yang sama di setiap halaman dan setiap laman agensi. Lajur **Sumber**:
- **MYDS**: teks Bahasa Melayu yang digunakan oleh MYDS sendiri di design.digital.gov.my.
- **SPLaSK**: nama halaman yang digunakan dalam panduan SPLaSK skill ini (dan kebanyakan portal agensi).
- **Common**: penggunaan lazim di laman kerajaan, bukan daripada senarai rasmi. Utamakan gaya bahasa agensi sendiri jika ada.

**Ejaan (Dewan Bahasa dan Pustaka):** gunakan *kemas kini* (dua perkataan) dan *e-mel*, walaupun MYDS menulis *kemaskini* dan *emel*. **Elakkan** label *Modul* bagi komponen Modal seperti di laman MYDS; gunakan *dialog* atau *tetingkap dialog*.

**Tarikh** ditulis *19 Februari 2024*. Singkatan bulan: Jan, Feb, Mac, Apr, Mei, Jun, Jul, Ogo, Sep, Okt, Nov, Dis. Atribut `timestamp` SPLaSK tetap dalam format `YYYY-MM-DD HH:MM:SS`.

Jadual istilah ada dalam bahagian English di atas (lajur Bahasa Melayu).
