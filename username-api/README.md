# Username Availability Checker API

Check whether a username is available on 20 popular platforms — GitHub, GitLab, dev.to, Dribbble, Behance, SoundCloud, Gumroad, Vimeo, Hashnode by default, plus 11 more on opt-in — in a single API call.

Built for:
- **Indie hackers** picking a handle before they launch
- **Brand teams** vetting a product name across socials and developer registries
- **Signup flows** that suggest "this handle is also free on X, Y, Z"

The API issues HTTP requests in parallel and returns a per-platform `available` / `taken` / `unknown` verdict plus the canonical profile URL.

This README is the API reference. For the steps to ship and earn from it, see:
- **`DEPLOY.md`** — push to GitHub and deploy to Render's free tier
- **`EARNINGS.md`** — list on RapidAPI, pricing tiers, realistic revenue curve

---

## Endpoints

### `GET /check/{username}`

Check a single username across all supported platforms (or a filtered subset).

**Path parameters**
- `username` — 1-39 chars: letters, digits, `.`, `-`, `_`

**Query parameters**
- `platforms` *(optional)* — comma-separated list, e.g. `github,gitlab,soundcloud`. Omit to check all default platforms. Use `GET /platforms` to see which names are valid.

**Example**

```bash
curl "https://<your-render-url>/check/torvalds?platforms=github,gitlab,soundcloud"
```

```json
{
  "username": "torvalds",
  "duration_ms": 612,
  "summary": {"available": 0, "taken": 3, "unknown": 0},
  "results": [
    {"platform": "github",     "status": "taken", "url": "https://github.com/torvalds",     "http_status": 200, "error": null},
    {"platform": "gitlab",     "status": "taken", "url": "https://gitlab.com/torvalds",     "http_status": 200, "error": null},
    {"platform": "soundcloud", "status": "taken", "url": "https://soundcloud.com/torvalds", "http_status": 200, "error": null}
  ]
}
```

### `GET /platforms`

Returns the list of supported platform identifiers, split into `default` (checked when `?platforms=` is omitted) and `opt_in` (must be requested explicitly).

### `GET /`

Health check and metadata.

### `GET /docs`

Auto-generated OpenAPI/Swagger UI — best place to try the API in a browser.

---

## Supported platforms

**Default (9 platforms, checked when `?platforms=` is omitted):**
GitHub, GitLab, dev.to, Dribbble, Behance, SoundCloud, Gumroad, Vimeo, Hashnode.

These were chosen because they return clean, distinguishable HTTP responses for real vs. nonexistent usernames.

**Opt-in (11 platforms, request via `?platforms=name1,name2`):**
Pinterest, Twitch, PyPI, Reddit, npm, Bitbucket, Medium, Product Hunt, Patreon, Substack, Buy Me a Coffee.

These are kept available but excluded from defaults because their CDNs return bot challenges, identical responses for real and fake users, or JavaScript-rendered pages that defeat server-side checks. Use them when you specifically need them; expect more `unknown` results.

**Not supported:** Instagram, TikTok, X/Twitter, Facebook — they aggressively block automated profile lookups, would produce unreliable `unknown` results, and most have ToS clauses against this kind of check.

---

## Local development

From `D:\Money-maker\username-api\`:

```powershell
# First-time setup — venv is already created and dependencies installed.
# If you ever need to rebuild it:
#   python -m venv .venv
#   .\.venv\Scripts\pip.exe install -r api/requirements.txt

# Start the API:
.\.venv\Scripts\python.exe -m uvicorn api.main:app --reload

# Then open http://127.0.0.1:8000/docs in a browser.
```

---

## Notes for callers

- Each request takes ~500-1500ms depending on platform response times.
- A status of `unknown` typically means the platform returned a redirect or non-standard code — treat it as inconclusive rather than as availability.
- This service issues read-only requests against public profile URLs. It does not authenticate to any platform and does not access private data.
