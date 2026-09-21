#!/usr/bin/env python3
"""Streamly4K — static site generator.

    python3 build.py            # writes the site into ../streamly4k/
"""
import os, re, json, shutil, datetime
from lib import (page, pagehead, faq_block, faq_jsonld, cta_band, icon,
                 BRAND, DOMAIN, BASE, TAGLINE, SETUP_LINKS)
import lib
import sections as S
import data

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = []          # (path, priority, changefreq)


def write(path, html, priority="0.7", freq="monthly"):
    rel = "index.html" if path == "/" else path.strip("/") + "/index.html"
    full = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    PAGES.append((path, priority, freq))
    print(f"  ✓ {path:<28} → {rel}")


def write_raw(rel, text):
    full = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"  ✓ {rel}")


ORG_LD = json.dumps({
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": BRAND,
    "url": BASE,
    "logo": BASE + "/favicon.svg",
    "description": TAGLINE,
    "contactPoint": [{"@type": "ContactPoint", "contactType": "customer support",
                      "availableLanguage": ["English", "Spanish"], "areaServed": "US"}],
}, ensure_ascii=False)


# ===========================================================================
# 1. HOME
# ===========================================================================
def build_home():
    # stats() now lives inside hero() as the glass bar, not as its own band
    body = (S.hero() + S.channels_section() +
            S.savings_section() + S.builder_section() + S.steps_section() +
            S.why_section() + S.platforms_rail() +
            faq_block(data.FAQ_HOME[:6]) +
            cta_band(f'Ready when <span class="grad">you are.</span>',
                     "Pick a plan, send your order, and we will have you watching in minutes."))
    ld = "[" + ORG_LD + "," + faq_jsonld(data.FAQ_HOME[:6]) + "," + json.dumps({
        "@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "url": BASE
    }) + "]"
    write("/", page("/",
          f"{BRAND} — IPTV Subscription USA | 25,000+ Live Channels in 4K",
          "Stream 25,000+ live TV channels, sports, movies and series in HD and 4K on any device. "
          "Plans from $39.99. Activated in 5–15 minutes. 7-day money-back guarantee.",
          body, jsonld=ld), priority="1.0", freq="weekly")


# ===========================================================================
# 2. PRICING
# ===========================================================================
def build_pricing():
    plans = ""
    for pid, name, tag, price, per, feats, best in [
        ("3m", "3 Months", "Basic", "39.99", "13.33",
         ["25,000+ live channels", "120,000+ movies &amp; series", "4K, HDR &amp; Full HD",
          "TV guide (EPG) included", "Catch-up up to 7 days", "24/7 WhatsApp support"], False),
        ("6m", "6 Months", "Standard", "69.99", "11.67",
         ["Everything in 3 Months", "Save $1.67 every month", "Priority support queue",
          "Free line transfer between devices", "7-day money-back guarantee"], False),
        ("12m", "12 Months", "Premium", "99.99", "8.33",
         ["Everything in 6 Months", "Best price per month", "Free setup help on any device",
          "Free re-activation if you change box", "Priority 24/7 support"], True),
    ]:
        li = "".join(f"<li>{icon('check')}<span>{f}</span></li>" for f in feats)
        flag = '<span class="plan__flag"><span class="badge">Best value</span></span>' if best else ""
        cls = " plan--best" if best else ""
        btn = "btn--primary" if best else "btn--ghost"
        plans += f"""<div class="plan{cls}">{flag}
      <div class="plan__name">{name} <span class="muted small">· {tag}</span></div>
      <div class="plan__price">${price}</div>
      <div class="plan__per">${per} / month · one-time payment</div>
      <ul>{li}</ul>
      <a href="#pricing" class="btn {btn} btn--block">Choose {name}</a>
    </div>"""

    incl_full = "".join(
        f'<div class="incl__item">{icon(ic)}<div><b>{t}</b><br><span>{d}</span></div></div>'
        for ic, t, d in data.INCLUDED)

    body = pagehead(
        "Pricing",
        'Simple pricing. <span class="grad">No surprises.</span>',
        "One line-up on every plan — only the length and the number of screens change. "
        "One-time payment, no contract, no auto-renewal.",
        crumbs=[("/", "Home"), (None, "Pricing")],
    ) + f"""
<section class="section--tight"><div class="wrap"><div class="plans reveal">{plans}</div>
  <p class="center muted small" style="margin-top:26px">Need more than one screen at a time? Add devices below — each extra device adds 50%.</p>
</div></section>

{S.builder_section(heading=False)}

<section class="section section--alt" id="included">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Included on every plan</span>
      <h2 class="d2">The term changes the price.<br><span class="grad">Never the line-up.</span></h2>
    </div>
    <div class="incl incl-2 reveal" style="max-width:900px;margin-inline:auto">{incl_full}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Compare</span>
      <h2 class="d2">How the plans stack up</h2>
    </div>
    <div class="table-wrap reveal">
      <table class="data">
        <thead><tr><th>What you get</th><th>3 Months</th><th>6 Months</th><th>12 Months</th></tr></thead>
        <tbody>
          <tr><td>Price (1 device)</td><td>$39.99</td><td>$69.99</td><td><strong>$99.99</strong></td></tr>
          <tr><td>Effective monthly cost</td><td>$13.33</td><td>$11.67</td><td><strong>$8.33</strong></td></tr>
          <tr><td>Live channels</td><td>25,000+</td><td>25,000+</td><td>25,000+</td></tr>
          <tr><td>Movies &amp; series</td><td>120,000+</td><td>120,000+</td><td>120,000+</td></tr>
          <tr><td>4K / HDR where available</td><td>{icon('check')}</td><td>{icon('check')}</td><td>{icon('check')}</td></tr>
          <tr><td>TV guide (EPG) &amp; catch-up</td><td>{icon('check')}</td><td>{icon('check')}</td><td>{icon('check')}</td></tr>
          <tr><td>24/7 WhatsApp support</td><td>{icon('check')}</td><td>{icon('check')}</td><td>{icon('check')}</td></tr>
          <tr><td>7-day money-back guarantee</td><td>{icon('check')}</td><td>{icon('check')}</td><td>{icon('check')}</td></tr>
          <tr><td>Free setup help on any device</td><td>—</td><td>{icon('check')}</td><td>{icon('check')}</td></tr>
          <tr><td>Free re-activation on a new box</td><td>—</td><td>—</td><td>{icon('check')}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

""" + faq_block([
        ("Is this a recurring subscription?",
         "No. You pay once for the term you choose. Nothing is stored, nothing renews automatically, and there is "
         "no card on file. When the term ends the line simply stops unless you choose to extend it."),
        ("What does an extra device cost?",
         "Each additional simultaneous device adds 50% of the plan price. A 12-month plan for one device is $99.99; "
         "for two devices it is $149.99. You only need extra devices if people want to watch different channels at "
         "the same time — you can install the app on as many devices as you like."),
        ("Which payment methods do you accept?",
         "Card (Visa and Mastercard), Apple Pay, Google Pay, Revolut and Wise. We send an invoice "
         "with the payment link after you place your order — no payment is taken on this website."),
        ("Can I switch plans later?",
         "Yes. Message us on WhatsApp and we will work out the difference and adjust your line. Your login details "
         "stay the same."),
        ("Do you offer a trial before I pay?",
         "Yes — up to 24 hours, free, so you can test the channels and the stability on your own connection first."),
    ], title="Pricing questions", eyebrow="Pricing FAQ",
       lede="The details people usually check before ordering.") + cta_band(
        'Pick a plan and <span class="grad">start watching.</span>',
        "Send your order on WhatsApp and we will have you set up in minutes.")

    write("/pricing", page("/pricing",
          f"Pricing — IPTV Plans from $39.99 | {BRAND}",
          "Streamly4K pricing: 3 months $39.99, 6 months $69.99, 12 months $99.99. One-time payment, "
          "no auto-renewal, 25,000+ channels on every plan, 7-day money-back guarantee.",
          body), priority="0.9", freq="weekly")


