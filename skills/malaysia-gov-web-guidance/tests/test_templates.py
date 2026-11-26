"""Checks the starter templates in assets/templates against the skill's own rules. Run: python -m unittest discover -s tests"""
import datetime as dt, glob, os, re, shutil, subprocess, sys, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(HERE, '..', 'assets', 'templates')
sys.path.insert(0, os.path.join(HERE, '..', 'scripts'))
import splask_scan as s  # noqa: E402

FILES = [f for f in glob.glob(os.path.join(T, '**', '*'), recursive=True) if f.endswith(('.php', '.ts', '.tsx', '.html'))]
SRC = {f: open(f, encoding='utf8').read() for f in FILES}
CODE = {f: t for f, t in SRC.items() if not f.endswith('example.html')}


class Templates(unittest.TestCase):
    def test_all_five_stacks(self):
        for d in ('plain-php', 'wordpress', 'joomla', 'laravel', 'nextjs'):
            self.assertTrue(os.path.isdir(os.path.join(T, d)), d)

    def test_only_official_tags(self):
        used = set()
        for t in SRC.values():
            used |= set(re.findall(r'(splwpk-[a-z0-9-]+)(?:="|\'|\b)', t))
        self.assertEqual(sorted(u for u in used if u not in s.TAGS), [])

    def test_no_current_time_timestamps(self):
        bad = r"timestamp=\"\{\{\s*now\(\)|timestamp=\"<\?=\s*date\(|timestamp=\{new Date|Factory::getDate\('now'\)->format\('Y-m-d H:i:s'\)|current_time\("
        for f, t in CODE.items():
            self.assertIsNone(re.search(bad, t), f)

    def test_no_framework_bound_tags(self):
        for f, t in CODE.items():
            self.assertIsNone(re.search(r'(x-bind|v-bind)?:splwpk-', t), f)

    def test_search_tag_on_form(self):
        for f, t in CODE.items():
            for m in re.finditer(r'<(\w+)\b[^>]*splwpk-search-function=', t):
                self.assertEqual(m.group(1), 'form', f)

    def test_masthead_wording(self):
        for d in ('plain-php/masthead.php', 'wordpress/parts/masthead.php', 'joomla/masthead.php',
                  'laravel/resources/views/partials/masthead.blade.php', 'nextjs/components/Masthead.tsx'):
            t = SRC[os.path.join(T, *d.split('/'))]
            for w in ('Portal Rasmi Kerajaan Malaysia', 'Official Malaysia Government Website', 'Kenal pasti begini'):
                self.assertIn(w, t, d)

    def test_multilang_only_with_two_languages(self):
        for f, t in CODE.items():
            if 'splwpk-multilang="splwpk-multilang"' in t:   # files that print the attribute
                self.assertRegex(t, r'count\(|length > 1|< 2', f)

    def test_example_scans_clean(self):
        r = s.scan_site(os.path.join(T, 'example.html'), None, dt.datetime(2026, 11, 25), myds=True, a11y=True)
        noisy = [x for x in r['results'] if x['level'] in ('FAIL', 'WARN') and not x['message'].startswith('no `splwpk-')]
        self.assertEqual(noisy, [])

    @unittest.skipUnless(shutil.which('php') or os.path.exists(r'C:\xampp\php\php.exe'), 'php not installed')
    def test_php_lint(self):
        php = shutil.which('php') or r'C:\xampp\php\php.exe'
        for f in CODE:
            if f.endswith('.php') and not f.endswith('.blade.php'):
                p = subprocess.run([php, '-l', f], capture_output=True, text=True)
                self.assertEqual(p.returncode, 0, f + p.stdout + p.stderr)


if __name__ == '__main__':
    unittest.main()
