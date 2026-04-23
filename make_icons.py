"""Generate PNG icons using only Python stdlib.

Produces a gradient square with a rounded-corner mask and a centered 'P' glyph.
Outputs:
  icon-192.png
  icon-512.png
  icon-maskable-512.png  (no rounded corners — safe-zone padded)
  apple-touch-icon.png   (180x180, no rounded corners — iOS adds its own mask)
"""
import struct
import zlib
import os
from pathlib import Path

OUT = Path(__file__).parent

# Accent gradient: blue -> purple (matches CSS --accent)
TOP = (59, 130, 246)     # #3b82f6
BOT = (139, 92, 246)     # #8b5cf6
WHITE = (255, 255, 255)

# A super-simple 7x9 pixel font for the letter "P". 1 = ink, 0 = empty.
GLYPH_P = [
    "1111100",
    "1000010",
    "1000010",
    "1000010",
    "1111100",
    "1000000",
    "1000000",
    "1000000",
    "1000000",
]

def lerp(a, b, t):
    return int(a + (b - a) * t)

def gradient(x, y, size):
    t = y / max(1, size - 1)
    return (lerp(TOP[0], BOT[0], t), lerp(TOP[1], BOT[1], t), lerp(TOP[2], BOT[2], t))

def in_rounded_square(x, y, size, radius):
    if x < radius and y < radius:
        dx, dy = radius - x, radius - y
        return dx * dx + dy * dy <= radius * radius
    if x >= size - radius and y < radius:
        dx, dy = x - (size - radius - 1), radius - y
        return dx * dx + dy * dy <= radius * radius
    if x < radius and y >= size - radius:
        dx, dy = radius - x, y - (size - radius - 1)
        return dx * dx + dy * dy <= radius * radius
    if x >= size - radius and y >= size - radius:
        dx, dy = x - (size - radius - 1), y - (size - radius - 1)
        return dx * dx + dy * dy <= radius * radius
    return True

def glyph_pixel(x, y, size, safe=0.6):
    # Center a scaled 7x9 glyph in a box that's `safe` of the icon size.
    gw, gh = 7, 9
    box = int(size * safe)
    scale = min(box // gw, box // gh)
    glyph_w = gw * scale
    glyph_h = gh * scale
    ox = (size - glyph_w) // 2
    oy = (size - glyph_h) // 2
    gx = (x - ox) // scale
    gy = (y - oy) // scale
    if 0 <= gx < gw and 0 <= gy < gh:
        return GLYPH_P[gy][gx] == "1"
    return False

def make_png(path, size, *, rounded=True, safe_pad=0.0):
    radius = int(size * 0.22) if rounded else 0
    # If maskable, shrink content area by safe_pad (e.g. 0.1 = 10% inset all sides)
    inset = int(size * safe_pad)
    raw = bytearray()
    for y in range(size):
        raw.append(0)  # PNG filter: None
        for x in range(size):
            if rounded and not in_rounded_square(x, y, size, radius):
                raw += bytes([0, 0, 0, 0])  # transparent outside rounded mask
                continue
            # Gradient background
            r, g, b = gradient(x, y, size)
            # Glyph overlay (only within safe inset)
            gx = x - inset
            gy = y - inset
            gsize = size - 2 * inset
            if 0 <= gx < gsize and 0 <= gy < gsize and glyph_pixel(gx, gy, gsize):
                r, g, b = WHITE
            raw += bytes([r, g, b, 255])

    def chunk(ctype, data):
        return (
            struct.pack(">I", len(data))
            + ctype
            + data
            + struct.pack(">I", zlib.crc32(ctype + data) & 0xFFFFFFFF)
        )

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)  # 8-bit RGBA
    idat = zlib.compress(bytes(raw), 9)
    with open(path, "wb") as f:
        f.write(sig)
        f.write(chunk(b"IHDR", ihdr))
        f.write(chunk(b"IDAT", idat))
        f.write(chunk(b"IEND", b""))

make_png(OUT / "icon-192.png", 192, rounded=True)
make_png(OUT / "icon-512.png", 512, rounded=True)
make_png(OUT / "icon-maskable-512.png", 512, rounded=False, safe_pad=0.1)
make_png(OUT / "apple-touch-icon.png", 180, rounded=False)

print("Generated:", *sorted(p.name for p in OUT.glob("*.png")))
