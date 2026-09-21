# Getting the order emails working

Three ways. **Option A is already switched on** — it needs one click and
nothing else.

---

## Option A — FormSubmit (already on, no account needed)  ← START HERE

Nothing to sign up for. It is configured in `assets/js/config.js`:

```js
formsubmit: "support@streamly4k.com",
```

**Change that to an inbox you can open right now.** If
`support@streamly4k.com` is not a real mailbox yet, put your own address
there — the activation email has to land somewhere you can read.

Then:

1. Place one test order on the site (local file, 127.0.0.1, anywhere).
2. FormSubmit emails that address a **confirmation link**. Click it once.
3. Place another test order. Now it arrives — and the customer gets the
   auto-reply too.

That is the whole setup. The customer's copy is the `autoReply` text in
the same config block; edit the wording there.

Abandoned checkouts come to you with the same one-time activation, and
deliberately send the customer nothing.

**The catch:** the emails are plain text, not the designed HTML ones, and
your address sits in the page source where a scraper can find it. Fine to
launch with. Move to Option B or C when you have ten minutes.

---

## Option B — EmailJS (styled emails, no server)

EmailJS sends from the browser, so it works on your laptop, on a local
server, and on any host. Free tier is 200 emails a month.

### 1. Create the account and connect your inbox

1. Sign up at <https://www.emailjs.com>.
2. **Email Services → Add New Service → Gmail** (or whatever you use) and
   connect the mailbox the orders should come from. Copy the **Service ID**
   (looks like `service_ab12cde`).
3. **Account → General** and copy the **Public Key**.

### 2. Create the templates

**Email Templates → Create New Template**, three times. For each one set
the **To Email** field to `{{to_email}}` — the site fills it in, which is
what lets the same service mail both you and the customer.

---

#### Template 1 — new order (goes to you)

*Subject:* `New order {{ref}} — {{total}} {{plan}}`

```
New order from the website.

Reference : {{ref}}
Plan      : {{plan}}
Total     : {{total}}
Per month : {{per_month}}

Email     : {{customer_email}}
Phone     : {{customer_phone}}
Placed    : {{placed_at}}

Reply to this email to reach them, or message {{customer_phone}} on WhatsApp.
```

Set **Reply To** to `{{customer_email}}` so hitting reply goes to the buyer.
Copy the **Template ID**.

---

#### Template 2 — confirmation (goes to the customer)

*Subject:* `Your {{brand}} order {{ref}}`

```
Thanks — we have your order.

Your reference is {{ref}}. Nothing has been charged yet. We will send your
invoice and payment options next, and your login details follow within
5–15 minutes of payment.

Plan      : {{plan}}
Total     : {{total}}
Per month : {{per_month}}

Fastest route is WhatsApp: {{whatsapp}}

Did not place this order? Ignore this email — nothing happens until you pay
an invoice.

{{brand}}
```

---

#### Template 3 — abandoned checkout (goes to you)

*Subject:* `Abandoned checkout — {{customer_email}}`

```
Someone filled in the order panel and left without placing the order.
Nothing has been sent to them.

Plan they had : {{plan}}
Total         : {{total}}
Email         : {{customer_email}}
Phone         : {{customer_phone}}
Page          : {{page}}
Left at       : {{placed_at}}

One nudge is a service. A second one is spam — if they do not reply, leave it.
```

This one is optional. Leave `templateAbandoned` empty to skip it.

### 3. Paste the four ids into the site

In `assets/js/config.js`:

```js
emailjs: {
  publicKey:         "YOUR_PUBLIC_KEY",
  serviceId:         "service_ab12cde",
  templateOrder:     "template_xxxxxxx",
  templateCustomer:  "template_yyyyyyy",
  templateAbandoned: "template_zzzzzzz"
},
```

Reload and place a test order. Both emails should arrive within seconds.

### 4. Lock it down

The public key is visible in the page — that is how EmailJS is designed to
work, but it means someone could call it from elsewhere. In **Account →
Security**, turn on **Allow only these domains** and add `streamly4k.com`.
Do that once the site is live.

---

## Option C — the serverless function (`api/order.js`)

Better long term: the key never reaches the browser, and it cannot be
abused from another site. It needs the site deployed to Vercel.

1. Deploy the repo (see `DEPLOY.md`).
2. **Settings → Environment Variables**, for Production, Preview *and*
   Development:

   | Name | Value |
   |---|---|
   | `RESEND_API_KEY` | key from resend.com |
   | `ORDER_TO` | support@streamly4k.com |
   | `ORDER_FROM` | `Streamly4K <orders@streamly4k.com>` |
   | `WHATSAPP` | 16615413954 |

3. **Redeploy.** Vercel reads these at build time — an existing deployment
   will not pick them up.
4. At Resend, **Domains → Add domain** for `streamly4k.com` and add the DNS
   records at your registrar. Mail from an unverified domain bounces.

Leave `formsubmit` and `emailjs.publicKey` empty and this path is used.

---

## Checking which one is running

Open the site, press F12 → **Network**, then place an order.

* a request to `formsubmit.co` → Option A is live
* a request to `api.emailjs.com` → Option B is live
* a request to `/api/order` → Option C; its response says what is wrong
  (`mail_not_configured` = variables missing or not redeployed)
* neither → both are unconfigured; the order still reaches WhatsApp

## Why no email arrives on a local preview

`api/order.js` only exists on a deployed Vercel site. Opening the HTML from
your computer, or serving it on `127.0.0.1`, means there is nothing at
`/api/order`, so the checkout skips the email and goes to WhatsApp. That is
deliberate — an order is never lost to a mail failure.

**FormSubmit and EmailJS have no such limitation** — both send from the
browser, so they work on a local file.
