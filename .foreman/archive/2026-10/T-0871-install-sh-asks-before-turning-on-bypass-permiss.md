---
id: T-0871
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T14:11:37Z
updated: 2026-10-15T14:14:49Z
base: 011ff34bbe68c883e67301596dd09fafafe23291
base_tree: 28ac020d939b3b4ae557f973dd682922e610f485
verified: strong
---
# install.sh asks before turning on bypass permissions, showing what it will change; --bypass opts in without asking; no terminal keeps the current mode
## Raw request
> install.sh asks before turning on bypass permissions, showing what it will change; --bypass opts in without asking; no terminal keeps the current mode
## Interpretation
A clean-HOME install (2026-10-15) set permissions.defaultMode=bypassPermissions silently; every rival adds commands without rewriting ~/.claude. Bypass stays the recommended mode (the guard is built for it) but becomes a consented choice.
## Assumptions (confidence)
## Acceptance criteria
- [x] on a tty install asks y/N (default N) before bypassPermissions and lists the wiring; --bypass sets it without asking; with no tty and no --bypass the mode is left as it was — verify with `python3 plugin/tests/run.py test_setup`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing install.sh test, then the prompt and --bypass
## Resume here
## Docs impact
README install steps and the bypass paragraph
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_setup` → exit 0 · Ran 32 tests in 1.8s (6 classes, 16 at a time; slowest: Install 2s, Uninstall 1s, InstallScript 0s) / OK [ran] [tree 96b78ca30406] (2026-10-15T14:13:05Z)
- `python3 plugin/tests/run.py test_setup` → ✗ exit 1 · Ran 32 tests in 2.1s (6 classes, 16 at a time; slowest: Install 2s, Uninstall 1s, InstallScript 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 96b78ca30406] (2026-10-15T14:13:09Z)
- `python3 plugin/tests/run.py test_setup` → exit 0 · Ran 32 tests in 1.8s (6 classes, 16 at a time; slowest: Install 2s, Uninstall 1s, InstallScript 0s) / OK [ran] [tree 96b78ca30406] (2026-10-15T14:13:09Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  briefs               foreman-desktop-d33873: STATE.md differs from the briefs (fm tidy --apply regenerates it); foreman-improve-20260927-4cffe6: STATE.md differs from the briefs (fm tidy --apply; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 14:08 UTC; claude plugin test [ran] [tree 96b78ca30406] (2026-10-15T14:14:38Z)
- (ac 1) `python3 plugin/tests/run.py test_setup` → exit 0 · Ran 32 tests in 1.8s (6 classes, 16 at a time; slowest: Install 2s, Uninstall 1s, InstallScript 0s) / OK [ran] [tree 96b78ca30406] (2026-10-15T14:14:48Z)
- (audit intent) `self: bypass is now a three-way choice in install.sh (ask on a tty, --bypass, --no-bypass); README updated in three places; the old round-trip test opts in with --bypass` → a newcomer's install no longer changes their permission mode without a yes; the prompt says why Foreman recommends bypass and how to undo it [tree 96b78ca30406] (2026-10-15T14:14:48Z)
- (audit adversary) `self: bypass is now a three-way choice in install.sh (ask on a tty, --bypass, --no-bypass); README updated in three places; the old round-trip test opts in with --bypass` → the tty check opens /dev/tty in a subshell, so curl|bash (stdin is the script) still asks on a real terminal and never reads the script as the answer; any answer but y/yes means No; a run with no terminal (CI, piped, detached) can't be talked into bypass [tree 96b78ca30406] (2026-10-15T14:14:48Z)
- (audit self) `self: bypass is now a three-way choice in install.sh (ask on a tty, --bypass, --no-bypass); README updated in three places; the old round-trip test opts in with --bypass` → no findings [tree 96b78ca30406] (2026-10-15T14:14:48Z)
## Log
- 2026-10-15T14:11:37Z created
- 2026-10-15T14:12:08Z focused
- 2026-10-15T14:14:49Z done
- 2026-10-15T14:14:49Z committed 427b8f4 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-round4-20261015: 437 ideas (9 lenses x 4 rounds + 3 deepen rounds, past every earlier run) from new evidence: a clean-HOME newcomer install, a survey…
- research T-0338-review: Changes needed. I could not run anything (no execution tool), so each finding comes from tracing the code by hand. The two HIGH findings are bypa…
- T-0009 [FEATURE L, done, 10 steps] Autonomy: plain-chat approvals, Claude runs everything, multi-lens audits before done
- decision 2026-09-26: T-0014 permission mode: fm serve passes --permission-mode only when given; otherwise Remote Control uses the user's own defaultMode (bypass here, se…
- similar past tasks were L: consider --tier L
## Lessons
- A trust-changing default needs a yes; offering it with the reason keeps the recommended path one keystroke away
## Files touched
- plugin/tests/test_setup.py
- install.sh
- README.md
