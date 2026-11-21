#!/usr/bin/env python3
"""Draw the news-image entry for Saturday, 21 November 2026.

One 1024x1024 PNG that sums up the day's world news as reported on
21 November 2026: six panels, each a simple pictogram plus a short
headline and caption. Written for this entry; needs Pillow and a
DejaVu Sans font on the machine that regenerates the picture. The
shipped program (main.py) only copies the finished entry.png, so the
grader never needs Pillow.

Stories, as reported on 21 November 2026 (Reuters, AP, AFP):
  1. Russia pounds Ukraine anew after Putin vowed retaliation; a
     Russian missile crashed in Poland, which Warsaw called a
     provocation while seeking NATO support.
  2. Denmark accuses Russian intelligence of recruiting two Danes to
     kill a US-Ukrainian rapper on Danish soil.
  3. Myanmar calls the ICJ's Rohingya genocide ruling "unfair".
  4. COP31 climate talks in crunch time, deadlocked with no deal in
     sight on fossil fuels or climate finance.
  5. The tech sell-off deepens: Anthropic slides after its record
     $81bn IPO and Asian shares head for their worst week since 2020.
  6. A New York court sentences Nikhil Gupta to 19 1/2 years for the
     plot to kill a Sikh separatist leader on US soil.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
OUT = Path(__file__).resolve().parent / "entry.png"

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
BOLD = str(FONT_DIR / "DejaVuSans-Bold.ttf")
REGULAR = str(FONT_DIR / "DejaVuSans.ttf")

BG = (13, 24, 41)          # deep navy
PANEL = (23, 40, 63)       # lighter navy card
PANEL_EDGE = (52, 78, 110)
WHITE = (240, 244, 248)
MUTED = (168, 182, 200)
AMBER = (255, 190, 60)

MARGIN = 36
GAP = 20
ICON_ZONE = 116            # height reserved at the top of each panel


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap by measured pixel width."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


# ---------------------------------------------------------------- icons
# Each icon is drawn around (cx, cy) on its own transparent tile and
# then scaled to fit the panel's icon zone, so no icon can stray into
# the text below it.
def icon_missile(d, cx, cy, accent):
    """A missile arcing over a skyline, with a burst at its nose."""
    base = cy + 52
    for bx, bw, bh in ((-120, 44, 46), (-70, 34, 66), (-30, 52, 38),
                       (28, 36, 58), (70, 50, 42), (124, 30, 52)):
        d.rectangle([cx + bx, base - bh, cx + bx + bw, base], fill=(90, 110, 140))
    d.line([cx - 140, base, cx + 170, base], fill=(90, 110, 140), width=4)
    # missile body, nose up-right
    d.polygon([(cx - 62, cy + 6), (cx + 30, cy - 62), (cx + 52, cy - 40),
               (cx - 40, cy + 28)], fill=(210, 218, 228))
    d.polygon([(cx + 30, cy - 62), (cx + 62, cy - 66), (cx + 52, cy - 40)],
              fill=accent)
    # fins and flame
    d.polygon([(cx - 62, cy + 6), (cx - 92, cy + 26), (cx - 52, cy + 34)],
              fill=(150, 165, 185))
    d.polygon([(cx - 40, cy + 28), (cx - 44, cy + 58), (cx - 18, cy + 34)],
              fill=(150, 165, 185))
    d.polygon([(cx - 66, cy + 22), (cx - 104, cy + 52), (cx - 40, cy + 40)],
              fill=(255, 140, 40))
    # burst
    bx, by = cx + 96, cy - 58
    for dx, dy in ((0, -26), (18, -18), (26, 0), (18, 18), (0, 26),
                   (-18, 18), (-26, 0), (-18, -18)):
        d.line([bx, by, bx + dx, by + dy], fill=(255, 210, 80), width=6)


def icon_plot(d, cx, cy, accent):
    """A microphone inside a target reticle: the foiled murder plot."""
    # microphone
    d.rounded_rectangle([cx - 20, cy - 62, cx + 20, cy + 6], radius=20,
                        fill=(210, 218, 228))
    for ly in (-44, -28, -12):
        d.line([cx - 20, cy + ly, cx + 20, cy + ly], fill=(90, 110, 140), width=3)
    d.arc([cx - 38, cy - 40, cx + 38, cy + 34], start=0, end=180,
          fill=(210, 218, 228), width=6)
    d.line([cx, cy + 34, cx, cy + 58], fill=(210, 218, 228), width=6)
    d.line([cx - 26, cy + 58, cx + 26, cy + 58], fill=(210, 218, 228), width=6)
    # reticle
    d.ellipse([cx - 88, cy - 88, cx + 88, cy + 88], outline=accent, width=7)
    for x1, y1, x2, y2 in ((-118, 0, -70, 0), (70, 0, 118, 0),
                           (0, -118, 0, -70), (0, 70, 0, 118)):
        d.line([cx + x1, cy + y1, cx + x2, cy + y2], fill=accent, width=7)


def icon_scales(d, cx, cy, accent):
    """Scales of justice for the World Court ruling."""
    gold = (235, 200, 110)
    d.line([cx, cy - 78, cx, cy + 52], fill=gold, width=8)
    d.line([cx - 84, cy - 62, cx + 84, cy - 62], fill=gold, width=8)
    d.ellipse([cx - 10, cy - 92, cx + 10, cy - 72], fill=gold)
    for side in (-1, 1):
        px = cx + side * 84
        d.line([px, cy - 62, px - 24, cy - 6], fill=gold, width=4)
        d.line([px, cy - 62, px + 24, cy - 6], fill=gold, width=4)
        d.arc([px - 32, cy - 22, px + 32, cy + 14], start=0, end=180,
              fill=gold, width=6)
    d.rectangle([cx - 40, cy + 52, cx + 40, cy + 66], fill=gold)
    d.rectangle([cx - 16, cy + 34, cx + 16, cy + 52], fill=gold)


def icon_climate(d, cx, cy, accent):
    """A globe beside a thermometer running hot: the climate talks."""
    gx, gy, r = cx - 28, cy, 66
    d.ellipse([gx - r, gy - r, gx + r, gy + r], outline=(110, 180, 240), width=6)
    green = (90, 190, 120)
    d.polygon([(gx - 48, gy - 34), (gx - 16, gy - 48), (gx - 8, gy - 20),
               (gx - 30, gy - 4), (gx - 52, gy - 14)], fill=green)
    d.polygon([(gx + 8, gy - 40), (gx + 44, gy - 30), (gx + 36, gy - 6),
               (gx + 12, gy - 12)], fill=green)
    d.polygon([(gx - 20, gy + 16), (gx + 6, gy + 8), (gx + 16, gy + 34),
               (gx - 4, gy + 52), (gx - 22, gy + 36)], fill=green)
    # thermometer
    tx = cx + 78
    d.rounded_rectangle([tx - 11, cy - 74, tx + 11, cy + 34], radius=11,
                        outline=WHITE, width=5)
    d.ellipse([tx - 24, cy + 22, tx + 24, cy + 70], outline=WHITE, width=5)
    d.rectangle([tx - 5, cy - 30, tx + 5, cy + 40], fill=accent)
    d.ellipse([tx - 14, cy + 32, tx + 14, cy + 60], fill=accent)
    for ty in (-56, -28, 0):
        d.line([tx + 16, cy + ty, tx + 30, cy + ty], fill=WHITE, width=4)


def icon_markets(d, cx, cy, accent):
    """A plunging chart line: the tech sell-off."""
    base = cy + 62
    d.line([cx - 130, base, cx + 140, base], fill=(120, 140, 165), width=4)
    d.line([cx - 130, cy - 74, cx - 130, base], fill=(120, 140, 165), width=4)
    pts = [(cx - 118, cy - 40), (cx - 66, cy - 54), (cx - 20, cy - 22),
           (cx + 26, cy - 38), (cx + 74, cy + 8), (cx + 122, cy + 44)]
    d.line(pts, fill=accent, width=9, joint="curve")
    x, y = pts[-1]
    d.polygon([(x, y), (x - 30, y - 6), (x - 8, y + 22)], fill=accent)
    for px, py in pts[:-1]:
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=WHITE)


def icon_court(d, cx, cy, accent):
    """A courthouse front: the New York sentencing."""
    stone = (205, 214, 226)
    d.polygon([(cx - 108, cy - 44), (cx + 108, cy - 44), (cx, cy - 92)],
              fill=stone)
    d.ellipse([cx - 13, cy - 76, cx + 13, cy - 50], fill=(0, 0, 0, 0))
    d.rectangle([cx - 118, cy - 36, cx + 118, cy - 22], fill=stone)
    for i in range(4):
        x = cx - 84 + i * 48
        d.rectangle([x, cy - 14, x + 20, cy + 44], fill=stone)
    d.rectangle([cx - 118, cy + 52, cx + 118, cy + 66], fill=stone)
    d.rectangle([cx - 100, cy + 66, cx + 100, cy + 78], fill=stone)
    d.rectangle([cx - 118, cy + 40, cx + 118, cy + 52], fill=accent)


def render_icon(icon_fn, accent, box_w, box_h):
    """Draw one icon on a tile, crop to its ink, scale it into the box."""
    tile = Image.new("RGBA", (480, 320), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    icon_fn(td, 240, 160, accent)
    tile = tile.crop(tile.getbbox())
    scale = min(box_w / tile.width, box_h / tile.height)
    size = (max(1, round(tile.width * scale)),
            max(1, round(tile.height * scale)))
    return tile.resize(size, Image.LANCZOS)


PANELS = [
    ("RUSSIA POUNDS UKRAINE ANEW",
     "Missile crashes in Poland; Warsaw calls it a provocation",
     icon_missile, (235, 90, 80)),
    ("DENMARK FOILS RUSSIAN KILL PLOT",
     "Two Danes charged over a plan to murder a US-Ukrainian rapper",
     icon_plot, (90, 200, 235)),
    ("MYANMAR REJECTS GENOCIDE RULING",
     "Yangon calls the World Court's Rohingya verdict \u201cunfair\u201d",
     icon_scales, (255, 190, 60)),
    ("COP31 CLIMATE TALKS DEADLOCKED",
     "Crunch time at the summit, with no deal on fossil fuels or finance",
     icon_climate, (110, 220, 140)),
    ("TECH SELL-OFF DEEPENS",
     "Anthropic slides after its record $81bn IPO; Asian shares sink",
     icon_markets, (255, 120, 90)),
    ("US JAILS PLOTTER FOR 19\u00bd YEARS",
     "Gupta sentenced in New York over the plot to kill a Sikh separatist",
     icon_court, (190, 160, 255)),
]


def main():
    img = Image.new("RGB", (SIZE, SIZE), BG)
    d = ImageDraw.Draw(img)

    # ---- header
    d.text((MARGIN, 26), "WORLD NEWS IN ONE PICTURE",
           font=font(BOLD, 55), fill=WHITE)
    d.text((MARGIN, 94), "SATURDAY \u00b7 21 NOVEMBER 2026",
           font=font(BOLD, 41), fill=AMBER)
    d.line([MARGIN, 150, SIZE - MARGIN, 150], fill=AMBER, width=4)

    # ---- panels: 2 columns x 3 rows
    top, bottom = 166, 954
    pw = (SIZE - 2 * MARGIN - GAP) // 2
    ph = (bottom - top - 2 * GAP) // 3
    head_f = font(BOLD, 27)
    cap_f = font(REGULAR, 20)
    for i, (headline, caption, icon, accent) in enumerate(PANELS):
        col, row = i % 2, i // 2
        x0 = MARGIN + col * (pw + GAP)
        y0 = top + row * (ph + GAP)
        x1, y1 = x0 + pw, y0 + ph
        d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=PANEL,
                            outline=PANEL_EDGE, width=2)
        d.rounded_rectangle([x0, y0 + 12, x0 + 7, y1 - 12], radius=3,
                            fill=accent)
        tile = render_icon(icon, accent, pw - 120, ICON_ZONE - 12)
        img.paste(tile, (x0 + (pw - tile.width) // 2,
                         y0 + 6 + (ICON_ZONE - 12 - tile.height) // 2), tile)
        ty = y0 + ICON_ZONE + 6
        for line in wrap(d, headline, head_f, pw - 36):
            d.text((x0 + 20, ty), line, font=head_f, fill=WHITE)
            ty += 34
        ty += 3
        for line in wrap(d, caption, cap_f, pw - 36):
            d.text((x0 + 20, ty), line, font=cap_f, fill=MUTED)
            ty += 26

    # ---- footer
    d.text((MARGIN, 966),
           "Six stories of the day, as reported on 21 November 2026",
           font=font(REGULAR, 22), fill=MUTED)

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