# ===========================================================================
# 3. CHANNELS
# ===========================================================================
def build_channels():
    blocks = ""
    for ic, name, count, desc, examples in data.CATEGORIES:
        chips = "".join(S._chip(e, ' style="min-width:120px;height:56px;font-size:.88rem"')
                        for e in examples)
        blocks += f"""<div class="card reveal" style="padding:26px">
      <div class="row" style="justify-content:space-between;align-items:flex-start">
        <div class="row" style="gap:14px">
          <span class="card__icon" style="margin:0">{icon(ic)}</span>
          <div><h3 style="margin:0">{name}</h3><p style="margin-top:4px">{desc}</p></div>
        </div>
        <span class="badge badge--soft">{count} channels</span>
      </div>
      <div class="row" style="gap:10px;margin-top:18px">{chips}</div>
    </div>"""

    body = pagehead(
        "Channel line-up",
        'Over <span class="grad">25,000 live channels.</span>',
        "Sports, entertainment, news, kids, documentaries and 2,800+ international channels — "
        "the same line-up on every plan.",
        crumbs=[("/", "Home"), (None, "Channels")],
        cta='<div class="row row-center" style="margin-top:28px"><a href="/pricing" class="btn btn--primary">See plans</a>'
            f'<a href="#" data-wa="Hi {BRAND}! Do you carry this channel: " class="btn btn--outline">Ask about a channel</a></div>',
    ) + f"""
<section class="section--tight">
  <div class="reveal" style="display:grid;gap:12px">{S.channels_marquee(4)}</div>
</section>

<section class="section">
  <div class="wrap"><div class="stack" style="gap:18px">{blocks}</div></div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Sport, specifically</span>
      <h2 class="d2">If it's on, <span class="grad">it's on.</span></h2>
      <p class="lede">The leagues and events people ask us about most.</p>
    </div>
    <div class="table-wrap reveal" style="max-width:900px;margin-inline:auto">
      <table class="data">
        <thead><tr><th>League / event</th><th>Coverage</th></tr></thead>
        <tbody>
          <tr><td>NFL &middot; regular season &amp; playoffs</td><td>National &amp; out-of-market feeds, RedZone</td></tr>
          <tr><td>NBA</td><td>National, local and international feeds</td></tr>
          <tr><td>MLB &amp; NHL</td><td>Full season coverage incl. regional networks</td></tr>
          <tr><td>College football &amp; basketball</td><td>ESPN family, SEC, ACC, Big Ten</td></tr>
          <tr><td>UFC &amp; boxing</td><td>Fight nights and most major PPV cards</td></tr>
          <tr><td>Soccer</td><td>Premier League, Champions League, LaLiga, Liga MX, MLS</td></tr>
          <tr><td>Motorsport</td><td>F1, NASCAR, MotoGP, IndyCar</td></tr>
          <tr><td>Golf &amp; tennis</td><td>The majors, PGA Tour, ATP &amp; WTA, Grand Slams</td></tr>
        </tbody>
      </table>
    </div>
    <p class="center muted small" style="margin-top:20px;max-width:70ch;margin-inline:auto">
      Channel and event availability changes over time and is not guaranteed for any specific broadcast.
      If there is something you need in particular, ask us before you order and we will tell you honestly.</p>
  </div>
</section>

""" + cta_band('One line-up. <span class="grad">Every plan.</span>',
               "Nothing is held back for a more expensive tier — the term is the only difference.")

    write("/channels", page("/channels",
          f"Channel List — 25,000+ Live TV Channels | {BRAND}",
          "Browse the Streamly4K channel line-up: sports, movies, entertainment, news, kids, documentaries "
          "and 2,800+ international channels. The same list on every plan.",
          body), priority="0.9")


# ===========================================================================
# 4. SETUP HUB + GUIDES
# ===========================================================================
SETUP_GUIDES = {
    "smart-tv": {
        "icon": "tv", "name": "Smart TV (Samsung & LG)",
        "title": "How to set up IPTV on a Samsung or LG Smart TV",
        "intro": "Samsung (Tizen) and LG (webOS) televisions both run IPTV apps natively — you do not need a box, "
                 "a stick or any extra hardware. The whole process takes about five minutes.",
        "app": "IPTV Smarters Pro or Smart STB",
        "steps": [
            "Open the app store on your TV — <strong>Samsung Apps</strong> on a Samsung, or the <strong>LG Content Store</strong> on an LG.",
            "Search for <strong>IPTV Smarters Pro</strong> (or <strong>Smart STB</strong> if Smarters is not available in your region) and install it.",
            "Open the app. It will show a <strong>MAC address</strong> on screen — send us that MAC address on WhatsApp.",
            "We register the MAC on our panel and reply with your portal URL, username and password.",
            "Choose <strong>Login with Xtream Codes API</strong>, enter the details we sent, and give the playlist a name.",
            "Wait 30–60 seconds for the channel list and TV guide to load, then start watching.",
        ],
        "tips": [
            "Use a wired Ethernet cable to your TV if you can — it is far more stable than Wi-Fi for live sport.",
            "If the app is missing from your store, your TV may be older than 2016; use a Firestick or Android box instead.",
            "Set the aspect ratio to <em>Original</em> in the player settings so 4K channels are not stretched.",
        ],
    },
    "firestick": {
        "icon": "stick", "name": "Amazon Firestick",
        "title": "How to set up IPTV on an Amazon Firestick or Fire TV",
        "intro": "The Firestick is the device we recommend most often: cheap, fast enough for 4K on the newer models, "
                 "and it works on any TV with an HDMI port.",
        "app": "IPTV Smarters Pro or TiviMate (via Downloader)",
        "steps": [
            "On your Firestick go to <strong>Settings → My Fire TV → Developer Options</strong> and turn on <strong>Apps from Unknown Sources</strong>.",
            "From the home screen, search for the <strong>Downloader</strong> app and install it.",
            "Open Downloader and enter the download URL we send you for the player app, then press <strong>Go</strong>.",
            "When the file downloads, choose <strong>Install</strong>, then <strong>Done</strong>, then delete the installer file to save space.",
            "Open the player, choose <strong>Add user → Login with Xtream Codes API</strong> and enter the username, password and portal URL from your activation email.",
            "Let the channels and the TV guide load, then start watching.",
        ],
        "tips": [
            "A Fire TV Stick 4K or 4K Max handles 4K channels comfortably; the basic Lite model is best kept to HD.",
            "Restart the stick once a week — it clears the cache and prevents most 'suddenly buffering' complaints.",
            "Do not run a VPN and a low-power stick together unless you need to; it costs you decoding headroom.",
        ],
    },
    "android": {
        "icon": "android", "name": "Android TV box & phone",
        "title": "How to set up IPTV on Android TV, a box or a phone",
        "intro": "Android is the most flexible platform for IPTV. Anything running Android 7 or newer works — "
                 "phones, tablets, TV boxes, NVIDIA Shield and Google TV devices.",
        "app": "TiviMate or IPTV Smarters Pro",
        "steps": [
            "Open the <strong>Google Play Store</strong> on your device.",
            "Search for <strong>TiviMate</strong> (best for TV boxes) or <strong>IPTV Smarters Pro</strong> (best for phones) and install it.",
            "Open the app and choose <strong>Add playlist → Xtream Codes</strong> (TiviMate) or <strong>Login with Xtream Codes API</strong> (Smarters).",
            "Enter the portal URL, username and password from your activation message.",
            "Give the playlist a name and let the channel list and EPG download.",
            "Optional: in TiviMate, open <strong>Settings → Playback</strong> and set the decoder to <em>Hardware</em> for smoother 4K.",
        ],
        "tips": [
            "NVIDIA Shield and Google TV Streamer give the best picture on large screens.",
            "Very cheap no-name Android boxes often have too little RAM for 4K — 2 GB is the practical minimum.",
            "On a phone, switch the player to <em>Software decoder</em> if a specific channel shows a green screen.",
        ],
    },
    "iphone-ipad": {
        "icon": "apple", "name": "iPhone, iPad & Apple TV",
        "title": "How to set up IPTV on iPhone, iPad and Apple TV",
        "intro": "On Apple devices everything is installed straight from the App Store — no sideloading, no developer "
                 "settings, nothing unusual.",
        "app": "IPTV Smarters Pro, Smarters Player Lite or GSE Smart IPTV",
        "steps": [
            "Open the <strong>App Store</strong> on your iPhone, iPad or Apple TV.",
            "Search for <strong>Smarters Player Lite</strong> or <strong>GSE Smart IPTV</strong> and install it.",
            "Open the app and choose <strong>Xtream Codes API</strong> as the login type.",
            "Enter the portal URL, username and password we sent you, and name the playlist.",
            "Wait for the channels and the TV guide to load.",
            "On Apple TV, use the Siri Remote to open <strong>Settings → Player</strong> and enable hardware decoding.",
        ],
        "tips": [
            "AirPlay from an iPhone to a TV works, but a direct Apple TV install is far more stable.",
            "Turn off Low Power Mode while streaming — it throttles the decoder and causes stutter.",
            "If a channel will not open on iOS but works elsewhere, switch the player's stream format to HLS.",
        ],
    },
    "pc-mac": {
        "icon": "laptop", "name": "PC, Mac & browser",
        "title": "How to watch IPTV on a PC, Mac or in your browser",
        "intro": "On a computer you have two good options: VLC (simple, no account needed) or a dedicated desktop "
                 "IPTV player with a proper TV guide.",
        "app": "VLC Media Player, MyIPTV Player or the web player",
        "steps": [
            "Download and install <strong>VLC Media Player</strong> from videolan.org — it is free and runs on Windows, macOS and Linux.",
            "Ask us for your <strong>M3U playlist URL</strong> (we send the Xtream Codes details by default).",
            "In VLC open <strong>Media → Open Network Stream</strong>, paste the M3U URL and press <strong>Play</strong>.",
            "Open <strong>View → Playlist</strong> to browse the channel list.",
            "For a proper TV guide, install <strong>MyIPTV Player</strong> (Windows) instead and add the same playlist plus the EPG URL.",
            "Alternatively, ask us for the web player link and sign in from any modern browser.",
        ],
        "tips": [
            "VLC has no TV guide — use MyIPTV Player or the web player if you want an EPG.",
            "On a Mac, IINA is a good alternative to VLC and handles 4K HEVC more smoothly.",
            "Wired Ethernet beats Wi-Fi, especially on a laptop that is also downloading in the background.",
        ],
    },
    "mag-box": {
        "icon": "devices", "name": "MAG & Enigma2 box",
        "title": "How to set up IPTV on a MAG, Formuler or Enigma2 box",
        "intro": "Set-top boxes such as MAG, Formuler, Zgemma and Dreambox connect using your box's MAC address "
                 "rather than a username and password.",
        "app": "Built-in portal (MAG / Formuler) or an Enigma2 playlist",
        "steps": [
            "Switch the box on and open <strong>Settings → System Settings → Servers → Portals</strong>.",
            "Find the <strong>MAC address</strong> of your box (it is also printed on the sticker underneath) and send it to us on WhatsApp.",
            "We register the MAC on our panel and confirm when it is live.",
            "Back on the box, enter the <strong>Portal URL</strong> we gave you into <em>Portal 1 URL</em> and give it a name.",
            "Save, then choose <strong>Restart Portal</strong> from the system menu.",
            "The channel list loads automatically when the box comes back up.",
        ],
        "tips": [
            "Enigma2 receivers use an M3U playlist or an Xtream plugin instead of a portal — tell us which model you have.",
            "If the portal is blank after a restart, check the box's date and time are set to automatic.",
            "Keep the box on a wired connection; MAG hardware has weak Wi-Fi radios.",
        ],
    },
}


