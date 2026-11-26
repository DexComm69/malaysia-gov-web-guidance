# MyDigital ID login starter (plain PHP / XAMPP)

"Log masuk dengan MyDigital ID" for a plain PHP site, with no Composer and no libraries: it needs PHP 8.1+ with the `curl` and `openssl` extensions (both are in XAMPP). It implements MyID Access as a standard OpenID Connect **authorization-code flow** (see the skill's `mydigital-id` guide and https://developer.digital-id.my).

| File | Does |
|---|---|
| `config.php` | Issuer, client ID/secret, redirect URI, claim names. All values come from MyDigital ID at onboarding: **TODO**, read from environment variables, never committed |
| `oidc.php` | The OIDC client: discovery, `state` + `nonce` + PKCE (S256), code exchange, RS256 ID-token signature check against the provider's JWKS, `iss` / `aud` / `exp` / `iat` / `nonce` checks |
| `bootstrap.php` | Secure session cookie (HttpOnly, Secure, SameSite=Lax), IC-number masking and hashing helpers |
| `login.php` | Starts login (redirects to MyDigital ID) |
| `callback.php` | Finishes login, starts a fresh session (`session_regenerate_id`), keeps the name and a masked / hashed IC number |
| `logout.php` | POST + CSRF token; ends the local session and the MyDigital ID session |
| `index.php` | Example page: "Log masuk dengan MyDigital ID" button, or the signed-in name |

**Tested** by the skill's `tests/test_mydigital_login.py` against a mock OpenID Connect provider (`tests/mock_oidc.mjs`): a full login, logout, a replayed code, a forged `state`, and ID tokens with a wrong signature, wrong audience, wrong issuer, wrong nonce, an expired token and an unsigned (`alg: none`) token, all of which must be rejected. It has **not** been run against MyDigital ID's real servers: do that in MyDigital ID's test environment before going live.

**Before going live (decisions for the agency, not for the code):**
- Confirm the exact claim names for name and IC number with MyDigital ID (`claim_name`, `claim_nric`).
- Decide with the agency's data owner whether to store the IC number or only a keyed hash of it (`nric_pepper`), and how long to keep it.
- Link the MyDigital ID identity to your own user table, and keep your own authorisation (roles): signing in proves who someone is, not what they may do.
- Serve over HTTPS only; register the exact `redirect_uri`; allow outbound HTTPS (port 443) from the server to the MyDigital ID host.
- Mobile apps: follow the guide's webview and "is the MyDigital ID app installed?" advice (`mydigital-id`).

`allow_http_for_local_testing` exists only for the automated tests; it must stay off in production.
