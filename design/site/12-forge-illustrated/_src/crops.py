"""qa-2x-crops.png: native device pixels at deviceScaleFactor 2 — the hero anvil and blow, the rune stone, the header mark and the footer mark."""
import io, os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
EXE = os.environ.get("CHROME_SHELL") or os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell")
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here); url = 'http://127.0.0.1:8712/index.html'
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE); pg = b.new_page(viewport={'width': 1440, 'height': 900}, device_scale_factor=2, color_scheme='dark')
    pg.goto(url); pg.wait_for_timeout(1700 + 120)          # just after the first blow
    hero = Image.open(io.BytesIO(pg.screenshot()))
    pg.evaluate("document.querySelector('.foot').scrollIntoView({block:'end',behavior:'instant'})"); pg.wait_for_timeout(1800)
    r = pg.evaluate("(() => { const e = document.querySelector('.foot .mark'); const b = e.getBoundingClientRect(); return [b.left, b.top, b.width, b.height]; })()")
    foot = Image.open(io.BytesIO(pg.screenshot())).crop(tuple(int(v * 2) for v in (r[0] - 10, r[1] - 10, r[0] + r[2] + 10, r[1] + r[3] + 10)))
    b.close()
crops = [('hero: anvil, bar and the blow (2x native)', hero.crop((1700, 560, 2700, 1180))),
         ('hero: rune stone and rivets (2x native)', hero.crop((1580, 1150, 2580, 1640))),
         ('header mark, logo-simple at 34 css px (2x native, then 4x nearest)', hero.crop((140, 10, 220, 90)).resize((320, 320), Image.NEAREST)),
         ('footer mark, inline vector (2x native)', foot)]
W = 2040; y = 0; rows = [(crops[0], crops[1]), (crops[2], crops[3])]
H = sum(max(a[1].size[1], c[1].size[1]) + 40 for a, c in rows) + 10
sheet = Image.new('RGB', (W, H), '#0A0C18'); d = ImageDraw.Draw(sheet); y = 10
for a, c in rows:
    x = 10
    for lab, im in (a, c):
        d.text((x, y), lab, fill='#FFC24D'); sheet.paste(im, (x, y + 22)); x += max(im.size[0], 1000) + 20
    y += max(a[1].size[1], c[1].size[1]) + 40
sheet.save(os.path.join(root, 'qa-2x-crops.png')); print(sheet.size)
