"""Offline tests for scripts/splask_scan.py. Run: python -m unittest discover -s tests"""
import contextlib, datetime as dt, io, json, os, sys, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'scripts'))
import splask_scan as s  # noqa: E402

SITE = os.path.join(HERE, 'fixtures', 'site', 'index.html')
BROKEN = os.path.join(HERE, 'fixtures', 'broken', 'index.html')
TODAY = dt.datetime(2026, 11, 25)


def find(r, level=None, crit=None, page=None, text=''):
    return [x for x in r['results'] if (level is None or x['level'] == level) and (crit is None or x['criterion'] == crit)
            and (page is None or x['page'] == page) and text in x['message']]


def run_cli(*args):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = s.main(list(args))
    return code, out.getvalue()


class BrokenPage(unittest.TestCase):
    """15 seeded faults on one council home page."""
    @classmethod
    def setUpClass(cls): cls.r = s.scan_site(BROKEN, None, TODAY)

    def test_fail_count(self): self.assertEqual(s.counts(self.r)['FAIL'], 26)
    def test_misspelled_tag(self): self.assertTrue(find(self.r, 'FAIL', 'Tag spelling', text='did you mean `splwpk-search-function`'))
    def test_tag_on_i(self): self.assertTrue(find(self.r, 'FAIL', 'Feedback Form', text='<i>'))
    def test_commented_tags(self): self.assertTrue(find(self.r, 'FAIL', 'Commented-out tags'))
    def test_stale_news(self): self.assertTrue(find(self.r, 'FAIL', 'Updated Content: News', text='days old'))
    def test_long_title(self): self.assertTrue(find(self.r, 'FAIL', 'SEO', text='<title>'))
    def test_every_fail_has_fix(self):
        self.assertEqual([x for x in self.r['results'] if x['level'] == 'FAIL' and not x['fix']], [])


class Site(unittest.TestCase):
    """A clean 4-page site: only the privacy page heading is untagged."""
    def test_discovery(self):
        self.assertEqual(list(s.discover(open(SITE, encoding='utf8').read(), SITE)), ['privacy', 'sitemap', 'feedback'])

    def test_home_only(self):
        r = s.scan_site(SITE, None, TODAY)
        self.assertEqual([p['name'] for p in r['pages']], ['home'])
        self.assertTrue(find(r, 'FAIL', 'Sitemap', 'home', 'no `splwpk-sitemap`'))

    def test_all_pages(self):
        r = s.scan_site(SITE, 'all', TODAY)
        self.assertEqual([p['name'] for p in r['pages']], ['home', 'privacy', 'sitemap', 'feedback'])
        self.assertEqual(s.counts(r)['FAIL'], 1)
        self.assertTrue(find(r, 'FAIL', 'Privacy Policy', 'privacy', 'heading is not tagged'))

    def test_criteria_url_downgrade(self):
        r = s.scan_site(SITE, 'sitemap', TODAY)
        w = find(r, 'WARN', 'Sitemap', 'home')
        self.assertTrue(w and 'Criteria URL' in w[0]['fix'])

    def test_select_by_number_name_and_path(self):
        for sel in ('2', 'sitemap', os.path.join(HERE, 'fixtures', 'site', 'peta-laman.html')):
            r = s.scan_site(SITE, sel, TODAY)
            self.assertEqual([p['name'] for p in r['pages']], ['home', 'sitemap'], sel)

    def test_unknown_page(self):
        self.assertTrue(find(s.scan_site(SITE, 'bogus', TODAY), 'WARN', 'Page choice', text='"bogus"'))

    def test_max_pages(self):
        self.assertEqual(len(s.scan_site(SITE, 'all', TODAY, max_pages=1)['pages']), 2)

    def test_follow_compat(self):
        self.assertEqual([p['name'] for p in s.scan(SITE, True, TODAY)['pages']], ['home', 'privacy'])


class Cli(unittest.TestCase):
    def test_fail_on(self):
        self.assertEqual(run_cli(SITE, '--today', '2026-11-25')[0], 0)
        self.assertEqual(run_cli(SITE, '--today', '2026-11-25', '--fail-on', 'fail')[0], 1)
        self.assertEqual(run_cli(SITE, '--today', '2026-11-25', '--pages', 'all', '--fail-on', 'warn')[0], 1)

    def test_json(self):
        r = json.loads(run_cli(SITE, '--today', '2026-11-25', '--format', 'json')[1])
        self.assertIn('results', r)

    def test_markdown(self):
        out = run_cli(SITE, '--today', '2026-11-25', '--format', 'md')[1]
        self.assertIn('| | Criterion | Page | Finding | Suggested fix |', out)

    def test_md_out(self):
        import tempfile
        f = os.path.join(tempfile.mkdtemp(), 'summary.md')
        run_cli(SITE, '--today', '2026-11-25', '--md-out', f)
        self.assertIn('SPLaSK 2.0 pre-check', open(f, encoding='utf8').read())

    def test_list_pages(self):
        out = run_cli(SITE, '--list-pages')[1]
        self.assertIn('1. privacy', out)


if __name__ == '__main__':
    unittest.main()
