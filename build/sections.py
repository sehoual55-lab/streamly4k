"""Streamly4K — reusable page sections."""
import pathlib, re
from lib import icon, ICONS, BRAND, pay_badges as _pay
import data

# Optional channel logos, supplied by you. See _chip() below.
LOGO_DIR = pathlib.Path(__file__).resolve().parent.parent / "assets" / "img" / "logos"


# --------------------------------------------------------------------------
def hero():
    return f"""<section class="hero">
  <!-- HERO BACKDROP: poster wall (built by main.js) → duotone → veil → grid -->
  <div class="hero__wall" aria-hidden="true"><div class="wallpar"><div class="wallgrid" id="wallgrid"></div></div></div>
  <div class="hero__veil" aria-hidden="true"></div>
  <div class="hero__bg"></div><div class="hero__grid"></div>
  <div class="wrap">
    <span class="pill"><span class="dot"></span>Live TV · Sports · Movies · 4K</span>
    <h1 class="d1">Every channel you love.<br><span class="grad">One simple subscription.</span></h1>
    <p class="lede center mx-auto">Live TV, sports, movies and series in HD and 4K, on the devices you already own.
      Most subscriptions are watching within 5&ndash;15 minutes of payment.</p>
    <div class="row hero__cta">
      <a href="/pricing" class="btn btn--primary btn--lg">See plans &amp; prices {icon("arrow")}</a>
      <a href="/free-trial" class="btn btn--ghost btn--lg">Start a free trial</a>
    </div>
    <div class="hero__trust">
      <span>{icon("shield")} 7-day money-back guarantee</span>
      <span>{icon("clock")} Live in 5&ndash;15 minutes</span>
      <span>{icon("headset")} 24/7 human support</span>
      <span>{icon("refresh")} No contract, no auto-renewal</span>
    </div>
    <div class="ratingcard" data-rating>
      <span class="ratingcard__stars">{icon("star") * 5}</span>
      <span><strong data-rating-score></strong> on <span data-rating-platform></span> &middot;
        <a data-rating-link href="#" class="muted"><span data-rating-count></span></a></span>
    </div>
{trustpilot()}
{stats()}
  </div>
</section>"""


# --------------------------------------------------------------------------
def trustpilot():
    """Trustpilot slot.

    Two states, both driven by C.rating in assets/js/config.js:

      * no verified rating yet  -> a plain "Review us on Trustpilot" link.
        An invitation is not a claim, so this is safe to ship on day one.
      * rating.show = true      -> the real score and review count.

    Deliberately NOT rendered: a placeholder score, a sample star count or a
    "4.8/5" awaiting real data. Publishing a rating you cannot evidence is
    unlawful advertising in the US (FTC) and the UK/EU, and Trustpilot
    delists businesses for it. Once the profile is live, drop Trustpilot's
    own TrustBox script in here instead — that is the licensed way to show
    their logo and a verified score.
    """
    return f"""    <div class="tp">
      <a class="tp__link" data-tp-url href="#" target="_blank" rel="noopener nofollow">
        <span class="tp__star" aria-hidden="true">{icon("star")}</span>
        <span class="tp__body">
          <span class="tp__rated" data-tp-rated>Review us on <strong>Trustpilot</strong></span>
          <span class="tp__score" data-tp-score hidden>
            <span class="tp__stars" data-tp-stars>{icon("star") * 5}</span>
            <strong data-rating-score></strong><span class="tp__of">/5</span>
            <span class="tp__count muted" data-rating-count></span>
          </span>
        </span>
      </a>
    </div>"""


# --------------------------------------------------------------------------
def stats():
    """The headline numbers — a glass bar sitting inside the hero."""
    items = [
        ("25,000+", "Live channels"),
        ("120,000+", "Movies &amp; series"),
        ("99.9%", "Server uptime target"),
        ("Up to 4K", "Picture quality"),
    ]
    cells = "".join(
        f'<div class="stats__item"><div class="stats__num">{n}</div><div class="stats__label">{l}</div></div>'
        for n, l in items
    )
    return f"""    <div class="statbar">
      <div class="stats">{cells}</div>
    </div>"""


