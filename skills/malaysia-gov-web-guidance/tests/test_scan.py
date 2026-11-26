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


class SiteRules(unittest.TestCase):
    def site(self, home_body, pages):
        import tempfile
        d = tempfile.mkdtemp()
        with open(os.path.join(d, 'index.html'), 'w', encoding='utf8') as h:
            h.write('<html lang="ms"><body>' + home_body + '</body></html>')
        for name, body in pages.items():
            with open(os.path.join(d, name), 'w', encoding='utf8') as h:
                h.write('<html lang="ms"><body>' + body + '</body></html>')
        return os.path.join(d, 'index.html')

    def test_misplaced_tag_elsewhere_keeps_home_fail(self):
        home = self.site('<a href="maklum-balas.html">Maklum Balas</a>',
                         {'maklum-balas.html': '<form action="/m"><button><i splwpk-feedback-form="splwpk-feedback-form"></i> Hantar</button></form>'})
        r = s.scan_site(home, 'feedback', TODAY)
        self.assertTrue(find(r, 'FAIL', 'Feedback Form', 'home', 'no `splwpk-feedback-form`'))
        self.assertFalse(find(r, 'WARN', 'Feedback Form', 'home', 'Criteria URL'))

    def test_correct_tag_elsewhere_softens_home_fail(self):
        home = self.site('<a href="maklum-balas.html">Maklum Balas</a>',
                         {'maklum-balas.html': '<form action="/m" splwpk-feedback-form="splwpk-feedback-form"><button>Hantar</button></form>'})
        r = s.scan_site(home, 'feedback', TODAY)
        self.assertTrue(find(r, 'WARN', 'Feedback Form', 'home', 'is not on the home page'))

    def test_splash_hint_only_with_a_home_link(self):
        plain = self.site('<h1>Majlis</h1><a href="hubungi.html">Hubungi</a>', {})
        self.assertFalse(find(s.scan_site(plain, None, TODAY), 'WARN', 'Page choice'))
        splash = self.site('<a href="/utama">Masuk ke laman utama</a>', {})
        self.assertTrue(find(s.scan_site(splash, None, TODAY), 'WARN', 'Page choice', text='splash'))


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


class Targets(unittest.TestCase):
    """data.gov.my titles and GAMMA names, with a fake fetcher (no network). The stand-in pages copy
    only the structure the scanner reads: data.gov.my puts "<title> | data.gov.my" in <title> (BM under
    /ms-MY/, 404 for an unknown id); GAMMA puts the name in div.product-info h2 and returns 200 without
    that block for an unknown id."""
    PAGES = {
        'https://data.gov.my/data-catalogue/air_pollution': (200, '<title>Monthly Air Pollution | data.gov.my</title>'),
        'https://data.gov.my/ms-MY/data-catalogue/air_pollution': (200, '<title>Pencemaran Udara Bulanan | data.gov.my</title>'),
        'https://data.gov.my/data-catalogue/nope': (404, ''),
        'https://data.gov.my/ms-MY/data-catalogue/nope': (404, ''),
        'https://gamma.malaysia.gov.my/app-details/77': (200, '<div class="product-info"><h2 class="title">GAMMA.my</h2></div>'),
        'https://gamma.malaysia.gov.my/app-details/0': (200, '<h2 class="title">Statistik Terkini</h2>'),
    }

    def setUp(self):
        self._get = s.get_page
        s.get_page = lambda u: self.PAGES.get(u, (0, ''))

    def tearDown(self):
        s.get_page = self._get

    def scan(self, links):
        import tempfile
        f = os.path.join(tempfile.mkdtemp(), 'index.html')
        with open(f, 'w', encoding='utf8') as h:
            h.write('<html lang="ms"><body>' + links + '</body></html>')
        return s.scan_site(f, None, TODAY, links='site')

    def test_dataset_title_en_and_bm(self):
        for text in ('Monthly Air Pollution', 'Pencemaran Udara Bulanan', 'monthly air pollution'):
            r = self.scan(f'<a splwpk-open-data="splwpk-open-data" href="https://data.gov.my/data-catalogue/air_pollution">{text}</a>')
            self.assertTrue(find(r, 'PASS', 'Presence of Datasets', text='matches'), text)

    def test_dataset_title_mismatch(self):
        r = self.scan('<a splwpk-open-data="splwpk-open-data" href="https://data.gov.my/data-catalogue/air_pollution">Data Udara</a>')
        f = find(r, 'FAIL', 'Presence of Datasets', text='does not match')
        self.assertTrue(f and 'Monthly Air Pollution' in f[0]['fix'])

    def test_dataset_missing(self):
        r = self.scan('<a splwpk-open-data="splwpk-open-data" href="https://data.gov.my/data-catalogue/nope">Rekaan</a>')
        self.assertTrue(find(r, 'FAIL', 'Presence of Datasets', text='does not exist'))

    def test_gamma_name(self):
        ok = self.scan('<a splwpk-mobile-apps="splwpk-mobile-apps" href="https://gamma.malaysia.gov.my/app-details/77">GAMMA.my</a>')
        self.assertTrue(find(ok, 'PASS', 'Mobile Apps', text='matches'))
        bad = self.scan('<a splwpk-mobile-apps="splwpk-mobile-apps" href="https://gamma.malaysia.gov.my/app-details/77">Aplikasi JDN</a>')
        self.assertTrue(find(bad, 'FAIL', 'Mobile Apps', text='"GAMMA.my"'))
        gone = self.scan('<a splwpk-mobile-apps="splwpk-mobile-apps" href="https://gamma.malaysia.gov.my/app-details/0">Lama</a>')
        self.assertTrue(find(gone, 'FAIL', 'Mobile Apps', text='does not exist'))

    def test_datagov_link_not_a_dataset(self):
        for href in ('https://data.gov.my/', 'https://data.gov.my/dashboard/kawasanku'):
            r = self.scan(f'<a splwpk-open-data="splwpk-open-data" href="{href}">Data terbuka</a>')
            self.assertTrue(find(r, 'FAIL', 'Presence of Datasets', text='not a dataset page'), href)

    def test_unreachable_is_warn(self):
        r = self.scan('<a splwpk-mobile-apps="splwpk-mobile-apps" href="https://gamma.malaysia.gov.my/app-details/5">X</a>')
        self.assertTrue(find(r, 'WARN', 'Mobile Apps', text='could not open'))


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


