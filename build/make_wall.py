#!/usr/bin/env python3
"""Streamly4K — generates the original artwork for the hero poster wall.

Each tile is a complete poster composition: an abstract cinematic key image,
a darkened lower third, a title set in condensed caps, a simulated billing
block and — on some — festival laurels. Titles are invented. Everything is
graded in colour the way a real one-sheet is, so the wall keeps tonal
variety instead of flattening to a single hue.

    python3 make_wall.py        ->  ../assets/img/wall/01.jpg … 26.jpg

Nothing here is traced, sampled or derived from anyone else's artwork.
"""
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 300, 450

# Poster colour schemes — (shadow rgb, highlight rgb). Real one-sheets lean on
# a small number of duotone grades; these are the common ones.
GRADES = [
    ((10, 24, 34), (255, 178, 92)),    # teal & orange
    ((20, 5, 9),   (255, 108, 88)),    # crimson
    ((5, 11, 28),  (150, 198, 255)),   # night blue
    ((16, 7, 28),  (214, 150, 255)),   # violet
    ((24, 15, 5),  (255, 206, 132)),   # amber sepia
    ((5, 19, 13),  (146, 238, 178)),   # toxic green
    ((7, 15, 23),  (202, 234, 255)),   # ice
    ((22, 5, 19),  (255, 142, 208)),   # magenta
    ((18, 18, 20), (236, 236, 240)),   # silver / mono
]


def colorize(gray, shadow, high):
    """Map a greyscale key image through a two-colour cinematic grade."""
    a = np.asarray(gray, dtype=np.float32) / 255.0
    lo = np.array(shadow, dtype=np.float32)
    hi = np.array(high, dtype=np.float32)
    curve = a ** 0.92
    rgb = lo[None, None, :] + (hi - lo)[None, None, :] * curve[:, :, None]
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")
_BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img")
OUT = os.path.join(_BASE, "wall")     # finished posters, with title type — hero wall
OUT_ART = os.path.join(_BASE, "art")  # the same key images WITHOUT type — catalogue tiles

# Invented titles — deliberately generic genre-film phrasing.
TITLES = [
    "NIGHT SIGNAL", "THE LAST CIRCUIT", "COLD HARBOUR", "SEVEN MILES DOWN",
    "AFTERGLOW", "RED SECTOR", "THE QUIET LINE", "SILENT ORBIT",
    "GLASS CITY", "THE RECKONING HOUR", "DEEP WATER RUN", "PAPER TIGERS",
    "VELOCITY", "THE LONG DARK", "SALT AND IRON", "NORTHBOUND",
    "THE FIFTH WINTER", "BROKEN COMPASS", "LAST LIGHT STATION", "THE HOLLOW COAST",
    "WILDFIRE SEASON", "THE NARROW ROAD", "TERMINAL VELOCITY DRIVE", "ASH & AMBER",
    "THE OUTER BANKS RUN", "MIDNIGHT FREQUENCY",
]

TAGLINES = ["ONE CHOICE CHANGES EVERYTHING", "SOME DOORS STAY SHUT",
            "THE TRUTH RUNS DEEPER", "NO ONE COMES BACK THE SAME",
            "EVERY SECOND COUNTS", "FROM THE DARK", ""]

FONT_TITLE = ["/mnt/skills/examples/canvas-design/canvas-fonts/BigShoulders-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf",
              "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf"]
FONT_SMALL = ["/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]


def load(paths, size):
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return None


# ---------------------------------------------------------------- helpers
def canvas(top=0.06, bottom=0.30, curve=1.4):
    y = (np.linspace(0, 1, H) ** curve)[:, None]
    return np.repeat(top + (bottom - top) * y, W, axis=1)


def glow(arr, cx, cy, r, strength, soft=1.9):
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - cx) / r) ** 2 + ((yy - cy) / r) ** 2)
    return arr + strength * np.exp(-(d ** soft) * 2.2)


def to_img(arr):
    return Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8), "L")


def from_img(img):
    return np.asarray(img, dtype=np.float32) / 255.0


# ---------------------------------------------------------------- motifs
def m_floodlights(rng):
    a = canvas(.03, .16)
    for _ in range(rng.randint(3, 5)):
        a = glow(a, rng.uniform(.1, .9) * W, rng.uniform(-.05, .22) * H,
                 rng.uniform(46, 96), rng.uniform(.55, .95))
    img = to_img(a); d = ImageDraw.Draw(img)
    for _ in range(rng.randint(4, 7)):
        x = rng.uniform(0, W)
        d.polygon([(x, 0), (x + rng.uniform(8, 26), 0),
                   (x + rng.uniform(40, 130), H), (x - rng.uniform(10, 70), H)],
                  fill=int(rng.uniform(28, 62)))
    return np.maximum(from_img(img), a)