# --------------------------------------------------------------------------
def _chip_slug(name):
    """'FOX Sports' -> 'fox-sports'  (filename you'd give its logo)."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _chip(name, extra=""):
    """A channel chip.

    Drop a file at assets/img/logos/<slug>.(svg|png|webp) and rebuild, and
    that channel renders as its logo instead of its name; otherwise the name
    stands in. Nothing is bundled — broadcaster logos are registered
    trademarks, and an unlicensed storefront displaying them is the fastest
    route to a complaint at your host or registrar (these rights-holders run
    active anti-IPTV enforcement). Only use files you are licensed to use:
    an affiliate/partner kit, or your provider's own assets.
    """
    slug = _chip_slug(name)
    for ext in ("svg", "png", "webp"):
        f = LOGO_DIR / f"{slug}.{ext}"
        if f.is_file():
            return (f'<span class="chip chip--logo"{extra}>'
                    f'<img src="/assets/img/logos/{slug}.{ext}" alt="{name}" '
                    f'loading="lazy" decoding="async"></span>')
    return f'<span class="chip"{extra}>{name}</span>'


def channels_marquee(rows=3):
    out = ""
    for i, row in enumerate(data.MARQUEE_ROWS[:rows]):
        rev = " marquee__track--rev" if i % 2 else ""
        dur = 42 + i * 9
        chips = "".join(_chip(c) for c in row)
        out += (f'<div class="marquee"><div class="marquee__track{rev}" '
                f'style="animation-duration:{dur}s">{chips}</div></div>')
    return out


def film_grid(size="w342"):
    """Two counter-scrolling poster rows over a full-bleed poster wash.

    Row one travels right, row two travels left. Each track holds its films
    twice so a 50% translate loops seamlessly; main.js sets the duration from
    the measured set width so both rows move at the same speed whatever the
    card size. Tracks pause on hover/focus so a title can actually be read.
    """
    def card(t, g, y, r, path):
        return f'''<article class="fcard" tabindex="0">
        <img class="fcard__art" src="https://image.tmdb.org/t/p/{size}{path}" alt="{t}"
             loading="lazy" decoding="async" referrerpolicy="no-referrer" width="342" height="513">
        <span class="fcard__shade" aria-hidden="true"></span>
        <span class="fcard__sheen" aria-hidden="true"></span>
        <div class="fcard__meta">
          <span class="fcard__tag">{g}</span>
          <div class="fcard__title">{t}</div>
          <div class="fcard__sub">{icon("sparkle")}4K &middot; Subtitles</div>
        </div>
      </article>'''

    films = list(data.TMDB_SLIDER)
    mid = (len(films) + 1) // 2
    rows = [films[:mid], films[mid:]]

    out = ""
    for i, row in enumerate(rows):
        cards = "".join(card(*f) for f in row)
        out += (f'''    <div class="frow frow--{"r" if i == 0 else "l"}">
      <div class="frow__track" data-frow>{cards}{cards}</div>
    </div>''')

    return f'''  <div class="filmwrap reveal">
    <div class="filmwrap__wall" aria-hidden="true"><div class="filmwrap__wallgrid" id="railwall"></div></div>
    <div class="filmwrap__veil" aria-hidden="true"></div>
    <div class="filmrows">
{out}
      <div class="filmrows__edge filmrows__edge--l" aria-hidden="true"></div>
      <div class="filmrows__edge filmrows__edge--r" aria-hidden="true"></div>
    </div>
    <div class="wrap">
      <div class="filmgrid__notes">
        <span>{icon("check")} Movies &amp; series on demand</span>
        <span>{icon("check")} New content added regularly</span>
      </div>
    </div>
  </div>'''


def channels_section():
    return f"""<section class="section section--alt" id="channels">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Inside the library</span>
      <h2 class="d2">Find what you <span class="grad">love to watch</span></h2>
      <p class="lede">Blockbusters, box sets and the classics — alongside 25,000+ live channels covering sports, news, kids and 2,800+ international feeds.</p>
    </div>
  </div>
{film_grid()}
  <div class="wrap" style="margin-top:44px">
    <div class="grid g-4 reveal">{category_cards(4)}</div>
    <p class="center" style="margin-top:32px">
      <a href="/channels" class="btn btn--ghost">Browse the full channel list {icon("arrow")}</a>
    </p>
  </div>
