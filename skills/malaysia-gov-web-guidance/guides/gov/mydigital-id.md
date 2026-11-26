---
id: mydigital-id
title: "MyDigital ID: sign-in (MyID Access SSO) and identity verification (MyID Verify)"
title_ms: "MyDigital ID: log masuk (MyID Access SSO) dan pengesahan identiti (MyID Verify)"
category: gov
keywords: "mydigital id myid access sso single sign-on log masuk login oidc openid connect oauth keycloak realm client id redirect uri nric mykad nama ekyc e-verification myid verify static live face match jpn callback webhook api key x-api-key x-client-id aes-256-gcm partners portal"
description: "How a government (or other) system lets people sign in with MyDigital ID (MyID Access: standard OpenID Connect) and how MyID Verify checks a person's name, IC number and face against JPN records. Summarised from MyDigital ID Sdn. Bhd.'s developer portal guides, with the design and data-handling decisions an agency has to make."
description_ms: "Cara sistem membenarkan log masuk dengan MyDigital ID (OpenID Connect) dan cara MyID Verify menyemak nama, nombor kad pengenalan dan wajah dengan rekod JPN."
sources: "MyDigital ID Developer Portal, https://developer.digital-id.my (Documentation tab): 'MyID Access Integration Guide' PP26400 v1.0 (marked PUBLIC); 'MyID Verify V1 Integration Guide' PP26399 v1.0 (marked PUBLIC); 'MyID Verify Technical Guide Document' (30/9/2026; its cover forbids reproduction, so it is only summarised here). Retrieved 2026-11-26."
authority: "MyDigital ID Sdn. Bhd. (operator of MyDigital ID). This guide is an unofficial summary; the documents on the portal are the authority."
status: current
retrieved: 2026-11-26
---

# MyDigital ID / MyDigital ID

## English

MyDigital ID is Malaysia's national digital identity, run by **MyDigital ID Sdn. Bhd.** (not JDN). Its developer portal, https://developer.digital-id.my, publishes the integration guides; the "Sample Code" tab was empty on 26 Nov 2026. Read the official guides before building: this page only summarises them, in this skill's own words, and they may have changed. **Credentials, the host name, the realm and API keys come from MyDigital ID when your agency is onboarded: never invent them; leave TODOs.**

There are two separate products:

| | MyID Access (SSO) | MyID Verify |
|---|---|---|
| What it does | Lets a person **sign in** to your system with their MyDigital ID app | **Checks** a person's name, IC number and face against JPN records (eKYC) |
| Typical gov use | Citizen login to an online service portal | Identity check during registration for a high-assurance service |
| Protocol | Standard **OpenID Connect**, authorization-code flow | Server-to-server REST API |

### MyID Access: signing in with MyDigital ID

**How it works.** Your app redirects the browser to the MyID Access server (an OpenID Connect provider) with `scope=openid`. The user scans a QR code (desktop) or opens the MyDigital ID app through a deep link (mobile), confirms with PIN or biometrics, and the app's digital certificate is checked (OCSP). The server then redirects back to your app with an authorization code, which your server exchanges for ID and access tokens. The identity claims are the person's **name and IC number (NRIC)** as on MyKad.

**What to register with MyDigital ID:** a client ID; the client type (**confidential** for server-side apps such as PHP/Laravel, Spring, Express, Django, which keep a client secret; **public** for SPAs and mobile apps); and the exact **redirect URI(s)** that receive the code, over HTTPS.

**Endpoints** follow the usual Keycloak-style OpenID Connect pattern, under the host and realm you are given: `https://<host>/realms/<realm>/protocol/openid-connect/` + `auth`, `token`, `userinfo`, `logout`. Use the provider's discovery document (`.well-known/openid-configuration` under the realm) if it is available, rather than hard-coding them.

**Build it like any careful OIDC client:**
- Use a maintained OIDC library for your stack instead of hand-written token handling. Check `state` (and `nonce`), validate the ID token's signature, issuer, audience and expiry.
- Use PKCE for public clients (SPAs, mobile) if the provider supports it; confirm with MyDigital ID.
- HTTPS everywhere: callback routes, API calls and redirect URIs. Your server must be able to reach the MyDigital ID host on port 443 (check agency firewalls early).
- **Logout** should end both your session and the SSO session (the `logout` endpoint).

**Mobile apps.** The guide asks for the OIDC flow in an **embedded webview**, not an in-app system browser or custom tab (Chrome Custom Tabs, SFSafariViewController); this is the opposite of the usual OAuth advice, so follow the MyDigital ID guide and note the reason in your design. A webview can't tell whether the MyDigital ID app is installed, so either detect it through its custom URL scheme (`mydigitalid://`) before starting login and ask the user to install it, or show a notice before login that the app is required.

