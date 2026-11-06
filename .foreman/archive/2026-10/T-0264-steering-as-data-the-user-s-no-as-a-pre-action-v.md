---
id: T-0264
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/, plugin/tests/, plugin/skills/, mods/foreman-ui/, MASTER.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-04T06:29:52Z
updated: 2026-10-04T06:39:57Z
batch: [T-0251, T-0252]
base: 6628b0d0595d89733c40dc89056668702aa23c15
base_tree: 3075ab82eea1526cd728ca14fdc70e09503f0e51
verified: strong
---
# Steering as data: the user's no as a pre-action veto, routing tables in routing.json
## Raw request
> T-0251: FEATURE: the user's "no" as a veto — a correction that says don't/never X becomes a pre-action check: a PreToolUse note when a command or edit matches it
> CONTEXT: corrections in the ledger (fmideas.taste), PreToolUse notes in fmhooks
> DONE-WHEN: after a recorded "never push without asking" correction, a git push command gets the note
> T-0252: FEATURE: routing as data — the stage keywords, built-in skills and split review groups move to plugin/skills/routing.json so fm evolve can target them
> DONE-WHEN: fmplugins and cmd_audit read the JSON and fm evolve accepts it as a target
## Interpretation
Two kinds of steering become data: what the user said not to do is checked before matching actions, and how Foreman routes stages to skills and reviewers lives in one JSON file fm evolve can tune with the bench.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0251: after a recorded "never push without asking" correction, a git push command gets a PreToolUse note quoting it — verify with `python3 plugin/tests/run.py -p "test_steering*" -k Veto`
- [x] T-0252: fmplugins (stage words, UI words, built-in skills) and fm audit --split (review groups) read plugin/skills/routing.json, and fm evolve accepts it as a target (a revision that isn't the same-shaped JSON is refused) — verify with `python3 plugin/tests/run.py -p "test_steering*" -k Routing`
## Non-goals
## Approach (options → choice → why)
Veto: the UserPromptSubmit correction path extracts a 'never/don't/stop X' phrase into the project's vetoes.json (key words, the user's words, date; newest 30); PreToolUse adds a note when a Bash command or an edit's path carries every key word (a note, not a block: a phrase match can be wrong). Rejected: scanning the ledger on every tool call (hook latency). Routing: c.routing() loads plugin/skills/routing.json (empty on error, so a broken file costs hints, not work); fmplugins/fmcli keep their constant names, filled from it; fmevolve.TEXT admits skills/routing.json and check_revision() refuses JSON that doesn't parse or changes the top-level keys; an ablation writes {}.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Tests first: plugin/tests/test_steering.py (Veto, Routing) fail
2. [x] Implement vetoes (record + PreToolUse note) and routing.json (load, readers, evolve target)
3. [x] foreman-ui: the newest recorded veto in the pane header (view model + mod + test)
4. [x] Docs: MASTER.md, CHANGELOG.md (and T-0263's sensitive-export note)
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p "test_steering*"` → ✗ exit 1 · Ran 5 tests in 0.6s (2 classes, 16 at a time; slowest: Veto 1s, Routing 0s) / FAILED (2 classes) [ran] [tree 12c7794c4b49] (2026-10-04T06:30:35Z)
- (step 2) `python3 plugin/tests/run.py -p "test_steering*"` → exit 0 · Ran 5 tests in 0.7s (2 classes, 16 at a time; slowest: Veto 1s, Routing 0s) / OK [ran] [tree 9b3c362bc68d] (2026-10-04T06:32:17Z)
- (step 3) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 62 tests across 1 file. [2.73s] [ran] [tree 9b3c362bc68d] (2026-10-04T06:32:19Z)
- (step 4) `grep -c 'routing.json' MASTER.md CHANGELOG.md` → exit 0 · MASTER.md:2 / CHANGELOG.md:1 [ran] [tree 990a4c890511] (2026-10-04T06:32:28Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 2 of 6 failed: fm doctor → ✗ exit 1 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: FAILED (22 pass, 4 warn, 1 fail); python3 plugin/tests/run.py → ✗ exit 1 · Ran 704 tests in 28.0s (147 classes, 16 at a time; slowest: Stop 21s, TaskLifecycle 19s, Parallel 18s) / FAILED (1 classes) [ran] [tree 990a4c890511] (2026-10-04T06:33:54Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (23 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.6    32.3     150  [0] / SessionEnd                  27.9    29.3     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 06:33 UTC; python3 plugin/tests/run.py → e [ran] [tree e9819afa8b51] (2026-10-04T06:35:29Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (23 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.6    31.5     150  [0] / SessionEnd                  28.1    29.3     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 06:33 UTC; python3 plugin/tests/run.py → e [ran] [tree 42d15f01e07c] (2026-10-04T06:39:50Z)
- (ac 1) `python3 plugin/tests/run.py -p "test_steering*" -k Veto` → exit 0 · Ran 5 tests in 1.3s (1 classes, 16 at a time; slowest: Veto 1s) / OK [ran] [tree 42d15f01e07c] (2026-10-04T06:39:57Z)
- (ac 2) `python3 plugin/tests/run.py -p "test_steering*" -k Routing` → exit 0 · Ran 3 tests in 0.1s (1 classes, 16 at a time; slowest: Routing 0s) / OK [ran] [tree 42d15f01e07c] (2026-10-04T06:39:57Z)
- (audit intent) `one fm-reviewer pass over all five lenses (research T-0264-review-1); 3 MEDIUM + 4 LOW fixed with tests` → criteria met; review groups only change how many reviewers, every lens is still reviewed [tree 42d15f01e07c] (2026-10-04T06:39:57Z)
- (audit adversary) `one fm-reviewer pass over all five lenses (research T-0264-review-1); 3 MEDIUM + 4 LOW fixed with tests` → fixed — routing_problem validates every table (a wrong-typed file can no longer break fm), built-in skill names must be plain, the quoted words are defanged [tree 42d15f01e07c] (2026-10-04T06:39:57Z)
- (audit edge) `one fm-reviewer pass over all five lenses (research T-0264-review-1); 3 MEDIUM + 4 LOW fixed with tests` → fixed — clause-by-clause veto extraction skipping opinions, curly apostrophes in both regexes, empty-word vetoes ignored, locked writes [tree 42d15f01e07c] (2026-10-04T06:39:57Z)
- (audit operator) `one fm-reviewer pass over all five lenses (research T-0264-review-1); 3 MEDIUM + 4 LOW fixed with tests` → ok — fm vetoes list/rm to drop a stale veto; doctor skips non-folder entries in skills/ [tree 42d15f01e07c] (2026-10-04T06:39:57Z)
- (audit maintainer) `one fm-reviewer pass over all five lenses (research T-0264-review-1); 3 MEDIUM + 4 LOW fixed with tests` → ok — tests for shapes, curly quotes, clauses, dedupe and removal [tree 42d15f01e07c] (2026-10-04T06:39:57Z)
## Log
- 2026-10-04T06:29:52Z created
- 2026-10-04T06:30:20Z set tier=M
- 2026-10-04T06:30:20Z set scope=['plugin/lib/', 'plugin/tests/', 'plugin/skills/', 'mods/foreman-ui/', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-04T06:30:20Z focused
- 2026-10-04T06:39:57Z done
- 2026-10-04T06:39:57Z committed e6c4293 (15 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0260 [FEATURE M, dropped, 3 steps] Evidence quality: inconclusive runs, assumed vs verified facts, surprise log
- research brainstorm-20261004-round8: Test oracle (merges "pre-edit test oracle child", "request-to-oracle child", "compile examples in a request into the test", "fork in…
- research T-0227-review: HIGH, missing: the UI half of the request is not built. [stale: plugin/lib/fmbudget.py, plugin/lib/fmwatch.py, plugin/tests/helpers.py changed si…
- T-0262 [FEATURE M, done, 4 steps] Smarter nudges: already-covered requests, decision revisit triggers, quieter ignored hints — lesson: Text Foreman later parses for tags…
- the similar finished task took 4 steps
- likely tests for the scope: plugin/tests/test_bench.py, plugin/tests/test_budget.py, plugin/tests/test_core.py, plugin/tests/test_docs.py, plugin/tests/test_doctor.py, plugin/tests/test_evolve.py, plugin/tests/test_friction.py,…
## Lessons
- A data file an optimizer can rewrite needs a full shape validator shared by the loader and the optimizer's gate; checking only top-level keys lets one wrong type take down every command
## Files touched
- plugin/tests/test_steering.py
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- plugin/skills/routing.json
- plugin/lib/fmcli.py
- plugin/lib/fmplugins.py
- plugin/lib/fmevolve.py
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/types/index.d.ts
- plugin/lib/fmwatch.py
- plugin/tests/test_ui.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmdoctor.py
