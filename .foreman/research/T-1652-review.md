**Verdict: changes needed.** Three MEDIUM findings: the worker write guard, release versioning, and the DTCG importer silently dropping tokens. I read the code and did not run any of it, so each reproducer is derived from the code.

Pre-audit: the large-file notices are only hotspot flags. The Chromium skip on `Xray` is real. `marketplace.json` needs no `plugin.json` edit, since `plugin/.claude-plugin/plugin.json` didn't change. Steps: no step names `fmcli.py`, `fmdesign.py` or the test file, so the plan is missing a step for them.

## lens: adversary
- MEDIUM — plugin/lib/fmcli.py:7182 and plugin/lib/fmdesign.py:~1871-1910 — `tokens` stays worker-allowed but now writes. `--to md --out FILE` goes through `write_section` and appends a `## Tokens` section to any existing UTF-8 file. `--to brand --out DIR` writes `favicon.svg` and `card.svg` into any directory. The T-1717 worker guard covers only `--save` and `--clear`. The comment at fmcli.py:7178 says `--out` is refused for workers because it would write past the run's own write guard. The "# T-1652: prints only" comment at fmdesign.py:1883 is now false. Reproducer: `FOREMAN_WORKER_OF=run-1 fm design tokens t.json --to md --out ~/.claude/CLAUDE.md`. Fix: raise a ValueError for a worker when `to in (brand, md)` and `--out` is set, as `--save` does. `palette --out` (fmdesign.py:1857) already has this flaw. — high
- LOW — plugin/lib/fmdesign.py:1684 — `xray --out` isn't checked against the page or the tokens file, and `write_atomic` replaces either with PNG bytes. Reproducer: `fm design xray page.html --tokens DESIGN.md --out DESIGN.md`. Fix: refuse when `realpath(out)` equals the page or tokens file; this is the same class as the earlier fmscene `--out` finding. — high

## lens: edge
- MEDIUM — plugin/lib/fmdesign.py:1432-1433, 1496-1520 — the DTCG importer drops tokens silently. When `light` or `dark` exists, all other top-level groups are ignored, and aliases resolve only within `flat["light"]` and the theme's own group. Reproducer: `{"global":{"blue":{"$type":"color","$value":"#00f"}},"light":{"bg":{"$type":"color","$value":"{global.blue}"}},"dark":{"bg":{"$type":"color","$value":"#000"}}}`. `bg` loses its light value with no message, which is the Tokens Studio layout. Composites, a non-sRGB colour without `hex`, unresolved aliases and name collisions in `_put` (`color.a` and `color-a` merge) are also dropped silently. Fix: treat non-theme top-level groups as shared, and count what was skipped and print it to stderr. — medium
- LOW — plugin/lib/fmdesign.py:1686 — a page with zero painted elements prints "0 of 0 … (100%)" and exits 0. Fix: say "nothing painted" and exit 2. — high
- LOW — plugin/lib/fmdesign.py:~1900 — `--to md --out X` where X is the source DESIGN.md replaces the `fm design extract` intro and drops its Source and contrast lines. Fix: refuse when `realpath(src)` equals `realpath(out)`. — medium

## lens: operator
- MEDIUM — plugin/lib/fmrelease.py:125-129 — `_bump` moves only the `foreman` and `foreman-ui` entries, so `foreman-design` stays at 0.1.0 forever. Its skills are symlinks into `plugin/skills`, whose content changes every release. Installs of it never see a version change, so they may never update. Fix: bump the `foreman-design` entry and its `plugin.json` with `foreman`, or drop `version` from the entry. — medium
- LOW — .claude-plugin/marketplace.json:25 — the description says to install the foreman plugin too. With both installed, ui-design, directions and design-extract are listed twice in every session, which costs always-on context with no gain. Fix: say plainly it is for installs without the foreman plugin and not to enable both. — medium
- LOW — plugin/lib/fmcli.py:6661,6663 — the `--light` and `--dark` help still says "tokens --to app|pane", but `--to brand` honours them (dark by default). Fix: update the help text. — high

## lens: maintainer
- LOW — plugin/tests/test_design_surfaces.py:683 — the xray test is skipped without Chromium, so criterion 4 is unproven there. Nothing covers the 3000-element cap, `--to brand` with a missing role (exit 2), `infer --json`, or a worker running `tokens --to md --out`. Fix: add the cheap non-browser ones.

## lens: intent
Nothing missing against the five criteria.

## Acceptance criteria
- Brand: met by code and test (favicon and card in the accent, bg and text roles). I did not run it.
- DTCG or Figma `.json` read as tokens: met. `--to md` reads back, and bad, deep or empty files exit 2. The silent drops above are not part of the criterion.
- `infer`: met.
- `xray`: met in code; the test needs Chromium, so I can't confirm it from here.
- Marketplace entry: met as written (`plugin.json` and the three skill links resolve). Whether Claude Code follows symlinks that point outside the plugin dir when it caches the plugin is not verifiable here.

## Implicit decisions
- Brand assets default to the dark theme.
- Brand assets use `system-ui` rather than the token font.
- xray treats a colour as on-token within ±2 per channel, ignores alpha, and counts both themes' hexes as valid.
- Figma "dark" is any mode name containing "dark".
- Proposed token names are `--color-N`, `--duration-N` and `--radius-N`.
- `foreman-design` is versioned independently, starting at 0.1.0.

## Not checked
I did not run the tests or Chromium, or `claude plugin validate`. I did not check plugin caching of symlinks. I did not check the `_safe_css` and `to_app` sinks beyond their existing contracts.

Noticed: `plugin/lib/fmdesign.py:1857` `palette --out` is worker-allowed and writes arbitrary paths (the same flaw as the first finding, but from T-1714).