</section>"""


def category_cards(limit=None, links=True):
    cats = data.CATEGORIES[:limit] if limit else data.CATEGORIES
    out = ""
    for ic, name, count, desc, examples in cats:
        ex = "".join(f'<span class="badge badge--soft" style="margin:4px 4px 0 0">{e}</span>' for e in examples[:4]) if not links else ""
        out += f"""<div class="cat">
      <div class="cat__top">{icon(ic)}<span class="cat__count">{count}</span></div>
      <h3>{name}</h3><p>{desc}</p>{'<div style="margin-top:12px">' + ex + '</div>' if ex else ''}
    </div>"""
    return out


# --------------------------------------------------------------------------
def savings_section():
    """Left column: six branded cards that collapse into one.

    Cards carry each service's own colour scheme (YouTube white-on-black
    type, Netflix red on near-black, and so on) but no logos or monogram
    tiles — see the note on data.STACK. The fan is real markup; main.js
    only adds the collapse trigger, so it still reads as a price list with
    JS off.
    """
    total = sum(price for _, price, _, _ in data.STACK)
    n = len(data.STACK)

    rows = ""
    for i, (name, price, bg, fg) in enumerate(data.STACK):
        rows += f"""<div class="srow" style="--bg:{bg};--fg:{fg};--i:{i}">
            <span class="srow__name">{name}</span>
            <span class="srow__price">${price:.2f}<i>/mo</i></span>
            <span class="srow__strike" aria-hidden="true"></span>
          </div>"""

    yearly = total * 12
    ours_m, ours_y = 8.33, 99.99
    save_m, save_y = total - ours_m, yearly - ours_y

    return f"""<section class="section section--alt savingsec">
  <div class="savingsec__glow" aria-hidden="true"></div>
  <div class="wrap">
    <div class="savings">
      <div class="reveal">
        <div class="row" style="justify-content:space-between;align-items:flex-start;margin-bottom:18px">
          <span class="eyebrow">Without {BRAND}</span>
          <span class="scribble">Every. Single. Month.</span>
        </div>

        <div class="stackfx" data-stack
             aria-label="Six separate subscriptions costing ${total:,.2f} a month, replaced by one {BRAND} subscription at ${ours_y:,.2f} a year">
          <div class="srows">
            {rows}
            <div class="srow srow--us">
              <span class="srow__name">{BRAND}</span>
              <span class="srow__price">${ours_y:,.2f}<i>/year</i></span>
            </div>
          </div>
          <div class="stackfx__count">
            <span class="stackfx__line">
              <span class="stackfx__n" data-stack-n>{n}</span>
              <span class="stackfx__w" data-stack-w>subscriptions</span>
            </span>
            <span class="stackfx__price">only ${ours_y:,.2f} USD for 1 year</span>
          </div>
        </div>
      </div>

      <div class="reveal">
        <span class="eyebrow">Let's do the math</span>
        <h2 class="d2" style="margin-top:14px">You save<br><span class="grad">${save_y:,.0f} a year.</span></h2>
        <p class="lede" style="margin-top:18px">{len(data.STACK)} subscriptions. {len(data.STACK)} logins.
          72 payments a year. Why keep paying month after month?</p>

        <table class="mathtable">
          <thead><tr><th></th><th>Monthly</th><th>Yearly</th></tr></thead>
          <tbody>
            <tr><td>Now &middot; {len(data.STACK)} subscriptions</td><td>${total:,.2f}</td><td>${yearly:,.2f}</td></tr>
            <tr class="is-us"><td>{BRAND}</td><td>${ours_m:,.2f}</td><td>${ours_y:,.2f}</td></tr>
            <tr class="is-save"><td>You save</td><td>+${save_m:,.2f}</td><td>+${save_y:,.2f}</td></tr>
          </tbody>
        </table>

        <p style="margin-top:26px"><strong>That is the stack a lot of US households pay for.</strong>
          {BRAND} is one subscription instead of six.</p>
        <a href="/pricing" class="btn btn--primary btn--lg" style="margin-top:24px">Get {BRAND} for $99.99 / year</a>
        <p class="xsmall muted" style="margin-top:16px;max-width:60ch">
          Example price comparison only — not a like-for-like content comparison. List prices checked September 2026
          and may change. {BRAND} is an independent reseller and is not affiliated with any service shown.</p>
      </div>
    </div>
  </div>
