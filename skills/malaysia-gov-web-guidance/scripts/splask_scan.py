#!/usr/bin/env python3
"""SPLaSK 2.0 + MYDS pre-check of a live site (or local HTML files).

  python splask_scan.py <home-url-or-file>                     home page only
  python splask_scan.py <home> --list-pages                    list the pages that can be scanned
  python splask_scan.py <home> --pages all                     home + every page found
  python splask_scan.py <home> --pages 1,3                     home + pages by number (from --list-pages)
  python splask_scan.py <home> --pages privacy,sitemap         home + pages by name
  python splask_scan.py <home> --pages /dasar-privasi,https://site.gov.my/peta-laman
  python splask_scan.py <home> --pages all --check-links     also check every same-site link (Active Link)
  options: --format text|json|md   --fail-on never|fail|warn   --max-pages N   --check-links [site|all]   --max-links N
           --md-out FILE   --today YYYY-MM-DD

Reads the HTML the server sends (like the SPLaSK crawler, it does NOT run JavaScript) and checks
the rules in JDN's Manual Tagging SPLaSK V2.0: tag names and spelling, tag placement (<form>, not
on <i>), timestamps and freshness windows, link targets (data.gov.my, GAMMA, MyGov), the privacy
page, home-page SEO limits, viewport, HTTPS, redirects and load time. Also checks the MYDS masthead.
Every FAIL comes with a suggested fix.

It is a PRE-CHECK, not SPLaSK. Some criteria can only be judged by SPLaSK itself (Google top-10
via SerpAPI, uptime, SPLaSK's own load-time measurement). Standard library only. Unofficial.
"""
import argparse, datetime as dt, difflib, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from html.parser import HTMLParser

UA = 'Mozilla/5.0 (compatible; mgwg-splask-scan/1.1; unofficial pre-check)'

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

# Pages a SPLaSK review usually needs: name -> (tags that point at it, link-text keywords)
PAGE_KINDS = {
    'privacy': (['splwpk-privacy-policy'], r'\b(dasar privasi|privasi|privacy)\b'),
    'sitemap': (['splwpk-sitemap'], r'\b(peta laman|peta portal|sitemap|site map)\b'),
    'feedback': (['splwpk-feedback-form'], r'\b(maklum ?balas|feedback|aduan)\b'),
    'search': (['splwpk-search-function', 'splwpk-advanced-search-function'], r'\b(carian terperinci|advanced search|carian|search)\b'),
    'contact': (['splwpk-contact-details'], r'\b(hubungi kami|hubungi|contact us|contact)\b'),
    'faq': (['splwpk-faq'], r'\b(soalan lazim|faq)\b'),
    'about': (['splwpk-about-us'], r'\b(tentang kami|mengenai kami|profil|about us)\b'),
    'news': (['splwpk-news', 'splwpk-broadcast', 'splwpk-gov-policies'], r'\b(berita|pengumuman|news|announcement)\b'),
    'client-charter': (['splwpk-client-charter'], r'\b(piagam pelanggan|client charter)\b'),
    'publication': (['splwpk-publication'], r'\b(penerbitan|publication)\b'),
    'archive': (['splwpk-electronic-archive'], r'\b(arkib|archive)\b'),
    'procurement': (['splwpk-procurement'], r'\b(sebut ?harga|tender|perolehan|procurement)\b'),
    'e-participation': (['splwpk-online-e-participation'], r'\b(e-?penyertaan|e-?participation)\b'),
    'cio': (['splwpk-publicising'], r'\b(ketua pegawai digital|cio|cdo)\b'),
    'freedom': (['splwpk-freedom'], r'\b(kebebasan maklumat|freedom of information)\b'),
}


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


def load(target, base=None):
    """URL or local file -> (html, final, hops, secs). Relative paths resolve against base (URL or file)."""
    if base and not re.match(r'https?://', target) and not os.path.isabs(target) and not os.path.isfile(target):
        if re.match(r'https?://', base): target = urllib.parse.urljoin(base, target)
        else: target = os.path.normpath(os.path.join(os.path.dirname(base), target.lstrip('/')))
    if re.match(r'https?://', target):
        html, final, hops, secs, _ = fetch(target)
        return html, final, hops, secs
    with open(target, encoding='utf8', errors='replace') as fh:
        return fh.read(), target, [], None


def looks_generated(stamps, today):
    """A timestamp within 15 minutes of now (live scan), or dated the scan day when --today is given."""
    now = dt.datetime.now()
    if today.date() == now.date():
        return any(abs((t - now).total_seconds()) < 900 for t in stamps)
    return any(t.date() == today.date() for t in stamps)


def parse_ts(v):
    try: return dt.datetime.strptime(v.strip(), '%Y-%m-%d %H:%M:%S')
    except Exception: return None


def tags_of(nodes):
    tagged = {}
    for n in nodes:
        for k in n.attrs:
            if k.startswith('splwpk-') and not k.endswith('-timestamp'):
                tagged.setdefault(k, []).append(n)
    return tagged


# ---------- fix suggestions ----------
def fix_missing(tag):
    crit, dim, days, extra = TAGS[tag]
    ts = ' timestamp="YYYY-MM-DD HH:MM:SS"' if 'ts' in extra else ''
    if 'form' in extra:
        return f'<form action="/carian" role="search" {tag}="{tag}">…</form>' if 'search' in tag else f'<form action="/maklum-balas" method="post" {tag}="{tag}">…</form> (the tag goes on the <form> itself)'
    if 'gamma' in extra: return f'<a href="https://gamma.malaysia.gov.my/app-details/<id>" {tag}="{tag}">App name as listed in GAMMA</a>'
    if 'datagov' in extra: return f'<a href="https://data.gov.my/…" {tag}="{tag}">Exact dataset title on data.gov.my</a>'
    if tag == 'splwpk-multilang': return f'<div {tag}="{tag}"><a href="?lang=ms" lang="ms">BM</a> | <a href="?lang=en" lang="en">EN</a></div>'
    if tag == 'splwpk-w3c': return f'<div role="group" aria-label="Saiz tulisan" {tag}="{tag}"><button type="button">A-</button><button type="button">A+</button></div>'
    return f'<a href="/…" {tag}="{tag}"{ts}>…</a>' + ('  (timestamp = the real date the content last changed)' if ts else '')