def m_skyline(rng):
    a = canvas(.62, .10, curve=.75)
    img = to_img(a); d = ImageDraw.Draw(img)
    for layer, (tone, base) in enumerate([(70, .58), (40, .70), (14, .84)]):
        x = -10
        while x < W + 10:
            w = rng.uniform(14, 40)
            top = H * base - rng.uniform(10, 105) * (1 - layer * .22)
            d.rectangle([x, top, x + w, H], fill=tone)
            if layer == 2:
                for _ in range(int(w * .5)):
                    wx, wy = rng.uniform(x + 3, x + w - 4), rng.uniform(top + 6, H - 8)
                    d.rectangle([wx, wy, wx + 2, wy + 3], fill=int(rng.uniform(90, 190)))
            x += w + rng.uniform(2, 9)
    return from_img(img)


def m_crowd(rng):
    a = canvas(.30, .05, curve=.8)
    a = glow(a, W * rng.uniform(.3, .7), H * .18, 120, .55)
    img = to_img(a); d = ImageDraw.Draw(img)
    for row, (tone, y0) in enumerate([(52, .70), (30, .80), (10, .92)]):
        x = -12
        while x < W + 12:
            r = rng.uniform(7, 14) * (1 + row * .25)
            cy = H * y0 + rng.uniform(-6, 6)
            d.ellipse([x, cy - r, x + r * 1.5, cy + r], fill=tone)
            d.rectangle([x, cy, x + r * 1.5, H], fill=tone)
            x += r * rng.uniform(1.1, 1.8)
    return from_img(img)


def m_rings(rng):
    a = canvas(.05, .14)
    cx, cy = W * rng.uniform(.3, .7), H * rng.uniform(.28, .5)
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    return a + .34 * (.5 + .5 * np.sin(d / rng.uniform(7, 16))) * np.exp(-d / rng.uniform(120, 220))


def m_shaft(rng):
    a = canvas(.04, .12)
    img = to_img(a); d = ImageDraw.Draw(img)
    ang = rng.uniform(-.7, -.3)
    for _ in range(rng.randint(5, 9)):
        x, w = rng.uniform(-W * .4, W * 1.2), rng.uniform(10, 40)
        d.polygon([(x, 0), (x + w, 0), (x + w + H * ang, H), (x + H * ang, H)],
                  fill=int(rng.uniform(40, 120)))
    img = img.filter(ImageFilter.GaussianBlur(rng.uniform(2, 6)))
    return np.maximum(from_img(img), a)


def m_ridges(rng):
    a = canvas(.58, .16, curve=.7)
    a = glow(a, W * rng.uniform(.25, .75), H * .2, 80, .5)
    img = to_img(a); d = ImageDraw.Draw(img)
    for layer in range(4):
        base, pts, x = H * (.40 + layer * .11), [(-10, H)], -10
        while x < W + 10:
            pts.append((x, base - rng.uniform(0, 60) * (1 - layer * .2)))
            x += rng.uniform(16, 42)
        pts.append((W + 10, H))
        d.polygon(pts, fill=int(96 - layer * 26))
    return from_img(img)


def m_spotlight(rng):
    a = canvas(.02, .08)
    cx, cy = W * rng.uniform(.35, .65), H * rng.uniform(.3, .44)
    a = glow(a, cx, cy, rng.uniform(70, 120), .85, soft=2.4)
    img = to_img(a); d = ImageDraw.Draw(img)
    hw = rng.uniform(16, 24)
    d.ellipse([cx - hw * .62, cy - hw * 1.5, cx + hw * .62, cy - hw * .25], fill=12)
    d.polygon([(cx - hw, H), (cx - hw * .72, cy - hw * .3),
               (cx + hw * .72, cy - hw * .3), (cx + hw, H)], fill=12)
    return from_img(img.filter(ImageFilter.GaussianBlur(1.1)))


def m_speed(rng):
    a = canvas(.05, .13)
    img = to_img(a); d = ImageDraw.Draw(img)
    for _ in range(rng.randint(26, 44)):
        y, x = rng.uniform(0, H), rng.uniform(-40, W)
        d.line([(x, y), (x + rng.uniform(30, 170), y + rng.uniform(-3, 3))],
               fill=int(rng.uniform(40, 200)), width=int(rng.uniform(1, 4)))
    img = img.filter(ImageFilter.GaussianBlur(rng.uniform(1.2, 2.6)))
    return np.maximum(from_img(img), a)


def m_stars(rng):
    a = canvas(.02, .05)
    for _ in range(rng.randint(2, 4)):
        a = glow(a, rng.uniform(0, W), rng.uniform(0, H * .7), rng.uniform(60, 140), rng.uniform(.14, .3))
    img = to_img(a); d = ImageDraw.Draw(img)
    for _ in range(rng.randint(130, 240)):
        x, y, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(.4, 1.6)
        d.ellipse([x, y, x + r, y + r], fill=int(rng.uniform(90, 255)))
    return from_img(img)


