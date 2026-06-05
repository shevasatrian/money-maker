# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **two-track income project**, not a single application. See `README.md` for the user-facing pitch, and `C:\Users\User\.claude\plans\what-can-make-money-validated-torvalds.md` for the strategic plan that drove every structural decision.

- **`passive-earners/`** is **docs only** — Track A is just walkthroughs for installing external bandwidth-sharing apps (Honeygain, EarnApp, etc.) on the user's PC. The apps live external to the repo. Do not look for or create code under `passive-earners/`.
- **`username-api/`** is **the only code**. A FastAPI service whose value is being listed on RapidAPI, where marketplace discovery substitutes for marketing.

## Run the API locally

The Python venv lives inside `username-api/` (self-contained). On Windows PowerShell:

```powershell
cd D:\Money-maker\username-api
.\.venv\Scripts\python.exe -m uvicorn api.main:app --reload
```

Then `http://127.0.0.1:8000/docs` for the Swagger UI. There are no tests, no linter, and no CI — this was a deliberate "smallest possible v0" choice; resist adding them unless the user asks.

To smoke-test from a shell:

```bash
curl http://127.0.0.1:8000/check/torvalds       # known taken on github/gitlab/soundcloud
curl http://127.0.0.1:8000/platforms            # default + opt-in lists
```

## Deploy

There is no local deploy command. The live service runs on **Koyeb** (free tier, no card required) at:

```
https://hot-olimpia-sheva-ee26b88b.koyeb.app
```

The GitHub repo is `github.com/shevasatrian/money-maker` on branch `master`. Koyeb is configured to auto-deploy from that repo with `workdir: username-api` and the Docker builder. See `username-api/DEPLOY.md` for the full walkthrough and Koyeb API setup details.

`render.yaml` still exists at the repo root as a fallback for Render Blueprint deployment. Do not move it inside `username-api/` — Render Blueprints only read it from the repo root. Render now requires card verification even for free tier; Koyeb does not.

## Architecture of `username-api/`

Two-file split, intentionally small:

- **`api/core.py`** — pure logic. Defines `Platform` dataclasses in the `PLATFORMS` tuple, the async `check_username()` function, and a small validator. No FastAPI, no HTTP framework dependencies.
- **`api/main.py`** — thin FastAPI layer. Three endpoints: `/`, `/platforms`, `/check/{username}`. Also defines four Pydantic response models (`HealthResponse`, `PlatformsResponse`, `CheckResponse`, `PlatformCheckResult`) that drive the OpenAPI schema RapidAPI imports. Keep these models rich — they are the listing's public documentation.

When the user asks to add a platform, edit `PLATFORMS` in `core.py`. The architecture supports three classification mechanisms per platform, in priority order:

1. **HTTP status code matching** — `available_codes` / `taken_codes` tuples. The most reliable signal.
2. **Body regex** — `available_body_regex` and `taken_body_regex`, used for SPAs that return 200 for everything. Inspected only on 2xx responses.
3. **`enabled` flag** — controls whether a platform is in the default check set or opt-in only.

## Non-obvious platform-set decisions (read before adding/changing platforms)

The default platform set was deliberately pruned to 9 reliable platforms during a smoke-test session. The 11 opt-in platforms (Reddit, npm, Pinterest, Twitch, PyPI, Bitbucket, Medium, Product Hunt, Patreon, Substack, Buy Me a Coffee) were moved out of the default set for specific reasons recorded in `core.py` comments — **TLS handshake failures, Cloudflare/Akamai bot challenges, SPA behavior returning 200 for everything, or identical responses for real and fake users**.

Do not "fix" these by moving them back into the default set without re-verifying the underlying behavior changed. Instagram, TikTok, X/Twitter, and Facebook are deliberately not in the catalog at all — they aggressively block automated checks and have ToS clauses against this kind of lookup.

## Constraints that shape every decision

These came from the user up front and override default engineering instincts:

- **$0 hosting** — Koyeb's free tier is the current host (no card required). Render now requires card verification even for free tier. Fly.io requires a card too. Don't suggest paid alternatives unless the user explicitly opens that door.
- **No marketing** — the entire deployment-to-RapidAPI flow exists to substitute marketplace discovery for marketing. Don't suggest social/audience growth strategies.
- **Daily trickle, not moonshot** — targets are $0.50-$2/day from Track A and $1-$15/day per API from Track B. The user prefers small reliable daily income over big launches.

These constraints are also captured in `C:\Users\User\.claude\projects\D--Money-maker\memory\user_money_goals.md` (auto-loaded into your context as user memory).

## Adding a second API

The plan calls for adding a second API niche once `username-api` hits ~$5/day on RapidAPI, then a third after that. When the user asks for this, mirror the `username-api/` structure: a sibling directory with its own `api/`, `Dockerfile`, `README.md`, `DEPLOY.md`, `EARNINGS.md`, and `RAPIDAPI.md`. Add a new service entry to the root `render.yaml` (Render fallback) and deploy the new service on Koyeb as a separate app. The strategic plan file lists candidate niches under "Niche directions worth scouting."