def check_page(html, final, is_home, today, add, page_label, hops=(), secs=None, is_url=False, check_links_on=False, due=None):
    """Run the checks for one page. Home pages get every check; other pages get tag and page-specific checks."""
    tree = Tree(); tree.feed(html); nodes = tree.nodes
    tagged = tags_of(nodes); fresh = {}
    A = lambda level, crit, msg, fix=None: add(level, crit, msg, fix, page_label)

    if is_url and is_home:
        A('PASS' if final.startswith('https://') else 'FAIL', 'HTTPS Availability', f'final URL {final}',
          None if final.startswith('https://') else 'serve the site over HTTPS and redirect http:// to https://')
        A('PASS' if len(hops) <= 5 else 'FAIL', 'Loading Time', f'{len(hops)} redirect(s) (max 5)',
          None if len(hops) <= 5 else 'link straight to the final URL; remove redirect chains')
        if secs is not None:
            A('PASS' if secs <= 5 else 'WARN', 'Loading Time', f'HTML fetched in {secs:.1f}s from here (SPLaSK measures its own; limit 5s)',
              None if secs <= 5 else 'reduce page weight, enable caching and compression')

    for k in sorted(tagged):
        if k in TAGS or k in UNOFFICIAL_OK: continue
        close = difflib.get_close_matches(k, TAGS.keys(), n=1, cutoff=0.8)
        A('FAIL', 'Tag spelling', f'`{k}` is not an official tag' + (f'; did you mean `{close[0]}`?' if close else ''),
          f'rename to {close[0]}="{close[0]}"' if close else 'remove it, or use a tag from the official list (splask-tagging)')
    for k in sorted(UNOFFICIAL_OK & tagged.keys()):
        A('INFO', 'Tag spelling', f'`{k}` is not in the official manual (harmless, scores nothing)')

    for tag, (crit, dim, days, extra) in TAGS.items():
        els = tagged.get(tag, [])
        if not els:
            if is_home:
                pair = {'splwpk-news': 'splwpk-gov-policies', 'splwpk-gov-policies': 'splwpk-news'}.get(tag)
                if pair and pair in tagged:
                    A('INFO', crit, f'no `{tag}`, but `{pair}` is present (the manual accepts either)'); continue
                A('FAIL', crit, f'no `{tag}` in the home page HTML', fix_missing(tag))
            continue
        ok = True
        on_i = [e for e in els if e.tag == 'i']
        if on_i:
            ok = False
            A('FAIL', crit, f'`{tag}` is on an <i> element ({len(on_i)}x)', f'move {tag}="{tag}" from the <i> icon to its <a> link' + (' or <form>' if 'form' in extra else ''))
        bad_val = [e for e in els if e.attrs.get(tag) != tag]
        if bad_val:
            A('WARN', crit, f'`{tag}` value should repeat the name (found "{bad_val[0].attrs.get(tag)}")', f'{tag}="{tag}"')
        if 'form' in extra:
            if not any(e.tag == 'form' or any(a.tag == 'form' for a in e.ancestors()) or any(d.tag == 'form' for d in e.descendants()) for e in els):
                ok = False; A('FAIL', crit, f'`{tag}` must be on a real <form>', fix_missing(tag))
            elif not any(e.tag == 'form' for e in els) and not on_i:
                wrap = next(e for e in els if e.tag != 'form')
                A('WARN', crit, f'`{tag}` is on a <{wrap.tag}> around (or inside) the form, not on the <form> itself; the manual puts it on the <form>',
                  f'move {tag}="{tag}" onto the <form> element (in a CMS, in the form module template override)')
        if 'ts' in extra:
            stamps = [(e, parse_ts(e.attrs.get('timestamp', ''))) for e in els]
            missing = [e for e, t in stamps if not e.attrs.get('timestamp')]
            badfmt = [e for e, t in stamps if e.attrs.get('timestamp') and not t]
            good = [t for e, t in stamps if t]
            if missing and not good:
                ok = False; A('FAIL', crit, f'`{tag}` has no timestamp ({len(missing)} element(s))', f'add timestamp="YYYY-MM-DD HH:MM:SS" from the content\'s real last-updated date')
            elif missing:
                A('WARN', crit, f'{len(missing)} of {len(els)} `{tag}` elements lack a timestamp (the dated ones are used)')
            if badfmt:
                ok = False; A('FAIL', crit, f'timestamp not in YYYY-MM-DD HH:MM:SS: "{badfmt[0].attrs.get("timestamp")}"', 'timestamp="2026-11-24 09:15:00" (24-hour)')
            if good and days:
                newest = max(good); age = max(0, (today.date() - newest.date()).days)
                if due is not None:
                    due.append({'tag': tag, 'criterion': crit, 'page': page_label, 'last_update': newest.strftime('%Y-%m-%d'),
                                'limit_days': days, 'due': (newest + dt.timedelta(days=days)).strftime('%Y-%m-%d'),
                                'days_left': days - age})
                if age > days:
                    ok = False; A('FAIL', crit, f'newest timestamp {newest:%Y-%m-%d} is {age} days old (limit {days})', f'update the content itself, then set timestamp to that real date (a fake date fails SPLaSK anyway)')
                elif newest > today + dt.timedelta(days=1):
                    ok = False; A('WARN', crit, f'timestamp {newest:%Y-%m-%d} is in the future', 'use the real last-updated date')
                else: fresh[tag] = f'; newest timestamp {newest:%Y-%m-%d}, {age} days old (limit {days})'
            elif good:
                fresh[tag] = f'; newest timestamp {max(good):%Y-%m-%d} (no freshness limit)'
            if good and looks_generated(good, today):
                A('WARN', crit, f'`{tag}` timestamp is the scan date/time ({max(good):%Y-%m-%d %H:%M}): check it is the real date the content changed, not the time the page was generated',
                  "take it from the CMS's modified date (WordPress get_the_modified_date('Y-m-d H:i:s', $id), Joomla HTMLHelper::_('date', $item->modified, 'Y-m-d H:i:s')); never the current time")
        if 'href' in extra and not any(e.attrs.get('href') or any(d.tag == 'a' and d.attrs.get('href') for d in e.descendants()) for e in els):
            ok = False; A('FAIL', crit, f'`{tag}` needs a link with href', fix_missing(tag))
        if 'gamma' in extra and not any('gamma.malaysia.gov.my' in e.attrs.get('href', '') for e in els if e.tag == 'a'):
            ok = False; A('FAIL', crit, 'mobile-apps tag must be on a link to the app page on gamma.malaysia.gov.my', fix_missing(tag))
        if 'datagov' in extra:
            links = [e.attrs.get('href', '') for e in els if e.tag == 'a'] + [d.attrs.get('href', '') for e in els for d in e.descendants() if d.tag == 'a']
            if not any('data.gov.my' in h for h in links):
                ok = False; A('FAIL', crit, 'open-data tag must link to a dataset on data.gov.my (link text = dataset title)', fix_missing(tag))
            else:
                if not check_links_on: A('INFO', crit, 'link text must equal the dataset title on data.gov.my; add --check-links to compare it')
        if tag == 'splwpk-privacy-policy' and is_home and not any(e.tag == 'a' and e.attrs.get('href') for e in els) \
                and not any(re.fullmatch(r'h[1-6]', e.tag) for e in els):
            ok = False; A('FAIL', crit, '`splwpk-privacy-policy` must be on the link (<a href>) to the privacy page, on every page',
                          '<a href="/dasar-privasi" splwpk-privacy-policy="splwpk-privacy-policy">Dasar Privasi</a>')
        if ok:
            A('PASS', crit, f'`{tag}` found ({len(els)}x)' + fresh.get(tag, ''))

    # privacy page heading rule (manual: dedicated page with tagged H1-H6 containing the keyword)
    heads = [n for n in nodes if re.fullmatch(r'h[1-6]', n.tag) and re.search(r'privasi|privacy', n.all_text(), re.I)]
    if not is_home and (page_label == 'privacy' or re.search(r'privasi|privacy', tree.title, re.I)):
        if not heads:
            A('FAIL', 'Privacy Policy', 'privacy page has no H1-H6 heading containing "privasi"/"privacy"',
              '<h1 splwpk-privacy-policy="splwpk-privacy-policy">Dasar Privasi</h1>')
        elif not any('splwpk-privacy-policy' in h.attrs for h in heads):
            A('FAIL', 'Privacy Policy', 'privacy page heading is not tagged',
              '<h1 splwpk-privacy-policy="splwpk-privacy-policy">Dasar Privasi</h1>')
        else:
            A('PASS', 'Privacy Policy', 'dedicated privacy page has a tagged heading with the keyword')

    if is_home:
        title = ' '.join(tree.title.split())
        A('PASS' if 0 < len(title) < 70 else 'FAIL', 'SEO', f'<title> is {len(title)} characters (must be under 70): "{title[:80]}"',
          None if 0 < len(title) < 70 else '<title>Agency name, short (under 70 characters)</title>')
        descs = [n.attrs.get('content', '') for n in nodes if n.tag == 'meta' and n.attrs.get('name', '').lower() == 'description']
        d = next((x for x in descs if x.strip()), '')
        A('PASS' if 0 < len(d) < 160 else 'FAIL', 'SEO', f'meta description is {len(d)} characters (must be 1-159)',
          None if 0 < len(d) < 160 else '<meta name="description" content="One-sentence summary of the site (under 160 characters)">')
        h1 = [n for n in nodes if n.tag == 'h1']
        A('PASS' if len(h1) == 1 else 'FAIL', 'SEO', f'{len(h1)} <h1> on the page (must be exactly 1)',
          None if len(h1) == 1 else ('keep one <h1> (the agency name or the page title, not both); make a site name repeated in the header a <p> or <a>, and other headings <h2>' if h1 else 'add one <h1> with the agency name or page subject'))
        noalt = [n for n in nodes if n.tag == 'img' and 'alt' not in n.attrs]
        A('PASS' if not noalt else 'FAIL', 'SEO', f'{len(noalt)} <img> without alt' + (f' (first: {noalt[0].attrs.get("src", "")[:60]})' if noalt else ''),
          None if not noalt else 'add alt="what the image shows" (or alt="" for purely decorative images)')
        dep = sorted({n.tag for n in nodes if n.tag in DEPRECATED})
        A('PASS' if not dep else 'FAIL', 'SEO', 'no deprecated HTML tags' if not dep else f'deprecated tags: {", ".join(dep)}',
          None if not dep else 'replace with modern HTML + CSS (e.g. <center> -> style="text-align:center")')
        vp = any(n.tag == 'meta' and n.attrs.get('name', '').lower() == 'viewport' and 'width=device-width' in n.attrs.get('content', '') for n in nodes)
        A('PASS' if vp else 'FAIL', 'Device Responsiveness', 'viewport meta present' if vp else 'missing viewport meta',
          None if vp else '<meta name="viewport" content="width=device-width, initial-scale=1">')
        mygov = [n.attrs.get('href', '') for n in nodes if n.tag == 'a' and 'malaysia.gov.my' in n.attrs.get('href', '')]
        exact = [h for h in mygov if re.fullmatch(r'https://www\.malaysia\.gov\.my/?', h)]
        if exact: A('PASS', 'Link to MyGov Portal', 'link to https://www.malaysia.gov.my found')
        elif mygov: A('WARN', 'Link to MyGov Portal', f'MyGov link is not exactly https://www.malaysia.gov.my: {mygov[0]}', '<a href="https://www.malaysia.gov.my">MyGov</a>')
        else: A('FAIL', 'Link to MyGov Portal', 'no link to https://www.malaysia.gov.my', '<a href="https://www.malaysia.gov.my">MyGov</a> (usually in the footer)')
        A('INFO', 'Find Website Using Search Tool', 'checked by SPLaSK via Google/SerpAPI (needs the SerpAPI token in the SPLaSK profile)')
        A('INFO', 'Downtime', 'checked by the SPLaSK crawler over time; not testable from one page load')
        if not check_links_on: A('INFO', 'Active Link', 'links not checked; add --check-links to test every link on the scanned pages')
        page_text = ' '.join(n.all_text() for n in tree.root.children)
        if any(m in page_text for m in MASTHEAD): A('PASS', 'MYDS masthead (not SPLaSK)', 'official masthead wording found in the server HTML')
        elif any(m in html for m in MASTHEAD): A('INFO', 'MYDS masthead (not SPLaSK)', 'masthead wording exists only inside a <script> (built by JavaScript)')
        else: A('INFO', 'MYDS masthead (not SPLaSK)', 'no official masthead wording ("Portal Rasmi Kerajaan Malaysia" / "Official Malaysia Government Website")')
        lang = next((n.attrs.get('lang', '') for n in nodes if n.tag == 'html'), '')
        A('PASS' if lang else 'WARN', 'Language', f'<html lang="{lang}">' if lang else '<html> has no lang attribute', None if lang else '<html lang="ms">')
        if (len(nodes) < 40 and len(set(tagged) & set(TAGS)) < 3) or (not tagged and re.search(r'id="(root|app|__next)"', html)):
            A('WARN', 'Rendering', 'very little server HTML: if the site renders with JavaScript, the crawler may not see its content or tags',
              'render the page (or at least its tags) on the server')
        official = len(set(tagged) & set(TAGS))
        homes = [] if official >= 5 else [n.attrs.get('href') for n in nodes if n.tag == 'a' and re.search(r'/(utama|home|homepage|laman-utama)(\.\w+)?/?$', n.attrs.get('href', ''), re.I)
                     and 'lang' not in n.attrs.get('href', '').lower()
                     and urllib.parse.urljoin(final, n.attrs.get('href', '')).rstrip('/') != final.rstrip('/')]
        if homes:
            A('WARN', 'Page choice', f'only {official} official tag(s) here: this may be a splash/landing page. SPLaSK scans the URL registered in the profile'
              + f'; try scanning {urllib.parse.urljoin(final, homes[0])}')

    js_tags = sorted(set(re.findall(r'splwpk-[a-z0-9-]+', ' '.join(re.findall(r'<script\b[^>]*>(.*?)</script>', html, re.S | re.I)))) - set(tagged))
    bound = sorted({k.split(':', 1)[1] for n in nodes for k in n.attrs
                    if re.match(r'(x-bind|v-bind)?:splwpk-[a-z0-9-]+$', k)} - set(tagged))
    if bound:
        A('FAIL', 'Rendering', f'tags bound by JavaScript (Alpine.js / Vue `x-bind:` or `:` attributes), so the crawler never sees them: {", ".join(bound[:8])}',
          'write the plain attribute in the server HTML, e.g. splwpk-multilang="splwpk-multilang" (not x-bind:splwpk-multilang)')
    js_tags = sorted(set(js_tags) - set(bound))
    if js_tags:
        A('WARN', 'Rendering', f'tags that appear only inside <script> (added by JavaScript, may be invisible to the crawler): {", ".join(js_tags[:8])}',
          'output these attributes in the server HTML instead of adding them with JavaScript')
    comment_markup = ' '.join(re.findall(r'<[a-zA-Z][^<>]*?[\s"\']splwpk-[a-z0-9-]+\s*=[^<>]*>', ' '.join(re.findall(r'<!--(.*?)-->', html, re.S))))
    commented = sorted(set(re.findall(r'splwpk-[a-z0-9-]+', comment_markup)) - set(tagged) - set(js_tags))
    if commented:
        A('FAIL', 'Commented-out tags', f'tags that exist only inside HTML comments <!-- --> (switched off): {", ".join(commented[:8])}',
          'remove the <!-- --> around that markup, or add the tag to the live element')
    return tree, tagged


