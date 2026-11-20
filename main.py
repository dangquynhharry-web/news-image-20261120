#!/usr/bin/env python3
"""News front page for Friday 20 November 2026.

Draws a 1024x1024 newspaper front page summing up the day's world news
and writes it to /output/entry.png.

Deterministic: all text, layout and colours are fixed in this file. No
network, no clock, no randomness, no system fonts (the DejaVu fonts the
page uses are bundled in fonts/ next to this script, so the program renders
identically wherever it runs).

Stories (as reported on 20 November 2026 by Reuters, AFP, The Guardian,
AP, SPA and the day's news briefs):
  1. A Houthi missile damages Riyadh's PIF Tower, the tallest tower in
     the capital's financial district; windows blown out across seven
     floors, no injuries reported.
  2. COP31's slimmed-down draft drops all fossil-fuel phase-out language
     and keeps a 35% electrification target for 2035; Panama threatens
     to block consensus as talks end Friday.
  3. Israeli forces cross the Yellow Line in central Gaza, the first
     incursion across the ceasefire boundary since the truce.
  4. Asian markets plunge Friday on AI-valuation fears; the Nikkei falls
     4.8%, and the S&P 500 logs a fifth straight daily loss on Thursday.
  5. Kenya discharges its last Ebola patient, 37 days after the first
     case of the outbreak.
  6. The UK pledges more than 1,000 drones for Ukraine in a 260-million-
     pound package.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (17, 17, 17)
RED = (163, 30, 34)
GREY = (90, 86, 78)

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, width, kicker, headline, deck, hsize, dsize,
          align="left", hspace=4, dspace=3):
    """Draw one story block; returns the y just below it."""
    fk = font(SANS_B, 20)
    fh = font(SERIF_B, hsize)
    fd = font(SANS, dsize)
    if kicker:
        draw.text((x, y), kicker, font=fk, fill=RED)
        y += 30
    lines = wrap(draw, headline, fh, width)
    for ln in lines:
        lx = x if align == "left" else x + (width - draw.textlength(ln, font=fh)) // 2
        draw.text((lx, y), ln, font=fh, fill=INK)
        y += hsize + hspace
    if deck:
        y += 2
        for ln in wrap(draw, deck, fd, width):
            lx = x if align == "left" else x + (width - draw.textlength(ln, font=fd)) // 2
            draw.text((lx, y), ln, font=fd, fill=INK)
            y += dsize + dspace
    return y


def rule(draw, x, y, width, thick=2):
    draw.rectangle([x, y, x + width, y + thick - 1], fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Double border frame.
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)
    d.rectangle([24, 24, W - 25, H - 25], outline=INK, width=1)

    x, cw = 44, W - 88  # content x and width

    # Masthead.
    fm = font(SERIF_B, 96)
    title = "THE WORLD"
    d.text(((W - d.textlength(title, font=fm)) // 2, 30), title,
           font=fm, fill=INK)
    rule(d, x, 148, cw, 2)
    fd_line = font(SANS_B, 27)
    date = "FRIDAY, 20 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=fd_line)) // 2, 158), date,
           font=fd_line, fill=INK)
    rule(d, x, 200, cw, 5)
    rule(d, x, 208, cw, 1)

    # Lead story: Houthi missile hits Riyadh's PIF Tower.
    y = block(d, x, 224, cw,
              "CONFLICT  —  RIYADH",
              "HOUTHI MISSILE HITS RIYADH TOWER",
              "The PIF Tower, headquarters of the Saudi sovereign wealth "
              "fund, is damaged as windows blow out across seven floors; "
              "no injuries are reported.",
              54, 22, align="center")
    rule(d, x, y + 10, cw, 2)

    # Row two: climate | Gaza.
    col_w = (cw - 24) // 2
    y2 = y + 26
    left_end = block(d, x, y2, col_w,
                     "CLIMATE  —  ANTALYA",
                     "COP31 DRAFT DROPS FOSSIL-FUEL PHASE-OUT",
                     "The slimmed-down draft removes all fossil-fuel "
                     "language and keeps a 35% electrification target for "
                     "2035; Panama threatens to block consensus.",
                     34, 20)
    right_end = block(d, x + col_w + 24, y2, col_w,
                      "CONFLICT  —  GAZA",
                      "ISRAELI FORCES CROSS GAZA'S YELLOW LINE",
                      "First incursion across the ceasefire boundary in "
                      "central Gaza since the truce.",
                      34, 20)
    y3 = max(left_end, right_end)
    d.line([x + col_w + 12, y2, x + col_w + 12, y3 - 6], fill=GREY, width=1)
    rule(d, x, y3 + 8, cw, 2)

    # Row three: markets | health | Ukraine.
    c3 = (cw - 48) // 3
    y4 = y3 + 24
    ends = []
    ends.append(block(d, x, y4, c3,
                      "MARKETS",
                      "ASIAN MARKETS PLUNGE ON AI FEARS",
                      "The Nikkei falls 4.8% on Friday; the S&P 500 logs a "
                      "fifth straight loss on Thursday.",
                      27, 19))
    ends.append(block(d, x + c3 + 24, y4, c3,
                      "HEALTH",
                      "KENYA'S LAST EBOLA PATIENT GOES HOME",
                      "Discharged 37 days after the outbreak's first case.",
                      27, 19))
    ends.append(block(d, x + 2 * (c3 + 24), y4, c3,
                      "UKRAINE",
                      "UK PLEDGES 1,000 DRONES FOR UKRAINE",
                      "A 260-million-pound package of long-range drones "
                      "and other capabilities.",
                      27, 19))
    y5 = max(ends)
    for gx in (x + c3 + 12, x + 2 * c3 + 36):
        d.line([gx, y4, gx, y5 - 6], fill=GREY, width=1)
    rule(d, x, y5 + 12, cw, 2)

    # Footer.
    ff = font(SANS_B, 18)
    foot = "SIX TOP STORIES  ·  FRIDAY 20 NOVEMBER 2026  ·  THE WORLD"
    d.text(((W - d.textlength(foot, font=ff)) // 2, y5 + 22), foot,
           font=ff, fill=GREY)
    fs = font(SANS, 15)
    src = "Sources: Reuters  ·  AFP  ·  The Guardian  ·  AP  ·  SPA"
    d.text(((W - d.textlength(src, font=fs)) // 2, y5 + 48), src,
           font=fs, fill=GREY)

    os.makedirs("/output", exist_ok=True)
    img.save("/output/entry.png", format="PNG")


if __name__ == "__main__":
    main()
