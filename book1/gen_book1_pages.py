# -*- coding: utf-8 -*-
# Book 1 interior generator: 50 bold & easy Aussie animal pages
# Canvas: 2550x3300 px = 8.5x11 in @ 300 DPI. Pure black lines on white.
# Caption strip: y >= 2900 kept empty (typeset separately by assembler).

import os, math
from PIL import Image, ImageDraw

W, H = 2550, 3300
S = 30          # main stroke width (~0.1 in print)
S2 = 20         # secondary stroke
CAP_TOP = 2900  # caption zone starts here

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "raw")
os.makedirs(OUT, exist_ok=True)

def canvas():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    return img, d

def E(d, cx, cy, rx, ry, w=S):
    d.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], outline=(0,0,0), width=w)

def C(d, cx, cy, r, w=S):
    E(d, cx, cy, r, r, w)

def L(d, x1, y1, x2, y2, w=S):
    d.line([x1, y1, x2, y2], fill=(0,0,0), width=w)

def A(d, cx, cy, rx, ry, a0, a1, w=S):
    d.arc([cx-rx, cy-ry, cx+rx, cy+ry], a0, a1, fill=(0,0,0), width=w)

def P(d, pts, w=S):
    if len(pts) > 2:
        d.polygon(pts, outline=(0,0,0), width=w)

def eyes(d, cx, cy, s, spread=1.0, sm=0.22):
    C(d, cx - s*spread, cy, s*sm, S2)
    C(d, cx + s*spread, cy, s*sm, S2)

def smile(d, cx, cy, s, a0=30, a1=150):
    A(d, cx, cy, s*0.55, s*0.4, a0, a1)

def happy_face(d, cx, cy, s, spread=1.0):
    eyes(d, cx, cy, s, spread)
    smile(d, cx, cy + s*0.25, s)

def leaf(d, cx, cy, s, ang=0.0, w=S2):
    pts = []
    for i in range(26):
        t = 2*math.pi*i/26
        r = s*(1.0 + 0.85*math.cos(t))/1.85
        pts.append((cx + r*math.cos(t + ang), cy + 0.55*r*math.sin(t + ang)))
    P(d, pts, w)

def branch(d, x1, y1, x2, y2):
    L(d, x1, y1, x2, y2, S)
    for t in (0.3, 0.55, 0.78):
        bx = x1 + (x2-x1)*t; by = y1 + (y2-y1)*t
        leaf(d, bx + 70, by - 55, 95, math.pi*0.15)
        leaf(d, bx - 60, by - 30, 85, math.pi*0.85)

def grass(d, cx, cy, s, n=6):
    for i in range(n):
        a = -math.pi/2 + (i-(n-1)/2)*0.22
        L(d, cx, cy, cx + s*1.5*math.cos(a), cy + s*math.sin(a), S2)

def star(d, cx, cy, s):
    pts = []
    for i in range(10):
        a = -math.pi/2 + i*math.pi/5
        r = s if i % 2 == 0 else s*0.42
        pts.append((cx + r*math.cos(a), cy + r*math.sin(a)))
    P(d, pts, S2-6)

def bubble(d, cx, cy, r):
    C(d, cx, cy, r, S2)

def wave(d, cx, cy, rx, a0=190, a1=350):
    A(d, cx, cy, rx, rx*0.20, a0, a1, S2)

def ground(d, y=2860):
    L(d, 300, y, 2250, y, S)

def rock(d, cx, cy, r):
    pts = []
    for i in range(14):
        a = 2*math.pi*i/14
        jitter = r * (0.78 if i % 2 else 1.0)
        pts.append((cx + jitter*math.cos(a), cy + r*0.62*math.sin(a) + (r*0.12 if a > math.pi else 0)))
    P(d, pts, S)

def sun(d, cx=2200, cy=380, r=150):
    C(d, cx, cy, r, S)
    for i in range(8):
        a = math.pi*2*i/8
        L(d, cx + (r+30)*math.cos(a), cy + (r+30)*math.sin(a),
           cx + (r+95)*math.cos(a), cy + (r+95)*math.sin(a), S2)

def cloud(d, cx, cy, s=180):
    C(d, cx, cy, s*0.55, S2)
    C(d, cx - s*0.62, cy + s*0.18, s*0.42, S2)
    C(d, cx + s*0.62, cy + s*0.18, s*0.42, S2)
    L(d, cx - s*1.0, cy + s*0.34, cx + s*1.1, cy + s*0.18, S2)

# ----------------_ARCHETYPES-----------------

def koala(d, cx, cy, s, nap=False, munch=False):
    ground(d)
    branch(d, 260, 640, 2270, 900)
    E(d, cx, cy+s*0.95, s*0.85, s*0.75)
    C(d, cx - s*0.75, cy - s*0.55, s*0.42)
    C(d, cx + s*0.75, cy - s*0.55, s*0.42)
    C(d, cx - s*0.75, cy - s*0.55, s*0.20, S2)
    C(d, cx + s*0.75, cy - s*0.55, s*0.20, S2)
    C(d, cx, cy, s*0.60)
    E(d, cx, cy + s*0.10, s*0.18, s*0.28)
    if nap:
        L(d, cx - s*0.45, cy - s*0.12, cx - s*0.2, cy - s*0.05, S2)
        L(d, cx + s*0.2, cy - s*0.05, cx + s*0.45, cy - s*0.12, S2)
    else:
        happy_face(d, cx, cy, s*0.9, 0.35)
    if munch:
        leaf(d, cx - s*1.6, cy + s*0.5, 170, math.pi/4)
    A(d, cx - s*0.85, cy + s*0.75, s*0.35, s*0.28, 200, 60, S2)
    A(d, cx + s*0.85, cy + s*0.75, s*0.35, s*0.28, 120, -20, S2)
    E(d, cx - s*0.45, cy + s*1.55, s*0.28, s*0.20)
    E(d, cx + s*0.30, cy + s*1.55, s*0.28, s*0.20)
    leaf(d, cx + s*1.7, cy - s*0.9, 120, math.pi)
    leaf(d, cx + s*1.95, cy - s*0.7, 100, math.pi)
    leaf(d, cx - s*1.7, cy - s*0.85, 115, 0.2)

