---
id: T-0089
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-02T19:05:06Z
updated: 2026-10-02T19:08:49Z
base: 994a4aa912590170d992e89c24c3fc45429e824c
verified: strong
---
# fm plugins sees directory-source marketplaces
## Raw request
> fm plugins index() misses directory-source marketplaces (known_marketplaces installLocation outside plugins/marketplaces/), so find/--pin can't see foreman-ui@foreman
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a plugin in a directory marketplace registered in known_marketplaces.json is found and pinnable — verify with `python3 -m unittest discover -s plugin/tests -p test_plugins.py -q`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] read installLocation marketplaces in index() and _marketplaces()
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 -m unittest discover -s plugin/tests -p test_plugins.py -q` → ✗ exit 1 · Ran 21 tests in 1.724s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree d724667519e7] (2026-10-02T19:06:12Z)
- (step 1) `python3 -m unittest discover -s plugin/tests -p test_plugins.py -q` → exit 0 · Ran 21 tests in 1.702s / OK [ran] [tree d724667519e7] (2026-10-02T19:06:12Z)
- (step 2) `fm plugins find foreman-ui` → exit 0 · foreman-ui@foreman                       available ~0 tok  Foreman inside Claude Code (mods): a band above the prompt, a docked d [ran] [tree d724667519e7] (2026-10-02T19:06:12Z)
- (ac 1) `python3 -m unittest discover -s plugin/tests -p test_plugins.py -q` → exit 0 · Ran 21 tests in 1.227s / OK [ran] [tree d724667519e7] (2026-10-02T19:08:49Z)
- (audit self) `re-read _marketplace_files: cached + installLocation sources, realpath-deduped, missing files skipped; _marketplaces now uses the manifest name (what marketplace remove takes); add_marketplace test still green` → no findings [tree d724667519e7] (2026-10-02T19:08:49Z)
## Log
- 2026-10-02T19:05:06Z created
- 2026-10-02T19:05:47Z planned from capture
- 2026-10-02T19:05:47Z focused
- 2026-10-02T19:05:54Z user approved core in Claude Code's permission prompt
- 2026-10-02T19:08:49Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0036-adversary: Confirmed: `check()` returns `Block` only when the category isn't in `ctx.allow`. Since `plugin` is in `ctx.allow` (from the earlier grant), `b…
- research t0036-operator: The implementation matches its documented contract and is well tested. Findings below are minor.
- research t0036-intent: MEDIUM** — `plugin/lib/fmplugins.py:388-398` (`content_hash`) — For a plugin that is not locally mirrored by its marketplace (a genuinely remote s…
- research t0036-adversary-recheck: All four call sites correctly updated to the 5-tuple. This confirms the pin plumbs through `_ask_prompt` (dialog) and `_grant_prompted`…
## Files touched
- plugin/lib/fmplugins.py
- plugin/tests/test_plugins.py
