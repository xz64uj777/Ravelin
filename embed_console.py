#!/usr/bin/env python3
import base64
import gzip
import pathlib
import urllib.request

root = pathlib.Path(".")
assets = pathlib.Path("app/src/main/assets/index.html")
assets.parent.mkdir(parents=True, exist_ok=True)
pin = "https://raw.githubusercontent.com/xz64uj777/Ravelin/14c3db84d0eac95b8acc21d3a334158bd1fadcd7/"
raw = None

try:
    parts = sorted(root.glob("Ravelin.html.gz.b64.*"))
    if parts:
        blob = "".join(p.read_text().replace("\n", "").replace(" ", "") for p in parts)
        raw = gzip.decompress(base64.b64decode(blob))
        print("decoded local parts", len(raw))
except Exception as exc:
    print("local gzip failed", exc)
    raw = None

if raw is None:
    blob = ""
    for i in range(3):
        url = pin + "Ravelin.html.gz.b64." + str(i)
        print("fetch", url)
        blob += urllib.request.urlopen(url).read().decode("ascii").replace("\n", "").replace(" ", "")
    raw = gzip.decompress(base64.b64decode(blob))
    print("decoded pinned parts", len(raw))

text = raw.decode("utf-8", errors="replace")
text = text.replace("window.RAVELIN_BUILD='v40'", "window.RAVELIN_BUILD='v41'")
text = text.replace("const RAVELIN_VERSION='40'", "const RAVELIN_VERSION='41'")
text = text.replace("RAVELIN-KYLE-2026-V40", "RAVELIN-KYLE-2026-V41")
text = text.replace(">v40</strong>", ">v41</strong>")
old = (
    "if(window.RavelinNative && RavelinNative.reloadLive){\n"
    "      try{ RavelinNative.reloadLive(url); return; }catch(e){}\n"
    "    }"
)
if old in text:
    text = text.replace(old, "/* v41: persist path uses applyHtml */", 1)
    print("disabled reloadLive shortcut")

hook = """<script>
window.fetchConsoleHtml = window.fetchConsoleHtml || (async function(){
  var BASE='https://raw.githubusercontent.com/xz64uj777/Ravelin/14c3db84d0eac95b8acc21d3a334158bd1fadcd7/';
  var names=['Ravelin.html.gz.b64.0','Ravelin.html.gz.b64.1','Ravelin.html.gz.b64.2'];
  var texts=await Promise.all(names.map(function(p){
    return fetch(BASE+p+'?t='+Date.now(),{cache:'no-store'}).then(function(r){
      if(!r.ok) throw new Error(p);
      return r.text();
    });
  }));
  var clean=texts.join('').replace(/\\s/g,'');
  var bin=atob(clean);
  var bytes=new Uint8Array(bin.length);
  for(var i=0;i<bin.length;i++) bytes[i]=bin.charCodeAt(i);
  var ds=new DecompressionStream('gzip');
  var stream=new Blob([bytes]).stream().pipeThrough(ds);
  var html=await new Response(stream).text();
  if(html.length<20000) throw new Error('short');
  return html;
});
</script>
"""
if "</body>" in text:
    text = text.replace("</body>", hook + "</body>", 1)

assets.write_bytes(text.encode("utf-8"))
print("wrote", assets, assets.stat().st_size)
