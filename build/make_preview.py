#!/usr/bin/env python3
"""Build a self-contained, clickable preview of the Streamly4K site.

 * rewrites every absolute internal link to a relative one so the site works
   when served from a sub-path (Artifact hosting, a zip opened locally, etc.)
 * injects a floating "Palette lab" so colour schemes can be compared live
"""
import os, re, shutil, json

SRC = "/home/claude/streamly4k"
DST = "/home/claude/preview"

SKIP_TOP = {".git", "build", "__pycache__"}
SKIP_FILES = {"README.md", ".gitignore", ".vercelignore"}

# --------------------------------------------------------------------------
PALETTES = [
    {
        "id": "mint", "name": "Signal Mint", "note": "The original mint direction",
        "dark": {"brand": "#00E08A", "brand-2": "#17C8E8", "brand-3": "#7BF3C0", "on-brand": "#04120C",
                 "bg": "#06070A", "bg-2": "#0A0C11", "surface": "#0F1219", "surface-2": "#161A23",
                 "surface-3": "#1D222C", "accent": "#FFC24D"},
        "light": {"brand": "#00A868", "brand-2": "#0E9FC4", "brand-3": "#067A4C", "on-brand": "#FFFFFF"},
    },
    {
        "id": "azure", "name": "Azure Ice", "note": "Trust, premium, broadcast-blue",
        "dark": {"brand": "#2F80FF", "brand-2": "#22D3EE", "brand-3": "#A5C9FF", "on-brand": "#F4F9FF",
                 "bg": "#04070F", "bg-2": "#080C16", "surface": "#0D121E", "surface-2": "#141A28",
                 "surface-3": "#1C2434", "accent": "#FFC24D"},
        "light": {"brand": "#1D5FD8", "brand-2": "#0E9FC4", "brand-3": "#163F8F", "on-brand": "#FFFFFF"},
    },
    {
        "id": "ember", "name": "Sunset Ember", "note": "Current — your pick",
        "dark": {"brand": "#FF4D2E", "brand-2": "#FF9A3D", "brand-3": "#FFC7A8", "on-brand": "#FFF4F0",
                 "bg": "#080605", "bg-2": "#0D0A09", "surface": "#131010", "surface-2": "#1A1614",
                 "surface-3": "#241E1B", "accent": "#FFD66B"},
        "light": {"brand": "#D93A1B", "brand-2": "#E07A12", "brand-3": "#9E2A12", "on-brand": "#FFFFFF"},
    },
    {
        "id": "crimson", "name": "Crimson Sport", "note": "Match-day urgency",
        "dark": {"brand": "#FF2D55", "brand-2": "#FF6B4A", "brand-3": "#FFA8B8", "on-brand": "#FFF3F5",
                 "bg": "#080507", "bg-2": "#0C090B", "surface": "#120E11", "surface-2": "#191418",
                 "surface-3": "#231C21", "accent": "#FFC24D"},
        "light": {"brand": "#D81E43", "brand-2": "#E0543A", "brand-3": "#9C1630", "on-brand": "#FFFFFF"},
    },
    {
        "id": "royal", "name": "Royal Violet", "note": "Premium, entertainment-first",
        "dark": {"brand": "#7C5CFF", "brand-2": "#C77DFF", "brand-3": "#C9BCFF", "on-brand": "#FBF9FF",
                 "bg": "#07060D", "bg-2": "#0B0A14", "surface": "#11101C", "surface-2": "#181626",
                 "surface-3": "#221F33", "accent": "#FFC24D"},
        "light": {"brand": "#5B3FE0", "brand-2": "#9B4DD8", "brand-3": "#432BA8", "on-brand": "#FFFFFF"},
    },
    {
        "id": "gold", "name": "Solar Gold", "note": "Luxury / concierge positioning",
        "dark": {"brand": "#F5C451", "brand-2": "#E8A020", "brand-3": "#FFE6A8", "on-brand": "#1A1305",
                 "bg": "#070706", "bg-2": "#0B0B09", "surface": "#111110", "surface-2": "#191816",
                 "surface-3": "#232220", "accent": "#7BD8F5"},
        "light": {"brand": "#A87A0B", "brand-2": "#C8901A", "brand-3": "#7A5806", "on-brand": "#FFFFFF"},
    },
]


def css_for(p):
    d = p["dark"]
    dark = "".join(f"--{k}:{v};" for k, v in d.items())
    dark += f"--brand-grad:linear-gradient(104deg,{d['brand']} 0%,{d['brand-2']} 100%);"
    dark += f"--brand-grad-r:linear-gradient(104deg,{d['brand-2']} 0%,{d['brand']} 100%);"
    l = p["light"]
    light = "".join(f"--{k}:{v};" for k, v in l.items())
    light += f"--brand-grad:linear-gradient(104deg,{l['brand']} 0%,{l['brand-2']} 100%);"
    light += f"--brand-grad-r:linear-gradient(104deg,{l['brand-2']} 0%,{l['brand']} 100%);"
    return f":root{{{dark}}}:root[data-theme=\"light\"]{{{light}}}"


PALETTE_DATA = {p["id"]: {"name": p["name"], "note": p["note"],
                          "css": css_for(p), "sw": [p["dark"]["brand"], p["dark"]["brand-2"]]}
                for p in PALETTES}

APPLY = """<script>
(function(){var P=%s;window.__S4KP=P;
function apply(id){var p=P[id]||P.ember;var s=document.getElementById('s4k-palette');
if(!s){s=document.createElement('style');s.id='s4k-palette';document.head.appendChild(s);}
s.textContent=p.css;}
var id='ember';try{id=localStorage.getItem('s4k-pal2')||'ember';}catch(e){}
window.__S4KPID=id;apply(id);window.__s4kApply=apply;})();
</script>""" % json.dumps(PALETTE_DATA, separators=(",", ":"))