def build_setup():
    cards = ""
    for slug, g in SETUP_GUIDES.items():
        cards += f"""<a href="/setup/{slug}" class="card card--hover">
      <span class="card__icon">{icon(g['icon'])}</span>
      <h3>{g['name']}</h3><p>{g['intro'][:110]}…</p>
      <span class="link-arrow small" style="margin-top:14px">Open guide {icon('arrow')}</span>
    </a>"""

    body = pagehead(
        "Setup guides",
        'Up and running in <span class="grad">about five minutes.</span>',
        "Pick your device and follow the steps. If you get stuck at any point, message us on WhatsApp — "
        "we will walk you through it, free of charge.",
        crumbs=[("/", "Home"), (None, "Setup")],
    ) + f"""
<section class="section--tight"><div class="wrap"><div class="grid g-3 reveal">{cards}</div></div></section>

<section class="section section--alt">
  <div class="wrap-narrow">
    <div class="section-head reveal">
      <span class="eyebrow">Before you start</span>
      <h2 class="d2">Three things worth checking</h2>
    </div>
    <div class="grid g-3 reveal">
      <div class="card"><span class="card__icon">{icon('zap')}</span><h3>Your speed</h3>
        <p>Around 15 Mbps for Full HD and 25 Mbps or more for 4K. Run a speed test on the device itself, not your phone.</p></div>
      <div class="card"><span class="card__icon">{icon('devices')}</span><h3>Your connection</h3>
        <p>Wired Ethernet is noticeably more stable than Wi-Fi for live sport. Use it if the cable can reach.</p></div>
      <div class="card"><span class="card__icon">{icon('doc')}</span><h3>Your details</h3>
        <p>Keep the activation message handy — you will need the portal URL, username and password.</p></div>
    </div>
  </div>
</section>

""" + cta_band('Stuck? <span class="grad">We will do it with you.</span>',
               "Send us a message and a member of the team will walk you through the setup on your device.",
               primary="Get help on WhatsApp", secondary=("/faq", "Read the FAQ"))

    write("/setup", page("/setup",
          f"IPTV Setup Guides — Smart TV, Firestick, Android, Apple | {BRAND}",
          "Step-by-step IPTV setup guides for Samsung and LG Smart TVs, Amazon Firestick, Android boxes, "
          "iPhone, iPad, Apple TV, PC, Mac and MAG boxes.",
          body, active="/setup"), priority="0.8")

    for slug, g in SETUP_GUIDES.items():
        steps = "".join(f"<li><span>{s}</span></li>" for s in g["steps"])
        tips = "".join(f"<li><span>{t}</span></li>" for t in g["tips"])
        others = "".join(
            f'<a href="/setup/{s2}" class="mini-plan"><b>{g2["name"]}</b>{icon("arrow")}</a>'
            for s2, g2 in SETUP_GUIDES.items() if s2 != slug)

        ld = json.dumps({
            "@context": "https://schema.org", "@type": "HowTo", "name": g["title"],
            "description": g["intro"],
            "step": [{"@type": "HowToStep", "position": i + 1,
                      "text": re.sub("<[^>]+>", "", s)} for i, s in enumerate(g["steps"])],
        }, ensure_ascii=False)

        body = pagehead(
            "Setup guide", g["title"], g["intro"],
            crumbs=[("/", "Home"), ("/setup", "Setup"), (None, g["name"])],
        ) + f"""
<section class="section--tight">
  <div class="wrap-narrow">
    <div class="callout reveal"><b>Recommended app:</b> {g['app']}. It is free — we will send you the exact
      download link with your activation details.</div>
  </div>
</section>

<section class="section" style="padding-top:20px">
  <div class="wrap-narrow prose reveal">
    <h2>Step by step</h2>
    <ol>{steps}</ol>
    <h2>Tips from our support team</h2>
    <ul>{tips}</ul>
    <h2>If something goes wrong</h2>
    <p>Nine times out of ten a problem at this stage is one of three things: a typo in the portal URL, the wrong
      login type selected in the app, or the box not having finished downloading the channel list. Close the app
      completely, reopen it and give it a minute before trying anything else.</p>
    <p>If it still will not play, <a href="#" data-wa="Hi {BRAND}! I need help setting up on {g['name']}.">message us on WhatsApp</a>
      with a photo of the screen. Support is available 24/7 and setup help is free.</p>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap-narrow">
    <h2 class="d3 center reveal" style="margin-bottom:24px">Setting up a different device?</h2>
    <div class="reveal">{others}</div>
  </div>
</section>

""" + cta_band('Not a customer yet?', "Start with a free trial and test it on this exact device before you pay.",
               primary="Order on WhatsApp", secondary=("/free-trial", "Start a free trial"))

        write(f"/setup/{slug}", page(f"/setup/{slug}",
              f"{g['title']} | {BRAND}",
              f"{g['intro'][:150]}",
              body, active="/setup", jsonld=ld), priority="0.7")


# ===========================================================================
# 5. REVIEWS
# ===========================================================================
def build_reviews():
    body = pagehead(
        "Reviews",
        'What our customers <span class="grad">actually say.</span>',
        "Every review on this page comes from a real Streamly4K customer. We do not write them ourselves and "
        "we do not buy them.",
        crumbs=[("/", "Home"), (None, "Reviews")],
    ) + f"""
<section class="section--tight">
  <div class="wrap">
    <!-- ==================================================================
         REVIEWS
         Add your real customer reviews in /assets/js/reviews.js
         Do NOT invent reviews: publishing fake testimonials is illegal
         advertising in the US (FTC Act §5) and in the UK/EU, and review
         platforms remove businesses that do it.
         ================================================================== -->
    <div class="reviews reveal" id="review-grid"></div>
    <div id="review-empty" class="card center reveal" style="max-width:640px;margin-inline:auto;padding:40px">
      <span class="card__icon mx-auto">{icon('chat')}</span>
      <h3 class="d4">We are collecting reviews right now</h3>
      <p style="margin-top:10px">This page fills up as customers send feedback. If you are already with us and the
        service is doing its job, we would be glad if you left a few honest words.</p>
      <div class="row row-center" style="margin-top:22px">
        <a href="#" data-wa="Hi {BRAND}! I'd like to leave a review." class="btn btn--primary">Leave a review</a>
        <a href="/free-trial" class="btn btn--outline">Try it free first</a>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Instead of a number</span>
      <h2 class="d2">Judge us on <span class="grad">what we promise.</span></h2>
      <p class="lede">Anyone can print a rating on a homepage. These are things you can actually hold us to.</p>
    </div>
    <div class="grid g-4 reveal">
      <div class="card"><span class="card__icon">{icon('clock')}</span><h3>24-hour free trial</h3>
        <p>Test the channels and the stability on your own connection before a penny changes hands.</p></div>
      <div class="card"><span class="card__icon">{icon('shield')}</span><h3>7-day money back</h3>
        <p>If the service does not work properly and we cannot fix it, you get your money back.</p></div>
      <div class="card"><span class="card__icon">{icon('refresh')}</span><h3>No auto-renewal</h3>
        <p>One payment, for the term you chose. No card on file, nothing to cancel later.</p></div>
      <div class="card"><span class="card__icon">{icon('headset')}</span><h3>A human, 24/7</h3>
        <p>Real support on WhatsApp — not a ticket queue that answers in three days.</p></div>
    </div>
  </div>
</section>

""" + cta_band('Try it before you trust it.',
               "A free 24-hour trial tells you more than any rating on a website ever could.",
               primary="Start a free trial", secondary=("/pricing", "See plans")) + """
<script src="/assets/js/reviews.js"></script>
<script>
(function(){
  var list = window.S4K_REVIEWS || [];
  var grid = document.getElementById('review-grid');
  var empty = document.getElementById('review-empty');
  if (!list.length) { grid.style.display = 'none'; return; }
  empty.style.display = 'none';
  grid.innerHTML = list.map(function(r){
    var stars = new Array(Math.max(1, Math.min(5, r.stars || 5)) + 1).join(
      '<svg viewBox="0 0 24 24" fill="currentColor"><path d="m12 2 2.9 6.3 6.9.8-5.1 4.6 1.4 6.8L12 17.2 5.9 20.5l1.4-6.8L2.2 9.1l6.9-.8L12 2Z"/></svg>');
    var initials = (r.name || '?').split(' ').map(function(w){return w[0];}).join('').slice(0,2).toUpperCase();
    return '<article class="review"><div class="review__stars">' + stars + '</div>' +
           '<p>' + r.text + '</p>' +
           '<div class="review__who"><span class="review__av">' + initials + '</span>' +
           '<span><b>' + r.name + '</b><span>' + (r.meta || '') + '</span></span></div></article>';
  }).join('');
})();
</script>"""

    write("/reviews", page("/reviews",
          f"Customer Reviews | {BRAND}",
          "Real customer reviews of Streamly4K, plus the guarantees you can hold us to: a free 24-hour trial, "
          "a 7-day money-back guarantee and 24/7 human support.",
          body), priority="0.6")

    write_raw("assets/js/reviews.js", """/* ==========================================================================
   Streamly4K — customer reviews
   --------------------------------------------------------------------------
   Paste your REAL customer reviews below, one object per review.
   Leave the array empty until you have genuine ones — the reviews page shows
   a clean "collecting reviews" state instead.

   ⚠️  Do not invent reviews or copy them from another site. Publishing fake
       testimonials is illegal advertising in the US (FTC Act §5, and the 2024
       Rule on Consumer Reviews and Testimonials, with civil penalties per
       violation) and in the UK/EU, and review platforms delist businesses
       that do it.

   Format:
   { name: "First L.", meta: "Firestick · Texas", stars: 5,
     text: "What the customer actually wrote." }
   ========================================================================== */

window.S4K_REVIEWS = [
  // { name: "", meta: "", stars: 5, text: "" },
];
""")


