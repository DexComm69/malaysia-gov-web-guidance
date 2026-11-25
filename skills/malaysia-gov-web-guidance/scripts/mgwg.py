#!/usr/bin/env python3
"""Search Malaysian government web guidance: MYDS (read live from design.digital.gov.my)
and the hand-written SPLaSK / MYDS guides bundled with this skill.

  python mgwg.py search "<query>" [--limit 8]   rank guides for a task (English or Malay query)
  python mgwg.py list [--category <name>]       list guides (id, status, title)
  python mgwg.py retrieve <id>[,<id>...] [--lang en|ms|both]
                                                print guides; MYDS pages are fetched live (cached 7 days)
  python mgwg.py check-classes <file>... [--css my.css] [--myds-css path]
                                                find classes the MYDS 1.0.0 stylesheet doesn't define

Standard library only (Python 3.8+). MYDS pages need internet access the first time.
This tool is unofficial and is not endorsed by JDN or GovTech Malaysia.
"""
import argparse, json, math, os, re, sys, tempfile, time, urllib.request
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GUIDES = os.path.join(ROOT, 'guides')
INDEX = os.path.join(ROOT, 'references', 'myds-index.json')
CACHE = os.path.join(tempfile.gettempdir(), 'mgwg-cache')
CACHE_DAYS = 7
MYDS_CSS_URL = 'https://cdn.jsdelivr.net/npm/@govtechmy/myds-style@1.0.0/dist/index.css'
UA = 'mgwg/1.0 (unofficial Malaysian gov web guidance skill)'

# Malay -> English query expansion, plus a few English synonyms.
SYN = {
    'carian': 'search', 'cari': 'search', 'borang': 'form', 'log': 'login', 'masuk': 'login', 'daftar': 'registration',
    'pendaftaran': 'registration', 'kata': 'password', 'laluan': 'password', 'pengepala': 'masthead header',
    'kepala': 'header masthead', 'kaki': 'footer', 'warna': 'color colour', 'fon': 'typography font', 'tipografi': 'typography',
    'kebolehcapaian': 'accessibility', 'aksesibiliti': 'accessibility', 'maklum': 'feedback', 'balas': 'feedback',
    'privasi': 'privacy policy', 'dasar': 'policy', 'butang': 'button', 'jadual': 'table data-table', 'tarikh': 'date',
    'pautan': 'link', 'navigasi': 'navbar navigation', 'menu': 'navbar dropdown', 'halaman': 'page', 'utama': 'landing home primary',
    'hubungi': 'contact', 'kami': 'contact', 'peta': 'sitemap', 'laman': 'website site', 'tag': 'tagging splask',
    'penandaan': 'tagging splask', 'kriteria': 'criteria splask', 'pemantauan': 'monitoring splask', 'grid': 'grid layout',
    'susun': 'layout grid', 'atur': 'layout grid', 'gelap': 'dark theme', 'tema': 'theme', 'ikon': 'icon', 'notifikasi': 'toast alert',
    'amaran': 'alert warning callout', 'dialog': 'dialog modal', 'muat': 'upload', 'naik': 'upload', 'fail': 'file upload',
    'senarai': 'list', 'ringkasan': 'summary summarylist', 'kuki': 'cookies banner', 'bahasa': 'language multilang',
    'dwibahasa': 'multilang bilingual language', 'responsif': 'responsive grid breakpoint', 'mudah': 'mobile', 'alih': 'mobile',
    'modal': 'dialog', 'header': 'masthead navbar', 'nav': 'navbar', 'colour': 'color', 'dropdown': 'dropdown select',
    'popup': 'dialog popover', 'php': 'html-css plain laravel', 'html': 'html-css plain', 'css': 'html-css tokens',
    'blade': 'laravel html-css', 'wcag': 'accessibility', 'a11y': 'accessibility', 'seo': 'seo splask',
    'gov.my': 'masthead official', 'official': 'masthead', 'logo': 'footer-logo logo', 'jata': 'footer-logo masthead logo',
    'sla': 'downtime splask', 'uptime': 'downtime splask', 'timestamp': 'tagging splask updated', 'splwpk': 'tagging splask',
}
STOP = set('a an the and or of to for in on with how do i is are my our we use using make build add create page dan atau untuk di ke yang dengan ini itu'.split())


