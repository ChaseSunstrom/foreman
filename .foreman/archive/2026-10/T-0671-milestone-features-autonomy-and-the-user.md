---
id: T-0671
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:13Z
updated: 2026-10-09T16:56:18Z
batch: [T-0439, T-0461, T-0477]
base: 0c5d535ea5fb4b468566bcb1fc1c5e3792fcdcc3
base_tree: 3e5545591548078637a2ffed93080ba3fc6c9367
verified: strong
---
# Milestone: Features — Autonomy and the user
## Raw request
> T-0439: FEATURE: Taste model and user portrait (C056, value 4/5, effort M, risk med)
>   first version: First version: fm taste proposes vetoes from repeated steers for one yes, and uses the record to default fm decide answers. Skip twin runs, interviews, arenas, field notes; pre-answering approvals must never touch guard categories.
>   what it is: Learn the user's preferences from their answers, steers and edits and pre-answer asks in their style.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 15 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0461: FEATURE: Ask less, ask better (C057, value 3/5, effort S, risk low)
>   first version: First version: in standard autonomy, collect non-urgent asks into one deadline-defaulted digest (default applied at the deadline, logged via fm decide). Skip rehearsal, information-gain ordering, pre-building answers.
>   what it is: Batch asks into a deadline-defaulted digest, rehearse them, order them by information gain and treat attention as a budget.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 11 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0477: FEATURE: Capture from anywhere (C060, value 3/5, effort M, risk low)
>   first version: First version: fm capture --from-file/stdin for pasted text, logs or transcripts (with excerpt attached) plus a clipboard/selection hook in the desktop app; screenshots as attached paths. Skip voice, recordings, tweet-close-outs.
>   what it is: Capture tasks from selected text, screenshots, voice, recordings and pasted transcripts.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 11 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Do T-0439, T-0461, T-0477 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0671. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0439: Taste model and user portrait (C056, value 4/5, effort M, risk med) works — verify with `python3 plugin/tests/run.py -p test_autonomy_user.py -k TasteVetoes`
- [x] T-0461: Ask less, ask better (C057, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_autonomy_user.py -k AskDigest`
- [x] T-0477: Capture from anywhere (C060, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_autonomy_user.py -k CaptureFromFile`
## Non-goals
## Approach (options → choice → why)
One milestone, three first slices, one test file plugin/tests/test_autonomy_user.py: TasteVetoes (fm taste proposes a veto from 3+ same-shaped steers for one yes via fm ask; fm decide defaults from the record; never touches guard categories), AskDigest (standard autonomy: non-urgent asks collect into one digest with a deadline; at the deadline the default is applied and logged by fm decide), CaptureFromFile (fm capture --from-file PATH / - attaches an excerpt and the path; images as attached paths). Member tests first; per step its own class; full gates once at close.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0439: Taste model and user portrait (C056, value 4/5, effort M, risk med)
2. [x] T-0461: Ask less, ask better (C057, value 3/5, effort S, risk low)
3. [x] T-0477: Capture from anywhere (C060, value 3/5, effort M, risk low)
## Resume here
## Docs impact
CHANGELOG entry; MASTER/help unchanged (no new commands beyond the milestone's)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_autonomy_user.py -k TasteVetoes` → ✗ exit 1 · Ran 4 tests in 5.3s (1 classes, 16 at a time; slowest: TasteVetoes 5s) / FAILED (1 classes) [ran] [tree d17b6abaa2fb] (2026-10-09T16:23:12Z)
- (step 1) `python3 plugin/tests/run.py -p test_autonomy_user.py -k TasteVetoes` → exit 0 · Ran 4 tests in 3.5s (1 classes, 16 at a time; slowest: TasteVetoes 4s) / OK [ran] [tree 6be03a4f30f0] (2026-10-09T16:25:14Z)
- (step 2) `python3 plugin/tests/run.py -p test_autonomy_user.py -k AskDigest` → exit 0 · Ran 3 tests in 3.4s (1 classes, 16 at a time; slowest: AskDigest 3s) / OK [ran] [tree 3c2adedb485f] (2026-10-09T16:26:43Z)
- (step 3) `python3 plugin/tests/run.py -p test_autonomy_user.py -k CaptureFromFile` → exit 0 · Ran 4 tests in 1.7s (1 classes, 16 at a time; slowest: CaptureFromFile 2s) / OK [ran] [tree 65013d4996e8] (2026-10-09T16:27:39Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (30 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                33.3    38.3     150  [0] / SessionEnd                  30.8    34.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 13:13 UTC; python3 plugin/tests/run.py → exit 0 · Ran 1021 tests i [ran] [tree 40cce72b3b27] (2026-10-09T16:30:59Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed on this tree (run at 16:30 UTC) [ran] [tree 40cce72b3b27] (2026-10-09T16:31:05Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (30 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                33.9    38.0     150  [0] / SessionEnd                  31.1    35.6     150  [0]; claude plugin test mods/foreman-ui → exit 0 · 0 fail / Ran 62 tests across 1 file. [3.19s]; python3 plugin/tests/run.py → exit 0 · Ran 1021 tests in 54.9s (256 classes, 16 at a tim [ran] [tree 40cce72b3b27] (2026-10-09T16:32:46Z)
- (step 1) `python3 plugin/tests/run.py -p test_autonomy_user.py` → ✗ exit 1 · Ran 15 tests in 3.1s (3 classes, 16 at a time; slowest: TasteVetoes 3s, AskDigest 2s, CaptureFromFile 1s) / FAILED (3 classes) [ran] [tree 8cecc5043aae] (2026-10-09T16:55:02Z)
- (step 1) `python3 plugin/tests/run.py -p test_autonomy_user.py -k TasteVetoes` → exit 0 · Ran 6 tests in 3.5s (1 classes, 16 at a time; slowest: TasteVetoes 4s) / OK [ran] [tree 8cc7f19f207b] (2026-10-09T16:55:57Z)
- (step 2) `python3 plugin/tests/run.py -p test_autonomy_user.py -k AskDigest` → exit 0 · Ran 4 tests in 2.2s (1 classes, 16 at a time; slowest: AskDigest 2s) / OK [ran] [tree 8cc7f19f207b] (2026-10-09T16:55:59Z)
- (step 3) `python3 plugin/tests/run.py -p test_autonomy_user.py -k CaptureFromFile` → exit 0 · Ran 5 tests in 1.3s (1 classes, 16 at a time; slowest: CaptureFromFile 1s) / OK [ran] [tree 8cc7f19f207b] (2026-10-09T16:56:00Z)
- (ac 1) `python3 plugin/tests/run.py -p test_autonomy_user.py -k TasteVetoes` → exit 0 · Ran 6 tests in 3.5s (1 classes, 16 at a time; slowest: TasteVetoes 4s) / OK [ran] [tree 71a544ca0fde] (2026-10-09T16:56:18Z)
- (ac 2) `python3 plugin/tests/run.py -p test_autonomy_user.py -k AskDigest` → exit 0 · Ran 4 tests in 2.2s (1 classes, 16 at a time; slowest: AskDigest 2s) / OK [ran] [tree 71a544ca0fde] (2026-10-09T16:56:18Z)
- (ac 3) `python3 plugin/tests/run.py -p test_autonomy_user.py -k CaptureFromFile` → exit 0 · Ran 5 tests in 1.3s (1 classes, 16 at a time; slowest: CaptureFromFile 1s) / OK [ran] [tree 71a544ca0fde] (2026-10-09T16:56:18Z)
- (audit intent) `one fm-reviewer pass (all lenses) over the milestone diff; 7 findings, 6 fixed test-first, 1 accepted` → all three members' criteria met per the reviewer; per-member tests green [tree 71a544ca0fde] (2026-10-09T16:56:18Z)
- (audit adversary) `one fm-reviewer pass (all lenses) over the milestone diff; 7 findings, 6 fixed test-first, 1 accepted` → guard asks matched by exact category only (force-push, plugins slipped) → synonyms+stems; --from-file read credential files → refused via the guard's _is_credential; secrets cut before redaction → redact first; stdin unbounded → 2 MB cap [tree 71a544ca0fde] (2026-10-09T16:56:18Z)
- (audit edge) `one fm-reviewer pass (all lenses) over the milestone diff; 7 findings, 6 fixed test-first, 1 accepted` → unreadable digest deadline applied every default → not due, reset on the next ask; all options vetoed hid the veto → says so [tree 71a544ca0fde] (2026-10-09T16:56:18Z)
- (audit operator) `one fm-reviewer pass (all lenses) over the milestone diff; 7 findings, 6 fixed test-first, 1 accepted` → fm taste adopt needs no proof of the user's yes — accepted, a veto only adds caution and steers come from fm task log [tree 71a544ca0fde] (2026-10-09T16:56:18Z)
## Log
- 2026-10-09T15:40:13Z created
- 2026-10-09T16:08:40Z criterion 1 verify: `` → `python3 plugin/tests/run.py -p test_autonomy_user.py -k TasteVetoes`
- 2026-10-09T16:08:41Z criterion 2 verify: `` → `python3 plugin/tests/run.py -p test_autonomy_user.py -k AskDigest`
- 2026-10-09T16:08:41Z criterion 3 verify: `` → `python3 plugin/tests/run.py -p test_autonomy_user.py -k CaptureFromFile`
- 2026-10-09T16:08:42Z set approved=True
- 2026-10-09T16:17:16Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0671.builder.md
- 2026-10-09T16:17:32Z focused
- 2026-10-09T16:34:27Z merged worktree-agent-a856bd7968ad5edc7 (5 file(s))
- 2026-10-09T16:34:30Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a856bd7968ad5edc7
- 2026-10-09T16:34:30Z focused
- 2026-10-09T16:35:04Z paused: focus moved to T-0702
- 2026-10-09T16:54:21Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-09T16:54:21Z focused
- 2026-10-09T16:55:48Z hypothesis confirmed: synonyms/stems, credential-path refusal, redact-before-fit, unreadable-deadline reset and the all-vetoed note make the 4 new review tests pass with the 11 old ones (15 OK)
- 2026-10-09T16:56:18Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0509 [FEATURE M, dropped, 0 steps] Taste model and user portrait (C056, value 4/5, effort M, risk med)
- T-0531 [FEATURE M, dropped, 0 steps] Ask less, ask better (C057, value 3/5, effort S, risk low)
- T-0547 [FEATURE M, dropped, 0 steps] Capture from anywhere (C060, value 3/5, effort M, risk low)
- decision 2026-09-26: Full autonomy never asks mid-run but still can't grant itself core or run destructive/irreversible guard categories: those are recorded with fm ask …
## Lessons
- A guard-word filter on free text needs the verbs people actually use (push, delete), not the category ids; test the phrasing, not the label.
## Files touched
- .claude/worktrees/agent-a856bd7968ad5edc7/plugin/tests/test_autonomy_user.py
- .claude/worktrees/agent-a856bd7968ad5edc7/plugin/lib/fmcore.py
- .claude/worktrees/agent-a856bd7968ad5edc7/plugin/lib/fmideas.py
- .claude/worktrees/agent-a856bd7968ad5edc7/plugin/lib/fmcli.py
- .claude/worktrees/agent-a856bd7968ad5edc7/MASTER.md
- plugin/tests/test_autonomy_user.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmideas.py
- CHANGELOG.md
- MASTER.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- plugin/lib/fmdoctor.py
- plugin/lib/fmeco.py
- plugin/lib/fmguard.py
- plugin/lib/fmhooks.py
- plugin/lib/fmlanes.py
- plugin/rules/foreman.md
- plugin/tests/test_ecosystem.py
- plugin/tests/test_guard_pipes.py
- plugin/tests/test_safety.py
- plugin/tests/test_suite_hygiene.py
