# Putting this on GitHub and Vercel

Two commands and three clicks. The repo is already committed on branch
`main` with a `.gitignore` — nothing to clean up first.

## 1. GitHub

Create an empty repository at <https://github.com/new>. Do **not** tick
"Add a README" — the repo already has history and an extra commit would
make the first push conflict.

Then, from this folder:

```bash
git remote add origin https://github.com/YOUR-USERNAME/streamly4k.git
git push -u origin main
```

## 2. Vercel

1. <https://vercel.com/new> → **Import** the repo you just pushed.
2. Framework preset: **Other**. Leave the build command empty and set the
   output directory to `./` — this is a static site with one serverless
   function, so there is nothing to build.
3. **Deploy.**

Vercel picks up `api/order.js` automatically because it sits in `/api`.

## 3. The environment variables

Without these the site works but sends no email. In Vercel →
**Settings → Environment Variables**:

| Name | Value |
|---|---|
| `RESEND_API_KEY` | your key from resend.com |
| `ORDER_TO` | support@streamly4k.com |
| `ORDER_FROM` | `Streamly4K <orders@streamly4k.com>` |
| `WHATSAPP` | 16615413954 |

Add them to **Production, Preview and Development**, then **redeploy** —
Vercel only reads them at build time, so an existing deployment will not
pick them up.

Before `ORDER_FROM` works, verify `streamly4k.com` at Resend
(**Domains → Add domain**) and add the DNS records they give you at your
registrar. Mail from an unverified domain bounces or lands in spam.

## 4. Check it

Place one test order with your own email. You should get two messages
within a few seconds: the order notification and the customer copy.

If nothing arrives, open **Vercel → your project → Logs** and place
another order. `mail_not_configured` means a variable is missing or you
have not redeployed since adding them.

## The domain

Vercel gives you a `*.vercel.app` URL immediately. To use
`streamly4k.com`, go to **Settings → Domains → Add**, then point the
registrar at the records Vercel shows.