def discover(home_html, home_url):
    """Find candidate pages linked from the home page: tagged links first, then keyword matches. Same site only."""
    tree = Tree(); tree.feed(home_html)
    is_url = re.match(r'https?://', home_url)
    host = urllib.parse.urlparse(home_url).netloc if is_url else None
    found = {}

    def norm(href):
        if not href or href.startswith(('#', 'javascript:', 'mailto:', 'tel:')): return None
        if is_url:
            u = urllib.parse.urljoin(home_url, href).split('#')[0]
            return u if urllib.parse.urlparse(u).netloc == host and u.rstrip('/') != home_url.rstrip('/') else None
        if re.match(r'https?://', href): return None
        p = os.path.normpath(os.path.join(os.path.dirname(home_url), href.lstrip('/').split('#')[0].split('?')[0]))
        return p if os.path.isfile(p) and os.path.abspath(p) != os.path.abspath(home_url) else None

    links = [n for n in tree.nodes if n.tag == 'a' and n.attrs.get('href')]
    text = lambda n: n.all_text() + ' ' + n.attrs.get('href', '').replace('-', ' ').replace('/', ' ')
    for name, (tags, kw) in PAGE_KINDS.items():
        tests = [lambda n, t=t: t in n.attrs for t in tags]                      # 1) the link itself carries the tag
        tests.append(lambda n: any(t in a.attrs for a in n.ancestors() for t in tags) and re.search(kw, text(n), re.I))  # 2) inside a tagged block + keyword
        tests.append(lambda n: re.search(kw, text(n), re.I))                     # 3) keyword only
        cand = None
        for test in tests:
            for n in links:
                if test(n):
                    u = norm(n.attrs['href'])
                    if u and u not in found.values(): cand = u; break
            if cand: break
        if cand: found[name] = cand
    return found


