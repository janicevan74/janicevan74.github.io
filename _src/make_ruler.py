#!/usr/bin/env python3
"""Printable miniature scale ruler (Letter + A4, landscape).

Every ruler is 9 in of paper. Tick positions are computed from the scale
ratio only, so 1 real foot at 1:12 is exactly 1 in (72 pt) on paper.
Run from the repo root:  python3 _src/make_ruler.py
"""
import os
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "downloads"); os.makedirs(OUT, exist_ok=True)
IN = 72.0; MM = 72 / 25.4
L = 9 * IN            # ruler length on paper
PAD = 0.25 * IN       # space before 0 and after the end
STRIP_H = 0.78 * IN
BERRY = HexColor("#7a2840"); INK = HexColor("#2a1a1f"); SOFT = HexColor("#6f5a60"); BLUSH = HexColor("#f6e8e8")

# (title, subtitle, unit length on paper (pt) of ONE real unit, minor step, mid step, major step, label every, unit text, max)
#   steps are in real units (feet or metres)
RULERS = [
    ("1:6", "Playscale · Escala de muñecas · 2 in = 1 ft", 2 * IN, 1/12, 0.5, 1, 1, "ft", 4.5),
    ("1:12", "One-inch scale · Escala de una pulgada · 1 in = 1 ft", 1 * IN, 1/12, 0.5, 1, 1, "ft", 9),
    ("1:24", "Half scale · Media escala · ½ in = 1 ft", 0.5 * IN, 0.25, 0.5, 1, 1, "ft", 18),
    ("1:48", "Quarter scale · Escala de un cuarto · ¼ in = 1 ft", 0.25 * IN, 1, 5, 5, 5, "ft", 36),
    ("1:12", "Metric · Métrico · 1 real m = 83.3 mm", 1000 / 12 * MM, 0.1, 0.5, 1, 1, "m", 2.7),
    ("1:24", "Metric · Métrico · 1 real m = 41.7 mm", 1000 / 24 * MM, 0.1, 0.5, 1, 1, "m", 5.4),
]

def near(a, b): return abs(a - b) < 1e-6
def is_mult(x, step): return near(round(x / step) * step, x)

def strip(c, x, y, r):
    title, sub, unit, minor, mid, major, every, utext, vmax = r
    w = L + 2 * PAD
    c.setFillColor(BLUSH); c.rect(x, y, w, STRIP_H, stroke=0, fill=1)
    c.setDash(3, 2); c.setStrokeColor(SOFT); c.setLineWidth(0.5); c.rect(x, y, w, STRIP_H, stroke=1, fill=0); c.setDash()
    c.setFillColor(BERRY); c.setFont("Helvetica-Bold", 13); c.drawString(x + 6, y + STRIP_H - 15, title)
    c.setFillColor(SOFT); c.setFont("Helvetica", 7.5); c.drawString(x + 40, y + STRIP_H - 13.5, sub)
    x0 = x + PAD; base = y + 4
    c.setStrokeColor(INK); c.setLineWidth(0.6); c.line(x0, base, x0 + vmax * unit, base)
    n = int(round(vmax / minor))
    ticks = []
    for i in range(n + 1):
        v = i * minor
        px = x0 + v * unit
        if is_mult(v, major): h, lw = 17, 0.8
        elif is_mult(v, mid): h, lw = 11, 0.6
        else: h, lw = 6, 0.4
        c.setLineWidth(lw); c.line(px, base, px, base + h)
        if is_mult(v, every):
            lab = f"{int(round(v))}"
            c.setFont("Helvetica-Bold" if v else "Helvetica", 7.5); c.setFillColor(INK)
            c.drawCentredString(px, base + h + 2.5, lab)
        ticks.append((v, px - x0))
    c.setFont("Helvetica", 7); c.setFillColor(SOFT)
    c.drawRightString(x + w - 6, y + STRIP_H - 13.5, "real " + ("feet · pies" if utext == "ft" else "metres · metros"))
    return ticks

def build(pagesize, tag):
    pw, ph = landscape(pagesize)
    path = os.path.join(OUT, f"MiniatureNestStudio_Scale_Ruler_{tag}.pdf")
    c = canvas.Canvas(path, pagesize=(pw, ph))
    c.setTitle("Miniature Scale Ruler · Regla de escala — MiniatureNestStudio")
    c.setAuthor("MiniatureNestStudio")
    w = L + 2 * PAD; x = (pw - w) / 2
    top = ph - 0.45 * IN
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 17); c.drawString(x, top - 12, "Miniature Scale Ruler · Regla de escala")
    c.setFont("Helvetica", 8.5); c.setFillColor(SOFT)
    c.drawString(x, top - 27, "Print at 100% / Actual size.  Imprime al 100% / Tamaño real.")
    c.drawString(x, top - 39, "Cut out each ruler and glue it to cardstock. Line up 0 with the edge of a piece: the number is its real-life size.")
    c.drawString(x, top - 51, "Recorta cada regla y pégala en cartulina. Pon el 0 en el borde de la pieza: el número es su tamaño en la vida real.")
    # print checks: 1 in square and 2 cm square
    sq_y = top - 58
    c.setStrokeColor(BERRY); c.setLineWidth(0.8)
    c.rect(x + w - IN - 20 * MM - 14, sq_y, IN, IN)
    c.rect(x + w - 20 * MM, sq_y, 20 * MM, 20 * MM)
    c.setFont("Helvetica", 7); c.setFillColor(BERRY)
    c.drawCentredString(x + w - IN / 2 - 20 * MM - 14, sq_y - 9, "1 in")
    c.drawCentredString(x + w - 10 * MM, sq_y - 9, "2 cm")
    y = sq_y - 22 - STRIP_H
    all_ticks = {}
    for r in RULERS:
        all_ticks[r[0] + r[7]] = strip(c, x, y, r)
        y -= STRIP_H + 0.1 * IN
    c.setFont("Helvetica", 7.5); c.setFillColor(SOFT)
    c.drawString(x, 0.35 * IN, "Free for personal use · Gratis para uso personal  ·  © MiniatureNestStudio  ·  miniatureneststudio.com")
    c.showPage(); c.save()
    assert y > 0.45 * IN, ("page overflow", tag, y)
    return path, all_ticks, (x + w - IN - 20 * MM - 14, sq_y)

if __name__ == "__main__":
    for ps, tag in [(letter, "Letter"), (A4, "A4")]:
        p, ticks, _ = build(ps, tag)
        print(p)
    # small preview image for the website page
    import subprocess
    prev = os.path.join(ROOT, "assets", "img", "ruler-preview")
    subprocess.run(["pdftoppm", "-r", "110", "-png", "-singlefile",
                    os.path.join(OUT, "MiniatureNestStudio_Scale_Ruler_Letter.pdf"), prev], check=True)
    print(prev + ".png")
