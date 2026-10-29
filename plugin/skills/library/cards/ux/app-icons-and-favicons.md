---
name: app-icons-and-favicons
title: App Icons and Favicons
area: ux
tags: [ux, favicon, app-icon, pwa, manifest, maskable, apple-touch-icon]
detect: [file:site.webmanifest, file:manifest.webmanifest]
related: [pwa, logo-design, icon-design, svg-icon-system, dark-mode, social-share-images]
---
A small icon set: SVG plus 32 px ICO, a 180 px Apple touch icon, and 192/512 px manifest icons including a maskable one.

## Verify
- `identify public/favicon.ico public/apple-touch-icon.png public/icon-192.png public/icon-512.png`: sizes 32 (in ICO), 180, 192, 512.
- `jq '.icons[] | {sizes, purpose}' public/site.webmanifest`: lists 192 and 512, with a `maskable` entry.
- `jq -e '.name and .start_url and .background_color and ([.icons[].sizes] | index("192x192") != null and index("512x512") != null)' public/site.webmanifest`: manifest fields and sizes (Lighthouse 12 dropped its pwa category); add a Playwright test that requests each `<link rel="icon">` and the manifest icons and expects status 200.
- `curl -sI http://localhost:3000/favicon.ico | head -1`: 200, not a 404 spam source.

## Test first
```python
import json, struct

def png_size(path):
    with open(path, "rb") as f:
        f.seek(16)
        return struct.unpack(">II", f.read(8))

def test_icons_exist_with_right_sizes():
    assert png_size("public/apple-touch-icon.png") == (180, 180)
    assert png_size("public/icon-192.png") == (192, 192)
    assert png_size("public/icon-512.png") == (512, 512)
    m = json.load(open("public/site.webmanifest"))
    assert any("maskable" in i.get("purpose", "") for i in m["icons"])
```

## Do
- Head tags: `<link rel="icon" href="/favicon.ico" sizes="32x32">`, `<link rel="icon" href="/icon.svg" type="image/svg+xml">`, `<link rel="apple-touch-icon" href="/apple-touch-icon.png">`, `<link rel="manifest" href="/site.webmanifest">`.
- Draw the icon as a simplified mark, not the full logo: legible at 16 px, 1-2 shapes, bold strokes.
- SVG favicon can adapt to dark mode with `@media (prefers-color-scheme: dark)` inside the file.
- Maskable icon: artwork inside the central 80 percent circle (safe zone), full-bleed background color, 512x512.
- Apple touch icon: 180x180, opaque background (iOS adds no transparency), no rounded corners (the OS rounds them).
- Set `theme-color` meta (with light and dark variants via `media`) and `background_color` in the manifest.
- Cache icons with long max-age and a hashed name when they change.
- Test in the browser tab at 100 percent zoom, on a dark tab bar, and as a home-screen icon.

## Avoid
- A single huge PNG scaled down by the browser.
- Transparent Apple touch icons (black background on iOS).
- Text in a favicon.
- Missing `/favicon.ico` that causes 404 on every crawler visit.

## Review
- [ ] All required sizes exist and the manifest lists 192, 512 and maskable.
- [ ] The mark is legible at 16 px on light and dark tab bars.
- [ ] Maskable art stays inside the safe zone.
- [ ] Head tags and theme-color are set; no icon 404s in the server log.
