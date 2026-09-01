#!/usr/bin/env python3
"""Bake the full Ravelin console into app/src/main/assets/index.html.

Prefer a full Ravelin.html already in the repo. Never overwrite a full
console with a splash/loader stub.
"""
import base64
import gzip
import pathlib
import urllib.request

root = pathlib.Path(".")
assets = pathlib.Path("app/src/main/assets/index.html")
assets.parent.mkdir(parents=True, exist_ok=True)
src = pathlib.Path("Ravelin.html")


def is_full(text: str) -> bool:
    return len(text) > 20000 and "RAVELIN-KYLE" in text and "class=\"tab\"" in text


text = None
if src.exists():
    candidate = src.read_text(encoding="utf-8", errors="replace")
    print("found Ravelin.html", len(candidate))
    if is_full(candidate):
        text = candidate

if text is None and assets.exists():
    candidate = assets.read_text(encoding="utf-8", errors="replace")
    print("found existing assets", len(candidate))
    if is_full(candidate):
        text = candidate

if text is None:
    raw = None
    try:
        parts = sorted(root.glob("Ravelin.html.gz.b64.*"))
        if parts:
            blob = "".join(p.read_text().replace("\n", "").replace(" ", "") for p in parts)
            raw = gzip.decompress(base64.b64decode(blob))
            print("decoded local gzip parts", len(raw))
    except Exception as exc:
        print("local gzip failed", exc)
        raw = None
    if raw is None:
        pin = "https://raw.githubusercontent.com/xz64uj777/Ravelin/14c3db84d0eac95b8acc21d3a334158bd1fadcd7/"
        blob = ""
        for i in range(3):
            url = pin + "Ravelin.html.gz.b64." + str(i)
            print("fetch", url)
            blob += urllib.request.urlopen(url).read().decode("ascii").replace("\n", "").replace(" ", "")
        raw = gzip.decompress(base64.b64decode(blob))
        print("decoded pinned parts", len(raw))
    text = raw.decode("utf-8", errors="replace")

if not is_full(text):
    raise SystemExit("refusing to embed splash/loader (%s bytes)" % len(text))

assets.write_text(text, encoding="utf-8")
if not src.exists() or not is_full(src.read_text(encoding="utf-8", errors="replace")):
    src.write_text(text, encoding="utf-8")
print("wrote", assets, assets.stat().st_size)
