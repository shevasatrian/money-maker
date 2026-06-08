# RapidAPI Listing Copy

Paste each section into the corresponding field when filling out the RapidAPI "Add New API" form.

---

## Listing Title

Username Availability Checker API

---

## Short Description

Check if a username is available on 20+ platforms (GitHub, Reddit, Twitch, dev.to, npm, Substack, and more) in one call.

---

## Long Description

Check whether a username or brand handle is available across 20 popular social, developer, and creator platforms in a single API call. All platform checks run in parallel; typical response time is 500–1500 ms.

### Platforms covered

**Default (checked every call):** GitHub, GitLab, dev.to, Dribbble, Behance, SoundCloud, Gumroad, Vimeo, Hashnode

**Opt-in (pass via `?platforms=`):** Pinterest, Twitch, PyPI, Reddit, npm, Bitbucket, Medium, Product Hunt, Patreon, Substack, Buy Me a Coffee

### Built for

- **Indie hackers** — pick a handle before you launch; check 9 platforms at once
- **Brand teams** — vet a product name across socials and dev registries in one request
- **Signup flows** — tell your users "this handle is also available on GitHub and dev.to"
- **Namespace monitoring** — check whether your brand name has been registered on a new platform

### Response shape

Each platform returns one of three statuses:
- `available` — the username is free
- `taken` — a profile exists at that URL
- `unknown` — the platform returned an ambiguous signal (treat as inconclusive, not available)

The top-level `summary` object gives you counts of each status so you can gate logic without iterating the full results array.

### Reliability notes

The 9 default platforms were chosen because they return clean, distinguishable HTTP signals for real vs. nonexistent profiles. The 11 opt-in platforms have higher rates of `unknown` responses due to bot-detection CDNs and JavaScript-rendered pages. Not supported: Instagram, TikTok, X/Twitter, Facebook — they aggressively block automated lookups.

---

## Tags

username
availability
social
branding
signup
developer-tools
username-checker
handle
namespace

---

## Categories

- Tools (primary)
- Data (secondary)
- Social (tertiary)

---

## Example Requests and Responses

### 1. Check a username across all default platforms

**Request:**
```bash
curl --request GET \
  --url 'https://hot-olimpia-sheva-ee26b88b.koyeb.app/check/coolbrand42' \
  --header 'X-RapidAPI-Key: YOUR_RAPIDAPI_KEY' \
  --header 'X-RapidAPI-Host: username-availability-checker.p.rapidapi.com'
```

**Response (200 OK):**
```json
{
  "username": "coolbrand42",
  "duration_ms": 743,
  "summary": { "available": 7, "taken": 1, "unknown": 1 },
  "results": [
    { "platform": "github",     "status": "available", "url": "https://github.com/coolbrand42",          "http_status": 404, "error": null },
    { "platform": "gitlab",     "status": "available", "url": "https://gitlab.com/coolbrand42",          "http_status": 302, "error": null },
    { "platform": "dev_to",     "status": "available", "url": "https://dev.to/coolbrand42",              "http_status": 404, "error": null },
    { "platform": "dribbble",   "status": "available", "url": "https://dribbble.com/coolbrand42",        "http_status": 404, "error": null },
    { "platform": "behance",    "status": "available", "url": "https://www.behance.net/coolbrand42",     "http_status": 404, "error": null },
    { "platform": "soundcloud", "status": "taken",     "url": "https://soundcloud.com/coolbrand42",      "http_status": 200, "error": null },
    { "platform": "gumroad",    "status": "available", "url": "https://coolbrand42.gumroad.com/",        "http_status": 404, "error": null },
    { "platform": "vimeo",      "status": "available", "url": "https://vimeo.com/coolbrand42",           "http_status": 404, "error": null },
    { "platform": "hashnode",   "status": "unknown",   "url": "https://hashnode.com/@coolbrand42",       "http_status": 200, "error": null }
  ]
}
```

### 2. Check specific platforms only

**Request:**
```bash
curl --request GET \
  --url 'https://hot-olimpia-sheva-ee26b88b.koyeb.app/check/torvalds?platforms=github,gitlab,soundcloud' \
  --header 'X-RapidAPI-Key: YOUR_RAPIDAPI_KEY' \
  --header 'X-RapidAPI-Host: username-availability-checker.p.rapidapi.com'
```

**Response (200 OK):**
```json
{
  "username": "torvalds",
  "duration_ms": 612,
  "summary": { "available": 0, "taken": 3, "unknown": 0 },
  "results": [
    { "platform": "github",     "status": "taken", "url": "https://github.com/torvalds",     "http_status": 200, "error": null },
    { "platform": "gitlab",     "status": "taken", "url": "https://gitlab.com/torvalds",     "http_status": 200, "error": null },
    { "platform": "soundcloud", "status": "taken", "url": "https://soundcloud.com/torvalds", "http_status": 200, "error": null }
  ]
}
```

### 3. List available platforms

**Request:**
```bash
curl --request GET \
  --url 'https://hot-olimpia-sheva-ee26b88b.koyeb.app/platforms' \
  --header 'X-RapidAPI-Key: YOUR_RAPIDAPI_KEY' \
  --header 'X-RapidAPI-Host: username-availability-checker.p.rapidapi.com'
```