def kangaroo(d, cx, cy, s, joey=False, small=False):
    ground(d)
    E(d, cx, cy + s*0.35, s*0.85, s*0.85)
    C(d, cx + s*0.55, cy - s*0.75, s*0.40)
    E(d, cx + s*0.35, cy - s*1.0, s*0.14, s*0.22)
    E(d, cx + s*0.75, cy - s*1.0, s*0.14, s*0.22)
    happy_face(d, cx + s*0.60, cy - s*0.78, s*0.30, 0.42)
    E(d, cx + s*0.72, cy - s*0.55, s*0.09, s*0.06, S2)
    A(d, cx - s*1.05, cy - s*0.6, s*1.15, s*0.55, 150, 395, S2)
    A(d, cx - s*0.2, cy + s*0.4, s*0.42, s*0.42, 60, 260, S2)
    L(d, cx - s*0.1, cy + 0*1, cx - s*0.55, cy - s*0.35, S)
    L(d, cx + s*0.5, cy + s*0.05, cx + s*0.15, cy - s*0.4, S)
    E(d, cx - s*0.45, cy + s*1.42, s*0.24, s*0.17)
    E(d, cx + s*0.42, cy + s*1.42, s*0.24, s*0.17)
    if joey:
        C(d, cx + s*0.05, cy + s*0.75, s*0.26)
        E(d, cx + s*0.28, cy + s*0.65, s*0.10, s*0.15)
        E(d, cx + s*0.44, cy + s*0.65, s*0.10, s*0.15)
        happy_face(d, cx + s*0.9*0.0 - s*0.005, cy + s*0.7, s*0.3, 0.30)
        star(d, cx - s*1.7, cy - s*1.3, 70)
    if small:
        grass(d, 420, 2850, 90); grass(d, 2120, 2850, 90)
    else:
        leaf(d, cx - s*1.9, cy - s*1.9, 150, math.pi/5)
        leaf(d, cx - s*2.2, cy - 1.4*1.05*s, 130, math.pi/2.4)

def wombat(d, cx, cy, s, burrow=False):
    ground(d)
    E(d, cx, cy + s*0.5, s*1.05, s*0.72)
    C(d, cx + s*0.55, cy - s*0.05, s*0.55)
    E(d, cx + s*0.28, cy - s*0.42, s*0.15, s*0.20)
    E(d, cx + s*0.80, cy - s*0.42, s*0.15, s*0.20)
    happy_face(d, cx + s*0.58, cy - s*0.05, s*0.42, 0.4)
    E(d, cx + s*0.70, cy + s*0.16, s*0.10, s*0.08, S2)
    A(d, cx - s*1.05, cy - s*0.15, s*0.5, s*0.4, 90, 270, S2)
    A(d, cx + s*0.05, cy - s*0.15, s*0.5, s*0.4, 270, 90, S2)
    A(d, cx - s*0.55, cy + s*0.9, s*0.30, s*0.22, 180, 350)
    A(d, cx + s*0.55, cy + s*0.9, s*0.30, s*0.22, 190, 360)
    if burrow:
        A(d, cx - s*1.9, cy - s*0.75, s*1.8, s*0.85, 180, 360, S)
        A(d, cx - s*1.55, cy - s*0.85, s*1.35, s*0.60, 185, 355, S2)
        grass(d, 350, 2850, 110); leaf(d, 2150, 750, 140, math.pi)
    else:
        grass(d, 420, 2840, 95); grass(d, 2140, 2840, 95)
        sun(d, 2150, 430, 145)

def platypus(d, cx, cy, s):
    for k in range(3):
        wave(d, cx, cy + s*(0.8 + k*0.55), s*(1.5 - k*0.1), 185, 355)
    P(d, [(cx - s*1.55, cy - s*0.12), (cx + s*0.55, cy + s*0.30),
          (cx + s*1.05, cy - s*0.02), (cx + s*0.95, cy - s*0.34),
          (cx + s*0.35, cy - s*0.40), (cx - s*0.85, cy - s*0.30)])
    arcB = (cx - s*1.05, cy - s*0.22, cx + s*0.15, cy + s*0.28)
    d.ellipse([cx - s*1.05, cy - s*0.22, cx + s*0.15, cy + s*0.30], outline=(0,0,0), width=S)
    P(d, [(cx + s*1.05, cy - s*0.10), (cx + s*2.05, cy - s*0.30),
          (cx + s*2.12, cy - s*0.02), (cx + s*2.05, cy + s*0.22),
          (cx + s*1.05, cy + s*0.12)])
    happy_face(d, cx + s*1.55, cy + s*0.02, s*0.22, 0.5)
    E(d, cx - s*0.42, cy + s*0.28, s*0.26, s*0.17)
    E(d, cx + s*0.42, cy + s*0.28, s*0.26, s*0.17)
    P(d, [(cx - s*1.2, cy + s*0.28), (cx - s*1.75, cy + s*0.75), (cx - s*1.5, cy + s*0.85), (cx - s*1.05, cy + s*0.45)])
    bubble(d, cx - s*1.9, cy - s*1.1, 70); bubble(d, cx - s*1.55, cy - s*1.5, 45)

