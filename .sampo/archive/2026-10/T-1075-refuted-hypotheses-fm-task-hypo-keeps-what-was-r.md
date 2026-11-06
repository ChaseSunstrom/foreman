---
id: T-1075
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/agents/fm-debugger.md, plugin/tests/test_diagnosis.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T05:25:39Z
base: 2794eee495cfd747a623b8f0eaba108764d1e2d9
base_tree: 2420eb7cdac04842d77a3c1bc78a07a81dfc6a75
verified: strong
---
# Refuted hypotheses: fm task hypo keeps what was ruled out and why; a debugger subagent and
## Raw request
> FEATURE: Refuted hypotheses: fm task hypo keeps what was ruled out and why; a debugger subagent and the next session read it first (wild C19)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
`fm task hypo ID mark N ruled-out --why "<reason>"` keeps the reason beside the ruled-out claim. `fm task hypo ID ruled` lists this task's refuted hypotheses and those of related tasks (same scope files). The next session sees them on resume, and the fm-debugger gets them first. The per-task ledger, probes and `mark` already exist (`task_hypo`, fmcli.py:301; `Brief.mark_hypothesis`, fmcore.py:1092). `fmcore.ruled_out` (fmcore.py:2979) feeds resume lines but reads only Log lines, not Hypotheses.
## Assumptions (confidence)
## Acceptance criteria
- [x] ruled-out with a reason is stored and shown, and `ruled` lists related tasks' refutations — verify with `python3 plugin/tests/run.py test_diagnosis`
- [x] The resume lines include refuted hypotheses, and the debugger agent file names the read-first step — verify with `python3 plugin/tests/run.py test_diagnosis test_handoff test_doctor`
## Non-goals
## Approach (options → choice → why)
(a) a new project-wide ruled-out file; (b) derive from the briefs' Hypotheses sections; (c) log lines only. Choose (b): no new storage, and it survives archive. - Add `--why` to the `hypo` parser (fmcli.py:4237). `mark_hypothesis` takes `why` and stores ` · why: …` (stripped on re-mark like `ran`). - Add `fmcore.refuted(p, b)` returning `[(task, n, claim, why)]` from `b` and from other briefs with overlapping scope or the same files, capped at 8. - `ruled_out()` uses it, so checkpoint resume lines and SessionStart carry it. - `task_hypo` gains action `ruled`, with `--write` creating `<p.dir>/handoffs/<ID>-ruled-out.md`. The stuck-rung nudges (fmcore.py:2387-2390) and fmrecall.py:353 point at it. - `plugin/agents/fm-debugger.md` step 0 reads that file first. The agent has only Read, Grep and Glob, so the main thread writes the file and names it in the brief.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: `mark 1 ruled-out --why X` shows "why: X" in the brief and in `hypo ruled` output; a second task on the same scope sees it; `ruled --write` creates the file; the checkpoint resume text contains "ruled out"; the fm-debugger.md text mentions `ruled-out.md`.
2. [x] Implement and update the agent prompt and the nudges.
## Resume here
## Docs impact
CHANGELOG.md; plugin/agents/fm-debugger.md step 0
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_diagnosis` → ✗ exit 1 · Ran 8 tests in 6.0s (6 classes, 16 at a time; slowest: WhyNotCaught 5s, Ladder 3s, Fingerprint 2s) / FAILED (1 classes) [ran] [tree a988ae892651] (2026-10-16T05:00:10Z)
- (step 2) `python3 plugin/tests/run.py test_diagnosis test_handoff test_doctor` → exit 0 · Ran 59 tests in 19.4s (26 classes, 16 at a time; slowest: Command 19s, ViewsRepair 14s, Tour 4s) / OK [ran] [tree dc13f98491f6] (2026-10-16T05:03:14Z)
- (ac 1) `python3 plugin/tests/run.py test_diagnosis` → exit 0 · Ran 8 tests in 1.9s (6 classes, 16 at a time; slowest: WhyNotCaught 2s, Refuted 1s, Ladder 1s) / OK [ran] [tree dc13f98491f6] (2026-10-16T05:03:19Z)
- (ac 2) `python3 plugin/tests/run.py test_diagnosis test_handoff test_doctor` → exit 0 · Ran 59 tests in 18.7s (26 classes, 16 at a time; slowest: Command 19s, ViewsRepair 13s, Tour 4s) / OK [ran] [tree dc13f98491f6] (2026-10-16T05:03:38Z)
- (step 1) `python3 plugin/tests/run.py test_diagnosis` → ✗ exit 1 · Ran 11 tests in 9.4s (6 classes, 16 at a time; slowest: Refuted 9s, WhyNotCaught 5s, Ladder 4s) / FAILED (1 classes) [ran] [tree 0a95bae26e8a] (2026-10-16T05:10:14Z)
- (step 2) `python3 plugin/tests/run.py test_diagnosis test_handoff test_doctor` → exit 0 · Ran 62 tests in 17.9s (26 classes, 16 at a time; slowest: Command 18s, ViewsRepair 12s, Refuted 4s) / OK [ran] [tree 7a577c8da761] (2026-10-16T05:13:32Z)
- (ac 1) `python3 plugin/tests/run.py test_diagnosis` → exit 0 · Ran 11 tests in 3.2s (6 classes, 16 at a time; slowest: Refuted 3s, WhyNotCaught 1s, Ladder 1s) / OK [ran] [tree 7a577c8da761] (2026-10-16T05:13:36Z)
- (ac 2) `python3 plugin/tests/run.py test_diagnosis test_handoff test_doctor` → exit 0 · Ran 62 tests in 17.4s (26 classes, 16 at a time; slowest: Command 17s, ViewsRepair 12s, Refuted 4s) / OK [ran] [tree 7a577c8da761] (2026-10-16T05:13:53Z)
- (ac 1) `python3 plugin/tests/run.py test_diagnosis` → exit 0 · Ran 11 tests in 4.0s (6 classes, 16 at a time; slowest: Refuted 4s, WhyNotCaught 2s, Ladder 1s) / OK [ran] [tree 74f8308375d4] (2026-10-16T05:25:06Z)
- (ac 2) `python3 plugin/tests/run.py test_diagnosis test_handoff test_doctor` → exit 0 · Ran 66 tests in 26.6s (26 classes, 16 at a time; slowest: Command 26s, ViewsRepair 19s, Refuted 4s) / OK [ran] [tree 74f8308375d4] (2026-10-16T05:25:06Z)
- (audit intent) `review: one fm-reviewer pass on the builder diff, 4 findings fixed by the builder test-first (defang + data label, separators, scan bound, ranking/age)` → a refuted hypothesis keeps its why and reaches the next attempt (resume lines, handoff file, fm-debugger step 0) [tree 74f8308375d4] (2026-10-16T05:25:06Z)
- (audit adversary) `review: one fm-reviewer pass on the builder diff, 4 findings fixed by the builder test-first (defang + data label, separators, scan bound, ranking/age)` → cross-task claim/why text is plained and defanged and labelled as quoted data in both outputs [tree 74f8308375d4] (2026-10-16T05:25:06Z)
- (audit edge) `review: one fm-reviewer pass on the builder diff, 4 findings fixed by the builder test-first (defang + data label, separators, scan bound, ranking/age)` → ' · why: ' and ' · ran `' inside claims are rewritten so they can't split a line; scan bounded to the newest 300 briefs [tree 74f8308375d4] (2026-10-16T05:25:06Z)
- (audit operator) `review: one fm-reviewer pass on the builder diff, 4 findings fixed by the builder test-first (defang + data label, separators, scan bound, ranking/age)` → 6 ms on 1,109 briefs; age shown per line [tree 74f8308375d4] (2026-10-16T05:25:06Z)
- (audit maintainer) `review: one fm-reviewer pass on the builder diff, 4 findings fixed by the builder test-first (defang + data label, separators, scan bound, ranking/age)` → _refuted_in/refuted_line/refuted in fmcore; age is the brief's last update, not the mark time (noted) [tree 74f8308375d4] (2026-10-16T05:25:06Z)
- `python3 plugin/tests/run.py test_diagnosis test_handoff test_doctor` → exit 0 · Ran 66 tests in 25.8s (26 classes, 16 at a time; slowest: Command 26s, ViewsRepair 18s, Refuted 5s) / OK [ran] [tree 74f8308375d4] (2026-10-16T05:25:38Z)
- (audit intent) `review: one fm-reviewer pass on the builder diff, 4 findings fixed by the builder test-first (defang + data label, separators, scan bound, ranking/age)` → a refuted hypothesis keeps its why and reaches the next attempt (resume lines, handoff file, fm-debugger step 0) [tree 74f8308375d4] (2026-10-16T05:25:38Z)
- (audit adversary) `review: one fm-reviewer pass on the builder diff, 4 findings fixed by the builder test-first (defang + data label, separators, scan bound, ranking/age)` → cross-task claim/why text is plained and defanged and labelled as quoted data in both outputs [tree 74f8308375d4] (2026-10-16T05:25:38Z)
- (audit edge) `review: one fm-reviewer pass on the builder diff, 4 findings fixed by the builder test-first (defang + data label, separators, scan bound, ranking/age)` → ' · why: ' and ' · ran `' inside claims are rewritten so they can't split a line; scan bounded to the newest 300 briefs [tree 74f8308375d4] (2026-10-16T05:25:38Z)
- (audit operator) `review: one fm-reviewer pass on the builder diff, 4 findings fixed by the builder test-first (defang + data label, separators, scan bound, ranking/age)` → 6 ms on 1,109 briefs; age shown per line [tree 74f8308375d4] (2026-10-16T05:25:38Z)
- (audit maintainer) `review: one fm-reviewer pass on the builder diff, 4 findings fixed by the builder test-first (defang + data label, separators, scan bound, ranking/age)` → _refuted_in/refuted_line/refuted in fmcore; age is the brief's last update, not the mark time (noted) [tree 74f8308375d4] (2026-10-16T05:25:38Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T04:22:39Z set scope=['plugin/lib/fmcore.py', 'plugin/lib/fmcli.py', 'plugin/agents/fm-debugger.md', 'plugin/tests/test_diagnosis.py']
- 2026-10-16T04:22:39Z set tier=M
- 2026-10-16T04:58:20Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1075.builder.md
- 2026-10-16T04:58:36Z focused
- 2026-10-16T05:01:38Z scope: plugin/lib/fmrecall.py — the brief's approach names its thrash nudge (fmrecall.py:353) as a pointer to hypo ruled
- 2026-10-16T05:01:57Z scope: plugin/skills/intake/references/debugging.md — docs for --why and hypo ruled --write
- 2026-10-16T05:13:14Z timing: refuted() on the real state (1109 briefs, T-1075's 4-path scope): 6 ms scanning the newest 300 by id, 14 ms scanning all; 0 rows (no brief here has a [ruled out] hypothesis yet)
- 2026-10-16T05:24:24Z merged worktree-agent-ad8af13d54faab895 (6 file(s))
- 2026-10-16T05:24:27Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad8af13d54faab895
- 2026-10-16T05:24:27Z focused
- 2026-10-16T05:24:35Z scope: CHANGELOG.md — release note for the merged builder work
- 2026-10-16T05:25:38Z done
- 2026-10-16T05:25:39Z committed 7fc55bd (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1076 [FEATURE M, active, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- T-1077 [CLEAN S, active, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged
- decision 2026-10-16: T-1054: every wild cluster (23) plus the earlier catalogue's skips became briefs T-1057..T-1087; the forever loop (T-1057) goes first after the demo…
- the similar finished task took 2 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/agents/fm-debugger.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_diagnosis.py; re-ground the plan against them before editing
## Lessons
- Text one task's brief quotes into another task's prompt is untrusted: plain, defang and label it at the point it crosses
## Plan gaps
- failed first: step 1 Failing tests: `mark 1 ruled-out --why X` shows "why: X" in the brief and in `hypo ruled` output; a…
## Files touched
- plugin/tests/test_diagnosis.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/lib/fmrecall.py
- plugin/agents/fm-debugger.md
- plugin/skills/intake/references/debugging.md
- CHANGELOG.md
