#!/usr/bin/env python3
"""Draw a newspaper front page summing up the world's news of
Friday 20 November 2026 and write it to /output/entry.png.

Deterministic: no network, no clock, no randomness. Every run writes
byte-identical output. Python 3.13, Pillow. The three DejaVu fonts the
page uses are bundled in fonts/ next to this file.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
OUT = "/output/entry.png"

W, H = 1024, 1024
MARGIN = 48
INK = (0, 0, 0)
PAPER = (255, 255, 255)
GREY = (90, 90, 90)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


SERIF_BOLD = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(text, fnt, width):
    """Split text into lines that fit width, measured with fnt."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, y, text, fnt, fill=INK):
    draw.text((W // 2, y), text, font=fnt, fill=fill, anchor="mt")


def draw_block(draw, x, y, width, kicker, headline, deck,
               head_font, deck_font, head_leading=1.12, deck_leading=1.35):
    """A story block: kicker, headline, deck. Returns the y below it."""
    if kicker:
        draw.text((x, y), kicker, font=SANS_BOLD(17), fill=INK)
        y += 26
    for line in wrap(headline, head_font, width):
        draw.text((x, y), line, font=head_font, fill=INK)
        y += int(head_font.size * head_leading)
    y += 4
    for line in wrap(deck, deck_font, width):
        draw.text((x, y), line, font=deck_font, fill=GREY)
        y += int(deck_font.size * deck_leading)
    return y


def rule(draw, y, width=3, x0=None, x1=None):
    x0 = MARGIN if x0 is None else x0
    x1 = W - MARGIN if x1 is None else x1
    draw.line([(x0, y), (x1, y)], fill=INK, width=width)
    return y + width


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    y = 40
    # Thin double rule above the masthead.
    y = rule(draw, y, 2)
    y += 6
    y = rule(draw, y, 1)
    y += 14

    # Masthead.
    draw_centered(draw, y, "THE WORLD", SERIF_BOLD(96))
    y += 118
    draw_centered(draw, y, "FRIDAY, 20 NOVEMBER 2026", SANS(22))
    y += 36
    y = rule(draw, y, 4)
    y += 28

    content_w = W - 2 * MARGIN

    # Lead story, full width.
    y = draw_block(
        draw, MARGIN, y, content_w,
        "RIYADH",
        "Houthi missile hits Riyadh's PIF Tower",
        "Windows blown out across seven floors of the Saudi sovereign "
        "wealth fund's headquarters; no injuries reported.",
        SERIF_BOLD(46), SANS(22),
    )
    y += 18
    y = rule(draw, y, 2)
    y += 22

    # Middle stories in two columns.
    col_w = (content_w - 32) // 2
    left_x, right_x = MARGIN, MARGIN + col_w + 32
    left_y = draw_block(
        draw, left_x, y, col_w,
        "CLIMATE  ·  ANTALYA",
        "COP31 draft drops fossil-fuel phase-out",
        "The slimmed-down draft removes all fossil-fuel language and "
        "keeps a 35% electrification target for 2035; Panama threatens "
        "to block consensus.",
        SERIF_BOLD(26), SANS(18),
    )
    right_y = draw_block(
        draw, right_x, y, col_w,
        "GAZA",
        "Israeli forces cross Gaza's Yellow Line",
        "First incursion across the ceasefire boundary in central Gaza "
        "since the truce.",
        SERIF_BOLD(26), SANS(18),
    )
    y = max(left_y, right_y) + 10
    y = rule(draw, y, 1, x0=left_x, x1=left_x + col_w)
    y = rule(draw, y, 1, x0=right_x, x1=right_x + col_w)
    y += 16

    left_y = draw_block(
        draw, left_x, y, col_w,
        "MARKETS",
        "Asian markets plunge on AI fears",
        "The Nikkei falls 4.8% on Friday; the S&P 500 logs a fifth "
        "straight daily loss on Thursday.",
        SERIF_BOLD(26), SANS(18),
    )
    right_y = draw_block(
        draw, right_x, y, col_w,
        "NAIROBI",
        "Kenya discharges its last Ebola patient",
        "Thirty-seven days after the outbreak's first case.",
        SERIF_BOLD(26), SANS(18),
    )
    y = max(left_y, right_y) + 14
    y = rule(draw, y, 2)
    y += 18

    # Bottom band story, full width.
    y = draw_block(
        draw, MARGIN, y, content_w,
        "LONDON",
        "UK pledges 1,000 drones for Ukraine",
        "A £260 million package of long-range drones and other "
        "capabilities.",
        SERIF_BOLD(30), SANS(19),
    )
    y += 16
    y = rule(draw, y, 1)
    y += 14

    # Source credit.
    draw_centered(
        draw, y,
        "Sources: Reuters  ·  AFP  ·  The Guardian  ·  AP  ·  SPA",
        SANS(16), fill=GREY,
    )

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG")


if __name__ == "__main__":
    main()