</section>"""


# --------------------------------------------------------------------------
def builder_section(heading=True):
    """Two-column order card: choose on the left, act on the right.

    The right column has two faces. By default it sells — what every plan
    includes, the guarantees, the payment marks. Press "Order now" and it
    turns into the invoice form, with a Back button to return. Swapping a
    column in place beats a modal here: the plan and the price stay on
    screen the whole time, so nobody has to remember what they picked while
    typing their email.

    Every data-* hook the pricing JS uses is preserved (data-term, data-dev,
    data-out-*), so the layout changed but the maths did not.
    """
    from lib import icon as _i, platform as _plat

    terms = ""
    for pid, name, tag, price, per, flag in [
            ("3m", "3 Months", "Basic", "39.99", "13.33", ""),
            ("6m", "6 Months", "Standard", "69.99", "11.67", ""),
            ("12m", "12 Months", "Premium", "99.99", "8.33", "Best value")]:
        on = " is-on" if pid == "12m" else ""
        flag_html = f'<span class="wterm__flag">{flag}</span>' if flag else ""
        terms += f"""<button type="button" class="wterm{on}" data-term="{pid}" aria-pressed="{str(pid=='12m').lower()}">
          {flag_html}
          <span class="wterm__main">
            <span class="wterm__name">{name}</span>
            <span class="wterm__tag">{tag}</span>
          </span>
          <span class="wterm__nums">
            <span class="wterm__price">${price}</span>
            <span class="wterm__per">${per}/mo</span>
          </span>
          <span class="wterm__tick">{_i("check")}</span>
        </button>"""

    plats = "".join(_plat(k) for k in
                    ["samsung", "lg", "sony", "apple", "appletv", "android",
                     "amazon", "roku", "chromecast", "xbox", "windows", "linux"])

    # right column, default face: two headline numbers then the feature tiles
    stats = (f'<div class="wfeat wfeat--big"><b>25,000+</b><span>Live TV channels</span></div>'
             f'<div class="wfeat wfeat--big"><b>120,000+</b><span>Movies &amp; series</span></div>')
    feats = "".join(
        f'<div class="wfeat">{_i(ic)}<span><b>{title}</b></span></div>'
        for ic, title, _desc in data.INCLUDED[:6]
    )

    head = ""
    if heading:
        head = """<div class="section-head reveal">
      <span class="eyebrow">Simple pricing</span>
      <h2 class="d2">One plan. <span class="grad">Pick your term.</span></h2>
      <p class="lede">Choose how long, and how many screens. Everything else is included.</p>
    </div>"""

    return f"""<section class="section" id="pricing">
  <div class="wrap">
    {head}
    <div class="wizard reveal">
      <div class="wizard__glow" aria-hidden="true"></div>
      <div class="wizcols">

        <!-- LEFT: what you are buying -->
        <div class="wizcol wizcol--pick">
          <div class="wrow">
            <h3 class="wrow__t">How long? <span>One-time payment, no auto-renewal</span></h3>
            <div class="wterms">{terms}</div>
          </div>

          <div class="wrow wrow--div">
            <h3 class="wrow__t">How many devices? <span>+50% per extra device</span></h3>
            <div class="wdev">
              <div class="stepper">
                <button type="button" data-dev="-1" aria-label="Fewer devices">{_i("minus")}</button>
                <span class="stepper__val" data-out-devices>1 device</span>
                <button type="button" data-dev="1" aria-label="More devices">{_i("plus")}</button>
              </div>
              <p class="wdev__note" data-out-screens>Watch on one screen at a time</p>
            </div>
            <div class="wplats">
              <div class="plats">{plats}</div>
              <p class="plats__note">Smart TV &middot; Firestick &middot; Android &middot; iPhone &amp; iPad &middot; PC &amp; Mac</p>
            </div>
          </div>

          <div class="wrow wrow--div wrow--total">
            <div class="wtotal">
              <span class="wtotal__amount" data-out-total>$99.99</span>
              <span class="wtotal__per" data-out-permonth>&asymp; $8.33 / month</span>
            </div>
            <div class="wtotal__meta" data-out-summary>12 Months &middot; 1 device</div>
            <button type="button" data-checkout-open class="btn btn--solid btn--block" style="margin-top:22px">
              Order now {_i("arrow")}</button>
          </div>
        </div>

        <!-- RIGHT: sells by default, becomes the invoice form on "Order now" -->
        <div class="wizcol wizcol--side">
          <div class="wside" data-side="incl">
            <h3 class="d4">Everything included, on every plan</h3>
            <p class="muted small" style="margin-top:6px">The term changes the price, never the line-up.</p>
            <div class="wfeats">{stats}{feats}</div>
            <a href="/pricing#included" class="link-arrow small" style="margin-top:18px;display:inline-flex">
              See everything included {_i("arrow")}</a>
            <div class="wside__foot">
              <div class="guarantees" style="margin-top:0;padding-top:0;border-top:0">
                <div class="guarantee">{_i("clock")}<b>Live in 5&ndash;15 min</b><span>usually, after payment</span></div>
                <div class="guarantee">{_i("shield")}<b>7-day money-back</b><span>guarantee</span></div>
                <div class="guarantee">{_i("headset")}<b>24/7 support</b><span>WhatsApp &amp; email</span></div>
              </div>
              <h4 class="eyebrow" style="margin-top:22px;display:block;color:var(--muted)">Pay your invoice with</h4>
              {_pay()}
            </div>
          </div>
{checkout_panel()}
        </div>

      </div>
    </div>
  </div>
