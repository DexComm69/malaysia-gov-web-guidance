"""Tests for scripts/splask_fix.py (scan --fix). Run: python -m unittest discover -s tests"""
import os, sys, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'scripts'))
import splask_fix as f  # noqa: E402
import splask_scan as s  # noqa: E402

OFFICIAL = set(s.TAGS)


def fix(html):
    return f.fix_html(html, OFFICIAL)


class Fix(unittest.TestCase):
    def test_typo_and_value(self):
        out, ch = fix('<a href="/p" splwpk-sitemaps="splwpk-sitemaps">P</a><a href="/f" splwpk-faq="faq" timestamp="2026-10-01 08:00:00">F</a>')
        self.assertIn('splwpk-sitemap="splwpk-sitemap"', out)
        self.assertIn('splwpk-faq="splwpk-faq"', out)
        self.assertIn('timestamp="2026-10-01 08:00:00"', out)
        self.assertEqual(len(ch), 2)

    def test_icon_to_link_keeps_timestamp(self):
        out, _ = fix('<a href="/h"><i class="i" splwpk-contact-details="splwpk-contact-details" timestamp="2026-11-12 11:30:05"></i> Hubungi</a>')
        self.assertIn('<a href="/h" splwpk-contact-details="splwpk-contact-details" timestamp="2026-11-12 11:30:05">', out)
        self.assertIn('<i class="i">', out)

    def test_wrapper_to_form(self):
        out, _ = fix('<div class="w" splwpk-search-function="splwpk-search-function"><form action="/c"><input name="q"></form></div>')
        self.assertIn('<div class="w">', out)
        self.assertIn('<form action="/c" splwpk-search-function="splwpk-search-function">', out)

    def test_feedback_icon_in_a_link_is_not_moved(self):
        src = '<a href="/maklum-balas"><i splwpk-feedback-form="splwpk-feedback-form"></i> Maklum Balas</a>'
        out, ch = fix(src)
        self.assertEqual((out, ch), (src, []))          # it belongs on a <form>, which isn't here

    def test_mygov_viewport_lang(self):
        out, ch = fix('<!DOCTYPE html><html><head><meta charset="utf-8"><title>T</title></head><body><a href="http://malaysia.gov.my/portal">MyGov</a></body></html>')
        self.assertIn('<html lang="ms">', out)
        self.assertIn('<meta charset="utf-8">\n<meta name="viewport"', out)
        self.assertIn('href="https://www.malaysia.gov.my"', out)
        self.assertEqual(len(ch), 3)

    def test_other_mygov_pages_untouched(self):
        src = '<a href="https://www.malaysia.gov.my/my/perkhidmatan">Perkhidmatan</a>'
        self.assertEqual(fix(src)[0], src)

    def test_never_touches_dates_or_text(self):
        src = '<html lang="ms"><head><meta name="viewport" content="width=device-width"></head><body><a href="/b" splwpk-news="splwpk-news" timestamp="20/11/2026">Berita</a><h1>Selamat</h1></body></html>'
        self.assertEqual(fix(src), (src, []))

    def test_result_scans_better(self):
        src = open(os.path.join(HERE, 'fixtures', 'broken', 'index.html'), encoding='utf8').read()
        out, ch = fix(src)
        import tempfile
        d = tempfile.mkdtemp()
        for name, html in (('a.html', src), ('b.html', out)):
            with open(os.path.join(d, name), 'w', encoding='utf8') as h: h.write(html)
        import datetime as dt
        before = s.counts(s.scan_site(os.path.join(d, 'a.html'), None, dt.datetime(2026, 11, 25)))['FAIL']
        after = s.counts(s.scan_site(os.path.join(d, 'b.html'), None, dt.datetime(2026, 11, 25)))['FAIL']
        self.assertLess(after, before)


if __name__ == '__main__':
    unittest.main()