def link_targets(tree, page_url, is_url, scope):
    """(target, link text) for every <a href> worth checking. scope 'site' = same site only, 'all' = external too."""
    host = urllib.parse.urlparse(page_url).netloc if is_url else None
    out = []
    for n in tree.nodes:
        h = (n.attrs.get('href') or '').strip() if n.tag == 'a' else ''
        if not h or h.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'data:')): continue
        if is_url:
            u = urllib.parse.urljoin(page_url, h).split('#')[0]
            if not u.startswith(('http://', 'https://')): continue
            if scope != 'all' and urllib.parse.urlparse(u).netloc != host: continue
        elif re.match(r'https?://', h):
            if scope != 'all': continue
            u = h.split('#')[0]
        else:
            rel = urllib.parse.unquote(h.split('#')[0].split('?')[0])
            if not rel: continue
            u = os.path.normpath(os.path.join(os.path.dirname(page_url), rel.lstrip('/')))
        out.append((u, ' '.join(n.all_text().split())[:40]))
    return out


def check_link(u):
    """-> (state, detail): state is 'ok', 'broken' or 'unreachable'."""
    if not re.match(r'https?://', u):
        ok = os.path.isfile(u) or os.path.isfile(os.path.join(u, 'index.html'))
        return ('ok', 'file') if ok else ('broken', 'file not found')
    last = ('unreachable', 'no response')
    for method in ('HEAD', 'GET'):
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, method=method, headers={'User-Agent': UA}), timeout=15)
            return 'ok', str(r.status)
        except urllib.error.HTTPError as e:
            if method == 'HEAD' and (e.code in (401, 403, 405, 429, 501) or e.code >= 500):
                last = ('broken', f'HTTP {e.code}'); continue          # some servers refuse HEAD: retry with GET
            if e.code in (401, 403, 429): return 'unreachable', f'HTTP {e.code} (blocked or rate-limited)'
            return 'broken', f'HTTP {e.code}'
        except Exception as e:
            last = ('unreachable', e.__class__.__name__)
    return last


def get_page(url):
    """-> (status, html). status 0 = no response. Replaceable in tests."""
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'ms,en'}), timeout=30)
        cs = r.headers.get_content_charset() or 'utf-8'
        return r.status, r.read().decode(cs, 'replace')
    except urllib.error.HTTPError as e:
        return e.code, ''
    except Exception:
        return 0, ''


def norm_title(t):
    import html as _h
    return re.sub(r'[\s"\'\u2018\u2019\u201c\u201d.,:;()\-]+', ' ', _h.unescape(t or '')).strip().casefold()


