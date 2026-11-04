# Sampo's logo: the anvil-stone

Design direction 12, the illustrated forge. A steel anvil set into a rune-cut stone, the stone bound with a riveted
iron band and a molten seam, a fire of many colours behind it (gold, the blue root, red, green, violet), a hammer and a
brass star over it. The Sampo of the Kalevala is forged, so the mark is the forge. [REVIEW.md](REVIEW.md) holds the
verdict and names the cold critiques; colours and motion come from [tokens.json](../tokens.json).

## The files

| File | What it is | Where it goes |
|---|---|---|
| mark.svg | the full mark, and the animated mark's still | dark surfaces, docs, the site |
| mark-animated.svg | the fire burns, the hammer strikes twice and throws sparks, the runes kindle, the rivets heat | the site's hero, splash screens |
| mark-light.svg | the mark for the day; the star in the light bronze | light surfaces |
| mark-simple.svg | the same silhouette with the detail taken out: three facets, one band, three plumes | 32 to 96 px |
| icon-16.svg | the 16 px icon, drawn for that size, not scaled; also the SVG favicon | tabs, tree views, browsers |
| favicon.ico | icon-16.svg at 16, 32 and 48 px | browsers that want an .ico |
| mono.svg | one ink, `currentColor` | print, stamps, the terminal, embossing |
| wordmark.svg | the mark and Sampo in the display face | headers, slides |
| readme-header-light.svg, readme-header-dark.svg | 1280 x 320 banner: dawn sky, or the night with the Otava | the README, with `<picture>` and `prefers-color-scheme` |
| share.svg, share.png | 1200 x 630 social card | og:image, twitter:image |
| app-icon.svg, app-icon-512.png, app-icon-1024.png | full-bleed square; the platform masks it | PWA manifest, stores |
| desktop-icon.svg, desktop-icon-1024.png | the rounded tile on the macOS icon grid, with its margin | Sampo Desktop |
| pane-glyph.txt | one terminal cell at rest and turning | the pane and the statusline |

## Rules

- **Light surfaces.** The anvil and the stone keep their iron by day; the fire stays the fire. Only the star changes:
  pale brass (#F0D392, the dark accent) at night, the light theme's bronze (#7A5A26) by day. Use mark-light.svg on
  light, mark.svg on dark.
- **Runes.** Five cut into the stone, each lit in one of the fire's colours. They are signs, not letters.
- **Small sizes.** 32 to 96 px: mark-simple.svg. Below 32 px: icon-16.svg or favicon.ico, never a scaled mark. The
  icon is ten shapes on the half-pixel grid: the stone, the band, the anvil, the fire.
- **Clear space.** A quarter of the mark's width on every side. Smallest full mark: 96 px.
- **Wordmark.** Sampo in Bodoni Moda (420, optical size 96), the tagline in its italic, the kicker in Martian Mono;
  both are under the SIL Open Font License, so the files carry them outlined to paths and render anywhere.
- **Motion.** The fire burns two to four short cycles; the hammer strikes twice on the strike easing (2.2 s a blow,
  from 0.4 s), each blow throwing sparks, flashing the seam and twinkling the star; the five runes kindle 300 ms apart
  from 0.6 s; the nine rivets heat in turn from 1 s. Everything ends by 4.8 s on the still: the hammer raised, the
  sparks and glows gone. Nothing loops. Under prefers-reduced-motion the file is mark.svg's still.
- **Never.** Recolour the fire or the runes, set the wordmark in live text, or put the mark on a mid-tone.

## Building

[build.py](build.py) makes every file here except this README, REVIEW.md and pane-glyph.txt; the drawing functions
live in [art.py](art.py):

    python3 design/sampo/logo/build.py [OUT]

It needs Python's standard library and rsvg-convert. The SVGs come out byte for byte, and a test rebuilds them to hold
that. build.py renders the PNGs (app-icon at 512 and 1024, desktop-icon at 1024, share at 1200 x 630) with
rsvg-convert, and packs favicon.ico from icon-16.svg rendered at 16, 32 and 48 px, each a PNG entry. The type is
outlined from [glyphs.json](glyphs.json): the outlines, widths and kerning of only the letters used.
`build.py --glyphs FONTDIR` re-extracts them from BodoniModa-normal.woff2, BodoniModa-italic.woff2 and
MartianMono-normal.woff2, which takes fontTools and brotli.