# ===========================================================================
# 6. BLOG
# ===========================================================================
BLOG_BODIES = {
    "what-is-iptv": [
        ("What IPTV actually means",
         "<p>IPTV stands for <strong>Internet Protocol Television</strong>. Instead of a signal arriving through a "
          "coaxial cable or a satellite dish, the television picture arrives as data over your normal internet "
          "connection — the same pipe that carries your email and your video calls.</p>"
          "<p>That is the whole idea. Everything else — the apps, the logins, the channel lists — is just plumbing "
          "built on top of it. If you have ever watched a live stream on YouTube, you have already used the "
          "underlying technology.</p>"),
        ("How a subscription works in practice",
         "<p>A provider runs servers that receive channel feeds and re-transmit them to subscribers. You get a set "
          "of login details, you enter those into a player app on your TV, stick or phone, and the app pulls the "
          "channel list and the TV guide from the server.</p>"
          "<ol><li>You order a plan and pay once for the term.</li>"
          "<li>The provider creates a line on their panel and sends you a portal URL, a username and a password.</li>"
          "<li>You install a free player app and enter those details.</li>"
          "<li>The channel list and the electronic programme guide download, and you watch.</li></ol>"),
        ("What it costs, and why",
         "<p>Most credible providers sit somewhere between $8 and $15 a month when you pay for a longer term. "
          "Anything dramatically below that is usually a reseller with no infrastructure of their own who will "
          "disappear in a month; anything far above it is usually a reseller charging a premium for the same feed.</p>"),
        ("Five things to check before you pay",
         "<ul><li><strong>A trial.</strong> Any provider confident in their servers will let you test on your own connection.</li>"
          "<li><strong>A real support channel.</strong> A WhatsApp number answered by a person beats a contact form.</li>"
          "<li><strong>A refund policy in writing.</strong> Not a promise in a chat message.</li>"
          "<li><strong>No auto-renewal.</strong> You should not have to cancel anything.</li>"
          "<li><strong>Honest answers.</strong> Ask whether they carry a specific channel. A provider who says "
          "'yes, everything' to every question is not being straight with you.</li></ul>"),
        ("Is it legal?",
         "<p>The technology is entirely legal — it is how most broadcasters now deliver their own apps. What matters "
          "legally is the licensing behind the content, and that varies by provider and by country. Rules differ "
          "significantly between jurisdictions, and it is worth understanding the position where you live before you "
          "subscribe to any service. We are not lawyers and this is not legal advice.</p>"),
    ],
    "iptv-vs-cable-cost": [
        ("The stack most households end up with",
         "<p>Almost nobody sets out to pay for six subscriptions. It happens one at a time: a live-TV package for "
          "sport, one streaming app for a series, another for the kids, a third because a film was only there.</p>"
          "<p>Using public September 2026 list prices, a fairly ordinary US stack looks like this: a live-TV base "
          "plan at $82.99, Sunday Ticket at $40.00, Netflix Standard at $19.99, HBO Max Standard at $18.49, "
          "Disney+ Premium at $18.99 and Peacock Premium at $12.99. That is $193.45 a month, or $2,321.40 a year, "
          "spread across six separate payments every month.</p>"),
        ("What the same money buys as one subscription",
         "<p>A 12-month IPTV subscription at $99.99 works out at $8.33 a month. Against the stack above, that is a "
          "difference of about $2,221 over a year — roughly the price of a decent television, every year, for "
          "something you were already paying for.</p>"
          "<p>It is worth being precise about what this comparison is and is not. It is a price comparison, not a "
          "like-for-like content comparison: the catalogues are not identical, some originals only exist on their "
          "home platform, and list prices change. What it does show is the scale of what a bundled subscription "
          "replaces.</p>"),
        ("The hidden costs people forget",
         "<ul><li><strong>Equipment rental.</strong> Cable boxes and DVR fees quietly add $10–$25 a month.</li>"
          "<li><strong>Regional sports fees.</strong> Often $10–$15 on top of the advertised price.</li>"
          "<li><strong>Annual price rises.</strong> Nearly every major service raised prices in the last two years.</li>"
          "<li><strong>Contract exit fees.</strong> Still common with traditional cable.</li></ul>"),
        ("Where cable and the big apps still win",
         "<p>Honesty is more useful than a sales pitch. Traditional providers give you a single company to hold "
          "accountable, guaranteed 4K on their flagship channels, and exclusive originals you cannot get elsewhere. "
          "If your household watches two shows and one is an exclusive, an app subscription is probably better value "
          "than anything else. The arithmetic only turns decisively when you are paying for several services at once.</p>"),
    ],
    "stop-iptv-buffering": [
        ("Start with the honest diagnosis",
         "<p>When a stream stutters, most people blame the provider first. In our support queue, server-side problems "
          "account for a small minority of buffering complaints. The overwhelming majority come down to the local "
          "network, the device, or the player settings — in roughly that order.</p>"
          "<p>Work through the list below in order. Do not skip ahead: the fixes are ordered by how often they turn "
          "out to be the cause.</p>"),
        ("The nine fixes, in order",
         "<ol><li><strong>Run a speed test on the streaming device itself</strong>, not your phone. You want 15 Mbps "
          "for Full HD and 25 Mbps+ for 4K, with a stable result rather than a high peak.</li>"
          "<li><strong>Switch to wired Ethernet.</strong> This single change resolves more buffering than everything "
          "else combined, particularly for live sport at peak times.</li>"
          "<li><strong>Move to the 5 GHz Wi-Fi band</strong> if a cable is impossible. 2.4 GHz is congested in most "
          "apartment buildings.</li>"
          "<li><strong>Restart the router and the streaming device.</strong> Unplug both for a full 30 seconds.</li>"
          "<li><strong>Clear the player app's cache</strong> and delete any old playlists you are no longer using.</li>"
          "<li><strong>Switch the decoder</strong> between hardware and software in the player settings. Some channels "
          "encode in a format your chip handles poorly.</li>"
          "<li><strong>Increase the buffer size</strong> in the player — 3 to 5 seconds smooths over small network dips.</li>"
          "<li><strong>Close background apps</strong> on the device, and pause any large downloads on the network.</li>"
          "<li><strong>Test a VPN.</strong> Some ISPs throttle sustained streaming traffic; if a VPN improves things "
          "dramatically, that is your answer.</li></ol>"),
        ("How to tell if it really is the server",
         "<p>Two quick tests. First, try a completely different channel from a different country — if that plays "
          "perfectly, your connection and device are fine and the issue is with one source. Second, try the same "
          "channel on your phone over mobile data. If it is smooth on mobile data and stutters on your home Wi-Fi, "
          "the problem is your network, not the provider.</p>"
          "<p>If both tests point at the server, message support with the channel name and the time. A good provider "
          "can usually move you to a different source within minutes.</p>"),
        ("The thing nobody wants to hear",
         "<p>If your household is streaming 4K while someone else is on a video call and a console is downloading a "
          "60 GB update, no provider on earth can deliver a clean picture. Buffering is often a bandwidth budget "
          "problem rather than a technical fault.</p>"),
    ],
    "best-device-for-iptv": [
        ("The short answer",
         "<p>For most people, a <strong>Fire TV Stick 4K Max</strong> is the best balance of price and performance. "
          "For anyone who wants the best possible picture on a large television and does not mind paying for it, an "
          "<strong>NVIDIA Shield TV Pro</strong> is still the strongest device you can buy.</p>"),
        ("Firestick: the default recommendation",
         "<p><strong>Good:</strong> cheap, small, works on any HDMI TV, supports every major player app, and the 4K Max "
          "has enough headroom for 4K streams with a VPN running.</p>"
          "<p><strong>Less good:</strong> limited storage, and the basic Lite model struggles above 1080p. Amazon's "
          "interface pushes its own content hard.</p>"),
        ("Android TV boxes: flexible, but buy carefully",
         "<p><strong>Good:</strong> TiviMate on Android TV is the best IPTV experience available anywhere — proper "
          "recording, multi-view, and a genuinely good programme guide.</p>"
          "<p><strong>Less good:</strong> the market is full of $25 boxes with 1 GB of RAM and fake specifications. "
          "If you go this route, buy a known brand. 2 GB of RAM is the practical minimum, 4 GB is comfortable.</p>"),
        ("Smart TV apps: convenient, rarely the best",
         "<p><strong>Good:</strong> no extra box, no extra remote, no extra HDMI port.</p>"
          "<p><strong>Less good:</strong> television processors are slow, app choice is restricted to what is in the "
          "manufacturer's store, and apps get dropped when a TV falls out of support. Fine as a starting point; "
          "most people end up adding a stick within a year.</p>"),
        ("What to avoid",
         "<ul><li>Pre-loaded boxes sold with a subscription 'included' — you are buying someone else's margin and "
          "no support.</li>"
          "<li>Anything advertised with specifications that seem impossible for the price.</li>"
          "<li>Very old hardware. A 2015 box will not decode modern 4K streams, whatever the seller says.</li></ul>"),
    ],
    "watch-nfl-without-cable": [
        ("What you are actually trying to solve",
         "<p>NFL rights are split across more parties than any other US sport, which is why no single subscription "
          "covers everything. Before spending money, work out which of these you actually need: your local team's "
          "games, out-of-market games, national primetime games, or the playoffs.</p>"),
        ("The routes, and what each one costs",
         "<ul><li><strong>An antenna.</strong> Free, once you buy it. Covers local CBS and FOX games in HD, which for "
          "many households is most of what they watch.</li>"
          "<li><strong>A live-TV streaming service.</strong> Around $83 a month for the base tier. Covers the national "
          "networks and ESPN.</li>"
          "<li><strong>Sunday Ticket.</strong> Roughly $40 a month during the season for out-of-market games.</li>"
          "<li><strong>Individual app subscriptions</strong> for the streaming-exclusive games.</li>"
          "<li><strong>An IPTV subscription.</strong> Bundles the channels into one line at a fraction of the price, "
          "with the trade-offs discussed below.</li></ul>"),
        ("The trade-offs, stated plainly",
         "<p>An antenna is the cheapest reliable option and nobody should skip it. Live-TV streaming services give you "
          "the most predictable quality and a company to complain to. IPTV gives you the widest coverage for the least "
          "money, but stream quality depends on the provider and the source, and licensing arrangements vary — it is "
          "worth understanding the position in your own country before subscribing to any service.</p>"),
        ("What we would do",
         "<p>Buy an antenna for the local games regardless — it costs $30 once and it never buffers. Then add whichever "
          "single subscription covers the gap for your household, rather than stacking three that overlap.</p>"),
    ],
    "iptv-buyers-checklist": [
        ("Why a checklist matters here",
         "<p>IPTV is a market with very low barriers to entry. Anyone can buy a reseller panel on a Tuesday and have a "
          "website live by Thursday. The difference between a provider who will still be answering messages in six "
          "months and one who will not is usually visible before you pay, if you know what to look for.</p>"),
        ("The ten questions",
         "<ol><li><strong>Will you give me a trial?</strong> A no here is the end of the conversation.</li>"
          "<li><strong>Do you carry this specific channel?</strong> Name one. Vague answers are a warning.</li>"
          "<li><strong>What happens if a stream goes down at kick-off?</strong> Listen for a process, not a promise.</li>"
          "<li><strong>Is there a written refund policy?</strong> Ask for the page, not a reassurance.</li>"
          "<li><strong>Does it auto-renew?</strong> It should not, and you should not need to cancel anything.</li>"
          "<li><strong>How do I contact you at 11pm on a Sunday?</strong> The answer should be a real channel.</li>"
          "<li><strong>How many devices does my plan cover at once?</strong> Get the number in writing.</li>"
          "<li><strong>Can I move my line to a new device later?</strong> Some providers charge for this.</li>"
          "<li><strong>What happens to my details?</strong> A provider with a privacy policy has thought about it.</li>"
          "<li><strong>What do you not carry?</strong> The most revealing question on this list.</li></ol>"),
        ("Red flags worth walking away from",
         "<ul><li>A price far below everyone else, with no explanation.</li>"
          "<li>Reviews that all appeared in the same week and read alike.</li>"
          "<li>Pressure to pay immediately in a way that cannot be reversed.</li>"
          "<li>No refund policy anywhere on the site.</li>"
          "<li>A provider who claims to carry absolutely everything, everywhere, always.</li></ul>"),
        ("And one thing in their favour",
         "<p>If a provider tells you honestly that they do not carry something, or that your internet connection is "
          "not fast enough for what you want, take it as a good sign. It is a great deal easier to promise everything "
          "than to keep a customer who was told the truth first.</p>"),
    ],
}