def rodent(d, cx, cy, s, spotted=False, stripes=False, glider=False, big_ears=False, slim=False):
    ground(d)
    C(d, cx + s*0.62, cy - s*0.3, s*0.52)
    E(d, cx + s*0.20, cy - s*0.68, s*0.15, s*0.20)
    E(d, cx + s*0.75, cy - s*0.68, s*0.15, s*0.20)
    if big_ears:
        E(d, cx - s*0.10, cy - s*0.75, s*0.20, s*0.30)
        E(d, cx + s*0.85, cy - s*0.68, s*0.20, s*0.30)
    happy_face(d, cx + s*0.62, cy - s*0.28, s*0.38, 0.42)
    P(d, [(cx + s*0.78, cy - s*0.16), (cx + s*1.05, cy - s*0.10), (cx + s*1.05, cy - s*0.24)])
    E(d, cx - s*0.25, cy + s*0.3, s*0.85, s*0.52)
    A(d, cx - s*0.75, cy + s*0.15, s*0.30, s*0.30, 180, 300, S2)
    A(d, cx + s*0.30, cy + s*0.15, s*0.30, s*0.30, 300, 120, S2)
    if glider and False:
        pass
    E(d, cx - s*0.62, cy + s*1.28, s*0.20, s*0.15)
    E(d, cx + s*0.40, cy + s*1.28, s*0.20, s*0.15)
    A(d, cx - s*1.15, cy + s*0.35, s*0.55, s*0.18, 120, 420, S2)
    if spotted:
        for (ox, oy) in [(-0.55, 0.05), (-0.2, 0.35), (0.1, 0.18), (-0.35, -0.15), (0.05, -0.05)]:
            C(d, cx + s*ox, cy + s*oy, s*0.10, S2)
    if stripes:
        for k in range(3):
            A(d, cx - s*(0.1 + 0.35*k), cy + s*0.3, s*0.25, s*0.35, 200, 340, S2)
    grass(d, 430, 2850, 100); grass(d, 2100, 2850, 100)
    leaf(d, cx - s*2.0, cy - s*1.1, 140, math.pi/4)

def bird(d, cx, cy, s, kind="generic"):
    ground(d)
    E(d, cx, cy + s*0.25, s*0.85, s*0.70)
    C(d, cx + s*0.8, cy - s*0.55, s*0.42)
    happy_face(d, cx + s*0.85, cy - s*0.6, s*0.32, 0.42)
    if kind in ("kookaburra", "cockatoo", "galah", "lorikeet"):
        P(d, [(cx + s*0.62, cy - s*0.92), (cx + s*0.55, cy - s*1.35), (cx + s*0.75, cy - s*1.28)])
        P(d, [(cx + s*0.88, cy - s*0.92), (cx + s*1.0, cy - s*1.32), (cx + s*1.12, cy - s*1.2)])
    if kind == "magpie":
        P(d, [(cx + s*0.75, cy - s*1.0), (cx + s*0.95, cy - s*1.42), (cx + s*1.15, cy - s*1.28)])
        A(d, cx - s*0.85, cy + s*0.2, s*0.35, s*0.3, 180, 360, S2)
    if kind in ("cassowary",):
        P(d, [(cx + s*0.62, cy - s*1.02), (cx + s*0.72, cy - s*1.28), (cx + s*0.82, cy - s*1.02)], S)
    if kind == "eagle":
        A(d, cx + s*1.15, cy - s*0.35, s*0.22, s*0.18, -60, 120)
    P(d, [(cx + s*1.14, cy - s*0.62), (cx + s*1.55, cy - s*0.48), (cx + s*1.14, cy - s*0.38)])
    A(d, cx - s*0.95, cy - s*0.35, s*0.32, s*0.26, 190, 10, S2)
    L(d, cx - s*0.25, cy + s*0.95, cx - s*0.25, cy + s*1.45, S)
    L(d, cx + s*0.35, cy + s*0.95, cx + s*0.35, cy + s*1.45, S)
    for (fx, fy) in ((cx - s*0.4, cy + s*1.5), (cx + s*0.2, cy + s*1.5)):
        L(d, fx - s*0.14, fy, fx - s*0.28, fy + s*0.14, S2)
        L(d, fx, fy, fx, fy + s*0.16, S2)
        L(d, fx + s*0.14, fy, fx + s*0.28, fy + s*0.14, S2)
    if kind in ("brolga", "jabiru"):
        L(d, cx - s*0.35, cy + s*0.9, cx - s*0.35, cy + s*1.75, S)
        L(d, cx + s*0.3, cy + s*0.9, cx + s*0.3, cy + s*1.75, S)
        for fx in (cx - s*0.55, cx + s*0.1):
            L(d, fx, cy + s*1.78, fx - s*0.22, cy + s*1.86, S2)
            L(d, fx, cy + s*1.78, fx + s*0.30, cy + s*1.86, S2)
    grass(d, 420, 2850, 95); grass(d, 2110, 2850, 95)
    if kind not in ("brolga", "jabiru"):
        sun(d, 2160, 400, 130)

