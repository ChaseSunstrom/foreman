---
id: T-2745
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-03T00:57:22Z
updated: 2026-11-03T02:13:53Z
builder_model: sonnet
base: 33f98a07b87307c3a86fabbed8e18bbd883c607c
base_tree: 6205133e8f1d03da313f3f5b8b2fdcdd886edd0f
plan0_at: 2026-11-03T00:57:49Z
plan0_scope: []
inferred_deps: [T-2742]
inferred_why: T-2742: named in its request
group: Sampo rename and its steps
lane_stop: merged 2026-11-03T02:12:13Z
verified: strong
---
# Ward knows Sampo: the guard treats sampo (and plugin/bin/sampo) exactly as fm, sampo* modules as fm* ones, SAMPO_STATE, SAMPO_HOME and SAMPO_CONFINE as their FOREMAN_ twins, and the new verb names as the old, then says so with KNOWS_SAMPO (T-2742, protected core: built in a lane, queued for the user's yes)
## Raw request
> Ward knows Sampo: the guard treats sampo (and plugin/bin/sampo) exactly as fm, sampo* modules as fm* ones, SAMPO_STATE, SAMPO_HOME and SAMPO_CONFINE as their FOREMAN_ twins, and the new verb names as the old, then says so with KNOWS_SAMPO (T-2742, protected core: built in a lane, queued for the user's yes)
## Interpretation
Reading 1 (chosen): before any sampo name works (T-2742), the guard must refuse under each new name what it refuses under the old: the program (sampo, plugin/bin/sampo, python .../sampo), interpreter imports of the renamed modules (sampo, sampo.*), the env twins (SAMPO_STATE, SAMPO_HOME, SAMPO_CONFINE beside FOREMAN_*), and the verb twins (rune=genesis, louhi=exam, ward=guard, smith=code, moons=genesis moonshot, underworld=the not-yet ledger). KNOWS_SAMPO = True tells the CLI it may honour them. Reading 2 (ruled out): rename the guard's own strings to sampo. Ruled out: the old names must keep being refused too; this adds twins, it renames nothing.
## Assumptions (confidence)
## Acceptance criteria
- [x] every refused fm form is refused the same way spelled with sampo (prove --yes-run, task set --allow, ask --standing, a state override, an interpreter importing sampo modules), and each allowed form stays allowed — verify with `python3 plugin/tests/run.py test_guard_sampo`
- [x] the existing guard suites pass unchanged — verify with `python3 plugin/tests/run.py test_guard test_guard_overrefusal test_guard_diff`
## Non-goals
## Approach (options → choice → why)
1. One table at the top of fmguard (FM_PROGRAMS, FM_MODULE_PREFIXES, ENV_TWINS, VERB_TWINS) and every site that keys on 'fm' reads it; a test spells each existing refused form both ways. Likely outcome: about a dozen sites read the table; no rule changes meaning. Fails if: a site matches 'fm' inside a regex or string the grep misses; the both-ways test over the existing refusal corpus catches it.
2. Rewrite sampo to fm in the command text before the guard parses it. Fails if: a rewrite of command text changes what a quoted argument says, and positions shift for the paths the guard reports.
3. Use what exists: the guard's existing refusal tests (test_guard*, test_guard_diff's FORMS) as the corpus to double. Likely outcome: no new fixtures beyond the sampo spellings.
4. Do less: only the program name. Fails if: SAMPO_STATE or an import of sampo.core would pass unseen.
Choice 1 on 3 (80%).
## Risks and rollback
A missed site is a bypass under the new name; the both-ways test over the refusal corpus is the check. It lands only on the user's yes (fm ask T-2745 core); until then plugin/bin/sampo refuses inside agent sessions. Rollback: git revert of the one commit.
## Execution prompt
## Steps
1. [x] red test: each refused fm form, spelled with sampo, SAMPO_* and the new verbs
2. [x] one name table in the guard (programs, module prefixes, env twins, verb twins) used at every site that keys on fm
3. [x] KNOWS_SAMPO = True
## Resume here
<!-- auto -->
- 2026-11-03T01:45:51Z steps 3/3 done
- git: worktree-agent-aff0dad78a11350da; 2 uncommitted: plugin/lib/fmguard.py, plugin/tests/test_guard_sampo.py
- touched since last checkpoint: plugin/lib/fmguard.py, plugin/tests/test_guard_sampo.py
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard_sampo` → exit 0 · Ran 7 tests in 1.6s (1 classes, 16 at a time; slowest: SameAsFm 1s) / OK [ran] [tree e29d0b3f53e1] [world 2f1906870a] (2026-11-03T01:00:32Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_overrefusal test_guard_diff` → exit 0 · Ran 326 tests in 9.7s (96 classes, 16 at a time; slowest: Mutation 9s, GuardAgainstBash 6s, Latency 4s) / OK [ran] [tree e29d0b3f53e1] [world 2f1906870a] (2026-11-03T01:00:42Z)
- (step 3) `python3 plugin/tests/run.py test_guard_sampo` → exit 0 · Ran 7 tests in 1.7s (1 classes, 16 at a time; slowest: SameAsFm 1s) / OK [ran] [tree e29d0b3f53e1] [world 2f1906870a] (2026-11-03T01:00:44Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_approve_reads test_guard test_guard_diff test_guard_evasions test_guard_exec_vectors test_guard_git test_guard_pipes test_guard_sampo test_settings_scopes && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.85s] [ran] [tree e29d0b3f53e1] [world 2f1906870a] (2026-11-03T01:01:11Z)
- (step 2) `python3 plugin/tests/run.py test_guard_sampo test_guard test_guard_overrefusal test_guard_diff` → exit 0 · Ran 327 tests in 9.6s (96 classes, 16 at a time; slowest: Mutation 9s, GuardAgainstBash 5s, Latency 4s) / OK [ran] [tree 8acecacc79dc] [world 2f1906870a] (2026-11-03T01:02:47Z)
- (step 2) `python3 plugin/tests/run.py test_guard_sampo test_guard test_guard_overrefusal test_guard_diff` → exit 0 · Ran 328 tests in 19.2s (96 classes, 16 at a time; slowest: Mutation 19s, GuardAgainstBash 14s, Latency 9s) / OK [ran] [tree 9c46bbf42859] [world 2f1906870a] (2026-11-03T01:46:48Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_sampo` → exit 0 · Ran 9 tests in 1.9s (1 classes, 16 at a time; slowest: SameAsFm 2s) / OK [ran] [tree 43ded16367ab] [world 2f1906870a] (2026-11-03T02:12:27Z)
- (ac 2) `python3 plugin/tests/run.py test_guard test_guard_overrefusal test_guard_diff` → exit 0 · Ran 328 tests in 11.4s (96 classes, 16 at a time; slowest: Mutation 11s, GuardAgainstBash 7s, Latency 5s) / OK [ran] [tree 43ded16367ab] [world 2f1906870a] (2026-11-03T02:12:39Z)
- (step 1) `python3 plugin/tests/run.py test_guard_sampo` → exit 0 · Ran 9 tests in 1.9s (1 classes, 16 at a time; slowest: SameAsFm 2s) / OK [ran] [tree 43ded16367ab] [world 2f1906870a] (2026-11-03T02:12:41Z)
- (step 2) `python3 plugin/tests/run.py test_guard_sampo` → exit 0 · Ran 9 tests in 1.9s (1 classes, 16 at a time; slowest: SameAsFm 2s) / OK [ran] [tree 43ded16367ab] [world 2f1906870a] (2026-11-03T02:12:44Z)
- (step 3) `python3 plugin/tests/run.py test_guard_sampo` → exit 0 · Ran 9 tests in 1.9s (1 classes, 16 at a time; slowest: SameAsFm 2s) / OK [ran] [tree 43ded16367ab] [world 2f1906870a] (2026-11-03T02:12:46Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_sampo` → exit 0 · Ran 9 tests in 2.3s (1 classes, 16 at a time; slowest: SameAsFm 2s) / OK [ran] [tree 3a5a6b8b5af6] [world 2f1906870a] (2026-11-03T02:13:22Z)
- (ac 2) `python3 plugin/tests/run.py test_guard test_guard_overrefusal test_guard_diff` → exit 0 · Ran 328 tests in 12.2s (96 classes, 16 at a time; slowest: Mutation 12s, GuardAgainstBash 7s, Trust 5s) / OK [ran] [tree 3a5a6b8b5af6] [world 2f1906870a] (2026-11-03T02:13:22Z)
- `python3 plugin/tests/run.py test_guard_sampo test_guard test_guard_overrefusal test_guard_diff` → exit 0 · Ran 328 tests in 11.8s (96 classes, 16 at a time; slowest: Mutation 11s, GuardAgainstBash 7s, Latency 5s) / OK [ran] [tree 3a5a6b8b5af6] [world 2f1906870a] (2026-11-03T02:13:22Z)
- (audit adversary) `read the merged diff: one name table (FM_PROGRAMS, FM_MODULE_PREFIXES via _sampo_name, ENV twins, VERB_TWINS, GUARD_FILES) read at every site that keyed on fm or FOREMAN_; a parity test spells the refusal corpus both ways with a floor of 40 refusals; the user approved it (fm ask core)` → a cold adversary review found no sampo form allowed while its fm twin is refused; its five parity nits (_PRE_DENY SAMPO_, .claude/sampo/state marks, GUARD_FILES for sampo/ward.py, sampo edit drafts, the .sampo mirror) are fixed and tested [tree 3a5a6b8b5af6] (2026-11-03T02:13:22Z)
- (audit edge) `read the merged diff: one name table (FM_PROGRAMS, FM_MODULE_PREFIXES via _sampo_name, ENV twins, VERB_TWINS, GUARD_FILES) read at every site that keyed on fm or FOREMAN_; a parity test spells the refusal corpus both ways with a floor of 40 refusals; the user approved it (fm ask core)` → the module twins follow T-2742's map exactly (fmguard→sampo.ward and the role names), pinned by a test [tree 3a5a6b8b5af6] (2026-11-03T02:13:22Z)
- (audit intent) `read the merged diff: one name table (FM_PROGRAMS, FM_MODULE_PREFIXES via _sampo_name, ENV twins, VERB_TWINS, GUARD_FILES) read at every site that keyed on fm or FOREMAN_; a parity test spells the refusal corpus both ways with a floor of 40 refusals; the user approved it (fm ask core)` → SAMPO.md's protected core: the guard change was built in a lane and merged only on the user's yes; no Sampo name works anywhere yet, and now each can be honoured safely [tree 3a5a6b8b5af6] (2026-11-03T02:13:22Z)
## Log
- 2026-11-03T00:57:22Z created
- 2026-11-03T00:57:37Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2745.builder.md
- 2026-11-03T00:57:49Z focused
- 2026-11-03T02:10:46Z user approved core in Claude Code's permission prompt
- 2026-11-03T02:12:13Z merged worktree-agent-aff0dad78a11350da (2 file(s))
- 2026-11-03T02:12:24Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aff0dad78a11350da
- 2026-11-03T02:12:24Z focused
- 2026-11-03T02:13:49Z done
- 2026-11-03T02:13:53Z committed 6534bc48 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, active, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; …
- decision 2026-11-03: [costly] [cites: user steer: read SAMPO.md (protected core queued for the user; nothing a user has may break)] The rename's guard step comes first: …
- T-2357 [FEATURE M, done, 3 steps] Installs are queued for one yes: night and tick timers staged, asked once, installed only after the user's yes (Mission 8, #11) — lesso…
- research mission-20261102-183526.pack: Genesis gen 4, Mission 1: #2 Exhaustive thinking. Foreman covers the whole space of a request and says what it left out. Carried g…
## Lessons
- Before renaming anything a guard matches by name, teach the guard the new name and prove parity over its whole refusal corpus; a rename is otherwise a bypass
## Files touched
- plugin/tests/test_guard_sampo.py
- plugin/lib/fmguard.py
- CHANGELOG.md
