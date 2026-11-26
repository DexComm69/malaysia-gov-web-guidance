"""`scan --render`: compare the server HTML with the page after JavaScript runs (optional; needs Playwright).

Tags that appear only after rendering were added by JavaScript, so the SPLaSK crawler (which does not run
JavaScript) never sees them. Uses Playwright's own Chromium if installed, else the system Edge or Chrome.
"""
import re


def rendered_html(target):
    """-> rendered HTML, or raises RuntimeError with an install hint."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise RuntimeError('Playwright is not installed: pip install playwright (then it uses Edge/Chrome, or run: playwright install chromium)')
    import os, pathlib
    url = target if re.match(r'https?://', target) else pathlib.Path(os.path.abspath(target)).as_uri()
    last = None
    with sync_playwright() as p:
        for kw in ({}, {'channel': 'msedge'}, {'channel': 'chrome'}):
            try:
                b = p.chromium.launch(**kw)
            except Exception as e:
                last = e; continue
            try:
                pg = b.new_page()
                pg.goto(url, wait_until='networkidle', timeout=45000)
                return pg.content()
            finally:
                b.close()
    raise RuntimeError(f'no browser available for --render ({str(last).splitlines()[0][:120] if last else "unknown"})')


def compare(server_tags, rendered, tags_of_html, add, page):
    """Report tags present only after JavaScript ran."""
    only_js = sorted(set(tags_of_html(rendered)) - set(server_tags))
    if only_js:
        add('FAIL', 'Rendering', f'tags that exist only after JavaScript runs (the crawler never sees them): {", ".join(only_js[:8])}',
            'print these attributes in the server HTML (template code), not with JavaScript', page)
    else:
        add('PASS', 'Rendering', 'the rendered page adds no tags that the server HTML lacks', None, page)
