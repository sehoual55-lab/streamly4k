#!/usr/bin/env python3
"""Refresh the catalogue snapshot in data.py from The Movie Database.

    export TMDB_API_KEY=your_key_here
    python3 fetch_tmdb.py && python3 build.py

Two things come back:

  * catalogue text — titles, years, genres and ratings — baked into data.py;
  * hero wall posters — image.tmdb.org URLs written into the marked block in
    assets/js/config.js. Nothing is downloaded: the pages hotlink TMDB's CDN.

Heads up on the posters: TMDB hosts studio artwork but holds no right to
license it onward, so a commercial storefront displaying it is the usual
starting point for a host or registrar takedown. Pass --no-posters (or set
WALL_POSTERS=0) to leave config.js alone and keep the generated tiles from
make_wall.py in the hero.

The key is read from the environment and never written into the site: this
script bakes plain text and image URLs in at build time, so nothing ships
with a credential in it and the live pages make no API calls.
"""
import os, re, sys, json, pathlib, datetime
from urllib.request import urlopen
from urllib.parse import urlencode

KEY = os.environ.get("TMDB_API_KEY", "").strip()
if not KEY:
    sys.exit("Set TMDB_API_KEY first:  export TMDB_API_KEY=...")

BASE = "https://api.themoviedb.org/3/"
HERE = pathlib.Path(__file__).resolve().parent

# Formats that make poor showcase tiles for an IPTV catalogue
TV_SKIP = {10767, 10763, 10764, 10766}     # talk, news, reality, soap
N_FILMS, N_TOP, N_SERIES = 12, 12, 12

# Hero wall: main.js sizes tiles to a target width, so a 1440px screen draws
# ~13 columns x 9 rows = 117 tiles. 100 posters covers a full screen with only
# a couple of repeats; going much higher costs bandwidth for no visible gain.
N_WALL = 100
WALL_PAGES = (1, 2, 3, 4, 5, 6, 7)
WALL_SIZE = "w185"          # ~18 KB each; tiles are small AND blurred
WALL_MIN_VOTES = 150        # keeps obscure filler and soft-porn listings out
DO_POSTERS = "--no-posters" not in sys.argv and os.environ.get("WALL_POSTERS") != "0"


def get(path, **params):
    params["api_key"] = KEY
    params.setdefault("language", "en-US")
    with urlopen(BASE + path + "?" + urlencode(params), timeout=25) as r:
        return json.load(r)


def write_wall():
    """Rewrite the wallImages block in assets/js/config.js with fresh posters."""
    seen, posters = set(), []
    for page in WALL_PAGES:
        for m in get("movie/popular", page=page)["results"]:
            path = m.get("poster_path")
            if (not path or path in seen or m.get("adult")
                    or (m.get("vote_count") or 0) < WALL_MIN_VOTES):
                continue
            seen.add(path)
            posters.append((m["title"], path))
    posters = posters[:N_WALL]
    if len(posters) < 12:
        sys.exit(f"Only {len(posters)} usable posters came back — leaving config.js alone.")

    urls = [f'"https://image.tmdb.org/t/p/{WALL_SIZE}{p}",' for _, p in posters]
    w = max(len(u) for u in urls)
    body = "\n".join(f"    {u:<{w}} /* {t} */" for u, (t, _) in zip(urls, posters))

    cfg = HERE.parent / "assets" / "js" / "config.js"
    src = cfg.read_text()
    START = "  /* --- TMDB WALL START (regenerate with build/fetch_tmdb.py) --- */\n"
    END = "  /* --- TMDB WALL END --- */\n"
    if START not in src or END not in src:
        sys.exit("Marker comments missing from config.js — refresh wallImages by hand.")
    head, rest = src.split(START, 1)
    _, tail = rest.split(END, 1)
    cfg.write_text(head + START + f"  wallImages: [\n{body}\n  ],\n" + END + tail)
    print(f"✓ config.js updated — {len(posters)} hero posters ({WALL_SIZE})")


def main():
    gm = {g["id"]: g["name"] for g in get("genre/movie/list")["genres"]}
    gt = {g["id"]: g["name"] for g in get("genre/tv/list")["genres"]}

    films = []
    for page in (1, 2):
        for m in get("movie/popular", page=page)["results"]:
            if not m.get("release_date") or not m.get("vote_average"):
                continue
            gid = (m.get("genre_ids") or [0])[0]
            films.append((m["title"], gm.get(gid, "Feature"),
                          int(m["release_date"][:4]), round(m["vote_average"], 1)))
    films.sort(key=lambda r: -r[3])

    top = []
    for page in (1, 2):
        for m in get("movie/top_rated", page=page)["results"]:
            if not m.get("release_date") or not m.get("vote_average"):
                continue
            gid = (m.get("genre_ids") or [0])[0]
            top.append((m["title"], gm.get(gid, "Feature"),
                        int(m["release_date"][:4]), round(m["vote_average"], 1)))
    top.sort(key=lambda r: -r[3])

    series = []
    for endpoint in ("tv/top_rated", "tv/popular"):
      for page in (1, 2):
        for t in get(endpoint, page=page)["results"]:
            ids = set(t.get("genre_ids") or [])
            if ids & TV_SKIP or not t.get("first_air_date") or not t.get("vote_average"):
                continue
            gid = (t.get("genre_ids") or [0])[0]
            series.append((t["name"], gt.get(gid, "Series"),
                           int(t["first_air_date"][:4]), round(t["vote_average"], 1)))
    series.sort(key=lambda r: -r[3])

    def rows(items, n):
        w = max(len(i[0]) for i in items[:n]) + 3
        return "\n".join(
            f'    ({json.dumps(t) + ",":<{w}} {json.dumps(g) + ",":<14} {y}, {v}),'
            for t, g, y, v in items[:n])

    block = (f'TMDB_FETCHED = "{datetime.date.today():%d %B %Y}"\n\n'
             "# Films — TMDB /movie/popular, filtered to released titles with a rating.\n"
             f"TMDB_FILMS = [\n{rows(films, N_FILMS)}\n]\n\n"
             "# Films — TMDB /movie/top_rated.\n"
             f"TMDB_TOP_FILMS = [\n{rows(top, N_TOP)}\n]\n\n"
             "# Series — TMDB /tv/popular and /tv/top_rated, talk, news and reality formats removed.\n"
             f"TMDB_SERIES = [\n{rows(series, N_SERIES)}\n]\n")

    data = HERE / "data.py"
    src = data.read_text()
    START = "# --- TMDB SNAPSHOT START (regenerate with fetch_tmdb.py) ---\n"
    END = "# --- TMDB SNAPSHOT END ---\n"
    if START not in src or END not in src:
        sys.exit("Marker comments missing from data.py — refresh the snapshot by hand.")
    head, rest = src.split(START, 1)
    _, tail = rest.split(END, 1)
    new = head + START + block + END + tail
    data.write_text(new)
    print(f"✓ data.py updated — {N_FILMS} + {N_TOP} films, {N_SERIES} series")

    if DO_POSTERS:
        write_wall()
    else:
        print("· hero posters skipped (--no-posters) — wall keeps make_wall.py tiles")

    print("  now run:  python3 build.py")


if __name__ == "__main__":
    main()
