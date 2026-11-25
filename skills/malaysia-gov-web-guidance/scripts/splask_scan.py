#!/usr/bin/env python3
"""SPLaSK 2.0 + MYDS pre-check of a live page (or a local HTML file).

  python splask_scan.py <url-or-file> [--follow] [--json] [--today YYYY-MM-DD]

Reads the HTML the server sends (like the SPLaSK crawler, it does NOT run JavaScript) and checks
the rules in JDN's Manual Tagging SPLaSK V2.0: tag names and spelling, tag placement (<form>, not
on <i>), timestamps and freshness windows, link targets (data.gov.my, GAMMA, MyGov), privacy page,
home-page SEO limits, viewport, HTTPS, redirects and load time. Also checks the MYDS masthead.

It is a PRE-CHECK, not SPLaSK. Some criteria can only be judged by SPLaSK itself (Google top-10
via SerpAPI, uptime, SPLaSK's own load-time measurement, Criteria URLs registered in the profile).
Standard library only. Unofficial; not endorsed by JDN.
"""
import argparse, datetime as dt, difflib, json, os, re, sys, time, urllib.parse, urllib.request
from html.parser import HTMLParser

UA = 'Mozilla/5.0 (compatible; mgwg-splask-scan/1.0; unofficial pre-check)'

# Official tags (Manual Tagging SPLaSK V2.0). value: (criterion, dimension, freshness_days or None, extra)
TAGS = {
    'splwpk-search-function': ('Search Function', 'Ease of Use', None, 'form'),
    'splwpk-advanced-search-function': ('Advanced Search Option', 'Ease of Use', None, 'form'),
    'splwpk-w3c': ('W3C Disability Accessibility', 'Ease of Use', None, ''),
    'splwpk-multilang': ('Multi-Language for Content', 'Accessibility', None, ''),
    'splwpk-sitemap': ('Sitemap', 'Accessibility', None, 'noi'),
    'splwpk-mobile-apps': ('Mobile Apps', 'Accessibility', None, 'gamma'),
    'splwpk-open-data': ('Presence of Datasets', 'Quality of Content', None, 'datagov'),
    'splwpk-publication': ('Publication', 'Quality of Content', None, ''),
    'splwpk-broadcast': ('Updated Content: Broadcast', 'Quality of Content', 30, 'ts'),
    'splwpk-about-us': ('Updated Content: About Us', 'Quality of Content', 30, 'ts'),
    'splwpk-news': ('Updated Content: News', 'Quality of Content', 30, 'ts'),
    'splwpk-gov-policies': ('Updated Content: Government Policies', 'Quality of Content', 30, 'ts'),
    'splwpk-faq': ('Updated Content: FAQ', 'Quality of Content', None, 'ts'),
    'splwpk-client-charter': ('Updated Content: Client Charter', 'Quality of Content', 60, 'ts'),
    'splwpk-contact-details': ('Updated Content: Contact Details', 'Quality of Content', 30, 'ts'),
    'splwpk-online-services': ('Number of Online Services', 'Quality of Content', None, 'href'),
    'splwpk-electronic-archive': ('Electronic Archive', 'Quality of Content', None, 'noi'),
    'splwpk-publicising': ('Publicising Agency CIO/CDO', 'Quality of Content', 30, 'ts noi'),
    'splwpk-freedom': ('Freedom of Information', 'Quality of Content', None, ''),
    'splwpk-procurement': ('Online Procurement Announcement', 'Quality of Content', None, 'noi'),
    'splwpk-online-e-participation': ('Online E-Participation', 'Quality of Content', None, 'noi'),
    'splwpk-privacy-policy': ('Privacy Policy', 'Privacy/Security', None, ''),
    'splwpk-feedback-form': ('Feedback Form', 'Responsiveness', None, 'form'),
}
UNOFFICIAL_OK = {'splwpk-pdpa'}  # seen in community modules; harmless, scores nothing
DEPRECATED = ('acronym applet basefont bgsound big blink center dir font frame frameset isindex keygen listing '
              'marquee menuitem multicol nextid nobr noembed noframes plaintext spacer strike tt xmp').split()
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
MASTHEAD = ('Portal Rasmi Kerajaan Malaysia', 'Official Malaysia Government Website')


