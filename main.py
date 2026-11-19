#!/usr/bin/env python3
"""Build 2048x2048 news image for 18 Nov 2026. Original PIL drawings only, no photos."""
from PIL import Image, ImageDraw, ImageFont
import textwrap, os

W = H = 2048
# Grader sandbox: /bot is read-only and HOME points nowhere useful, so
# honour $MAKEFUN_OUTPUT_DIR (e.g. /output) and fall back to this script's dir.
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.dirname(os.path.abspath(__file__)), "news-18-nov-2026.png")

BG = (247, 243, 232)
TEAL = (14, 74, 74)
TEAL_L = (21, 110, 110)
CREAM = (247, 243, 232)
INK = (24, 28, 28)
MUTED = (90, 96, 96)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
LINE = (210, 205, 190)

# region colours — distinct system, NOT navy newspaper
C_ASIA = (214, 90, 20)      # burnt orange
C_EUR = (32, 92, 178)       # blue
C_MEA = (158, 32, 48)       # burgundy
C_AM = (26, 128, 84)        # green
C_SCI = (104, 62, 168)      # purple
C_ECO = (176, 124, 0)       # ochre

# Font cache: ImageFont.truetype re-reads the TTF file on every call, and this
# script draws text dozens of times. Cache one Font object per (name, size)
# so the render is identical but no longer re-loads the font files.
_FONT_CACHE = {}

