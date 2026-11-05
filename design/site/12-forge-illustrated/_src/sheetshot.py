import os
from playwright.sync_api import sync_playwright
EXE = os.environ.get("CHROME_SHELL") or os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell")
here = os.path.dirname(os.path.abspath(__file__))
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE); pg = b.new_page(viewport={'width': 1680, 'height': 900})
    pg.goto('file://' + os.path.join(here, 'sheet.html')); pg.wait_for_timeout(2700)
    pg.screenshot(path=os.path.join(os.path.dirname(here), 'logo-sheet.png'), full_page=True); b.close()