def build_blog():
    cards = ""
    for p in data.BLOG:
        cards += f"""<a href="/blog/{p['slug']}" class="postcard">
      <div class="postcard__img">{icon(p['icon'])}</div>
      <div class="postcard__body">
        <div class="postcard__meta"><span>{p['cat']}</span><span>·</span><span>{p['read']} read</span></div>
        <h3>{p['title']}</h3><p>{p['excerpt']}</p>
        <span class="link-arrow">Read article {icon('arrow')}</span>
      </div>
    </a>"""

    body = pagehead(
        "Blog",
        'Straight answers about <span class="grad">streaming TV.</span>',
        "Guides, comparisons and troubleshooting from the people who answer the support messages. "
        "No filler, no affiliate padding.",
        crumbs=[("/", "Home"), (None, "Blog")],
    ) + f"""
<section class="section--tight"><div class="wrap"><div class="grid g-3 reveal">{cards}</div></div></section>
""" + cta_band('Questions the blog did not answer?',
               "Message us — we would rather talk you out of the wrong plan than sell you one.",
               primary="Ask on WhatsApp", secondary=("/faq", "Read the FAQ"))

    write("/blog", page("/blog", f"Blog — IPTV Guides, Comparisons & Fixes | {BRAND}",
          "Practical IPTV guides from the Streamly4K support team: how IPTV works, what it really costs "
          "versus cable, how to stop buffering and which device to buy.",
          body), priority="0.7", freq="weekly")

    for p in data.BLOG:
        secs = BLOG_BODIES.get(p["slug"], [])
        prose = "".join(f"<h2>{h}</h2>{b}" for h, b in secs)
        related = [q for q in data.BLOG if q["slug"] != p["slug"]][:3]
        rel = "".join(
            f'<a href="/blog/{q["slug"]}" class="mini-plan"><b>{q["title"]}</b>{icon("arrow")}</a>'
            for q in related)

        ld = json.dumps({
            "@context": "https://schema.org", "@type": "BlogPosting",
            "headline": p["title"], "description": p["excerpt"],
            "datePublished": p["date"], "dateModified": p["date"],
            "author": {"@type": "Organization", "name": BRAND},
            "publisher": {"@type": "Organization", "name": BRAND,
                          "logo": {"@type": "ImageObject", "url": BASE + "/favicon.svg"}},
            "mainEntityOfPage": f"{BASE}/blog/{p['slug']}",
        }, ensure_ascii=False)

        body = f"""<section class="pagehead">
  <div class="wrap-narrow">
    <nav class="crumbs"><a href="/">Home</a><span>/</span><a href="/blog">Blog</a><span>/</span><span>{p['cat']}</span></nav>
    <span class="eyebrow">{p['cat']}</span>
    <h1 class="d2" style="margin-top:14px">{p['title']}</h1>
    <p class="lede center">{p['excerpt']}</p>
    <div class="row row-center muted small" style="margin-top:20px;gap:16px">
      <span>{p['date_h']}</span><span>·</span><span>{p['read']} read</span><span>·</span><span>{BRAND} team</span>
    </div>
  </div>
</section>

<section class="section" style="padding-top:20px">
  <div class="wrap-narrow prose reveal">{prose}
    <div class="callout" style="margin-top:44px"><b>Want to test this yourself?</b> We offer a free 24-hour trial
      so you can check the channels and the stability on your own connection before paying anything.
      <a href="/free-trial">Start a free trial →</a></div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap-narrow">
    <h2 class="d3 center reveal" style="margin-bottom:24px">Keep reading</h2>
    <div class="reveal">{rel}</div>
  </div>
</section>

""" + cta_band('Ready to try it?', "Plans from $39.99, activated in minutes, cancel nothing because nothing renews.")

        write(f"/blog/{p['slug']}", page(f"/blog/{p['slug']}",
              f"{p['title']} | {BRAND}", p["excerpt"], body,
              active="/blog", jsonld=ld, og_type="article"), priority="0.6")