def echidna(d, cx, cy, s, ants=False):
    ground(d)
    A(d, cx - 20, cy + s*0.45, s*1.0, s*0.72, 175, 368, S)
    C(d, cx + s*0.75, cy + s*0.3, s*0.40)
    happy_face(d, cx + s*0.8, cy + s*0.3, s*0.28, 0.42)
    P(d, [(cx + s*1.18, cy + s*0.18), (cx + s*1.42, cy + s*0.22), (cx + s*1.2, cy + s*0.34)])
    for k in range(9):
        x = cx - s*0.85 + k*s*0.22
        P(d, [(x, cy - s*0.05), (x + 40, cy - s*0.55), (x + 85, cy - s*0.02)], S2)
    for k in range(5):
        x = cx - s*0.6 + k*s*0.22
        P(d, [(x, cy - s*0.25), (x + 36, cy - s*0.72), (x + 76, cy - s*0.22)], S2)
    if ants:
        for (ax, ay) in [(cx - s*1.8, cy + s*1.05), (cx - s*1.35, cy + s*0.9), (cx - s*0.9, cy + s*1.02), (cx - s*0.95, cy + s*0.75)]:
            C(d, ax, ay, 16, 12)
            L(d, ax + 12, ay, ax + 34, ay, 12)
            C(d, ax + 20, ay - 14, 10, 10)
    grass(d, 500, 2850, 90); leaf(d, 2100, 720, 150, math.pi)

def dog(d, cx, cy, s, chunky=False):
    ground(d)
    bh = s*0.62 if chunky else s*0.55
    E(d, cx + s*0.55, cy - s*0.15, bh, s*0.5)
    C(d, cx - s*0.65, cy - s*0.35, s*0.52)
    happy_face(d, cx - s*0.35, cy - s*0.4, s*0.34, 0.5)
    E(d, cx - s*0.45, cy + s*0.02, s*0.10, s*0.07, S2)
    if chunky:
        C(d, cx - s*0.75, cy - s*0.92, s*0.18)
        C(d, cx + s*0.05, cy - s*0.92, s*0.18)
    else:
        P(d, [(cx - s*0.62, cy - s*0.72), (cx - s*0.55, cy - s*1.15), (cx - s*0.28, cy - s*0.80)])
        P(d, [(cx + s*0.05, cy - s*0.75), (cx + s*0.3, cy - s*1.12), (cx + s*0.35, cy - s*0.72)])
    P(d, [(cx - s*0.2, cy - s*0.36), (cx + s*0.06, cy - s*0.30), (cx - s*0.2, cy - s*0.22)])
    E(d, cx + s*1.05, cy, s*0.48, s*0.42)
    A(d, cx + s*0.35, cy + s*0.75, s*(0.75 if chunky else 0.55), s*0.35, 30, 150, S2)
    A(d, cx + s*0.35, cy + s*0.75, s*(0.75 if chunky else 0.55), s*0.35, 210, 330, S2)
    A(d, cx - s*0.35, cy - s*0.95, s*0.35, s*0.35, 260, 60, S2)
    star(d, 2150, 500, 130); star(d, 380, 900, 110)
    grass(d, 460, 2850, 95); grass(d, 2080, 2850, 95)

def lizard(d, cx, cy, s, frill=False, tongue=False, stripes=False):
    ground(d)
    A(d, cx, cy + s*0.15, s*1.15, s*0.40, 180, 360, S)
    A(d, cx, cy + s*0.15, s*1.15, s*0.40, 0, 180, S)
    A(d, cx + s*1.15, cy + s*0.15, s*0.65, s*0.28, 240, 480, S2)
    C(d, cx + s*1.55, cy + s*0.05, s*0.30)
    happy_face(d, cx + s*1.6, cy + s*0.02, s*0.28, 0.45)
    if frill:
        for k in range(9):
            a = math.pi - k*math.pi/8
            x1 = cx - s*0.35 + (k-4)*s*0.09
            P(d, [(cx - s*1.15 + k*s*0.28, cy + s*0.15),
                  (cx - s*1.0 + k*s*0.28 + 30, cy - s*0.75),
                  (cx - s*1.35 + k*s*0.28 + 55, cy + s*0.15)], S2)
    if tongue:
        L(d, cx + s*1.85, cy + s*0.15, cx + s*1.95, cy + s*0.42, S2)
        C(d, cx + s*1.93, cy + s*0.48, s*0.07, 10)
    if stripes:
        for k in range(4):
            L(d, cx - s*(0.7 - k*0.35), cy - s*0.2, cx - s*(0.7 - k*0.35), cy + s*0.55, S2)
    L(d, cx - s*0.75, cy + s*0.5, cx - s*0.85, cy + s*0.95, S)
    L(d, cx - s*0.15, cy + s*0.5, cx + s*0.05, cy + s*0.95, S)
    L(d, cx + s*0.55, cy + s*0.5, cx + s*0.65, cy + s*0.95, S)
    L(d, cx + s*1.05, cy + s*0.4, cx + s*1.15, cy + s*0.9, S)
    rock(d, 480, 2820, 130); rock(d, 2000, 2810, 110)
    grass(d, 700, 2840, 90); grass(d, 1750, 2840, 85)