class Node:
    __slots__ = ('tag', 'attrs', 'parent', 'children', 'text')
    def __init__(s, tag, attrs, parent):
        s.tag, s.attrs, s.parent, s.children, s.text = tag, attrs, parent, [], []
    def ancestors(s):
        p = s.parent
        while p: yield p; p = p.parent
    def descendants(s):
        for c in s.children:
            yield c; yield from c.descendants()
    def all_text(s):
        return ' '.join(' '.join(s.text).split() + [c.all_text() for c in s.children]).strip()


class Tree(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True)
        s.root = Node('#root', {}, None); s.cur = s.root; s.nodes = []
        s.title = ''; s._in_title = False; s._skip = 0
    def handle_starttag(s, t, a):
        n = Node(t, {k: (v if v is not None else '') for k, v in a}, s.cur)
        s.cur.children.append(n); s.nodes.append(n)
        if t == 'title': s._in_title = True
        if t in ('script', 'style'): s._skip += 1
        if t not in VOID: s.cur = n
    def handle_startendtag(s, t, a):
        n = Node(t, {k: (v if v is not None else '') for k, v in a}, s.cur)
        s.cur.children.append(n); s.nodes.append(n)
    def handle_endtag(s, t):
        if t == 'title': s._in_title = False
        if t in ('script', 'style'): s._skip = max(0, s._skip - 1)
        p = s.cur
        while p is not s.root and p.tag != t: p = p.parent
        if p is not s.root: s.cur = p.parent
    def handle_data(s, d):
        if s._in_title: s.title += d
        elif not s._skip and d.strip(): s.cur.text.append(d)


class CountRedirects(urllib.request.HTTPRedirectHandler):
    def __init__(s): s.hops = []
    def redirect_request(s, req, fp, code, msg, headers, newurl):
        s.hops.append((code, newurl)); return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url, attempts=3):
    last = None
    for n in range(attempts):
        h = CountRedirects(); op = urllib.request.build_opener(h)
        t0 = time.time()
        try:
            r = op.open(urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'ms,en'}), timeout=30)
            body = r.read(); secs = time.time() - t0
            cs = r.headers.get_content_charset() or 'utf-8'
            return body.decode(cs, 'replace'), r.geturl(), h.hops, secs, r.status
        except Exception as e:
            last = e; time.sleep(2 * (n + 1))
    raise last


def parse_ts(v):
    try: return dt.datetime.strptime(v.strip(), '%Y-%m-%d %H:%M:%S')
    except Exception: return None


