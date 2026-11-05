import os, json, collections
from playwright.sync_api import sync_playwright
EXE = os.environ.get("CHROME_SHELL") or os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell")
here = os.path.dirname(os.path.abspath(__file__)); url = 'http://127.0.0.1:8712/index.html'
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE); pg = b.new_page(viewport={'width': 1440, 'height': 900})
    b.start_tracing(page=pg, categories=['devtools.timeline', 'disabled-by-default-devtools.timeline'])
    pg.goto(url); pg.wait_for_timeout(1500)
    data = json.loads(b.stop_tracing())
    ev = [e for e in data['traceEvents'] if e.get('ph') == 'X' and 'dur' in e]
    main = collections.Counter(e['tid'] for e in ev if e['name'] == 'RunTask').most_common(3)
    tids = {e['tid'] for e in ev if e['name'] in ('ParseHTML', 'Layout')}
    tid = list(tids)[0]
    tasks = [e for e in ev if e['tid'] == tid and e['name'] == 'RunTask' and e['dur'] > 40000]
    for t in tasks:
        kids = collections.Counter()
        for e in ev:
            if e['tid'] == tid and e['ts'] >= t['ts'] and e['ts'] + e['dur'] <= t['ts'] + t['dur'] and e['name'] != 'RunTask':
                kids[e['name']] += e['dur']
        print(round(t['dur'] / 1000), 'ms:', [(k, round(v / 1000, 1)) for k, v in kids.most_common(8)])
    b.close()