</section>"""


# --------------------------------------------------------------------------
def checkout_panel():
    """The invoice form — the right column's second face, not a modal.

    Deliberately not a payment form: no card fields, no processor anywhere on
    this site. It takes an email and a phone number, hands them to the
    endpoint that mails the order to you and a confirmation to the customer,
    then opens WhatsApp so the conversation starts with the order already in
    it. If the mail step fails the WhatsApp hand-off still happens, so an
    order is never lost to a network error.
    """
    from lib import icon as _i
    return f"""          <div class="wside wside--cko" data-side="cko" hidden>
            <div class="cko__hd">
              <div>
                <h3 class="d4" id="cko-title">Where should we send your invoice?</h3>
                <p class="muted small" style="margin-top:6px">Your invoice and activation details go to
                  your email. Nothing is charged here.</p>
              </div>
              <button type="button" class="cko__back" data-checkout-close>
                {_i("chevron")}<span>Back</span></button>
            </div>

            <div class="cko__order">
              <div class="cko__order-top">
                <span class="eyebrow">Your order</span>
                <span class="muted xsmall" data-out-permonth-c>&asymp; $8.33 / month</span>
              </div>
              <div class="cko__order-main">
                <b data-out-summary>12 Months &middot; 1 device</b>
                <span class="cko__amount" data-out-total>$99.99</span>
              </div>
            </div>

            <form class="cko__form" data-checkout-form novalidate>
              <div class="field">
                <label class="label" for="cko-mail">Email address</label>
                <input class="input" id="cko-mail" name="email" type="email" inputmode="email"
                       autocomplete="email" placeholder="you@email.com" required>
                <p class="cko__err" data-err-for="email" hidden></p>
              </div>

              <div class="field" style="margin-bottom:0">
                <label class="label" for="cko-phone">WhatsApp number</label>
                <div class="cko__phone">
                  <select class="select" id="cko-dial" name="dial" aria-label="Country dialling code"></select>
                  <input class="input" id="cko-phone" name="phone" type="tel" inputmode="tel"
                         autocomplete="tel" placeholder="661 541 3954" required>
                </div>
                <p class="cko__err" data-err-for="phone" hidden></p>
                <p class="xsmall muted" style="margin-top:8px" data-dial-note></p>
              </div>

              <button type="submit" class="btn btn--primary btn--block cko__submit" style="margin-top:22px">
                <span data-cko-label>Place order &mdash; <b data-out-total>$99.99</b></span>
                {_i("arrow")}
              </button>

              <p class="cko__note"><b>No payment is taken on this page.</b> We send your invoice and
                payment instructions by email, and on WhatsApp.</p>
            </form>

            <div class="cko__done" data-checkout-done hidden>
              <span class="cko__tick">{_i("check")}</span>
              <h4 class="d4">Order received</h4>
              <p class="muted small" data-cko-done-msg>Check your email for the confirmation. We are
                opening WhatsApp so you can finish with a real person.</p>
              <p class="cko__ref">Reference <b data-cko-ref>&mdash;</b></p>
              <a href="#" class="btn btn--wa btn--block" data-cko-wa style="margin-top:18px">
                Continue on WhatsApp</a>
            </div>
          </div>"""


def steps_section():
    return f"""<section class="section section--alt" id="how">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">How it works</span>
      <h2 class="d2">Choose. Order. <span class="grad">Start watching.</span></h2>
      <p class="lede">No hardware, no contract, no waiting around.</p>
    </div>

    <div class="step reveal">
      <div class="step__num">01</div>
      <div class="step__body">
        <h3>Choose your plan</h3>
        <p>Pick your subscription length and how many devices need to watch at the same time.
           Every plan carries the same channels and the same library.</p>
      </div>
      <div>
        <a href="/pricing" class="mini-plan"><b>3 Months</b><span class="t">Try it out</span><span class="p">$39.99</span></a>
        <a href="/pricing" class="mini-plan"><b>6 Months</b><span class="t">Save $1.67/mo</span><span class="p">$69.99</span></a>
        <a href="/pricing" class="mini-plan is-best"><b>12 Months</b><span class="badge">Best value</span><span class="p">$99.99</span></a>
      </div>
    </div>

    <div class="step reveal">
      <div class="step__num">02</div>
      <div class="step__body">
        <h3>Send your order</h3>
        <p>Message us on WhatsApp or fill in the short order form. Tell us the device you plan to watch on and
           we send an invoice with payment instructions. Nothing is charged on this website.</p>
      </div>
      <div>
        <div class="card">
          <div class="row" style="gap:12px">
            <span class="card__icon" style="margin:0">{icon("wallet")}</span>
            <div><b style="font-family:var(--font-display)">Invoice by email &amp; WhatsApp</b>
              <div class="muted small">Card, Apple&nbsp;Pay, Google&nbsp;Pay, Revolut or Wise</div></div>
          </div>
          {_pay(["visa","mastercard","apple-pay","google-pay"], style=' style="margin-top:16px"')}
        </div>
      </div>
    </div>

    <div class="step reveal">
      <div class="step__num">03</div>
      <div class="step__body">
        <h3>Get activated</h3>
        <p>Once payment clears we send your login and a setup guide for your exact device. You are usually
           watching within 5 to 15 minutes.</p>
        <a href="/setup" class="btn btn--ghost" style="margin-top:20px">See the setup guides</a>
      </div>
      <div>
        <div class="mailcard">
          <div class="mailcard__top">
            <span class="mailcard__avatar">S</span>
            <div class="mailcard__from"><b>{BRAND}</b><span>no-reply@streamly4k.com</span></div>
            <span class="mailcard__when">Just now</span>
          </div>
          <div class="mailcard__subj">Subject &nbsp;Your {BRAND} login is ready</div>
          <h4>You're in. Start watching.</h4>
          <div class="credrow"><span>Portal</span><span>your-portal ••••</span></div>
          <div class="credrow"><span>Username</span><span>•••• •••• 57</span></div>
          <div class="credrow"><span>Expires</span><span>in 12 months</span></div>
        </div>
      </div>
    </div>
  </div>
