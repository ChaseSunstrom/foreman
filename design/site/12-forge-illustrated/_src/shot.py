"""Quick screenshots: shot.py OUT W H [theme] [wait_ms] [scroll_selector] [dpr] [rm]"""
import sys, os
from playwright.sync_api import sync_playwright
EXE = os.environ.get("CHROME_SHELL") or os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell")
here = os.path.dirname(os.path.abspath(__file__)); page_url = 'http://127.0.0.1:8712/index.html'
out, w, h = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
theme = sys.argv[4] if len(sys.argv) > 4 else 'dark'; wait = int(sys.argv[5]) if len(sys.argv) > 5 else 3000
sel = sys.argv[6] if len(sys.argv) > 6 else ''; dpr = float(sys.argv[7]) if len(sys.argv) > 7 else 1; rm = len(sys.argv) > 8 and sys.argv[8] == 'rm'
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE)
    pg = b.new_page(viewport={'width': w, 'height': h}, color_scheme=theme, device_scale_factor=dpr, reduced_motion='reduce' if rm else 'no-preference')
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
    pg.goto(page_url, wait_until='load')
    if sel:
        pg.evaluate(f"document.querySelector('{sel}').scrollIntoView({{block:'start'}})")
    pg.wait_for_timeout(wait)
    pg.screenshot(path=out)
    print('errors:', errs)
    b.close()