def camel(d, cx, cy, s):
    ground(d)
    E(d, cx, cy + s*0.35, s*0.95, s*0.60)
    A(d, cx - s*0.75, cy - s*0.1, s*0.48, s*0.42, 180, 360, S)
    A(d, cx + s*0.12, cy - s*0.1, s*0.48, s*0.42, 180, 360, S)
    A(d, cx - s*1.05, cy - s*0.35, s*0.35, s*0.55, 235, 385, S)
    C(d, cx - s*1.28, cy - s*1.05, s*0.32)
    happy_face(d, cx - s*1.3, cy - s*1.1, s*0.30, 0.45)
    P(d, [(cx - s*1.05, cy - s*1.2), (cx - s*1.28, cy - s*1.3), (cx - s*1.52, cy - s*1.18)])
    L(d, cx - s*0.5, cy + s*0.9, cx - s*0.5, cy + s*1.4, S)
    L(d, cx + s*0.45, cy + s*0.9, cx + s*0.45, cy + s*1.4, S)
    E(d, cx - s*0.62, cy + s*1.42, s*0.22, s*0.15)
    E(d, cx + s*0.33, cy + s*1.42, s*0.22, s*0.15)
    sun(d, 2120, 500, 150); star(d, 400, 850, 110)
    grass(d, 500, 2850, 90); grass(d, 1950, 2840, 80)

def turtle(d, cx, cy, s):
    for k in range(3):
        wave(d, cx, cy + s*0.95 + k*s*0.55, s*1.45 - k*0.5*s, 180, 360)
    d.ellipse([cx - s*1.0, cy - s*0.75, cx + s*1.0, cy + s*0.55], outline=(0,0,0), width=S)
    A(d, cx - s*0.5, cy - s*0.75, s*0.5, s*0.55, 180, 360)
    C(d, cx, cy - s*0.1, s*0.28)
    for k, a in ((0, 200), (1, 250), (2, 300), (3, 340)):
        x = cx + (k-1.5)*s*0.5; y = cy - s*0.18
        C(d, x, y, s*0.16, S2)
    C(d, cx + s*1.12, cy - s*0.15, s*0.30)
    happy_face(d, cx + s*1.15, cy - s*0.18, s*0.24, 0.45)
    P(d, [(cx + s*1.3, cy + s*0.05), (cx + s*1.55, cy + s*0.2), (cx + s*1.3, cy + s*0.28)])
    P(d, [(cx - s*1.0, cy - s*0.25), (cx - s*1.5, cy - s*0.65), (cx - s*1.55, cy - s*0.25), (cx - s*1.25, cy - s*0.08)])
    P(d, [(cx + s*0.35, cy + s*0.52), (cx + s*0.75, cy + s*0.92), (cx + s*0.35, cy + s*0.9)])
    E(d, cx - s*0.85, cy + s*0.75, s*0.5, s*0.28)
    bubble(d, cx - s*1.7, cy - s*1.3, 60); bubble(d, cx - s*1.2, cy - s*1.7, 40)

def dugong(d, cx, cy, s):
    for k in range(3):
        wave(d, cx, cy + s*(0.9 + k*0.6), s*1.7 - k*s*0.45, 180, 360)
    E(d, cx, cy, s*1.1, s*0.62)
    A(d, cx + s*0.55, cy + s*0.15, s*0.42, s*0.30, 300, 100, S2)
    C(d, cx + s*1.02, cy - s*0.3, s*0.30)
    happy_face(d, cx + s*1.06, cy - s*0.32, s*0.26, 0.45)
    E(d, cx + s*1.18, cy - s*0.16, s*0.09, s*0.07, S2)
    P(d, [(cx + s*0.55, cy - s*0.6), (cx + s*0.95, cy - s*1.05), (cx + s*0.15, cy - s*0.72)], S2)
    P(d, [(cx - s*1.06, cy - s*0.15), (cx - s*1.6, cy - s*0.5), (cx - s*1.6, cy - s*0.05), (cx - s*1.18, cy + s*0.25)])
    bubble(d, cx - s*1.8, cy - s*1.35, 70); bubble(d, cx - s*1.35, cy - s*1.8, 45); bubble(d, cx - s*0.95, cy - s*1.55, 30)

def dolphin(d, cx, cy, s):
    for k in range(2):
        wave(d, cx, cy + s*1.1 + k*s*0.6, s*1.6, 180, 360)
    A(d, cx, cy + s*0.2, s*1.05, s*0.55, 180, 360, S)
    A(d, cx, cy - s*0.2, s*0.85, s*0.45, 0, 180, S)
    C(d, cx + s*0.95, cy - s*0.35, s*0.28)
    eyes(d, cx + s*0.98, cy - s*0.32, s*0.22, 0.0, 0.15)
    smile(d, cx + s*1.02, cy - s*0.18, s*0.25, 200, 340)
    P(d, [(cx + s*0.15, cy - s*0.62), (cx + s*0.55, cy - s*1.15), (cx + s*0.75, cy - s*0.5)])
    A(d, cx - s*0.35, cy + s*0.15, s*0.35, s*0.5, 300, 80, S2)
    A(d, cx - s*0.35, cy + s*0.15, s*(0.35 if True else 0.35), s*0.5, 60, 170, S2)
    bubble(d, cx + s*1.45, cy - s*0.9, 55); bubble(d, cx + s*1.8, cy - s*1.25, 35)
    star(d, 420, 700, 110)

