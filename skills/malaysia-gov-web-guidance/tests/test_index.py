"""Offline tests for scripts/myds_index.py (update-index), with a fake MYDS site. Run: python -m unittest discover -s tests"""
import contextlib, datetime as dt, io, json, os, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'scripts'))
import myds_index as m  # noqa: E402

B = m.BASE


def navpage(links):
    return '<nav>' + ''.join(f'<a href="{h}">{t}</a>' for h, t in links) + '</nav><article><h1>Intro</h1></article>'


def doc(h1, *sections):
    return f'<nav><h3>MYDS</h3></nav><article><h1>{h1}</h1>' + ''.join(f'<h2>{x}</h2>' for x in sections) + '<figcaption>Import</figcaption></article>'


NAV = [('/en/docs/design/button', 'Button'), ('/en/docs/design/chip', 'Chip'), ('/en/docs/design/colour', 'Colour'),
       ('/en/docs/develop/button', 'Button'), ('/en/docs/develop/date-range-picker', 'Date Range Picker')]
SITE = {
    f'{B}/en/docs/design': (200, navpage(NAV)),
    f'{B}/en/docs/develop': (200, navpage(NAV)),
    f'{B}/en/docs/design/chip': (200, doc('Chip', 'Anatomy', 'States', 'States')),
    f'{B}/ms/docs/design/chip': (200, doc('Cip', 'Anatomi')),
    f'{B}/en/docs/develop/date-range-picker': (200, doc('Date Range Picker', 'Work In Progress')),
    f'{B}/ms/docs/develop/date-range-picker': (200, doc('Pemilih Julat Tarikh', 'Work In Progress')),
    f'{B}/en/docs/design/old-page': (404, ''),
    f'{B}/en/docs/develop/hidden': (200, doc('Hidden')),
}


def entry(pid, title, cat):
    sec, slug = pid.split('-', 1)
    path = f'/docs/{sec}' if slug == 'intro' else f'/docs/{sec}/{slug}'
    return {'id': pid, 'category': cat, 'title': title, 'title_ms': title, 'url_en': f'{B}/en{path}', 'url_ms': f'{B}/ms{path}',
            'status': 'current', 'sections': ['Usage']}


INDEX = {'note': 'test', 'retrieved': '2026-11-01', 'pages': [
    entry('design-intro', 'Design', 'myds-foundation'), entry('develop-intro', 'Develop', 'myds-setup'),
    entry('design-button', 'Button', 'myds-component-design'),
    entry('design-colour', 'Color', 'myds-foundation'),              # renamed on the site: "Colour"
    entry('develop-button', 'Button', 'myds-component-react'),
    entry('design-old-page', 'Old', 'myds-component-design'),        # gone: 404
    entry('develop-hidden', 'Hidden', 'myds-component-react'),       # not in the nav, still online
]}


class UpdateIndex(unittest.TestCase):
    def setUp(self):
        self._get = m.get
        m.get = lambda u, attempts=3: SITE.get(u, (0, ''))
        self.path = os.path.join(tempfile.mkdtemp(), 'myds-index.json')
        with open(self.path, 'w', encoding='utf8') as f:
            json.dump(INDEX, f, ensure_ascii=False, indent=1)

    def tearDown(self):
        m.get = self._get

    def test_report_only_writes_nothing(self):
        before = open(self.path, encoding='utf8').read()
        rep, n = m.run(False, False, self.path)
        self.assertEqual(n, 7)                                          # 5 nav links + 2 section intro pages
        self.assertEqual(rep['new'], ['design-chip', 'develop-date-range-picker'])
        self.assertEqual([r[0] for r in rep['renamed']], ['design-colour'])
        self.assertEqual(rep['removed'], [('design-old-page', 404)])
        self.assertEqual(rep['unlisted'], [('develop-hidden', 200)])
        self.assertEqual(open(self.path, encoding='utf8').read(), before)

    def test_write(self):
        m.run(True, False, self.path, today=dt.date(2026, 12, 1))
        d = json.load(open(self.path, encoding='utf8'))
        pages = {p['id']: p for p in d['pages']}
        self.assertEqual(d['retrieved'], '2026-12-01')
        self.assertNotIn('design-old-page', pages)                     # 404: dropped
        self.assertIn('develop-hidden', pages)                         # still online: kept
        self.assertEqual(pages['design-colour']['title'], 'Colour')
        chip = pages['design-chip']
        self.assertEqual((chip['title'], chip['title_ms'], chip['status']), ('Chip', 'Cip', 'current'))
        self.assertEqual(chip['sections'], ['Anatomy', 'States'])      # article headings only, repeated once
        self.assertEqual(chip['category'], 'myds-component-design')    # from its nav neighbour design-button
        self.assertEqual(chip['url_ms'], f'{B}/ms/docs/design/chip')
        drp = pages['develop-date-range-picker']
        self.assertEqual((drp['status'], drp['title_ms'], drp['category']), ('stub', 'Pemilih Julat Tarikh', 'myds-component-react'))

    def test_up_to_date_after_write(self):
        m.run(True, False, self.path)
        rep, _ = m.run(False, False, self.path)
        self.assertEqual((rep['new'], rep['renamed'], rep['removed']), ([], [], []))

    def test_fail_on_change_exit_code(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(m.main(['--index', self.path, '--fail-on-change']), 1)
            m.main(['--index', self.path, '--write'])
            self.assertEqual(m.main(['--index', self.path, '--fail-on-change']), 0)

    def test_site_down(self):
        m.get = lambda u, attempts=3: (0, '')
        with self.assertRaises(SystemExit):
            m.run(False, False, self.path)


if __name__ == '__main__':
    unittest.main()
