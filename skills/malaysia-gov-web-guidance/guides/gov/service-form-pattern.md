---
id: service-form-pattern
title: "Government online service forms: fields, validation, submission, acknowledgement"
title_ms: "Borang perkhidmatan dalam talian kerajaan: medan, pengesahan, penghantaran, pengakuan terima"
category: gov
keywords: "form borang permohonan application request service perkhidmatan gos online service submit hantar validation pengesahan error ralat summary ringkasan acknowledgement pengakuan reference number nombor rujukan thank you terima kasih pdpa consent persetujuan e-rating feedback csrf post redirect get"
description: "The end-to-end pattern for a public government form (application, request, complaint, registration): accessible fields, server-side validation with an error summary, PDPA notice, safe submission, an acknowledgement page with a reference number, automatic notification and GOS e-Rating. Use when building any form that the public submits."
description_ms: "Corak lengkap borang awam kerajaan: medan, pengesahan, notis PDPA, penghantaran selamat, halaman pengakuan dengan nombor rujukan, notifikasi automatik dan GOS e-Rating."
sources: "MYDS design/text-input, design/radio, design/checkbox, design/date-field, develop/accessibility (WCAG 2.2); SPLaSK GOS criteria (Rajah 1, malaysia.gov.my): feedback auto-notification, availability of GOS e-Rating, online service security; Personal Data Protection Act 2010 (Malaysia), general notice principle"
authority: "Unofficial synthesis of MYDS (GovTech Malaysia / JDN), SPLaSK (JDN), WCAG 2.2 and PDPA 2010"
status: current
retrieved: 2026-11-25
---

# Government online service forms / Borang perkhidmatan dalam talian kerajaan

## English

A form the public submits is a **government online service (GOS)**. Besides MYDS and accessibility, SPLaSK's GOS criteria apply: feedback auto-notification, availability of GOS e-Rating, aid and help resources, and online service security. Retrieve `splask-criteria-checklist` for the full list.

### 1. Fields (MYDS `design-text-input`, `design-radio`, `design-checkbox`, `design-date-field`)
- Each field has a visible `<label for>`, an optional hint *above* or *below* the field (be consistent), and an error message. Link the hint and the error with `aria-describedby`.
- Use the right input type and `autocomplete`: `name`, `tel` + `inputmode="tel"`, `email`, `street-address`, `postal-code`. For quantities, use `type="text"` with `inputmode="numeric"`, because `type="number"` changes value on scroll and shows spinners.
- Group radio buttons and checkboxes in a `<fieldset>` with a `<legend>`.
- Dates: use `<input type="date">` with `min`/`max` taken from the business rules, and check them again on the server.
- Mark optional fields as optional, rather than marking every required one. The form should then say "all fields are required unless marked optional" (BM: *semua medan wajib diisi kecuali yang ditanda pilihan*).
- Ask only for data the service needs (PDPA data minimisation). Don't ask for a MyKad number unless the service truly requires it.

### 2. Validation and errors
- **Always validate on the server.** Browser validation is only a convenience.
- On failure, re-render the form with HTTP **422**, keep what the user entered, and set `aria-invalid="true"` on each bad field. At the top, show an error summary (`role="alert"`, `tabindex="-1"`, focused on load) whose items link to each field (`href="#field-id"`).
- Write messages that say how to fix the problem: "Masukkan nombor telefon seperti 012-3456789", not "Format tidak sah".

### 3. PDPA notice
- Before the submit button, show a short notice: what personal data is collected, why, who it's shared with, how long it's kept, and a link to the privacy policy and PDPA statement (`splwpk-privacy-policy`, `splwpk-pdpa` in the footer).
- PDPA's application to federal and state government is limited and is debated for local authorities. Whether an explicit **consent checkbox** is needed is a policy decision for the agency, so **ask the user**. Don't decide it silently either way.

### 4. Safe submission
- Use a CSRF token on every POST, check the token on the server, and limit the request size.
- Use **Post/Redirect/Get**: on success, store the record and answer `303 See Other` to the acknowledgement page, so a refresh can't submit twice.
- Escape all output (`htmlspecialchars` in PHP) and use HTTPS only.

### 5. Acknowledgement (GOS: feedback auto-notification)
- The acknowledgement page shows:
  - a **reference number** (for example `<AGENCY>-<SERVICE>-<YYYYMMDD>-<random>`);
  - a summary of what was submitted;
  - what happens next, and when;
  - how to ask about it (contact details).
- Send an **automatic acknowledgement** by e-mail or SMS with the same reference number. SPLaSK checks "feedback auto-notification".
- Opening the acknowledgement page directly, without a submission, should redirect back to the form.

### 6. GOS e-Rating and help
- Offer the **GOS e-Rating** on or after the acknowledgement. SPLaSK checks "availability of GOS e-Rating". The agency's SPLaSK supervisor can say how e-Rating is embedded.
- Link to help and FAQ for the service ("aid, tools and help resources").

## Bahasa Melayu

Borang yang dihantar oleh orang awam ialah **perkhidmatan dalam talian kerajaan (GOS)**. Kriteria GOS SPLaSK terpakai: notifikasi automatik maklum balas, ketersediaan GOS e-Rating, bantuan, dan keselamatan perkhidmatan.

1. **Medan:** label yang kelihatan, teks petunjuk, mesej ralat dipaut dengan `aria-describedby`, jenis input dan `autocomplete` yang betul, `<fieldset>`/`<legend>` untuk butang radio, tarikh dengan `min`/`max`. Minta data yang perlu sahaja (prinsip PDPA).
2. **Pengesahan:** sentiasa di pelayan. Jika gagal: status 422, simpan input pengguna, `aria-invalid`, ringkasan ralat (`role="alert"`, difokuskan) dengan pautan ke setiap medan. Mesej menerangkan cara membetulkan.
3. **Notis PDPA** sebelum butang hantar. Sama ada kotak persetujuan diperlukan ialah keputusan agensi: **tanya pengguna**.
4. **Penghantaran selamat:** token CSRF, Post/Redirect/Get (303), *escape* output, HTTPS.
5. **Pengakuan terima:** halaman dengan **nombor rujukan**, ringkasan, langkah seterusnya, dan e-mel/SMS automatik dengan nombor yang sama.
6. **GOS e-Rating** dan pautan bantuan atau soalan lazim.
