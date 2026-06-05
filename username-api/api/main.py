"""FastAPI entry point for the Username Availability Checker API.

Endpoints:
  GET  /              - health/root
  GET  /platforms     - list supported platforms
  GET  /check/{u}     - check availability for a username across platforms

The OpenAPI schema at /openapi.json is what RapidAPI ingests to generate the
public listing, so keep titles, descriptions, and examples developer-facing.
"""

from __future__ import annotations

import time
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from .core import (
    PLATFORMS,
    check_username,
    validate_username,
)


class PlatformCheckResult(BaseModel):
    platform: str = Field(..., example="github")
    status: str = Field(
        ...,
        example="available",
        description="One of: available, taken, unknown",
    )
    url: str = Field(..., example="https://github.com/coolbrand42")
    http_status: int | None = Field(None, example=404)
    error: str | None = Field(None, example=None)


class CheckResponse(BaseModel):
    username: str = Field(..., example="coolbrand42")
    duration_ms: int = Field(
        ...,
        example=743,
        description="Wall-clock time for all platform checks in milliseconds",
    )
    summary: dict = Field(
        ..., example={"available": 7, "taken": 1, "unknown": 1}
    )
    results: list[PlatformCheckResult]


class PlatformsResponse(BaseModel):
    default: list[str] = Field(
        ...,
        example=["github", "gitlab", "dev_to", "dribbble", "behance",
                 "soundcloud", "gumroad", "vimeo", "hashnode"],
    )
    opt_in: list[str] = Field(
        ...,
        example=["pinterest", "twitch", "pypi", "reddit", "npm",
                 "bitbucket", "medium", "producthunt", "patreon",
                 "substack", "buymeacoffee"],
    )


class HealthResponse(BaseModel):
    service: str = Field(..., example="Username Availability Checker")
    version: str = Field(..., example="1.0.0")
    platforms: int = Field(..., example=20)
    docs: str = Field(..., example="/docs")


app = FastAPI(
    title="Username Availability Checker",
    description=(
        "Check whether a username is available on 20+ popular platforms "
        "(GitHub, GitLab, dev.to, Dribbble, Behance, SoundCloud, Gumroad, Vimeo, "
        "Hashnode by default, plus 11 more on opt-in) in a single API call.\n\n"
        "**Use cases:** indie hackers picking a handle before launch, brand teams "
        "vetting a product name across socials and dev registries, signup flows that "
        "suggest 'this handle is also free on X, Y, Z'.\n\n"
        "All platform checks run in parallel. Typical response time: 500–1500 ms.\n\n"
        "A status of `unknown` means the platform returned an ambiguous response "
        "(bot challenge, redirect, SPA 200-for-everything) — treat as inconclusive, "
        "not available."
    ),
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "shevasatrian@inquivix.com",
    },
    license_info={"name": "MIT"},
    openapi_tags=[
        {"name": "check", "description": "Username availability checks across platforms"},
        {"name": "meta", "description": "Health check and platform discovery"},
    ],
)


@app.get(
    "/",
    tags=["meta"],
    summary="Health check",
    description="Returns service metadata. Use this as the ping target for keep-alive monitors.",
    response_model=HealthResponse,
)
def root() -> dict:
    return {
        "service": "Username Availability Checker",
        "version": app.version,
        "platforms": len(PLATFORMS),
        "docs": "/docs",
    }


@app.get(
    "/platforms",
    tags=["meta"],
    summary="List supported platforms",
    description=(
        "Returns all platform identifiers split into two groups:\n\n"
        "- **default** — checked automatically when `?platforms=` is omitted "
        "(9 platforms with reliable HTTP signals)\n"
        "- **opt_in** — must be requested explicitly via `?platforms=name1,name2`; "
        "these have higher rates of `unknown` responses due to bot-detection CDNs\n\n"
        "Use the names returned here as values in the `platforms` query parameter "
        "of `/check/{username}`."
    ),
    response_model=PlatformsResponse,
)
def list_platforms() -> dict:
    return {
        "default": [p.name for p in PLATFORMS if p.enabled],
        "opt_in": [p.name for p in PLATFORMS if not p.enabled],
    }


@app.get(
    "/check/{username}",
    tags=["check"],
    summary="Check username availability",
    description=(
        "Checks whether `username` is available across all default platforms "
        "(or a filtered subset) in parallel.\n\n"
        "**Path parameter:** `username` — 1–39 characters: letters, digits, `.`, `-`, `_`\n\n"
        "**Query parameter:** `platforms` — optional comma-separated platform names "
        "(e.g. `github,reddit,twitch`). Omit to check all 9 default platforms. "
        "Names come from `GET /platforms`.\n\n"
        "**Status values per platform:**\n"
        "- `available` — profile does not exist (username is free)\n"
        "- `taken` — profile exists\n"
        "- `unknown` — ambiguous response; treat as inconclusive\n\n"
        "Typical latency: 500–1500 ms (bound by the slowest responding platform)."
    ),
    response_model=CheckResponse,
    responses={400: {"description": "Invalid username format or unknown platform name"}},
)
async def check(
    username: str,
    platforms: Annotated[
        str | None,
        Query(
            description=(
                "Comma-separated platform names to check. "
                "Defaults to all 9 default platforms. "
                "Example: `github,reddit,twitch`"
            )
        ),
    ] = None,
) -> dict:
    err = validate_username(username)
    if err:
        raise HTTPException(status_code=400, detail=err)

    requested: list[str] | None = None
    if platforms:
        requested = [p.strip() for p in platforms.split(",") if p.strip()]
        known = {p.name for p in PLATFORMS}
        unknown = [p for p in requested if p not in known]
        if unknown:
            raise HTTPException(
                status_code=400,
                detail=f"unknown platform(s): {', '.join(unknown)}",
            )

    started = time.perf_counter()
    results = await check_username(username, platforms=requested)
    elapsed_ms = round((time.perf_counter() - started) * 1000)

    summary = {
        "available": sum(1 for r in results if r.status == "available"),
        "taken": sum(1 for r in results if r.status == "taken"),
        "unknown": sum(1 for r in results if r.status == "unknown"),
    }
    return {
        "username": username,
        "duration_ms": elapsed_ms,
        "summary": summary,
        "results": [r.to_dict() for r in results],
    }
