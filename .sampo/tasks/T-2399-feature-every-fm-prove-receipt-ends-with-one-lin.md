---
id: T-2399
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmprove.py, plugin/tests/test_prove.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-31T14:03:49Z
updated: 2026-11-02T00:12:28Z
group: Mission 7 proof inbox
base: 112e684253f269b6fc95316028024afdd61cb7d9
base_tree: dccdbbfa065d876c3e97490791921dce236f493a
predict_minutes: 7
predict_attempts: 1
plan0_at: 2026-11-01T23:58:23Z
plan0_scope: [plugin/lib/fmprove.py, plugin/tests/test_prove.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# Every fm prove receipt ends with one line saying what it does not prove
## Raw request
> FEATURE: every fm prove receipt ends with one line saying what it does not prove (Mission 7 inbox, tier 1)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm prove's text output ends with a 'Does not prove:' line for its mode (scan, --only, --docs, --infra, --release, --data, --migration; not --rollup, --json or a usage error), and the scan receipt in research/ ends with the scan line — verify with `python3 plugin/tests/run.py test_prove test_find`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: fm prove on a fixture repo ends with 'Does not prove:'; the receipt file's last line is the same; fm prove --docs ends with its line; --json has does_not_prove
2. [x] fmprove: one DOES_NOT constant per mode appended to the text, the receipt and the JSON; MASTER and CHANGELOG
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_prove.DocsProof test_find` → ✗ exit 1 · Ran 144 tests in 8.2s (24 classes, 16 at a time; slowest: FindBlindSpots 8s, FindCli 6s, FindRenders 6s) / FAILED (2 classes: test_prove.DocsProof, test_find.FindProve) [ran] [tree e48dee92b26f] (2026-11-01T23:58:48Z)
- (step 1) `python3 plugin/tests/run.py test_prove.DocsProof test_find` → exit 0 · Ran 144 tests in 8.8s (24 classes, 16 at a time; slowest: FindBlindSpots 9s, FindRenders 6s, FindCli 6s) / OK [ran] [tree 859141debb8d] (2026-11-02T00:00:09Z)
- (step 2) `python3 plugin/tests/run.py test_prove test_find` → exit 0 · Ran 229 tests in 9.0s (37 classes, 16 at a time; slowest: FindBlindSpots 9s, InfraProof 7s, FindCli 6s) / OK [ran] [tree 859141debb8d] (2026-11-02T00:00:19Z)
- (ac 1) `python3 plugin/tests/run.py test_prove test_find` → exit 0 · Ran 229 tests in 8.8s (37 classes, 16 at a time; slowest: FindBlindSpots 9s, InfraProof 7s, FindCli 6s) / OK [ran] [tree 5475ce09eee8] (2026-11-02T00:06:29Z)
- (audit edge) `self-review: one wrapper around the old body (renamed _prove) prints the mode's DOES_NOT line after any result, skipped for --rollup and --json (each mode's JSON stays parseable) and for exit 2 except --docs, whose 2 means nothing checkable; the scan receipt file ends with the scan line; mode detection reads the same args the dispatch does, --only first` → a usage error (not a directory) prints no line; --docs with nothing checkable still prints its line; --json output still parses [tree 5475ce09eee8] (2026-11-02T00:06:29Z)
- (audit self) `self-review: one wrapper around the old body (renamed _prove) prints the mode's DOES_NOT line after any result, skipped for --rollup and --json (each mode's JSON stays parseable) and for exit 2 except --docs, whose 2 means nothing checkable; the scan receipt file ends with the scan line; mode detection reads the same args the dispatch does, --only first` → no findings [tree 5475ce09eee8] (2026-11-02T00:06:29Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 5475ce09eee8] (2026-11-02T00:07:23Z)
## Log
- 2026-10-31T14:03:49Z created
- 2026-11-01T23:44:05Z planned from capture
- 2026-11-01T23:58:22Z focused
- 2026-11-01T23:58:23Z predicted from its closes: 7 min, 1 attempt(s)
- 2026-11-01T23:58:24Z criterion 1 verify: `python3 plugin/tests/run.py test_prove` → `python3 plugin/tests/run.py test_prove test_find`
- 2026-11-01T23:58:24Z criterion 1 text: fm prove PATH's text output and its research/ receipt end with a 'Does not prove:' line fitted to the mode (scan: leads and held-back findings are untried, a proven ticket shows a failing test, not the fix or the cause, nothing outside fm find's finders was looked at); fm prove --docs ends with its own (a documented command ran, not that the prose is right); --json carries it as does_not_prove → fm prove's text output ends with a 'Does not prove:' line for its mode (scan, --only, --docs, --infra, --release, --data, --migration; not --rollup, --json or a usage error), and the scan receipt in research/ ends with the scan line
- 2026-11-01T23:58:24Z scope: --json left as each mode prints it (appending would break the JSON); one wrapper adds the line for every mode
- 2026-11-02T00:00:19Z scope: test_find holds the scan receipt's test
- 2026-11-02T00:06:53Z done
- 2026-11-02T00:06:55Z committed 18abf408 (5 files)
- 2026-11-02T00:07:23Z guard authorization added: publish
- 2026-11-02T00:12:28Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2397 [FEATURE S, done, 3 steps] Research claims say how they were learned (ran, read, recalled); fm prove labels a Decision resting only on recalled ones — lesson: Bef…
- T-1873 [FEATURE M, done, 3 steps] Fm scene gallery: every built-in scene on one contact sheet, each with a one-line caption — lesson: A playbook has a token ceiling (tes…
- T-2353 [FEATURE M, done, 3 steps] The router picks the cheapest model that holds: probing down a tier, and fm run uses it too (Mission 8, #9) — lesson: A confirmation st…
- decision 2026-10-31: Mission 6 (tools, #5) approach A: wire the parts Foreman has into one loop on the active task (T-2270's hook notices the miss; fm which, fm lib and …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_prove.py
## Preflight
Changed in scope since this was planned (2026-10-31): CHANGELOG.md, MASTER.md, plugin/lib/fmprove.py, plugin/tests/test_prove.py; re-ground the plan against them before editing
## Lessons
- Say what a passing check does not show in the same breath as the pass, so nobody reads more into a green than it carries
## Plan gaps
- failed first: step 1 red tests: fm prove on a fixture repo ends with 'Does not prove:'; the receipt file's last line is …
## Files touched
- plugin/tests/test_find.py
- plugin/tests/test_prove.py
- plugin/lib/fmprove.py
- MASTER.md
- CHANGELOG.md