def toks(s):
    return [t for t in re.findall(r'[a-z0-9][a-z0-9.\-]*', s.lower()) if t not in STOP]


def frontmatter(raw):
    m = re.match(r'---\n(.*?)\n---\n', raw, re.S)
    meta = {}
    if m:
        for l in m.group(1).split('\n'):
            k, _, v = l.partition(':')
            v = v.strip()
            if v.startswith('"'):
                try: v = json.loads(v)
                except Exception: v = v.strip('"')
            meta[k.strip()] = v
    return meta, (raw[m.end():] if m else raw)


def load():
    docs = []
    for dp, _, fs in os.walk(GUIDES):
        for f in fs:
            if f.endswith('.md'):
                meta, body = frontmatter(open(os.path.join(dp, f), encoding='utf8').read())
                meta.update(_path=os.path.join(dp, f), _body=body, _kind='local')
                meta.setdefault('id', f[:-3])
                docs.append(meta)
    for p in json.load(open(INDEX, encoding='utf8'))['pages']:
        d = dict(p)
        d.update(_kind='myds', _body=' '.join(p.get('sections', [])),
                 description=('[STUB at source] ' if p['status'] == 'stub' else '') + 'MYDS: ' + p['title'] + ' (' + p['category'] + ')')
        docs.append(d)
    return docs


def search(q, limit):
    docs = load()
    exp = []
    for t in toks(q):
        exp.append((t, 1.0))
        exp += [(s, 0.8) for s in SYN.get(t, '').split()]
    fields = [{'title': toks(d.get('title', '') + ' ' + d.get('title_ms', '') + ' ' + d['id'].replace('-', ' ')),
               'kw': toks(d.get('keywords', '') + ' ' + d.get('category', '')),
               'desc': toks(d.get('description', '') + ' ' + d.get('description_ms', '')),
               'body': toks(d['_body'])} for d in docs]
    N, df = len(docs), {}
    for f in fields:
        for t in set(sum(f.values(), [])):
            df[t] = df.get(t, 0) + 1
    W = {'title': 4.0, 'kw': 3.0, 'desc': 2.0, 'body': 1.0}
    res = []
    for d, f in zip(docs, fields):
        score = 0.0
        for t, w in exp:
            idf = math.log(1 + (N - df.get(t, 0) + 0.5) / (df.get(t, 0) + 0.5))
            for fld, fw in W.items():
                arr = f[fld]
                c = sum(1 for x in arr if x == t or (len(t) > 3 and x.startswith(t)))
                if c:
                    L = max(len(arr), 1)
                    score += w * fw * idf * c * 2.2 / (c + 1.2 * (0.25 + 0.75 * L / (400 if fld == 'body' else 12)))
        if d.get('status') == 'stub': score *= 0.3
        if d.get('category') == 'gov': score *= 1.15
        if score > 0: res.append((score, d))
    res.sort(key=lambda x: -x[0])
    top = res[0][0] if res else 1
    print(json.dumps([{'id': d['id'], 'title': d.get('title', ''), 'category': d.get('category', ''), 'status': d.get('status', ''),
                       'description': d.get('description', '')[:220], 'score': round(s / top, 3)} for s, d in res[:limit]],
                     ensure_ascii=False, indent=1))


def do_list(cat):
    for d in sorted(load(), key=lambda d: (d.get('category', ''), d['id'])):
        if not cat or d.get('category') == cat:
            print(f"{d.get('category',''):24} {d['id']:34} {d.get('status',''):8} {d.get('title','')}")