def datagov_titles(url):
    """Dataset titles (English and Malay) for a data.gov.my link -> ('ok'|'missing'|'unreachable', [titles])."""
    parts = urllib.parse.urlparse(url)
    path = re.sub(r'^/(ms-MY|en-GB)(?=/)', '', parts.path)
    if not re.match(r'^/data-catalogue/[^/]+/?$', path):
        return 'not-dataset', []
    titles, states = [], []
    for prefix in ('', '/ms-MY'):
        st, html = get_page(f'{parts.scheme}://{parts.netloc}{prefix}{path}')
        states.append(st)
        m = re.search(r'<title>(.*?)</title>', html, re.S | re.I)
        t = re.sub(r'\s*\|\s*data\.gov\.my\s*$', '', ' '.join(m.group(1).split())) if m else ''
        if st == 200 and t and not t.lower().startswith('oops'):
            titles.append(t)
    if titles: return 'ok', titles
    return ('missing' if 404 in states else 'unreachable'), []


def gamma_name(url):
    """App name on a GAMMA app page -> ('ok'|'missing'|'unreachable', [name])."""
    st, html = get_page(url)
    if st == 404: return 'missing', []
    if st != 200: return 'unreachable', []
    t = Tree(); t.feed(html)
    for n in t.nodes:
        if n.tag == 'div' and 'product-info' in n.attrs.get('class', '').split():
            h = next((d for d in n.descendants() if d.tag == 'h2'), None)
            if h and h.all_text(): return 'ok', [' '.join(h.all_text().split())]
    return 'missing', []


def check_targets(pages_trees, add):
    """--check-links: data.gov.my dataset titles and GAMMA app names must match the tagged link text."""
    jobs = []
    for name, tree, url in pages_trees:
        for tag, host, crit, lookup, what in (('splwpk-open-data', 'data.gov.my', 'Presence of Datasets', datagov_titles, 'dataset title'),
                                             ('splwpk-mobile-apps', 'gamma.malaysia.gov.my', 'Mobile Apps', gamma_name, 'app name')):
            for e in [n for n in tree.nodes if tag in n.attrs]:
                for a in [e] + list(e.descendants()):
                    href = a.attrs.get('href', '') if a.tag == 'a' else ''
                    if host in href:
                        jobs.append((name, crit, what, lookup, href, ' '.join(a.all_text().split())))
    seen = set()
    for name, crit, what, lookup, href, text in jobs:
        if (href, text) in seen: continue
        seen.add((href, text))
        state, titles = lookup(href)
        if state == 'not-dataset':
            add('FAIL', crit, f'{href} is not a dataset page; the open-data tag needs a link to a specific dataset',
                'link to https://data.gov.my/data-catalogue/<dataset-id>, with the dataset title as the link text', name)
        elif state == 'missing':
            add('FAIL', crit, f'{href} does not exist ({what} not found)', f'link to a real {"dataset on data.gov.my" if "Datasets" in crit else "app page on GAMMA"}', name)
        elif state == 'unreachable':
            add('WARN', crit, f'could not open {href} to compare the {what}; try again later', None, name)
        elif norm_title(text) in {norm_title(t) for t in titles}:
            add('PASS', crit, f'link text "{text}" matches the {what} on {urllib.parse.urlparse(href).netloc}', None, name)
        else:
            add('FAIL', crit, f'link text "{text}" does not match the {what}: ' + ' / '.join(f'"{t}"' for t in titles),
                f'use the exact {what} as the link text: {titles[0]}', name)


def check_links(pages_trees, add, is_url, scope, max_links):
    import concurrent.futures as cf
    seen, order = {}, []
    for name, tree, url in pages_trees:
        for u, text in link_targets(tree, url, is_url, scope):
            if u not in seen:
                seen[u] = (name, text); order.append(u)
    skipped = max(0, len(order) - max_links); order = order[:max_links]
    with cf.ThreadPoolExecutor(4) as ex:
        states = dict(zip(order, ex.map(check_link, order)))
    for u in [u for u in order if states[u][0] == 'unreachable']:   # second chance, one at a time
        time.sleep(1); states[u] = check_link(u)
    shown = lambda u: u.replace(chr(92), '/')
    broken = [u for u in order if states[u][0] == 'broken']
    for u in broken:
        page, text = seen[u]
        add('FAIL', 'Active Link', f'broken link {shown(u)} ({states[u][1]})' + (f', link text "{text}"' if text else ''),
            'fix the link or remove it; if the page moved, redirect the old URL to the new one', page)
    for u in order:
        if states[u][0] == 'unreachable':
            add('WARN', 'Active Link', f'could not check {shown(u)} ({states[u][1]}); try again later', None, seen[u][0])
    scope_txt = 'same site' if scope != 'all' else 'including external'
    unchecked = sum(1 for u in order if states[u][0] == 'unreachable')
    add('PASS' if not broken and not unchecked else 'INFO', 'Active Link', f'{len(order)} unique link(s) tried ({scope_txt}): {len(broken)} broken, {unchecked} could not be checked'
        + (f'; {skipped} more not checked (--max-links)' if skipped else ''))


MASTHEAD_TOGGLE = ('Kenal pasti begini', "Here's how you know", 'Here&#x27;s how you know', 'Here&#39;s how you know')


def myds_checks(tree, html, add, page):
    import html as _html
    """--myds: official masthead, Poppins/Inter, light mode by default (MYDS, not scored by SPLaSK)."""
    nodes = tree.nodes
    text_nodes = [n for n in nodes if n.text and any(m in ' '.join(n.text) for m in MASTHEAD)]
    if not text_nodes:
        add('WARN', 'MYDS: masthead', 'no official masthead ("Portal Rasmi Kerajaan Malaysia" / "Official Malaysia Government Website") in the server HTML',
            'add the masthead above the site header (guide: masthead-html)', page)
    else:
        first_h1 = next((i for i, n in enumerate(nodes) if n.tag == 'h1'), None)
        pos = nodes.index(text_nodes[0])
        if first_h1 is not None and pos > first_h1:
            add('WARN', 'MYDS: masthead', 'the masthead comes after the page heading; MYDS puts it at the very top, above the site header',
                'move the masthead markup to the start of <body>', page)
        elif not any(t in _html.unescape(html) for t in MASTHEAD_TOGGLE):
            add('WARN', 'MYDS: masthead', 'masthead found, but without its "Kenal pasti begini" / "Here\'s how you know" toggle',
                'add the toggle that explains .gov.my and HTTPS (guide: masthead-html)', page)
        else:
            add('PASS', 'MYDS: masthead', 'official masthead wording and toggle, above the page heading', None, page)
    css = ' '.join(n.attrs.get('href', '') for n in nodes if n.tag == 'link') + ' ' + ' '.join(
        re.findall(r'<style\b[^>]*>(.*?)</style>', html, re.S | re.I)) + ' ' + ' '.join(n.attrs.get('style', '') for n in nodes)
    fams = set(re.findall(r'family=([A-Za-z+]+)', css))
    other = sorted(f.replace('+', ' ') for f in fams if f.lower() not in ('poppins', 'inter'))
    has = {f for f in ('Poppins', 'Inter') if re.search(f, css, re.I)} | ({'Poppins', 'Inter'} if 'myds-style' in css else set())
    if has >= {'Poppins', 'Inter'}:
        add('PASS', 'MYDS: fonts', 'Poppins and Inter (or the MYDS stylesheet) are loaded', None, page)
    elif other:
        add('WARN', 'MYDS: fonts', f'loads {", ".join(other)} instead of Poppins (headings) and Inter (body)',
            'MYDS uses Poppins and Inter; if the agency has its own brand fonts, this is a conflict to raise, not to decide silently', page)
    else:
        add('INFO', 'MYDS: fonts', 'Poppins/Inter not seen in the server HTML; they may be loaded by an external stylesheet', None, page)
    html_node = next((n for n in nodes if n.tag == 'html'), None)
    dark = html_node is not None and ('dark' in html_node.attrs.get('class', '').split() or html_node.attrs.get('data-theme', '') == 'dark')
    add('WARN' if dark else 'PASS', 'MYDS: colour mode', '<html> starts in dark mode' if dark else 'light mode by default',
        'start in light mode; offer dark mode as a user choice' if dark else None, page)


