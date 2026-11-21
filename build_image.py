#!/usr/bin/env python3
"""Build the 1024x1024 news-summary image for make.fun bounty news-image-20261120.
Flat vector style, dark navy + warm orange, all text drawn with PIL for legibility.
Output: news.png (1024x1024, must be <= 1 MiB).
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (14, 26, 43)
NAVY2 = (20, 38, 62)
ORANGE = (249, 115, 22)
ORANGE_L = (255, 150, 60)
WHITE = (255, 255, 255)
GRAY = (196, 205, 216)
RED = (239, 68, 68)
RED_D = (185, 28, 28)
GREEN = (34, 197, 94)

FDIR = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(FDIR + name, size)

f_kicker = font("DejaVuSans-Bold.ttf", 30)
f_title = font("DejaVuSans-Bold.ttf", 72)
f_sub = font("DejaVuSans-Bold.ttf", 30)
f_head = font("DejaVuSans-Bold.ttf", 37)
f_body = font("DejaVuSans.ttf", 27)
f_small = font("DejaVuSans.ttf", 23)
f_num = font("DejaVuSans-Bold.ttf", 44)

img = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(img)

# Top orange bar
d.rectangle([0, 0, W, 10], fill=ORANGE)

# Kicker
d.text((48, 36), "FRIDAY  •  20 NOVEMBER 2026", font=f_kicker, fill=ORANGE_L)
# Title
d.text((48, 78), "THE WORLD", font=f_title, fill=WHITE)
d.text((48, 152), "IN ONE DAY", font=f_title, fill=ORANGE)
# Divider
d.rectangle([48, 248, 976, 252], fill=(60, 80, 110))

stories = [
    ("01", "MARKETS IN MELTDOWN",
     "Nasdaq -5.3%, S&P 500 -3.7%, Dow -950 pts. Bitcoin sinks below $57,000 — its lowest since Sept 2024."),
    ("02", "NVIDIA IN TURMOIL",
     "Shares -14% in a day. CEO Jensen Huang resigns amid scandal; the SEC is said to probe its accounting."),
    ("03", "ANTHROPIC'S RECORD IPO",
     "The biggest IPO ever debuts +34%, then slides back to $88.91 — almost its $83 issue price."),
    ("04", "SEC CHARGES $560M PONZI",
     "Backward Hat Capital accused of defrauding 2,000+ investors with fake AI FX trading since 2022."),
]

y = 282
for num, head, body in stories:
    # number badge
    d.rounded_rectangle([48, y, 108, y + 60], radius=8, fill=ORANGE)
    tw = d.textlength(num, font=f_num)
    d.text((48 + (60 - tw) / 2, y + 6), num, font=f_num, fill=NAVY)
    # headline
    d.text((132, y + 2), head, font=f_head, fill=WHITE)
    # body wrapped
    lines = textwrap.wrap(body, width=52)
    by = y + 52
    for ln in lines:
        d.text((132, by), ln, font=f_body, fill=GRAY)
        by += 34
    y = by + 26
    if num != "04":
        d.line([48, y - 12, 976, y - 12], fill=(40, 58, 84), width=2)

# Bottom strip: mini candlestick chart (red, descending) + ticker
chart_x0, chart_y0, chart_w, chart_h = 48, 868, 560, 110
d.rounded_rectangle([36, 856, 636, 990], radius=10, fill=NAVY2)
candles = [(0.92, 0.88), (0.86, 0.78), (0.80, 0.68), (0.70, 0.55), (0.58, 0.42), (0.46, 0.30), (0.34, 0.18)]
cw = chart_w // len(candles)
for i, (lo_frac, hi_frac) in enumerate(candles):
    cx = chart_x0 + i * cw + cw // 2
    y_hi = chart_y0 + int(hi_frac * chart_h)
    y_lo = chart_y0 + int(lo_frac * chart_h)
    d.line([cx, y_hi - 8, cx, y_lo + 8], fill=RED, width=3)
    d.rectangle([cx - 16, y_hi, cx + 16, y_lo], fill=RED_D if i % 2 else RED)
d.text((660, 872), "BTC  $55,950", font=f_head, fill=WHITE)
d.text((660, 920), "-9.6% today", font=f_head, fill=RED)
d.text((48, 1000 - 14), "", font=f_small, fill=GRAY)

img.save("/home/hatch/workspace/makefun-news-image/news.png", "PNG", optimize=True)
import os
print("saved", os.path.getsize("/home/hatch/workspace/makefun-news-image/news.png"), "bytes")
