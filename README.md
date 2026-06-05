# Money-maker

Two parallel tracks for earning a few dollars a day with $0 starting capital, comfortable coding skills, and no marketing.

**Track A — Passive earners** is install-and-leave. Bandwidth-sharing apps on your existing PC earn $0.50-$2/day starting within 24 hours. Low ceiling, no maintenance. Its job is to make sure money lands every day, immediately.

**Track B — `username-api`** is a small FastAPI service deployed free to Render and listed on RapidAPI. Marketplace discovery does the marketing for you. Slow start (weeks to first dollar), but the revenue compounds — and adding a second API later multiplies it.

---

## Layout

```
.
├── README.md                ← you are here
├── render.yaml              ← Render Blueprint (builds username-api/ via rootDir)
├── .gitignore
│
├── passive-earners/         ← Track A: docs only, apps live external
│   ├── README.md            ← overview, earnings, hard rules
│   └── APPS.md              ← per-app: signup, install, payout, stacking
│
└── username-api/            ← Track B: FastAPI service + docs
    ├── README.md            ← API reference (endpoints, examples, local dev)
    ├── DEPLOY.md            ← Render free-tier deploy walkthrough
    ├── EARNINGS.md          ← RapidAPI listing, pricing, revenue curve
    ├── Dockerfile
    ├── .dockerignore
    ├── api/                 ← FastAPI app
    └── .venv/               ← Python venv (gitignored)
```

## Where to start

1. **Today (30 min):** open `passive-earners/README.md`, then `APPS.md`, install the apps. Money starts trickling in within 24 hours.
2. **This week (10-20 hrs):** open `username-api/README.md` to understand the service, then `DEPLOY.md` to push it live on Render, then `EARNINGS.md` to list it on RapidAPI.

## Strategic context

The reasoning behind picking these two specific tracks (and rejecting alternatives like Etsy, Chrome extensions, trading bots, content monetization) is in the plan file at:

```
C:\Users\User\.claude\plans\what-can-make-money-validated-torvalds.md
```

Read it if you're tempted to swap one of these tracks for something else — the rejected alternatives are documented with reasons.

## Realistic combined trajectory

| Period | Track A | Track B | Combined daily |
|---|---|---|---|
| Week 1 | $0.30-$1.00 | $0 | **$0.30-$1.00** |
| Month 1 | $0.80-$1.80 | $0-$3 | **$0.80-$4.80** |
| Month 3 | $1.00-$2.00 (plateau) | $3-$10 | **$4-$12** |
| Month 6+ | $1.00-$2.00 (plateau) | $5-$15 per API, scale by adding more | **$10-$30+** |

This isn't get-rich. It's a "few dollars every day, growing slowly" plan, which is exactly what was asked for.