def a11y_checks(tree, add, page, is_home):
    """--a11y: basic checks the server HTML can show (not a full WCAG audit)."""
    nodes = tree.nodes
    ids = [n.attrs['id'] for n in nodes if n.attrs.get('id')]
    labelled = {n.attrs.get('for') for n in nodes if n.tag == 'label'}
    named = lambda n: n.attrs.get('aria-label') or n.attrs.get('aria-labelledby') or n.attrs.get('title')
    unl = []
    for n in nodes:
        if n.tag in ('input', 'select', 'textarea'):
            if n.tag == 'input' and n.attrs.get('type', 'text').lower() in ('hidden', 'submit', 'button', 'reset', 'image'):
                continue
            if (n.attrs.get('id') in labelled) or any(a.tag == 'label' for a in n.ancestors()) or named(n):
                continue
            unl.append(n.attrs.get('name') or n.attrs.get('id') or n.tag)
    add('WARN' if unl else 'PASS', 'Accessibility: form labels',
        f'{len(unl)} form field(s) without a label (first: {unl[0]})' if unl else 'every form field has a label',
        '<label for="id">…</label> for each field (a placeholder is not a label)' if unl else None, page)
    def has_name(n):
        return n.all_text() or named(n) or any(d.tag == 'img' and d.attrs.get('alt') for d in n.descendants()) \
            or any(d.tag in ('svg',) and (d.attrs.get('aria-label') or any(t.tag == 'title' for t in d.descendants())) for d in n.descendants())
    empty = [n for n in nodes if (n.tag == 'button' or (n.tag == 'a' and n.attrs.get('href'))) and not has_name(n)]
    if empty:
        e = empty[0]
        add('WARN', 'Accessibility: names', f'{len(empty)} link(s)/button(s) with no text a screen reader can read (first: <{e.tag}> {e.attrs.get("href", "")[:40]})',
            'add visible text, or aria-label="…" on icon-only links and buttons', page)
    levels = [int(n.tag[1]) for n in nodes if re.fullmatch(r'h[1-6]', n.tag)]
    jump = next(((a, b) for a, b in zip(levels, levels[1:]) if b > a + 1), None)
    if jump:
        add('WARN', 'Accessibility: headings', f'heading level jumps from h{jump[0]} to h{jump[1]}', f'use h{jump[0] + 1} (style it with CSS if it should look smaller)', page)
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        add('WARN', 'Accessibility: duplicate ids', f'duplicate id(s): {", ".join(dup[:5])}', 'make each id unique (labels and aria references depend on them)', page)
    if is_home:
        first = [n for n in nodes if n.tag == 'a' and n.attrs.get('href')][:3]
        skip = any(n.attrs['href'].startswith('#') and re.search(r'skip|langkau|terus ke', n.all_text(), re.I) for n in first)
        add('PASS' if skip else 'WARN', 'Accessibility: skip link', 'skip link at the start of the page' if skip else 'no "skip to main content" link at the start of the page',
            None if skip else '<a class="skip-link" href="#kandungan">Langkau ke kandungan utama</a> as the first link, with <main id="kandungan">', page)


