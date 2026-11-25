---
id: masthead-html
title: "Official government masthead in plain HTML/PHP (no React)"
title_ms: "Masthead rasmi kerajaan dalam HTML/PHP biasa (tanpa React)"
category: gov
keywords: "masthead header pengepala official malaysia government website portal rasmi kerajaan here's how you know kenal pasti begini gov.my https lock flag jalur gemilang php blade html plain"
description: "Drop-in masthead for PHP/Blade/HTML sites using MYDS classes and the official EN/MS wording, built on <details> so it works without JavaScript. Use at the top of every Malaysian government page."
description_ms: "Masthead sedia guna untuk laman PHP/HTML dengan kelas MYDS dan teks rasmi BM/EN."
sources: "https://design.digital.gov.my/en/docs/develop/masthead ; github.com/govtechmy/myds packages/react/src/components/masthead.tsx ; apps/docs/locales/en.ts and ms.ts (Masthead strings) ; packages/react/src/svg/icons/malaysia-flag.svg"
authority: "MYDS, GovTech Malaysia / Jabatan Digital Negara"
status: current
retrieved: 2026-11-25
---

# Official government masthead / Masthead rasmi kerajaan

## English

MYDS defines the masthead as "a standardized header for Malaysian government websites": a thin bar above the site header with the Malaysian flag, the line "Official Malaysia Government Website", and a "Here's how you know" toggle that explains `.gov.my` and HTTPS. The official component is React-only (`@govtechmy/myds-react/masthead`). The markup below reproduces it for PHP/HTML using the classes from the published MYDS stylesheet (see `myds-plain-html-php`).

**Wording: use it verbatim (from the MYDS locale files):**

| Key | English | Bahasa Melayu |
|---|---|---|
| title | Official Malaysia Government Website | Portal Rasmi Kerajaan Malaysia |
| trigger | Here's how you know | Kenal pasti begini |
| official (heading) | Official government websites end with .gov.my | Pautan portal rasmi berakhir dengan .gov.my |
| official (body) | If the link does not end with .gov.my, exit the website immediately even if it looks similar. | Sekiranya anda melihat pautan selain .gov.my, segera tutupkan halaman itu walaupun ia menyerupai portal rasmi! |
| secure (heading) | Secure websites use HTTPS | Portal yang selamat menggunakan HTTPS |
| secure (body) | Look for the lock icon (🔒) or https:// as an added precaution. If not present, leave the site immediately. | Periksa ikon kunci mangga (🔒) atau https:// di depan pautan. Sekiranya tiada, tinggalkan laman sesawang serta merta. |

**Markup (PHP; `$lang` is `'ms'` or `'en'`):**

```php
<?php $m = [
  'ms' => ['title' => 'Portal Rasmi Kerajaan Malaysia', 'how' => 'Kenal pasti begini',
           'off_h' => 'Pautan portal rasmi berakhir dengan .gov.my',
           'off_b' => 'Sekiranya anda melihat pautan selain .gov.my, segera tutupkan halaman itu walaupun ia menyerupai portal rasmi!',
           'sec_h' => 'Portal yang selamat menggunakan HTTPS',
           'sec_b' => 'Periksa ikon kunci mangga (🔒) atau https:// di depan pautan. Sekiranya tiada, tinggalkan laman sesawang serta merta.'],
  'en' => ['title' => 'Official Malaysia Government Website', 'how' => "Here's how you know",
           'off_h' => 'Official government websites end with .gov.my',
           'off_b' => 'If the link does not end with .gov.my, exit the website immediately even if it looks similar.',
           'sec_h' => 'Secure websites use HTTPS',
           'sec_b' => 'Look for the lock icon (🔒) or https:// as an added precaution. If not present, leave the site immediately.'],
][$lang]; ?>
<details id="masthead" class="masthead bg-bg-washed print:hidden" data-nosnippet>
  <summary class="mx-auto flex max-w-screen-xl items-center gap-2 px-4.5 py-2 md:px-6 text-body-sm text-txt-black-700">
    <img src="/assets/img/malaysia-flag.svg" width="32" height="16" alt="" aria-hidden="true">
    <span><?= $m['title'] ?></span>
    <span class="text-txt-primary"><?= $m['how'] ?></span>
  </summary>
  <div class="mx-auto grid max-w-screen-xl gap-4.5 px-4.5 pb-6 pt-3 md:px-6 sm:grid-cols-2">
    <div>
      <p class="text-body-sm font-medium text-txt-black-900"><?= $m['off_h'] ?></p>
      <p class="text-body-sm text-txt-black-700"><?= $m['off_b'] ?></p>
    </div>
    <div>
      <p class="text-body-sm font-medium text-txt-black-900"><?= $m['sec_h'] ?></p>
      <p class="text-body-sm text-txt-black-700"><?= $m['sec_b'] ?></p>
    </div>
  </div>
</details>
```

```css
/* Every utility class above is defined in @govtechmy/myds-style 1.0.0 (checked with check-classes). */
/* <details> gives keyboard + screen-reader toggle for free; just tidy the marker */
.masthead > summary { cursor: pointer; list-style: none; }
.masthead > summary::-webkit-details-marker { display: none; }
.masthead > summary:focus-visible { outline: 2px solid rgb(var(--fr-primary)); outline-offset: -2px; }
```

Notes:
- Use the MYDS flag icon from https://github.com/govtechmy/myds/blob/main/packages/react/src/svg/icons/malaysia-flag.svg (save it as `/assets/img/malaysia-flag.svg`). Don't draw a different flag.
- `data-nosnippet` keeps search engines from using the masthead text as the page snippet (the MYDS component does the same).
- The masthead sits **above** the site's own navbar and is not part of `<header>` navigation. The skip link (`develop-skiplink`) should come before it in the DOM.
- If the project does use React, use the official component instead (`develop-masthead`).

## Bahasa Melayu

MYDS mentakrifkan *masthead* sebagai pengepala standard bagi laman web Kerajaan Malaysia. Ia ialah jalur nipis di atas pengepala laman, mengandungi bendera Malaysia, teks "Portal Rasmi Kerajaan Malaysia", dan butang "Kenal pasti begini" yang menerangkan domain `.gov.my` dan HTTPS. Komponen rasmi hanya tersedia untuk React. Markup di atas menghasilkan semula komponen itu untuk PHP/HTML menggunakan kelas daripada *stylesheet* MYDS.

- Gunakan teks rasmi dalam jadual di atas tanpa diubah.
- Gunakan ikon bendera MYDS: https://github.com/govtechmy/myds/blob/main/packages/react/src/svg/icons/malaysia-flag.svg
- `<details>`/`<summary>` membolehkan *masthead* dibuka dan ditutup dengan papan kekunci dan pembaca skrin tanpa JavaScript.
- Letakkan *masthead* di bahagian paling atas halaman, selepas *skip link* dan sebelum bar navigasi.
