"""hero-frames.png: nine frames over the first 8 s, each labelled with when it was taken (ms after navigation)."""
import io, os, time
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
EXE = os.environ.get("CHROME_SHELL") or os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell")
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
AT = [250, 700, 1200, 1650, 1900, 2600, 4100, 5100, 7900]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE); pg = b.new_page(viewport={'width': 1440, 'height': 900}, color_scheme='dark')
    pg.goto('http://127.0.0.1:8712/index.html', wait_until='commit'); t0 = time.time(); shots = []
    for ms in AT:
        while (time.time() - t0) * 1000 < ms: time.sleep(.005)
        real = int((time.time() - t0) * 1000); shots.append((real, Image.open(io.BytesIO(pg.screenshot()))))
    b.close()
W, H = 480, 300; sheet = Image.new('RGB', (W * 3 + 40, H * 3 + 40), '#0A0C18'); d = ImageDraw.Draw(sheet)
for i, (ms, im) in enumerate(shots):
    x, y = 10 + (i % 3) * (W + 10), 10 + (i // 3) * (H + 10)
    sheet.paste(im.resize((W, H), Image.LANCZOS), (x, y)); d.rectangle((x, y, x + 74, y + 20), fill='#000'); d.text((x + 6, y + 4), f'{ms / 1000:.2f} s', fill='#FFC24D')
sheet.save(os.path.join(root, 'hero-frames.png')); print([s[0] for s in shots])