# ---------- live MYDS fetch ----------
class _Text(HTMLParser):
    BLOCK = {'h1', 'h2', 'h3', 'h4', 'p', 'li', 'pre', 'blockquote'}
    SKIP = ('script', 'style', 'svg', 'nav', 'aside', 'header', 'footer')

    def __init__(s):
        super().__init__(); s.out = []; s.cur = ''; s.skip = 0; s.inmain = 0; s.tag = None; s.row = None; s.cell = None

    def handle_starttag(s, t, a):
        if t in s.SKIP: s.skip += 1
        if t in ('main', 'article'): s.inmain += 1
        if t in s.BLOCK: s.flush(); s.tag = t
        if t == 'br': s.cur += '\n'
        if t == 'tr': s.flush(); s.row = []
        if t in ('td', 'th') and s.row is not None:
            if s.cell is not None: s.row.append(re.sub(r'\s+', ' ', s.cell).strip())
            s.cell = ''

    def handle_endtag(s, t):
        if t in s.SKIP: s.skip = max(0, s.skip - 1)
        if t in s.BLOCK: s.flush()
        if t in ('main', 'article'): s.inmain -= 1
        if t in ('td', 'th') and s.row is not None and s.cell is not None:
            s.row.append(re.sub(r'\s+', ' ', s.cell).strip()); s.cell = None
        if t == 'tr' and s.row is not None:
            if s.cell is not None: s.row.append(re.sub(r'\s+', ' ', s.cell).strip()); s.cell = None
            if s.inmain and any(s.row): s.out.append('| ' + ' | '.join(s.row) + ' |')
            s.row = None

    def handle_data(s, d):
        if not s.skip and s.inmain:
            if s.cell is not None: s.cell += d
            else: s.cur += d

    def flush(s):
        t = s.cur.strip(); s.cur = ''
        if not t: return
        pre = {'h1': '# ', 'h2': '## ', 'h3': '### ', 'h4': '#### ', 'li': '- '}.get(s.tag, '')
        if s.tag == 'pre': t = '```\n' + t + '\n```'
        s.out.append(pre + re.sub(r'[ \t]+', ' ', t))


NAV = {'Previous', 'Next', 'Sebelumnya', 'Seterusnya'}


def page_text(html):
    p = _Text(); p.feed(html); p.flush()
    out, skip_next = [], False
    for l in p.out:
        s = l.strip()
        if s.startswith(('### On this page', '### Di halaman ini')): break
        if skip_next: skip_next = False; continue
        if s in NAV: skip_next = True; continue
        if s in ('On this page', 'Di halaman ini', 'SourceStorybook', 'SumberStorybook') or re.match(r'(PreviewCode|PratontonKod)', s): continue
        if out and out[-1] == l: continue
        out.append(l)
    return '\n'.join(out)


def fetch(url):
    os.makedirs(CACHE, exist_ok=True)
    fn = os.path.join(CACHE, re.sub(r'[^a-z0-9]+', '_', url.lower()) + '.txt')
    if os.path.exists(fn) and time.time() - os.path.getmtime(fn) < CACHE_DAYS * 86400:
        return open(fn, encoding='utf8').read(), True
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    data = urllib.request.urlopen(req, timeout=60).read().decode('utf8', 'replace')
    open(fn, 'w', encoding='utf8').write(data)
    return data, False


