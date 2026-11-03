# Sampo's logo: Runestone

A rune-cut millstone that is also an engine: an iron disc in a hammered-bronze rim, eight runes round the run of the
stone, eight harps of curved furrows, and a forge-lit eye crossed by the rynd bar that drives it. The draft and its
reasoning are in [directions/runestone](../directions/runestone/README.md); [REVIEW.md](REVIEW.md) holds the cold
reviews. Colours and motion come from [tokens.json](../tokens.json).

## The files

| File | What it is | Where it goes |
|---|---|---|
| mark.svg | the full mark, and the animated mark's still | dark surfaces, docs, the site |
| mark-animated.svg | the stone turns, the runes light, sparks leave the rim | the site's hero, splash screens |
| mark-light.svg | the mark for parchment | light surfaces |
| icon-16.svg | the 16 px icon, drawn for that size, not scaled; also the SVG favicon | tabs, tree views, browsers |
| favicon.ico | icon-16.svg at 16, 32 and 48 px | browsers that want an .ico |
| mono.svg | one ink, `currentColor` | print, stamps, the terminal, embossing |
| wordmark.svg | the mark and SAMPO in the display face | headers, slides |
| readme-header-light.svg, readme-header-dark.svg | 960 x 240 header | the README, with `<picture>` and `prefers-color-scheme` |
| share.svg, share.png | 1200 x 630 social card | og:image, twitter:image |
| app-icon.svg, app-icon-512.png, app-icon-1024.png | full-bleed square; the platform masks it | PWA manifest, stores |
| desktop-icon.svg, desktop-icon-1024.png | the rounded tile on the macOS icon grid, with its margin | Sampo Desktop |
| pane-glyph.txt | one terminal cell at rest and turning | the pane and the statusline |

## Rules

- **Light surfaces.** On parchment the disc keeps its iron: it takes the light theme's stone role (#16181C, "the iron
  the mark is cut in") and the rim takes the light theme's bronze (#7A5020, 6:1 on parchment). Hammered bronze
  (#B07A3B) is the rim at night. Use mark-light.svg on light, mark.svg on dark; never invert the disc.
- **Runes.** Eight staves pointing at the eye, each its own silhouette, clockwise from the top: one branch, opposed
  hooks, a short slant across (naudiz), a small bump mid-stave (thorn), a chevron off the stave, a cross bar and a
  slant, a bare stave, a double chevron. Radial, so none stands upright as a letter.
- **Small sizes.** Below 96 px use icon-16.svg or favicon.ico, never the scaled mark: under 96 px its runes stop
  reading as eight different signs. The icon has no runes and no ticks. Its bar sits on whole pixels (row 7, columns
  5 to 10) and stops a pixel short of the eye at each end, so forge light shows past it.
- **Clear space.** Half the rim's radius on every side. Smallest full mark: 96 px.
- **Furrows.** #4A5160, 2.2:1 on the disc: present, never louder than the runes.
- **Wordmark.** SAMPO in TeX Gyre Pagella Bold (a Palatino-metric face under the GUST Font License, matching font.display's stack), outlined to paths so it
  renders anywhere, caps tracked +0.06em (the token's +0.02em is for mixed-case headlines), kerned.
- **Motion.** One and a quarter turns (450 degrees) on the mill easing, 4.2 s; the runes light 240 ms apart from
  1.2 s; three sparks of r=2 leave the rim beside the last rune at 2.9 to 4.0 s, as it lights and while the stone
  still moves, flying along the clockwise tangent, with the spin. Nothing loops. Under
  prefers-reduced-motion the file is mark.svg's still: every rune lit, no sparks.
- **Never.** Recolour the runes, add a glow filter, set the wordmark in live text, or put the mark on a mid-tone.

## Building

[build.py](build.py) makes every file here except this README, REVIEW.md and pane-glyph.txt, from one geometry:

    python3 design/sampo/logo/build.py [OUT]

It needs only Python's standard library and rsvg-convert. The SVGs come out byte for byte, and a test rebuilds them
to hold that. The PNGs come from the SVGs with rsvg-convert:

    rsvg-convert -w 512 -h 512 app-icon.svg -o app-icon-512.png
    rsvg-convert -w 1024 -h 1024 app-icon.svg -o app-icon-1024.png
    rsvg-convert -w 1024 -h 1024 desktop-icon.svg -o desktop-icon-1024.png
    rsvg-convert -w 1200 -h 630 share.svg -o share.png

favicon.ico packs icon-16.svg rendered at 16, 32 and 48 px. Each size is a PNG with a 16-byte directory entry (32 bits
per pixel) after the 6-byte header. Windows Vista and later and every current browser read PNG entries. The type is
outlined from [glyphs.json](glyphs.json): the Pagella outlines, widths and kerning of only the letters used.
`build.py --glyphs FONTDIR` re-extracts them, which takes fontTools.
