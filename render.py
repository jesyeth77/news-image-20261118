#!/usr/bin/env python3
"""Render the 18 Nov 2026 world-news infographic (1024x1024 PNG).

Reads the baked news data from data/news.json and draws a newspaper-style
one-page summary to assets/entry.png. Deterministic: same input gives the
same output bytes (no timestamps, no randomness, fonts bundled in fonts/).
Run: python3 render.py
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
MARGIN = 44

PAPER = (250, 246, 239)
NAVY = (16, 36, 62)
RED = (192, 57, 43)
GOLD = (242, 201, 76)
INK = (28, 28, 28)
GRAY = (110, 110, 110)
HAIRLINE = (216, 210, 196)
WHITE = (255, 255, 255)
LIGHT_BLUE = (169, 195, 222)


def font(name, size):
    return ImageFont.truetype(os.path.join(HERE, "fonts", name), size)


def wrap(draw, text, fnt, max_w):
    """Wrap text to lines that fit max_w (by pixel width)."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, fill, max_w, leading):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def main():
    with open(os.path.join(HERE, "data", "news.json"), encoding="utf-8") as f:
        data = json.load(f)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_mast = font("DejaVuSans-Bold.ttf", 72)
    f_date = font("DejaVuSans-Bold.ttf", 26)
    f_tag = font("DejaVuSans.ttf", 20)
    f_kicker = font("DejaVuSans-Bold.ttf", 20)
    f_head_lead = font("DejaVuSans-Bold.ttf", 38)
    f_sum_lead = font("DejaVuSans.ttf", 23)
    f_head = font("DejaVuSans-Bold.ttf", 26)
    f_sum = font("DejaVuSans.ttf", 18)
    f_also = font("DejaVuSans.ttf", 19)
    f_foot = font("DejaVuSans.ttf", 16)

    # ---- header band ----
    d.rectangle([0, 0, W, 150], fill=NAVY)
    d.rectangle([0, 150, W, 156], fill=RED)
    d.text((MARGIN, 26), data["masthead"], font=f_mast, fill=WHITE)
    d.text((MARGIN, 104), data["date"].upper(), font=f_date, fill=GOLD)
    tag = data["tagline"]
    tw = d.textlength(tag, font=f_tag)
    d.text((W - MARGIN - tw, 108), tag, font=f_tag, fill=LIGHT_BLUE)

    y = 178
    # ---- lead story ----
    lead = data["lead"]
    d.text((MARGIN, y), lead["kicker"], font=f_kicker, fill=RED)
    y += 30
    y = draw_wrapped(d, MARGIN, y, lead["headline"], f_head_lead, INK,
                     W - 2 * MARGIN, 48)
    y += 12
    y = draw_wrapped(d, MARGIN, y, lead["summary"], f_sum_lead, INK,
                     W - 2 * MARGIN, 31)
    y += 18
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=HAIRLINE, width=2)
    y += 18

    # ---- 2x2 grid ----
    stories = data["stories"]
    col_w = (W - 2 * MARGIN - 20) // 2
    row_h = 172
    for i, st in enumerate(stories):
        cx = MARGIN + (i % 2) * (col_w + 20)
        cy = y + (i // 2) * (row_h + 18)
        d.text((cx, cy), st["kicker"], font=f_kicker, fill=RED)
        yy = cy + 28
        yy = draw_wrapped(d, cx, yy, st["headline"], f_head, INK, col_w, 32)
        yy += 6
        draw_wrapped(d, cx, yy, st["summary"], f_sum, INK, col_w, 24)
    y = y + 2 * row_h + 18
    y += 14
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=HAIRLINE, width=2)
    y += 16

    # ---- also today ----
    d.text((MARGIN, y), "ALSO TODAY", font=f_kicker, fill=RED)
    y += 30
    for item in data["also"]:
        d.text((MARGIN, y), "•", font=f_also, fill=RED)
        draw_wrapped(d, MARGIN + 24, y, item, f_also, INK,
                     W - 2 * MARGIN - 24, 26)
        y += 30
    y += 8
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=HAIRLINE, width=2)
    y += 14

    # ---- footer ----
    foot = "Sources: " + data["footer_sources"]
    d.text((MARGIN, y), foot, font=f_foot, fill=GRAY)
    stamp = "18 NOV 2026"
    d.text((W - MARGIN - d.textlength(stamp, font=f_foot), y), stamp,
           font=f_foot, fill=GRAY)

    assert y + 20 <= H - 10, f"layout overflow: y={y}"
    out = os.path.join(HERE, "assets", "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
