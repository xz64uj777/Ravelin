#!/usr/bin/env python3
import base64, gzip, pathlib, urllib.request
root = pathlib.Path('.')
assets = pathlib.Path('app/src/main/assets/index.html')
assets.parent.mkdir(parents=True, exist_ok=True)
src = pathlib.Path('Ravelin.html')

def is_full(text):
    return text and len(text) > 20000 and 'RAVELIN-KYLE' in text and 'class="tab"' in text

text = None
frags = sorted((root/'console').glob('part*.htmlfrag')) if (root/'console').exists() else []
if frags:
    text = ''.join(p.read_text(encoding='utf-8', errors='replace') for p in frags)
    print('joined fragments', len(frags), len(text or ''))
    if not is_full(text):
        text = None

if text is None and src.exists():
    candidate = src.read_text(encoding='utf-8', errors='replace')
    print('found Ravelin.html', len(candidate))
    if is_full(candidate):
        text = candidate

if text is None and assets.exists():
    candidate = assets.read_text(encoding='utf-8', errors='replace')
    print('found assets', len(candidate))
    if is_full(candidate):
        text = candidate

if text is None:
    raw = None
    try:
        parts = sorted(root.glob('Ravelin.html.gz.b64.*'))
        if parts:
            blob = ''.join(p.read_text().replace('\n','').replace(' ','') for p in parts)
            raw = gzip.decompress(base64.b64decode(blob))
            print('decoded local gzip', len(raw))
    except Exception as exc:
        print('local gzip failed', exc)
        raw = None
    if raw is None:
        pin = 'https://raw.githubusercontent.com/xz64uj777/Ravelin/14c3db84d0eac95b8acc21d3a334158bd1fadcd7/'
        blob = ''
        for i in range(3):
            url = pin + 'Ravelin.html.gz.b64.' + str(i)
            print('fetch', url)
            blob += urllib.request.urlopen(url).read().decode('ascii').replace('\n','').replace(' ','')
        raw = gzip.decompress(base64.b64decode(blob))
        print('decoded pinned gzip', len(raw))
    text = raw.decode('utf-8', errors='replace')

if not is_full(text):
    raise SystemExit('refusing to embed splash/loader (%s bytes)' % len(text or ''))

assets.write_text(text, encoding='utf-8')
src.write_text(text, encoding='utf-8')
print('wrote', assets, assets.stat().st_size)
