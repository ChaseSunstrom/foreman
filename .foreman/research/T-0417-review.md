## Verdict
Changes needed. The placeholder selector and the alert rule will flag healthy apps. A permanent spinner can also make the crawl hit its timeout and lose every result.

## Findings

**intent / edge**
- HIGH — `smoke_web.cjs:231` — `[class*="placeholder" i]:empty` also matches `<input class="placeholder:text-gray-400">`. Tailwind does this, and `input` is a void element, so `:empty` matches. Any healthy Tailwind form is reported as "loading placeholder still showing". `[class*="loading"]` and `[class*="spinner"]` also match permanent UI such as a connection indicator or a `spinner-btn`. Fix: drop the `:empty` clause and `[class*=placeholder]`. Match loading and spinner classes only on non-form elements. Prefer `aria-busy` and skeleton or shimmer classes. Confidence: high.
- MEDIUM — `smoke_web.cjs:286` — The alert rule only checks `visible()` (width and height > 0). The Next.js `#__next-route-announcer__` has `role="alert"`, is 1px and clipped, and holds the page title. It is flagged as "alert shown" after navigation. Fix: ignore elements ≤ 2px or with a clip. Skip alerts with `aria-live="polite"` content that isn't an error. Confidence: medium.
- MEDIUM — `smoke_web.cjs:291-300` — Fixed or sticky elements that overlap by design are flagged. Examples: a fixed header with a fixed sidebar at the corner, a sticky table header with a sticky first column, and a modal over a fixed button. Fix: restrict the check to elements that are both `position:fixed`, and ignore sticky elements and anything under an open `[role=dialog]`. Confidence: medium.
- MEDIUM — `smoke_web.cjs:250-258` — Only the page's own origin is checked. An SPA on :5173 calling an API on :8000 gets no 4xx/5xx or request-failed report. The console "Failed to load resource" line is also dropped at line 248. A broken backend is invisible, which is the exact JARVIS case. Fix: check every origin except known third parties, or report cross-origin 5xx and failures. Confidence: high.
- MEDIUM — `smoke_web.cjs:308-310` — This is a silent false negative. An SPA with no `role=tab` is checked at its start view only, and the output shows nothing missing. Tabs hidden behind a phone hamburger menu are skipped by the `isVisible` check, which hides them at 390px, where the bugs are. Fix: report "0 tabs found" in the output, and fall back to `nav a, [role=tab], [role=link]`. Confidence: high.
- MEDIUM — `smoke_web.cjs:269` vs `fmsmoke.py:151` — Settle time is up to 5.5 s per view. That is 25 views × 2 viewports ≈ 275 s, over the 240 s timeout. The JSON line prints only at the end, so a timeout loses every defect found so far and returns only "did not finish". A permanent spinner (the first finding) triggers this. Fix: add a global deadline in the script and print partial results when it expires. Confidence: high.
- MEDIUM — `fmsmoke.py:158` — `fm check` runs smoke on every task close. A stopped dev server gives `ERR_CONNECTION_REFUSED` and blocks unrelated tasks. A machine or lane without Playwright raises `UsageError` and also blocks. Fix: name "server not running" explicitly, and consider a `--skip-if-down` mode or a clear `fm smoke set off` hint in the error. Confidence: medium.
- LOW — `fmsmoke.py:146` — `"/.claude/" in d` tests the absolute path. Any project that lives under `~/.claude` (Foreman itself) never finds Playwright. Fix: test `os.path.relpath(d, root)`. Confidence: high.
- LOW — `fmhooks.py:1478` — `meta.smoke` is truthy for `{"off": why}`. The drive then says "fm smoke, then …", and `fm smoke` errors. Fix: test `.get("smoke", {}).get("web")`. Confidence: high.
- LOW — `smoke_web.cjs:305` — The tab name is not truncated, so a long name causes ENAMETOOLONG and the whole crawl reports "crawl crashed". Fix: `.slice(0, 40)`. Confidence: medium.

**adversary**
- LOW — `fmsmoke.py:155` and `:142` — `FOREMAN_SMOKE_RUNNER` runs any command, and `FOREMAN_PLAYWRIGHT` is `require()`d. This is the same privilege as the process environment, so it is not an escalation. But `FOREMAN_SMOKE_RUNNER='echo {"views":[],"defects":[]}' fm check` forges a passing gate and records it as evidence. Fix: ignore the runner unless a test marker is set, for example `FOREMAN_TEST`. Confidence: medium.
- LOW — `fmsmoke.py:211` — Defect text comes from the page (console, alert and tab text) and reaches the terminal and the model unfiltered. Control characters, escape sequences and injected instructions pass through. Fix: strip `[\x00-\x1f\x7f-\x9f]` and cap the length. Also, `json.loads` may return a non-dict, or defects may lack keys, which raises a traceback. Confidence: medium.

**drive**
- MEDIUM — `fmhooks.py:1472-1481` — The drained push skips the `DRIVE_MAX` and `_progressed` guards. It fires once per `len(briefs)` value, so it cannot loop by itself. A loop is still possible if each pass captures and drops a "defect": `briefs` grows and the push comes back every time. It also fires once per session. A full-autonomy session that only answers a question gets "check the whole product". Fix: apply the `DRIVE_MAX` check, and require that this session did work. Confidence: medium.

**operator**
- LOW — `fmdoctor.py:59` — `check_product` has no test; only `nudge` does. `surfaces` runs `git ls-files` with a 10 s timeout (a miss returns PASS, which is acceptable). It also reads every `package.json` up to 200 KB when there is no AI match, so a large monorepo could be slow. It also warns on any tracked `.html` or `.css`. Confidence: medium.

## Acceptance criteria
- Smoke names each defect and fails; passes on a healthy page: met. The mock-runner tests and the recorded JARVIS browser run support this. The false-positive risks above remain.
- `fm check` runs `fm smoke` when set: met (`test_check_runs_smoke`).
- A drained queue in full autonomy gets one push: met (`test_drained_queue_checks_the_product`).

## Not checked
I did not run any tests or a browser. I did not check how `fm check` times out its gate commands or the `_progressed` semantics, and I did not read the CHANGELOG claims against the JARVIS run.