</section>"""


# --------------------------------------------------------------------------
def why_section():
    cards = ""
    for ic, title, desc in data.INCLUDED:
        cards += f"""<div class="card card--hover">
      <span class="card__icon">{icon(ic)}</span>
      <h3>{title}</h3><p>{desc}</p>
    </div>"""
    return f"""<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Why {BRAND}</span>
      <h2 class="d2">Built to be the <span class="grad">only subscription</span> you need</h2>
      <p class="lede">One line-up, one price, one place to ask for help.</p>
    </div>
    <div class="grid g-4 reveal">{cards}</div>
  </div>
</section>"""


# --------------------------------------------------------------------------
def devices_section():
    """Setup cards, each headed by the platform marks it actually covers.

    MAG/Enigma2 has no brand mark in the set, so it keeps the generic glyph
    rather than borrowing someone else's — an icon has to mean what it shows.
    """
    from lib import platform as _plat
    MARKS = {
        "/setup/smart-tv":    ["samsung", "lg", "sony"],
        "/setup/firestick":   ["amazon"],
        "/setup/android":     ["android", "chromecast"],
        "/setup/iphone-ipad": ["apple", "appletv"],
        "/setup/pc-mac":      ["windows", "apple", "linux"],
    }
    cards = ""
    for ic, name, sub, href in data.DEVICES:
        keys = MARKS.get(href)
        head = ("".join(_plat(k) for k in keys) if keys else icon(ic))
        cls = "card__marks" if keys else "card__icon"
        cards += f"""<a href="{href}" class="card card--hover">
      <span class="{cls}">{head}</span>
      <h3>{name}</h3><p>{sub}</p>
      <span class="link-arrow small" style="margin-top:14px">Setup guide {icon("arrow")}</span>
    </a>"""
    return f"""<section class="section section--alt">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Works on what you own</span>
      <h2 class="d2">No new hardware. <span class="grad">No adapters.</span></h2>
      <p class="lede">If it streams, it works. Pick your device and follow the guide — it takes a few minutes.</p>
    </div>
    <div class="grid g-3 reveal">{cards}</div>
  </div>