# ===========================================================================
# 7. FAQ / CONTACT / ORDER / TRIAL / THANK YOU
# ===========================================================================
def build_support_pages():
    all_faq = data.FAQ_HOME + data.FAQ_EXTRA
    body = pagehead("Help centre", 'Questions, <span class="grad">answered honestly.</span>',
                    "If your question is not here, message us — we answer within minutes, day or night.",
                    crumbs=[("/", "Home"), (None, "FAQ")]) + \
        faq_block(all_faq, title="Everything people ask", eyebrow="FAQ",
                  lede="Ordering, setup, devices, payment and support.") + \
        cta_band('Still not sure?', "Ask us anything before you order. We would rather answer ten questions than "
                                    "refund one order.", primary="Ask on WhatsApp", secondary=("/pricing", "See plans"))
    write("/faq", page("/faq", f"FAQ — IPTV Questions Answered | {BRAND}",
          "Answers to the most common questions about Streamly4K: activation time, devices, free trial, "
          "payment, refunds, VPNs and support.",
          body, jsonld=faq_jsonld(all_faq)), priority="0.7")

    # ---- Contact ----
    body = pagehead("Contact", 'We answer in <span class="grad">minutes, not days.</span>',
                    "Support runs 24 hours a day, every day of the year. WhatsApp is the fastest way to reach us.",
                    crumbs=[("/", "Home"), (None, "Contact")]) + f"""
<section class="section--tight">
  <div class="wrap">
    <div class="grid g-3 reveal">
      <a href="#" data-wa="Hi {BRAND}!" class="card card--hover"><span class="card__icon">{icon('wa')}</span>
        <h3>WhatsApp</h3><p><span data-wa-text>+1 (661) 541-3954</span> — the fastest route. Typical reply time is a few minutes, 24/7.</p>
        <span class="link-arrow small" style="margin-top:14px">Open chat {icon('arrow')}</span></a>
      <a href="#" data-mail class="card card--hover"><span class="card__icon">{icon('mail')}</span>
        <h3>Email</h3><p><span data-mail-text>support@streamly4k.com</span> — best for invoices and refunds.</p>
        <span class="link-arrow small" style="margin-top:14px">Send an email {icon('arrow')}</span></a>
      <a href="/setup" class="card card--hover"><span class="card__icon">{icon('doc')}</span>
        <h3>Setup guides</h3><p>Step-by-step instructions for every device we support.</p>
        <span class="link-arrow small" style="margin-top:14px">Browse guides {icon('arrow')}</span></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap-narrow">
    <div class="card reveal" style="padding:clamp(26px,4vw,44px)">
      <h2 class="d3">Send us a message</h2>
      <p class="muted" style="margin-top:8px">Fill this in and it opens WhatsApp with your message ready to send.</p>
      <form id="order-form" style="margin-top:26px">
        <div class="field"><label class="label" for="c-name">Your name</label>
          <input class="input" id="c-name" name="Name" placeholder="Jordan" required></div>
        <div class="field"><label class="label" for="c-topic">What is it about?</label>
          <select class="select" id="c-topic" name="Topic">
            <option>A question before ordering</option><option>Free trial</option>
            <option>Setup help</option><option>A channel or stream problem</option>
            <option>Billing, invoice or refund</option><option>Something else</option>
          </select></div>
        <div class="field"><label class="label" for="c-msg">Your message</label>
          <textarea class="textarea" id="c-msg" name="Message" rows="4" placeholder="Tell us what you need…" required></textarea></div>
        <button type="submit" class="btn btn--primary btn--block" style="margin-top:22px">
          {icon('wa')} Send on WhatsApp</button>
        <p class="xsmall muted center" style="margin-top:12px">Nothing is stored on this website — the form simply
          opens WhatsApp with your message prepared.</p>
      </form>
    </div>
  </div>
</section>"""
    write("/contact", page("/contact", f"Contact Us — 24/7 Support | {BRAND}",
          "Contact Streamly4K support on WhatsApp or by email, 24 hours a day, every day. "
          "Help with ordering, setup, streams, invoices and refunds.",
          body), priority="0.6")

    # ---- Order ----
    body = pagehead("Order", 'Order in <span class="grad">under a minute.</span>',
                    "Pick your plan, tell us your device, and we send an invoice with the payment options. "
                    "No payment is taken on this website.",
                    crumbs=[("/", "Home"), (None, "Order")]) + \
        S.builder_section(heading=False) + f"""
<section class="section section--alt">
  <div class="wrap-narrow">
    <div class="card reveal" style="padding:clamp(26px,4vw,44px)">
      <h2 class="d3">Prefer a form?</h2>
      <p class="muted" style="margin-top:8px">Fill this in and we will send your invoice by email and WhatsApp.</p>
      <form id="order-form" style="margin-top:26px">
        <div class="grid g-2" style="gap:18px">
          <div class="field" style="margin:0"><label class="label" for="o-name">Full name</label>
            <input class="input" id="o-name" name="Name" required></div>
          <div class="field" style="margin:0"><label class="label" for="o-mail">Email</label>
            <input class="input" id="o-mail" name="Email" type="email" required></div>
        </div>
        <div class="grid g-2" style="gap:18px;margin-top:18px">
          <div class="field" style="margin:0"><label class="label" for="o-plan">Plan</label>
            <select class="select" id="o-plan" name="Plan">
              <option>12 Months — $99.99</option><option>6 Months — $69.99</option><option>3 Months — $39.99</option>
            </select></div>
          <div class="field" style="margin:0"><label class="label" for="o-dev">Devices at the same time</label>
            <select class="select" id="o-dev" name="Devices">
              <option>1 device</option><option>2 devices</option><option>3 devices</option>
              <option>4 devices</option><option>5 devices</option>
            </select></div>
        </div>
        <div class="field"><label class="label" for="o-what">What will you watch on?</label>
          <select class="select" id="o-what" name="Device">
            <option>Samsung or LG Smart TV</option><option>Amazon Firestick / Fire TV</option>
            <option>Android TV box or phone</option><option>iPhone, iPad or Apple TV</option>
            <option>PC, Mac or browser</option><option>MAG or Enigma2 box</option><option>Not sure yet</option>
          </select></div>
        <div class="field"><label class="label" for="o-note">Anything we should know? (optional)</label>
          <textarea class="textarea" id="o-note" name="Notes" rows="3"
            placeholder="A channel you need, a country, a preferred payment method…"></textarea></div>
        <button type="submit" class="btn btn--primary btn--block" style="margin-top:22px">
          {icon('wa')} Send my order</button>
        <p class="xsmall muted center" style="margin-top:12px">This opens WhatsApp with your order details ready to send.
          Nothing is charged until you receive and pay an invoice.</p>
      </form>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid g-4 reveal">
      <div class="card"><span class="card__icon">{icon('clock')}</span><h3>5–15 minutes</h3><p>Typical activation time once payment is confirmed.</p></div>
      <div class="card"><span class="card__icon">{icon('lock')}</span><h3>No card stored</h3><p>You pay an invoice. We never hold your card details.</p></div>
      <div class="card"><span class="card__icon">{icon('refresh')}</span><h3>No auto-renewal</h3><p>One payment for the term. Nothing to cancel.</p></div>
      <div class="card"><span class="card__icon">{icon('shield')}</span><h3>7-day guarantee</h3><p>Money back if we cannot make it work for you.</p></div>
    </div>
  </div>
</section>"""
    write("/order", page("/order", f"Order Your Subscription | {BRAND}",
          "Order a Streamly4K subscription: choose your term and devices, send your order on WhatsApp, "
          "and get activated in 5–15 minutes. No payment taken on the website.",
          body), priority="0.8")

    # ---- Free trial ----
    body = pagehead("Free trial", 'Try it for <span class="grad">24 hours. Free.</span>',
                    "A real trial on your own connection and your own device — the only way to know whether a "
                    "service is right for you. No card, no commitment.",
                    crumbs=[("/", "Home"), (None, "Free trial")],
                    cta=f'<div class="row row-center" style="margin-top:28px">'
                        f'<a href="#" data-wa="Hi {BRAND}! I would like the free 24-hour trial. My device is: " '
                        f'class="btn btn--primary btn--lg">{icon("wa")} Request my free trial</a></div>') + f"""
<section class="section--tight">
  <div class="wrap">
    <div class="grid g-3 reveal">
      <div class="card"><span class="card__icon">{icon('chat')}</span><h3>1. Message us</h3>
        <p>Tell us which device you want to test on — Firestick, Smart TV, phone, whatever you have.</p></div>
      <div class="card"><span class="card__icon">{icon('zap')}</span><h3>2. Get your line</h3>
        <p>We send trial login details and the right setup guide, usually within a few minutes.</p></div>
      <div class="card"><span class="card__icon">{icon('eye')}</span><h3>3. Test properly</h3>
        <p>Check your channels, watch something live at peak time, and see how it holds up.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap-narrow prose reveal">
    <h2>What to actually test</h2>
    <p>Most people load the trial, see that channels appear and stop there. That tells you almost nothing. In the
      24 hours you have, do these five things instead:</p>
    <ol>
      <li>Watch a live event at peak time — that is when servers are under load.</li>
      <li>Open the specific channels you care about most, not just the first one in the list.</li>
      <li>Check the TV guide fills in properly for those channels.</li>
      <li>Try a 4K stream if 4K matters to you, and watch for five minutes rather than ten seconds.</li>
      <li>Ask support a question and see how long the reply takes.</li>
    </ol>
    <h2>The honest limitations</h2>
    <p>A trial line runs on the same servers as a paid line, but trials are limited to a single device and 24 hours.
      If a specific channel is missing during the trial, tell us — sometimes it is a source we can add, and sometimes
      the honest answer is that we do not carry it.</p>
    <div class="callout"><b>No card, no forms, no small print.</b> We ask for a device type and a WhatsApp number.
      That is the whole process.</div>
  </div>
</section>

""" + cta_band('See it for yourself first.',
               "Twenty-four hours on your own connection tells you more than any review page.",
               primary="Request my free trial", secondary=("/pricing", "See plans"))
    write("/free-trial", page("/free-trial", f"Free 24-Hour IPTV Trial — No Card Needed | {BRAND}",
          "Test Streamly4K free for 24 hours on your own device and connection. No card, no commitment. "
          "Request your trial on WhatsApp and get login details in minutes.",
          body), priority="0.8")

    # ---- Thank you ----
    body = f"""<section class="pagehead" style="padding-bottom:80px">
  <div class="wrap-narrow">
    <span class="card__icon mx-auto" style="width:66px;height:66px;border-radius:20px">{icon('check-circle')}</span>
    <h1 class="d2" style="margin-top:20px">Order received. <span class="grad">Welcome aboard.</span></h1>
    <p class="lede center">We have your order. Your invoice is on its way by email and WhatsApp — once payment is
      confirmed, your line is usually live within 5 to 15 minutes.</p>
    <div class="row row-center" style="margin-top:30px">
      <a href="/setup" class="btn btn--primary btn--lg">Get your device ready</a>
      <a href="#" data-wa="Hi {BRAND}! I just placed an order." class="btn btn--outline btn--lg">Message support</a>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap-narrow">
    <div class="grid g-3 reveal">
      <div class="card"><span class="card__icon">{icon('mail')}</span><h3>Check your inbox</h3>
        <p>Including the spam folder. The invoice comes from our support address.</p></div>
      <div class="card"><span class="card__icon">{icon('doc')}</span><h3>Install the app</h3>
        <p>Get ahead: install the player for your device while you wait.</p></div>
      <div class="card"><span class="card__icon">{icon('headset')}</span><h3>We are here</h3>
        <p>Anything at all, message us on WhatsApp. Support runs 24/7.</p></div>
    </div>
  </div>
</section>"""
    write("/thank-you", page("/thank-you", f"Thank You — Order Received | {BRAND}",
          "Thanks for your order. Your invoice is on its way and your subscription will be live shortly.",
          body, bar=False), priority="0.2")


