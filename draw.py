#!/usr/bin/env python3
"""Draw entry.png: a newspaper front page summing up Friday 20 November 2026.

Run from the repository root:  python3 draw.py
Writes entry.png next to this script. Pillow only; no network, no clock.
"""

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
MARGIN = 48
GUTTER = 24
COL_W = (PAGE - 2 * MARGIN - GUTTER) // 2

PAPER = (247, 243, 232)
NAVY = (26, 34, 64)
GOLD = (201, 162, 39)
INK = (20, 20, 20)
KICKER_RED = (163, 29, 29)
DECK_GREY = (61, 61, 61)
RULE = (26, 34, 64)
FAINT = (120, 116, 104)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width`."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if fnt.getlength(trial) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    """Draw wrapped lines starting at (x, y); return y below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def paint_globe(draw, cx, cy, r):
    """A simple wireframe globe: outline, meridians, parallels."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=3)
    draw.ellipse([cx - r * 0.55, cy - r, cx + r * 0.55, cy + r],
                 outline=GOLD, width=2)
    draw.ellipse([cx - r * 0.22, cy - r, cx + r * 0.22, cy + r],
                 outline=GOLD, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=GOLD, width=2)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             start=200, end=340, fill=GOLD, width=2)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             start=20, end=160, fill=GOLD, width=2)


def paint_masthead(draw):
    band_h = 118
    draw.rectangle([0, 0, PAGE, band_h], fill=NAVY)
    paint_globe(draw, 72, band_h // 2, 34)
    title = font(SERIF_B, 58)
    title_text = "ONE DAY IN THE WORLD"
    tw = draw.textlength(title_text, font=title)
    draw.text(((PAGE - tw) / 2, 18), title_text, font=title, fill=(255, 255, 255))
    date_f = font(SANS_B, 21)
    date_text = "FRIDAY, 20 NOVEMBER 2026"
    dw = draw.textlength(date_text, font=date_f)
    draw.text(((PAGE - dw) / 2, 82), date_text, font=date_f, fill=GOLD)
    draw.rectangle([0, band_h, PAGE, band_h + 4], fill=GOLD)
    return band_h + 4


LEAD = {
    "kicker": "TRILATERAL SUMMIT  ·  SHENZHEN",
    "headline": "Trump, Xi and Putin meet in Shenzhen",
    "deck": ("The three leaders hold their first trilateral summit, backing "
             "efforts to stop nuclear proliferation and discussing Ukraine, "
             "Iran, trade and energy."),
}

STORIES = [
    {
        "kicker": "WORLD COURT",
        "headline": "Myanmar committed genocide against Rohingya, UN court rules",
        "deck": ("The International Court of Justice finds Myanmar's military "
                 "intended to destroy a substantial part of the minority."),
    },
    {
        "kicker": "WASHINGTON",
        "headline": "Trump puts Iran war decision off to 2027",
        "deck": ("The president says there is no rush and he will 'see what "
                 "happens' after 1 January."),
    },
    {
        "kicker": "MIDDLE EAST",
        "headline": "Houthis strike Riyadh; tanker hits mine near Hormuz",
        "deck": ("A landmark tower is damaged in the Saudi capital and a "
                 "tanker catches fire east of the strait."),
    },
    {
        "kicker": "WEATHER",
        "headline": "Cyclone Akvan nears India's east coast",
        "deck": ("About 300,000 people evacuated in Odisha as the storm heads "
                 "for landfall with 90–110 km/h winds."),
    },
    {
        "kicker": "SCIENCE",
        "headline": "Voyager 1 reaches a light-day from Earth",
        "deck": ("NASA confirms the milestone: nearly 50 years after launch, "
                 "the probe is a full light-day out."),
    },
    {
        "kicker": "MARKETS",
        "headline": "Anthropic IPO is the largest on record",
        "deck": ("The AI firm raises $81.3bn at $83 a share and its stock "
                 "begins trading on Nasdaq as ANT."),
    },
]

ALSO_TODAY = ("ALSO TODAY:  COP31 climate talks close in Antalya  ·  Kyiv hit "
              "by four ballistic missiles  ·  Genoa airport halts flights "
              "after drones are seen")

FOOTER = "Sources: Reuters, BBC, The Hindu, Space, Marketscreener  ·  Friday, 20 November 2026"


def paint_lead(draw, y):
    kicker_f = font(SANS_B, 17)
    head_f = font(SERIF_B, 52)
    deck_f = font(SERIF, 23)
    draw.text((MARGIN, y), LEAD["kicker"], font=kicker_f, fill=KICKER_RED)
    y += 30
    y = text_block(draw, MARGIN, y,
                   wrap(LEAD["headline"], head_f, PAGE - 2 * MARGIN),
                   head_f, INK, 58)
    y += 6
    y = text_block(draw, MARGIN, y,
                   wrap(LEAD["deck"], deck_f, PAGE - 2 * MARGIN),
                   deck_f, DECK_GREY, 30)
    return y + 14


def paint_story(draw, story, x, y):
    kicker_f = font(SANS_B, 15)
    head_f = font(SERIF_B, 27)
    deck_f = font(SERIF, 19)
    draw.text((x, y), story["kicker"], font=kicker_f, fill=KICKER_RED)
    y += 26
    y = text_block(draw, x, y,
                   wrap(story["headline"], head_f, COL_W),
                   head_f, INK, 31)
    y += 4
    y = text_block(draw, x, y,
                   wrap(story["deck"], deck_f, COL_W),
                   deck_f, DECK_GREY, 24)
    return y


def paint_grid(draw, y):
    row_gap = 38
    left_x = MARGIN
    right_x = MARGIN + COL_W + GUTTER
    divider_x = MARGIN + COL_W + GUTTER // 2
    top = y
    for row in range(3):
        left = STORIES[row * 2]
        right = STORIES[row * 2 + 1]
        left_bottom = paint_story(draw, left, left_x, y)
        right_bottom = paint_story(draw, right, right_x, y)
        y = max(left_bottom, right_bottom) + row_gap
    draw.line([divider_x, top, divider_x, y - row_gap], fill=FAINT, width=1)
    return y - row_gap


def paint_strip(draw, y):
    strip_f = font(SANS_B, 18)
    draw.line([MARGIN, y, PAGE - MARGIN, y], fill=RULE, width=2)
    y += 12
    y = text_block(draw, MARGIN, y,
                   wrap(ALSO_TODAY, strip_f, PAGE - 2 * MARGIN),
                   strip_f, INK, 25)
    y += 12
    draw.line([MARGIN, y, PAGE - MARGIN, y], fill=RULE, width=2)
    return y


def paint_footer(draw, y):
    foot_f = font(SANS, 16)
    fw = draw.textlength(FOOTER, font=foot_f)
    draw.text(((PAGE - fw) / 2, y), FOOTER, font=foot_f, fill=FAINT)


def main():
    canvas = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(canvas)
    y = paint_masthead(draw)
    y += 22
    y = paint_lead(draw, y)
    draw.line([MARGIN, y, PAGE - MARGIN, y], fill=RULE, width=2)
    y += 26
    y = paint_grid(draw, y)
    y += 24
    y = paint_strip(draw, y)
    paint_footer(draw, y + 20)
    canvas.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
