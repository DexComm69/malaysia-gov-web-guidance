#!/usr/bin/env python3
"""Keep references/myds-index.json in step with the MYDS documentation site.

  python mgwg.py update-index                 report new, removed and renamed MYDS pages (writes nothing)
  python mgwg.py update-index --write         update the index: add new pages, drop pages that are gone, fix titles
  python mgwg.py update-index --refresh --write
                                              also re-read every page's title, BM title, section headings and stub status
  python mgwg.py update-index --fail-on-change
                                              exit code 1 if anything changed (for a scheduled CI job)

The page list comes from the documentation's own side navigation (design.digital.gov.my has no
usable sitemap). A page is only dropped when its URL really returns 404; a page that is merely
missing from the navigation is reported, not removed. Fresh fetches only (the 7-day cache is not
used). Standard library only. Unofficial.
"""
import argparse, datetime as dt, json, os, re, sys, time, urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from splask_scan import Tree  # noqa: E402  (same HTML tree parser as the scanner)

BASE = 'https://design.digital.gov.my'
INDEX = os.path.join(os.path.dirname(HERE), 'references', 'myds-index.json')
UA = 'mgwg-update-index/1.0 (unofficial Malaysian gov web guidance skill)'
SECTIONS = ('design', 'develop')
LINK = re.compile(r'^/en/docs/(design|develop)/([a-z0-9][a-z0-9-]*)$')


def get(url, attempts=3):
    """-> (status, html). 0 = no response after retries. Replaceable in tests."""
    for n in range(attempts):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=30)
            return r.status, r.read().decode(r.headers.get_content_charset() or 'utf-8', 'replace')
        except urllib.error.HTTPError as e:
            return e.code, ''
        except Exception:
            if n < attempts - 1: time.sleep(2 * (n + 1))
    return 0, ''


def text(n):
    return ' '.join(n.all_text().split())


def nav():
    """Pages listed in the docs navigation, in order: [(id, path, link text)]."""
    seen, out = set(), []
    for sec in SECTIONS:
        st, html = get(f'{BASE}/en/docs/{sec}')
        if st != 200:
            raise SystemExit(f'could not read the MYDS navigation at {BASE}/en/docs/{sec} (HTTP {st or "no response"}); try again later')
        t = Tree(); t.feed(html)
        if f'/en/docs/{sec}' not in seen:   # the section's own landing page
            seen.add(f'/en/docs/{sec}'); out.append((f'{sec}-intro', f'/en/docs/{sec}', ''))
        for a in t.nodes:
            m = LINK.match(a.attrs.get('href', '')) if a.tag == 'a' else None
            if m and a.attrs['href'] not in seen:
                seen.add(a.attrs['href'])
                out.append((f'{m.group(1)}-{m.group(2)}', a.attrs['href'], text(a)))
    return out


def page_meta(path):
    """Title, BM title, section headings and status of one page, from its <article>."""
    meta = {}
    for lang in ('en', 'ms'):
        st, html = get(BASE + path.replace('/en/', f'/{lang}/', 1))
        if st != 200:
            if lang == 'en': return None
            continue
        t = Tree(); t.feed(html)
        art = next((n for n in t.nodes if n.tag == 'article'), None)
        scope = list(art.descendants()) if art else t.nodes
        h1 = next((text(n) for n in scope if n.tag == 'h1'), '')
        if lang == 'en':
            meta['title'] = h1
            meta['sections'] = list(dict.fromkeys(text(n) for n in scope if n.tag in ('h2', 'h3') and text(n)))  # repeated headings once
            meta['status'] = 'stub' if (not meta['sections'] or meta['sections'] == ['Work In Progress']
                                        or any(x.lower().startswith('work in progress') for x in meta['sections'][:1])) else 'current'
        else:
            meta['title_ms'] = h1
    meta.setdefault('title_ms', meta.get('title', ''))
    return meta


def guess_category(pid, order, by_id):
    """Category of the nearest known neighbour in the navigation (pages are grouped by kind there)."""
    i = order.index(pid)
    for j in sorted(range(len(order)), key=lambda k: (abs(k - i), k)):
        if order[j] != pid and order[j] in by_id and order[j].split('-')[0] == pid.split('-')[0]:
            return by_id[order[j]]['category']
    return 'myds-component-design' if pid.startswith('design-') else 'myds-component-react'