def scan(target, follow=False, today=None):
    res = []
    def add(level, crit, msg): res.append({'level': level, 'criterion': crit, 'message': msg})
    today = today or dt.datetime.now()
    is_url = re.match(r'https?://', target)
    if is_url:
        html, final, hops, secs, status = fetch(target)
    else:
        html = open(target, encoding='utf8', errors='replace').read(); final, hops, secs, status = target, [], None, 200
    tree = Tree(); tree.feed(html); nodes = tree.nodes

    # ---------- transport (crawler-measured; indicative only) ----------
    if is_url:
        add('PASS' if final.startswith('https://') else 'FAIL', 'HTTPS Availability', f'final URL {final}')
        add('PASS' if len(hops) <= 5 else 'FAIL', 'Loading Time', f'{len(hops)} redirect(s) (max 5)')
        add('PASS' if secs <= 5 else 'WARN', 'Loading Time', f'HTML fetched in {secs:.1f}s from here (SPLaSK measures its own; limit 5s)')

    # ---------- tags ----------
    tagged = {}; fresh_note = {}
    for n in nodes:
        for k in n.attrs:
            if k.startswith('splwpk-') and not k.endswith('-timestamp'):
                tagged.setdefault(k, []).append(n)
    for k in sorted(tagged):
        if k in TAGS or k in UNOFFICIAL_OK: continue
        close = difflib.get_close_matches(k, TAGS.keys(), n=1, cutoff=0.8)
        add('FAIL', 'Tag spelling', f'`{k}` is not an official tag' + (f'; did you mean `{close[0]}`?' if close else ''))
    for k in sorted(UNOFFICIAL_OK & tagged.keys()):
        add('INFO', 'Tag spelling', f'`{k}` is not in the official manual (harmless, scores nothing)')
    for tag, (crit, dim, days, extra) in TAGS.items():
        els = tagged.get(tag, [])
        if not els:
            pair = {'splwpk-news': 'splwpk-gov-policies', 'splwpk-gov-policies': 'splwpk-news'}.get(tag)
            if pair and pair in tagged:   # manual: "news and/or government policies"
                add('INFO', crit, f'no `{tag}`, but `{pair}` is present (the manual accepts either)'); continue
            add('FAIL', crit, f'no `{tag}` found in the server HTML (unless registered as a Criteria URL on another page)'); continue
        on_i = [e for e in els if e.tag == 'i']
        if on_i:
            add('FAIL', crit, f'`{tag}` is on an <i> element ({len(on_i)}x); tag the link/element itself')
        bad_val = [e for e in els if e.attrs.get(tag) != tag]
        if bad_val:
            add('WARN', crit, f'`{tag}` value should repeat the name (found "{bad_val[0].attrs.get(tag)}")')
        ok = True
        if 'form' in extra:
            has_form = any(e.tag == 'form' or any(a.tag == 'form' for a in e.ancestors()) or any(d.tag == 'form' for d in e.descendants()) for e in els)
            if not has_form: ok = False; add('FAIL', crit, f'`{tag}` must be on/around a real <form>')
        if 'ts' in extra:
            stamps = [(e, parse_ts(e.attrs.get('timestamp', ''))) for e in els]
            missing = [e for e, t in stamps if not e.attrs.get('timestamp')]
            badfmt = [e for e, t in stamps if e.attrs.get('timestamp') and not t]
            good = [t for e, t in stamps if t]
            if missing and not good: ok = False; add('FAIL', crit, f'`{tag}` has no timestamp="YYYY-MM-DD HH:MM:SS" ({len(missing)} element(s))')
            elif missing: add('WARN', crit, f'{len(missing)} of {len(els)} `{tag}` elements lack a timestamp (the dated ones are used)')
            if badfmt: ok = False; add('FAIL', crit, f'timestamp not in YYYY-MM-DD HH:MM:SS: "{badfmt[0].attrs.get("timestamp")}"')
            if good and days:
                newest = max(good); age = (today - newest).days
                if age > days: ok = False; add('FAIL', crit, f'newest timestamp {newest:%Y-%m-%d} is {age} days old (limit {days})')
                elif newest > today + dt.timedelta(days=1): ok = False; add('WARN', crit, f'timestamp {newest:%Y-%m-%d} is in the future')
                else: fresh_note[tag] = f'; newest timestamp {newest:%Y-%m-%d}, {age} days old (limit {days})'
            elif good:
                fresh_note[tag] = f'; newest timestamp {max(good):%Y-%m-%d} (no freshness limit)'
        if 'href' in extra:
            if not any(e.attrs.get('href') or any(d.tag == 'a' and d.attrs.get('href') for d in e.descendants()) for e in els):
                ok = False; add('FAIL', crit, f'`{tag}` needs a link with href')
        if 'gamma' in extra:
            links = [e.attrs.get('href', '') for e in els if e.tag == 'a']
            if not any('gamma.malaysia.gov.my' in h for h in links):
                ok = False; add('FAIL', crit, 'mobile-apps tag must be on a link to the app page on gamma.malaysia.gov.my')
        if 'datagov' in extra:
            links = [e.attrs.get('href', '') for e in els if e.tag == 'a'] + [d.attrs.get('href', '') for e in els for d in e.descendants() if d.tag == 'a']
            if not any('data.gov.my' in h for h in links):
                ok = False; add('FAIL', crit, 'open-data tag must link to a dataset on data.gov.my (link text = dataset title)')
            else:
                add('INFO', crit, 'check by hand that the link text equals the dataset title on data.gov.my')
        if tag == 'splwpk-privacy-policy' and not any(e.tag == 'a' and e.attrs.get('href') for e in els):
            ok = False; add('FAIL', crit, '`splwpk-privacy-policy` must be on the link (<a href>) to the privacy page, on every page')
        if ok and not on_i:
            add('PASS', crit, f'`{tag}` found ({len(els)}x)' + fresh_note.get(tag, ''))

    # privacy policy: link + dedicated page with tagged heading containing keyword
    pp = tagged.get('splwpk-privacy-policy', [])
    pp_link = next((e.attrs.get('href') for e in pp if e.tag == 'a' and e.attrs.get('href')), None)
    if follow and pp_link and is_url:
        purl = urllib.parse.urljoin(final, pp_link)
        try:
            phtml = fetch(purl)[0]; pt = Tree(); pt.feed(phtml)
            heads = [n for n in pt.nodes if re.fullmatch(r'h[1-6]', n.tag)]
            kw = [h for h in heads if re.search(r'privasi|privacy', h.all_text(), re.I)]
            if not kw: add('FAIL', 'Privacy Policy', f'privacy page {purl} has no H1-H6 heading containing "privasi"/"privacy"')
            elif not any('splwpk-privacy-policy' in h.attrs for h in kw): add('FAIL', 'Privacy Policy', 'privacy page heading is not tagged splwpk-privacy-policy')
            else: add('PASS', 'Privacy Policy', 'dedicated page has a tagged heading with the keyword')
        except Exception as e:
            add('WARN', 'Privacy Policy', f'could not open privacy page {purl}: {e.__class__.__name__}')
    elif pp_link:
        add('INFO', 'Privacy Policy', 'run with --follow (URLs only) to check the dedicated privacy page heading' if is_url else 'check by hand that the privacy page has a tagged H1-H6 heading containing "privasi"/"privacy"')

    # ---------- untagged crawler rules (home page) ----------
    title = ' '.join(tree.title.split())
    add('PASS' if 0 < len(title) < 70 else 'FAIL', 'SEO', f'<title> is {len(title)} characters (must be under 70): "{title[:80]}"')
    descs = [n.attrs.get('content', '') for n in nodes if n.tag == 'meta' and n.attrs.get('name', '').lower() == 'description']
    d = next((x for x in descs if x.strip()), '')
    add('PASS' if 0 < len(d) < 160 else 'FAIL', 'SEO', f'meta description is {len(d)} characters (must be 1-159)')
    h1 = [n for n in nodes if n.tag == 'h1']
    add('PASS' if len(h1) == 1 else 'FAIL', 'SEO', f'{len(h1)} <h1> on the page (must be exactly 1)')
    noalt = [n for n in nodes if n.tag == 'img' and 'alt' not in n.attrs]
    add('PASS' if not noalt else 'FAIL', 'SEO', f'{len(noalt)} <img> without alt' + (f' (first: {noalt[0].attrs.get("src", "")[:60]})' if noalt else ''))
    dep = sorted({n.tag for n in nodes if n.tag in DEPRECATED})
    add('PASS' if not dep else 'FAIL', 'SEO', 'no deprecated HTML tags' if not dep else f'deprecated tags: {", ".join(dep)}')
    vp = any(n.tag == 'meta' and n.attrs.get('name', '').lower() == 'viewport' and 'width=device-width' in n.attrs.get('content', '') for n in nodes)
    add('PASS' if vp else 'FAIL', 'Device Responsiveness', 'viewport meta present' if vp else 'missing <meta name="viewport" content="width=device-width, initial-scale=1">')
    mygov = [n.attrs.get('href', '') for n in nodes if n.tag == 'a' and 'malaysia.gov.my' in n.attrs.get('href', '')]
    exact = [h for h in mygov if re.fullmatch(r'https://www\.malaysia\.gov\.my/?', h)]
    if exact: add('PASS', 'Link to MyGov Portal', 'link to https://www.malaysia.gov.my found')
    elif mygov: add('WARN', 'Link to MyGov Portal', f'MyGov link is not exactly https://www.malaysia.gov.my: {mygov[0]}')
    else: add('FAIL', 'Link to MyGov Portal', 'no link to https://www.malaysia.gov.my')
    add('INFO', 'Find Website Using Search Tool', 'checked by SPLaSK via Google/SerpAPI (needs the SerpAPI token in the SPLaSK profile)')
    add('INFO', 'Active Link / Downtime', 'checked by the SPLaSK crawler over time; not testable from one page load')

    # ---------- MYDS identity ----------
    page_text = ' '.join(n.all_text() for n in tree.root.children)
    mh = [m for m in MASTHEAD if m in page_text]
    if mh: add('PASS', 'MYDS masthead (not SPLaSK)', 'official masthead wording found in the server HTML')
    elif any(m in html for m in MASTHEAD): add('INFO', 'MYDS masthead (not SPLaSK)', 'masthead wording exists only inside a <script> (built by JavaScript); visitors see it, but it is not in the server HTML')
    else: add('INFO', 'MYDS masthead (not SPLaSK)', 'no official masthead wording ("Portal Rasmi Kerajaan Malaysia" / "Official Malaysia Government Website")')
    js_tags = sorted(set(re.findall(r'splwpk-[a-z0-9-]+', ' '.join(re.findall(r'<script\b[^>]*>(.*?)</script>', html, re.S | re.I)))) - set(tagged))
    if js_tags:
        add('WARN', 'Rendering', f'tags that appear only inside <script> (added by JavaScript, may be invisible to the crawler): {", ".join(js_tags[:8])}')
    comment_markup = ' '.join(re.findall(r'<[a-zA-Z][^<>]*?[\s"\']splwpk-[a-z0-9-]+\s*=[^<>]*>', ' '.join(re.findall(r'<!--(.*?)-->', html, re.S))))
    commented = sorted(set(re.findall(r'splwpk-[a-z0-9-]+', comment_markup)) - set(tagged) - set(js_tags))
    if commented:
        add('FAIL', 'Commented-out tags', f'tags that exist only inside HTML comments <!-- --> (switched off): {", ".join(commented[:8])}')
    lang = next((n.attrs.get('lang', '') for n in nodes if n.tag == 'html'), '')
    add('PASS' if lang else 'WARN', 'Language', f'<html lang="{lang}">' if lang else '<html> has no lang attribute')
    if len(nodes) < 40 or (not tagged and re.search(r'id="(root|app|__next)"', html)):
        add('WARN', 'Rendering', 'very little server HTML: if the site renders with JavaScript, the crawler may not see its content or tags')
    official_found = len(set(tagged) & set(TAGS))
    if official_found < 5:
        homes = [n.attrs.get('href') for n in nodes if n.tag == 'a' and re.search(r'/(utama|home|homepage|laman-utama)(\.\w+)?/?$', n.attrs.get('href', ''), re.I)
                 and 'lang' not in n.attrs.get('href', '').lower()]
        add('WARN', 'Page choice', f'only {official_found} official tag(s) here: this may be a splash/landing page. SPLaSK scans the URL registered in the profile' + (f'; try scanning {urllib.parse.urljoin(final, homes[0])}' if homes else ''))
    return {'target': target, 'final_url': final, 'redirects': len(hops), 'results': res}


def report(r):
    order = {'FAIL': 0, 'WARN': 1, 'INFO': 2, 'PASS': 3}
    rs = sorted(r['results'], key=lambda x: (order[x['level']], x['criterion']))
    print(f"SPLaSK 2.0 pre-check: {r['target']}\n(final URL {r['final_url']}; unofficial, the SPLaSK assessment is the authority)\n")
    for x in rs:
        print(f"{x['level']:5} {x['criterion']:38} {x['message']}")
    c = {k: sum(1 for x in rs if x['level'] == k) for k in order}
    print(f"\n{c['FAIL']} FAIL, {c['WARN']} WARN, {c['PASS']} PASS, {c['INFO']} INFO")


if __name__ == '__main__':
    try: sys.stdout.reconfigure(encoding='utf-8')
    except Exception: pass
    ap = argparse.ArgumentParser()
    ap.add_argument('target'); ap.add_argument('--follow', action='store_true'); ap.add_argument('--json', action='store_true')
    ap.add_argument('--today', default='')
    a = ap.parse_args()
    today = dt.datetime.strptime(a.today, '%Y-%m-%d') if a.today else None
    r = scan(a.target, a.follow, today)
    print(json.dumps(r, ensure_ascii=False, indent=1)) if a.json else report(r)
