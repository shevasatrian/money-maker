"""Generate RapidAPI listing artwork for the Username Availability Checker.

Run from the username-api dir with the venv python:
    venv\\Scripts\\python.exe assets\\make_logo.py

Outputs (both PNG, ready to upload):
    assets/logo.png    500x500  -> RapidAPI "Upload Image" (recommended 500x500)
    assets/banner.png  1200x630 -> social/banner card

No SVG, no external rasterizer: drawn directly with Pillow using Segoe UI Bold.
Pillow is a local-only dev dependency (not in requirements.txt, not deployed).
"""

from __future__ import annotations

import os

from PIL import Image, ImageDraw, ImageFont

FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_SEMI = r"C:\Windows\Fonts\seguisb.ttf"  # Segoe UI Semibold
if not os.path.exists(FONT_SEMI):
    FONT_SEMI = FONT_BOLD

# Brand palette
BG_TOP = (37, 99, 235)      # indigo-blue
BG_BOT = (13, 17, 23)       # near-black (github dark)
WHITE = (255, 255, 255)
GREEN = (34, 197, 94)       # "available" green
MUTED = (148, 163, 184)


def _vertical_gradient(size: tuple[int, int], top, bot) -> Image.Image:
    w, h = size
    base = Image.new("RGB", size, top)
    top_arr = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(h - 1, 1)
        top_arr.putpixel(
            (0, y),
            (
                round(top[0] + (bot[0] - top[0]) * t),
                round(top[1] + (bot[1] - top[1]) * t),
                round(top[2] + (bot[2] - top[2]) * t),
            ),
        )
    return top_arr.resize(size)


def _font(path: str, sz: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, sz)


def _checkmark(draw: ImageDraw.ImageDraw, cx: int, cy: int, r: int) -> None:
    """A green circular badge with a white check, centered at (cx, cy)."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GREEN)
    w = max(r // 5, 4)
    p1 = (cx - r * 0.42, cy + r * 0.02)
    p2 = (cx - r * 0.10, cy + r * 0.34)
    p3 = (cx + r * 0.46, cy - r * 0.36)
    draw.line([p1, p2], fill=WHITE, width=w)
    draw.line([p2, p3], fill=WHITE, width=w)


def make_logo() -> None:
    S = 500
    img = _vertical_gradient((S, S), BG_TOP, BG_BOT)
    d = ImageDraw.Draw(img)

    # Big "@" glyph, centered a touch high to leave room for the wordmark.
    at_font = _font(FONT_BOLD, 300)
    at = "@"
    box = d.textbbox((0, 0), at, font=at_font)
    aw, ah = box[2] - box[0], box[3] - box[1]
    ax = (S - aw) / 2 - box[0]
    ay = (S - ah) / 2 - box[1] - 40
    d.text((ax, ay), at, font=at_font, fill=WHITE)

    # Green "available" check badge, overlapping the @ at lower-right.
    _checkmark(d, cx=S - 150, cy=S - 175, r=58)

    # Wordmark.
    wm_font = _font(FONT_SEMI, 46)
    wm = "Username Checker"
    wb = d.textbbox((0, 0), wm, font=wm_font)
    d.text(((S - (wb[2] - wb[0])) / 2 - wb[0], 408), wm, font=wm_font, fill=WHITE)

    img.save("assets/logo.png")
    print("wrote assets/logo.png (500x500)")


def make_banner() -> None:
    W, H = 1200, 630
    img = _vertical_gradient((W, H), BG_TOP, BG_BOT)
    d = ImageDraw.Draw(img)

    # Left: big @ mark with check badge.
    at_font = _font(FONT_BOLD, 360)
    box = d.textbbox((0, 0), "@", font=at_font)
    d.text((150 - box[0], (H - (box[3] - box[1])) / 2 - box[1]), "@", font=at_font, fill=WHITE)
    _checkmark(d, cx=150 + (box[2] - box[0]) - 30, cy=H // 2 + 95, r=58)

    # Right: title + subtitle + bullets.
    tx = 560
    title_font = _font(FONT_BOLD, 72)
    d.text((tx, 150), "Username", font=title_font, fill=WHITE)
    d.text((tx, 230), "Availability API", font=title_font, fill=WHITE)

    sub_font = _font(FONT_SEMI, 34)
    d.text((tx, 340), "Check 20+ platforms in one call", font=sub_font, fill=MUTED)

    chips = "GitHub  ·  GitLab  ·  dev.to  ·  Reddit  ·  npm  ·  +15 more"
    max_w = W - tx - 48  # keep the line clear of the right margin
    chip_sz = 28
    while chip_sz > 16:
        chip_font = _font(FONT_SEMI, chip_sz)
        cb = d.textbbox((0, 0), chips, font=chip_font)
        if cb[2] - cb[0] <= max_w:
            break
        chip_sz -= 1
    d.text((tx, 410), chips, font=chip_font, fill=(203, 213, 225))

    img.save("assets/banner.png")
    print("wrote assets/banner.png (1200x630)")


if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    make_logo()
    make_banner()
