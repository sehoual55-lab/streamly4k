"""Streamly4K — content data shared across pages (US / English market)."""

# --------------------------------------------------------------------------
# Channel names used in the marquee rows and the channel page.
# Text only — no third-party logo artwork is shipped with this template.
# To use real logos, drop PNG/SVG files into /assets/img/logos/ and swap the
# chip markup for <img src="/assets/img/logos/espn.svg" alt="ESPN">.
# --------------------------------------------------------------------------
MARQUEE_ROWS = [
    ["ESPN", "NFL Network", "NBA TV", "FOX Sports", "NBC Sports",
     "CBS Sports", "MLB Network", "NHL Network", "beIN SPORTS", "TNT Sports",
     "Golf Channel", "Tennis Channel", "Marquee Sports", "ACC Network",
     "SEC Network", "FS1", "Big Ten Network", "ESPN Deportes", "DAZN"],
    ["HBO", "Showtime", "STARZ", "Cinemax", "AMC", "FX", "USA", "TNT", "TBS",
     "Paramount Network", "Syfy", "Bravo", "Comedy Central", "IFC",
     "Sundance TV", "TCM", "Lifetime", "Hallmark", "Freeform", "BBC America",
     "Court TV", "ION Mystery", "Great American Family", "CMT", "E!"],
    ["CNN", "FOX News", "MSNBC", "CNBC", "Bloomberg", "NewsNation", "ABC",
     "NBC", "CBS", "FOX", "PBS", "Discovery", "History", "Nat Geo",
     "Animal Planet", "TLC", "A&E", "Science", "Al Jazeera", "CGTN",
     "FOX Business", "FOX Weather", "American Heroes Channel"],
    ["Cartoon Network", "Nickelodeon", "Disney Channel", "Nick Jr.",
     "Boomerang", "PBS Kids", "MTV", "BET", "Telemundo", "Univision",
     "Food Network", "HGTV", "Travel Channel", "Oxygen", "WE tv", "AXS TV",
     "The Weather Channel", "truTV", "Disney XD", "Nicktoons", "Estrella TV",
     "Antenna TV"],
]

# --------------------------------------------------------------------------
# On-demand tiles. `img` is optional: drop a JPG at /assets/img/posters/<slug>.jpg
# and it will be used automatically; otherwise a branded gradient tile shows.
# --------------------------------------------------------------------------
# --- TMDB SNAPSHOT START (regenerate with fetch_tmdb.py) ---
TMDB_FETCHED = "21 September 2026"

# Films — TMDB /movie/popular, filtered to released titles with a rating.
TMDB_FILMS = [
    ("Toy Story 5",               "Animation", 2026, 8.4),
    ("Obsession",                 "Thriller",  2026, 8.2),
    ("Colony",                    "Action",    2026, 8.1),
    ("The Odyssey",               "Adventure", 2026, 8.0),
    ("Spider-Man: Brand New Day", "Sci-Fi",    2026, 7.9),
    ("Zip Wire",                  "Action",    2026, 7.6),
    ("Coyote vs. Acme",           "Comedy",    2026, 7.6),
    ("Minions & Monsters",        "Family",    2026, 7.6),
    ("Moana",                     "Family",    2026, 7.4),
    ("Resident Evil",             "Horror",    2026, 7.4),
    ("Vishwanath & Sons",         "Drama",     2026, 7.2),
    ("The End of Oak Street",     "Mystery",   2026, 7.0),
]

# Films — TMDB /movie/top_rated.
TMDB_TOP_FILMS = [
    ("Avatar Aang: The Last Airbender",              "Animation", 2026, 9.1),
    ("Demon Slayer: Infinity Castle",                "Animation", 2025, 8.8),
    ("The Shawshank Redemption",                     "Drama",     1994, 8.7),
    ("The Godfather",                                "Crime",     1972, 8.7),
    ("Project Hail Mary",                            "Sci-Fi",    2026, 8.6),
    ("The Godfather Part II",                        "Crime",     1974, 8.6),
    ("12 Angry Men",                                 "Drama",     1957, 8.6),
    ("Schindler's List",                             "Drama",     1993, 8.6),
    ("The Dark Knight",                              "Action",    2008, 8.5),
    ("Spirited Away",                                "Animation", 2001, 8.5),
    ("The Green Mile",                               "Drama",     1999, 8.5),
    ("The Lord of the Rings: The Return of the King", "Adventure", 2003, 8.5),
]

