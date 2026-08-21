# -*- coding: utf-8 -*-
"""
Renders ONE chocolate bar shape in 4 different colours.
Geometry is identical in every image - only the colour changes.
That is what makes a "CHOOSE THE RIGHT COLOUR" poll look fair.

Usage:  python3 make_chocolate.py
Output: chocolate_brown.png / chocolate_pink.png / chocolate_white.png / chocolate_colourful.png
"""
from PIL import Image, ImageDraw, ImageFilter

S = 1080                      # square canvas - fits YouTube poll tiles
COLS, ROWS = 4, 6             # squares on the bar
BAR_W, BAR_H = 620, 860       # bar size in px
BG = (255, 255, 255)

def shade(c, f):
    """Lighten (f>1) or darken (f<1) an RGB colour."""
    return tuple(max(0, min(255, int(v * f))) for v in c)

def draw_bar(colours, out):
    """colours: a single RGB tuple, or a list of RGB (one per square)."""
    img = Image.new("RGB", (S, S), BG)
    d = ImageDraw.Draw(img)

    x0, y0 = (S - BAR_W) // 2, (S - BAR_H) // 2
    x1, y1 = x0 + BAR_W, y0 + BAR_H

    # soft drop shadow
    sh = Image.new("RGB", (S, S), BG)
    ImageDraw.Draw(sh).rounded_rectangle([x0 + 14, y0 + 18, x1 + 14, y1 + 18],
                                         radius=26, fill=(196, 196, 196))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    img = Image.blend(img, sh, 0.55)
    d = ImageDraw.Draw(img)

    base = colours if isinstance(colours, tuple) else colours[0]
    d.rounded_rectangle([x0, y0, x1, y1], radius=26, fill=shade(base, 0.72))

    pad, gap = 26, 12
    cw = (BAR_W - pad * 2 - gap * (COLS - 1)) / COLS
    ch = (BAR_H - pad * 2 - gap * (ROWS - 1)) / ROWS

    for r in range(ROWS):
        for c in range(COLS):
            col = colours if isinstance(colours, tuple) else colours[(r * COLS + c) % len(colours)]
            sx = x0 + pad + c * (cw + gap)
            sy = y0 + pad + r * (ch + gap)
            ex, ey = sx + cw, sy + ch
            # raised square: dark base, lit top-left face, bright top edge
            d.rounded_rectangle([sx, sy, ex, ey], radius=10, fill=shade(col, 0.60))
            d.rounded_rectangle([sx + 5, sy + 5, ex - 9, ey - 9], radius=8, fill=col)
            d.rounded_rectangle([sx + 5, sy + 5, ex - 9, sy + 5 + ch * 0.30],
                                radius=8, fill=shade(col, 1.16))
    img.save(out, quality=95)
    print("wrote", out)

RAINBOW = [(228, 62, 62), (243, 156, 30), (250, 214, 45),
           (72, 180, 92), (58, 132, 226), (146, 84, 200)]

draw_bar((109, 66, 36),   "chocolate_brown.png")      # CORRECT
draw_bar((235, 130, 175), "chocolate_pink.png")
draw_bar((238, 232, 220), "chocolate_white.png")
draw_bar(RAINBOW,         "chocolate_colourful.png")
