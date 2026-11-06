---
id: T-0073
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-09-27T04:02:42Z
updated: 2026-09-27T04:34:42Z
base: 9ae0a68f36945a2a255e3631a1c887a1fec9b546
verified: strong
---
# Merge candidate improve/20260927 (T-0071 super brainstorm + rounds A–H) into main and push
## Raw request
> Merge candidate improve/20260927 (T-0071 super brainstorm + rounds A–H) into main and push
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] main contains the candidate and fm check passes — verify with `git merge-base --is-ancestor improve/20260927 HEAD && fm check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fast-forward foreman/build to improve/20260927, move main, fm check, push, remove the worktree
## Resume here
## Docs impact
## Verification evidence
- (step 1) `fm check: python3 -m unittest discover -s plugin/tests -q; fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · 4 passed: python3 -m unittest discover -s plugin/tests -q → exit 0 · Ran 497 tests in 133.960s / OK; fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                29.9    31.4     150  [0] / SessionEnd                  27.4    34.0     150  [0] [ran] [tree 9e547bc9093b] (2026-09-27T04:34:24Z)
- (ac 1) `git merge-base --is-ancestor 849ee3f HEAD && git rev-parse --abbrev-ref main@{upstream} >/dev/null && test "$(git rev-parse main)" = "$(git rev-parse origin/main)"` → exit 0 · (no output) [ran] [tree 9e547bc9093b] (2026-09-27T04:34:33Z)
- (audit self) `self checklist: ff-only merge, ancestor check before moving main, gates on the merged tree, push of both branches, worktree removed` → no findings [tree 9e547bc9093b] (2026-09-27T04:34:34Z)
- (audit adversary) `the merged diff's security-sensitive code was reviewed by the adversary lens in t0071-abc-review, t0071-de-review and t0071-fg-review; findings fixed with tests; the merge adds nothing beyond that diff (ff-only)` → ok [tree 9e547bc9093b] (2026-09-27T04:34:42Z)
- (audit self) `self checklist: ff-only merge, ancestor check before moving main, gates on the merged tree, push of both branches, worktree removed` → no findings [tree 9e547bc9093b] (2026-09-27T04:34:42Z)
## Log
- 2026-09-27T04:02:42Z created
- 2026-09-27T04:02:42Z focused
- 2026-09-27T04:31:46Z user approved core in Claude Code's permission prompt
- 2026-09-27T04:34:42Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0069 [FEATURE S, done, 1 steps] Merge candidate improve/20260926 (T-0063: smarter + leaner Foreman) into foreman/build and main, push
- T-0071 [FEATURE L, done, 5 steps] Super-brainstorm (recursive multi-round fm ideas) + implement every grounded idea and the inbox, recursing until dry; candidate improve…
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- T-0063 [FEATURE L, done, 6 steps] Candidate improve/20260926: a smarter, leaner Foreman (T-0040, T-0042..T-0048, T-0060..T-0062), built in the worktree, eval-refereed, m…
## Files touched
- CHANGELOG.md
- MASTER.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmcost.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmhooks.py
- plugin/lib/fmideas.py
- plugin/lib/fmmap.py
- plugin/lib/fmrecall.py
- plugin/lib/fmserve.py
- plugin/rules/foreman.md
- plugin/skills/brainstorm/SKILL.md
- plugin/skills/intake/SKILL.md
- plugin/skills/intake/references/execute.md
- plugin/skills/reflect/SKILL.md
- plugin/tests/test_cli.py
- plugin/tests/test_diff_gates.py
- plugin/tests/test_hooks.py
- plugin/tests/test_ideas.py
- plugin/tests/test_memory.py
- plugin/tests/test_round_f.py
- plugin/tests/test_round_g.py
- plugin/tests/test_speed.py
- plugin/tests/test_unattended.py
