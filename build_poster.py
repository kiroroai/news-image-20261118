#!/usr/bin/env python3
"""Build the broadsheet poster for Wednesday 18 November 2026.

Renders entry.png (1024x1024) with PIL from the story list below.
Every string in this file is a fact checked against at least two
independent news sources (AP, Reuters, BBC, CNN, AFP) on 19 Nov 2026.
Run: python3 build_poster.py   (writes entry.png next to this file)
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 236)
INK = (17, 17, 17)
RED = (164, 31, 31)
GREY = (90, 86, 78)
RULE = (60, 58, 52)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Word-wrap text to fit max_w pixels; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.22)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def centre(draw, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return y + int(fnt.size * 1.2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36  # side margin

    # ---- Masthead -------------------------------------------------
    d.rectangle([0, 0, W, 6], fill=INK)
    y = 22
    y = centre(d, y, "THE WORLD IN ONE DAY", font(SERIF_B, 50))
    d.line([mx, y + 2, W - mx, y + 2], fill=RULE, width=2)
    y += 14
    y = centre(d, y, "WEDNESDAY  18  NOVEMBER  2026", font(SANS_B, 36), fill=RED)
    y += 4
    y = centre(d, y, "THE DAY'S WORLD NEWS  \u00b7  ONE PAGE  \u00b7  EVERY STORY REPORTED TODAY",
               font(SANS, 15), fill=GREY)
    d.line([mx, y + 8, W - mx, y + 8], fill=INK, width=3)
    y += 18

    # ---- Lead story: Iran / Gulf ----------------------------------
    d.text((mx, y), "THE GULF  \u2014  LEAD STORY", font=font(SANS_B, 15), fill=RED)
    y += 24
    y = draw_wrapped(d, mx, y, "IRAN WIDENS GULF WAR TO KUWAIT",
                     font(SERIF_B, 42), W - 2 * mx, leading=48)
    y = draw_wrapped(d, mx, y, "AND BAHRAIN", font(SERIF_B, 42),
                     W - 2 * mx, leading=48)
    y += 4
    y = draw_wrapped(
        d, mx, y,
        "Iranian drones target US Patriot batteries and launchers at Ali Al Salem "
        "air base in Kuwait; Bahrain says its defences intercepted several attacks "
        "before dawn \u2014 a day after US jets struck an Iranian missile site on "
        "Qeshm Island. Kuwait says its air defences engaged the drones; US Central "
        "Command says no American troops were hurt.",
        font(SANS, 18), W - 2 * mx, leading=23)
    y += 8
    d.line([mx, y, W - mx, y], fill=RULE, width=2)
    y += 12

    # ---- Second tier: three columns -------------------------------
    col_w = (W - 2 * mx - 2 * 24) // 3
    cols = [
        ("UKRAINE \u2014 WAR",
         "KERCH BRIDGE ROAD SPAN COLLAPSES",
         "Ukrainian missiles and drones destroy the road arch linking Russia "
         "and Crimea; two people killed and road traffic halted."),
        ("CHINA \u2014 DIPLOMACY",
         "XI AND PUTIN MEET IN SHENZHEN",
         "The two leaders talk ahead of Thursday\u2019s first-ever trilateral "
         "with Trump at the APEC summit in China."),
        ("ASIA-PACIFIC \u2014 SUMMITS",
         "QUAD LEADERS MEET IN MANILA",
         "Australia, India, Japan and the US meet at leader level for the first "
         "time in over two years; Trump claims a \u201cvery big\u201d Philippines "
         "trade deal \u2014 Manila says nothing was signed."),
    ]
    top = y
    bottom = top
    for i, (tag, head, cap) in enumerate(cols):
        x = mx + i * (col_w + 24)
        yy = top
        d.text((x, yy), tag, font=font(SANS_B, 13), fill=RED)
        yy += 20
        yy = draw_wrapped(d, x, yy, head, font(SERIF_B, 22),
                          col_w, leading=26)
        yy += 3
        yy = draw_wrapped(d, x, yy, cap, font(SANS, 14), col_w, leading=18)
        bottom = max(bottom, yy)
        if i < 2:
            d.line([x + col_w + 12, top, x + col_w + 12, bottom + 4],
                   fill=RULE, width=1)
    y = bottom + 10
    d.line([mx, y, W - mx, y], fill=INK, width=3)
    y += 8
    d.text((mx, y), "ALSO TODAY", font=font(SANS_B, 15), fill=RED)
    y += 24

    # ---- Grid: 2 columns x 5 rows ---------------------------------
    grid = [
        ("US POLITICS",
         "Peltola wins Alaska; Democrats take Senate 56\u201344",
         "Mary Peltola beats Sen. Dan Sullivan in the last midterm race \u2014 "
         "the Democrats\u2019 ninth Senate pickup."),
        ("ISRAEL",
         "Knesset elects Kahana speaker in blow to Netanyahu",
         "Matan Kahana wins 66\u201352; Trump\u2019s Board of Peace faults Israel "
         "and Hamas over the Gaza ceasefire."),
        ("GAZA",
         "950,000 displaced Gazans on flood-prone ground",
         "WHO warns as the war\u2019s fourth winter begins; cold and flooding "
         "threaten camps across the Strip."),
        ("AFRICA \u2014 HEALTH",
         "Ebola in DR Congo passes 11,000 cases",
         "Nearly 3 in 4 infected children under 5 die, health officials report."),
        ("US \u2014 HEALTH",
         "America loses measles-free status after 26 years",
         "More than 5,400 cases and 10 deaths this year, the worst since the "
         "early 1990s."),
        ("TECH \u2014 MARKETS",
         "Nvidia posts record $115.8bn in sales",
         "Revenue doubles year on year; the board rules out Jensen Huang "
         "returning as chief executive."),
        ("UKRAINE \u2014 WAR",
         "Russia launches 141 drones at Ukraine overnight",
         "Air defences down 126; three hurt in Kyiv as debris falls on "
         "several districts."),
        ("CULTURE",
         "Word of the year 2026: \u201cHuman\u201d",
         "Cambridge Dictionary picks the 15th-century word as AI blurs what "
         "it means to be human."),
    ]
    gw = (W - 2 * mx - 28) // 2
    gh = 94
    for idx, (tag, head, cap) in enumerate(grid):
        r, c = divmod(idx, 2)
        x = mx + c * (gw + 28)
        yy = y + r * gh
        d.text((x, yy), tag, font=font(SANS_B, 12), fill=RED)
        yy += 17
        yy = draw_wrapped(d, x, yy, head, font(SERIF_B, 19), gw, leading=22)
        yy += 1
        draw_wrapped(d, x, yy, cap, font(SANS, 14), gw, leading=17)
        if c == 0:
            d.line([x + gw + 14, y + r * gh, x + gw + 14, y + (r + 1) * gh - 10],
                   fill=RULE, width=1)

    # ---- Footer ----------------------------------------------------
    fy = H - 26
    d.line([mx, fy - 8, W - mx, fy - 8], fill=RULE, width=1)
    centre(d, fy, "All events reported on Wednesday 18 November 2026  \u00b7  "
                  "Sources: AP, Reuters, BBC, CNN, AFP",
           font(SANS, 12), fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
