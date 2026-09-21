/* ==========================================================================
   POST /api/order  —  sends two emails for one order
   --------------------------------------------------------------------------
   A static site cannot send mail, so this runs as a Vercel serverless
   function next to it. It takes the order the checkout panel posted and
   sends:

     1. a notification to you, with the customer's email and phone
     2. a confirmation to the customer, with the plan they picked

   It NEVER touches payment details — the site has no card fields.

   Set these in Vercel -> Project -> Settings -> Environment Variables:

     RESEND_API_KEY   an API key from resend.com (free tier is plenty)
     ORDER_TO         where your notifications go, e.g. support@streamly4k.com
     ORDER_FROM       a verified sender, e.g. "Streamly4K <orders@streamly4k.com>"
     WHATSAPP         digits only, e.g. 16615413954   (optional, used in the
                      customer email's button)

   Resend needs the sending DOMAIN verified before ORDER_FROM will work —
   that is a DNS step on their dashboard, not something the site can do.

   If any variable is missing the function returns 503 and the checkout
   still hands the customer to WhatsApp, so no order is lost.
   ========================================================================== */

const BRAND = "Streamly4K";
const SITE = "https://streamly4k.com";

function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, (c) => (
    { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]
  ));
}

/* Email clients strip <style> blocks and ignore most modern CSS, so every
   rule here is inline and the layout is a table. Dark background with the
   brand orange, to match the site. */
function shell(title, inner) {
  return `<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(title)}</title></head>
<body style="margin:0;padding:0;background:#080605;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#080605;padding:32px 16px;">
<tr><td align="center">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
         style="max-width:520px;background:#131010;border:1px solid #241E1B;border-radius:18px;overflow:hidden;">
    <tr><td style="padding:26px 28px 0;">
      <span style="font:800 21px/1 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#F6F1EE;letter-spacing:-.6px;">
        Streamly<span style="color:#FF4D2E;">4K</span></span>
    </td></tr>
    ${inner}
    <tr><td style="padding:22px 28px 28px;border-top:1px solid #241E1B;">
      <p style="margin:0;font:400 12px/1.6 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#8E837E;">
        ${esc(BRAND)} · <a href="${SITE}" style="color:#8E837E;">${SITE.replace("https://", "")}</a><br>
        You received this because this address was used to place an order.
      </p>
    </td></tr>
  </table>
</td></tr></table></body></html>`;
}

function row(label, value) {
  return `<tr>
    <td style="padding:9px 0;font:400 13px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#8E837E;">${esc(label)}</td>
    <td align="right" style="padding:9px 0;font:600 13px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#F6F1EE;">${esc(value)}</td>
  </tr>`;
}

function ownerEmail(o) {
  return shell(`New order ${o.ref}`, `
    <tr><td style="padding:18px 28px 0;">
      <h1 style="margin:0;font:800 22px/1.3 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#F6F1EE;letter-spacing:-.4px;">
        New order — ${esc(o.ref)}</h1>
      <p style="margin:8px 0 0;font:400 14px/1.6 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#C9BEB8;">
        Placed from the checkout panel. Send the invoice and activation details.</p>
    </td></tr>
    <tr><td style="padding:18px 28px 4px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
             style="background:#1A1614;border:1px solid #241E1B;border-radius:12px;padding:6px 16px;">
        ${row("Plan", o.plan || "—")}
        ${row("Total", o.total || "—")}
        ${row("Per month", o.perMonth || "—")}
        ${row("Email", o.email)}
        ${row("Phone", o.phone)}
        ${row("Placed", new Date().toUTCString())}
      </table>
    </td></tr>
    <tr><td style="padding:18px 28px 6px;">
      <a href="https://wa.me/${esc((process.env.WHATSAPP || "").replace(/\D/g, ""))}"
         style="display:inline-block;background:#25D366;color:#fff;text-decoration:none;
                font:700 14px/1 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
                padding:13px 20px;border-radius:12px;">Open WhatsApp</a>
      <a href="mailto:${esc(o.email)}"
         style="display:inline-block;margin-left:8px;background:#1A1614;color:#F6F1EE;text-decoration:none;
                border:1px solid #241E1B;font:700 14px/1 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
                padding:13px 20px;border-radius:12px;">Reply by email</a>
    </td></tr>`);
}

function customerEmail(o) {
  const wa = (process.env.WHATSAPP || "").replace(/\D/g, "");
  return shell(`Your ${BRAND} order ${o.ref}`, `
    <tr><td style="padding:18px 28px 0;">
      <h1 style="margin:0;font:800 23px/1.3 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#F6F1EE;letter-spacing:-.4px;">
        Thanks — we have your order.</h1>
      <p style="margin:10px 0 0;font:400 15px/1.65 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#C9BEB8;">
        Your reference is <b style="color:#FF9A3D;">${esc(o.ref)}</b>. Nothing has been charged yet —
        we will send your invoice and payment options next, and your login details follow within
        5–15 minutes of payment.</p>
    </td></tr>
    <tr><td style="padding:20px 28px 4px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
             style="background:#1A1614;border:1px solid #241E1B;border-radius:12px;padding:6px 16px;">
        ${row("Plan", o.plan || "—")}
        ${row("Total", o.total || "—")}
        ${row("Per month", o.perMonth || "—")}
      </table>
    </td></tr>
    ${wa ? `<tr><td style="padding:20px 28px 6px;">
      <a href="https://wa.me/${esc(wa)}"
         style="display:block;text-align:center;background:#25D366;color:#fff;text-decoration:none;
                font:700 15px/1 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
                padding:15px 20px;border-radius:12px;">Finish on WhatsApp</a>
      <p style="margin:12px 0 0;text-align:center;font:400 12px/1.6 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#8E837E;">
        Fastest route — we usually reply in minutes, 24/7.</p>
    </td></tr>` : ""}
    <tr><td style="padding:16px 28px 6px;">
      <p style="margin:0;font:400 13px/1.65 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#8E837E;">
        Did not place this order? Ignore this email — nothing happens until you pay an invoice.</p>
    </td></tr>`);
}

