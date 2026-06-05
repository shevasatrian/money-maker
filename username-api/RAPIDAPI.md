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
  --url 'https://YOUR-RENDER-URL.onrender.com/check/coolbrand42' \
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
  --url 'https://YOUR-RENDER-URL.onrender.com/check/torvalds?platforms=github,gitlab,soundcloud' \
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
  --url 'https://YOUR-RENDER-URL.onrender.com/platforms' \
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
  --url 'https://YOUR-RENDER-URL.onrender.com/check/this!!invalid'
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

---

## Pre-Publish Checklist

- [ ] Replace `YOUR-RENDER-URL` in all curl examples with the actual Render URL
- [ ] Replace `username-availability-checker` in `X-RapidAPI-Host` with the slug RapidAPI assigns
- [ ] Test one curl example end-to-end before publishing the listing
- [ ] Upload a banner image (1200×630 px recommended; dark background, white text works well)
- [ ] Set categories: Tools (primary), Data, Social
- [ ] Set visibility to **Public** before clicking Publish
