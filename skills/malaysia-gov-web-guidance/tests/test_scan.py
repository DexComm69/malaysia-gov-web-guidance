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


class Timestamps(unittest.TestCase):
    def test_generated_at_request_time(self):
        import tempfile
        f = os.path.join(tempfile.mkdtemp(), 'index.html')
        with open(f, 'w', encoding='utf8') as h:
            h.write('<html lang="ms"><body><a href="/t" splwpk-about-us="splwpk-about-us" timestamp="2026-11-25 08:14:02">Tentang Kami</a></body></html>')
        self.assertTrue(find(s.scan_site(f, None, TODAY), 'WARN', 'Updated Content: About Us', text='scan date/time'))
        self.assertFalse(find(s.scan_site(SITE, None, TODAY), 'WARN', text='scan date/time'))


class Placement(unittest.TestCase):
    def page(self, body):
        import tempfile
        f = os.path.join(tempfile.mkdtemp(), 'index.html')
        with open(f, 'w', encoding='utf8') as h:
            h.write('<html lang="ms"><body>' + body + '</body></html>')
        return s.scan_site(f, None, TODAY)

    def test_freshness_limit_shown(self):
        r = self.page('<a href="/t" splwpk-about-us="splwpk-about-us" timestamp="2026-11-03 09:00:00">Tentang</a>')
        self.assertTrue(find(r, 'PASS', 'Updated Content: About Us', text='(limit 30)'))
        self.assertFalse(find(r, 'PASS', 'Updated Content: About Us', text='no freshness limit'))

    def test_age_never_negative(self):
        r = self.page('<a href="/b" splwpk-news="splwpk-news" timestamp="2026-11-25 10:42:17">Berita</a>')
        self.assertTrue(find(r, 'PASS', 'Updated Content: News', text='0 days old'))

    def test_wrapper_div_warns(self):
        r = self.page('<div splwpk-search-function="splwpk-search-function"><form action="/c"><input name="q"></form></div>')
        self.assertTrue(find(r, 'WARN', 'Search Function', text='not on the <form> itself'))
        r = self.page('<form action="/c" splwpk-search-function="splwpk-search-function"><input name="q"></form>')
        self.assertFalse(find(r, 'WARN', 'Search Function'))

    def test_date_only_timestamp_fails(self):
        r = self.page('<a href="/h" splwpk-contact-details="splwpk-contact-details" timestamp="2026-11-12">Hubungi</a>')
        self.assertTrue(find(r, 'FAIL', 'Updated Content: Contact Details', text='not in YYYY-MM-DD HH:MM:SS'))


class Frameworks(unittest.TestCase):
    def page(self, body):
        import tempfile
        f = os.path.join(tempfile.mkdtemp(), 'index.html')
        with open(f, 'w', encoding='utf8') as h:
            h.write('<html lang="ms"><body>' + body + '</body></html>')
        return s.scan_site(f, None, TODAY)

    def test_alpine_bound_tag(self):
        r = self.page('<div x-data="{}" x-bind:splwpk-multilang="ml"><a href="?lang=en">EN</a></div>')
        self.assertTrue(find(r, 'FAIL', 'Rendering', text='splwpk-multilang'))

    def test_vue_shorthand_bound_tag(self):
        self.assertTrue(find(self.page('<div :splwpk-w3c="x">A+</div>'), 'FAIL', 'Rendering', text='splwpk-w3c'))

    def test_icon_reported_once(self):
        r = self.page('<form action="/m"><button><i splwpk-feedback-form="splwpk-feedback-form"></i> Hantar</button></form>')
        self.assertEqual(len(find(r, None, 'Feedback Form')), 1)


class Links(unittest.TestCase):
    LINKS = os.path.join(HERE, 'fixtures', 'links', 'index.html')

    def test_broken_link_found(self):
        r = s.scan_site(self.LINKS, None, TODAY, links='site')
        fails = find(r, 'FAIL', 'Active Link')
        self.assertEqual(len(fails), 1)
        self.assertIn('tiada.html', fails[0]['message'])
        self.assertTrue(fails[0]['fix'])

    def test_same_site_only_by_default(self):
        # ok.html, tiada.html and folder/ (index.html); anchors, mailto and the external MyGov link are skipped
        r = s.scan_site(self.LINKS, None, TODAY, links='site')
        self.assertTrue(find(r, 'INFO', 'Active Link', text='3 unique link(s) tried (same site): 1 broken'))

    def test_off_by_default(self):
        r = s.scan_site(self.LINKS, None, TODAY)
        self.assertFalse(find(r, 'FAIL', 'Active Link'))
        self.assertTrue(find(r, 'INFO', 'Active Link', text='--check-links'))


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
