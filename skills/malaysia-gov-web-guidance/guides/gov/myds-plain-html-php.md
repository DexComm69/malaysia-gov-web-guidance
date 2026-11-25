---
id: myds-plain-html-php
title: "Using MYDS in plain HTML / PHP / Blade (no React, no build step)"
title_ms: "Menggunakan MYDS dalam HTML / PHP / Blade biasa (tanpa React)"
category: gov
keywords: "myds php html css blade laravel xampp plain vanilla no react cdn jsdelivr myds-style tokens colour color rgb var font inter poppins grid 12-8-4 breakpoints light dark theme setup install stylesheet utility classes purged"
description: "How to get MYDS look and tokens into a PHP/HTML project without React: pinned stylesheet, fonts, the rgb(var(--token)) pattern, the 12-8-4 grid in CSS, light-mode default, and why some Tailwind classes are missing. Start here for any non-React gov project."
description_ms: "Cara menggunakan token dan gaya MYDS dalam projek PHP/HTML tanpa React."
sources: "https://design.digital.gov.my/en/docs/develop/install ; /style-configuration ; /design/12-8-4-grid ; /design/typography ; /design/color ; npm @govtechmy/myds-style@1.0.0 (dist/index.css) ; github.com/govtechmy/myds packages/style"
authority: "MYDS, GovTech Malaysia / Jabatan Digital Negara"
status: current
retrieved: 2026-11-25
---

# Using MYDS in plain HTML / PHP / Blade / Menggunakan MYDS tanpa React

## English

MYDS ships two packages: `@govtechmy/myds-style` (CSS: tokens plus utility classes) and `@govtechmy/myds-react` (components). The official guides assume React (Next.js, Vite, or Laravel with Inertia/React). For a plain PHP project (XAMPP, CodeIgniter, Blade without React), use **only the style package**, plus the HTML/CSS ("transitory assistance", `ta-*`) components where they exist.

### 1. Load fonts and the stylesheet

```html
<!-- MYDS typefaces: Poppins for headings, Inter for body (style-configuration) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=Poppins:ital,wght@0,400;0,500;0,600;1,400;1,500;1,600&display=swap">
<!-- Pin the version; self-host this file for intranet/offline servers -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@govtechmy/myds-style@1.0.0/dist/index.css">
<link rel="stylesheet" href="/assets/css/app.css"><!-- your own CSS, after MYDS -->
```

For servers without internet access, which is common on agency intranets, download `dist/index.css` and the font files into the project and link them locally. This skill's `check-classes` command downloads the same file and caches it.

### 2. Use tokens, not hex codes

Tokens are CSS custom properties holding **space-separated RGB triplets**, so wrap them in `rgb()`:

```css
.card   { background: rgb(var(--bg-white)); border: 1px solid rgb(var(--otl-gray-200)); border-radius: 8px; }
.muted  { color: rgb(var(--txt-black-500)); }
.btn-primary { background: rgb(var(--bg-primary-600)); color: rgb(var(--txt-white)); }
.btn-primary:focus-visible { outline: 3px solid rgb(var(--fr-primary)); }
.overlay { background: rgb(var(--bg-black-900) / 0.5); } /* alpha works too */
```

Prefixes: `bg-` background, `txt-` text, `otl-` outline/border, `fr-` focus ring. Families: `white`, `washed`, `dialog`, `black-*`, `gray-*`, `primary-*`, `danger-*`, `success-*`, `warning-*`, plus `-disabled` variants. The full list is in https://github.com/govtechmy/myds/blob/main/packages/style/styles/theme/light.css. Theme tokens switch automatically under `.dark`. Primitive tokens (`--_primary-600`, …) never change.

### 3. Theme

"It is required to support the light mode by default" (style-configuration). Dark mode is optional. It applies when `class="dark"` is on `<html>`; see `develop-use-theme` / `develop-theme-switch` for behaviour.

### 4. Utility classes exist only if a MYDS component uses them

`dist/index.css` is a purged Tailwind build. Classes like `bg-bg-washed`, `text-txt-black-700`, `text-body-sm`, `max-w-screen-xl`, `rounded-md` and `font-heading` exist. Many others don't, especially layout classes: for example `grid-cols-12`, `md:grid-cols-8`, `col-span-6`, `md:flex-row`, `lg:px-8`, `min-h-screen` and `w-1/2`. So build the page grid with your own CSS (section 5). Before relying on a utility class, check it:

```sh
python <skill>/scripts/mgwg.py check-classes path/to/page.php
```

For anything missing, write a small rule in your own CSS using tokens. Don't add the Tailwind CDN script to a production gov site.

### 5. Layout: the 12-8-4 grid

| Breakpoint | Width | Columns | Gap / edge padding |
|---|---|---|---|
| Desktop | ≥ 1024px | 12 | 24px, max content width 1280px |
| Tablet | 768–1023px | 8 | 24px |
| Mobile | ≤ 767px | 4 | 18px |

Article text is capped at 640px, and images or charts inside articles at up to 740px.