def penguin(d, cx, cy, s):
    rock(d, cx, 2830, 260)
    E(d, cx, cy + s*0.1, s*0.72, s*0.95)
    C(d, cx, cy + s*0.42, s*0.46, S2)
    happy_face(d, cx, cy - s*0.05, s*0.6, 0.5)
    P(d, [(cx + s*0.62, cy - s*0.35), (cx + s*0.95, cy - s*0.18), (cx + s*0.62, cy - s*0.05)])
    A(d, cx - s*0.72, cy - s*0.1, s*0.30, s*0.55, 180, 90, S2)
    A(d, cx + s*0.05, cy - s*0.1, s*0.30, s*0.55, 60, 170, S2)
    for fx in (cx - s*0.35, cx + s*0.15):
        P(d, [(fx, cy + s*1.02), (fx - s*0.2, cy + s*1.1), (fx + s*0.12, cy + s*1.1)])
    bubble(d, cx - s*1.8, cy - s*0.9, 60)
    star(d, 2130, 480, 120)

def seahorse(d, cx, cy, s):
    A(d, cx, cy - s*0.2, s*0.55, s*0.42, 270, 330, S)
    A(d, cx, cy + s*0.35, s*0.42, s*0.55, 200, 330, S)
    A(d, cx, cy + s*0.35, s*0.42, s*0.55, 150, 200, S)
    A(d, cx - s*0.1, cy + s*0.9, s*0.35, s*0.42, 320, 140, S)
    A(d, cx - s*0.35, cy - s*0.5, s*0.32, s*0.26, 150, 210, S2)
    E(d, cx - s*0.05, cy - s*0.95, s*0.13, s*0.09, S2)
    happy_face(d, cx + s*0.1, cy - s*0.75, s*0.30, 0.35)
    for k, a0 in ((1, 95), (2, 120), (3, 145)):
        L(d, cx - s*0.12 + k*s*0.16, cy - s*0.62, cx + k*s*0.20, cy - s*1.35, S2)
    C(d, cx - s*0.2, cy - s*0.02, s*0.14, S2)
    leaf(d, 400, 2650, 150, math.pi/2); leaf(d, 2130, 2520, 170, math.pi/1.6)
    bubble(d, cx - s*1.7, cy - s*1.5, 60); bubble(d, cx - s*1.25, cy - s*1.95, 42)

def fish(d, cx, cy, s, clown=False):
    for k in range(2):
        wave(d, cx, cy + s*1.35 + k*s*0.55, s*1.5, 180, 360)
    E(d, cx, cy, s*0.95, s*0.62)
    C(d, cx + s*0.72, cy - s*0.05, s*0.30)
    eyes(d, cx + s*0.72, cy - s*0.12, s*0.24, 0.0, 0.16)
    smile(d, cx + s*0.78, cy + s*0.05, s*0.26, 190, 350)
    P(d, [(cx - s*0.92, cy - s*0.1), (cx - s*1.55, cy - s*0.45), (cx - s*1.55, cy + s*0.35), (cx - s*0.92, cy + s*0.12)])
    P(d, [(cx - s*0.1, cy - s*0.55), (cx + s*0.2, cy - s*1.15), (cx + s*0.4, cy - s*0.6)])
    P(d, [(cx - s*0.02, cy + s*0.5), (cx + s*0.25, cy + s*1.05), (cx + s*0.45, cy + s*0.42)])
    if clown:
        A(d, cx + s*0.3, cy - s*0.1, s*0.62, s*0.62, 245, 295, S2)
        A(d, cx - s*0.25, cy - s*0.1, s*0.62, s*0.6, 245, 295, S2)
    bubble(d, cx + s*1.35, cy - s*0.85, 55); bubble(d, cx + s*1.7, cy - s*1.3, 38)
    leaf(d, 390, 2600, 160, math.pi/2)

def jelly(d, cx, cy, s):
    A(d, cx, cy, s*0.95, s*0.78, 180, 360, S)
    C(d, cx, cy - s*0.35, s*0.35, S2)
    happy_face(d, cx, cy - s*0.45, s*0.42, 0.4)
    for k in range(5):
        x = cx - s*0.72 + k*s*0.36
        A(d, x, cy + s*0.05, s*0.16, s*0.72, 20, 160, S2)
        A(d, x, cy + s*0.75, s*0.16, s*0.45, 200, 340, S2)
    bubble(d, cx - s*1.65, cy - s*0.55, 58); bubble(d, cx + s*1.6, cy - s*0.95, 72)
    bubble(d, cx + s*1.25, cy - s*1.6, 40); bubble(d, cx - s*1.3, cy - s*1.25, 34)

def octo(d, cx, cy, s):
    A(d, cx, cy + s*0.1, s*0.8, s*0.7, 180, 360, S)
    L(d, cx - s*0.8, cy + s*0.05, cx - s*0.8, cy + s*0.15, S)
    L(d, cx + s*0.8, cy + s*0.05, cx + s*0.8, cy + s*0.15, S)
    happy_face(d, cx, cy + s*0.05, s*0.55, 0.45)
    for k in range(6):
        x = cx - s*0.68 + k*s*0.27
        dirn = 1 if k % 2 == 0 else -1
        A(d, x + dirn*s*0.06, cy + s*0.85, s*0.14, s*0.55, 330, 150, S2)
        C(d, x, cy + s*1.48, s*0.09, S2)
    bubble(d, cx - s*1.5, cy - s*0.7, 52); bubble(d, cx + s*1.4, cy - s*1.05, 66)

