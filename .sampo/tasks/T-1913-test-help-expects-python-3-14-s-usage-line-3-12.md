---
id: T-1913
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/tests/test_help.py]
depends_on: []
source: user
created: 2026-10-29T04:33:55Z
updated: 2026-10-29T04:39:56Z
base: 6e128b9daedb862c595343428a073cc3227b2fb4
base_tree: 6a12ae58f4aaaa1152bfd2d0a0c56c7516f82eca
plan0_at: 2026-10-29T04:33:56Z
plan0_scope: [plugin/tests/test_help.py]
verified: strong
---
# test_help expects Python 3.14's usage line; 3.12 prints the parent's options first
## Raw request
> test_help expects Python 3.14's usage line; 3.12 prints the parent's options first
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm help task and fm help task drop are checked by their own help text, on 3.12 and 3.14 — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_help`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] assert help text, not the usage prefix; green on 3.12 and 3.14
## Resume here
<!-- auto -->
- 2026-10-29T04:38:26Z steps 1/1 done
- git: foreman/build; 5 uncommitted: CHANGELOG.md, plugin/lib/fmcore.py, plugin/tests/test_gate_friction.py, plugin/tests/test_help.py, plugin/tests/test_site_hero.py
- touched since last checkpoint: plugin/tests/test_help.py
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_help` → red as expected (exit 1) · Ran 6 tests in 1.4s (3 classes, 16 at a time; slowest: Help 1s, PromptApprovals 1s, Rules 0s) / FAILED (1 classes) [ran] [tree 6a12ae58f4aa] (2026-10-29T04:34:02Z)
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_help` → exit 0 · Ran 6 tests in 1.0s (3 classes, 16 at a time; slowest: Help 1s, PromptApprovals 1s, Rules 0s) / OK [ran] [tree 27acd7c34cd1] (2026-10-29T04:34:16Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcore.py — commit it through a task, or git checkout it back / fm doctor: OK (48 pass, 6 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                42.5    44.5     150  [0] / SessionEnd                  36.5    40.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-u [ran] [tree 27acd7c34cd1] (2026-10-29T04:39:44Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_help` → exit 0 · Ran 6 tests in 1.0s (3 classes, 16 at a time; slowest: Help 1s, PromptApprovals 1s, Rules 0s) / OK [ran] [tree 27acd7c34cd1] (2026-10-29T04:39:51Z)
- (audit intent) `S: lenses only` → help text checked on 3.12 and 3.14 [tree 27acd7c34cd1] (2026-10-29T04:39:51Z)
- (audit edge) `S: lenses only` → words past a name still read as a question, not a usage page [tree 27acd7c34cd1] (2026-10-29T04:39:51Z)
- (audit self) `S: lenses only` → no findings [tree 27acd7c34cd1] (2026-10-29T04:39:51Z)
## Log
- 2026-10-29T04:33:55Z created
- 2026-10-29T04:33:55Z focused
- 2026-10-29T04:39:54Z done
- 2026-10-29T04:39:56Z committed dc79554a (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1635-review: Approve with nits. [stale: plugin/lib/fmscene.py, plugin/tests/test_scene.py changed since it was written]
- T-1797 [FEATURE M, done, 3 steps] CC 2.1.305-2.1.312 adoption: give fm-reviewer/fm-recon an autoCompactWindow; fm doctor poi — lesson: Subagent transcripts carry their p…
- T-0802 [FEATURE S, done, 2 steps] fm research list and fm research show NAME — lesson: when users and criteria keep reaching for a command that doesn't exist, add it
- decision 2026-10-23: T-1265: fm ideas caches the pack as the lens children's shared system text, with a warm first child, instead of fork subagents
- similar finished tasks took 2–3 steps
## Lessons
- assert a command's own help text, not argparse's usage prefix, which differs across Pythons
## Files touched
- plugin/tests/test_help.py