# Series — TMDB /tv/popular and /tv/top_rated, talk, news and reality formats removed.
TMDB_SERIES = [
    ("Dutton Ranch",                    "Western",   2026, 9.2),
    ("Breaking Bad",                    "Drama",     2008, 9.0),
    ("Avatar: The Last Airbender",      "Animation", 2005, 8.8),
    ("Frieren: Beyond Journey's End",   "Animation", 2023, 8.8),
    ("Chernobyl",                       "Drama",     2019, 8.7),
    ("Arcane",                          "Animation", 2021, 8.7),
    ("One Piece",                       "Action",    1999, 8.7),
    ("The Pitt",                        "Drama",     2025, 8.7),
    ("The Mentalist",                   "Crime",     2008, 8.4),
    ("Criminal Minds",                  "Crime",     2005, 8.3),
    ("Lioness",                         "Drama",     2023, 8.2),
    ("Reacher",                         "Action",    2022, 8.1),
]
# --- TMDB SNAPSHOT END ---


# --------------------------------------------------------------------------
# Channel categories (channels page + homepage grid)
# --------------------------------------------------------------------------
CATEGORIES = [
    ("trophy", "Sports", "3,200+",
     "NFL, NBA, MLB, NHL, college football, UFC, boxing, F1, golf, tennis and the major PPV events.",
     ["ESPN", "NFL Network", "NBA TV", "FOX Sports 1", "Big Ten Network", "DAZN"]),
    ("film", "Movies & Premium", "1,900+",
     "HBO, Showtime, STARZ, Cinemax and the movie channels, plus a 120,000-title on-demand library.",
     ["HBO", "Showtime", "STARZ", "Cinemax", "AMC", "TCM"]),
    ("tv", "Entertainment", "2,400+",
     "The big networks and cable entertainment: comedy, reality, drama and everything in between.",
     ["ABC", "NBC", "CBS", "FOX", "USA", "TNT"]),
    ("news", "News & Business", "600+",
     "US and international news around the clock, plus business and market coverage.",
     ["CNN", "FOX News", "MSNBC", "FOX Business", "Bloomberg", "Al Jazeera"]),
    ("kids", "Kids & Family", "700+",
     "Cartoons, pre-school and family channels, with a parental-lock PIN on every package.",
     ["Cartoon Network", "Nickelodeon", "Disney Channel", "Disney XD", "Nicktoons", "PBS Kids"]),
    ("globe", "International", "2,800+",
     "Spanish, Arabic, Indian, Filipino, Portuguese, Polish, Turkish, African and more.",
     ["Telemundo", "Univision", "MBC", "Zee TV", "TFC", "TVP"]),
    ("eye", "Documentary", "800+",
     "Nature, history, science, engineering and true-crime documentary channels.",
     ["Discovery", "History", "Nat Geo", "American Heroes Channel", "Science", "ID"]),
    ("music", "Music & Lifestyle", "500+",
     "Music video channels, concerts, food, home, travel and lifestyle programming.",
     ["MTV", "BET", "Food Network", "HGTV", "Travel Channel", "AXS TV"]),
]

# --------------------------------------------------------------------------
# What the subscription includes
# --------------------------------------------------------------------------
INCLUDED = [
    ("hd", "4K, HDR &amp; Full HD", "Every channel at the best quality your connection allows."),
    ("trophy", "All the sport", "NFL, NBA, MLB, NHL, UFC, boxing, F1 and major PPV events."),
    ("globe", "International channels", "2,800+ channels in Spanish, Arabic, Hindi, Tagalog and more."),
    ("grid", "TV guide (EPG)", "A full 7-day electronic programme guide, built in."),
    ("zap", "Anti-freeze servers", "Load-balanced servers tuned for low buffering at peak times."),
    ("devices", "Every device you own", "Smart TV, Firestick, Android, iPhone, iPad, PC, Mac, MAG."),
    ("refresh", "Catch-up TV", "Rewind up to 7 days on most channels and watch what you missed."),
    ("headset", "24/7 human support", "Real people on WhatsApp and email, every day of the year."),
]