def hermit(d, cx, cy, s):
    rock(d, cx, 2830, s*1.1)
    A(d, cx, cy + s*0.2, s*0.85, s*0.7, 150, 390, S)
    A(d, cx + s*0.28, cy + s*0.28, s*0.28, s*0.42, 40, 320, S2)
    for k in range(4):
        L(d, cx - s*0.1 + k*s*0.3, cy + s*0.05, cx - s*0.16 + k*s*0.3, cy - s*0.6, S2)
    C(d, cx - s*0.98, cy + s*0.08, s*0.30)
    happy_face(d, cx - s*0.32, cy + s*0.05, s*0.30, 0.4)
    P(d, [(cx + s*0.68, cy + s*0.15), (cx + s*1.15, cy - s*0.12), (cx + s*0.95, cy + s*0.35)], S2)
    bubble(d, cx - s*1.9, cy - s*1.1, 50)

def whale(d, cx, cy, s):
    for k in range(2):
        wave(d, cx, cy + s*1.15 + k*s*0.6, s*1.75, 180, 360)
    E(d, cx, cy + s*0.1, s*1.15, s*0.62)
    C(d, cx - s*0.72, cy - s*0.42, s*0.34)
    happy_face(d, cx - s*0.78, cy - s*0.4, s*0.3, 0.45)
    P(d, [(cx + s*0.9, cy - s*0.5), (cx + s*1.6, cy - s*1.0), (cx + s*1.42, cy - s*0.28), (cx + s*1.05, cy - s*0.12)])
    A(d, cx - s*0.05, cy + s*0.2, s*0.4, s*0.45, 280, 100, S2)
    for (bx, by, br) in ((cx - s*0.55, cy - s*0.95, 40), (cx - s*0.25, cy - s*1.22, 52), (cx + s*0.05, cy - s*0.95, 44)):
        C(d, bx, by, br, S2)
    bubble(d, cx + s*1.75, cy + s*0.5, 55)

def frog(d, cx, cy, s):
    E(d, cx, cy + s*0.95, s*1.5, s*0.42)
    L(d, cx - s*1.42, cy + s*0.6, cx + s*1.42, cy + s*0.7, S2)
    E(d, cx, cy + s*0.35, s*0.85, s*0.55)
    C(d, cx - s*0.42, cy - s*0.08, s*0.26)
    C(d, cx + s*0.55, cy - s*0.08, s*0.26)
    eyes(d, cx, cy - s*0.02, s*0.5, spread=0.28, sm=0.10)
    A(d, cx, cy + s*0.35, s*0.5, s*0.28, 25, 155, S2)
    A(d, cx - s*0.65, cy + s*0.5, s*0.32, s*0.25, 180, 340)
    A(d, cx + s*0.7, cy + s*0.5, s*0.32, s*0.25, 200, 360)
    bubble(d, cx - s*1.6, cy - s*1.05, 55); bubble(d, cx + s*1.35, cy - s*0.75, 45)

def butterfly(d, cx, cy, s):
    ground(d)
    E(d, cx - s*0.85, cy - s*0.35, s*0.62, s*0.78, S2)
    E(d, cx + s*0.85, cy - s*0.35, s*0.62, s*0.78, S2)
    E(d, cx - s*0.62, cy + s*0.55, s*0.44, s*0.54, S2)
    E(d, cx + s*0.62, cy + s*0.55, s*0.44, s*0.54, S2)
    E(d, cx, cy, s*0.14, s*0.85)
    C(d, cx, cy - s*0.22, s*0.13, S2)
    L(d, cx - s*0.06, cy - s*0.34, cx - s*0.35, cy - s*0.95, S2)
    L(d, cx + s*0.06, cy - s*0.34, cx + s*0.35, cy - s*0.95, S2)
    C(d, cx - s*0.36, cy - s*0.98, s*0.08, 12)
    C(d, cx + s*0.36, cy - s*0.98, s*0.08, 12)
    C(d, cx - s*0.85, cy - s*0.35, s*0.22, S2)
    C(d, cx + s*0.85, cy - s*0.35, s*0.22, S2)
    A(d, cx, cy + s*0.55, s*0.44, s*0.54, 200, 340, S2)
    leaf(d, cx + s*1.9, cy + s*1.15, 150, math.pi/3)
    star(d, 450, 800, 105)

