"""End-to-end test of assets/templates/mydigital-id-login against a mock OpenID Connect provider.
Needs php (with curl + openssl) and node; skipped otherwise. Run: python -m unittest discover -s tests"""
import http.cookiejar, os, re, shutil, socket, subprocess, sys, time, unittest, urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, '..', 'assets', 'templates', 'mydigital-id-login')
PHP = shutil.which('php') or (r'C:\xampp\php\php.exe' if os.path.exists(r'C:\xampp\php\php.exe') else None)
NODE = shutil.which('node')


def free_port():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close(); return p


def wait(port):
    for _ in range(100):
        try:
            socket.create_connection(('127.0.0.1', port), 0.2).close(); return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError(f'port {port} did not open')


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None


@unittest.skipUnless(PHP and NODE, 'php and node are needed')
class MyDigitalIdLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.idp_port, cls.app_port = free_port(), free_port()
        cls.issuer = f'http://127.0.0.1:{cls.idp_port}/realms/test'
        cls.idp = subprocess.Popen([NODE, os.path.join(HERE, 'mock_oidc.mjs'), str(cls.idp_port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        env = dict(os.environ, MYID_ISSUER=cls.issuer, MYID_CLIENT_ID='test-client', MYID_CLIENT_SECRET='test-secret',
                   MYID_REDIRECT_URI=f'http://127.0.0.1:{cls.app_port}/callback.php', MYID_AFTER_LOGOUT=f'http://127.0.0.1:{cls.app_port}/',
                   MYID_ALLOW_HTTP_FOR_TESTS='1', MYID_NRIC_PEPPER='test-pepper')
        args = [PHP]
        if os.name == 'nt': args += ['-d', 'extension_dir=' + os.path.join(os.path.dirname(PHP), 'ext'), '-d', 'extension=curl', '-d', 'extension=openssl']
        cls.app_proc = subprocess.Popen(args + ['-S', f'127.0.0.1:{cls.app_port}', '-t', TPL], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        wait(cls.idp_port); wait(cls.app_port)

    @classmethod
    def tearDownClass(cls):
        for p in (cls.app_proc, cls.idp):
            p.terminate(); p.wait(5)

    def setUp(self):
        self.jar = http.cookiejar.CookieJar()
        self.op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar), NoRedirect())
        self.mode('ok')

    def mode(self, m):
        urllib.request.urlopen(f'http://127.0.0.1:{self.idp_port}/_mode?m={m}').read()

    def get(self, url, data=None):
        try:
            with self.op.open(url, data=data) as r:
                return r.status, r.headers.get('Location'), r.read().decode('utf8', 'replace')
        except urllib.error.HTTPError as e:
            with e:
                return e.code, e.headers.get('Location'), e.read().decode('utf8', 'replace')

    def app(self, path):
        return f'http://127.0.0.1:{self.app_port}/{path}'

    def login(self, tamper_state=False):
        st, loc, _ = self.get(self.app('login.php'))
        self.assertEqual(st, 302)
        q = urllib.parse.parse_qs(urllib.parse.urlparse(loc).query)
        self.assertTrue(loc.startswith(self.issuer + '/protocol/openid-connect/auth'))
        self.assertEqual((q['code_challenge_method'][0], q['scope'][0]), ('S256', 'openid'))
        self.assertTrue(q['state'][0] and q['nonce'][0])
        st, cb, _ = self.get(loc)                                   # the provider approves and redirects back
        self.assertEqual(st, 302)
        if tamper_state:
            cb = re.sub(r'state=[^&]+', 'state=forged', cb)
        return self.get(cb), cb

    def test_happy_path(self):
        (st, loc, _), _ = self.login()
        self.assertEqual((st, loc), (303, 'index.php'))
        st, _, html = self.get(self.app('index.php'))
        self.assertIn('Selamat datang, ALI BIN ABU', html)
        self.assertIn('******-**-1234', html)                        # masked on screen
        self.assertNotIn('910203', html)                             # the full IC number is never shown

    def test_code_cannot_be_replayed(self):
        (st, _, _), cb = self.login()
        self.assertEqual(st, 303)
        self.assertEqual(self.get(cb)[0], 401)

    def test_forged_state_rejected(self):
        (st, _, _), _ = self.login(tamper_state=True)
        self.assertEqual(st, 401)

    def test_bad_tokens_rejected(self):
        for m in ('badsig', 'wrongaud', 'wrongiss', 'expired', 'wrongnonce', 'algnone'):
            self.setUp(); self.mode(m)
            (st, _, html), _ = self.login()
            self.assertEqual(st, 401, m)
            self.assertIn('Log masuk gagal', html, m)

    def test_logout(self):
        self.login()
        st, _, html = self.get(self.app('index.php'))
        csrf = re.search(r'name="csrf" value="([^"]+)"', html).group(1)
        self.assertEqual(self.get(self.app('logout.php'), urllib.parse.urlencode({'csrf': 'wrong'}).encode())[0], 405)
        st, loc, _ = self.get(self.app('logout.php'), urllib.parse.urlencode({'csrf': csrf}).encode())
        self.assertEqual(st, 303)
        self.assertTrue(loc.startswith(self.issuer + '/protocol/openid-connect/logout') and 'id_token_hint=' in loc)
        self.assertIn('Log masuk dengan MyDigital ID', self.get(self.app('index.php'))[2])


if __name__ == '__main__':
    unittest.main()
