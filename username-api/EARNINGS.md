# How `username-api` makes money

This is the revenue side of Track B. By the time you're here, you've already deployed to Render (`DEPLOY.md`) and have a public URL serving the API. The path from "public URL" to "money in your account" runs through RapidAPI.

---

## Why RapidAPI

RapidAPI is an **API marketplace**: developers go there to search for APIs the same way they go to npm to search for packages. That's the key property — discovery happens *inside the marketplace*, so you don't need to market the API anywhere else. List it, write decent copy, and developers searching for "check username availability" find it.

What RapidAPI also handles for you, for free:
- **Billing** — subscribers' credit cards go to RapidAPI; you get paid via PayPal or Stripe.
- **Auth** — every request carries an `X-RapidAPI-Key` header that identifies the subscriber. You don't write any auth code.
- **Rate limiting** — RapidAPI enforces the per-tier limits you configure (e.g., 100 requests/day on the free tier).
- **Analytics** — built-in dashboards show requests, conversions, and revenue.

You pay RapidAPI a **20% revenue share**. That's the trade for the discovery + billing infra.

---

## Step 1 — Provider signup

1. Go to **https://rapidapi.com/provider** and sign up.
2. Verify your email.
3. Add a payout method: PayPal or Stripe Connect. RapidAPI pays out monthly once you cross their threshold (typically $20).

---

## Step 2 — Add the API

1. From the provider dashboard: **Add New API**.
2. Choose **Use OpenAPI Spec → Import from URL**.
3. Paste: `https://<your-render-url>/openapi.json`
4. RapidAPI fetches the spec and auto-generates a listing draft: endpoints, parameters, example responses — all from the FastAPI metadata you already wrote.
5. Review the draft. Fix anything that looks weird (rare, since FastAPI's OpenAPI export is clean).

---

## Step 3 — Pricing template

Recommended four-tier setup. The free tier exists to convert subscribers to paid; the upper tiers exist to capture occasional high-volume users without leaving money on the table.

| Tier | Price | Quota | Overage | Purpose |
|---|---|---|---|---|
| **Basic** | Free | 100 requests/day | hard cap | Lets developers try the API; this is the discovery hook |
| **Pro** | $5/mo | 10,000 requests/month | $0.001/extra request | The default conversion target — light prod use |
| **Ultra** | $20/mo | 100,000 requests/month | $0.0005/extra request | High-volume apps; price/req drops to reward volume |
| **Mega** | Custom | unlimited | n/a | Enterprise; reply manually when someone clicks |

Why these specific numbers:
- **Free 100/day** is enough for a developer to integrate and test, not enough to run a production app — that forces a Pro upgrade for anything serious.
- **Pro at $5/mo** is the "no-decision price" — under $10/mo a developer doesn't escalate to their manager, they just expense it.
- **Ultra at $20/mo** captures the upper-middle of demand. Set the per-request overage on Pro low enough that 10k+ users naturally migrate to Ultra.

---

## Step 4 — Listing copy

This matters more than the code. RapidAPI's search ranks on title keywords and description quality. Use the README's title and first paragraph as a base, then tune for search:

**Title:** `Username Availability Checker API`
Use the exact phrase a developer would Google. Avoid clever brand names.

**Short description (one line):** `Check whether a username is available on 20+ social, dev, and creator platforms in a single API call.`

**Long description:** Paste the value-prop paragraph from `README.md`, plus a bulleted "use cases" list (indie hackers, brand teams, signup flows), plus one full example request/response (copy from the README).

**Tags:** `username`, `availability`, `social`, `branding`, `signup`, `developer-tools`, `username-checker`, `handle`.

**Categories:** Tools, Data, Social — pick three.

**Code examples:** RapidAPI auto-generates these in curl, JS, Python, Ruby, Go, etc. from the OpenAPI spec. Verify one of them actually works by copy-pasting into a terminal.

---

## Step 5 — Publish

Click Publish. The listing goes into RapidAPI's index, becomes searchable within a few hours, and may take 1-2 weeks to start ranking in the relevant search queries.

---

## Realistic revenue curve

| Period | What's happening | Expected daily revenue |
|---|---|---|
| **Week 1-2** | RapidAPI indexes the listing. Search ranking is low. Maybe 0-2 curious browsers/day, 0 signups. | **$0** |
| **Week 3-4** | First free-tier signups. ~3-5% convert to Pro within their trial period. | **$0-$3** |
| **Month 2** | Ranking stabilizes for your target keywords. Steady free-tier signups, ongoing Pro conversions. | **$1-$5** |
| **Month 3** | If listing copy is good, ~5-10 active paid subscribers. Maybe one Ultra. | **$3-$10** |
| **Month 6+** | Plateau on this single API. Compound by adding a second API (see scaling below). | **$5-$15 per API** |

These numbers assume *no marketing* — purely organic RapidAPI discovery. If you do post the API in a few relevant developer forums (one-time, not a campaign), the curve accelerates by ~3-4 weeks.

---

## Kill / scale decision tree

**After 4 weeks with 0 paid conversions:**
The niche is wrong, not the API. Kill the listing, redeploy the same Render infra for a different API from the niche list in the strategic plan file (`C:\Users\User\.claude\plans\what-can-make-money-validated-torvalds.md` → "Niche directions worth scouting"). Don't sink-cost.

**After 4 weeks with 1-3 paid subscribers:**
Working but slow. Tune the listing copy (better title keywords, more use-case bullets, screenshots) and wait another month before deciding.

**After 4 weeks with 5+ paid subscribers:**
This niche works. Don't touch it. Start building a second API in an adjacent niche — disposable-email detection, profanity classification, color-palette extraction. RapidAPI listings cross-link by provider; a second listing both earns separately AND drives traffic back to the first.

---

## Scaling: when to add API #2

Trigger: API #1 hits **$5/day** sustained for a month. That signals you've found a real niche and the marketplace flywheel is working.

Pick the second niche from the strategic plan's list. Reuse the same Render Docker pattern, the same FastAPI scaffolding, the same RapidAPI listing template. The second API takes a fraction of the time to ship because the infra is already proven.

Two APIs at $5-10/day each = $10-$20/day. Three is $15-$30/day. That's the path to the "few dollars every day" goal compounding into real money.

---

## Tax note (US)

RapidAPI payouts come via PayPal or Stripe Connect. In the US, the IRS treats this as self-employment income; once you cross **$600/year**, RapidAPI files a 1099-NEC for you. Keep records of:
- Render hosting costs (deductible business expense)
- Domain costs if you ever buy one
- Any tooling subscriptions used to build/maintain the API

Treat the first few dollars as "interesting data, not material income" for tax purposes; once you're at $50+/month sustained, talk to a tax person about quarterly estimated payments. (Non-US users: check your local rules on hobby vs. business income.)
