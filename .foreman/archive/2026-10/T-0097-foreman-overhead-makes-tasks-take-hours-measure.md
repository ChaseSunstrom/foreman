---
id: T-0097
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-02T20:09:43Z
updated: 2026-10-02T22:16:03Z
base: 37ddda77d5d0fcbbfbc1d101b658afd9a1e26de5
verified: ok
---
# Find and cut where Foreman's time goes
## Raw request
> PERF: Foreman overhead makes tasks take hours; measure where the time goes (ceremony, gates, reviews) and cut it
> CONTEXT: user report from a long-running Volt session; Foreman should keep driving the queue unattended
## Interpretation
Tasks take hours; measure the split (planning, executing, gates, reviews, close-out bookkeeping) across real ledgers, then cut the biggest Foreman-caused costs.
## Assumptions (confidence)
## Acceptance criteria
- [x] a time breakdown over real ledgers, and the top Foreman costs cut with before/after numbers — verify with `python3 -m unittest discover -s plugin/tests -q`
## Non-goals
## Approach (options → choice → why)
Options: (a) measure from ledgers first, cut the top costs with before/after numbers; (b) guess and trim ceremony. Choice: (a). Why: PERF needs numbers, and the user's sessions are the data.
## Risks and rollback
## Execution prompt
## Steps
1. [x] measure: time split from ledgers
2. [x] cut the top costs
3. [x] before/after numbers, docs
## Resume here
## Docs impact
CHANGELOG.md; plugin/rules/foreman.md and plugin/skills/next/SKILL.md point at one-call finish; evals re-synced
## Verification evidence
- (step 1) `python3 ledger analysis over state/projects/*/ledger.jsonl` → 287 tasks: close-out 42 h, gates 18.8 h, 18 fm calls/task median (2026-10-02T21:59:42Z)
- (step 2) `python3 -m unittest discover -s plugin/tests -q` → all green; finish M/L + inbox drive tested (2026-10-02T21:59:42Z)
- (step 3) `fm docs` → no drift; CHANGELOG + rules + next skill updated (2026-10-02T21:59:42Z)
- (ac 1) `python3 -m unittest discover -s plugin/tests -q` → exit 0 · Ran 521 tests in 176.908s / OK [ran] [tree 06ed8f54cf00] (2026-10-02T22:13:01Z)
- (audit intent) `self-review of the diff against the ledger findings` → the measured top Foreman-side cost (close-out bookkeeping) is cut to one call, and drive no longer stops on an empty queue in full autonomy — the user's 'slow' and 'stops' complaints [tree 06ed8f54cf00] (2026-10-02T22:13:01Z)
- (audit edge) `self-review of the diff against the ledger findings` → unknown or empty lens refused before any run; a failing criterion stops before audits (existing test); standard autonomy still leaves inbox triage to the user (tested) [tree 06ed8f54cf00] (2026-10-02T22:13:01Z)
- (audit intent) `self-review of the diff against the ledger findings` → close-out bookkeeping cut to one call; drive works inbox requests in full autonomy [tree 06ed8f54cf00] (2026-10-02T22:16:03Z)
- (audit edge) `self-review of the diff against the ledger findings` → unknown or empty lens refused before any run; failing criterion stops before audits; standard autonomy unchanged [tree 06ed8f54cf00] (2026-10-02T22:16:03Z)
- (audit adversary) `self-review of the diff against the ledger findings` → guard-* eval prompts only re-embed the rules text (sync_evals); finish records audits only after every check passed, so it can't close over a failure; drive-on-inbox never touches what needs the user's yes (waits_on_user and fm ask still gate) [tree 06ed8f54cf00] (2026-10-02T22:16:03Z)
## Log
- 2026-10-02T20:09:43Z created
- 2026-10-02T20:29:15Z planned from capture
- 2026-10-02T20:29:15Z focused
- 2026-10-02T21:55:28Z user approved core in Claude Code's permission prompt
- 2026-10-02T21:56:12Z scope: drive in full autonomy also takes captured inbox items (user: 'continue implementing everything, don't stop until complete'); rules/next skill point at one-call finish
- 2026-10-02T22:16:03Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0096 [FIX M, done, 3 steps] Drive resumes when background work finished mid-turn — lesson: A wait that depends on an event the hook might never see needs a second sign…
- playbook Context Budget (skills/playbooks/references/context/context-budget.md)
- research brainstorm-20260926-super-slate: Built under T-0071, in rounds (inbox items folded in):
- research t0023-grounding: Ledger events (this project, ~700 events): step_done 66, step_add 64, task_set 61, ac_check 58, audit 37, subagent 35,
- the similar finished task took 3 steps
- start here (files T-0096 touched): CHANGELOG.md, plugin/lib/fmhooks.py, plugin/tests/test_hooks.py
## Measurements
close-out fm calls per M task: 7–9 (evidence and ac check per criterion, two audits, docs, done) → 1 (fm task finish); across 287 real tasks the median was 18 bookkeeping fm calls per task, close-out 42 h of 125 h; gates 18.8 h (Volt cargo test median 477 s — project-side, unchanged); drive in full autonomy no longer stops with 18 inbox requests left
## Lessons
- Measure from the ledgers before cutting: the bookkeeping round-trips, not the tools, were Foreman's own cost.
## Files touched
- CHANGELOG.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- plugin/rules/foreman.md
- plugin/skills/next/SKILL.md
- plugin/tests/test_hooks.py
- plugin/tests/test_round_i.py
- plugin/tests/test_speed.py