/* The abandoned-cart notice. It goes to YOU, never to the customer:
   emailing someone who never completed an order is a fast route to spam
   complaints, and in the UK/EU it needs a lawful basis you may not have.
   So this hands you a one-click follow-up and lets you decide. */
function abandonedEmail(o) {
  const wa = (process.env.WHATSAPP || "").replace(/\D/g, "");
  const firstLine = `Hi — you started an order with ${BRAND}`
    + (o.plan ? ` (${o.plan})` : "")
    + ` but did not finish. Was something unclear, or did you hit a problem?`
    + ` Reply here and we will sort it out — and if you would rather not hear`
    + ` from us again, just say so and we will not write twice.`;
  const mailto = `mailto:${encodeURIComponent(o.email)}`
    + `?subject=${encodeURIComponent("Your " + BRAND + " order")}`
    + `&body=${encodeURIComponent(firstLine)}`;
  const waLink = wa
    ? `https://wa.me/${(o.phone || "").replace(/\D/g, "") || wa}?text=${encodeURIComponent(firstLine)}`
    : "";

  return shell(`Abandoned checkout — ${o.email}`, `
    <tr><td style="padding:18px 28px 0;">
      <h1 style="margin:0;font:800 22px/1.3 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#F6F1EE;letter-spacing:-.4px;">
        Abandoned checkout</h1>
      <p style="margin:8px 0 0;font:400 14px/1.6 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#C9BEB8;">
        Someone filled in the order panel and left without placing the order.
        Nothing has been sent to them.</p>
    </td></tr>
    <tr><td style="padding:18px 28px 4px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
             style="background:#1A1614;border:1px solid #241E1B;border-radius:12px;padding:6px 16px;">
        ${row("Plan they had", o.plan || "—")}
        ${row("Total", o.total || "—")}
        ${row("Email", o.email)}
        ${row("Phone", o.phone || "not entered")}
        ${row("Page", o.page || "—")}
        ${row("Left at", new Date().toUTCString())}
      </table>
    </td></tr>
    <tr><td style="padding:16px 28px 0;">
      <p style="margin:0 0 10px;font:600 13px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#8E837E;">
        Ready to send — both open with the message already written:</p>
      ${waLink ? `<a href="${waLink}"
         style="display:inline-block;background:#25D366;color:#fff;text-decoration:none;
                font:700 14px/1 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
                padding:13px 20px;border-radius:12px;">Message on WhatsApp</a>` : ""}
      <a href="${mailto}"
         style="display:inline-block;margin-left:8px;background:#1A1614;color:#F6F1EE;text-decoration:none;
                border:1px solid #241E1B;font:700 14px/1 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
                padding:13px 20px;border-radius:12px;">Email them</a>
    </td></tr>
    <tr><td style="padding:16px 28px 6px;">
      <p style="margin:0;font:400 12px/1.65 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#8E837E;">
        One nudge is a service. A second one is spam — if they do not reply, leave it.</p>
    </td></tr>`);
}

async function send(key, payload) {
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!r.ok) throw new Error(`resend ${r.status}: ${await r.text()}`);
  return r.json();
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "method_not_allowed" });
  }

  const key  = process.env.RESEND_API_KEY;
  const to   = process.env.ORDER_TO;
  const from = process.env.ORDER_FROM;
  if (!key || !to || !from) {
    // Not configured yet. The checkout treats this as "email skipped" and
    // still sends the customer to WhatsApp.
    return res.status(503).json({ error: "mail_not_configured" });
  }

  const b = typeof req.body === "string" ? JSON.parse(req.body || "{}") : (req.body || {});
  const isAbandoned = b.type === "abandoned";
  const o = {
    page: String(b.page || "").slice(0, 80),
    ref: String(b.ref || "").slice(0, 32),
    email: String(b.email || "").trim().slice(0, 160),
    phone: String(b.phone || "").trim().slice(0, 40),
    plan: String(b.plan || "").slice(0, 120),
    total: String(b.total || "").slice(0, 40),
    perMonth: String(b.perMonth || "").slice(0, 40),
  };
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(o.email) || !o.ref) {
    return res.status(400).json({ error: "bad_request" });
  }

  try {
    if (isAbandoned) {
      // Only you are mailed here. The customer gets nothing — see the note
      // on abandonedEmail().
      await send(key, {
        from, to: [to], reply_to: o.email,
        subject: `Abandoned checkout — ${o.email}${o.total ? " (" + o.total + ")" : ""}`,
        html: abandonedEmail(o),
      });
      return res.status(200).json({ ok: true, type: "abandoned" });
    }

    // The notification to you is the one that must not fail — it is the
    // order itself. The customer confirmation is best-effort.
    await send(key, {
      from, to: [to], reply_to: o.email,
      subject: `New order ${o.ref} — ${o.total || ""} ${o.plan || ""}`.trim(),
      html: ownerEmail(o),
    });
    send(key, {
      from, to: [o.email],
      subject: `Your ${BRAND} order ${o.ref}`,
      html: customerEmail(o),
    }).catch(() => {});
    return res.status(200).json({ ok: true, ref: o.ref });
  } catch (e) {
    console.error("order mail failed:", e && e.message);
    return res.status(502).json({ error: "mail_failed" });
  }
}