**Response (200 OK):**
```json
{
  "default": ["github", "gitlab", "dev_to", "dribbble", "behance", "soundcloud", "gumroad", "vimeo", "hashnode"],
  "opt_in":  ["pinterest", "twitch", "pypi", "reddit", "npm", "bitbucket", "medium", "producthunt", "patreon", "substack", "buymeacoffee"]
}
```

### 4. Invalid username (400 error)

**Request:**
```bash
curl --request GET \
  --url 'https://hot-olimpia-sheva-ee26b88b.koyeb.app/check/this!!invalid'
```

**Response (400 Bad Request):**
```json
{
  "detail": "username must be 1-39 chars of letters, digits, '.', '-', or '_'"
}
```

---

## Pricing Tier Configuration

| Tier  | Price       | Quota                  | Overage                   |
|-------|-------------|------------------------|---------------------------|
| Basic | Free        | 100 requests/day       | Hard cap (no overage)     |
| Pro   | $5.00/month | 10,000 requests/month  | $0.001 per extra request  |
| Ultra | $20.00/month| 100,000 requests/month | $0.0005 per extra request |
| Mega  | Custom      | Unlimited              | Contact provider          |

Basic (100/day) is enough to integrate and test, but not enough for production traffic — it nudges real users toward Pro. Pro at $5/mo is under any "needs manager approval" threshold. Ultra's per-request overage rate is lower than Pro's to encourage upward migration rather than throttling.

### RapidAPI pricing form — exact field entries

RapidAPI's **Plans & Pricing** form asks for more than the table above: a quota
**period**, a **rate limit** (req/sec, abuse protection), a **hard-limit** toggle, and
the **overage** price. Enter each plan exactly as below. Create them in order; the
free Basic plan must exist before paid plans can reference the same quota object.

The rate limits matter operationally: one `/check` call fans out to ~9 external HTTP
GETs, so an unthrottled client can hammer the Koyeb free tier. The per-second caps
below keep a single key from saturating the instance.

**Basic — Free**
- Price: `0`
- Requests quota: `100` per **Day**
- Rate limit: `2` requests / **second**
- Hard limit: **ON** (requests beyond quota are rejected, not billed)
- Overage: none

**Pro — $5.00 / month**
- Price: `5.00`, recurrence **Monthly**
- Requests quota: `10000` per **Month**
- Rate limit: `10` requests / **second**
- Hard limit: **OFF** (allow overage)
- Overage: `0.001` USD per request beyond quota

**Ultra — $20.00 / month**
- Price: `20.00`, recurrence **Monthly**
- Requests quota: `100000` per **Month**
- Rate limit: `20` requests / **second**
- Hard limit: **OFF** (allow overage)
- Overage: `0.0005` USD per request beyond quota

**Mega — Custom**
- Price: `Custom` (or set a high flat price, e.g. `99.00`, if RapidAPI requires a number)
- Requests quota: effectively unlimited (set a very high cap, e.g. `5000000` / Month)
- Rate limit: `40` requests / **second**
- Hard limit: **OFF**
- Overage: contact-provider / negotiated

> Set every plan's visibility to **Public** so it appears on the listing. Leaving a
> plan Private hides it from subscribers and it cannot generate revenue.

---

## Publish Checklist (current flow)

The fastest path uses the live OpenAPI spec, which now carries the Koyeb base URL
in its `servers` field — importing it auto-creates the base URL **and** all three
endpoints in one step.

1. [ ] **Base URL + endpoints (the two blockers):** In the Provider Dashboard, open
   the API → **Definition / API Specs**. Use **Import from OpenAPI** and point it at:
   `https://hot-olimpia-sheva-ee26b88b.koyeb.app/openapi.json`
   This wires the base URL and the `/`, `/platforms`, `/check/{username}` endpoints
   automatically. (If you created the API via the UI without import, set the base URL
   to `https://hot-olimpia-sheva-ee26b88b.koyeb.app` and add the three endpoints by hand.)
2. [ ] **Long description:** paste the Long Description section above into the API's
   Long Description field (the import fills the short description from the spec).
3. [ ] **Image:** upload `username-api/assets/logo.png` (500×500, matches RapidAPI's
   recommended size). `assets/banner.png` (1200×630) is available for socials.
4. [ ] **Categories:** Tools (primary), Data, Social.
5. [ ] **Pricing tiers:** under **Plans & Pricing**, create the four tiers from the
   "Pricing Tier Configuration" table above (Basic free / Pro $5 / Ultra $20 / Mega
   custom). Without a paid tier there is nothing to earn — this is the revenue step.
6. [ ] **Smoke-test:** run one example from "Example Requests and Responses" through the
   RapidAPI playground (it injects your test `X-RapidAPI-Key`) and confirm a 200.
7. [ ] **Publish:** set visibility to **Public**, then Publish.

> Note: the `X-RapidAPI-Host` in the examples (`username-availability-checker.p.rapidapi.com`)
> is illustrative — RapidAPI assigns the real host when you publish. Update the examples
> if the assigned slug differs.