def scan_site(home, pages=None, today=None, max_pages=15, links=None, max_links=150, due_within=None, myds=False, a11y=False, render=False):
    """pages: None (home only) | 'all' | list of names, numbers (1-based, from discover order) or URLs/paths."""
    today = today or dt.datetime.now()
    results = []
    def add(level, crit, msg, fix=None, page='home'):
        results.append({'level': level, 'criterion': crit, 'message': msg, 'fix': fix, 'page': page})

    html, final, hops, secs = load(home)
    is_url = bool(re.match(r'https?://', home))
    due = []
    home_tree, home_tags = check_page(html, final, True, today, add, 'home', hops, secs, is_url, bool(links), due)
    trees = [('home', home_tree, final)]
    if myds: myds_checks(home_tree, html, add, 'home')
    if a11y: a11y_checks(home_tree, add, 'home', True)
    found = discover(html, final)
    chosen = []
    if pages:
        names = list(found)
        items = names if pages == 'all' else [p.strip() for p in pages.split(',') if p.strip()]
        for it in items:
            if it.isdigit() and 1 <= int(it) <= len(names): chosen.append((names[int(it) - 1], found[names[int(it) - 1]]))
            elif it in found: chosen.append((it, found[it]))
            elif re.match(r'https?://', it) or it.startswith('/') or os.path.exists(it) or '.' in it:
                same = [n for n, u in found.items() if os.path.normcase(os.path.normpath(u)) == os.path.normcase(os.path.normpath(it))
                        or (is_url and u.rstrip('/') == urllib.parse.urljoin(final, it).rstrip('/'))]
                chosen.append((same[0] if same else (it.rstrip('/').split('/')[-1] or it), it))
            else: add('WARN', 'Page choice', f'page "{it}" was not found on the home page (run --list-pages to see the options)')
        chosen = chosen[:max_pages]

    scanned = [{'name': 'home', 'url': final}]
    tags_by_page = {'home': home_tags}
    for name, target in chosen:
        try:
            phtml, pfinal, _, _ = load(target, final)
        except Exception as e:
            add('WARN', 'Page fetch', f'could not open {target}: {e.__class__.__name__}', page=name); continue
        start = len(results)
        ptree, ptags = check_page(phtml, pfinal, False, today, add, name, due=due)
        trees.append((name, ptree, pfinal))
        if a11y: a11y_checks(ptree, add, name, False)
        # shared header/footer: drop findings that repeat the home page word for word
        home_seen = {(x['level'], x['criterion'], x['message']) for x in results[:start] if x['page'] == 'home'}
        results[start:] = [x for x in results[start:] if (x['level'], x['criterion'], x['message']) not in home_seen]
        scanned.append({'name': name, 'url': pfinal if is_url else pfinal.replace(chr(92), '/')}); tags_by_page[name] = ptags

    # a tag missing on the home page but present on a scanned page -> SPLaSK only sees it via a Criteria URL
    criteria_urls = []
    for r in results:
        if r['page'] == 'home' and r['level'] == 'FAIL' and r['message'].startswith('no `splwpk-'):
            tag = re.search(r'`(splwpk-[a-z0-9-]+)`', r['message']).group(1)
            crit = TAGS[tag][0]
            bad_pages = {x['page'] for x in results if x['level'] == 'FAIL' and x['criterion'] == crit and x['page'] != 'home'}
            where = [p for p, tg in tags_by_page.items() if p != 'home' and tag in tg and p not in bad_pages]
            if where:
                url = next(s['url'] for s in scanned if s['name'] == where[0])
                r['level'] = 'WARN'
                r['message'] = f'`{tag}` is not on the home page but is on "{where[0]}" ({url})'
                r['fix'] = f'register {url} as a Criteria URL for this tag in the SPLaSK site profile, or also tag it on the home page'
                criteria_urls.append({'tag': tag, 'criterion': TAGS[tag][0], 'url': url})
    if render:
        import splask_render
        def _tags(h):
            t = Tree(); t.feed(h); return tags_of(t.nodes)
        for name, tree_, url in trees:
            try:
                splask_render.compare(tags_of(tree_.nodes), splask_render.rendered_html(url if name != 'home' else home), _tags, add, name)
            except RuntimeError as e:
                add('WARN', 'Rendering', f'--render skipped: {e}', None, name); break
    if links:
        check_links(trees, add, is_url, links, max_links)
        check_targets(trees, add)
    seen_due, due_list = set(), []
    for d in sorted(due, key=lambda d: (d['due'], d['page'] != 'home')):
        if (d['tag'], d['last_update']) not in seen_due:
            seen_due.add((d['tag'], d['last_update'])); due_list.append(d)
            if due_within is not None and 0 <= d['days_left'] <= due_within:
                add('WARN', d['criterion'], f"goes stale on {d['due']} ({d['days_left']} days): last updated {d['last_update']}, limit {d['limit_days']} days",
                    'update the content itself before that date (its timestamp then follows the real change)', d['page'])
    return {'target': home, 'final_url': final, 'redirects': len(hops), 'pages': scanned, 'discovered': found, 'results': results,
            'due': due_list, 'criteria_urls': criteria_urls}


def scan(target, follow=False, today=None):
    """Backward-compatible single-page scan (follow=True also checks the privacy page)."""
    return scan_site(target, 'privacy' if follow else None, today)


ORDER = {'FAIL': 0, 'WARN': 1, 'INFO': 2, 'PASS': 3}


def counts(r):
    return {k: sum(1 for x in r['results'] if x['level'] == k) for k in ORDER}


EN = {
    'title': 'SPLaSK 2.0 pre-check',
    'final': 'final URL {url}; unofficial, the SPLaSK assessment is the authority',
    'pages': 'Pages scanned', 'fix': 'fix',
    'due_head': 'Freshness due dates (each item fails on its due date unless the content itself is updated):',
    'due_row': '  {crit:38} last update {last}   due {due}   {left}',
    'overdue': 'OVERDUE', 'today': 'due today', 'in_days': 'in {n} days',
    'crit_head': 'Register these pages as Criteria URLs in the SPLaSK site profile:',
    'totals': '{FAIL} FAIL, {WARN} WARN, {PASS} PASS, {INFO} INFO',
    'md_title': 'SPLaSK 2.0 pre-check', 'md_totals': '**{FAIL} fail** · {WARN} warn · {PASS} pass · {INFO} info',
    'md_pages': 'Pages', 'md_cols': '| | Criterion | Page | Finding | Suggested fix |',
    'md_due': '### Freshness due dates', 'md_due_cols': '| Item | Last update | Due | |',
    'md_crit': '### Criteria URLs to register in the SPLaSK site profile', 'md_crit_cols': '| Tag | Page |',
    'md_pass': '{n} passing checks', 'md_foot': '_Unofficial pre-check; the SPLaSK assessment is the authority._',
    'md_days': '{n} days', 'md_overdue': '❌ overdue', 'md_today': '⚠️ today',
}


def _localise(r, lang):
    """(labels, results, due) for the report language; findings are translated only for display."""
    if lang != 'ms':
        return EN, r['results'], r.get('due') or [], (lambda lv: lv)
    import splask_i18n as t
    due = [dict(d, criterion=t.CRITERIA.get(d['criterion'], d['criterion'])) for d in r.get('due') or []]
    return t.LABELS, [t.translate_result(x) for x in r['results']], due, (lambda lv: t.LEVEL.get(lv, lv))


def report(r, lang='en'):
    L, res, due, lvl = _localise(r, lang)
    rs = sorted(res, key=lambda x: (ORDER[x['level']], x['page'] != 'home', x['page'], x['criterion']))
    print(f"{L['title']}: {r['target']}\n(" + L['final'].format(url=r['final_url']) + ')')
    print(L['pages'] + ': ' + ', '.join(f"{p['name']} ({p['url']})" for p in r['pages']) + '\n')
    multi = len(r['pages']) > 1
    for x in rs:
        where = f"[{x['page']}] " if multi and x['page'] != 'home' else ''
        print(f"{lvl(x['level']):6} {x['criterion']:38} {where}{x['message']}")
        if x.get('fix') and x['level'] in ('FAIL', 'WARN'):
            print(f"{'':45}-> {L['fix']}: {x['fix']}")
    if due:
        print('\n' + L['due_head'])
        for d in due:
            left = L['overdue'] if d['days_left'] < 0 else (L['today'] if d['days_left'] == 0 else L['in_days'].format(n=d['days_left']))
            print(L['due_row'].format(crit=d['criterion'], last=d['last_update'], due=d['due'], left=left))
    if r.get('criteria_urls'):
        print('\n' + L['crit_head'])
        for c_ in r['criteria_urls']:
            print(f"  {c_['tag']:32} {c_['url']}")
    print('\n' + L['totals'].format(**counts(r)))


