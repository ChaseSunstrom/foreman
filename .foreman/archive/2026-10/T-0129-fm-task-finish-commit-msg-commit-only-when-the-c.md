---
id: T-0129
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-03T04:44:01Z
updated: 2026-10-03T05:24:10Z
base: 72acf213043b41ab6fb7310e5eb421c67387606b
base_tree: ccad6119c6763dac0e6bbf8abe7852076d31f4c2
verified: strong
---
# fm task finish --commit: commit the task's own files only after a successful close; S --audit always counts as self
## Raw request
> fm task finish --commit '<msg>': commit only when the close succeeded (a piped finish && git commit committed after a refused close, twice this session)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] refused close commits nothing; success commits only the task's files — verify with `python3 plugin/tests/run.py -p test_round_i.py`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, --commit, self audit for S
## Resume here
## Docs impact
plugin/rules/foreman.md, plugin/skills/next/SKILL.md, CHANGELOG.md: --commit
## Verification evidence
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py` → exit 0 · 5 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.9    32.2     150  [0] / SessionEnd                  29.1    31.3     150  [0]; claude plugin test mods/foreman-ui → exit 0 · 0 fail / Ran 37 tests across 1 file. [1.76s]; python3 plugin/tests/run.py → exit 0 · Ran 540 tests in 18.5s (1 [ran] [tree b10f4fd1c7ff] (2026-10-03T05:23:56Z)
- (ac 1) `python3 plugin/tests/run.py -p test_round_i.py` → exit 0 · Ran 9 tests in 3.3s (1 classes, 16 at a time; slowest: RoundI 3s) / OK [ran] [tree b10f4fd1c7ff] (2026-10-03T05:24:03Z)
- (step 1) `python3 plugin/tests/run.py -p test_round_i.py` → exit 0 · Ran 9 tests in 3.3s (1 classes, 16 at a time; slowest: RoundI 3s) / OK [ran] [tree b10f4fd1c7ff] (2026-10-03T05:24:03Z)
- (audit self) `self: refused close commits nothing (tested); only snapshot-diff files staged; commit failure is reported after done` → no findings [tree b10f4fd1c7ff] (2026-10-03T05:24:03Z)
- (audit adversary) `self: refused close commits nothing (tested); only snapshot-diff files staged; commit failure is reported after done` → the guard-* eval prompts only re-embed the rules text (sync_evals); --commit stages paths from git's own diff, never shell-expanded [tree b10f4fd1c7ff] (2026-10-03T05:24:10Z)
- (audit self) `self: refused close commits nothing (tested); only snapshot-diff files staged; commit failure is reported after done` → no findings [tree b10f4fd1c7ff] (2026-10-03T05:24:10Z)
## Log
- 2026-10-03T04:44:01Z created
- 2026-10-03T05:22:21Z planned from capture
- 2026-10-03T05:22:21Z focused
- 2026-10-03T05:24:10Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0018-final-intent: HIGH — round 6 shipped with no recorded reviewer audit — `research/` (missing `t0018-r6-*` files) vs `tasks/T-0018-...md:81`.
- research t0018-final-operator: Not directly related. I have sufficient evidence now. Let me finalize.
- research t0018-r6-r7-adversary-edge: MEDIUM** — EDGE lens — `~/.claude/foreman/plugin/lib/fmhooks.py:360-364` vs `~/.claude/foreman/plugin/lib/fmcore…
- research T-0078-review: Verdict: changes needed (one MEDIUM, fail-open, plus a LOW).** `~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0078.diff` is …
## Files touched
- plugin/tests/test_round_i.py
- plugin/lib/fmcli.py
- plugin/skills/next/SKILL.md
- plugin/rules/foreman.md
- CHANGELOG.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