# ===========================================================================
# 8. LEGAL
# ===========================================================================
LEGAL = {
    "terms": ("Terms of Service", "The rules that apply when you buy a subscription from us.", """
<h2>1. Who we are</h2>
<p>{B} ("we", "us") operates the website {D} and sells access to a third-party streaming service as an independent
reseller. We are not a broadcaster, and we are not affiliated with, endorsed by or connected to any channel, network,
studio, streaming platform or device manufacturer referenced on this website.</p>

<h2>2. What you are buying</h2>
<p>You are buying access to a streaming line for a fixed term. Channel line-ups, catalogues and stream sources change
over time and are not guaranteed for any specific channel, event or broadcast. We describe the service as accurately
as we can, and we will always tell you honestly before you order whether we carry something you ask about.</p>

<h2>3. Ordering and payment</h2>
<ul>
<li>No payment is taken on this website. After you place an order we send an invoice with payment instructions.</li>
<li>All prices are shown in US dollars and are one-time payments for the term selected.</li>
<li>There is no automatic renewal and no card is stored. Your line stops at the end of the term unless you choose to extend.</li>
<li>Your subscription becomes active once payment has been confirmed, normally within 5 to 15 minutes.</li>
</ul>

<h2>4. Your responsibilities</h2>
<ul>
<li>Provide accurate contact details so we can deliver your login and support you.</li>
<li>Keep your login details private. Sharing or reselling your line is grounds for termination without refund.</li>
<li>Use no more simultaneous connections than your plan allows.</li>
<li>Ensure your internet connection meets the minimum requirements (around 15 Mbps for HD, 25 Mbps for 4K).</li>
<li>Comply with the laws that apply where you live. You are responsible for your own legal position.</li>
</ul>

<h2>5. Support</h2>
<p>Support is available 24 hours a day by WhatsApp and email. Setup assistance on any supported device is included
at no extra cost. We aim to respond within minutes, but we do not guarantee a specific response time.</p>

<h2>6. Service availability</h2>
<p>We work to keep the service running continuously but we do not guarantee uninterrupted availability. Interruptions
can result from maintenance, source outages, your own internet connection or events beyond our control. Where an
outage is on our side and cannot be resolved, our refund policy applies.</p>

<h2>7. Termination</h2>
<p>We may suspend or terminate a subscription without refund where a customer shares login details, exceeds their
connection limit, attempts to resell access, or abuses our staff. We will always explain the reason.</p>

<h2>8. Limitation of liability</h2>
<p>To the fullest extent permitted by law, our total liability in connection with the service is limited to the amount
you paid for your current subscription term. We are not liable for indirect or consequential losses, including missed
broadcasts. Nothing in these terms limits liability that cannot be limited by law.</p>

<h2>9. Changes</h2>
<p>We may update these terms. The version published on this page at the time of your order is the version that applies
to that order.</p>

<h2>10. Contact</h2>
<p>Questions about these terms: <a href="#" data-mail><span data-mail-text></span></a>.</p>
"""),
    "privacy": ("Privacy Policy", "What data we collect, why we collect it, and what we never do with it.", """
<h2>What we collect</h2>
<p>We deliberately collect as little as possible. To run your account we hold:</p>
<ul>
<li>Your name and email address.</li>
<li>Your WhatsApp number, if you contact us that way.</li>
<li>Your order details: plan, term, number of devices and device type.</li>
<li>Your support messages, so we have the history when you come back.</li>
</ul>

<h2>What we do not collect</h2>
<ul>
<li>We do not store your card details. Payments are handled by the payment provider on your invoice.</li>
<li>We do not log or profile what you watch.</li>
<li>We do not sell, rent or share your details with advertisers or data brokers.</li>
</ul>

<h2>Why we hold it</h2>
<p>To create and maintain your subscription, to send your invoice and login details, to provide support, and to meet
our accounting obligations. That is the whole list.</p>

<h2>How long we keep it</h2>
<p>Account and support data is kept while your subscription is active and for up to 24 months afterwards, so that we
can help a returning customer. Invoice records are kept for as long as tax law requires. You can ask us to delete your
data sooner and we will, except where we are legally required to keep an invoice record.</p>

<h2>Cookies and analytics</h2>
<p>This website uses no advertising cookies and no third-party tracking pixels. Your chosen colour theme is stored in
your own browser and never leaves your device. Fonts are loaded from Google Fonts, which receives your IP address as
part of that request.</p>

<h2>Your rights</h2>
<p>You can ask us what we hold about you, ask for it to be corrected, ask for a copy, or ask for it to be deleted.
Email <a href="#" data-mail><span data-mail-text></span></a> and we will respond within 30 days.</p>

<h2>Security</h2>
<p>This website is served over HTTPS. Account details are held on access-controlled systems. No system is perfectly
secure, but we hold very little about you, which is the strongest protection we can offer.</p>

<h2>Changes</h2>
<p>If this policy changes we will update this page. Material changes will be communicated to active customers.</p>
"""),
    "refund": ("Refund Policy", "When you get your money back, and how to ask for it.", """
<h2>The short version</h2>
<p>If the service does not work properly for you and we cannot fix it, you get a refund within 7 days of activation.
No arguments, no hoops.</p>

<h2>When a refund applies</h2>
<ul>
<li>The service will not activate on any supported device after our support team has tried to resolve it.</li>
<li>There is a persistent fault on our side that we cannot fix within a reasonable time.</li>
<li>The service is materially different from what we described to you before you ordered.</li>
</ul>

<h2>When it does not</h2>
<ul>
<li>Your internet connection is below the minimum requirement and cannot support streaming.</li>
<li>A specific channel or event is unavailable, where the rest of the service works.</li>
<li>You changed your mind after more than 7 days.</li>
<li>You shared your login, exceeded your connection limit or breached our terms.</li>
<li>You declined to let our support team attempt to fix the issue.</li>
</ul>

<h2>How to request one</h2>
<ol>
<li>Message us on WhatsApp or email within 7 days of activation, describing the problem.</li>
<li>Give our support team a fair chance to fix it — most issues are resolved in minutes.</li>
<li>If it cannot be resolved, we process the refund to your original payment method.</li>
</ol>
<p>Refunds are normally processed within 5 to 10 working days, depending on your payment provider.</p>

<h2>Free trial first</h2>
<p>The best way to avoid needing this policy is to take the free 24-hour trial. It costs nothing, needs no card,
and tells you whether the service works on your own connection before any money changes hands.
<a href="/free-trial">Start a free trial →</a></p>
"""),
    "dmca": ("DMCA & Copyright", "How to contact us about a copyright concern.", """
<h2>Our position</h2>
<p>{B} is an independent reseller. We do not host, upload, record, store or transmit any video content on this
website or on our own infrastructure. This website is a storefront: it contains our own text and design, and
descriptive references to channel names for identification purposes only.</p>

<h2>Trademarks</h2>
<p>All channel names, network names, brand names, logos and trademarks referenced anywhere on this website are the
property of their respective owners. Their use here is nominative and descriptive — to identify the channels a
package may include — and does not imply any affiliation with, sponsorship by or endorsement from those owners.</p>

<h2>Notices</h2>
<p>If you believe that material accessible through this website infringes a copyright you own or control, send a
notice to <a href="#" data-mail><span data-mail-text></span></a> including:</p>
<ul>
<li>Identification of the copyrighted work you claim has been infringed.</li>
<li>The specific URL or material you are referring to, with enough detail for us to locate it.</li>
<li>Your name, address, telephone number and email address.</li>
<li>A statement that you have a good-faith belief the use is not authorised by the owner, its agent or the law.</li>
<li>A statement, under penalty of perjury, that the information is accurate and that you are the owner or authorised
to act on the owner's behalf.</li>
<li>Your physical or electronic signature.</li>
</ul>

<h2>What we do with a notice</h2>
<p>We review every notice we receive and respond promptly. Where material on this website is the subject of a valid
notice, we remove it. Where a notice concerns content delivered by an upstream supplier, we forward it to that
supplier and confirm to you that we have done so.</p>

<h2>Customers</h2>
<p>Customers are responsible for complying with the copyright and broadcasting laws that apply where they live.
If you are unsure of your legal position, take advice before subscribing to any streaming service.</p>
"""),
}


