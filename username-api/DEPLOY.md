# Deploy `username-api` (free, no card required)

This walkthrough takes you from "code on GitHub" to "publicly reachable API on the internet" in about 10 minutes using **Koyeb** — a free Docker hosting platform that requires no credit card.

---

## Why Koyeb (not Render)

Render now requires a credit card on file even for their free tier (the card is not charged, but it is required for verification during Blueprint provisioning). If your card is declined or you prefer not to enter payment info, Koyeb is the replacement:

- **No credit card required** — free tier is accessible with just an email signup
- **Native Docker support** — reads your `Dockerfile` directly, no extra config files needed
- **Always-on free instance** — Koyeb's free tier does not sleep (unlike Render's free tier which sleeps after 15 min inactivity)
- **Automatic HTTPS** — public URL with TLS included

Free tier limits: 1 app, 512 MB RAM, shared CPU, 1 GB outbound bandwidth/month. More than enough for early RapidAPI traffic.

---

## Step 1 — Sign up for Koyeb

1. Go to **https://www.koyeb.com** and click **Get started for free**.
2. Sign up with your GitHub account (`shevasatrian`) — no card prompt.
3. Authorize Koyeb to read your GitHub repos.

---

## Step 2 — Create a new app

1. In the Koyeb dashboard, click **Create App**.
2. Choose **GitHub** as the deployment source.
3. Select the `shevasatrian/money-maker` repo.
4. **Branch:** `master`
5. **Service directory (root directory):** `username-api`

Koyeb auto-detects the `Dockerfile` inside `username-api/` and selects Docker as the build method.

---

## Step 3 — Configure the service

In the service configuration screen:

| Field | Value |
|---|---|
| **Builder** | Dockerfile (auto-detected) |
| **Run command** | *(leave blank — Dockerfile CMD is used)* |
| **Port** | `8000` |
| **Health check path** | `/` |
| **Instance type** | Free |
| **Regions** | Pick the one closest to you (or leave default) |

Environment variables — click **Add variable**:

| Key | Value |
|---|---|
| `PYTHONUNBUFFERED` | `1` |

Click **Deploy**.

---

## Step 4 — Wait for the build

Koyeb pulls your repo, builds the Docker image, and starts the container. First build takes 3–5 minutes (downloading the Python base image, installing fastapi + uvicorn + httpx).

When the status shows **Healthy**, Koyeb assigns a public URL. Your live URL is:

```
https://hot-olimpia-sheva-ee26b88b.koyeb.app
```

---

## Step 5 — Verify the deployment

```powershell
curl https://hot-olimpia-sheva-ee26b88b.koyeb.app/
curl https://hot-olimpia-sheva-ee26b88b.koyeb.app/platforms
curl https://hot-olimpia-sheva-ee26b88b.koyeb.app/check/torvalds
```

Expected results:
- `/` — JSON with service name, version, platform count, docs path
- `/platforms` — `default` (9 platforms) and `opt_in` (11 platforms) lists
- `/check/torvalds` — 9 platform results, all `taken`

Open `https://hot-olimpia-sheva-ee26b88b.koyeb.app/docs` in a browser for the Swagger UI.

---

## Auto-deploy on push

In Koyeb's service settings, enable **Auto-deploy** — every push to `master` on GitHub triggers a rebuild and redeploy automatically.

---

## Keeping the service warm

Koyeb's free tier does not sleep between requests, so cold-starts are not an issue. No pinger needed.

If you want uptime monitoring anyway (to get email alerts on crashes), sign up at **https://uptimerobot.com** (free) and add an HTTP monitor pointing to `https://hot-olimpia-sheva-ee26b88b.koyeb.app/`.

---

## Upgrade trigger

When monthly recurring revenue from RapidAPI exceeds ~$10/mo, consider Koyeb's Starter plan or Render's Starter plan ($7/mo) for a dedicated instance and higher bandwidth limits. Neither upgrade is needed at zero or early revenue.

---

## Troubleshooting

**Build fails with "Dockerfile not found":**
Confirm that **Service directory** is set to `username-api` (not the repo root). Koyeb looks for `Dockerfile` inside the service directory.

**Service starts but `/check/<username>` returns all `unknown`:**
The platform checks are hitting GitHub, GitLab, etc. from Koyeb's shared IP range. This is normal at low traffic. If it worsens, adding a short `time.sleep(0.5)` between batches in `core.py` can help avoid rate limits.

**Koyeb shows "Unhealthy" after deploy:**
The health check hits `GET /` — confirm the container is listening on port 8000. Check Koyeb's **Runtime logs** tab for the actual error.

---

## Render (alternative — requires card verification)

If you later get a working card or want to try Render, the repo already includes a `render.yaml` at the root that configures everything. Steps:

1. Sign up at **https://render.com** with your GitHub account.
2. **New → Blueprint** → select `shevasatrian/money-maker`.
3. Render reads `render.yaml`, previews one free Docker web service.
4. Enter payment info (required even for free tier) → click **Apply**.
5. Public URL assigned after ~5-minute build.

Render's free tier sleeps after 15 minutes of inactivity (30s cold-start on next request). Set up a UptimeRobot monitor on `https://<render-url>/` at 5-minute intervals to keep it warm.