**Data you receive is personal data.** You get the person's full name and IC number.
- Store only what the service needs. Link accounts on the IC number, but consider storing a **hash** (for example SHA-256 with a secret salt/pepper kept outside the database) instead of the raw number; the guide leaves this to your agency's data-governance rules, so ask the agency's data owner (this is a decision for the user, not something to assume).
- Never log raw IC numbers or tokens; mask them on screen (for example `******-**-1234`).
- Treat MyDigital ID as the login method, not a replacement for authorisation: your system still decides what each person may do.

**UI wording.** BM first: *Log masuk dengan MyDigital ID* / *Log in with MyDigital ID*. The guides don't publish an official button design or logo-usage rules; ask MyDigital ID before using their logo.

### MyID Verify: checking identity against JPN

Two kinds:
- **Static**: your server sends a name, IC number and a face photo; the API compares them with JPN's records and returns whether the face matches and a face score (0–100). There is **no liveness or anti-spoofing check**, so it is meant for cases where a liveness check has already been done, or for re-confirming an existing customer. Photos are JPEG/PNG, under 7 MB.
- **Live**: real-time verification with liveness, done in the person's MyDigital ID app. Your server starts a request; the result arrives later at your registered **callback URL** (and can also be polled). Requests expire after a few minutes.

What an integration involves (details are in the official guides):
- **Credentials** issued at onboarding: a client ID, an API key, and a client secret. Depending on the version, calls are authenticated with headers carrying the client ID and API key, or with an OAuth2 *client credentials* token. The secret is also used to compute an integrity hash over the request (and, optionally, to encrypt the name, IC number and photo with AES-256-GCM). **Keep the secret and API key on the server only**, in environment variables or a secrets store, never in front-end code or the repository.
- **IP whitelisting**: requests come from your server's registered IP, so plan for a static outbound IP.
- **Callbacks (Live)**: a public HTTPS endpoint that accepts JSON POSTs. **Verify every callback** with the integrity hash described in the guide before trusting it, and treat it as idempotent (the same result may arrive twice).
- **Rate limits** (tens of requests per minute) and documented status codes: handle "face not detected", "name/IC mismatch", "request expired", "user cancelled" and "rate limited" with clear messages and a retry path, not a dead end.
- A **Partners Portal** lets the agency's staff see transaction logs and billing; verification is a charged service.

**Decisions to raise with the user (don't decide them silently):** whether Verify is needed at all (most services only need sign-in); Static vs Live; what happens when a face doesn't match (manual review, re-capture, counter visit); how long photos and results are kept, and who can see them.

## Bahasa Melayu

MyDigital ID ialah identiti digital nasional yang dikendalikan oleh **MyDigital ID Sdn. Bhd.** Panduan integrasi rasmi ada di https://developer.digital-id.my (tab *Documentation*). Halaman ini hanya ringkasan; rujuk dokumen rasmi. **Client ID, host, realm dan kunci API diberikan oleh MyDigital ID semasa agensi didaftarkan: jangan reka; tinggalkan TODO.**

**MyID Access (log masuk):** OpenID Connect biasa (*authorization code flow*, `scope=openid`). Pengguna mengimbas kod QR atau membuka aplikasi MyDigital ID, mengesahkan dengan PIN/biometrik, dan sistem anda menerima **nama dan nombor kad pengenalan**. Daftarkan *client* (jenis *confidential* untuk aplikasi pelayan seperti PHP/Laravel; *public* untuk SPA dan aplikasi mudah alih) dan *redirect URI* HTTPS yang tepat. Gunakan pustaka OIDC yang diselenggara; semak `state`/`nonce` dan tandatangan token. Untuk aplikasi mudah alih, panduan rasmi meminta *embedded webview* dan semakan sama ada aplikasi MyDigital ID dipasang (`mydigitalid://`), atau notis sebelum log masuk.

**Data peribadi:** simpan hanya yang perlu; pertimbangkan *hash* nombor kad pengenalan (keputusan pemilik data agensi); jangan log nombor kad pengenalan atau token; samarkan di skrin. Teks butang: *Log masuk dengan MyDigital ID*.

**MyID Verify:** menyemak nama, nombor kad pengenalan dan wajah dengan rekod JPN. *Static* (tanpa semakan *liveness*) atau *Live* (dengan *liveness*, keputusan dihantar ke *callback URL* anda). Kunci API dan *client secret* hanya di pelayan; IP pelayan perlu didaftarkan; sahkan setiap *callback* dengan *hash* integriti; urus had kadar dan kod status dengan mesej yang jelas. Bincang dengan pengguna: perlukah Verify, Static atau Live, tindakan jika wajah tidak sepadan, dan tempoh simpanan data.