# --------------------------------------------------------------------------
# Competitor stack used in the savings calculator (public list prices,
# checked September 2026 — update the numbers when they change).
# --------------------------------------------------------------------------
# (name, monthly price, card background, card text colour)
#
# Each card carries the service's own colour scheme so the stack reads as
# six different products rather than six identical tiles. NO LOGOS and no
# monogram tiles: a letter in a brand-coloured rounded square is that
# company's icon redrawn, which is exactly the thing that gets a reseller
# a trademark complaint. Name + colour + honest price is comparative
# advertising; the mark is not ours to use.
STACK = [
    ("YouTube TV Base Plan", 82.99, "#FFFFFF", "#0F0F0F"),
    ("NFL Sunday Ticket",    40.00, "#013369", "#FFFFFF"),
    ("Netflix Standard",     19.99, "#0B0B0B", "#E50914"),
    ("HBO Max Standard",     18.49, "#1A0B3D", "#FFFFFF"),
    ("Disney+ Premium",      18.99, "#0C1E4D", "#FFFFFF"),
    ("Peacock Premium",      12.99, "#0A0A0A", "#F5F5F5"),
]

# --------------------------------------------------------------------------
# Supported devices
# --------------------------------------------------------------------------
DEVICES = [
    ("tv", "Smart TV", "Samsung Tizen, LG webOS, Android TV, Google TV", "/setup/smart-tv"),
    ("stick", "Firestick & Fire TV", "Fire TV Stick, 4K, Max, Fire TV Cube", "/setup/firestick"),
    ("android", "Android", "Phones, tablets, TV boxes, NVIDIA Shield", "/setup/android"),
    ("apple", "Apple", "iPhone, iPad, Apple TV 4K", "/setup/iphone-ipad"),
    ("laptop", "PC, Mac & browser", "Windows, macOS, Linux, any modern browser", "/setup/pc-mac"),
    ("devices", "MAG & Enigma2", "MAG boxes, Formuler, Zgemma, Dreambox", "/setup/mag-box"),
]

# --------------------------------------------------------------------------
# FAQ used on the homepage and (expanded) on /faq
# --------------------------------------------------------------------------
FAQ_HOME = [
    ("How fast will my subscription be active?",
     "Most orders are activated within 5 to 15 minutes of your payment being confirmed. You receive your login "
     "details by email and on WhatsApp, together with a setup guide for the device you told us you use. "
     "If you order late at night, activation can occasionally take a little longer."),
    ("Do I need to buy any hardware?",
     "No. Streamly4K works on devices you already own — your Smart TV, a Firestick, an Android box, your phone, "
     "tablet, laptop or a MAG box. All you need is an internet connection of around 15 Mbps for HD and 25 Mbps "
     "for 4K, and an app we help you install for free."),
    ("Is there a free trial?",
     "Yes. We offer a trial of up to 24 hours so you can test the channels, the picture quality and the stability "
     "on your own connection before you pay anything. Message us on WhatsApp and we will set it up."),
    ("How many devices can I use at once?",
     "One device per connection by default. If several people in the house want to watch different channels at "
     "the same time, add extra devices when you order — each additional device adds 50% to the price of the plan."),
    ("What happens if a channel stops working?",
     "Message us on WhatsApp. Channel line-ups change and sources occasionally go down; in most cases we can "
     "restore a stream or point you at an alternative within minutes. Support is available 24/7."),
    ("How do I pay, and is it a recurring charge?",
     "We send you an invoice with payment instructions by email and WhatsApp. It is a single one-time payment for "
     "the term you chose — nothing is stored, nothing renews automatically, and you decide whether to renew."),
    ("Can I get a refund?",
     "Yes. If the service does not work properly for you and we cannot fix it, you can request a refund within "
     "7 days of activation under our refund policy."),
    ("Do I need a VPN?",
     "Not usually. Some internet providers throttle streaming traffic, and if yours does, a VPN can make playback "
     "smoother. We will tell you honestly if we think your connection needs one."),
]

FAQ_EXTRA = [
    ("Which app do you use?",
     "It depends on your device. We mainly use IPTV Smarters Pro, TiviMate and similar standard IPTV players. "
     "All of them are free to install, and our setup guides walk through each one step by step."),
    ("Can I watch on holiday or in another country?",
     "Yes. Your subscription is tied to your account rather than your home address, so it works anywhere with a "
     "decent internet connection."),
    ("Do you keep a record of what I watch?",
     "No. We store the details we need to run your account — your email, your WhatsApp number and your order — "
     "and nothing about your viewing. See our privacy policy for the full detail."),
    ("What internet speed do I need?",
     "About 15 Mbps for Full HD and 25 Mbps or more for 4K. A wired Ethernet connection to your TV box is always "
     "more stable than Wi-Fi, especially for live sport."),
    ("Can I upgrade or add a device later?",
     "Yes. Message us on WhatsApp and we will work out the difference and adjust your line — you keep the same "
     "login details."),
    ("What happens when my subscription ends?",
     "Your line simply stops working. There is no automatic renewal and no card on file. If you want to continue, "
     "message us before the end date and we extend the same account."),
]

