"""Frame rate and long tasks, measured in the page with the Performance API. measure.py W H [dpr]"""
import sys, os, json
from playwright.sync_api import sync_playwright
EXE = os.environ.get("CHROME_SHELL") or os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell")
here = os.path.dirname(os.path.abspath(__file__)); url = 'http://127.0.0.1:8712/index.html'
w, h = int(sys.argv[1]), int(sys.argv[2]); dpr = float(sys.argv[3]) if len(sys.argv) > 3 else 1; url += sys.argv[4] if len(sys.argv) > 4 else ''
INIT = """
window.__lt = []; new PerformanceObserver(l => l.getEntries().forEach(e => __lt.push({t: Math.round(e.startTime), d: Math.round(e.duration)}))).observe({type: 'longtask', buffered: true});
window.__rec = (ms) => new Promise(res => { const ts = []; const t0 = performance.now(); const f = t => { ts.push(t); if (t - t0 < ms) requestAnimationFrame(f); else res(ts); }; requestAnimationFrame(f); });
"""
def stats(ts):
    d = sorted(b - a for a, b in zip(ts, ts[1:])); n = len(d)
    return {'fps': round(1000 * n / (ts[-1] - ts[0]), 1), 'median_ms': round(d[n // 2], 1), 'p95_ms': round(d[int(n * .95)], 1), 'worst_ms': round(d[-1], 1), 'frames_over_33ms': sum(x > 33.4 for x in d)}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE)
    pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=dpr, color_scheme='dark'); pg.add_init_script(INIT)
    pg.goto(url, wait_until='load'); pg.wait_for_timeout(1500)
    if os.environ.get('HIDE'): pg.add_style_tag(content=os.environ['HIDE'] + '{display:none!important}'); pg.wait_for_timeout(300)
    cdp = pg.context.new_cdp_session(pg); cdp.send('Performance.enable')
    met = lambda: {m['name']: m['value'] for m in cdp.send('Performance.getMetrics')['metrics']}
    m0 = met(); ts_idle = pg.evaluate('__rec(6000)'); m1 = met(); idle = stats(ts_idle); nf = len(ts_idle) - 1
    idle['main_thread_ms_per_frame'] = {k: round((m1[k] - m0[k]) * 1000 / nf, 2) for k in ('TaskDuration', 'ScriptDuration', 'LayoutDuration', 'RecalcStyleDuration')}
    idle['load_avg'] = open('/proc/loadavg').read().split()[0]
    scroll = pg.evaluate("""(async () => { const p = __rec(7000); const H = document.documentElement.scrollHeight - innerHeight; let y = 0;
      const iv = setInterval(() => { y = Math.min(H, y + 90); scrollTo(0, y); }, 50); const ts = await p; clearInterval(iv); return ts; })()""")
    scroll = stats(scroll)
    lt = pg.evaluate('__lt'); nav = pg.evaluate("JSON.stringify(performance.getEntriesByType('navigation')[0].toJSON())")
    nav = json.loads(nav)
    print(json.dumps({'viewport': f'{w}x{h}@{dpr}', 'hero_idle': idle, 'scrolling': scroll,
                      'longtasks': {'count': len(lt), 'longest_ms': max([x['d'] for x in lt] or [0]), 'all': lt[:12]},
                      'domContentLoaded_ms': round(nav['domContentLoadedEventEnd']), 'load_ms': round(nav['loadEventEnd'])}, indent=1))
    b.close()
