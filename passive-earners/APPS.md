# Track A — Per-app deep dive

Install the apps in the order below. After each install, sign in, leave the app running, then move to the next.

**General install pattern for all five apps on Windows 11:**
1. Download the Windows installer from the official site (links below).
2. Run the installer; allow Windows Defender to elevate if prompted.
3. Launch the app, create an account or sign in.
4. Enable "Start on system boot" in the app's settings (every app has this, usually labeled "Run on startup" or "Launch with Windows").
5. Verify the app's dashboard shows a non-zero status indicator within a few minutes.

After 24 hours, check each dashboard — you should see "earned today" numbers in the cents.

---

## 1. Honeygain — the baseline

- **Signup:** https://honeygain.com — click "Sign Up", create an account.
- **Download:** the Windows installer is on the dashboard after signup, or directly at https://honeygain.com/download.
- **What it sells:** residential bandwidth, mostly to data-aggregation and ad-verification firms.
- **Realistic daily earnings:** $0.20-$0.80 on a typical US/EU home connection. Capped at $30/month per device per their ToS.
- **Payout:** $20 minimum, via PayPal or BTC. Approximately monthly cadence.
- **Stacks safely with:** EarnApp, Pawns.app, Repocket. Not PacketStream (see below).
- **Risks/ToS:** Don't run multiple Honeygain instances on the same IP — they detect and ban. One PC, one account.
- **Verdict:** **Install.** This is the highest-paying single app in the category and the foundation of any stack.

## 2. EarnApp — the second-highest payer

- **Signup:** https://earnapp.com — sign in with Google or email.
- **Download:** Windows installer is on the dashboard.
- **What it sells:** residential bandwidth via Bright Data's SDK (BrightData is the corporate parent — they're the largest residential-proxy network in the world).
- **Realistic daily earnings:** $0.10-$0.50 on a US/EU connection.
- **Payout:** $1 minimum (lowest threshold of any app in this list), via PayPal, BTC, Tether, or Amazon gift card. Monthly.
- **Stacks safely with:** Honeygain, Pawns.app, Repocket. Bright Data is huge and well-behaved.
- **Risks/ToS:** Pay attention to Bright Data's Acceptable Use docs — same general "no corporate networks" rule applies.
- **Verdict:** **Install.** Lowest payout threshold means you see real money fastest with this one.

## 3. Pawns.app — bandwidth + occasional surveys

- **Signup:** https://pawns.app — create account.
- **Download:** Windows app from the dashboard.
- **What it sells:** residential bandwidth, plus occasionally prompts you with paid surveys (a few cents each, 5-10 minutes).
- **Realistic daily earnings:** $0.10-$0.40 bandwidth + variable survey income (if you bother).
- **Payout:** $5 minimum via PayPal or BTC. Approximately weekly cadence once you cross threshold.
- **Stacks safely with:** Honeygain, EarnApp, Repocket. Note: Pawns.app and IPRoyal Pawns are the same company; don't install both.
- **Risks/ToS:** Standard residential-proxy ToS.
- **Verdict:** **Install.** Solid stacker. Skip the surveys unless you have idle time — the hourly rate on surveys is bad.

## 4. Repocket — the small stacker

- **Signup:** https://repocket.com — create account.
- **Download:** Windows installer from the dashboard.
- **What it sells:** residential bandwidth, smaller network than the above three.
- **Realistic daily earnings:** $0.10-$0.40 on a US/EU connection.
- **Payout:** $20 minimum via PayPal. Monthly.
- **Stacks safely with:** Honeygain, EarnApp, Pawns.app.
- **Risks/ToS:** Their network is younger and the buyer pool is smaller, so daily earnings can swing more than the bigger networks.
- **Verdict:** **Install as a stacker.** Wouldn't bother running it alone, but it adds 30-50 cents/day on top of the others for no extra effort.

## 5. PacketStream — opt-in fifth slot

- **Signup:** https://packetstream.io — create account.
- **Download:** Windows app from the dashboard.
- **What it sells:** residential bandwidth, similar to the others but with a flat $0.10/GB rate that you can see in real time on the dashboard.
- **Realistic daily earnings:** $0.05-$0.30. Lower than the others because the rate is fixed and conservative.
- **Payout:** $5 minimum via PayPal. On-demand once you cross threshold.
- **Stacks safely with:** EarnApp, Pawns.app, Repocket. **Sometimes conflicts with Honeygain** on the same IP (both apps may compete for the same proxy buyer and one stops earning) — watch the dashboards for ~3 days; if Honeygain drops to $0/day after installing PacketStream, uninstall PacketStream.
- **Risks/ToS:** Standard residential-proxy ToS. They've been around since 2015, which is a good sign for legitimacy.
- **Verdict:** **Install as a stacker if you want every last cent.** Skip if you'd rather keep the setup minimal — Repocket gives similar earnings with less conflict risk.

---

## What NOT to install (commonly mentioned but skip them)

- **PrivadoVPN** — different category (VPN with built-in earning), conflicts with everything above.
- **MysteriumVPN node** — pays in MYST tokens, painful to convert, not worth it for solo home users.
- **Any "earn crypto by sharing CPU/GPU" app** — usually pays in obscure tokens, often masks crypto mining that destroys your hardware, never breaks even on electricity in the US/EU.
- **TraffMonetizer** — listed in many guides; ToS-aggressive about banning stackers. Skip.
- **Splynx, Bright SDK direct integrations** — for businesses, not solo users.

---

## After 30 days

By day 30 with a 4-5 app stack on a US/EU connection, your dashboards should show:
- Honeygain: $5-$20 earned, approaching first payout.
- EarnApp: $1+ already paid out at least once.
- Pawns.app: $3-$10 earned.
- Repocket: $2-$8 earned.
- PacketStream (if installed): $1-$5 earned.

Total: roughly **$15-$50/month** ($0.50-$1.65/day). That's the realistic ceiling for this track on one home IP. Don't try to push past it — additional accounts on the same IP get banned, and the legitimate game stops here.

When you hit this plateau, your attention should already be shifted to Track B (`username-api/`), which by then is starting to convert RapidAPI subscribers and has the potential to grow well past Track A's ceiling.
