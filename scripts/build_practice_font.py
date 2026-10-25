"""Build the book's original seven-letter modular font and verify its contents.

Source grids are editable. Shared pixel edges are removed before outlining;
the result is vector contours rather than overlapping square glyphs.
"""
from pathlib import Path
import json
import shutil
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/designs/practice-font-grid.json"
OUTPUT = ROOT / "assets/fonts/PracticeGridAtlas-Regular.ttf"


def grid_contours(rows, cell, left):
    edges = set()
    for row, line in enumerate(rows):
        for col, value in enumerate(line):
            if value != "1":
                continue
            x, y = left + col * cell, (len(rows) - 1 - row) * cell
            # Clockwise outer paths; holes acquire the opposite winding.
            points = [(x, y), (x, y + cell), (x + cell, y + cell), (x + cell, y)]
            for a, b in zip(points, points[1:] + points[:1]):
                if (b, a) in edges:
                    edges.remove((b, a))
                else:
                    edges.add((a, b))
    contours = []
    while edges:
        first, current = min(edges)
        edges.remove((first, current))
        points = [first]
        while current != first:
            points.append(current)
            candidates = sorted(b for a, b in edges if a == current)
            if len(candidates) != 1:
                raise ValueError("Grid has ambiguous corner-touching outline")
            nxt = candidates[0]
            edges.remove((current, nxt))
            current = nxt
        contours.append(points)
    return contours


def make_glyph(contours):
    pen = TTGlyphPen(None)
    for points in contours:
        pen.moveTo(points[0])
        for point in points[1:]:
            pen.lineTo(point)
        pen.closePath()
    return pen.glyph()


def build():
    data = json.loads(SOURCE.read_text())
    assert set(data["glyphs"]) == set("AEHILOT")
    for rows in data["glyphs"].values():
        assert len(rows) == 7 and all(len(r) == 5 and set(r) <= set("01") for r in rows)
    glyph_order = [".notdef", "space"] + sorted(data["glyphs"])
    glyphs = {"space": make_glyph([])}
    glyphs[".notdef"] = make_glyph(grid_contours(
        ["11111", "10001", "10001", "10001", "10001", "10001", "11111"],
        data["cell"], data["left_side_bearing"]))
    for name, rows in data["glyphs"].items():
        glyphs[name] = make_glyph(grid_contours(rows, data["cell"], data["left_side_bearing"]))
    metrics = {name: (data["advance"], data["left_side_bearing"]) for name in glyph_order}
    metrics["space"] = (data["space_advance"], 0)
    fb = FontBuilder(data["units_per_em"], isTTF=True)
    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap({32: "space", **{ord(n): n for n in data["glyphs"]}})
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=800, descent=-200, lineGap=0)
    fb.setupNameTable({
        "familyName": data["family"], "styleName": "Regular",
        "uniqueFontIdentifier": "PracticeGridAtlas-Regular-1.000",
        "fullName": data["family"] + " Regular",
        "psName": "PracticeGridAtlas-Regular", "version": "Version 1.000",
        "copyright": "Original educational grid font for Learn-Font. CC0 1.0.",
        "licenseDescription": "CC0 1.0 Universal; see practice-font-README.md",
        "licenseInfoURL": "https://creativecommons.org/publicdomain/zero/1.0/",
    })
    fb.setupOS2(sTypoAscender=800, sTypoDescender=-200, sTypoLineGap=0,
                usWinAscent=800, usWinDescent=200, sxHeight=0, sCapHeight=700,
                usWeightClass=400, usWidthClass=5, fsType=0)
    fb.setupPost()
    fb.setupMaxp()
    # Fixed OpenType epoch timestamps keep rebuilds byte-for-byte reproducible.
    fb.font["head"].created = fb.font["head"].modified = 3786912000
    fb.font.recalcTimestamp = False
    fb.save(OUTPUT)
    verify(data)
    shutil.copy2(OUTPUT, ROOT / "assets/designs/practice-font-Regular.ttf")


def verify(data):
    font = TTFont(OUTPUT, recalcTimestamp=False)
    assert set(font.getBestCmap()) == {32, *map(ord, "AEHILOT")}
    assert font["head"].unitsPerEm == 1000
    assert font["maxp"].numGlyphs == 9
    glyph_set = font.getGlyphSet()
    for char in "AEHILOT":
        assert font.getBestCmap()[ord(char)] == char
        assert font["hmtx"][char] == (600, 50)
        assert font["glyf"][char].numberOfContours > 0
        pen = BoundsPen(glyph_set)
        glyph_set[char].draw(pen)
        assert pen.bounds == (50, 0, 550, 700), (char, pen.bounds)
    assert font["glyf"]["space"].numberOfContours == 0
    assert font["hmtx"]["space"] == (300, 0)
    for sample in ["HELLO", "A LITTLE", "AEHILOT"]:
        assert all(ord(c) in font.getBestCmap() for c in sample)
    print(json.dumps({"file": str(OUTPUT.relative_to(ROOT)), "encoded_characters": 8,
                      "glyphs_including_notdef": 9, "samples": ["HELLO", "A LITTLE"]}))


if __name__ == "__main__":
    build()