def run(write=False, refresh=False, index_path=INDEX, today=None):
    data = json.load(open(index_path, encoding='utf8'))
    pages = data['pages']
    by_id = {p['id']: p for p in pages}
    listed = nav()
    order = [pid for pid, _, _ in listed]
    path_of = {pid: path for pid, path, _ in listed}
    nav_text = {pid: t for pid, _, t in listed}
    report = {'new': [], 'removed': [], 'unlisted': [], 'renamed': [], 'refreshed': []}

    for pid in order:
        if pid in by_id:
            old, new = by_id[pid]['title'], nav_text[pid]
            if new and ' '.join(old.split()) != new:
                report['renamed'].append((pid, old, new))
        else:
            report['new'].append(pid)
    for pid, p in by_id.items():
        if pid in path_of: continue
        st, _ = get(p['url_en'])
        (report['removed'] if st == 404 else report['unlisted']).append((pid, st))

    if write:
        removed = {pid for pid, _ in report['removed']}
        pages = [p for p in pages if p['id'] not in removed]
        by_id = {p['id']: p for p in pages}
        for pid, old, new in report['renamed']:
            by_id[pid]['title'] = new
        for pid in report['new']:
            meta = page_meta(path_of[pid])
            if not meta: continue
            entry = {'id': pid, 'category': guess_category(pid, order, by_id), 'title': meta['title'] or nav_text[pid],
                     'title_ms': meta['title_ms'], 'url_en': BASE + path_of[pid],
                     'url_ms': BASE + path_of[pid].replace('/en/', '/ms/', 1), 'status': meta['status'], 'sections': meta['sections']}
            pages.append(entry); by_id[pid] = entry
        if refresh:
            for p in pages:
                meta = page_meta(p['url_en'].replace(BASE, ''))
                if not meta: continue
                changed = {k: v for k, v in meta.items() if v and p.get(k) != v}
                if changed:
                    p.update(changed); report['refreshed'].append((p['id'], sorted(changed)))
        data['pages'] = pages
        data['retrieved'] = (today or dt.date.today()).isoformat()
        with open(index_path, 'w', encoding='utf8', newline='\n') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=1))
    return report, len(order)


def show(report, n_nav, write, index_path=INDEX):
    print(f'MYDS navigation lists {n_nav} pages.')
    rows = [('New pages', [f'{p}' for p in report['new']]),
            ('Renamed', [f'{p}: "{o}" -> "{n}"' for p, o, n in report['renamed']]),
            ('Gone (HTTP 404)', [f'{p}' for p, _ in report['removed']]),
            ('Not in the navigation but still online (kept)', [f'{p} (HTTP {st or "no response"})' for p, st in report['unlisted']]),
            ('Refreshed', [f'{p}: {", ".join(k)}' for p, k in report['refreshed']])]
    for label, items in rows:
        if items:
            print(f'\n{label} ({len(items)}):'); [print('  ' + x) for x in items]
    changes = sum(len(report[k]) for k in ('new', 'renamed', 'removed', 'refreshed'))
    if not changes and not report['unlisted']:
        print('\nThe index is up to date.')
    elif not write:
        print('\nNothing written. Run with --write to update references/myds-index.json.')
    else:
        try: shown = os.path.relpath(index_path)
        except ValueError: shown = index_path          # Windows: index on another drive
        print(f'\n{shown} updated. In the offline edition, new pages are read live until its bundled copies are rebuilt.')
    return changes


def main(argv=None):
    try: sys.stdout.reconfigure(encoding='utf-8')
    except Exception: pass
    ap = argparse.ArgumentParser(description='Check references/myds-index.json against the MYDS documentation site')
    ap.add_argument('--write', action='store_true', help='update the index (default: report only)')
    ap.add_argument('--refresh', action='store_true', help='with --write: also re-read every page (about 230 requests)')
    ap.add_argument('--fail-on-change', action='store_true', help='exit code 1 if the index is out of date')
    ap.add_argument('--index', default=INDEX, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    report, n = run(a.write, a.refresh and a.write, a.index)
    changes = show(report, n, a.write, a.index)
    return 1 if a.fail_on_change and changes else 0


if __name__ == '__main__':
    sys.exit(main())
