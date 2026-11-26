#!/usr/bin/env python3
"""Build the malaysia-gov-web-guidance skill from this repository (the single source).

  python tools/build.py                                   # public .skill -> dist/malaysia-gov-web-guidance.skill
  python tools/build.py --out my.skill --install DIR      # also install the built skill into DIR
  python tools/build.py --overlay PRIVATE_DIR ...         # a private edition: copy PRIVATE_DIR/files over the
                                                          # skill, then apply PRIVATE_DIR/patches.json
  python tools/build.py --check                           # only check that the build works (CI)

patches.json is a list of {"file", "find", "replace"}: exact text replacements. The build stops if a
"find" text is not found exactly once, so a private edition can never silently drift from this repo.
Tests, evals and caches are left out of the .skill file. Standard library only.
"""
import argparse, json, os, shutil, sys, tempfile, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = 'malaysia-gov-web-guidance'
SRC = os.path.join(ROOT, 'skills', NAME)
SKIP_DIRS = {'__pycache__', 'tests', 'evals', '.pytest_cache'}


def build(overlay=None):
    tmp = tempfile.mkdtemp(prefix='mgwg-build-')
    out = os.path.join(tmp, NAME)
    shutil.copytree(SRC, out, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    if overlay:
        files = os.path.join(overlay, 'files')
        if os.path.isdir(files):
            shutil.copytree(files, out, dirs_exist_ok=True)
        pf = os.path.join(overlay, 'patches.json')
        for p in (json.load(open(pf, encoding='utf8')) if os.path.exists(pf) else []):
            path = os.path.join(out, p['file'])
            text = open(path, encoding='utf8').read().replace('\r\n', '\n')
            n = text.count(p['find'])
            if n != 1:
                sys.exit(f"patch failed: {p['file']}: the text to replace was found {n} times (expected 1):\n  {p['find'][:120]}\n"
                         "The public file changed. Update patches.json in the overlay to match it.")
            open(path, 'w', encoding='utf8', newline='\n').write(text.replace(p['find'], p['replace']))
    return out


def zip_skill(folder, dest):
    os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)
    n = 0
    with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as z:
        for dp, dn, fn in os.walk(folder):
            dn[:] = sorted(d for d in dn if d not in SKIP_DIRS)
            for f in sorted(fn):
                if f.endswith('.pyc'): continue
                full = os.path.join(dp, f)
                z.write(full, NAME + '/' + os.path.relpath(full, folder).replace(os.sep, '/')); n += 1
    return n


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--overlay', help='private overlay folder (files/ + patches.json)')
    ap.add_argument('--out', default=os.path.join(ROOT, 'dist', NAME + '.skill'))
    ap.add_argument('--install', help='also install the built skill into this folder (replaced)')
    ap.add_argument('--check', action='store_true', help='build and validate only; write nothing')
    a = ap.parse_args(argv)
    folder = build(a.overlay)
    for need in ('SKILL.md', 'scripts/mgwg.py', 'scripts/splask_scan.py'):
        if not os.path.exists(os.path.join(folder, need)): sys.exit(f'missing {need}')
    head = open(os.path.join(folder, 'SKILL.md'), encoding='utf8').read(400)
    if not head.startswith('---') or f'name: {NAME}' not in head: sys.exit('SKILL.md frontmatter is missing or has the wrong name')
    if a.check:
        print(f'ok: build of {NAME} works' + (' (with overlay)' if a.overlay else '')); return 0
    n = zip_skill(folder, a.out)
    print(f'{a.out}: {n} files, {os.path.getsize(a.out):,} bytes')
    if a.install:
        dest = os.path.expanduser(a.install)
        if os.path.basename(os.path.normpath(dest)) != NAME: sys.exit(f'--install must end in /{NAME}')
        if os.path.exists(dest): shutil.rmtree(dest)
        shutil.copytree(folder, dest, ignore=shutil.ignore_patterns(*SKIP_DIRS - {'evals'}))
        print(f'installed into {dest}')
    shutil.rmtree(os.path.dirname(folder), ignore_errors=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
