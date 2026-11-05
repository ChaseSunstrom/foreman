"""Full-page capture: scroll through so every observer fires, then shoot. fullpage.py OUT W [theme] [rm] [nojs]"""
import sys, os
from playwright.sync_api import sync_playwright
EXE = os.environ.get("CHROME_SHELL") or os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell")
here = os.path.dirname(os.path.abspath(__file__)); url = 'http://127.0.0.1:8712/' + (sys.argv[5] if len(sys.argv) > 5 else 'index.html')
out, w = sys.argv[1], int(sys.argv[2]); theme = sys.argv[3] if len(sys.argv) > 3 else 'dark'
rm = 'rm' in sys.argv[4:]; nojs = 'nojs' in sys.argv[4:]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE)
    ctx = b.new_context(viewport={'width': w, 'height': 900}, color_scheme=theme, reduced_motion='reduce' if rm else 'no-preference', java_script_enabled=not nojs)
    pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(url, wait_until='load'); pg.wait_for_timeout(2500)
    if not nojs:
        y = 0
        while y < pg.evaluate('document.documentElement.scrollHeight'): pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(160); y += 450
        pg.evaluate('window.scrollTo(0,0)'); pg.wait_for_timeout(2600)
        ov = pg.evaluate('document.documentElement.scrollWidth - innerWidth')
        print('overflow-x:', ov)
    if not nojs: pg.add_style_tag(content='.sec,.record,.foot{content-visibility:visible!important}'); pg.wait_for_timeout(1500)
    pg.screenshot(path=out, full_page=True)
    print('errors:', errs)
    b.close()
