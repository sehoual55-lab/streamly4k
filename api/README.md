# Order emails — what to set up

`order.js` is a Vercel serverless function. It runs beside the static site and
sends two emails whenever someone places an order in the checkout panel:

1. **To you** — the plan, total, the customer's email and phone number.
2. **To the customer** — a confirmation with their reference and plan.

It also handles **abandoned checkouts**: if someone types a valid email into
the panel and then leaves without ordering, you get one email with what they
had chosen and a ready-written follow-up (WhatsApp and mailto links that open
with the message already in them).

That follow-up goes to **you**, never automatically to the customer. Mailing
someone who never completed an order is the quickest way to get your sending
domain marked as spam, and in the UK/EU it needs a lawful basis you may not
have — so whether to reach out stays your call. Turn the whole thing off with
`order.abandon.enabled = false` in `assets/js/config.js`.

There are no card fields anywhere on this site, so this function never sees
payment details.

## The four environment variables

In Vercel: **Project → Settings → Environment Variables**.

| Name | Example | Needed |
|---|---|---|
| `RESEND_API_KEY` | `re_xxxxxxxx` | yes |
| `ORDER_TO` | `support@streamly4k.com` | yes |
| `ORDER_FROM` | `Streamly4K <orders@streamly4k.com>` | yes |
| `WHATSAPP` | `16615413954` | optional |

## Getting the key

1. Sign up at **resend.com** (the free tier covers a few thousand emails a month).
2. **Domains → Add domain →** `streamly4k.com`, then add the DNS records it
   gives you at your registrar. This step is what makes `ORDER_FROM` work —
   you cannot send from a domain you have not verified, and mail from an
   unverified domain lands in spam or bounces.
3. **API Keys → Create** → paste it into `RESEND_API_KEY`.

Redeploy after adding the variables — Vercel only picks them up on a new build.

## If you skip all this

Nothing breaks. The function returns `503`, the checkout treats the email step
as skipped, and the customer is still handed to WhatsApp with their order and
reference. You just do not get the email copy.

The same is true if Resend is down or slow: the checkout waits 8 seconds, then
completes anyway. An order is never lost to a failed email.

## Using a different provider

Swap the `send()` function for your provider's API. Everything else — the
validation, the escaping, the two templates — stays as it is.