# ----------------PAGE PLANS-----------------
PAGES = [
    ("koala nap", lambda d, s: (sun(d, 2150, 430, 130), koala(d, 1175, 1500, s, nap=True))),
    ("koala munch", lambda d, s: koala(d, 1275, 1580, s, munch=True)),
    ("kangaroo", lambda d, s: kangaroo(d, 1275, 1560, s)),
    ("kangaroo joey", lambda d, s: kangaroo(d, 1275, 1560, s, joey=True)),
    ("wallaby", lambda d, s: kangaroo(d, 1275, 1620, s*0.85, small=True)),
    ("wombat", lambda d, s: wombat(d, 1275, 1600, s)),
    ("wombat burrow", lambda d, s: wombat(d, 1450, 1550, s, burrow=True)),
    ("platypus", lambda d, s: platypus(d, 1150, 1500, s)),
    ("quokka", lambda d, s: rodent(d, 1240, 1600, s)),
    ("quokka closeup", lambda d, s: rodent(d, 1275, 1450, s*1.25)),
    ("emu", lambda d, s: bird(d, 1275, 1560, s, kind="emu")),
    ("kookaburra", lambda d, s: bird(d, 1240, 1520, s, kind="kookaburra")),
    ("galah", lambda d, s: bird(d, 1240, 1560, s, kind="galah")),
    ("cockatoo", lambda d, s: bird(d, 1240, 1560, s, kind="cockatoo")),
    ("magpie", lambda d, s: bird(d, 1240, 1540, s, kind="magpie")),
    ("lorikeet", lambda d, s: bird(d, 1240, 1560, s, kind="lorikeet")),
    ("cassowary", lambda d, s: bird(d, 1275, 1560, s, kind="cassowary")),
    ("brolga", lambda d, s: bird(d, 1240, 1440, s, kind="brolga")),
    ("jabiru", lambda d, s: bird(d, 1240, 1440, s, kind="jabiru")),
    ("eagle", lambda d, s: bird(d, 1240, 1500, s, kind="eagle")),
    ("pelican", lambda d, s: bird(d, 1240, 1500, s, kind="pelican")),
    ("echidna", lambda d, s: echidna(d, 1250, 1650, s)),
    ("echidna ants", lambda d, s: echidna(d, 1275, 1620, s, ants=True)),
    ("dingo", lambda d, s: dog(d, 1275, 1560, s)),
    ("tasmanian devil", lambda d, s: dog(d, 1240, 1600, s, chunky=True)),
    ("frill lizard", lambda d, s: lizard(d, 1150, 1600, s, frill=True)),
    ("blue tongue", lambda d, s: lizard(d, 1150, 1600, s, tongue=True)),
    ("goanna", lambda d, s: lizard(d, 1150, 1600, s, stripes=True)),
    ("bilby", lambda d, s: rodent(d, 1240, 1580, s, big_ears=True)),
    ("numbat", lambda d, s: rodent(d, 1240, 1600, s, stripes=True)),
    ("quoll", lambda d, s: rodent(d, 1240, 1600, s, spotted=True)),
    ("hopping mouse", lambda d, s: rodent(d, 1240, 1640, s*0.8, big_ears=True)),
    ("bandicoot", lambda d, s: rodent(d, 1240, 1580, s*0.92)),
    ("bettong", lambda d, s: rodent(d, 1240, 1600, s*0.95)),
    ("potoroo", lambda d, s: rodent(d, 1240, 1620, s*0.9)),
    ("possum", lambda d, s: rodent(d, 1240, 1560, s, big_ears=True)),
    ("sugar glider", lambda d, s: rodent(d, 1240, 1560, s, big_ears=True)),
    ("camel", lambda d, s: camel(d, 1275, 1560, s)),
    ("turtle", lambda d, s: turtle(d, 1200, 1450, s)),
    ("dugong", lambda d, s: dugong(d, 1150, 1450, s)),
    ("dolphin", lambda d, s: dolphin(d, 1150, 1400, s)),
    ("little penguin", lambda d, s: penguin(d, 1240, 1500, s)),
    ("seahorse", lambda d, s: seahorse(d, 1300, 1500, s)),
    ("clownfish", lambda d, s: fish(d, 1150, 1450, s, clown=True)),
    ("jellyfish", lambda d, s: jelly(d, 1275, 1450, s)),
    ("octopus", lambda d, s: octo(d, 1275, 1350, s)),
    ("hermit crab", lambda d, s: hermit(d, 1275, 1500, s)),
    ("whale", lambda d, s: whale(d, 1120, 1400, s)),
    ("frog", lambda d, s: frog(d, 1240, 1400, s)),
    ("butterfly", lambda d, s: butterfly(d, 1240, 1500, s)),
]

def main():
    for i, (name, fn) in enumerate(PAGES, 1):
        img, d = canvas()
        fn(d, 260)
        # seeded simple variation: 2 extra grass/leaf accents pseudo-random per page
        seed = i * 7919
        if seed % 3 == 0:
            grass(d, 2600 - (seed % 700) - 300, 2860, 70, 4)
        if seed % 4 == 1:
            leaf(d, 300 + (seed % 500), 650 + (seed % 400), 110, (seed % 6) * math.pi / 6)
        if seed % 5 == 2:
            star(d, (seed % 1800) + 350, 560 + (seed % 300), 100)
        img = img.rotate(180 if seed % 11 == 0 else 0)
        path = os.path.join(OUT, "page_%02d.png" % i)
        img.save(path, dpi=(300, 300))
        print("saved", path, name)
    print("total pages:", len(PAGES))

    # contact sheet 5x10
    tw, th = 255, 330
    sheet = Image.new("RGB", (tw*5, th*10), "white")
    for i, (name, fn) in enumerate(PAGES):
        p = Image.open(os.path.join(OUT, "page_%02d.png" % (i+1))).resize((tw, th))
        sheet.paste(p, ((i % 5)*tw, (i//5)*th))
    sheet.save(os.path.join(ROOT, "contact_sheet.png"))
    print("contact sheet saved")

if __name__ == "__main__":
    main()

