# Streamly4K — streamly4k.com

A fast, static, SEO-ready marketing site for a US-market IPTV subscription service.
No build step required to deploy: the `streamly4k/` folder is the site.

---

## 1. Before you go live — edit these

| What | Where |
|---|---|
| **WhatsApp number, email, prices** | `assets/js/config.js` — the only file you normally need |
| **Domain / canonical URLs** | `build/lib.py` → `BASE` and `DOMAIN`, then rebuild |
| **Real customer reviews** | `assets/js/reviews.js` (ships empty on purpose — see below) |
| **Catalogue titles** | `build/data.py` → `TMDB_FILMS` / `TMDB_SERIES`, or re-run `build/fetch_tmdb.py` |
| **Hero wall art** | `assets/img/wall/` → regenerate with `build/make_wall.py` |

### The only required edit

Open `assets/js/config.js` and change:

```js
whatsapp: "12025550123",            // your real number, digits only, no + and no spaces
email:    "support@streamly4k.com", // your real support address
```

Every WhatsApp button, the order form, the contact form and the pricing calculator
read from this file. Prices live here too — change `plans[].price` and the whole
site updates.

---

## 2. Deploy to Vercel via GitHub

```bash
cd streamly4k
git init
git add .
git commit -m "Streamly4K site"
git branch -M main
git remote add origin https://github.com/<your-user>/streamly4k.git
git push -u origin main
```

Then on **vercel.com → Add New → Project → Import** your repo:

- **Framework preset:** Other
- **Build command:** leave empty
- **Output directory:** leave empty (root)
- **Install command:** leave empty

Deploy, then **Settings → Domains → Add `streamly4k.com`** and point your DNS:

| Type | Name | Value |
|---|---|---|
| A | `@` | `76.76.21.21` |
| CNAME | `www` | `cname.vercel-dns.com` |

`vercel.json` already sets clean URLs (`/pricing`, not `/pricing/index.html`),
long-term caching on `/assets/*` and basic security headers.

---

## 3. Rebuilding after a content change

Page content lives in Python so 27 pages share one header, one footer and one nav.

```bash
cd build
python3 build.py      # regenerates everything into ../streamly4k/
```

| File | Holds |
|---|---|
| `build/lib.py` | Head, header, nav, footer, page shell, icons, FAQ/CTA blocks |
| `build/sections.py` | Homepage sections (hero, stats, marquee, posters, savings, pricing builder, steps) |
| `build/data.py` | Channel lists, categories, FAQ text, blog index |
| `build/build.py` | One function per page + sitemap/robots/vercel.json |
| `build/make_wall.py` | Draws the 26 original hero-wall tiles into `assets/img/wall/` |
| `build/fetch_tmdb.py` | Refreshes the catalogue titles from TMDB (text only) |

`assets/css/style.css` and `assets/js/*.js` are **not** generated — edit them directly.

---

## 4. Pages

```
/                    /pricing            /channels
/setup               /setup/smart-tv     /setup/firestick
/setup/android       /setup/iphone-ipad  /setup/pc-mac
/setup/mag-box       /reviews            /blog  (+ 6 articles)
/faq                 /contact            /order
/free-trial          /thank-you          /404
/legal/terms         /legal/privacy      /legal/refund   /legal/dmca
```

Plus `sitemap.xml`, `robots.txt`, `site.webmanifest`, `favicon.svg`.

---

## 5. Two things deliberately left empty

**Reviews.** `assets/js/reviews.js` ships with an empty array and the reviews page
shows an honest "collecting reviews" state until you fill it. Publishing invented
testimonials is illegal advertising in the US (FTC Act §5 and the 2024 Rule on
Consumer Reviews and Testimonials, which carries civil penalties per violation)
and in the UK/EU, and Trustpilot delists businesses for it. Collect real ones and
paste them in — the format is documented at the top of that file.

**The rating badge.** `config.js` has `rating.show: false`, so the "4.7 on
Trustpilot · 51 reviews" style badge is removed from the page entirely. Set it to
`true` and fill in the real score, count and profile URL once you have a real
profile — the badge then links to it.

Everything else on the site — activation times, the guarantee, the savings
comparison — is written so you can stand behind it. The savings figures use
published September 2026 list prices and are labelled as a price comparison, not
a content comparison.

---

## 6. Catalogue data & artwork

The on-demand section is built from a TMDB snapshot baked into `data.py` at
build time — **text only**: titles, years, genres, ratings. To refresh it:

```bash
export TMDB_API_KEY=your_key      # never commit this
cd build && python3 fetch_tmdb.py && python3 build.py
```

The key stays in your shell. Nothing ships with a credential in it and the
live pages make no API calls, so there is no key for anyone to lift from the
page source.

**No poster artwork is used.** TMDB hosts studio artwork but holds no right to
license it onward, and studio poster art on a commercial storefront is the
usual trigger for a host takedown — the claim goes to Vercel and your
registrar, not to a search engine, so keeping the site out of Google does not
avoid it. The hero wall and the catalogue tiles use 26 original greyscale
images drawn by `build/make_wall.py`, tinted to the brand colour at runtime.
Re-run that script for a fresh set, or drop your own licensed 2:3 JPGs into
`assets/img/wall/` and list them in `config.js`.

TMDB's terms require the attribution line already printed under the catalogue
section. Leave it in place.

---

## 7. Brand

| Token | Value |
|---|---|
| Ink (warm black) | `#080605` |
| Ember (primary) | `#FF4D2E` |
| Amber (secondary) | `#FF9A3D` |
| Gradient | `104deg, #FF4D2E → #FF9A3D` |
| Accent (badges/stars) | `#FFD66B` |
| Display type | Outfit 700/800 |
| Body type | Inter 400/500/600 |
| Handwriting | Caveat 600 |

The logo mark is inline SVG in `build/lib.py` (`LOGO_MARK`) and standalone in
`favicon.svg` — a play triangle with signal bars trailing off to the left.

Light mode deepens the brand to `#D93A1B → #E07A12` so it stays legible on white.
All six tokens live at the top of `assets/css/style.css` — nothing else hard-codes a
brand colour, so a future re-skin is a six-value edit.

---

## 8. Local preview

```bash
cd streamly4k
python3 -m http.server 8000
# open http://localhost:8000
```

Clean URLs only work on Vercel; locally use `/pricing/` with the trailing slash.
