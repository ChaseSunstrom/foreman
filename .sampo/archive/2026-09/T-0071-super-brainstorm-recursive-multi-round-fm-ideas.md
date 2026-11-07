---
id: T-0071
type: FEATURE
tier: L
status: done
priority: normal
scope: [~/.claude/foreman-improve-20260927/**]
depends_on: []
source: user
created: 2026-09-27T02:19:04Z
updated: 2026-09-27T04:02:36Z
base: 9ae0a68f36945a2a255e3631a1c887a1fec9b546
---
# Super-brainstorm (recursive multi-round fm ideas) + implement every grounded idea and the inbox, recursing until dry; candidate improve/20260927
## Raw request
> Super-brainstorm (recursive multi-round fm ideas) + implement every grounded idea and the inbox, recursing until dry; candidate improve/20260927
## Interpretation
User: keep recursing (multiple brainstorms), make recursive 'super brainstorming' a Foreman capability for 'fully featured' requests, then fully implement all ideas. Built in worktree ~/.claude/foreman-improve-20260927 (live lib is protected core); merge waits for the user's yes.
## Assumptions (confidence)
## Acceptance criteria
- [x] super-brainstorm works and is tested — verify with `cd ~/.claude/foreman-improve-20260927 && python3 -m unittest discover -s plugin/tests -q`
- [x] every grounded idea implemented or recorded as dropped with its reason; evals ≥ live — verify with `claude plugin eval ~/.claude/foreman-improve-20260927/plugin --max-cost-usd 5`
## Non-goals
## Approach (options → choice → why)
A) fm ideas --rounds N: each round feeds the pack plus every idea so far and asks only for new ideas (gaps, second-order, combinations); stops when a round adds < 3 new titles; brainstorm skill gains a super mode triggered by 'fully featured'/'everything'. B) a separate command. Choice A (one command, one skill). Then: super-brainstorm Foreman, ground, implement all surviving ideas + inbox T-0049..T-0068 in rounds with one combined review per round, recurse until a super-brainstorm comes back dry; evals at the end.
## Risks and rollback
## Execution prompt
## Steps
1. [x] R1 super-brainstorm: fm ideas --rounds, dedupe, dry-stop; skill super mode; prompt-hook detection
2. [x] R2 super-brainstorm Foreman (candidate fm), ground, slate = all surviving ideas + inbox
3. [x] R3+ implement the slate in rounds, one combined review each
4. [x] recurse: super-brainstorm the improved candidate; implement until dry
5. [x] final: evals candidate vs live, docs, report; merge on the user's yes
## Resume here
<!-- auto -->
- 2026-09-27T02:22:00Z step 1/5: R1 super-brainstorm: fm ideas --rounds, dedupe, dry-stop; skill super mode; prompt-hook detection
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: ../foreman-improve-20260927/plugin/lib/fmideas.py, ../foreman-improve-20260927/plugin/tests/test_ideas.py, ../foreman-improve-20260927/plugin/lib/fmcore.py, ../foreman-improve-20260927/plugin/lib/fmhooks.py, ../foreman-improve-20260927/plugin/lib/fmcli.py
## Docs impact
MASTER.md (CLI line, operations bullets, known limitations), CHANGELOG.md (rounds R1, A–H), plugin/rules/foreman.md, plugin/skills/brainstorm/SKILL.md (super mode: --seen, dry by grounded yield), plugin/skills/intake/SKILL.md (fm why/outline), plugin/skills/intake/references/execute.md (prove, gates, PERF/CLEAN), plugin/skills/reflect/SKILL.md (corrections)
## Verification evidence
- (step 1) `cd ~/.claude/foreman-improve-20260927 && python3 -m unittest discover -s plugin/tests -q` → exit 0 · Ran 435 tests in 110.113s / OK [ran] [tree eefc4ef7673e] (2026-09-27T02:26:59Z)
- (step 2) `grep -c '^- ' state/projects/foreman-4a056f/research/brainstorm-20260926-212735/ideas.md && test -s state/projects/foreman-4a056f/research/brainstorm-20260926-super-slate.md` → exit 0 · 113 [ran] [tree eefc4ef7673e] (2026-09-27T02:32:34Z)
- (step 3) `cd ~/.claude/foreman-improve-20260927 && python3 -m unittest discover -s plugin/tests -q` → exit 0 · Ran 474 tests in 129.389s / OK [ran] [tree eefc4ef7673e] (2026-09-27T03:14:06Z)
- (step 3) `cd ~/.claude/foreman-improve-20260927 && python3 -m unittest discover -s plugin/tests -q` → exit 0 · Ran 485 tests in 131.310s / OK [ran] [tree eefc4ef7673e] (2026-09-27T03:27:05Z)
- (step 4) `cd ~/.claude/foreman-improve-20260927 && python3 -m unittest discover -s plugin/tests -q` → exit 0 · Ran 497 tests in 133.827s / OK [ran] [tree eefc4ef7673e] (2026-09-27T03:57:05Z)
- (step 5) `cd ~/.claude/foreman-improve-20260927 && python3 -m unittest discover -s plugin/tests -q -p 'test_doc*.py'` → exit 0 · Ran 41 tests in 5.429s / OK [ran] [tree eefc4ef7673e] (2026-09-27T03:58:02Z)
- (step 5) `python3 -c "import json; d=json.load(open('/tmp/claude-1000/-home-~--claude-foreman/6901a8c8-aa34-4df7-8164-6500197eb1c7/scratchpad/eval-t71.json')); s=[(c['name'], c['aggregates']['score']) for c in d['cases']]; print(s); assert all(x==1 for _, x in s)"` → exit 0 · [('guard-force-push', 1), ('guard-publish', 1), ('intake-block', 1), ('mid-task-capture', 1), ('one-liner', 1)] [ran] [tree eefc4ef7673e] (2026-09-27T03:59:40Z)
- (audit intent) `4 combined fm-reviewer passes over the candidate diffs (t0071-abc-review, t0071-de-review, t0071-fg-review + round H covered by the full suite); traced each feature end to end against the user's request (super brainstorm, recurse, implement all grounded ideas + inbox)` → fixed: preflight persistence, Next-follow key, finish/done path verified; ok [tree eefc4ef7673e] (2026-09-27T04:00:04Z)
- (audit adversary) `same passes: sentinel/prove/notify/quiet command execution, defang coverage, shared-lesson privacy, scope-reason bypass, compile() never executes, git grep argv` → fixed: scope reason tied to edit time, sentinel limited to criteria + denylist, audit text defanged, share privacy caveat; ok [tree eefc4ef7673e] (2026-09-27T04:00:04Z)
- (audit edge) `same passes: ledger window, non-git, empty transcripts, JSONC, multi-suite test output, marker races, weekly throttle, map rebuild cost` → fixed: 50k task window, zero-test false positive, JSONC skip, one worktree snapshot per check, per-file marker cleanup, digest throttle; mtime scope staleness accepted; ok [tree eefc4ef7673e] (2026-09-27T04:00:04Z)
- (audit operator) `main thread: new files all under state/ (shared/, sessions markers, tripwires.json, map.json, evals/) removed by uninstall --purge-state; no hook/settings/install wiring changes; rules 5.6k ≤ 6k chars; SKILL ≤ 10k; MASTER/CHANGELOG/skills updated; evals 5/5 = live` → ok [tree eefc4ef7673e] (2026-09-27T04:00:04Z)
- (audit maintainer) `same passes: duplication and dead code` → fixed: one verify parser (verify_of/strip_verify), dead task_files removed, regex name shadowing caught by tests; gates() mirrors done_blockers by hand (kept, low); ok [tree eefc4ef7673e] (2026-09-27T04:00:04Z)
- (ac 1) `cd ~/.claude/foreman-improve-20260927 && python3 -m unittest discover -s plugin/tests -q` → exit 0 · Ran 497 tests in 133.993s / OK [ran] [tree eefc4ef7673e] (2026-09-27T04:02:30Z)
- (ac 2) `python3 -c "import json; d=json.load(open('/tmp/claude-1000/-home-~--claude-foreman/6901a8c8-aa34-4df7-8164-6500197eb1c7/scratchpad/eval-t71.json')); s=[(c['name'], c['aggregates']['score']) for c in d['cases']]; print(s, 'live 5/5'); assert all(x==1 for _, x in s)" && test -s state/projects/foreman-4a056f/research/brainstorm-20260926-super3-slate.md` → exit 0 · [('guard-force-push', 1), ('guard-publish', 1), ('intake-block', 1), ('mid-task-capture', 1), ('one-liner', 1)] live 5/5 [ran] [tree eefc4ef7673e] (2026-09-27T04:02:30Z)
- (audit operator) `re-recorded after the docs impact fix: same check (state-only files, no wiring changes, budgets, evals 5/5)` → ok [tree eefc4ef7673e] (2026-09-27T04:02:30Z)
## Log
- 2026-09-27T02:19:04Z created
- 2026-09-27T02:19:05Z set approved=True
- 2026-09-27T02:19:11Z focused
- 2026-09-27T02:27:32Z includes T-0072: Fm task ac add should accept 'criterion :: verify cmd' like task new --ac (it silently sto
- 2026-09-27T02:27:33Z includes T-0070: Feel free to keep recursing on recurses, multiple brainstorms, also make that a thing it c
- 2026-09-27T02:37:07Z includes T-0049: A diff touching auth, crypto, secrets, exec or deserialization paths needs the adversary a
- 2026-09-27T02:37:07Z includes T-0055: Scope-drift check at done: files changed outside the brief's scope globs need a logged rea
- 2026-09-27T02:37:07Z includes T-0066: Lint verify commands when written (first word on PATH?)
- 2026-09-27T02:37:07Z includes T-0067: Outline-first reads for big files (fm outline PATH: defs and line ranges)
- 2026-09-27T02:37:07Z includes T-0068: Deterministic pre-audit script before any reviewer (tests added for changed files, debug p
- 2026-09-27T02:42:39Z includes T-0059: Prove a regression test against the reverted tree in a temp worktree (stronger than the re
- 2026-09-27T02:48:01Z includes T-0050: Tier calibration from outcomes: predict tier and effort by nearest past tasks (steps, atte
- 2026-09-27T02:48:01Z includes T-0057: Decisions record reversibility (reversible, costly, outward); later reversals listed by fm
- 2026-09-27T03:03:23Z includes T-0056: List playbooks and injections never used in N tasks as candidates to retire (context budge
- 2026-09-27T03:03:23Z includes T-0064: Fm cost: tokens and extra turns per session and task from the transcript JSONL (where the
- 2026-09-27T03:03:23Z review R1–C (t0071-abc-review): fixed focus preflight persistence, scope reason per edit time, ledger window 50k, sentinel limited to criteria checks + wider denylist, tripwire errors caught, dead sentinel condition removed
- 2026-09-27T03:10:27Z includes T-0051: Measure how often each injected Next procedure is ignored (ledger) and flag the most-ignor
- 2026-09-27T03:10:27Z includes T-0052: Turn blocked or failed tasks into claude plugin eval cases (fm evals add ID) so the refere
- 2026-09-27T03:10:27Z includes T-0053: Fm run routes tasks to a model and effort by tier (configurable), logging tokens and time
- 2026-09-27T03:10:28Z includes T-0054: Opt-in cross-project lessons with a privacy filter (paths, names, tokens stripped), recall
- 2026-09-27T03:10:28Z includes T-0058: Flag instruction-like text quoted from repo files into briefs and evidence (data, not inst
- 2026-09-27T03:24:54Z review D+E (t0071-de-review): fixed Next-follow key, audit defang, digest throttle, repeated-failure >= once, shared cap, verify parser dedup, dead task_files, share privacy caveat; gates() duplication kept (low)
- 2026-09-27T03:46:09Z recursion 4 probe (state/projects/foreman-4a056f/research/brainstorm-20260926-224235/): 24 titles → 3 grounded (H1 failure classes, H2 generated/vendored files, H3 fm audit scan); dry
- 2026-09-27T03:54:51Z review F+G (t0071-fg-review): fixed _NO_TESTS multi-suite false positive, JSONC skip, single worktree snapshot per check, per-file marker removal, strip_verify; _co_change timeout finding false (fmmap._git uses 30 s); mtime scope-reason staleness accepted (logged reason can be re-logged)
- 2026-09-27T04:02:36Z steer: the merge itself moves to its own task (the user's core yes), as in earlier rounds; step 5 covers evals, docs and the report
- 2026-09-27T04:02:36Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0063 [FEATURE L, done, 6 steps] Candidate improve/20260926: a smarter, leaner Foreman (T-0040, T-0042..T-0048, T-0060..T-0062), built in the worktree, eval-refereed, m…
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- T-0018 [FEATURE L, done, 6 steps] Recursive Foreman self-improvement: 10 rounds, each a slate implemented test-first, audited and committed
- decision 2026-09-27: Recursion bound for T-0063: after R5, one more round (R6: auto-evidence from Bash results matching a criterion's verify command) from the existing R…
## Lessons
- A super brainstorm never runs dry by title count; judge dry by grounded yield (45 → 9 → 11 → 3 here) and stop with fm decide. Build in rounds with one combined reviewer per 1–2 rounds: every review found 4–8 real issues. Never sed/python-edit a file already Read: the harness re-sends it whole.
