---
id: T-2191
type: FEATURE
tier: L
status: done
priority: urgent
scope: []
depends_on: []
source: user
created: 2026-10-30T16:52:44Z
updated: 2026-10-30T19:09:04Z
base: e09f12f0a2c01d4608438c206da5a3c180a4e3db
base_tree: be31ccd6d06a025ef0e28bf243d9dc2e7188bc74
plan0_at: 2026-10-30T18:54:21Z
plan0_scope: []
verified: strong
---
# The user's standing intent (steer 2026-10-30 #7, STANDING INTENT): file it in the tower…
## Raw request
> FEATURE!: The user's standing intent (steer 2026-10-30 #7, STANDING INTENT): file it in the tower as the user's standing intent read by every cold read and seed (fm genesis charter / spec.md), on top of every earlier steer and under gen-0, for every project fm genesis runs on; make it a default of fm genesis draft (a drafted gen-0 for any repo carries it); add it to #13's exam (drafts and generations are graded on it). The intent: a harness that figures out and does everything itself; the user's only jobs are gen-0's goals and yes to what leaves the machine or touches protected core; every steer is a miss to learn from. 1 anticipate (generalize each steer's pattern; before filing a tower doc ask what he'd say and act first; more ambitious, complete, general, honest, less hand-holding); 2 act, don't advise (a capability counts only when real sessions use it by default); 3 next-level, not polish (tier 3-4 first, one moonshot a generation, nothing killed for ambition, failures to not-yet and retried); 4 complete, the frame grows; 5 general (ecosystem tools, structure-aware parsing, runtime signals over hand-written rules); 6 truth over self-image (signals Foreman didn't author; a check that measures format is a bug); 7 spend where it decides something; 8 every lesson becomes code (rule plus check, same task); 9 never trade safety for autonomy
## Interpretation
Steer 2026-10-30 #7, the user's STANDING INTENT: it supersedes nothing in gen-0, sits on top of every earlier steer, and applies to every project fm genesis runs on, not just Foreman. Three homes: (1) the charter every cold read and seed sees (_charter gets a <standing-intent> block beside <gen-0> and <user-steers>, and spec.md quotes it), so 'what would he say if he read this now?' is asked by the reader of every tower file; (2) fm genesis draft's gen-0 template carries it as a section, so any repo's drafted gen-0 starts from it (the user still confirms gen-0); (3) #13's exam grades drafts (it is in the draft) and generations (a tower doc that breaks a clause fails its cold read). The text ships with the plugin (one file), not in one project's state. Its nine clauses map onto rules already recorded (steers 1-6) plus two new ones: anticipate (generalize each steer's pattern before filing) and act, don't advise (a capability counts only when sessions use it by default, T-2184's reach check).
## Assumptions (confidence)
## Acceptance criteria
- [x] every cold read's charter carries the standing intent in its own fenced block, and spec.md quotes it — verify with `python3 plugin/tests/run.py test_genesis`
- [x] fm genesis draft's gen-0 for any repo carries the standing intent section — verify with `python3 plugin/tests/run.py test_genesis`
- [x] #13's exam fails a draft without the standing intent, and the cold reader asks what the user would say and fails a file a clause rules out — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
Complete version: plugin/skills/genesis/references/intent.md holds the intent verbatim (one source); fmgenesis.INTENT reads it; _charter appends <standing-intent> (fenced, c.plain) so drift, put's cold read, spec and select readers see it; draft's TEMPLATE gains a '## Standing intent' section filled from INTENT; spec.md writes it under its header; #13's exam (_misses) adds a check that a drafted gen-0 carries the intent section and its nine clause names; the cold reader's prompt asks 'what would the user say if he read this now?' and fails a file a clause rules out; the §8 report's scorecard row for #13 counts it. Options: per-project tower file (rejected: the intent is for every project), into gen-0 itself on Foreman (rejected: gen-0 is sealed and the user's own text), plugin file plus charter block plus draft default (chosen). The check: tests over _charter, draft, spec and the exam's misses; a Haiku smoke of fm genesis exam on the held-out third.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: charter block, draft section, spec quote, exam miss, the reader's question
2. [x] intent.md and fmgenesis.INTENT; charter, spec and draft template
3. [x] #13's exam check and the reader's prompt; zero-token arms only (this generation's Haiku smoke runs are spent)
4. [x] the steer 7 rule gets its check; docs: MASTER, README, CHANGELOG, genesis skill, site Genesis page
## Resume here
## Docs impact
~/.claude/foreman/MASTER.md ~/.claude/foreman/README.md ~/.claude/foreman/CHANGELOG.md ~/.claude/foreman/plugin/skills/genesis/SKILL.md ~/.claude/foreman/site/genesis/genesis.js
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 90 tests in 6.9s (13 classes, 16 at a time; slowest: GenesisCheck 7s, GenesisLive 5s, GenesisSweep 5s) / FAILED (5 classes) [ran] [tree 2b9311ef5334] (2026-10-30T18:54:29Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_exam` → exit 0 · Ran 117 tests in 22.3s (23 classes, 16 at a time; slowest: ExamGen 22s, ExamAuthors 17s, GenesisCheck 15s) / OK [ran] [tree fc4adde5ca92] (2026-10-30T18:55:09Z)
- (step 3) `fm genesis exam --arm oracle --per-kind 3` → exit 0 · draft-oracle genesis-s0: 3 held out + 0 train closed of 3 (3 on what it was given) / ~/.claude/foreman/state/projects/foreman-4a056f/exam/genesis-s0/oracle [ran] [tree fc4adde5ca92] (2026-10-30T18:55:29Z)
- (step 3) `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 91 tests in 11.9s (13 classes, 16 at a time; slowest: GenesisCheck 12s, GenesisSweep 9s, GenesisLive 9s) / FAILED (3 classes) [ran] [tree 6d4aa10049db] (2026-10-30T19:02:38Z)
- (step 3) `python3 plugin/tests/run.py test_genesis test_exam` → exit 0 · Ran 118 tests in 24.3s (23 classes, 16 at a time; slowest: ExamGen 24s, ExamAuthors 18s, GenesisCheck 16s) / OK [ran] [tree 55bbc2be72b0] (2026-10-30T19:03:08Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 91 tests in 7.0s (13 classes, 16 at a time; slowest: GenesisCheck 7s, GenesisSweep 5s, GenesisLive 5s) / OK [ran] [tree 2668b8777b85] (2026-10-30T19:04:41Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 91 tests in 7.0s (13 classes, 16 at a time; slowest: GenesisCheck 7s, GenesisSweep 5s, GenesisLive 5s) / OK [ran] [tree 2668b8777b85] (2026-10-30T19:04:41Z)
- (ac 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 91 tests in 7.0s (13 classes, 16 at a time; slowest: GenesisCheck 7s, GenesisSweep 5s, GenesisLive 5s) / OK [ran] [tree 2668b8777b85] (2026-10-30T19:04:41Z)
- (step 1) `python3 plugin/tests/run.py test_genesis test_exam` → exit 0 · Ran 118 tests in 22.6s (23 classes, 16 at a time; slowest: ExamGen 22s, ExamAuthors 17s, GenesisCheck 15s) / OK [ran] [tree 2668b8777b85] (2026-10-30T19:04:41Z)
- (step 4) `python3 plugin/tests/run.py test_genesis test_exam` → exit 0 · Ran 118 tests in 22.6s (23 classes, 16 at a time; slowest: ExamGen 22s, ExamAuthors 17s, GenesisCheck 15s) / OK [ran] [tree 2668b8777b85] (2026-10-30T19:04:41Z)
- (audit intent) `one foreman:fm-reviewer pass over five lenses (research T-2191-review): 2 MEDIUM + 2 LOW fixed test-first, 1 LOW skipped with reason; oracle arm of #13 closes 3/3 held out with the intent check` → the standing intent has one source and reaches every reader (charter, drift, seed, spec, draft, site); #13 fails a draft missing any whole clause; a gen-2+ seed without it drifts; steer 7's rule check is now a passing test [tree 2668b8777b85] (2026-10-30T19:04:41Z)
- (audit edge) `one foreman:fm-reviewer pass over five lenses (research T-2191-review): 2 MEDIUM + 2 LOW fixed test-first, 1 LOW skipped with reason; oracle arm of #13 closes 3/3 held out with the intent check` → whitespace-normalised whole-clause match; clause 9 has no body; the intent file is trusted and read like genesis.md; gen-1's hand-written seed is exempt from the drift rule, later seeds are written by fm genesis seed with it [tree 2668b8777b85] (2026-10-30T19:04:41Z)
- (audit adversary) `one foreman:fm-reviewer pass over five lenses (research T-2191-review): 2 MEDIUM + 2 LOW fixed test-first, 1 LOW skipped with reason; oracle arm of #13 closes 3/3 held out with the intent check` → a tower file that tries to close <standing-intent> is fenced (tested); plain_lines in the charter; the site escapes head and rest; the intent adds no grant and lowers no guard (clause 9) [tree 2668b8777b85] (2026-10-30T19:04:41Z)
- (audit operator) `one foreman:fm-reviewer pass over five lenses (research T-2191-review): 2 MEDIUM + 2 LOW fixed test-first, 1 LOW skipped with reason; oracle arm of #13 closes 3/3 held out with the intent check` → about 430 more Haiku input tokens per cold read and drift check (roughly 13k a generation); nothing added to session start, hooks or the prompt note [tree 2668b8777b85] (2026-10-30T19:04:41Z)
- (audit maintainer) `one foreman:fm-reviewer pass over five lenses (research T-2191-review): 2 MEDIUM + 2 LOW fixed test-first, 1 LOW skipped with reason; oracle arm of #13 closes 3/3 held out with the intent check` → one source file parsed once by intent_clauses() for the exam and the site; the 'given' exemption is a single condition, untested and noted in the review [tree 2668b8777b85] (2026-10-30T19:04:41Z)
## Log
- 2026-10-30T16:52:44Z created
- 2026-10-30T16:52:51Z set priority=urgent
- 2026-10-30T16:53:41Z planned: it has criteria and steps
- 2026-10-30T18:47:12Z step 3 text: #13's exam check and the reader's prompt; Haiku smoke of fm genesis exam held out → #13's exam check and the reader's prompt; zero-token arms only (this generation's Haiku smoke runs are spent)
- 2026-10-30T18:47:12Z set approved=True
- 2026-10-30T18:47:12Z approved on the user's yes 2026-10-30: 'I approve all changes btw, you don't need to ask for my approval'
- 2026-10-30T18:54:21Z focused
- 2026-10-30T19:03:53Z guard authorization added: publish
- 2026-10-30T19:05:13Z done
- 2026-10-30T19:05:15Z committed 265c2417 (9 files)
- 2026-10-30T19:05:50Z guard authorization added: publish
- 2026-10-30T19:09:04Z publish grant used by fm ship
## Follow-ups captured
## Build vs reuse
Reuses fmgenesis._charter (the cold-read charter that already fences <gen-0> and <user-steers>), draft's gen-0 TEMPLATE, the spec.md writer, #13's exam miss check (_misses) and the READ_CHILD cold-reader prompt; the genesis skill's references/ folder holds the one new file (intent.md, the intent verbatim, one source). Nothing new is built beside them: no new verb, no new store.
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (seventh): STANDING INTENT] [check: pending T-2191] The user's standing intent (on top of every earlier steer, u…
- research draft-mission-genesis-gen1: Task: T-2093 (brief 1, fm genesis check), T-2095 (brief 2, fm genesis step), T-2099 (brief 3, fm genesis draft/spec), T-2102 (brief …
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- research mission-20261030-025317: Request: Mission 3, Genesis gen 1: #1 Initiative — Foreman finds work nobody asked for in any project (scout probes for the project, bu…
## Why not caught
steer 7 was filed as a decision with a pending check; nothing put it in front of the readers or graded drafts on it until this task
## Lessons
- A rule that says 'a format check is a bug' must not be enforced by a format check: grade the whole clause, and hold every writer (drafts and later seeds) to it mechanically, with the cold read as a second line.
## Plan gaps
- failed first: step 1 red tests: charter block, draft section, spec quote, exam miss, the reader's question
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- plugin/templates/genesis.md
- site/genesis/genesis.js
- plugin/templates/standing-intent.md
- CHANGELOG.md
- MASTER.md
- README.md
- plugin/skills/genesis/SKILL.md
