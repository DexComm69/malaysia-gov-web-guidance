#!/usr/bin/env python3
"""Safe, mechanical SPLaSK fixes for static HTML files (used by `scan --fix`).

Only changes that need no judgement are made, and each one is listed:
  - misspelled official tag names (splwpk-sitemaps -> splwpk-sitemap) and values that don't repeat the name
  - a tag on an <i> icon moved to the link (<a>) or <form> around it
  - a search / advanced-search / feedback tag on a wrapper moved onto the single <form> inside it
  - the MyGov link set to exactly https://www.malaysia.gov.my
  - a missing viewport meta tag and a missing <html lang> (lang="ms") added

Never changed: timestamps and dates, link targets other than MyGov, page text, titles, descriptions,
alt text, commented-out markup, anything added by JavaScript. Those need real facts or a decision.
The original file is left alone; the result is written next to it as <name>.fixed.html.
"""
import difflib, re
from html.parser import HTMLParser

FORM_TAGS = {'splwpk-search-function', 'splwpk-advanced-search-function', 'splwpk-feedback-form'}
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())


class _El:
    __slots__ = ('tag', 'attrs', 'start', 'end', 'parent', 'children')

    def __init__(s, tag, attrs, start, end, parent):
        s.tag, s.attrs, s.start, s.end, s.parent, s.children = tag, attrs, start, end, parent, []

    def descendants(s):
        for c in s.children:
            yield c; yield from c.descendants()


class _Spans(HTMLParser):
    """Element tree with the exact source span of every start tag."""
    def __init__(s, src):
        super().__init__(convert_charrefs=True)
        s.src = src
        s.lines = [0]
        for m in re.finditer('\n', src): s.lines.append(m.end())
        s.root = _El('#root', [], 0, 0, None); s.cur = s.root; s.all = []

    def _pos(s):
        line, col = s.getpos()
        return s.lines[line - 1] + col

    def handle_starttag(s, tag, attrs):
        start = s._pos(); raw = s.get_starttag_text() or ''
        el = _El(tag, attrs, start, start + len(raw), s.cur)
        s.cur.children.append(el); s.all.append(el)
        if tag not in VOID: s.cur = el

    def handle_startendtag(s, tag, attrs):
        start = s._pos(); raw = s.get_starttag_text() or ''
        el = _El(tag, attrs, start, start + len(raw), s.cur)
        s.cur.children.append(el); s.all.append(el)

    def handle_endtag(s, tag):
        p = s.cur
        while p is not s.root and p.tag != tag: p = p.parent
        if p is not s.root: s.cur = p.parent


def _render(tag, attrs, selfclose):
    def one(k, v):
        if v is None: return k
        q = '"' if '"' not in v else "'"
        return f'{k}={q}{v}{q}'
    return '<' + ' '.join([tag] + [one(k, v) for k, v in attrs]) + (' />' if selfclose else '>')


def fix_html(src, official):
    """-> (new_src, [change descriptions])."""
    p = _Spans(src); p.feed(src); p.close()
    new_attrs = {id(e): list(e.attrs) for e in p.all}
    changes, inserts = [], []

    def get(e, k):
        return next((v for a, v in new_attrs[id(e)] if a == k), None)

    def set_attr(e, k, v):
        lst = new_attrs[id(e)]
        for i, (a, _) in enumerate(lst):
            if a == k: lst[i] = (k, v); return
        lst.append((k, v))

    def drop(e, k):
        new_attrs[id(e)] = [(a, v) for a, v in new_attrs[id(e)] if a != k]

    for e in p.all:
        for k, v in list(new_attrs[id(e)]):
            if not k.startswith('splwpk-') or k.endswith('-timestamp'): continue
            name = k
            if k not in official:
                close = difflib.get_close_matches(k, official, n=1, cutoff=0.8)
                if not close: continue
                name = close[0]
                lst = new_attrs[id(e)]
                lst[lst.index((k, v))] = (name, name)
                changes.append(f'<{e.tag}>: renamed {k} to {name}')
            elif v != k:
                set_attr(e, k, k); changes.append(f'<{e.tag}>: {k} value set to "{k}"')
    for e in p.all:
        tags = [k for k, _ in new_attrs[id(e)] if k in official]
        for k in tags:
            target = None
            if e.tag == 'i':
                anc = e.parent
                while anc is not None and anc.tag not in ('a', 'form', '#root'): anc = anc.parent
                want = 'form' if k in FORM_TAGS else 'a'
                if anc is not None and anc.tag == want: target = anc
                elif k in FORM_TAGS:
                    a = e.parent
                    while a is not None and a.tag not in ('form', '#root'): a = a.parent
                    target = a if a is not None and a.tag == 'form' else None
            elif k in FORM_TAGS and e.tag != 'form':
                forms = [d for d in e.descendants() if d.tag == 'form']
                if len(forms) == 1: target = forms[0]
            if target is not None and get(target, k) is None:
                ts = get(e, 'timestamp')
                drop(e, k); set_attr(target, k, k)
                if ts is not None and get(target, 'timestamp') is None and not any(x.startswith('splwpk-') for x, _ in new_attrs[id(e)]):
                    drop(e, 'timestamp'); set_attr(target, 'timestamp', ts)
                changes.append(f'moved {k} from <{e.tag}> to <{target.tag}>')
    for e in p.all:
        href = get(e, 'href') if e.tag == 'a' else None
        if href and re.match(r'https?://(www\.)?malaysia\.gov\.my(/[^#?]*)?/?$', href, re.I) \
                and not re.fullmatch(r'https://www\.malaysia\.gov\.my/?', href) and re.sub(r'https?://(www\.)?malaysia\.gov\.my', '', href, flags=re.I).strip('/') in ('', 'portal'):
            set_attr(e, 'href', 'https://www.malaysia.gov.my'); changes.append(f'MyGov link {href} -> https://www.malaysia.gov.my')
    html_el = next((e for e in p.all if e.tag == 'html'), None)
    if html_el is not None and not get(html_el, 'lang'):
        set_attr(html_el, 'lang', 'ms'); changes.append('added lang="ms" to <html>')
    if not any(e.tag == 'meta' and (get(e, 'name') or '').lower() == 'viewport' for e in p.all):
        head = next((e for e in p.all if e.tag == 'head'), None)
        if head is not None:
            charset = next((e for e in head.children if e.tag == 'meta' and get(e, 'charset') is not None), None)
            at = (charset or head).end
            inserts.append((at, '\n<meta name="viewport" content="width=device-width, initial-scale=1">'))
            changes.append('added <meta name="viewport" content="width=device-width, initial-scale=1">')

    edits = []
    for e in p.all:
        if new_attrs[id(e)] != list(e.attrs):
            raw = src[e.start:e.end]
            edits.append((e.start, e.end, _render(e.tag, new_attrs[id(e)], raw.rstrip().endswith('/>'))))
    edits += [(at, at, text) for at, text in inserts]
    out = src
    for a, b, text in sorted(edits, key=lambda x: (x[0], x[1]), reverse=True):
        out = out[:a] + text + out[b:]
    return out, changes
