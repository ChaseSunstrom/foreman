---
name: svg-icon-system
title: "SVG icon system"
area: looks
tags: [icons, svg, iconography, stroke, grid, accessibility]
detect: []
related: [svg-canvas, look-transit-signage, look-lab-notebook]
---
One grid, one stroke, one corner rule and drawn optical sizes, so every icon in a product reads as one family.

## Grid
A 24-unit `viewBox`, 2 units of padding: the drawing lives in 2-22. Keyline shapes look the same size: circle 20 across, square 18, portrait 16 by 20, landscape 20 by 16. Straight lines sit on whole or half units.

## Stroke
One width for the whole set: 1.5 beside text at weight 400, 2 beside 500-600. `stroke="currentColor"`, `fill="none"`, round caps and joins. Colour comes from the text; an icon that carries meaning holds 3:1 against what touches it (`ui/type-and-colour.md`); a status icon goes with a word.

## Corners
Outer corners of shapes 12 units or larger take radius 2, smaller ones 1; inner corners come from the round join.

## Optical size
Rendered stroke stays between 1.25 and 2 CSS px. At 16 px the 24 drawing thins to 1 px: draw a 16-unit variant with fewer details instead. At 32 the 24 drawing scales; at 48 and up use a variant or `vector-effect="non-scaling-stroke"`.

## Markup
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="1em" height="1em" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">
  <rect x="3" y="5" width="18" height="16" rx="2"/>
  <path d="M3 10h18M8 3v4M16 3v4"/>
</svg>
```
Decorative or inside a labelled button: `aria-hidden="true"`. Alone with meaning: `role="img"` and a label. Sized in `em`, centred on its text's line.

## Suits
Any product UI, docs site or app with more than a handful of icons.
Not for: illustration, logos, emoji (never icons).

## Verify
- `pytest -q test_icons.py`: every icon in the set passes.
- `grep -rn "<svg" src | grep -v currentColor`: lists only illustrations.

## Test first
Commit the check before the first icon; run it on each one.
```python
# test_icons.py
import pathlib
import xml.etree.ElementTree as ET

STROKE = "1.5"  # the set's one width
BOX = {"rect": lambda n: [n("x"), n("x") + n("width"), n("y"), n("y") + n("height")],
       "circle": lambda n: [n("cx") - n("r"), n("cx") + n("r"), n("cy") - n("r"), n("cy") + n("r")],
       "line": lambda n: [n("x1"), n("x2"), n("y1"), n("y2")]}  # the live-area check; paths are checked by eye


def check(svg):
    if "<!DOCTYPE" in svg.upper() or "<!ENTITY" in svg.upper():
        return ["a DOCTYPE or ENTITY has no place in an icon"]
    try:
        root = ET.fromstring(svg)
    except ET.ParseError as e:
        return [f"not well-formed: {e}"]
    bad = []
    if root.get("viewBox") != "0 0 24 24":
        bad.append("viewBox is not 0 0 24 24")
    if (root.get("fill"), root.get("stroke"), root.get("stroke-width")) != ("none", "currentColor", STROKE):
        bad.append("root needs fill=none, stroke=currentColor and the set's width")
    if root.get("aria-hidden") != "true" and not (root.get("role") == "img" and root.get("aria-label")):
        bad.append("neither hidden nor labelled")
    for e in root.iter():
        tag = e.tag.split("}")[-1]
        bad += [f"{tag}: {k}={e.get(k)}" for k in ("fill", "stroke") if e.get(k) not in (None, "none", "currentColor")]
        if e.get("stroke-width") not in (None, STROKE):
            bad.append(f"{tag}: stroke-width {e.get('stroke-width')}")
        if tag in BOX:
            try:
                box = BOX[tag](lambda k: float(e.get(k, "0")))
            except ValueError:
                bad.append(f"{tag}: a size off the 24-unit grid")
                continue
            if any(not 2 <= v <= 22 for v in box):
                bad.append(f"{tag} leaves the 2-22 live area")
    return bad


def test_icons():
    icons = sorted(pathlib.Path("src/icons").glob("*.svg"))
    assert icons, "no icons in src/icons"
    for path in icons:
        assert check(path.read_text(encoding="utf-8")) == [], path
```

## Do
- Draw new icons from the keyline shapes, never by scaling another set's icon.

## Avoid
- Mixing sets: two icon libraries in one product read as two products.

## Review
- [ ] One stroke width, one corner radius, round caps across the set.
- [ ] Every icon is hidden or labelled; icon-only buttons have a name.
- [ ] 16 px icons are drawn variants, not shrunk 24s.