# --------------------------------------------------------------------------
# Blog posts: (slug, title, excerpt, category, date, read, body_sections)
# --------------------------------------------------------------------------
BLOG = [
    {
        "slug": "what-is-iptv",
        "title": "What is IPTV, and how does it actually work?",
        "excerpt": "A plain-English explanation of internet television: what it is, how a subscription works, "
                   "what it costs and what to check before you buy.",
        "cat": "Guide", "date": "2026-09-08", "date_h": "8 September 2026", "read": "7 min",
        "icon": "tv",
    },
    {
        "slug": "iptv-vs-cable-cost",
        "title": "IPTV vs cable and streaming apps: the real cost in 2026",
        "excerpt": "We add up what a typical US household pays for cable plus streaming apps, and compare it with "
                   "a single IPTV subscription.",
        "cat": "Comparison", "date": "2026-09-02", "date_h": "2 September 2026", "read": "6 min",
        "icon": "wallet",
    },
    {
        "slug": "stop-iptv-buffering",
        "title": "How to stop IPTV buffering: 9 fixes that actually work",
        "excerpt": "Buffering is almost never the server. Here is the order to check things in, from your router "
                   "to your player settings.",
        "cat": "Troubleshooting", "date": "2026-08-26", "date_h": "26 August 2026", "read": "8 min",
        "icon": "zap",
    },
    {
        "slug": "best-device-for-iptv",
        "title": "The best device for IPTV in 2026 (and what to avoid)",
        "excerpt": "Firestick, Android box, Smart TV app or NVIDIA Shield? An honest look at what each one is good "
                   "and bad at.",
        "cat": "Hardware", "date": "2026-08-18", "date_h": "18 August 2026", "read": "9 min",
        "icon": "devices",
    },
    {
        "slug": "watch-nfl-without-cable",
        "title": "How to watch NFL games without cable in 2026",
        "excerpt": "Every legal and practical route to Sunday football — broadcast, streaming apps, Sunday Ticket "
                   "and IPTV — with the trade-offs of each.",
        "cat": "Sports", "date": "2026-08-11", "date_h": "11 August 2026", "read": "7 min",
        "icon": "trophy",
    },
    {
        "slug": "iptv-buyers-checklist",
        "title": "Before you buy an IPTV subscription: a 10-point checklist",
        "excerpt": "The questions worth asking any provider before you pay — and the answers that should make you "
                   "walk away.",
        "cat": "Guide", "date": "2026-08-04", "date_h": "4 August 2026", "read": "6 min",
        "icon": "shield",
    },
]