def report_md(r, lang='en'):
    L, res, due, _ = _localise(r, lang)
    c = counts(r)
    icon = {'FAIL': '❌', 'WARN': '⚠️', 'INFO': 'ℹ️', 'PASS': '✅'}
    out = [f"## {L['md_title']}: `{r['final_url']}`", '', L['md_totals'].format(**c) + '  ',
           L['md_pages'] + ': ' + ', '.join(f"`{p['name']}`" for p in r['pages']), '',
           L['md_cols'], '|---|---|---|---|---|']
    esc = lambda s: (s or '').replace('|', '\\|').replace('\n', ' ')
    for x in sorted(res, key=lambda x: (ORDER[x['level']], x['page'] != 'home', x['criterion'])):
        if x['level'] == 'PASS': continue
        out.append(f"| {icon[x['level']]} | {esc(x['criterion'])} | {esc(x['page'])} | {esc(x['message'])} | {('`' + esc(x['fix']) + '`') if x.get('fix') else ''} |")
    if due:
        out += ['', L['md_due'], '', L['md_due_cols'], '|---|---|---|---|']
        for d in due:
            n = d['days_left']
            left = L['md_overdue'] if n < 0 else (L['md_today'] if n == 0 else ('⚠️ ' if n <= 7 else '') + L['md_days'].format(n=n))
            out.append(f"| {esc(d['criterion'])} | {d['last_update']} | {d['due']} | {left} |")
    if r.get('criteria_urls'):
        out += ['', L['md_crit'], '', L['md_crit_cols'], '|---|---|']
        out += [f"| `{c_['tag']}` | {esc(c_['url'])} |" for c_ in r['criteria_urls']]
    out += ['', f"<details><summary>{L['md_pass'].format(n=c['PASS'])}</summary>", '']
    out += [f"- {esc(x['criterion'])} ({x['page']}): {esc(x['message'])}" for x in res if x['level'] == 'PASS']
    out += ['', '</details>', '', L['md_foot']]
    print('\n'.join(out))


def list_pages(home):
    html, final, _, _ = load(home)
    found = discover(html, final)
    print(f'Pages linked from {final} that a SPLaSK review can include:\n')
    if not found: print('  (none found; pass page URLs to --pages directly)')
    for i, (name, url) in enumerate(found.items(), 1):
        print(f'  {i:2}. {name:16} {url.replace(chr(92), "/")}')
    print('\nScan them with --pages all, by number (--pages 1,3), by name (--pages privacy,sitemap) or by URL.')
    return found


def main(argv=None):
    try: sys.stdout.reconfigure(encoding='utf-8')
    except Exception: pass
    ap = argparse.ArgumentParser(description='SPLaSK 2.0 + MYDS pre-check (unofficial)')
    ap.add_argument('target', help='home page URL or local HTML file')
    ap.add_argument('--pages', default='', help="extra pages: 'all', numbers, names or URLs (comma-separated)")
    ap.add_argument('--list-pages', action='store_true', help='list the pages that can be scanned, then exit')
    ap.add_argument('--follow', action='store_true', help='shortcut for --pages privacy')
    ap.add_argument('--max-pages', type=int, default=15)
    ap.add_argument('--check-links', nargs='?', const='site', choices=['site', 'all'], default=None,
                    help='check every link on the scanned pages for the Active Link criterion (site = same site, the default; all = external too), '
                         'and compare data.gov.my dataset titles and GAMMA app names with the tagged link text')
    ap.add_argument('--max-links', type=int, default=150)
    ap.add_argument('--lang', choices=['en', 'ms'], default='en', help='report language: en (default) or ms (Bahasa Melayu)')
    ap.add_argument('--fix', action='store_true', help='write <page>.fixed.html with safe mechanical fixes (local .html files only)')
    ap.add_argument('--render', action='store_true', help='compare with the page after JavaScript runs (needs Playwright + Edge/Chrome)')
    ap.add_argument('--myds', action='store_true', help='also check the MYDS masthead, fonts and light mode (not scored by SPLaSK)')
    ap.add_argument('--a11y', action='store_true', help='also run basic accessibility checks (labels, names, headings, skip link)')
    ap.add_argument('--due-within', type=int, default=None, metavar='DAYS', help='WARN for timestamped items that go stale within DAYS days')
    ap.add_argument('--format', choices=['text', 'json', 'md'], default='text')
    ap.add_argument('--json', action='store_true', help='same as --format json')
    ap.add_argument('--fail-on', choices=['never', 'fail', 'warn'], default='never', help='exit code 1 on FAIL (or WARN)')
    ap.add_argument('--md-out', default='', help='also append the Markdown report to this file (e.g. $GITHUB_STEP_SUMMARY)')
    ap.add_argument('--today', default='')
    a = ap.parse_args(argv)
    if a.list_pages:
        list_pages(a.target); return 0
    today = dt.datetime.strptime(a.today, '%Y-%m-%d') if a.today else None
    pages = a.pages or ('privacy' if a.follow else None)
    r = scan_site(a.target, pages, today, a.max_pages, a.check_links, a.max_links, a.due_within, a.myds, a.a11y, a.render)
    fmt = 'json' if a.json else a.format
    if fmt == 'json': print(json.dumps(r, ensure_ascii=False, indent=1))
    elif fmt == 'md': report_md(r, a.lang)
    else: report(r, a.lang)
    if a.fix:
        import splask_fix
        for pg in r['pages']:
            path = pg['url'] if pg['name'] != 'home' else a.target
            if re.match(r'https?://', path) or not re.search(r'\.html?$', path, re.I) or not os.path.isfile(path):
                print(f"\n--fix: skipped {pg['name']} ({path}): only local .html files can be fixed; fix the template that produces it"); continue
            src = open(path, encoding='utf-8', errors='replace').read()
            out, changes = splask_fix.fix_html(src, set(TAGS))
            if not changes:
                print(f"\n--fix: {path}: nothing to fix automatically"); continue
            dest = re.sub(r'(\.html?)$', r'.fixed\1', path, flags=re.I)
            with open(dest, 'w', encoding='utf-8', newline='') as f: f.write(out)
            print(f"\n--fix: wrote {dest} ({len(changes)} change(s); dates, text and links other than MyGov are never changed):")
            for c_ in changes: print('  - ' + c_)
    if a.md_out:
        import contextlib, io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): report_md(r, a.lang)
        with open(a.md_out, 'a', encoding='utf-8') as f: f.write(buf.getvalue() + '\n')
    c = counts(r)
    return 1 if (a.fail_on == 'fail' and c['FAIL']) or (a.fail_on == 'warn' and (c['FAIL'] or c['WARN'])) else 0


if __name__ == '__main__':
    sys.exit(main())