def m_horizon(rng):
    hz = rng.uniform(.38, .5)
    a = canvas(.52, .08, curve=.9)
    a[int(H * hz):, :] = np.linspace(.30, .04, H - int(H * hz))[:, None]
    cx = W * rng.uniform(.3, .7)
    a = glow(a, cx, H * hz, rng.uniform(40, 80), .85, soft=2.2)
    img = to_img(a); d = ImageDraw.Draw(img)
    for i in range(int(H * (1 - hz) / 6)):
        y, w = H * hz + i * 6 + rng.uniform(0, 3), rng.uniform(16, 70)
        d.line([(cx - w, y), (cx + w, y)], fill=int(max(0, 150 - i * 6)), width=1)
    return from_img(img.filter(ImageFilter.GaussianBlur(.8)))


def m_grid(rng):
    a = canvas(.04, .10)
    img = to_img(a); d = ImageDraw.Draw(img)
    hz, vx = H * rng.uniform(.32, .44), W * rng.uniform(.35, .65)
    for i in range(-14, 15):
        d.line([(vx + i * W * .11, H), (vx, hz)], fill=int(rng.uniform(40, 95)), width=1)
    y, step = hz, 2.0
    while y < H:
        d.line([(0, y), (W, y)], fill=int(rng.uniform(45, 110)), width=1)
        step *= 1.32; y += step
    return glow(from_img(img), vx, hz, 70, .5)


def m_bokeh(rng):
    a = canvas(.03, .11)
    img = to_img(a)
    for _ in range(rng.randint(12, 22)):
        layer = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(layer)
        r = rng.uniform(8, 42)
        x, y = rng.uniform(-10, W), rng.uniform(-10, H)
        d.ellipse([x - r, y - r, x + r, y + r], fill=int(rng.uniform(60, 220)))
        layer = layer.filter(ImageFilter.GaussianBlur(r * rng.uniform(.18, .45)))
        img = Image.fromarray(np.maximum(np.asarray(img), np.asarray(layer)))
    return np.maximum(from_img(img), a)


def m_curtain(rng):
    a = canvas(.10, .04, curve=1.1)
    img = to_img(a); d = ImageDraw.Draw(img)
    x = 0
    while x < W:
        w = rng.uniform(10, 26)
        d.rectangle([x, 0, x + w, H], fill=int(rng.uniform(18, 90)))
        x += w
    img = img.filter(ImageFilter.GaussianBlur(rng.uniform(1.5, 3.5)))
    return glow(from_img(img), W * rng.uniform(.2, .8), H * rng.uniform(.1, .3), 110, .45)


MOTIFS = [m_floodlights, m_skyline, m_crowd, m_rings, m_shaft, m_ridges,
          m_spotlight, m_speed, m_stars, m_horizon, m_grid, m_bokeh, m_curtain]


# ------------------------------------------------------- poster composition
def wrap(draw, text, font, maxw):
    if font is None:
        return [text]
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines[:3]


def laurels(d, cx, cy, h, tone):
    """A pair of festival laurel branches."""
    for side in (-1, 1):
        for i in range(7):
            t = i / 6
            ang = math.radians(-58 + t * 116)
            px = cx + side * (h * .40) * (0.35 + 0.65 * math.sin(math.radians(20 + t * 140)))
            py = cy - h * .42 + t * h * .84
            r = h * (0.13 - 0.05 * abs(t - .5) * 2)
            d.ellipse([px - r * .45, py - r, px + r * .45, py + r], fill=tone)