# --- FILM SLIDER START (regenerate with fetch_tmdb.py) ---
# (title, genre, year, rating, tmdb poster path) — the homepage slider.
TMDB_SLIDER = [
    ("Avatar Aang: The Last Airbender",           "Animation",  2026, 9.1, "/3sgnSfNT27Bx5O5ukr7B26mhEQq.jpg"),
    ("Facing El Chapo",                           "Crime",      2026, 8.8, "/alpf5v4UqSFawPmG9RX03Or4BDk.jpg"),
    ("Demon Slayer: Infinity Castle",             "Animation",  2025, 8.8, "/fWVSwgjpT2D78VUh6X8UBd2rorW.jpg"),
    ("The Shawshank Redemption",                  "Drama",      1994, 8.7, "/9cqNxx0GxF0bflZmeSMuL5tnGzr.jpg"),
    ("The Godfather",                             "Drama",      1972, 8.7, "/3bhkrj58Vtu7enYsRolD1fZdja1.jpg"),
    ("Project Hail Mary",                         "Sci-Fi",     2026, 8.6, "/yihdXomYb5kTeSivtFndMy5iDmf.jpg"),
    ("Interstellar",                              "Adventure",  2014, 8.5, "/yQvGrMoipbRoddT0ZR8tPoR7NfX.jpg"),
    ("The Dark Knight",                           "Action",     2008, 8.5, "/qJ2tW6WMUDux911r6m7haRef0WH.jpg"),
    ("Toy Story 5",                               "Animation",  2026, 8.4, "/sfQtVlIHljToOwYjhe21KPGzZWK.jpg"),
    ("Inception",                                 "Action",     2010, 8.4, "/xlaY2zyzMfkhk0HSC5VUwzoZPU1.jpg"),
    ("The Shadow's Edge",                         "Action",     2025, 8.3, "/cHKo3m8N1fwvEy2ZEr0xGmmMODV.jpg"),
    ("The Wild Robot",                            "Family",     2024, 8.3, "/wTnV3PCVW5O92JMrFvvrRcV39RU.jpg"),
    ("Obsession",                                 "Horror",     2026, 8.2, "/bRwnj8WEKBCvmfeUNOukJPwB43K.jpg"),
    ("Avengers: Endgame",                         "Adventure",  2019, 8.2, "/ulzhLuWrPK07P1YkdWQLZnQh1JL.jpg"),
    ("Avengers: Infinity War",                    "Adventure",  2018, 8.2, "/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg"),
    ("The Super Mario Galaxy Movie",              "Family",     2026, 8.2, "/eJGWx219ZcEMVQJhAgMiqo8tYY.jpg"),
    ("Colony",                                    "Action",     2026, 8.1, "/tN799oUR0f1gUKDYdMNrDaY7I51.jpg"),
    ("The Avengers",                              "Sci-Fi",     2012, 8.1, "/RYMX2wcKCBAr24UyPD7xwmjaTn.jpg"),
    ("The Odyssey",                               "Adventure",  2026, 8.0, "/5rhTDKUhPYvpdQIijFIs5VoWsON.jpg"),
    ("Mayday",                                    "Action",     2026, 8.0, "/hVXjX1jLZ1ljFSNGXpjJfbTUOa7.jpg"),
    ("Spider-Man: Brand New Day",                 "Sci-Fi",     2026, 7.9, "/bjiS5ipwxb9JFy3XRRN4OAilSeX.jpg"),
    ("Spider-Man: No Way Home",                   "Action",     2021, 7.9, "/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg"),
    ("Harry Potter and the Philosopher's Stone",  "Adventure",  2001, 7.9, "/wuMc08IPKEatf9rnMNXvIDxqP4W.jpg"),
    ("Zootopia 2",                                "Animation",  2025, 7.7, "/oJ7g2CifqpStmoYQyaLQgEU32qO.jpg"),
    ("The Terminator",                            "Action",     1984, 7.7, "/qvktm0BHcnmDpul4Hz01GIazWPr.jpg"),
    ("Evil Dead Burn",                            "Horror",     2026, 7.7, "/uRxrNXQWkHoENm3nwVOZDYSCx2F.jpg"),
    ("Coyote vs. Acme",                           "Comedy",     2026, 7.6, "/kYDCl2y0VPvhT5eYWbMRInPoB03.jpg"),
    ("Minions & Monsters",                        "Adventure",  2026, 7.6, "/4LwvU9SZc8QQzW1X1FAPhNbXnEU.jpg"),
    ("Avatar: Fire and Ash",                      "Sci-Fi",     2025, 7.6, "/bRBeSHfGHwkEpImlhxPmOcUsaeg.jpg"),
]
# --- FILM SLIDER END ---


# --------------------------------------------------------------------------
# Device rail (homepage "on any device" section)
# --------------------------------------------------------------------------
# Each entry is (mark, label). `mark` is a key from lib.PLATFORMS and renders
# that brand's own glyph; prefix it with "icon:" to fall back to one of our
# generic glyphs instead. MAG and Enigma2 have no mark in the set, so they use
# a generic one rather than borrowing another brand's — an icon has to mean
# what it shows. Only list a device you actually support and can help set up.
DEVICE_RAIL = [
    [("samsung", "Samsung TV"), ("lg", "LG TV"), ("sony", "Sony TV"),
     ("amazon", "Firestick"), ("android", "Android TV"), ("roku", "Roku"),
     ("chromecast", "Chromecast"), ("appletv", "Apple TV"), ("xbox", "Xbox")],
    [("apple", "iPhone"), ("apple", "iPad"), ("android", "Android phone"),
     ("android", "Android Box"), ("windows", "Windows PC"), ("apple", "macOS"),
     ("linux", "Linux"), ("icon:stick", "MAG Box"), ("icon:devices", "Enigma2")],
]

DEVICE_CHECKS = [
    "Choose up to 5 devices with your plan",
    "Firestick, Android TV, smart TV, Apple TV, phone and computer",
    "EPG / TV guide support on compatible players",
    "Login details arrive by email and WhatsApp, usually within 5&ndash;15 minutes "
    "after payment confirmation",
]
