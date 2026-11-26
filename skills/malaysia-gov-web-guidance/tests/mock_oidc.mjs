// Mock OpenID Connect provider for testing assets/templates/mydigital-id-login (no dependencies).
// Usage: node mock_oidc.mjs <port>. Issuer: http://127.0.0.1:<port>/realms/test
// GET /_mode?m=<mode> switches the next tokens to an attack: badsig | wrongaud | wrongiss | expired | wrongnonce | algnone | ok
import http from 'node:http';
import crypto from 'node:crypto';

const port = Number(process.argv[2] || 8899);
const ISS = `http://127.0.0.1:${port}/realms/test`;
const CLIENT = { id: 'test-client', secret: 'test-secret' };
const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const other = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const KID = 'k1';
const codes = new Map();
let mode = 'ok';
let lastIdToken = '';

const b64u = (b) => Buffer.from(b).toString('base64url');
function sign(claims, alg = 'RS256', key = privateKey) {
  const h = b64u(JSON.stringify({ alg, typ: 'JWT', kid: KID }));
  const p = b64u(JSON.stringify(claims));
  if (alg === 'none') return `${h}.${p}.`;
  return `${h}.${p}.${b64u(crypto.sign('sha256', Buffer.from(`${h}.${p}`), key))}`;
}
function json(res, code, body) { res.writeHead(code, { 'Content-Type': 'application/json' }); res.end(JSON.stringify(body)); }
function body(req) { return new Promise((r) => { let d = ''; req.on('data', (c) => (d += c)); req.on('end', () => r(new URLSearchParams(d))); }); }

http.createServer(async (req, res) => {
  const u = new URL(req.url, `http://127.0.0.1:${port}`);
  const p = u.pathname.replace('/realms/test', '');
  if (u.pathname === '/_mode') { mode = u.searchParams.get('m') || 'ok'; return json(res, 200, { mode }); }
  if (u.pathname === '/_last') return json(res, 200, { id_token: lastIdToken });
  if (p === '/.well-known/openid-configuration') return json(res, 200, {
    issuer: ISS, authorization_endpoint: `${ISS}/protocol/openid-connect/auth`, token_endpoint: `${ISS}/protocol/openid-connect/token`,
    userinfo_endpoint: `${ISS}/protocol/openid-connect/userinfo`, jwks_uri: `${ISS}/protocol/openid-connect/certs`,
    end_session_endpoint: `${ISS}/protocol/openid-connect/logout`, id_token_signing_alg_values_supported: ['RS256'],
    code_challenge_methods_supported: ['S256'],
  });
  if (p === '/protocol/openid-connect/certs') return json(res, 200, { keys: [{ ...publicKey.export({ format: 'jwk' }), kid: KID, use: 'sig', alg: 'RS256' }] });
  if (p === '/protocol/openid-connect/auth') {
    const q = u.searchParams;
    if (q.get('client_id') !== CLIENT.id || q.get('response_type') !== 'code' || q.get('code_challenge_method') !== 'S256' || !q.get('nonce')) return json(res, 400, { error: 'invalid_request' });
    const code = crypto.randomBytes(16).toString('hex');
    codes.set(code, { nonce: q.get('nonce'), challenge: q.get('code_challenge'), redirect: q.get('redirect_uri') });
    // the user approves in the MyDigital ID app; here we approve at once
    res.writeHead(302, { Location: `${q.get('redirect_uri')}?code=${code}&state=${encodeURIComponent(q.get('state'))}` });
    return res.end();
  }
  if (p === '/protocol/openid-connect/token' && req.method === 'POST') {
    const f = await body(req);
    const c = codes.get(f.get('code')); codes.delete(f.get('code'));            // one-time codes
    if (!c || f.get('client_id') !== CLIENT.id || f.get('client_secret') !== CLIENT.secret || f.get('redirect_uri') !== c.redirect) return json(res, 400, { error: 'invalid_grant' });
    const verifierHash = b64u(crypto.createHash('sha256').update(f.get('code_verifier') || '').digest());
    if (verifierHash !== c.challenge) return json(res, 400, { error: 'invalid_grant', error_description: 'PKCE' });
    const now = Math.floor(Date.now() / 1000);
    const claims = { iss: ISS, sub: 'user-910203011234', aud: CLIENT.id, iat: now, exp: now + 300, nonce: c.nonce, nama: 'ALI BIN ABU', nric: '910203-01-1234' };
    if (mode === 'wrongaud') claims.aud = 'someone-else';
    if (mode === 'wrongiss') claims.iss = 'https://evil.example/realms/test';
    if (mode === 'expired') { claims.iat = now - 3600; claims.exp = now - 1800; }
    if (mode === 'wrongnonce') claims.nonce = 'not-the-nonce';
    const idToken = mode === 'algnone' ? sign(claims, 'none') : mode === 'badsig' ? sign(claims, 'RS256', other.privateKey) : sign(claims);
    lastIdToken = idToken;
    return json(res, 200, { access_token: crypto.randomBytes(16).toString('hex'), token_type: 'Bearer', expires_in: 300, id_token: idToken });
  }
  if (p === '/protocol/openid-connect/logout') return json(res, 200, { logged_out: true, id_token_hint: u.searchParams.get('id_token_hint') ? 'present' : 'missing' });
  json(res, 404, { error: 'not_found' });
}).listen(port, '127.0.0.1', () => console.log(`mock oidc on ${ISS}`));