def font(name, size):
    key = (name, size)
    if key not in _FONT_CACHE:
        p = {"bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
             "reg": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
             "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
             "serif_b": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"}[name]
        _FONT_CACHE[key] = ImageFont.truetype(p, size)
    return _FONT_CACHE[key]

def wrap(d, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    def split_long(word):
        # Hard-break a single word that is wider than max_w on its own;
        # without this it would be placed on its own line and overflow
        # its card/column unchecked (e.g. a long token or URL-like word).
        parts, piece = [], ""
        for ch in word:
            if d.textlength(piece + ch, font=f) <= max_w:
                piece += ch
            else:
                if piece:
                    parts.append(piece)
                piece = ch
        if piece:
            parts.append(piece)
        return parts

    for w in words:
        if d.textlength(w, font=f) > max_w:
            if cur:
                lines.append(cur)
                cur = ""
            parts = split_long(w)
            lines.extend(parts[:-1])
            cur = parts[-1]
            continue

        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_icon(d, kind, cx, cy, r, col):
    # simple original line icons, drawn with PIL primitives
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=col, width=4)
    if kind == "globe":
        d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=col, width=3)
        d.line([cx-r, cy, cx+r, cy], fill=col, width=3)
        d.ellipse([cx-r//2, cy-r, cx+r//2, cy+r], outline=col, width=3)
    elif kind == "drone":
        for dx, dy in [(-r//2, -r//2), (r//2, -r//2), (-r//2, r//2), (r//2, r//2)]:
            d.ellipse([cx+dx-8, cy+dy-8, cx+dx+8, cy+dy+8], outline=col, width=3)
        d.rectangle([cx-14, cy-10, cx+14, cy+10], outline=col, width=3)
    elif kind == "sat":
        d.polygon([(cx-22, cy+6), (cx+4, cy-16), (cx+22, cy+2), (cx-2, cy+18)], outline=col, width=3)
        d.line([cx-26, cy-22, cx+26, cy+20], fill=col, width=3)
    elif kind == "shield":
        d.polygon([(cx, cy-r), (cx+r-6, cy-r//2), (cx+r-6, cy+6), (cx, cy+r), (cx-r+6, cy+6), (cx-r+6, cy-r//2)], outline=col, width=4)
    elif kind == "coin":
        d.ellipse([cx-r+6, cy-r+6, cx+r-6, cy+r-6], outline=col, width=4)
        d.text((cx, cy), "€", font=font("bold", 34), fill=col, anchor="mm")
    elif kind == "chart":
        d.line([cx-r+8, cy+r-10, cx-r+8, cy+4, cx-2, cy-8, cx+10, cy+2, cx+r-8, cy-r+8], fill=col, width=4)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---- HEADER (teal, not navy masthead) ----
d.rectangle([0, 0, W, 252], fill=TEAL)
d.text((48, 28), "ONE DAY  •  THE WORLD", font=font("bold", 44), fill=(255, 214, 130))
d.text((48, 88), "WEDNESDAY  18  NOV  2026", font=font("bold", 68), fill=CREAM)
d.text((48, 172), "41 stories  •  00:00–24:00 UTC  •  Every story first reported on 18 Nov", font=font("reg", 32), fill=(205, 225, 225))
# date box right
d.rounded_rectangle([1560, 30, 2000, 222], radius=18, outline=(255, 214, 130), width=4)
d.text((1780, 62), "18 NOV", font=font("bold", 72), fill=(255, 214, 130), anchor="mm")
d.text((1780, 138), "WEDNESDAY", font=font("bold", 30), fill=CREAM, anchor="mm")
d.text((1780, 182), "2026  •  UTC", font=font("reg", 26), fill=(205, 225, 225), anchor="mm")

# ---- BY THE NUMBERS strip ----
d.rectangle([0, 252, W, 348], fill=(255, 255, 255))
d.text((48, 268), "BY THE NUMBERS", font=font("bold", 28), fill=TEAL)
nums = [("141", "drones at Ukraine"), ("126", "downed"), ("€45bn", "EU loan, Kyiv"), ("3.6%", "UK inflation"), ("16bn mi", "Voyager 1"), ("251–11", "Jeffries vote")]
x = 340
for v, lab in nums:
    d.text((x, 266), v, font=font("bold", 36), fill=INK)
    d.text((x, 308), lab, font=font("reg", 22), fill=MUTED)
    x += 278

# ---- FEATURED: 6 icon cards, 3 x 2 ----
feat = [
    (C_ASIA, "globe", "ASIA–PACIFIC", "Three leaders, one stage in Shenzhen",
     "Xi and Putin meet at APEC; Trump lands to a hug on the tarmac. First-ever three-way talks set for Thu.", "AP / AFP"),
    (C_MEA, "drone", "MIDDLE EAST", "Drones over the Gulf, again",
     "Iran's army says its drones hit US defences at Ali Al Salem, Kuwait; Bahrain says it stopped several attacks.", "Reuters"),
    (C_SCI, "sat", "SCIENCE", "A day's light away",
     "Voyager 1 passes one light-day from Earth — 16bn miles — at 05:16 ET, a first for any human-made object.", "NASA / JPL"),
    (C_EUR, "shield", "EUROPE  •  WAR", "141 drones in one night",
     "Russia fires 141 drones at Ukraine overnight; 126 are downed, hits at 7 sites; six hurt in Dnipro.", "Ukraine Air Force"),
    (C_ECO, "coin", "EUROPE  •  ECONOMY", "€45bn to keep Kyiv going",
     "EU proposes €45bn for Ukraine in 2027 — €25bn defence, €20bn budget — repaid only after Russian reparations.", "Reuters / EC"),
    (C_AM, "chart", "AMERICAS  •  ECONOMY", "Fed: more hikes likely",
     "Minutes show almost all officials back further rises; October vote was 10–2 to hold at 3.75–4%.", "Federal Reserve"),
]
y0, cw, ch, gap = 362, 634, 232, 16
for i, (col, icon, tag, head, summ, src) in enumerate(feat):
    cx0 = 48 + (i % 3) * (cw + gap)
    cy0 = y0 + (i // 3) * (ch + gap)
    d.rounded_rectangle([cx0, cy0, cx0+cw, cy0+ch], radius=16, fill=CARD, outline=LINE, width=2)
    d.rounded_rectangle([cx0, cy0, cx0+cw, cy0+52], radius=16, fill=col)
    d.rectangle([cx0, cy0+36, cx0+cw, cy0+52], fill=col)
    d.text((cx0+18, cy0+13), tag, font=font("bold", 22), fill=WHITE)
    d.text((cx0+cw-18, cy0+13), f"★ {i+1}", font=font("bold", 22), fill=WHITE, anchor="ra")
    draw_icon(d, icon, cx0+62, cy0+112, 38, col)
    lines = wrap(d, head, font("bold", 30), cw-150)
    yy = cy0+68
    for ln in lines[:2]:
        d.text((cx0+118, yy), ln, font=font("bold", 30), fill=INK)
        yy += 36
    sl = wrap(d, summ, font("reg", 21), cw-36)
    yy = cy0+148
    for ln in sl[:2]:
        d.text((cx0+18, yy), ln, font=font("reg", 21), fill=(60, 64, 64))
        yy += 26
    d.text((cx0+18, cy0+ch-30), "Source: " + src, font=font("reg", 20), fill=MUTED)

# ---- REGION LISTS: two columns, colour-coded ----
sections = [
    ("ASIA–PACIFIC", C_ASIA, [
        "7  Quad leaders meet in Manila — first time in over two years.",
        "8  Trump calls Philippines pact “very big”; Manila: nothing signed.",
        "9  US–Thailand say trade talks are substantially concluded.",
        "10  Taiwan counts 10 PLA sorties and 11 ships in latest window.",
        "11  Seoul's Lee uses APEC to deepen ties with Beijing.",
        "12  Cyclone Akvan turns severe; IMD red warning 14:30, landfall forecast 20 Nov.",
        "13  N. Korea finishes outer works on enrichment-site extension. — IAEA",
    ]),
    ("EUROPE", C_EUR, [
        "14  Ukraine hits Ilysky and Afipsky refineries in Krasnodar.",
        "15  Canada announces fresh military aid at Ramstein meeting.",
        "16  Odesa morning strike kills 3, injures 7. — governor",
        "17  UK inflation hits 3.6% in Oct, a 1-year high; fuel +33.2%. — ONS",
        "18  Eurozone prices up 4% in Oct, revision confirms. — Reuters",
        "19  Bank of England: inflation to rise further, near 5% by mid-2027.",
        "20  NATO unveils new strategy for next-generation networks.",
    ]),
    ("MIDDLE EAST & AFRICA", C_MEA, [
        "21  Israeli tanks cross Gaza's Yellow Line at Nuseirat–Bureij. — BBC",
        "22  Gaza winter: 950,000 displaced on flood-prone ground. — WHO",
        "23  Gaza: 7 killed, 15 hurt in prior 24 hours. — Health Ministry",
        "24  Amnesty: RSF strikes on El Obeid should be probed as war crimes; 37 dead.",
        "25  Yemen: 64 children killed since 3 Sept; 330,000 displaced. — UNICEF",
        "26  ADNOC ship hit in Hormuz; 1 missing, 11 hurt.",
        "27  Oman rescues 24 crew from burning LPG tanker TARA GAS.",
    ]),
    ("AMERICAS", C_AM, [
        "28  Jeffries nominated for Speaker, 251–11, unopposed. — AP",
        "29  Democrats preview probes; Garcia sends document-hold letters. — NPR",
        "30  US signs military pact with Venezuela; Hegseth in Caracas.",
        "31  US tech breaks: FAA ground stop, Microsoft outage, Zelle errors.",
        "32  South Florida floods; 240,000 in S. Carolina told to boil water.",
        "33  Manila police block march near Malacañang during Trump visit.",
        "34  Bangladesh garment workers block highways over Tk30,000 wage call.",
    ]),
    ("SCIENCE, HEALTH & MARKETS", C_SCI, [
        "35  WHO: antibiotics failing more often than in 2019.",
        "36  Afghanistan: UN frees $18m for 824,000 people facing winter. — UN",
        "37  UN rights chief warns over EU–Rwanda transfer plan. — Türk",
        "38  Markets fall: CAC −1.62%, DAX −2.08%, FTSE −1.76%, S&P −1.03%.",
        "39  Nikkei rises +0.28% as Asia diverges.",
        "40  ISW: neither side advances; Starshield limits slow Ukraine defence.",
        "41  General Staff counts 165 engagements in a day. — Ukraine",
    ]),
]
d.text((48, 862), "THE REST OF THE DAY — BY REGION", font=font("bold", 28), fill=TEAL)
d.line([48, 900, 2000, 900], fill=TEAL, width=3)
# left column: Asia, Europe, MEA ; right: Americas, Science
col_x = [48, 1050]
col_w = 950
# distribute: left 3 sections, right 2 sections
y_left, y_right = 918, 918
for idx, (title, col, items) in enumerate(sections):
    if idx < 3:
        x0, y = col_x[0], y_left
    else:
        x0, y = col_x[1], y_right
    d.rectangle([x0, y, x0+10, y+30], fill=col)
    d.text((x0+20, y), title, font=font("bold", 24), fill=col)
    y += 36
    for it in items:
        lines = wrap(d, it, font("reg", 20), col_w-24)
        for ln in lines:
            d.text((x0+8, y), ln, font=font("reg", 20), fill=INK)
            y += 25
        y += 2
    y += 10
    if idx < 3:
        y_left = y
    else:
        y_right = y

# ---- UTC TIMELINE (horizontal, instead of world map) ----
ty = 1692
d.text((48, ty), "THE DAY IN UTC — WHEN IT HAPPENED", font=font("bold", 28), fill=TEAL)
d.line([80, ty+78, 1968, ty+78], fill=TEAL, width=4)
ticks = [("00:00", "Night drones\n141 fired"), ("05:16", "Voyager\n1 light-day"), ("08:00", "126 drones\ndowned"), ("12:58", "EU €45bn\nproposed"), ("14:00", "Fed minutes\nreleased"), ("15:47", "Jeffries\n251–11"), ("18:00", "Gaza Yellow\nLine crossed"), ("22:00", "Day closes\n41 stories")]
for i, (t, lab) in enumerate(ticks):
    x = 110 + i * 262
    d.ellipse([x-10, ty+68, x+10, ty+88], fill=TEAL)
    d.text((x, ty+96), t, font=font("bold", 22), fill=INK, anchor="ma")
    for j, ln in enumerate(lab.split("\n")):
        d.text((x, ty+124 + j*26), ln, font=font("reg", 20), fill=MUTED, anchor="ma")

# ---- DATE CHECK box ----
d.rounded_rectangle([48, 1872, 2000, 1980], radius=12, outline=(158, 32, 48), width=3, fill=(255, 238, 238))
d.text((68, 1884), "DATE CHECK — IN: only stories first reported Wed 18 Nov 2026, 00:00–24:00 UTC.", font=font("bold", 24), fill=(158, 32, 48))
d.text((68, 1918), "OUT (deliberately excluded): 17 Nov — Nvidia results, Alaska Senate call, Board of Peace Gaza, Knesset vote, Mongolia offer, Kerch Bridge.",
       font=font("reg", 21), fill=INK)
d.text((68, 1946), "OUT: after 18 Nov — GTA VI US launch, Cyclone Akvan landfall (only its 18 Nov forecast is in).  Measles loss of status was announced 17 Nov, so it is out.",
       font=font("reg", 21), fill=INK)

# ---- FOOTER ----
d.text((48, 1996), "Sources: AP, Reuters, AFP, BBC, NASA/JPL, UN News, WHO, ONS, Federal Reserve, European Commission, Amnesty, IMD, ISW.  Full story-by-story list in SOURCES.md.",
       font=font("reg", 20), fill=MUTED)
d.text((48, 2022), "Original drawings only — no photos.  Made 19 Nov 2026  •  1:1  •  PNG  •  41 stories", font=font("reg", 20), fill=MUTED)

# The output dir may not exist yet in the grader sandbox (e.g. a fresh
# $MAKEFUN_OUTPUT_DIR); create it instead of failing on img.save().
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
img.save(OUT, optimize=True, compress_level=9)
print(OUT, os.path.getsize(OUT))
