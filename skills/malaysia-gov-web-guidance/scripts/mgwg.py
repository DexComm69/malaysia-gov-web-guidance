#!/usr/bin/env python3
"""Search Malaysian government web guidance: MYDS (read live from design.digital.gov.my)
and the hand-written SPLaSK / MYDS guides bundled with this skill.

  python mgwg.py search "<query>" [--limit 8]   rank guides for a task (English or Malay query)
  python mgwg.py list [--category <name>]       list guides (id, status, title)
  python mgwg.py retrieve <id>[,<id>...] [--lang en|ms|both]
                                                print guides; MYDS pages are fetched live (cached 7 days)
  python mgwg.py prefetch all|<category>|<id,...> [--lang en|ms|both]
                                                warm the cache for slow or offline use
  python mgwg.py tokens [--filter otl]          list MYDS theme tokens with light/dark hex values
  python mgwg.py scan <url|file.html> [--list-pages] [--pages all|1,3|privacy,sitemap|<urls>]
                    [--format text|json|md] [--fail-on never|fail|warn]
                                                SPLaSK 2.0 + MYDS pre-check of a site, with a fix for every FAIL
                                                (no JavaScript, like the crawler; see splask_scan.py --help)
  python mgwg.py update-index [--write] [--refresh] [--fail-on-change]
                                                compare the MYDS page index with the live docs navigation
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
BUNDLED_CSS = os.path.join(ROOT, 'assets', 'tokens', 'myds-style-1.0.0.css')  # present in offline builds only
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
    # forms: MYDS has no "form" page, the parts are separate components
    'form': 'input text-input select checkbox radio date-field date-picker text-area label file-upload',
    'forms': 'input text-input select checkbox radio date-field date-picker text-area label file-upload',
    'field': 'input text-input label', 'fields': 'input text-input label', 'validation': 'input text-input error',
    'error': 'text-input input alert-dialog callout', 'medan': 'input text-input label', 'pengesahan': 'input error',
    'permohonan': 'form input registration', 'request': 'form input', 'application': 'form input registration',
    # reviews
    'audit': 'audit checklist review', 'review': 'audit checklist', 'semak': 'audit checklist review',
    'semakan': 'audit checklist review', 'pematuhan': 'compliance audit checklist splask', 'compliance': 'audit checklist splask',
    'status': 'lookup status service-form-pattern', 'lookup': 'lookup service-form-pattern', 'track': 'lookup status',
    'check': 'audit checklist', 'dashboard': 'data-table table grid internal', 'admin': 'internal dashboard',
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
    local_ids = {d['id'] for d in docs}
    for p in json.load(open(INDEX, encoding='utf8'))['pages']:
        if p['id'] in local_ids: continue   # offline builds bundle the page itself
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


def cache_path(url):
    return os.path.join(CACHE, re.sub(r'[^a-z0-9]+', '_', url.lower()) + '.txt')


def fetch(url, attempts=3):
    """Return (html, note). Uses a fresh cache, else the network with retries, else a stale cache.
    Slow or filtered agency networks are common, so a single failed request must not lose the page."""
    os.makedirs(CACHE, exist_ok=True)
    fn = cache_path(url)
    if os.path.exists(fn) and time.time() - os.path.getmtime(fn) < CACHE_DAYS * 86400:
        return open(fn, encoding='utf8').read(), 'cached'
    err = None
    for n in range(attempts):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            data = urllib.request.urlopen(req, timeout=30).read().decode('utf8', 'replace')
            open(fn, 'w', encoding='utf8').write(data)
            return data, 'live'
        except Exception as e:  # network errors vary by platform; retry them all
            err = e
            if n < attempts - 1:
                time.sleep(2 * (n + 1))
    if os.path.exists(fn):
        age = int((time.time() - os.path.getmtime(fn)) / 86400)
        return open(fn, encoding='utf8').read(), f'STALE cache, {age} days old: the live fetch failed'
    raise err


def prefetch(sel, lang):
    """Warm the cache (e.g. before going offline, or on a slow network) so later retrieves are instant."""
    pages = [d for d in load() if d['_kind'] == 'myds']
    if sel != 'all':
        want = set(x.strip() for x in sel.split(','))
        pages = [d for d in pages if d['id'] in want or d['category'] in want]
    langs = ['en', 'ms'] if lang == 'both' else [lang]
    ok = bad = 0
    for d in pages:
        for lg in langs:
            try:
                _, note = fetch(d['url_' + lg]); ok += 1
                print(f'ok    {d["id"]} [{lg}] {note}')
            except Exception as e:
                bad += 1; print(f'FAIL  {d["id"]} [{lg}] {e.__class__.__name__}')
    print(f'\n{ok} cached, {bad} failed. Cache: {CACHE} (kept {CACHE_DAYS} days; stale copies are used if a later fetch fails).')
    try:
        fetch(MYDS_CSS_URL); print('ok    MYDS stylesheet (for check-classes)')
    except Exception as e:
        print(f'FAIL  MYDS stylesheet {e.__class__.__name__}')


def tokens(flt, myds_css):
    """List MYDS theme tokens (bg-/txt-/otl-/fr-) with resolved light and dark hex values."""
    if not myds_css and os.path.exists(BUNDLED_CSS): myds_css = BUNDLED_CSS
    if not myds_css:
        try:
            fetch(MYDS_CSS_URL); myds_css = cache_path(MYDS_CSS_URL)
        except Exception as e:
            sys.exit(f"Could not download {MYDS_CSS_URL} ({e}). Pass --myds-css <path>.")
    css = open(myds_css, encoding='utf8', errors='replace').read()
    prim = dict(re.findall(r'--(_[a-z]+(?:-\d+)?):\s*(\d+ \d+ \d+)', css))
    def block(sel):
        out = {}
        for m in re.finditer(re.escape(sel) + r'\s*\{([^}]*)\}', css):
            out.update(re.findall(r'--((?:bg|txt|otl|fr)-[a-z0-9-]+):\s*([^;}]+)', m.group(1)))
        return out
    def hexof(v):
        m = re.match(r'var\(--(_[a-z]+(?:-\d+)?)\)\s*(/\s*[\d.]+)?', v.strip())
        if not m or m.group(1) not in prim: return v.strip()
        h = '#' + ''.join(f'{int(x):02X}' for x in prim[m.group(1)].split())
        return h + (f' (alpha {m.group(2)[1:].strip()})' if m.group(2) else '') + f'  [{m.group(1)}]'
    light, dark = block(':root'), block('.dark')
    rows = [k for k in light if flt in k]
    print(f'{"token":28} {"light":34} dark')
    for k in rows:
        print(f'--{k:26} {hexof(light[k]):34} {hexof(dark.get(k, "")) if k in dark else "-"}')
    print(f'\n{len(rows)} tokens. Use as rgb(var(--<token>)), e.g. color: rgb(var(--txt-black-900)).')


def outline(d):
    secs = d.get('sections') or []
    return ('Section outline from the index (not the page text): ' + '; '.join(secs)) if secs else 'No outline available.'


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
                    html, note = fetch(url)
                    print(f"## {'English' if lg == 'en' else 'Bahasa Melayu'} (from {url}, {note})\n")
                    print(page_text(html))
                except Exception as e:
                    print(f"!! Could not fetch {url} after 3 attempts ({e.__class__.__name__}: {e}).\n"
                          f"   {outline(d)}\n"
                          f"   Tell the user, give them the URL, and do not fill in MYDS rules from memory. "
                          f"Try again later, or run `prefetch` when the connection is better.")
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


CLASS_TOKEN = re.compile(r'^-?[A-Za-z_][A-Za-z0-9_\-:/.\[\]%#!]*$')
STR_LIT = re.compile(r"'([^'\\]*)'|\"([^\"\\]*)\"|`([^`\\$]*)`")


def strip_template(s):
    """Split a class attribute value into static text and embedded expressions.
    Handles PHP <?...?>, Blade {{ }}, JS ${...} (nested) and HTML built by string concatenation
    (class="tile' + (est ? ' est' : '') + '"). Returns (static_text, expressions)."""
    exprs = []
    def grab(m):
        exprs.append(m.group(0)); return ' '
    s = re.sub(r'<\?.*?\?>|\{\{.*?\}\}|\{!!.*?!!\}', grab, s, flags=re.S)
    out, i = [], 0
    while i < len(s):                      # ${ ... } with nesting
        if s.startswith('${', i):
            depth, j = 1, i + 2
            while j < len(s) and depth:
                depth += {'{': 1, '}': -1}.get(s[j], 0); j += 1
            exprs.append(s[i:j]); out.append(' '); i = j
        else:
            out.append(s[i]); i += 1
    return ''.join(out), exprs


def concat_strings(s, q):
    """HTML built by JS string concatenation, e.g. class="tile' + (est ? ' est' : '') + '".
    Splitting on the JS quote alternates string / code / string ...; keep only the string parts."""
    parts = s.split(q)
    return ' '.join(parts[0::2])


def looks_like_class(t):
    if not CLASS_TOKEN.match(t) or not re.search(r'[A-Za-z]', t):
        return False
    if re.search(r'(?<![0-9])\.|\.(?![0-9])', t):      # dots only inside numbers (px-4.5), not c.id
        return False
    if '[' in t and not re.search(r'-\[', t):          # brackets only for arbitrary values (w-[10px])
        return False
    return True


def class_tokens(val, outer_quote):
    static, exprs = strip_template(val)
    inner = "'" if outer_quote == '"' else '"'
    if inner in static and '+' in static:
        static = concat_strings(static, inner)
    toks = static.split()
    for e in exprs:                        # classes inside ${...} or PHP/Blade: only quoted literals count
        for m in STR_LIT.finditer(e):
            before = e[:m.start()].rstrip()
            after = e[m.end():].lstrip()
            if before.endswith('[') or after.startswith(']'):
                continue                   # array key: $errors['nama']
            if re.search(r'[A-Za-z0-9_]\s*\($', before) or (before.endswith(',') and re.search(r'[A-Za-z_]\w*\s*\([^()]*$', before)):
                continue                   # function argument: __('label'), e('x', 'y')
            toks += ''.join(m.groups(default='')).split()
    return [t for t in toks if looks_like_class(t)]


def check_classes(files, extra_css, myds_css):
    if not myds_css and os.path.exists(BUNDLED_CSS): myds_css = BUNDLED_CSS
    if not myds_css:
        try:
            fetch(MYDS_CSS_URL)
            myds_css = cache_path(MYDS_CSS_URL)
        except Exception as e:
            sys.exit(f"Could not download {MYDS_CSS_URL} ({e}). Download it yourself and pass --myds-css <path>.")
    known = css_selectors([myds_css] + extra_css)
    missing = {}
    for f in files:
        src = open(f, encoding='utf8', errors='replace').read()
        for m in re.finditer(r'\bclass(?:Name)?\s*=\s*(["\'])(.*?)\1', src, re.S):
            for c in class_tokens(m.group(2), m.group(1)):
                if c not in known and not c.startswith(('js-', 'is-', 'has-')):
                    missing.setdefault(c, set()).add(os.path.basename(f))
        for m in re.finditer(r'classList\.(?:add|toggle|remove)\(\s*([\'"])([^\'"]+)\1', src):
            for c in m.group(2).split():
                if CLASS_TOKEN.match(c) and c not in known and not c.startswith(('js-', 'is-', 'has-')):
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
    if len(sys.argv) > 1 and sys.argv[1] == 'scan':   # all scan options live in splask_scan.py
        sys.path.insert(0, HERE); import splask_scan
        sys.exit(splask_scan.main(sys.argv[2:]))
    if len(sys.argv) > 1 and sys.argv[1] == 'update-index':   # options live in myds_index.py
        sys.path.insert(0, HERE); import myds_index
        sys.exit(myds_index.main(sys.argv[2:]))
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)
    s = sp.add_parser('search'); s.add_argument('query'); s.add_argument('--limit', type=int, default=8)
    l = sp.add_parser('list'); l.add_argument('--category', default='')
    r = sp.add_parser('retrieve'); r.add_argument('ids'); r.add_argument('--lang', default='both')
    c = sp.add_parser('check-classes'); c.add_argument('files', nargs='+'); c.add_argument('--css', nargs='*', default=[]); c.add_argument('--myds-css', default='')
    pf = sp.add_parser('prefetch'); pf.add_argument('ids', help="comma-separated ids, a category name, or 'all'"); pf.add_argument('--lang', default='both')
    tk = sp.add_parser('tokens'); tk.add_argument('--filter', default=''); tk.add_argument('--myds-css', default='')
    sp.add_parser('scan', help='SPLaSK pre-check (options: python mgwg.py scan --help)')
    sp.add_parser('update-index', help='check the MYDS page index against the live site (options: python mgwg.py update-index --help)')
    a = ap.parse_args()
    if a.cmd == 'tokens': tokens(a.filter, a.myds_css); sys.exit()
    if a.cmd == 'search': search(a.query, a.limit)
    elif a.cmd == 'list': do_list(a.category)
    elif a.cmd == 'prefetch': prefetch(a.ids, a.lang)
    elif a.cmd == 'check-classes': check_classes(a.files, a.css, a.myds_css)
    else: retrieve(a.ids, a.lang)