def compose(art, rng, idx):
    """Turn a colour key image into a finished poster."""
    img = art.convert("RGB")
    d = ImageDraw.Draw(img)

    layout = rng.choice(["bottom", "bottom", "bottom", "top", "lower-left"])
    title = TITLES[idx % len(TITLES)]
    tag = rng.choice(TAGLINES)

    # ---- darkened title zone
    band = Image.new("L", (W, H), 0)
    bd = ImageDraw.Draw(band)
    if layout == "top":
        for i in range(int(H * .42)):
            bd.line([(0, i), (W, i)], fill=int(235 * (1 - i / (H * .42)) ** 1.5))
    else:
        top = int(H * .48)
        for i in range(top, H):
            bd.line([(0, i), (W, i)], fill=int(238 * ((i - top) / (H - top)) ** .85))
    mask = np.asarray(band).astype(np.float32)[:, :, None] / 255 * .88
    img = Image.fromarray((np.asarray(img).astype(np.float32) * (1 - mask)).astype(np.uint8))
    d = ImageDraw.Draw(img)

    # ---- type
    fs = rng.randint(24, 33) if len(title) < 16 else rng.randint(19, 25)
    ft = load(FONT_TITLE, fs)
    fsmall = load(FONT_SMALL, 6)
    lines = wrap(d, title, ft, W - 34)

    if layout == "top":
        y = 26
    elif layout == "lower-left":
        y = H - 30 - len(lines) * (fs + 2) - 26
    else:
        y = H - 26 - len(lines) * (fs + 2) - 30

    if tag and layout != "lower-left":
        fttag = load(FONT_SMALL, 7)
        if fttag:
            tw = d.textlength(tag, font=fttag)
            d.text(((W - tw) / 2, y - 14), tag, fill=(196, 196, 200), font=fttag)

    for ln in lines:
        tw = d.textlength(ln, font=ft) if ft else len(ln) * fs * .5
        x = 18 if layout == "lower-left" else (W - tw) / 2
        d.text((x, y), ln, fill=(248, 246, 244), font=ft)
        y += fs + 2

    # ---- billing block: rows of tiny bars, the way credits read at distance
    y += 10
    for row in range(rng.randint(3, 6)):
        widths, total = [], 0
        while total < W - 60:
            seg = rng.uniform(10, 34)
            widths.append(seg); total += seg + 5
        x = (W - (total - 5)) / 2 if layout != "lower-left" else 18
        for seg in widths:
            d.rectangle([x, y, x + seg, y + 2], fill=(rng.randint(140, 190),) * 3)
            x += seg + 5
        y += 6

    # ---- occasional laurels
    if rng.random() < .30 and layout != "top":
        laurels(d, W / 2, H * .40, 38, (190, 190, 194))
        if fsmall:
            for k, txt in enumerate(("OFFICIAL", "SELECTION")):
                tw = d.textlength(txt, font=fsmall)
                d.text(((W - tw) / 2, H * .40 - 8 + k * 8), txt, fill=(200, 200, 204), font=fsmall)

    # ---- edge
    d.rectangle([0, 0, W - 1, H - 1], outline=(64, 62, 62))
    return img


def finish(img, rng, grain=0.032, blur=0.45, vignette=0.5):
    arr = np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0
    yy, xx = np.mgrid[0:H, 0:W]
    dd = np.sqrt(((xx - W / 2) / (W * .78)) ** 2 + ((yy - H / 2) / (H * .78)) ** 2)
    arr = arr * (1 - vignette * np.clip(dd - .42, 0, 1) ** 1.5)[:, :, None]
    arr = arr + rng.normal(0, grain, arr.shape)
    out = Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8), "RGB")
    return out.filter(ImageFilter.GaussianBlur(blur)) if blur else out


# ---------------------------------------------------------------- main
def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(OUT_ART, exist_ok=True)
    if load(FONT_TITLE, 20) is None:
        print("  ! no condensed display font found — titles will fall back to a bitmap face")
    n, total, total_art = 0, 0, 0
    for variant in range(2):
        for i, motif in enumerate(MOTIFS):
            seed = 4400 + variant * 137 + i * 19
            rng = random.Random(seed)
            nprng = np.random.default_rng(seed)
            grade = GRADES[(i + variant * 5) % len(GRADES)]
            art = colorize(to_img(motif(rng)), *grade)

            # untyped key image — used behind the catalogue titles
            plain = finish(art, np.random.default_rng(seed + 1),
                           grain=.028 + variant * .010,
                           blur=.45 + variant * .20,
                           vignette=.50 + variant * .10)

            # full poster with title, tagline, billing block — used on the hero wall
            poster = finish(compose(art, rng, n), nprng,
                            grain=.028 + variant * .010,
                            blur=.40 + variant * .20,
                            vignette=.46 + variant * .10)
            n += 1
            pw = os.path.join(OUT, f"{n:02d}.jpg")
            pa = os.path.join(OUT_ART, f"{n:02d}.jpg")
            poster.save(pw, "JPEG", quality=76, optimize=True, progressive=True,
                        subsampling=1)
            plain.save(pa, "JPEG", quality=74, optimize=True, progressive=True,
                       subsampling=1)
            total += os.path.getsize(pw)
            total_art += os.path.getsize(pa)
            print(f"  ✓ {n:02d}.jpg  {motif.__name__[2:]:<12} "
                  f"{TITLES[(n-1) % len(TITLES)]:<26} "
                  f"poster {os.path.getsize(pw)/1024:5.1f} KB · art {os.path.getsize(pa)/1024:5.1f} KB")
    print(f"\n{n} posters ({total/1024:.0f} KB) + {n} untyped key images ({total_art/1024:.0f} KB)"
          f", {W}×{H} colour JPEG")


if __name__ == "__main__":
    main()
