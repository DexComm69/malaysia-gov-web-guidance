---
id: myds-react-nextjs
title: "MYDS in React / Next.js: components, SPLaSK tags in JSX, BM/EN routing, doc gaps"
title_ms: "MYDS dalam React / Next.js: komponen, tag SPLaSK dalam JSX, laluan BM/EN, jurang dokumentasi"
category: gov
keywords: "react next.js nextjs app router tsx typescript jsx vite inertia myds-react component import splwpk attribute timestamp typescript augmentation asChild slot language switch tukar bahasa multilang hreflang locale middleware ssr server render props undocumented"
description: "How to build gov pages with the official MYDS React components: confirming imports, putting splwpk-* tags and timestamps in JSX/TSX so they survive SSR and TypeScript, building the BM/EN language switch and locale routing, and known gaps in the MYDS React docs. Use for any React, Next.js, Vite or Inertia gov project."
description_ms: "Cara membina halaman kerajaan dengan komponen React MYDS rasmi: import, tag splwpk-* dalam JSX/TSX, penukar bahasa BM/EN, dan jurang dalam dokumentasi React MYDS."
sources: "MYDS develop/install, develop/nextjs, develop/usage and each develop-<component> page; npm @govtechmy/myds-react 1.0.2 export map (40 subpath exports, checked 2026-11-25); React DOM attribute handling (custom attributes are passed through as strings since React 16); round-3 stress test of this skill (Next.js 14 App Router build)"
authority: "Unofficial synthesis; MYDS by GovTech Malaysia / JDN"
status: current
retrieved: 2026-11-25
---

# MYDS in React / Next.js / MYDS dalam React / Next.js

## English

### 1. Components and imports
- Import each component from its own subpath, e.g. `@govtechmy/myds-react/button`, and load the stylesheet once with `@govtechmy/myds-style/full.css` (`develop-install`, `develop-nextjs`). Use the CSS import **or** the Tailwind preset, not both, unless your project already uses Tailwind (`develop-style-configuration`).
- **Retrieve the `develop-<component>` page for every MYDS component you import.** This is the exception to SKILL.md's "3–6 guides" budget: an import or prop you haven't confirmed is a guess.
- The docs list only some props. Native attributes (`id`, `name`, `type`, `aria-*`, `autoComplete`) are not documented. If the package is installed, confirm them in `node_modules/@govtechmy/myds-react/dist/**/*.d.ts`; otherwise **say they are unconfirmed**. Then render the page and check the HTML: a broken `id` on an Input silently breaks the label link.

### 2. SPLaSK tags in JSX / TSX
- Hyphenated attribute names pass straight through to the DOM in React, and TypeScript doesn't type-check hyphenated JSX attributes on HTML elements:
  ```tsx
  <form role="search" action="/carian" splwpk-search-function="splwpk-search-function">…</form>
  ```
- `timestamp` has **no hyphen**, so TypeScript rejects it on an `<a>`. Declare it once:
  ```ts
  // types/splask.d.ts
  import 'react';
  declare module 'react' {
    interface HTMLAttributes<T> { timestamp?: string }
  }
  ```
  Then write `<a href="/berita" splwpk-news="splwpk-news" timestamp={formatSplask(news.updatedAt)}>`, where `formatSplask` returns `YYYY-MM-DD HH:MM:SS` in Malaysia time.
- **Put tags on native elements.** A MYDS component only forwards unknown props if it spreads them, and that isn't documented. Prefer a native element (`<a>`, `<form>`, `<div>`), or a component's `asChild` child (Radix Slot merges props onto the child).
- **Check the server HTML, not DevTools:** `curl -s http://localhost:3000/ms | grep -o 'splwpk-[a-z0-9-]*' | sort -u`. In the Next.js App Router, both server and client components are server-rendered, so the tags are in the first HTML response. Tags added in `useEffect` are not.

### 3. BM / EN routing and the language switch
- Put the locale in the path (`/ms/...`, `/en/...`) under `app/[lang]/`, and set `<html lang={lang}>` in that root layout. Use middleware to redirect bare paths to `/ms` (BM is the default for gov sites).
- Declare the alternates: `export const metadata = { alternates: { languages: { ms: '/ms/…', en: '/en/…' } } }`.
- **The switch** links to the *same page* in the other language, not to the home page. Mark each label with its own language, show the current language, and tag the control:
  ```tsx
  <nav aria-label={lang === 'ms' ? 'Bahasa' : 'Language'} splwpk-multilang="splwpk-multilang">
    <a href={`/ms${path}`} lang="ms" hrefLang="ms" aria-current={lang === 'ms' ? 'true' : undefined}>BM</a>
    <a href={`/en${path}`} lang="en" hrefLang="en" aria-current={lang === 'en' ? 'true' : undefined}>EN</a>
  </nav>
  ```
  The same pattern works in PHP: links to `?lang=` or `/en/…`, with the tag on the wrapper.

### 4. Masthead
Use `@govtechmy/myds-react/masthead` and pass the official wording as children: "Portal Rasmi Kerajaan Malaysia" / "Official Malaysia Government Website", "Kenal pasti begini" / "Here's how you know" (see `masthead-html` for the full text). Don't rely on any built-in default text, because the docs don't say whether the component localises itself.

### 5. Known gaps in the MYDS React docs (observed 25 Nov 2026)
Tell the user when one of these affects their page. Don't guess silently.
- Callout `variant`, Button `variant`, Label/Input `size` and Link `underline`: the enum values aren't listed (examples show `primary-fill`, `primary-ghost`, `default-outline` for Button).
- Navbar: the anatomy uses `NavbarActionGroup` but the import list exports `NavbarAction`.
- Table: the anatomy places `TableCaption` last. In HTML, `<caption>` must be the first child of `<table>`, so render it first.
- Callout: the anatomy uses `CalloutClose`, which isn't in the import list.
- Masthead: one docs demo shows "Official Malays**ian** Government Website". The MYDS locale files and www.malaysia.gov.my use "Official Malays**ia** Government Website", so use that.

## Bahasa Melayu

1. **Import** setiap komponen daripada laluannya sendiri (`@govtechmy/myds-react/<nama>`). Dapatkan halaman `develop-<komponen>` bagi setiap komponen yang digunakan. Prop yang tidak didokumenkan (`id`, `name`, `aria-*`) mesti disahkan dalam fail `.d.ts` pakej, atau dinyatakan sebagai belum disahkan.
2. **Tag SPLaSK dalam JSX:** atribut berjarak sempang (`splwpk-*`) dihantar terus ke DOM. Untuk `timestamp`, tambah pengisytiharan TypeScript (lihat di atas). Letak tag pada elemen HTML asli, dan semak HTML daripada pelayan dengan `curl`.
3. **Laluan bahasa:** `/ms/...` dan `/en/...`, `<html lang>` dalam *layout*, BM sebagai lalai. Penukar bahasa memaut ke *halaman yang sama* dalam bahasa lain, setiap label ditanda `lang`, dan pembungkusnya ditag `splwpk-multilang`.
4. **Masthead:** berikan teks rasmi sebagai *children*. Gunakan "Official Malaysia Government Website" (bukan "Malaysian").
5. **Jurang dokumentasi MYDS React:** nilai `variant`/`size` tidak disenaraikan, `NavbarAction` berbanding `NavbarActionGroup`, dan `TableCaption` mesti diletakkan pertama dalam HTML. Beritahu pengguna jika ia menjejaskan halaman.