class MydsAndA11y(unittest.TestCase):
    def page(self, head, body, **kw):
        import tempfile
        f = os.path.join(tempfile.mkdtemp(), 'index.html')
        with open(f, 'w', encoding='utf8') as h:
            h.write(f'<html lang="ms" {kw.get("htmlattr", "")}><head>{head}</head><body>{body}</body></html>')
        return s.scan_site(f, None, TODAY, myds=True, a11y=True)

    GOOD_HEAD = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins&family=Inter">'
    MASTHEAD = '<div class="masthead">Portal Rasmi Kerajaan Malaysia <button>Kenal pasti begini</button></div>'

    def test_clean_page(self):
        r = self.page(self.GOOD_HEAD, '<a href="#k">Langkau ke kandungan utama</a>' + self.MASTHEAD +
                      '<main id="k"><h1>Utama</h1><h2>Berita</h2><label for="q">Cari</label><input id="q" name="q"></main>')
        self.assertFalse([x for x in r['results'] if x['criterion'].startswith(('MYDS:', 'Accessibility:')) and x['level'] == 'WARN'])

    def test_masthead_problems(self):
        self.assertTrue(find(self.page('', '<h1>X</h1>'), 'WARN', 'MYDS: masthead', text='no official masthead'))
        self.assertTrue(find(self.page('', '<h1>X</h1>' + self.MASTHEAD), 'WARN', 'MYDS: masthead', text='after the page heading'))
        self.assertTrue(find(self.page('', '<div>Portal Rasmi Kerajaan Malaysia</div><h1>X</h1>'), 'WARN', 'MYDS: masthead', text='toggle'))

    def test_fonts_and_dark_mode(self):
        r = self.page('<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans" rel="stylesheet">', '<h1>X</h1>', htmlattr='class="dark"')
        self.assertTrue(find(r, 'WARN', 'MYDS: fonts', text='Plus Jakarta Sans'))
        self.assertTrue(find(r, 'WARN', 'MYDS: colour mode'))

    def test_a11y_problems(self):
        r = self.page('', '<h1>X</h1><h3>Y</h3><input name="emel" placeholder="E-mel"><button><i class="icon"></i></button>'
                          '<a href="/x"></a><div id="a"></div><div id="a"></div>')
        for crit, text in (('Accessibility: form labels', 'emel'), ('Accessibility: names', '2 link'), ('Accessibility: headings', 'h1 to h3'),
                           ('Accessibility: duplicate ids', 'a'), ('Accessibility: skip link', 'no "skip')):
            self.assertTrue(find(r, 'WARN', crit, text=text), crit)

    def test_off_by_default(self):
        r = s.scan_site(SITE, None, TODAY)
        self.assertFalse([x for x in r['results'] if x['criterion'].startswith(('MYDS:', 'Accessibility:'))])


