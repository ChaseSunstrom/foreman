---
id: T-2146
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T10:46:44Z
updated: 2026-10-30T12:17:48Z
base: dca36dd298f5d8761f8c9d381ddb61d8f30a8d1c
base_tree: 7f06e0e0e2aa0b4ce63eca77486aa1a1a32f63e3
plan0_at: 2026-10-30T11:58:45Z
plan0_scope: []
verified: strong
---
# UserPromptSubmit runs fm clauses on multi-part prompts so the Stop clauses gate works…
## Raw request
> UserPromptSubmit runs fm clauses on multi-part prompts so the Stop clauses gate works without the agent running it
## Interpretation
A user prompt with 3–12 clauses (fmrecall.clauses) is recorded at UserPromptSubmit as meta clauses {at, open}, so the T-2138 Stop gate works without the agent running fm clauses. Tasks don't exist yet at submit, so the open list is re-accounted against tasks when read (Stop gate, fm clauses --show/--note): a clause a task now covers drops out. Sensitive projects and program-sent prompts record nothing; a 1–2 clause prompt leaves the old list alone.
## Assumptions (confidence)
## Acceptance criteria
- [x] a multi-part prompt records its clauses at submit and the Stop gate holds a done claim on the uncovered one; a task covering a clause drops it; a 2-clause prompt records nothing — verify with `python3 plugin/tests/run.py test_hooks.Stop`
## Non-goals
## Approach (options → choice → why)
Options: (a) record at submit, re-account on read (chosen: no write in Stop, which holds the lock; one function for gate and verb); (b) account at submit (wrong: tasks come later); (c) run fm clauses from the Stop hook on the transcript's last prompt (re-parses the transcript each Stop, slower). Bounds 3–12 keep terse prompts and pasted logs out.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then record at submit + re-account on read
## Resume here
<!-- auto -->
- 2026-10-30T12:05:13Z steps 1/1 done
- git: foreman/build; 5 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmhooks.py, plugin/lib/fmrecall.py, plugin/tests/test_hooks.py
- touched since last checkpoint: CHANGELOG.md, MASTER.md, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2146b.edit, plugin/lib/fmhooks.py, plugin/lib/fmrecall.py, plugin/tests/test_hooks.py
## Docs impact
MASTER.md T-2138 paragraph, CHANGELOG Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.Stop` → exit 0 · Ran 48 tests in 30.6s (1 classes, 16 at a time; slowest: Stop 30s) / OK [ran] [tree ab34939a5c8d] (2026-10-30T12:01:36Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.Stop test_request` → exit 0 · Ran 54 tests in 30.9s (7 classes, 16 at a time; slowest: Stop 31s, Reactions 2s, Steers 1s) / OK [ran] [tree f5e5b72f5e74] (2026-10-30T12:08:14Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks.Stop` → exit 0 · Ran 48 tests in 31.0s (1 classes, 16 at a time; slowest: Stop 31s) / OK [ran] [tree f5e5b72f5e74] (2026-10-30T12:08:59Z)
- (audit intent) `one fm-reviewer pass over the diff; 2 medium + 2 small findings fixed test-first; 54 Stop/request tests + test_docs green` → the Stop clauses gate now works with no fm clauses run; a task captured after the prompt covers its clause [tree f5e5b72f5e74] (2026-10-30T12:08:59Z)
- (audit edge) `one fm-reviewer pass over the diff; 2 medium + 2 small findings fixed test-first; 54 Stop/request tests + test_docs green` → slash commands, headless workers, >12 or <3 clauses and sensitive projects record nothing; 1-content-word clauses skipped [tree f5e5b72f5e74] (2026-10-30T12:08:59Z)
- (audit adversary) `one fm-reviewer pass over the diff; 2 medium + 2 small findings fixed test-first; 54 Stop/request tests + test_docs green` → clauses are c.redact'd before storage; another session's list never holds this one [tree f5e5b72f5e74] (2026-10-30T12:08:59Z)
- (audit operator) `one fm-reviewer pass over the diff; 2 medium + 2 small findings fixed test-first; 54 Stop/request tests + test_docs green` → each clause holds the stop once; fm clauses --note still clears [tree f5e5b72f5e74] (2026-10-30T12:08:59Z)
- (audit maintainer) `one fm-reviewer pass over the diff; 2 medium + 2 small findings fixed test-first; 54 Stop/request tests + test_docs green` → unaccounted() shared by the gate and fm clauses; per-clause hashes capped at 50 [tree f5e5b72f5e74] (2026-10-30T12:08:59Z)
## Log
- 2026-10-30T10:46:44Z created
- 2026-10-30T10:46:45Z noticed by an agent (research T-2138-review): have a UserPromptSubmit hook run `fm clauses` on multi-part prompts, so the gate doesn't depend on the agent opting in
- 2026-10-30T11:53:25Z planned: it has criteria and steps
- 2026-10-30T11:53:26Z set tier=M
- 2026-10-30T11:58:45Z focused
- 2026-10-30T11:58:53Z criterion 1 verify: `python3 plugin/tests/run.py test_clauses` → `python3 plugin/tests/run.py test_hooks.Stop`
- 2026-10-30T12:09:37Z done
- 2026-10-30T12:09:39Z committed 0ebbd4ac (5 files)
- 2026-10-30T12:15:08Z guard authorization added: publish
- 2026-10-30T12:17:48Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2138-review: Verdict: approve with nits.** The gate does what the acceptance criterion says. I did not run the tests. The nits below are scope and test gaps, …
- T-1879 [CLEAN M, done, 3 steps] Robustness sweep: every state-reading verb survives a malformed brief or meta (truncated f — lesson: An idempotence check compares what t…
- playbook Security Bounty Hunter (fm playbooks show security/bounty-triage)
- decision 2026-10-30: [cites: user steer 2026-10-29: COVERAGE BY GRID, NOT BY LUCK] Genesis standing rule: coverage by grid — coverage.md (fm genesis put): rows = the 13 …
- the similar finished task took 3 steps
## Lessons
- a gate keyed on a set re-fires on every subset; key each item
## Files touched
- plugin/lib/fmhooks.py
- plugin/lib/fmrecall.py
- plugin/tests/test_hooks.py
- CHANGELOG.md
- MASTER.md