LAB = """
<style>
#plab{position:fixed;left:16px;bottom:16px;z-index:400;font-family:var(--font-body,system-ui);
 background:color-mix(in srgb,var(--bg) 88%, transparent);border:1px solid var(--line-strong);
 border-radius:18px;backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
 box-shadow:0 24px 60px -24px rgba(0,0,0,.8);max-width:min(300px,calc(100vw - 32px));overflow:hidden}
#plab-head{display:flex;align-items:center;gap:10px;padding:12px 14px;cursor:pointer;user-select:none}
#plab-dot{width:22px;height:22px;border-radius:7px;background:var(--brand-grad);flex:0 0 auto}
#plab-head b{font-family:var(--font-display,inherit);font-size:.85rem;font-weight:700;flex:1;color:var(--text)}
#plab-head i{font-style:normal;color:var(--muted);font-size:.78rem;transition:transform .25s}
#plab.closed #plab-body{display:none}
#plab.closed #plab-head i{transform:rotate(-90deg)}
#plab-body{padding:0 12px 12px;display:grid;gap:6px}
#plab-note{font-size:.72rem;color:var(--muted);padding:0 2px 6px;line-height:1.45}
.plab-opt{display:flex;align-items:center;gap:10px;width:100%;padding:9px 10px;border-radius:11px;
 border:1.5px solid transparent;background:var(--surface-2);cursor:pointer;text-align:left;transition:.18s}
.plab-opt:hover{background:var(--surface-3)}
.plab-opt.on{border-color:var(--brand);background:color-mix(in srgb,var(--brand) 12%,var(--surface-2))}
.plab-sw{width:30px;height:20px;border-radius:6px;flex:0 0 auto;box-shadow:inset 0 0 0 1px rgba(255,255,255,.12)}
.plab-opt span{display:block;font-size:.82rem;font-weight:600;color:var(--text);font-family:var(--font-display,inherit)}
.plab-opt small{display:block;font-size:.68rem;color:var(--muted);margin-top:1px}
@media(max-width:620px){#plab{left:10px;bottom:10px;right:76px;max-width:none}}
</style>
<div id="plab" class="closed" role="region" aria-label="Palette lab">
  <div id="plab-head" role="button" tabindex="0" aria-expanded="false">
    <span id="plab-dot"></span><b>Palette lab</b><i>▾</i>
  </div>
  <div id="plab-body">
    <div id="plab-note">Preview only — pick a scheme and browse the site in it. Your choice follows you from page to page.</div>
  </div>
</div>
<script>
(function(){
  var P=window.__S4KP||{},lab=document.getElementById('plab'),body=document.getElementById('plab-body'),
      head=document.getElementById('plab-head');
  Object.keys(P).forEach(function(id){
    var p=P[id],b=document.createElement('button');
    b.className='plab-opt'+(id===window.__S4KPID?' on':'');b.type='button';b.dataset.p=id;
    b.innerHTML='<span class="plab-sw" style="background:linear-gradient(104deg,'+p.sw[0]+','+p.sw[1]+')"></span>'+
                '<span>'+p.name+'<small>'+p.note+'</small></span>';
    b.addEventListener('click',function(){
      window.__s4kApply(id);
      try{localStorage.setItem('s4k-pal2',id);}catch(e){}
      body.querySelectorAll('.plab-opt').forEach(function(o){o.classList.toggle('on',o.dataset.p===id);});
    });
    body.appendChild(b);
  });
  function toggle(){var c=lab.classList.toggle('closed');head.setAttribute('aria-expanded',String(!c));}
  head.addEventListener('click',toggle);
  head.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();toggle();}});
})();
</script>
"""


def build():
    if os.path.exists(DST):
        shutil.rmtree(DST)
    os.makedirs(DST)

    # copy tree
    for item in os.listdir(SRC):
        if item in SKIP_TOP or item in SKIP_FILES:
            continue
        s, d = os.path.join(SRC, item), os.path.join(DST, item)
        (shutil.copytree if os.path.isdir(s) else shutil.copy2)(s, d)

    # known page paths
    pages = set()
    for dp, dn, fn in os.walk(DST):
        if "index.html" in fn:
            rel = os.path.relpath(dp, DST)
            pages.add("/" if rel == "." else "/" + rel.replace(os.sep, "/"))

    counts = {}
    for dp, dn, fn in os.walk(DST):
        for f in fn:
            if not f.endswith(".html"):
                continue
            full = os.path.join(dp, f)
            depth = len(os.path.relpath(dp, DST).split(os.sep)) if os.path.relpath(dp, DST) != "." else 0
            up = "../" * depth
            html = open(full, encoding="utf-8").read()

            def fix(m):
                attr, path, frag = m.group(1), m.group(2), m.group(3) or ""
                if path == "/":
                    tgt = "index.html"
                elif path in pages:
                    tgt = path.lstrip("/") + "/index.html"
                else:
                    tgt = path.lstrip("/")
                return f'{attr}="{up}{tgt}{frag}"'

            html, n = re.subn(r'(href|src)="(/[^"#]*)(#[^"]*)?"', fix, html)
            counts[os.path.relpath(full, DST)] = n

            html = html.replace("</head>", APPLY + "\n</head>", 1)
            html = html.replace("</body>", LAB + "\n</body>", 1)
            open(full, "w", encoding="utf-8").write(html)

    print(f"{len(counts)} files rewritten")
    print(f"  total link rewrites: {sum(counts.values())}")
    print(f"  min/max per file: {min(counts.values())}/{max(counts.values())}")
    print(f"  pages discovered: {len(pages)}")


if __name__ == "__main__":
    build()