class DueAndCriteria(unittest.TestCase):
    def test_due_dates(self):
        r = s.scan_site(SITE, None, TODAY)
        d = {x['tag']: x for x in r['due']}
        self.assertEqual(d['splwpk-contact-details']['due'], '2026-12-01')
        self.assertEqual(d['splwpk-contact-details']['days_left'], 6)
        self.assertNotIn('splwpk-faq', d)                       # FAQ has no freshness limit
        self.assertEqual(r['due'], sorted(r['due'], key=lambda x: x['due']))

    def test_due_within_warns(self):
        r = s.scan_site(SITE, None, TODAY, due_within=7)
        self.assertTrue(find(r, 'WARN', 'Updated Content: Contact Details', text='goes stale on 2026-12-01'))
        self.assertFalse(find(r, 'WARN', 'Updated Content: News', text='goes stale'))

    def test_criteria_url_list(self):
        r = s.scan_site(SITE, 'all', TODAY)
        self.assertEqual(sorted(c['tag'] for c in r['criteria_urls']), ['splwpk-feedback-form', 'splwpk-sitemap'])

    def test_markdown_sections(self):
        out = run_cli(SITE, '--today', '2026-11-25', '--pages', 'all', '--format', 'md')[1]
        self.assertIn('### Freshness due dates', out)
        self.assertIn('### Criteria URLs to register', out)


class Malay(unittest.TestCase):
    def test_text_report_in_bm(self):
        out = run_cli(BROKEN, '--today', '2026-11-25', '--lang', 'ms')[1]
        self.assertIn('Semakan awal SPLaSK 2.0', out)
        self.assertIn('GAGAL', out)
        self.assertIn('bukan tag rasmi; mungkin maksud anda `splwpk-search-function`?', out)
        self.assertIn('Tarikh luput kesegaran', out)

    def test_markdown_in_bm(self):
        out = run_cli(SITE, '--today', '2026-11-25', '--pages', 'all', '--format', 'md', '--lang', 'ms')[1]
        self.assertIn('| | Kriteria | Halaman | Dapatan | Cadangan pembetulan |', out)
        self.assertIn('Criteria URL untuk didaftarkan', out)

    def test_every_criterion_has_a_bm_name(self):
        import splask_i18n as t
        self.assertEqual([c for c, *_ in s.TAGS.values() if c not in t.CRITERIA], [])

    def test_json_stays_english(self):
        r = json.loads(run_cli(SITE, '--today', '2026-11-25', '--format', 'json', '--lang', 'ms')[1])
        self.assertTrue(any(x['criterion'] == 'Search Function' for x in r['results']))


class Render(unittest.TestCase):
    def test_tags_added_by_javascript(self):
        import splask_render as rd
        orig = rd.rendered_html
        rd.rendered_html = lambda target: '<html><body><div splwpk-multilang="splwpk-multilang"></div><a href="/f" splwpk-faq="splwpk-faq">F</a></body></html>'
        try:
            import tempfile
            f = os.path.join(tempfile.mkdtemp(), 'index.html')
            with open(f, 'w', encoding='utf8') as h:
                h.write('<html lang="ms"><body><a href="/f" splwpk-faq="splwpk-faq">F</a></body></html>')
            r = s.scan_site(f, None, TODAY, render=True)
            self.assertTrue(find(r, 'FAIL', 'Rendering', text='(the crawler never sees them): splwpk-multilang'))
        finally:
            rd.rendered_html = orig

    def test_no_browser_is_a_warning(self):
        import splask_render as rd
        orig = rd.rendered_html
        def boom(target): raise RuntimeError('Playwright is not installed')
        rd.rendered_html = boom
        try:
            self.assertTrue(find(s.scan_site(SITE, None, TODAY, render=True), 'WARN', 'Rendering', text='--render skipped'))
        finally:
            rd.rendered_html = orig


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
