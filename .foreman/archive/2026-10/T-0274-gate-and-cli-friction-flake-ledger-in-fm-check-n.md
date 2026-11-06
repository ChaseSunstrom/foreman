---
id: T-0274
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/, MASTER.md, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-04T07:11:27Z
updated: 2026-10-04T07:18:19Z
batch: [T-0272, T-0273]
base: fdc3f3529b78ab0fcf20686631d11562aabbc2be
base_tree: be66567c7cb0ae2df4b55273dbbc4bf64acf673f
verified: strong
---
# Gate and CLI friction: flake ledger in fm check, nearest-command help on fm typos
## Raw request
> T-0272: Flake ledger: fm check records which tests failed per run; a test that fails and then passes on the same tree is listed as flaky (the failing run still fails)
> T-0273: Typo help: an unknown fm subcommand or flag suggests the nearest real one
## Interpretation
Two frictions from this session: a gate class failed once under load and nothing recorded which; wrong fm flags cost a retry each time.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0272: a test that fails in fm check and then passes on the same tree is listed as flaky (the failing run still fails), and a known-flaky test's later failure says so — verify with `python3 plugin/tests/run.py -p "test_gate_friction*" -k Flakes`
- [x] T-0273: an unknown fm subcommand or flag names the nearest real one — verify with `python3 plugin/tests/run.py -p "test_gate_friction*" -k Typos`
## Non-goals
## Approach (options → choice → why)
Flakes: parse failing test names from each gate's output (unittest FAIL/ERROR lines, pytest FAILED, go --- FAIL, cargo test … FAILED) into the project's flakes.json as pending for (command, tree); the same command passing on the same tree turns them flaky (count, last). Never a retry or a pass: the failing run's verdict stands; fm check only adds a line. Rejected: automatic rerun (hides real races, doubles gate time). Typos: _Parser.error appends difflib.get_close_matches over the choices of an invalid choice, and over every option string of every subparser for an unrecognized flag.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Tests first: plugin/tests/test_gate_friction.py (Flakes, Typos) fail
2. [x] Implement the flake ledger in cmd_check and nearest-match errors in _Parser
3. [x] Docs: MASTER.md, CHANGELOG.md
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p "test_gate_friction*"` → ✗ exit 1 · Ran 3 tests in 0.5s (2 classes, 16 at a time; slowest: Flakes 0s, Typos 0s) / FAILED (2 classes) [ran] [tree df5ad2a4b810] (2026-10-04T07:11:51Z)
- (step 2) `python3 plugin/tests/run.py -p "test_gate_friction*"` → exit 0 · Ran 3 tests in 0.5s (2 classes, 16 at a time; slowest: Flakes 1s, Typos 0s) / OK [ran] [tree cb4ff1a6d6e1] (2026-10-04T07:13:26Z)
- (step 3) `grep -c 'T-0274' MASTER.md CHANGELOG.md` → exit 0 · MASTER.md:1 / CHANGELOG.md:1 [ran] [tree cb4ff1a6d6e1] (2026-10-04T07:13:26Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  integrity            6 repo(s) and state intact / fm doctor: OK (24 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.5    35.0     150  [0] / SessionEnd                  27.9    29.7     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 06:33 UTC; python3 plugin/tests/run.py → exit 0 · Ran 728 te [ran] [tree cb4ff1a6d6e1] (2026-10-04T07:14:15Z)
- (step 2) `fm task prove --hunks: python3 plugin/tests/run.py -p "test_gate_friction*"` → 5/6 hunks proven; unproven: plugin/lib/fmcli.py @@ -1878,0 +1884,3 @@ def lazy(module, func): [inconclusive] [ran] [tree cb4ff1a6d6e1] (2026-10-04T07:14:23Z)
- (step 2) `fm task prove --hunks: python3 plugin/tests/run.py -p "test_gate_friction*"` → exit 0 · 6/6 hunks proven [ran] [tree 770fbe9c9f7e] (2026-10-04T07:14:35Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  integrity            6 repo(s) and state intact / fm doctor: OK (24 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 07:14 UTC; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 06:33 UTC; [ran] [tree 770fbe9c9f7e] (2026-10-04T07:15:17Z)
- (step 2) `python3 plugin/tests/run.py -p "test_gate_friction*"` → exit 0 · Ran 6 tests in 0.9s (2 classes, 16 at a time; slowest: Flakes 1s, Typos 0s) / OK [ran] [tree e27054c509c8] (2026-10-04T07:17:28Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  integrity            6 repo(s) and state intact / fm doctor: OK (24 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.2    31.3     150  [0] / SessionEnd                  27.9    28.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 06:33 UTC; python3 plugin/tests/run.py → exit 0 · Ran 731 te [ran] [tree e27054c509c8] (2026-10-04T07:18:17Z)
- (ac 1) `python3 plugin/tests/run.py -p "test_gate_friction*" -k Flakes` → exit 0 · Ran 4 tests in 0.9s (1 classes, 16 at a time; slowest: Flakes 1s) / OK [ran] [tree e27054c509c8] (2026-10-04T07:18:19Z)
- (ac 2) `python3 plugin/tests/run.py -p "test_gate_friction*" -k Typos` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: Typos 0s) / OK [ran] [tree e27054c509c8] (2026-10-04T07:18:19Z)
- (audit intent) `fm-reviewer pass over all lenses (research T-0274-review-1); 2 MEDIUM + 4 LOW fixed with tests; fm task prove --hunks 6/6 (it found the untested _ARGV default first)` → criteria met; corrected the docs — T-0047's single rerun still decides the verdict [tree e27054c509c8] (2026-10-04T07:18:19Z)
- (audit adversary) `fm-reviewer pass over all lenses (research T-0274-review-1); 2 MEDIUM + 4 LOW fixed with tests; fm task prove --hunks 6/6 (it found the untested _ARGV default first)` → ok — the ledger can't change an exit code; LockTimeout caught [tree e27054c509c8] (2026-10-04T07:18:19Z)
- (audit edge) `fm-reviewer pass over all lenses (research T-0274-review-1); 2 MEDIUM + 4 LOW fixed with tests; fm task prove --hunks 6/6 (it found the untested _ARGV default first)` → fixed — dotted unittest names only, rerun-pass names recorded, damaged entries dropped singly, removed gates pruned [tree e27054c509c8] (2026-10-04T07:18:19Z)
- (audit operator) `fm-reviewer pass over all lenses (research T-0274-review-1); 2 MEDIUM + 4 LOW fixed with tests; fm task prove --hunks 6/6 (it found the untested _ARGV default first)` → fixed — flag suggestions from every command and the root (-p), deterministic order [tree e27054c509c8] (2026-10-04T07:18:19Z)
- (audit maintainer) `fm-reviewer pass over all lenses (research T-0274-review-1); 2 MEDIUM + 4 LOW fixed with tests; fm task prove --hunks 6/6 (it found the untested _ARGV default first)` → ok — note_flakes is one function; tests for each path [tree e27054c509c8] (2026-10-04T07:18:19Z)
## Log
- 2026-10-04T07:11:27Z created
- 2026-10-04T07:11:41Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmcore.py', 'plugin/tests/', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-04T07:11:41Z focused
- 2026-10-04T07:18:19Z done
- 2026-10-04T07:18:19Z committed 6379c01 (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-pass-2: Source: research/brainstorm-20261004-020314 (4 lenses × 2 rounds, past pass 1 and three earlier lists; 82 new titles). Pack: pass 1's results…
- research t0063-final-review: MEDIUM — `plugin/lib/fmcore.py:842-845` (FIX red→green requirement) and `plugin/lib/fmcli.py:71-73` (M/L lesson requirement) — the user expl…
- research T-0261-review-1: No bypass found. [stale: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmguard.py changed since it was written]
- research brainstorm-pass-1: Source: research/brainstorm-20261004-013651 (4 lenses × 3 rounds, past the four earlier idea lists; 132 new titles). Pack: the user's words, …
- likely tests for the scope: plugin/tests/test_core.py
## Lessons
- Before adding a mechanism, read how the code already handles the same event (here a rerun that turns a fail into a pass): the new feature must feed it, not contradict it in the docs
## Files touched
- plugin/tests/test_gate_friction.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- CHANGELOG.md
- MASTER.md
