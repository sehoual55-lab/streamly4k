# Publishing on Namecheap (cPanel hosting)

Namecheap shared hosting runs Apache, not Node. Two consequences:

* The site itself works fine — it is static HTML.
* **`api/order.js` will never run there.** That file is a Vercel
  serverless function. Do not upload the `api/` folder; it does nothing on
  cPanel. Order emails go through **FormSubmit** instead, which runs in the
  browser and works on any host. See `EMAIL-SETUP.md`.

The upside: Namecheap gives you real mailboxes, so you can finally have
`support@streamly4k.com` — which is what FormSubmit needs.

---

## 1. Upload the site

Use `streamly4k-namecheap.zip` — it contains only what belongs on a web
server (no `build/`, no `api/`, no `node_modules/`, no `.git`).

1. cPanel → **File Manager** → open **public_html**.
2. Delete anything already in there (`default.html`, the parking page).
3. **Upload** the zip.
4. Right-click it → **Extract**, then delete the zip.

`index.html` must sit directly in `public_html`, not inside a subfolder.
If extracting created `public_html/streamly4k/`, move the contents up one
level.

### Check `.htaccess` arrived

It starts with a dot, so File Manager hides it by default:
**Settings** (top right) → tick **Show Hidden Files**.

It forces HTTPS, sets the security headers, serves `/404.html`, and caches
assets for a year. Without it the site still works, just slower and
without those headers.

---

## 2. Create the support mailbox

This is the piece that makes the order emails work.

1. cPanel → **Email Accounts** → **Create**.
2. Address `support`, domain `streamly4k.com`, set a password.
3. Open **Webmail** (cPanel → Email Accounts → Check Email) and keep that
   tab handy.

Optional but easier: **Forwarders** → forward `support@streamly4k.com` to
your Gmail, so everything lands in one inbox.

---

## 3. Switch the emails on

`assets/js/config.js` already has:

```js
formsubmit: "support@streamly4k.com",
```

Now that the mailbox exists, that address works.

1. Open the live site and place one test order.
2. FormSubmit emails `support@streamly4k.com` a **confirmation link** —
   check Webmail, including the spam folder.
3. Click it once.
4. Place another test order. It arrives, and the customer gets the
   auto-reply.

If it still does not arrive, press **F12 → Console** on the site and place
an order. The page prints the reason.

---

## 4. Point the domain

If the domain is registered at Namecheap and hosted there too, it is
usually already pointed. Otherwise:

**Domain List → Manage → Nameservers → Namecheap BasicDNS**, or set the
nameservers cPanel gave you in the welcome email. DNS takes anywhere from
minutes to a few hours.

### SSL

cPanel → **SSL/TLS Status** → select the domain → **Run AutoSSL**. Free,
and takes a few minutes. Do this before testing — `.htaccess` forces
HTTPS, so without a certificate the browser will warn.

---

## Updating the site later

Edit the source, run `python3 build/build.py`, then re-upload the changed
files through File Manager. The generator rewrites every page, so for a
content change it is simplest to re-upload the whole thing.

---

## Namecheap vs Vercel

| | Namecheap | Vercel |
|---|---|---|
| Static site | ✅ | ✅ |
| `api/order.js` | ❌ never runs | ✅ |
| FormSubmit / EmailJS | ✅ | ✅ |
| Mailboxes at your domain | ✅ included | ❌ separate service |
| Deploying an update | upload files | `git push` |
| Free SSL | AutoSSL | automatic |

You can also use both: Namecheap for `support@streamly4k.com`, Vercel for
the site. Point the domain's MX records at Namecheap and the A record at
Vercel.
