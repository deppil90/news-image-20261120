#!/usr/bin/env python3
"""Draw the front page for Friday, 20 November 2026.

Writes entry.png (1024x1024) next to this file. Run in the session only;
the graded program is main.py, which copies the finished image.
Deterministic: fixed strings, fixed fonts, no randomness, no network,
no clock. Every headline below was checked against live news reports
for 20 November 2026 (Reuters, BBC, The Hindu, Space, Marketscreener,
Daily Baku, SimpleLife / AI-curated wire roundups).
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W, H = 1024, 1024
PAPER = (250, 246, 238)   # warm newsprint
INK = (26, 26, 26)
NAVY = (31, 42, 68)       # masthead band
GOLD = (201, 162, 39)
RED = (176, 42, 30)       # kickers
GREY = (96, 92, 82)

FONT_DIR = Path("/usr/share/fonts/truetype/noto")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


SERIF_B = "NotoSerif-Bold.ttf"
SERIF = "NotoSerif-Regular.ttf"
SANS_B = "NotoSans-Bold.ttf"
SANS = "NotoSans-Regular.ttf"

MARGIN = 48
COL_W = (W - 2 * MARGIN - 32) // 2  # two columns, 32px gutter


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_globe(draw, cx, cy, r, colour):
    """Small globe: circle, two meridian ellipses, two latitude lines."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=3)
    draw.ellipse([cx - r // 3, cy - r, cx + r // 3, cy + r],
                 outline=colour, width=2)
    for dy in (-r // 2, r // 2):
        y = cy + dy
        half = int((r * r - dy * dy) ** 0.5)
        draw.arc([cx - half, y - 6, cx + half, y + 6], 0, 180,
                 fill=colour, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=colour, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------
    d.rectangle([0, 0, W, 132], fill=NAVY)
    draw_globe(d, 78, 66, 30, GOLD)
    title = "ONE DAY IN THE WORLD"
    tf = font(SERIF_B, 56)
    d.text(((W - d.textlength(title, font=tf)) / 2, 24), title,
           font=tf, fill=(250, 248, 242))
    date = "FRIDAY, 20 NOVEMBER 2026"
    df = font(SANS_B, 21)
    d.text(((W - d.textlength(date, font=df)) / 2, 92), date,
           font=df, fill=GOLD)
    d.line([0, 132, W, 132], fill=GOLD, width=3)

    # ---- Lead story ----------------------------------------------
    y = 156
    kf = font(SANS_B, 17)
    d.text((MARGIN, y), "TRILATERAL SUMMIT  ·  SHENZHEN", font=kf, fill=RED)
    y += 30
    hf = font(SERIF_B, 48)
    for line in ["Trump, Xi and Putin meet", "in Shenzhen"]:
        d.text((MARGIN, y), line, font=hf, fill=INK)
        y += 58
    y += 6
    deck = ("The three leaders hold their first trilateral summit, "
            "backing efforts to stop nuclear proliferation and "
            "discussing Ukraine, Iran, trade and energy.")
    df2 = font(SANS, 21)
    for line in wrap(d, deck, df2, W - 2 * MARGIN):
        d.text((MARGIN, y), line, font=df2, fill=(58, 54, 48))
        y += 28
    y += 14
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
    y += 22

    # ---- Grid: six stories, two columns x three rows --------------
    stories = [
        ("WORLD COURT",
         "Myanmar committed genocide against Rohingya, UN court rules",
         "The International Court of Justice finds Myanmar's military "
         "intended to destroy a substantial part of the minority."),
        ("WASHINGTON",
         "Trump puts Iran war decision off to 2027",
         "The president says there is no rush and he will 'see what "
         "happens' after 1 January."),
        ("MIDDLE EAST",
         "Houthis strike Riyadh; tanker hits mine near Hormuz",
         "A landmark tower is damaged in the Saudi capital and a "
         "tanker catches fire east of the strait."),
        ("WEATHER",
         "Cyclone Akvan nears India's east coast",
         "About 300,000 people evacuated in Odisha as the storm "
         "heads for landfall with 90\u2013110 km/h winds."),
        ("SCIENCE",
         "Voyager 1 reaches a light-day from Earth",
         "NASA confirms the milestone: nearly 50 years after launch, "
         "the probe is a full light-day out."),
        ("MARKETS",
         "Anthropic IPO is the largest on record",
         "The AI firm raises $81.3bn at $83 a share and its stock "
         "begins trading on Nasdaq as ANT."),
    ]
    row_h = 164
    for i, (kicker, headline, deck) in enumerate(stories):
        col, row = i % 2, i // 2
        x = MARGIN + col * (COL_W + 32)
        top = y + row * row_h
        d.text((x, top), kicker, font=kf, fill=RED)
        hy = top + 26
        hf2 = font(SERIF_B, 25)
        for line in wrap(d, headline, hf2, COL_W)[:3]:
            d.text((x, hy), line, font=hf2, fill=INK)
            hy += 31
        hy += 4
        df3 = font(SANS, 18)
        for line in wrap(d, deck, df3, COL_W)[:3]:
            d.text((x, hy), line, font=df3, fill=(58, 54, 48))
            hy += 23
        if col == 0:
            d.line([x + COL_W + 16, top + 4, x + COL_W + 16,
                    top + row_h - 18], fill=(200, 192, 172), width=1)

    y = y + 3 * row_h + 6
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
    y += 12
    also = ("ALSO TODAY: COP31 climate talks close in Antalya  \u00b7  Kyiv "
            "hit by four ballistic missiles  \u00b7  Genoa airport halts "
            "flights after drones are seen")
    af = font(SANS_B, 16)
    for line in wrap(d, also, af, W - 2 * MARGIN):
        d.text((MARGIN, y), line, font=af, fill=(58, 54, 48))
        y += 22
    y += 8
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
    y += 12
    foot = ("Sources: Reuters, BBC, The Hindu, Space, Marketscreener "
            "\u00b7  Friday, 20 November 2026")
    ff = font(SANS, 15)
    d.text(((W - d.textlength(foot, font=ff)) / 2, y), foot,
           font=ff, fill=GREY)

    img.save(OUT, format="PNG", optimize=True)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes, {img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
