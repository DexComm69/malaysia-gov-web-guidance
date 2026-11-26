<?php
/**
 * Minimal, dependency-free OpenID Connect client for MyDigital ID (MyID Access) on plain PHP / XAMPP.
 * Needs the openssl and curl extensions. Authorization-code flow with state, nonce and PKCE (S256);
 * the ID token's RS256 signature is verified against the provider's JWKS, and iss / aud / exp / iat / nonce
 * are checked. If you can use Composer, a maintained library (e.g. jumbojett/openid-connect-php) is a
 * good alternative; keep the same checks.
 *
 * Guide: mydigital-id. Official docs: https://developer.digital-id.my
 */
declare(strict_types=1);

final class MyIdOidc
{
    private array $cfg;
    private ?array $discovery = null;

    public function __construct(array $cfg)
    {
        foreach (['issuer', 'client_id', 'redirect_uri'] as $k) {
            if (empty($cfg[$k])) throw new InvalidArgumentException("missing config: $k");
        }
        if (!str_starts_with($cfg['redirect_uri'], 'https://') && empty($cfg['allow_http_for_local_testing'])) {
            throw new InvalidArgumentException('redirect_uri must use HTTPS');
        }
        $this->cfg = $cfg + ['scope' => 'openid', 'leeway' => 60, 'timeout' => 15];
    }

    // ---------- step 1: send the user to MyDigital ID ----------
    public function loginUrl(): string
    {
        $state = self::random(32);
        $nonce = self::random(32);
        $verifier = self::random(48);
        $_SESSION['myid'] = ['state' => $state, 'nonce' => $nonce, 'verifier' => $verifier, 'started' => time()];
        $q = [
            'response_type' => 'code',
            'client_id' => $this->cfg['client_id'],
            'redirect_uri' => $this->cfg['redirect_uri'],
            'scope' => $this->cfg['scope'],
            'state' => $state,
            'nonce' => $nonce,
            'code_challenge' => self::b64url(hash('sha256', $verifier, true)),
            'code_challenge_method' => 'S256',
        ];
        return $this->endpoint('authorization_endpoint') . '?' . http_build_query($q, '', '&', PHP_QUERY_RFC3986);
    }

    // ---------- step 2: back from MyDigital ID ----------
    /** @return array verified ID-token claims */
    public function handleCallback(array $get): array
    {
        $saved = $_SESSION['myid'] ?? null;
        unset($_SESSION['myid']);                                   // one use only
        if (!$saved) throw new RuntimeException('no login in progress (session expired?)');
        if (isset($get['error'])) throw new RuntimeException('login was not completed: ' . substr((string) $get['error'], 0, 60));
        if (!isset($get['state']) || !hash_equals($saved['state'], (string) $get['state'])) throw new RuntimeException('state mismatch');
        if (time() - $saved['started'] > 600) throw new RuntimeException('login took too long; start again');
        if (empty($get['code'])) throw new RuntimeException('no authorization code');

        $form = [
            'grant_type' => 'authorization_code',
            'code' => (string) $get['code'],
            'redirect_uri' => $this->cfg['redirect_uri'],
            'client_id' => $this->cfg['client_id'],
            'code_verifier' => $saved['verifier'],
        ];
        if (!empty($this->cfg['client_secret'])) $form['client_secret'] = $this->cfg['client_secret'];   // confidential client
        $tok = $this->post($this->endpoint('token_endpoint'), $form);
        if (empty($tok['id_token'])) throw new RuntimeException('token response has no id_token');

        $claims = $this->verifyIdToken($tok['id_token'], $saved['nonce']);
        $_SESSION['myid_tokens'] = ['id_token' => $tok['id_token']];   // kept only for logout (id_token_hint)
        return $claims;
    }

    public function logoutUrl(string $postLogoutRedirect): string
    {
        $q = ['client_id' => $this->cfg['client_id'], 'post_logout_redirect_uri' => $postLogoutRedirect];
        if (!empty($_SESSION['myid_tokens']['id_token'])) $q['id_token_hint'] = $_SESSION['myid_tokens']['id_token'];
        return $this->endpoint('end_session_endpoint') . '?' . http_build_query($q, '', '&', PHP_QUERY_RFC3986);
    }

    // ---------- ID token verification ----------
    public function verifyIdToken(string $jwt, string $expectedNonce): array
    {
        $parts = explode('.', $jwt);
        if (count($parts) !== 3) throw new RuntimeException('malformed id_token');
        [$h64, $p64, $s64] = $parts;
        $header = json_decode(self::b64urlDecode($h64), true);
        $claims = json_decode(self::b64urlDecode($p64), true);
        if (!is_array($header) || !is_array($claims)) throw new RuntimeException('malformed id_token');
        if (($header['alg'] ?? '') !== 'RS256') throw new RuntimeException('unexpected id_token algorithm');   // never accept "none" or HS*

        $key = $this->publicKey($header['kid'] ?? null);
        $ok = openssl_verify("$h64.$p64", self::b64urlDecode($s64), $key, OPENSSL_ALGO_SHA256);
        if ($ok !== 1) throw new RuntimeException('id_token signature is not valid');

        $now = time(); $leeway = (int) $this->cfg['leeway'];
        if (($claims['iss'] ?? '') !== $this->cfg['issuer']) throw new RuntimeException('id_token issuer mismatch');
        $aud = (array) ($claims['aud'] ?? []);
        if (!in_array($this->cfg['client_id'], $aud, true)) throw new RuntimeException('id_token audience mismatch');
        if (count($aud) > 1 && ($claims['azp'] ?? '') !== $this->cfg['client_id']) throw new RuntimeException('id_token azp mismatch');
        if (!isset($claims['exp']) || $now > (int) $claims['exp'] + $leeway) throw new RuntimeException('id_token expired');
        if (isset($claims['iat']) && (int) $claims['iat'] > $now + $leeway) throw new RuntimeException('id_token issued in the future');
        if (!isset($claims['nonce']) || !hash_equals($expectedNonce, (string) $claims['nonce'])) throw new RuntimeException('id_token nonce mismatch');
        return $claims;
    }