def build_legal():
    from lib import BRAND as B
    for slug, (title, lede, html) in LEGAL.items():
        prose = html.replace("{B}", BRAND).replace("{D}", DOMAIN)
        body = pagehead("Legal", title, lede,
                        crumbs=[("/", "Home"), (None, title)]) + f"""
<section class="section" style="padding-top:24px">
  <div class="wrap-narrow prose reveal">
    <p class="muted small">Last updated: 21 September 2026</p>
    {prose}
    <div class="callout" style="margin-top:44px"><b>Questions?</b> Message us on
      <a href="#" data-wa="Hi {BRAND}! I have a question about your {title.lower()}.">WhatsApp</a> or email
      <a href="#" data-mail><span data-mail-text></span></a>.</div>
  </div>
</section>"""
        write(f"/legal/{slug}", page(f"/legal/{slug}", f"{title} | {BRAND}", lede, body, bar=False),
              priority="0.3", freq="yearly")


# ===========================================================================
# 9. 404 + STATIC FILES
# ===========================================================================
def build_extras():
    body = f"""<section class="pagehead" style="padding-bottom:100px">
  <div class="wrap-narrow">
    <div class="d1 grad" style="line-height:1">404</div>
    <h1 class="d3" style="margin-top:12px">This page has gone off air.</h1>
    <p class="lede center">The link is broken or the page has moved. Here is where most people were heading.</p>
    <div class="row row-center" style="margin-top:30px">
      <a href="/" class="btn btn--primary">Back to home</a>
      <a href="/pricing" class="btn btn--outline">See plans</a>
      <a href="/setup" class="btn btn--outline">Setup guides</a>
    </div>
  </div>
</section>"""
    html = page("/404", f"Page not found | {BRAND}", "The page you were looking for does not exist.",
                body, bar=False)
    write_raw("404.html", html)

    # Favicon. The header mark is a hollow stroke on no background, which a
    # browser tab cannot rely on — tab strips are light in one OS theme and
    # dark in the other. So the icon version sits the same mark on the site's
    # near-black tile, legible either way, and the tile is inset so the glyph
    # still reads at 16px.
    write_raw("favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40">\n'
              + (lib.LOGO_GRAD % {"id": "g"}) + "\n"
              + '  <rect width="40" height="40" rx="9" fill="#0F0C0B"/>\n'
              + '  <g transform="translate(20 20) scale(.84) translate(-20 -20)">\n'
              + (lib.LOGO_PATHS % {"id": "g"}) + "\n  </g>\n</svg>")

    # Apache/cPanel equivalent of vercel.json. Namecheap shared hosting has
    # no serverless runtime, so /api/order.js never runs there — the order
    # emails go through FormSubmit or EmailJS instead (see EMAIL-SETUP.md).
    write_raw(".htaccess", """# ---------------------------------------------------------------------------
# Streamly4K — Apache config for cPanel hosting (Namecheap and similar)
# ---------------------------------------------------------------------------

# Pages are folder/index.html, so /pricing already works. This also lets
# /pricing.html resolve to /pricing without a redirect loop.
Options -MultiViews
RewriteEngine On

# force https
RewriteCond %{HTTPS} !=on
RewriteCond %{HTTP:X-Forwarded-Proto} !https
RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [R=301,L]

# strip a trailing .html if someone types one
RewriteCond %{THE_REQUEST} \s/+(.+?)\.html[\s?] [NC]
RewriteRule ^ /%1 [R=301,L]

ErrorDocument 404 /404.html

<IfModule mod_headers.c>
  Header always set X-Content-Type-Options "nosniff"
  Header always set X-Frame-Options "SAMEORIGIN"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set Permissions-Policy "geolocation=(), microphone=(), camera=()"
  # fingerprinted assets can be cached hard; html must not be
  <FilesMatch "\.(css|js|jpg|jpeg|png|webp|svg|woff2?|ico)$">
    Header set Cache-Control "public, max-age=31536000, immutable"
  </FilesMatch>
  <FilesMatch "\.html$">
    Header set Cache-Control "public, max-age=0, must-revalidate"
  </FilesMatch>
</IfModule>

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/plain text/xml \
    application/javascript application/json image/svg+xml
</IfModule>

<IfModule mod_mime.c>
  AddType image/svg+xml .svg
  AddType application/manifest+json .webmanifest
</IfModule>
""")

    write_raw("robots.txt", f"""User-agent: *
Allow: /
Disallow: /thank-you

Sitemap: {BASE}/sitemap.xml
""")

    write_raw("site.webmanifest", json.dumps({
        "name": BRAND, "short_name": BRAND, "start_url": "/", "display": "standalone",
        "background_color": "#080605", "theme_color": "#080605",
        "icons": [{"src": "/favicon.svg", "sizes": "any", "type": "image/svg+xml"}],
    }, indent=2))

    write_raw("vercel.json", json.dumps({
        "cleanUrls": True,
        "trailingSlash": False,
        "headers": [
            {"source": "/assets/(.*)",
             "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
            {"source": "/(.*)", "headers": [
                {"key": "X-Content-Type-Options", "value": "nosniff"},
                {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
                {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
                {"key": "Permissions-Policy", "value": "geolocation=(), microphone=(), camera=()"},
            ]},
        ],
    }, indent=2))


def build_sitemap():
    today = datetime.date.today().isoformat()
    urls = "".join(
        f"\n  <url><loc>{BASE}{'' if p == '/' else p}{'/' if p == '/' else ''}</loc>"
        f"<lastmod>{today}</lastmod><changefreq>{f}</changefreq><priority>{pr}</priority></url>"
        for p, pr, f in sorted(set(PAGES)))
    write_raw("sitemap.xml",
              f'<?xml version="1.0" encoding="UTF-8"?>\n'
              f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}\n</urlset>\n')


# ===========================================================================
def main():
    print(f"\nBuilding {BRAND} → {os.path.abspath(OUT)}\n")
    build_home()
    build_pricing()
    build_channels()
    build_setup()
    build_reviews()
    build_blog()
    build_support_pages()
    build_legal()
    build_extras()
    build_sitemap()
    print(f"\nDone — {len(PAGES)} pages.\n")


if __name__ == "__main__":
    main()
