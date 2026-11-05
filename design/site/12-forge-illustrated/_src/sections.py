"""Each section at W x 900: section-<name>-W.png. sections.py OUTDIR W [theme] [names...]"""
import sys, os
from playwright.sync_api import sync_playwright
EXE = os.environ.get("CHROME_SHELL") or os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell")
here = os.path.dirname(os.path.abspath(__file__)); url = 'http://127.0.0.1:8712/index.html'
out, w = sys.argv[1], int(sys.argv[2]); theme = sys.argv[3] if len(sys.argv) > 3 else 'dark'
names = sys.argv[4:] or ['how', 'smith', 'rune', 'ward', 'moons', 'record']
SEL = {'how': '#how', 'smith': '#smith', 'rune': '#rune', 'ward': '#ward', 'moons': '#moons', 'record': '#record'}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE)
    pg = b.new_page(viewport={'width': w, 'height': 900}, color_scheme=theme)
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(url, wait_until='load'); pg.wait_for_timeout(1500)
    for n in names:
        pg.evaluate(f"window.scrollTo(0, document.querySelector('{SEL[n]}').getBoundingClientRect().top + scrollY - 57)")
        pg.wait_for_timeout(2300)
        pg.screenshot(path=os.path.join(out, f'section-{n}-{w}.png'))
    print('errors:', errs); b.close()