</section>"""


# --------------------------------------------------------------------------
def platforms_rail():
    """"On any device" — two counter-scrolling rails of the platforms we cover.

    Two sizing rules make the loop seamless:

    * The shift is -(50% + gap/2). With the content duplicated, half the track
      falls half a gap short of one whole set, so a flat -50% jumps at the
      seam. The track is width:max-content so its box hugs the tiles — a
      stretched box makes 50% mean something other than one set.
    * Each half repeats the set REPEAT times. Two copies alone are not enough:
      once the track has travelled one set, only one set is left to cover the
      viewport, and on a wide monitor that leaves visible empty space at the
      right-hand end. Half the track has to be wider than the widest screen.

    The marks are emitted once into a hidden sprite and referenced with <use>,
    so repeating them costs a few bytes each instead of a full path.
    """
    from lib import PLATFORMS

    REPEAT = 3          # per half -> half is ~3.8k px wide, past any monitor
    seen, sprite = [], ""
    for row in data.DEVICE_RAIL:
        for mark, _ in row:
            if not mark.startswith("icon:") and mark not in seen:
                seen.append(mark)
    for key in seen:
        title, d = PLATFORMS[key]
        sprite += f'<symbol id="pm-{key}" viewBox="0 0 24 24"><path d="{d}"/></symbol>'
    sprite = (f'<svg class="drails__sprite" aria-hidden="true" focusable="false">'
              f'<defs>{sprite}</defs></svg>')

    def tile(mark, label):
        if mark.startswith("icon:"):
            glyph = icon(mark.split(":", 1)[1])
        else:
            glyph = (f'<svg viewBox="0 0 24 24" fill="currentColor" role="img" '
                     f'aria-label="{label}"><use href="#pm-{mark}"/></svg>')
        return f'<div class="dtile">{glyph}<b>{label}</b></div>'

    rails = ""
    for i, row in enumerate(data.DEVICE_RAIL):
        half = "".join(tile(m, l) for m, l in row) * REPEAT
        rails += (f'<div class="drail drail--{"r" if i == 0 else "l"}">'
                  f'<div class="drail__track">{half}{half}</div></div>')

    checks = "".join(
        f'<li>{icon("check")}<span>{c}</span></li>' for c in data.DEVICE_CHECKS
    )

    return f"""<section class="section section--alt devrail">
  {sprite}
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Watch your way</span>
      <h2 class="d2">{BRAND} on <span class="grad">any device</span></h2>
      <p class="lede">Set up {BRAND} on the devices you already use at home or on the go &mdash;
        including <a href="/setup/firestick">the Amazon Firestick</a>.</p>
      <p class="devrail__note"><b>Choose up to 5 devices with your plan.</b></p>
    </div>
  </div>
  <div class="drails reveal">{rails}</div>
  <div class="wrap">
    <ul class="dchecks reveal">{checks}</ul>
    <div class="center" style="margin-top:30px">
      <a href="/setup" class="btn btn--ghost reveal">See the setup guides {icon("arrow")}</a>
    </div>
  </div>
</section>"""
