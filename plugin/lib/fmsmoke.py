"""fm smoke (T-0417): the product checked the way its user uses it. JARVIS closed 34 tasks with its tests green while
two panels of its web UI never loaded; nothing Foreman ran had ever opened the page. `fm smoke set web <url>` records
the address and makes `fm smoke` one of the project's gates; `fm smoke` opens it in a headless browser (the project's
own Playwright) at desktop and phone width, clicks every tab, and names each defect a user would see."""
import glob
import json
import os
import re
import shlex
import shutil
import subprocess
import tempfile
import time

import fmcore as c

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "smoke_web.cjs")
GATE = "fm smoke"
KEEP = 3  # screenshot runs kept per project


def playwright(root):
    """The Playwright package a crawl can require: FOREMAN_PLAYWRIGHT, else the project's node_modules (a sub-app's
    too, as JARVIS keeps it in jarvis-web/), never a worktree's copy."""
    if os.environ.get("FOREMAN_PLAYWRIGHT"):
        return os.environ["FOREMAN_PLAYWRIGHT"]
    for depth in ("", "*/", "*/*/"):
        for d in sorted(glob.glob(os.path.join(root, depth + "node_modules/playwright"))):
            if ".claude/" not in os.path.relpath(d, root) and os.path.isfile(os.path.join(d, "package.json")):
                return d  # review: relative, so a project under ~/.claude still finds its own
    return None


def _runner():
    """FOREMAN_SMOKE_RUNNER stands in for the browser, only for a Foreman home in a temp folder (the tests'), so a
    command can't forge a passing gate with it (review)."""
    runner = os.environ.get("FOREMAN_SMOKE_RUNNER")
    tmp = os.path.realpath(tempfile.gettempdir()) + os.sep
    return runner if runner and os.path.realpath(c.foreman_home()).startswith(tmp) else None


def _clean(text):
    """Page text (console lines, alerts, tab names) reaches the terminal and the model: no control characters, capped."""
    return c.fit(re.sub(r"[\x00-\x1f\x7f-\x9f]+", " ", str(text)), 300)


def crawl(pw, url, out, timeout=240):
    """{"views": [...], "defects": [{"where", "what"}], "notes": [...]} from one crawl."""
    os.makedirs(out, exist_ok=True)
    runner = _runner()
    cmd = shlex.split(runner) + [url, out] if runner else ["node", SCRIPT, pw, url, out]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        res = json.loads(r.stdout.strip().splitlines()[-1])
        if not isinstance(res, dict):
            raise ValueError(res)
    except (OSError, subprocess.TimeoutExpired) as e:
        return {"views": [], "defects": [{"where": "smoke", "what": f"the crawl did not finish: {e}"}]}
    except (ValueError, IndexError):
        return {"views": [], "defects": [{"where": "smoke", "what": "the crawl failed: "
                                          + _clean((r.stderr or r.stdout).strip())}]}
    return {"views": [_clean(v) for v in res.get("views") or []],
            "defects": [{"where": _clean(d.get("where", "?")), "what": _clean(d.get("what", "?"))}
                        for d in res.get("defects") or [] if isinstance(d, dict)],
            "notes": [_clean(n) for n in res.get("notes") or []]}


def nudge(surfaces, meta):
    """fm doctor's line for a project that ships a web UI nobody checks (None when there's nothing to say)."""
    if "web UI" in surfaces and not meta.get("smoke"):  # {"web": url}, or {"off": why} for a UI no URL serves
        return "this project has a web UI and no product check: fm smoke set web <url>"
    return None


def cmd_smoke(args):
    import fmcli
    p = fmcli.resolve(args)
    if args.action == "set" and args.words[:1] == ["off"]:  # a UI no URL serves (a plugin's own UI mod): no gate
        with c.lock(p.dir):
            meta = c.read_meta(p)
            meta["smoke"] = {"off": " ".join(args.words[1:]) or "no URL serves this UI"}
            meta["checks"] = [x for x in meta.get("checks") or [] if x != GATE]
            c.write_meta(p, meta)
        return fmcli.out(args, meta["smoke"], f"fm smoke is off here ({meta['smoke']['off']}).")
    if args.action == "set":
        if len(args.words) != 2 or args.words[0] != "web" or not args.words[1].startswith(("http://", "https://")):
            raise fmcli.UsageError("fm smoke set web <http(s) url> (or fm smoke set off <why>)")
        with c.lock(p.dir):
            meta = c.read_meta(p)
            meta["smoke"] = {"web": args.words[1]}
            meta["checks"] = list(meta.get("checks") or []) + ([GATE] if GATE not in (meta.get("checks") or []) else [])
            c.write_meta(p, meta)
        return fmcli.out(args, meta["smoke"], f"fm smoke checks {args.words[1]}; it is one of this project's gates "
                                              f"(fm check runs it).")
    url = (c.read_meta(p).get("smoke") or {}).get("web")
    if not url:
        raise fmcli.UsageError("nothing to check yet: fm smoke set web <url> (the address the user opens)")
    pw = playwright(p.root)
    if not pw and not _runner():  # review: a lane or machine without it isn't a product defect; say so, don't block
        return fmcli.out(args, {"url": url, "skipped": "no Playwright"},
                         f"fm smoke: skipped {url}: no Playwright in this checkout (npm i -D playwright, then npx "
                         f"playwright install chromium; or FOREMAN_PLAYWRIGHT=<its package folder>).")
    runs = os.path.join(p.dir, "smoke")
    out = os.path.join(runs, time.strftime("%Y%m%d-%H%M%S", time.gmtime()))
    res = crawl(pw, url, out)
    for old in sorted(glob.glob(os.path.join(runs, "*")))[:-KEEP]:
        shutil.rmtree(old, ignore_errors=True)
    defects = res.get("defects") or []
    c.log_event(p, "smoke", data={"url": url, "views": len(res.get("views") or []), "defects": len(defects)},
                session=fmcli.session())
    text = (f"fm smoke: {url}: {len(res.get('views') or [])} views, "
            + (f"{len(defects)} defects:\n" + "\n".join(f"  ✗ {d['where']}: {d['what']}" for d in defects)
               if defects else "no defects.")
            + "".join(f"\n  · {n}" for n in res.get("notes") or [])
            + (f"\nThe page didn't load: start it, or fm smoke set off <why> to stop checking it."
               if any(d["what"].startswith("did not load") for d in defects) else "")
            + f"\nScreenshots: {out}")
    fmcli.out(args, dict(res, url=url, shots=out), text)
    if defects:
        raise SystemExit(1)
