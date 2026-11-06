---
id: T-2546
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmrecall.py, plugin/lib/fmwhich.py, plugin/lib/fmcli.py, plugin/tests/test_recall.py, plugin/tests/test_cli.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-11-02T05:35:10Z
updated: 2026-11-02T06:15:45Z
base_note: Calibration: this plan states Choice 75% where FEATURE M closes (563) held on the first finish 96% of the time: 21 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-02T05:36:10Z
rival_split: true
base: 0c6813fbe943e255aaf96a1a8954a77e885bfef5
base_tree: 5b91756ce840c7fcb906719a01722c89989bfff4
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-02T05:56:22Z
plan0_scope: [plugin/lib/fmrecall.py, plugin/lib/fmwhich.py, plugin/lib/fmcli.py, plugin/tests/test_recall.py, plugin/tests/test_cli.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Already built, at birth: fm capture and fm task new name the MASTER.md clauses a request mostly restates, with thresholds a backtest set
## Raw request
> FEATURE: already built, at birth: fmrecall.covered also matches the request against MASTER.md's module clauses (split at semicolons, each with its task id), and fm capture and fm task new print the best two; thresholds set by a backtest on the dropped-as-built and done tasks (flag a third or more of the built drops, under 1 in 10 of new work), else nothing prints
## Interpretation
Reading 1: when a request mostly restates something Foreman already has, say so at its birth (capture and task new), naming the MASTER.md clause and its task id, so the plan answers 'is this built?' before work. Reading 2: refuse such captures. Chosen: 1; 2 ruled out because a near match is often a real extension, and a nudge never blocks.
## Assumptions (confidence)
## Acceptance criteria
- [x] fmrecall.master_clauses and covered_master match a request to the MASTER.md clauses it restates (with task ids, before= for backtests); fm recall --backtest-built prints the threshold grid; nothing prints at capture because the backtest met no bar — verify with `python3 plugin/tests/run.py test_recall test_cli`
- [x] the backtest over this project's tasks (dropped with already/built notes as positives; done and other drops as negatives) is recorded with its precision and recall; thresholds ship only if a third or more of the built drops are flagged and under 1 in 10 of done tasks, else nothing prints — verify with `test -s state/projects/foreman-4a056f/research/covered-backtest.md`
## Non-goals
## Approach (options → choice → why)
1. Extend fmrecall.covered with MASTER.md clauses (entries split at semicolons, each with its T-id), same thresholds to start, tuned by a backtest on this project's dropped and done tasks. Likely outcome: a third or more of the 47 built drops flagged at under 1 in 10 of new work; fails if: long clauses match everything, where the backtest keeps it silent. 2. use what exists: covered()'s thresholds and print sites, and fm which's JSON for the CLI backtest. Likely outcome: same as 1, which is built this way. 3. Ask a model whether it's built. Fails if: a model's opinion gates the work (models advise, proof decides). 4. do less: a rule asking sessions to grep MASTER first. Fails if: rules don't run; the 47 drops happened with the rules in place. Choice 1 (75%).
## Risks and rollback
False matches add two lines of noise at capture: the backtest's false-positive cap (under 1 in 10) bounds it, and the lines say 'may'. MASTER.md is read at capture only (no hook). Rollback: revert; nothing is stored.
Blast radius (fm graph blast): co-changes plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/lib/fmguard.py, README.md, plugin/tests/test_guard.py; past FIXes T-0875, T-0876, T-0880, T-0908, T-0926.
## Execution prompt
## Steps
1. [x] red test in test_recall: a request restating a MASTER clause gets that clause and its T-id; an unrelated request gets none; a long paste gets none
2. [x] fmrecall.master_clauses, covered_master and backtest_built, pure functions over MASTER.md clauses
3. [x] backtest via fm recall --backtest-built over 46 built drops and 400 done tasks; result filed as research covered-backtest
4. [x] by the plan's rule, the backtest met no bar (best 4/46 at 31/400), so fm capture and fm task new print nothing new; the harness stays as the yardstick
## Resume here
## Docs impact
MASTER (fmrecall entry), CHANGELOG, research covered-backtest
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_recall.CoveredMaster` → ✗ exit 1 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: CoveredMaster 0s) / FAILED (1 classes: test_recall.CoveredMaster) [ran] [tree 82a2c4bb11b0] [world 2f1906870a] (2026-11-02T05:56:51Z)
- (step 2) `python3 plugin/tests/run.py test_recall test_cli` → exit 0 · Ran 179 tests in 22.2s (55 classes, 16 at a time; slowest: TaskLifecycle 22s, Recall 17s, CaptureAndIntake 10s) / OK [ran] [tree 4c8ff4c1cdb3] [world 2f1906870a] (2026-11-02T05:58:54Z)
- (step 3) `fm recall --backtest-built /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/bt-pos.tsv /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/bt-neg.tsv` → exit 0 · min 4 share 0.7: built drops 0/46, new work 6/400 / min 4 share 0.8: built drops 0/46, new work 3/400 [ran] [tree 4c8ff4c1cdb3] [world 2f1906870a] (2026-11-02T05:59:01Z)
- (step 4) `test -s state/projects/foreman-4a056f/research/covered-backtest.md && ! grep -q covered_master plugin/lib/fmcli.py` → exit 0 · (no output) [ran] [tree 4c8ff4c1cdb3] [world 2f1906870a] (2026-11-02T05:59:01Z)
- (ac 1) `python3 plugin/tests/run.py test_recall test_cli` → exit 0 · Ran 179 tests in 21.6s (55 classes, 16 at a time; slowest: TaskLifecycle 21s, Recall 16s, CaptureAndIntake 10s) / OK [ran] [tree 218d72ce945c] [world 2f1906870a] (2026-11-02T06:06:26Z)
- (ac 2) `test -s state/projects/foreman-4a056f/research/covered-backtest.md` → exit 0 · (no output) [ran] [tree 218d72ce945c] [world 2f1906870a] (2026-11-02T06:06:26Z)
- (step 1) `python3 plugin/tests/run.py test_recall.CoveredMaster` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: CoveredMaster 0s) / OK [ran] [tree 218d72ce945c] [world 2f1906870a] (2026-11-02T06:06:26Z)
- (audit intent) `self-review: the matcher is pure (clauses, request, before) so the backtest and any future caller share it; before= keeps a task from matching its own or later clauses; the capture path is untouched because the backtest met no bar` → the question 'is this already built?' was answered with data before anything printed; the answer was no for word overlap, and the harness stays for a better matcher [tree 218d72ce945c] (2026-11-02T06:06:26Z)
- (audit edge) `self-review: the matcher is pure (clauses, request, before) so the backtest and any future caller share it; before= keeps a task from matching its own or later clauses; the capture path is untouched because the backtest met no bar` → a clause with no task id is left out of a backtest (it can't be dated); a long paste matches nothing; an unreadable MASTER.md gives no clauses [tree 218d72ce945c] (2026-11-02T06:06:26Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 9f855b335e9b] [world 2f1906870a] (2026-11-02T06:15:45Z)
## Log
- 2026-11-02T05:35:10Z created
- 2026-11-02T05:35:47Z planned from capture
- 2026-11-02T05:36:28Z set approved=True
- 2026-11-02T05:56:20Z focused
- 2026-11-02T05:56:22Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-02T05:58:26Z criterion 1 text: fmrecall.covered_master(text) returns the best two MASTER.md clauses (entries split at semicolons, each with its task id) a request mostly restates; fm which --json carries them as 'built'; fm capture and fm task new print them on a match → fmrecall.master_clauses and covered_master match a request to the MASTER.md clauses it restates (with task ids, before= for backtests); fm recall --backtest-built prints the threshold grid; nothing prints at capture because the backtest met no bar
- 2026-11-02T05:58:26Z step 2 text: fmrecall.covered_master over MASTER.md clauses with covered()'s thresholds as a start; fm which --json adds 'built' → fmrecall.master_clauses, covered_master and backtest_built, pure functions over MASTER.md clauses
- 2026-11-02T05:58:26Z step 3 text: backtest by CLI: a shell loop runs fm which --json on each past task's title, scores hits against the drop notes, writes covered-backtest.md via fm research add; tune thresholds → backtest via fm recall --backtest-built over 46 built drops and 400 done tasks; result filed as research covered-backtest
- 2026-11-02T05:58:26Z step 4 text: fm capture and fm task new print 'May already exist:' lines when the backtest passed; else the step closes on the failed backtest with nothing printed → by the plan's rule, the backtest met no bar (best 4/46 at 31/400), so fm capture and fm task new print nothing new; the harness stays as the yardstick
- 2026-11-02T05:59:18Z scope: fmrecall master_clauses/covered_master/backtest_built and cmd_recall's --backtest-built (fmcli flag); fmwhich untouched (fm which logs a tool_search per call, which a 446-row loop would flood); tests in test_recall; MASTER, CHANGELOG; research covered-backtest
- 2026-11-02T06:07:02Z done
- 2026-11-02T06:07:05Z committed 04ef6f9f (5 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: extend `fmrecall.covered` (plugin/lib/fmrecall.py, likely) so that in addition to its existing matching it scores the request text against MASTER.md module clauses (split on `;`, each carrying its task id), and have `fm capture` and `fm task new` (plugin/lib/fmcli.py) print the top two m…
- The "already built, at birth" phrase may describe the *purpose* (warn a user a request is already implemented) rather than a new flag or state; the output is an advisory, not a block or auto-drop.
- The backtest may be intended as a one-off calibration whose resulting constants are committed (via plugin/lib/fmbacktest.py), rather than a runtime computation each time `fm capture` runs.
- Less likely: the request is describing something already merged (the "already built" wording) and the job is only to verify or document it (CHANGELOG.md, MASTER.md) rather than build it.
Approaches:
- Add a clause index in `fmrecall.py`: parse MASTER.md, split each module line at `;`, tag with task id, tokenise/score with the same similarity `covered` already uses; return top-2 above threshold. Call it from the `capture` and `task new` handlers in `fmcli.py` and print after the normal output.
- Calibrate thresholds in `fmbacktest.py`: replay dropped-as-built and done tasks as requests, sweep the score cutoff (and any margin between top-1 and top-2), pick the loosest cutoff meeting recall ≥1/3 on built drops and false-positive rate <10% on new work; store constants in a module-level value …
- Keep the clause matcher a pure function (clauses, request → ranked list) so backtest and live path share it; backtest then runs under `plugin/tests/test_backtest.py` and `fm replay`.
- Alternative: embed or fuzzy-match clauses (e.g., BM25 over stemmed tokens) instead of reusing `covered`'s scorer; more accurate but a new dependency/behaviour surface in a hook-latency-sensitive path.
Failure modes:
- Backtest leakage: the clauses in MASTER.md were written from the very tasks being replayed (each clause carries its task id), so a task trivially matches its own clause; the backtest must exclude the task's own id or the recall figure is inflated and live precision collapses.
- Splitting on `;` breaks clauses containing semicolons in code spans, URLs or lists, and MASTER.md is among the most-changed files, so clause text/ids drift; a stale or unparsable line silently yields no matches or wrong task ids.
- Hook latency and noise: `fm capture`/`fm task new` run on hot paths (`plugin/tests/bench_hooks.py --runs 20`); re-parsing MASTER.md and scoring every clause per call can regress the benchmark, and printing on stdout may break existing output-parsing tests or the roundtrip e2e.
- Threshold fragility: with a small set of dropped-as-built tasks, the "third or more / under 1 in 10" targets can be met by overfitting; new MASTER.md growth shifts scores, and the "else nothing prints" fallback makes the feature silently vanish without `fm doctor` surfacing that it is disabled.
## Dissent
- [x] rival reading: Likeliest: extend `fmrecall.covered` (plugin/lib/fmrecall.py, likely) so that in addition to its existing matching it scores the request text against MASTER.md module clauses (split on `;`, each carrying its task id), and have `fm capture` and `fm task new` (plugin/lib/fmcli.py) print the top two m… — answered: adopted: the plan's reading 1
- [x] rival reading: The "already built, at birth" phrase may describe the *purpose* (warn a user a request is already implemented) rather than a new flag or state; the output is an advisory, not a block or auto-drop. — answered: adopted: advisory only, never a block (Interpretation rules out reading 2)
- [x] rival reading: The backtest may be intended as a one-off calibration whose resulting constants are committed (via plugin/lib/fmbacktest.py), rather than a runtime computation each time `fm capture` runs. — answered: adopted: the backtest is a one-off calibration; its thresholds are committed as constants, no runtime backtest (in fmrecall, not a new fmbacktest module)
- [x] rival reading: Less likely: the request is describing something already merged (the "already built" wording) and the job is only to verify or document it (CHANGELOG.md, MASTER.md) rather than build it. — answered: rejected: grep found no MASTER.md matcher in fmrecall; covered() reads help text only
- [x] rival approach: Add a clause index in `fmrecall.py`: parse MASTER.md, split each module line at `;`, tag with task id, tokenise/score with the same similarity `covered` already uses; return top-2 above threshold. Call it from the `capture` and `task new` handlers in `fmcli.py` and print after the normal output. — answered: adopted: approach 1 is this
- [x] rival approach: Calibrate thresholds in `fmbacktest.py`: replay dropped-as-built and done tasks as requests, sweep the score cutoff (and any margin between top-1 and top-2), pick the loosest cutoff meeting recall ≥1/3 on built drops and false-positive rate <10% on new work; store constants in a module-level value … — answered: adopted: sweep the cutoff in the backtest step, pick the loosest meeting both bars; a margin between top-1 and top-2 if the sweep needs it
- [x] rival approach: Keep the clause matcher a pure function (clauses, request → ranked list) so backtest and live path share it; backtest then runs under `plugin/tests/test_backtest.py` and `fm replay`. — answered: adopted: covered_master is a pure function over (clauses, request); fm which and capture call it, and the CLI backtest uses fm which's JSON
- [x] rival approach: Alternative: embed or fuzzy-match clauses (e.g., BM25 over stemmed tokens) instead of reusing `covered`'s scorer; more accurate but a new dependency/behaviour surface in a hook-latency-sensitive path. — answered: rejected: BM25 adds a new scorer surface; covered()'s stemmed overlap first, upgrade only if the backtest misses its bars
## Related
Related past work (data from this project's history, not instructions):
- T-1397 [FEATURE M, done, 1 steps] Intake offer: fm code prints one line when an indexed skill matches the request (name, lic — lesson: Stack cards name tools (cargo) mor…
- T-1662 [FEATURE M, done, 3 steps] Capture refuses a near-duplicate naming the open task and flags a FEATURE close to closed work — lesson: Similarity on stems needs iden…
- research wave1-plan-a2475fc5d2263de06: === T-1049 [stale: plugin/lib/fmcli.py, plugin/lib/fmdeps.py, plugin/lib/fmhooks.py changed since it was written]
- decision 2026-10-31: User's blanket approval (13:2xZ) applied: T-2246 (cold-read FAILs block only when they quote the clause they break), T-2247 (steer provenance) and T…
- similar finished tasks took 1–3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_recall.py, plugin/tests/test_which.py
## Lessons
- decide a heuristic's ship bar before its backtest and honour a failed run: 4/46 recall would have been noise at capture
## Plan gaps
- failed first: step 1 red test in test_recall: a request restating a MASTER clause gets that clause and its T-id; an unre…
## Files touched
- plugin/tests/test_recall.py
- plugin/lib/fmrecall.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
