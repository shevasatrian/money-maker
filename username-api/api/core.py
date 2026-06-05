"""Username availability checker across public platforms.

Each platform is checked by issuing an HTTP GET to a profile URL with a
realistic User-Agent. A 404 (and a few platform-specific signals) means the
username is available; a 200 means it's taken. Anything else is reported as
"unknown" so callers can decide how to treat ambiguity.
"""

from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass
from typing import Literal

import httpx

Status = Literal["available", "taken", "unknown"]

_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0 Safari/537.36"
)

_DEFAULT_HEADERS = {
    "User-Agent": _USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


@dataclass(frozen=True)
class Platform:
    name: str
    url_template: str
    # Status codes that mean the username is AVAILABLE (profile does not exist).
    available_codes: tuple[int, ...] = (404,)
    # Status codes that mean the username is TAKEN (profile exists).
    taken_codes: tuple[int, ...] = (200,)
    # Optional regex; if matched in the response body of a 200, treat as available
    # (covers platforms that return 200 with a "not found" page).
    available_body_regex: str | None = None
    # Optional regex; if matched in the response body of a 200, treat as taken.
    taken_body_regex: str | None = None
    # Some platforms block automated GETs; we skip them by default.
    enabled: bool = True


PLATFORMS: tuple[Platform, ...] = (
    # --- Reliable platforms (enabled by default) ---
    Platform("github", "https://github.com/{u}"),
    # GitLab redirects nonexistent profiles to /users/sign_in (302).
    Platform("gitlab", "https://gitlab.com/{u}",
             available_codes=(301, 302, 404), taken_codes=(200,)),
    Platform("dev_to", "https://dev.to/{u}"),
    Platform("dribbble", "https://dribbble.com/{u}"),
    Platform("behance", "https://www.behance.net/{u}"),
    Platform("soundcloud", "https://soundcloud.com/{u}"),
    Platform("gumroad", "https://{u}.gumroad.com/",
             available_codes=(404, 410), taken_codes=(200,)),
    Platform("vimeo", "https://vimeo.com/{u}"),
    # Hashnode is an SPA that returns 200 for missing users; detect via title.
    Platform("hashnode", "https://hashnode.com/@{u}",
             available_body_regex=r"User not found"),

    # --- Opt-in platforms (unreliable due to bot detection / SPA / CDN).
    # Callers can include them via ?platforms=name but expect more 'unknown'
    # responses than the default set.
    Platform("pinterest", "https://www.pinterest.com/{u}/",
             taken_body_regex=r"Profile\s*\|\s*Pinterest", enabled=False),
    Platform("twitch", "https://www.twitch.tv/{u}", enabled=False),
    Platform("pypi", "https://pypi.org/user/{u}/", enabled=False),
    Platform("reddit", "https://www.reddit.com/user/{u}/about.json",
             available_codes=(404,), taken_codes=(200,), enabled=False),
    Platform("npm", "https://www.npmjs.com/~{u}", enabled=False),
    Platform("bitbucket", "https://bitbucket.org/{u}/", enabled=False),
    Platform("medium", "https://medium.com/@{u}", enabled=False),
    Platform("producthunt", "https://www.producthunt.com/@{u}", enabled=False),
    Platform("patreon", "https://www.patreon.com/{u}", enabled=False),
    Platform("substack", "https://{u}.substack.com/",
             available_codes=(404,), taken_codes=(200,), enabled=False),
    Platform("buymeacoffee", "https://www.buymeacoffee.com/{u}", enabled=False),
)

PLATFORMS_BY_NAME: dict[str, Platform] = {p.name: p for p in PLATFORMS}


# RFC-loose username validation. Most platforms permit 1-39 chars, letters/digits/-/_.
_USERNAME_RE = re.compile(r"^[A-Za-z0-9_.\-]{1,39}$")


def validate_username(username: str) -> str | None:
    """Return an error string if invalid, else None."""
    if not username:
        return "username is required"
    if not _USERNAME_RE.match(username):
        return "username must be 1-39 chars of letters, digits, '.', '-', or '_'"
    return None


@dataclass
class PlatformResult:
    platform: str
    status: Status
    url: str
    http_status: int | None
    error: str | None = None

    def to_dict(self) -> dict:
        return {
            "platform": self.platform,
            "status": self.status,
            "url": self.url,
            "http_status": self.http_status,
            "error": self.error,
        }


async def _check_one(
    client: httpx.AsyncClient, platform: Platform, username: str
) -> PlatformResult:
    url = platform.url_template.format(u=username)
    try:
        response = await client.get(
            url, headers=_DEFAULT_HEADERS, follow_redirects=False, timeout=8.0
        )
    except httpx.TimeoutException:
        return PlatformResult(platform.name, "unknown", url, None, "timeout")
    except httpx.HTTPError as exc:
        return PlatformResult(platform.name, "unknown", url, None, str(exc))

    code = response.status_code

    # Body-regex overrides (only inspected on 2xx to avoid unnecessary work).
    if 200 <= code < 300:
        if platform.available_body_regex and re.search(
            platform.available_body_regex, response.text
        ):
            return PlatformResult(platform.name, "available", url, code)
        if platform.taken_body_regex and re.search(
            platform.taken_body_regex, response.text
        ):
            return PlatformResult(platform.name, "taken", url, code)

    if code in platform.available_codes:
        return PlatformResult(platform.name, "available", url, code)
    if code in platform.taken_codes:
        return PlatformResult(platform.name, "taken", url, code)
    # Redirect to a login or root page usually means "not found" for many platforms,
    # but we don't assume — flag as unknown so the caller decides.
    return PlatformResult(platform.name, "unknown", url, code)


async def check_username(
    username: str, platforms: list[str] | None = None
) -> list[PlatformResult]:
    """Check `username` against a subset (or all) of supported platforms in parallel."""
    if platforms:
        selected = [PLATFORMS_BY_NAME[p] for p in platforms if p in PLATFORMS_BY_NAME]
    else:
        selected = [p for p in PLATFORMS if p.enabled]

    limits = httpx.Limits(max_connections=20, max_keepalive_connections=20)
    async with httpx.AsyncClient(limits=limits, http2=False) as client:
        tasks = [_check_one(client, p, username) for p in selected]
        return await asyncio.gather(*tasks)