def retrieve(ids, lang):
    docs = {d['id']: d for d in load()}
    for i in [x.strip() for x in ids.split(',') if x.strip()]:
        d = docs.get(i)
        if not d:
            close = [k for k in docs if i in k or k in i][:5]
            print(f"!! no guide '{i}'. Did you mean: {', '.join(close) or '(run list)'}")
            continue
        if d['_kind'] == 'local':
            raw = open(d['_path'], encoding='utf8').read()
            if lang in ('en', 'ms'):
                head, _, rest = raw.partition('\n## English\n')
                en, _, ms = rest.partition('\n## Bahasa Melayu\n')
                raw = head + ('\n## English\n' + en if lang == 'en' else '\n## Bahasa Melayu\n' + ms)
            print(raw)
        else:
            langs = ['en', 'ms'] if lang == 'both' else [lang if lang in ('en', 'ms') else 'en']
            print(f"---\nid: {i}\ncategory: {d['category']}\nstatus: {d['status']}\nauthority: MYDS, GovTech Malaysia / Jabatan Digital Negara\n"
                  f"source_en: {d['url_en']}\nsource_ms: {d['url_ms']}\n---\n")
            for lg in langs:
                url = d['url_' + lg]
                try:
                    html, cached = fetch(url)
                    print(f"## {'English' if lg == 'en' else 'Bahasa Melayu'} (live from {url}{', cached' if cached else ''})\n")
                    print(page_text(html))
                except Exception as e:
                    print(f"!! Could not fetch {url} ({e.__class__.__name__}: {e}). Open it in a browser, or retry when online.")
                print()
        print('\n' + '=' * 70 + '\n')


# ---------- class checker ----------
def css_selectors(paths):
    names = set()
    for p in paths:
        css = re.sub(r'/\*.*?\*/', '', open(p, encoding='utf8', errors='replace').read(), flags=re.S)
        for sel in re.findall(r'([^{}]+)\{', css):
            for m in re.finditer(r'\.((?:\\.|[A-Za-z0-9_-])+)', sel):
                names.add(re.sub(r'\\(.)', r'\1', m.group(1)))
    return names


def check_classes(files, extra_css, myds_css):
    if not myds_css:
        try:
            fetch(MYDS_CSS_URL)
            myds_css = os.path.join(CACHE, re.sub(r'[^a-z0-9]+', '_', MYDS_CSS_URL.lower()) + '.txt')
        except Exception as e:
            sys.exit(f"Could not download {MYDS_CSS_URL} ({e}). Download it yourself and pass --myds-css <path>.")
    known = css_selectors([myds_css] + extra_css)
    missing = {}
    for f in files:
        src = open(f, encoding='utf8', errors='replace').read()
        for m in re.finditer(r'class(?:Name)?\s*=\s*(["\'])(.*?)\1', src, re.S):
            val = re.sub(r'<\?.*?\?>|\{\{.*?\}\}|\$\{.*?\}', ' ', m.group(2), flags=re.S)
            for c in val.split():
                if c not in known and not c.startswith(('js-', 'is-', 'has-')):
                    missing.setdefault(c, set()).add(os.path.basename(f))
    if not missing:
        print('All classes are defined (MYDS 1.0.0 + given CSS).')
    for c in sorted(missing):
        print(f'MISSING  {c:34} in {", ".join(sorted(missing[c]))}')
    print(f'\n{len(missing)} class(es) not defined by MYDS 1.0.0' + (' or the given --css files' if extra_css else '') +
          '. Project-specific classes are fine if your own CSS defines them; pass it with --css.')


if __name__ == '__main__':
    try: sys.stdout.reconfigure(encoding='utf-8')
    except Exception: pass
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)
    s = sp.add_parser('search'); s.add_argument('query'); s.add_argument('--limit', type=int, default=8)
    l = sp.add_parser('list'); l.add_argument('--category', default='')
    r = sp.add_parser('retrieve'); r.add_argument('ids'); r.add_argument('--lang', default='both')
    c = sp.add_parser('check-classes'); c.add_argument('files', nargs='+'); c.add_argument('--css', nargs='*', default=[]); c.add_argument('--myds-css', default='')
    a = ap.parse_args()
    if a.cmd == 'search': search(a.query, a.limit)
    elif a.cmd == 'list': do_list(a.category)
    elif a.cmd == 'check-classes': check_classes(a.files, a.css, a.myds_css)
    else: retrieve(a.ids, a.lang)