```css
.container { max-width: 1280px; margin-inline: auto; padding-inline: 18px; }
.grid-myds { display: grid; gap: 18px; grid-template-columns: repeat(4, minmax(0, 1fr)); }
@media (min-width: 768px)  { .container { padding-inline: 24px; } .grid-myds { gap: 24px; grid-template-columns: repeat(8, minmax(0, 1fr)); } }
@media (min-width: 1024px) { .grid-myds { grid-template-columns: repeat(12, minmax(0, 1fr)); } }
.article { max-width: 640px; }
```

### 6. Typography

Headings use Poppins (`font-heading`): h1 36/44px, h2 30/38, h3 24/32, h4 20/28, h5 16/24, h6 14/20, in weights 400/500/600. Body text uses Inter (`font-body`): 16/24px by default, with 14/20 for small text. Retrieve `design-typography` for the full scale and rich-text styles.

### 7. Components without React

- **Available as HTML/CSS:** Button (`develop-ta-button`) and Toggle (`develop-ta-toggle`). Their CSS is in https://github.com/govtechmy/myds/blob/main/apps/docs/public/assets/ta-preview.
- **Official component is React-only; plain HTML version in this skill:** Masthead (`masthead-html`).
- **Everything else:** read the component's *design* guide (`design-<name>`) for anatomy, states and spacing, and the *develop* guide (`develop-<name>`) for structure and ARIA. Then build it in HTML with tokens. Prefer native elements (`<details>`, `<dialog>`, `<select>`, `<input type="date">`) wherever they meet the design. The other `ta-*` pages are still "Work In Progress" at the source.
- **A React-only component in a non-React project is not a conflict to ask about.** Use the native HTML element styled with MYDS tokens, for example `<input type="date">` for the date picker, and mention it in the reply. Only ask if the user specifically wants the MYDS look of that component.

### 8. Language switch

Link to the *same page* in the other language (`?lang=en` or `/en/...`), and mark each label with its own language: `<a href="?lang=en" lang="en" hreflang="en">EN</a>`. Show the current language with `aria-current="true"`, set `<html lang>` to match, and tag the wrapper `splwpk-multilang="splwpk-multilang"`. See `myds-react-nextjs` §3 for the full pattern.

### 9. Token names

To list every theme token with its light and dark value, run `python scripts/mgwg.py tokens` (or `tokens --filter otl`). Use those names instead of guessing.

### 10. Known conflict: input border contrast (MYDS vs WCAG)

MYDS outlines inputs with `otl-gray-200` (#E4E4E7, **1.27:1** on white) or `otl-gray-300` (#D4D4D8, **1.48:1**). WCAG 2.2 success criterion 1.4.11 (non-text contrast) requires **3:1** for the visual boundary that identifies a form control. A thin light-grey border is usually the only boundary of a text input, so it fails unless the field also has a distinct background fill.

This is a conflict between two official requirements, so follow SKILL.md: **ask the user**. Give the options:
- keep the MYDS border;
- use a darker token for input borders only, for example `--_gray-500` (#6B6B74, 5.28:1);
- give fields a filled background that meets 3:1 against the page.

Recommend the darker border, because accessibility is a legal and SPLaSK requirement and the visual change is small. In a non-interactive run, keep the MYDS default and list this as the first question.

## Bahasa Melayu

MYDS terdiri daripada dua pakej: `@govtechmy/myds-style` (CSS: token dan kelas utiliti) dan `@govtechmy/myds-react` (komponen React). Untuk projek PHP biasa, gunakan **pakej gaya sahaja**:

1. Muatkan fon Poppins (tajuk) dan Inter (teks), dan *stylesheet* `@govtechmy/myds-style@1.0.0/dist/index.css`. Tetapkan versi; simpan salinan setempat jika pelayan tiada akses internet.
2. Gunakan token, bukan kod hex: `color: rgb(var(--txt-black-700));`. Awalan `bg-` (latar), `txt-` (teks), `otl-` (garis luar), `fr-` (cincin fokus).
3. Mod cerah wajib disokong secara lalai; mod gelap pilihan melalui kelas `.dark` pada `<html>`.
4. *Stylesheet* ini ialah binaan Tailwind yang dipangkas, jadi tidak semua kelas utiliti wujud. Semak dengan `mgwg.py check-classes`, dan tulis CSS sendiri menggunakan token untuk kelas yang tiada.
5. Grid 12-8-4: desktop ≥1024px 12 lajur (jarak 24px, lebar maksimum 1280px); tablet 768–1023px 8 lajur (24px); mudah alih ≤767px 4 lajur (18px). Lebar teks artikel maksimum 640px.
6. Komponen HTML/CSS rasmi setakat ini hanya Butang dan *Toggle*. Gunakan `masthead-html` untuk *masthead*. Komponen lain dibina sendiri berdasarkan panduan reka bentuk MYDS. Komponen yang hanya ada dalam React (contoh: pemilih tarikh) diganti dengan elemen HTML asli yang digayakan dengan token MYDS; ini bukan konflik yang perlu ditanya.
7. Senarai nama token: `python scripts/mgwg.py tokens`.
8. **Konflik diketahui:** warna garis luar medan input MYDS (`otl-gray-200`, 1.27:1) gagal syarat kontras WCAG 1.4.11 (3:1). Tanya pengguna: kekalkan warna MYDS, guna garis lebih gelap (contoh `--_gray-500`, 5.28:1), atau beri medan latar berwarna.