    // ---------- helpers ----------
    private function endpoint(string $name): string
    {
        if ($this->discovery === null) {
            $this->discovery = $this->get(rtrim($this->cfg['issuer'], '/') . '/.well-known/openid-configuration');
            if (($this->discovery['issuer'] ?? '') !== $this->cfg['issuer']) throw new RuntimeException('discovery issuer mismatch');
        }
        $url = $this->discovery[$name] ?? '';
        if ($url === '') throw new RuntimeException("provider has no $name");
        return $url;
    }

    private function publicKey(?string $kid)
    {
        $jwks = $this->get($this->endpoint('jwks_uri'));
        foreach ($jwks['keys'] ?? [] as $k) {
            if (($k['kty'] ?? '') !== 'RSA' || ($kid !== null && ($k['kid'] ?? null) !== $kid)) continue;
            if (isset($k['use']) && $k['use'] !== 'sig') continue;
            $pem = self::rsaJwkToPem($k['n'], $k['e']);
            $key = openssl_pkey_get_public($pem);
            if ($key) return $key;
        }
        throw new RuntimeException('signing key not found in JWKS');
    }

    private function get(string $url): array
    {
        return $this->http($url, null);
    }

    private function post(string $url, array $form): array
    {
        return $this->http($url, http_build_query($form, '', '&'));
    }

    private function http(string $url, ?string $body): array
    {
        $local = !empty($this->cfg['allow_http_for_local_testing']);
        if (!$local && !str_starts_with($url, 'https://')) throw new RuntimeException('provider endpoint is not HTTPS');
        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => (int) $this->cfg['timeout'],
            CURLOPT_SSL_VERIFYPEER => true, CURLOPT_SSL_VERIFYHOST => 2, CURLOPT_FOLLOWLOCATION => false,
            CURLOPT_HTTPHEADER => ['Accept: application/json'],
        ]);
        if ($body !== null) {
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
            curl_setopt($ch, CURLOPT_HTTPHEADER, ['Accept: application/json', 'Content-Type: application/x-www-form-urlencoded']);
        }
        $raw = curl_exec($ch);
        $status = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
        $err = curl_error($ch);
        curl_close($ch);
        if ($raw === false) throw new RuntimeException('could not reach the identity provider: ' . $err);
        $data = json_decode((string) $raw, true);
        if ($status !== 200 || !is_array($data)) throw new RuntimeException("identity provider returned HTTP $status");
        return $data;
    }

    public static function random(int $bytes): string
    {
        return self::b64url(random_bytes($bytes));
    }

    public static function b64url(string $bin): string
    {
        return rtrim(strtr(base64_encode($bin), '+/', '-_'), '=');
    }

    public static function b64urlDecode(string $s): string
    {
        $d = base64_decode(strtr($s, '-_', '+/') . str_repeat('=', (4 - strlen($s) % 4) % 4), true);
        if ($d === false) throw new RuntimeException('bad base64url');
        return $d;
    }

    /** RSA JWK (n, e) -> PEM public key (SubjectPublicKeyInfo), without external libraries. */
    public static function rsaJwkToPem(string $n, string $e): string
    {
        $int = function (string $bin): string {
            $bin = ltrim($bin, "\x00");
            if ($bin === '' || ord($bin[0]) > 0x7f) $bin = "\x00" . $bin;
            return "\x02" . self::derLen(strlen($bin)) . $bin;
        };
        $rsaKey = $int(self::b64urlDecode($n)) . $int(self::b64urlDecode($e));
        $rsaKey = "\x30" . self::derLen(strlen($rsaKey)) . $rsaKey;
        $algo = "\x30\x0d\x06\x09\x2a\x86\x48\x86\xf7\x0d\x01\x01\x01\x05\x00";   // rsaEncryption, NULL
        $bits = "\x03" . self::derLen(strlen($rsaKey) + 1) . "\x00" . $rsaKey;
        $spki = "\x30" . self::derLen(strlen($algo . $bits)) . $algo . $bits;
        return "-----BEGIN PUBLIC KEY-----\n" . chunk_split(base64_encode($spki), 64, "\n") . "-----END PUBLIC KEY-----\n";
    }

    private static function derLen(int $len): string
    {
        if ($len < 0x80) return chr($len);
        $out = '';
        while ($len > 0) { $out = chr($len & 0xff) . $out; $len >>= 8; }
        return chr(0x80 | strlen($out)) . $out;
    }
}
