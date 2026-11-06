---
id: T-2125
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T08:06:48Z
updated: 2026-10-30T10:01:28Z
base: fafad9f521931cf8a5d7dda813dc06d6729dc816
base_tree: ad55a3746c25402664c736712aa19bf23fb3979d
plan0_at: 2026-10-30T09:38:50Z
plan0_scope: []
verified: strong
---
# Value ranking: severity x proof x reach / effort, per-finder precision from outcomes, a mute floor, abstain below a threshold (Mission 3 brief 6)
## Raw request
> Value ranking: severity x proof x reach / effort, per-finder precision from outcomes, a mute floor, abstain below a threshold (Mission 3 brief 6)
## Interpretation
fm find --rank: each finding gets score = severity(kind) x reach / effort x precision(finder); rows print best first with the score. Precision comes from what happened to findings that became tasks: fm find --capture N files the top N as discovered tasks tagged finder=NAME; a done task that survived (fmoutcomes) counts as real, a dropped one as a false alarm; prior 0.5 over 10 cases. A finder whose precision falls under 0.3 is muted (listed as muted, not ranked). When nothing scores above the abstain threshold, the verb says so instead of ranking noise.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm find --rank orders a vuln and a bug above slow and docs, and a finder under the floor is muted — verify with `python3 plugin/tests/run.py test_find`
## Non-goals
## Approach (options → choice → why)
A: static severity table only (no learning) — rejected, no mute floor possible. B: per-finding labels kept in a find ledger — rejected, a second store beside tasks. C (chosen): tasks carry finder= meta, precision read from task fates (fmoutcomes survived/reverted + dropped) — reuses the task store and outcomes. Proof is constant for fm find (every finding is a lead) and effort is unknown before a fix, so both start at 1: ponytail ceiling, a proven finding (failing test) or a hunk-size estimate can feed them later. Reach = files that name the symbol as a whole word, capped.
## Risks and rollback
## Execution prompt
## Steps
1. [x] score + reach + --rank ordering (vuln/secret/bug above slow/docs) test-first
2. [x] --capture N with finder meta; precision from task fates; mute floor 0.3 and abstain threshold, tested with seeded tasks
3. [x] finders arm uses --rank so rank_hit can close; docs (MASTER fmfind, CHANGELOG, README fm find line)
## Resume here
<!-- auto -->
- 2026-10-30T09:50:40Z steps 3/3 done
- git: foreman/build; 7 uncommitted: CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmcli.py, plugin/lib/fmexam.py, plugin/lib/fmfind.py, plugin/tests/test_find.py
- touched since last checkpoint: plugin/lib/fmexam.py, CHANGELOG.md, MASTER.md, README.md, plugin/tests/test_find.py, plugin/lib/fmcli.py, plugin/lib/fmfind.py
## Docs impact
MASTER fmfind entry, CHANGELOG, README row
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 21 tests in 6.2s (12 classes, 16 at a time; slowest: FindCli 6s, FindRenders 5s, DryRun 1s) / OK [ran] [tree 978c06b0c1a2] (2026-10-30T09:40:24Z)
- (ac 1) `python3 plugin/tests/run.py test_find 2>&1 | grep -E "^(FAIL|ERROR|OK|Ran|FAILED)|Error:" | head -12` → ✗ exit 1 · Ran 24 tests in 6.3s (13 classes, 16 at a time; slowest: FindCli 6s, FindRenders 4s, DryRun 1s) / FAILED (1 classes) [ran] [tree e6a694fa11ca] (2026-10-30T09:43:41Z)
- (ac 1) `python3 plugin/tests/run.py test_find 2>&1 | grep -E "^(FAIL|ERROR|OK|Ran|FAILED)|Error|assert" | head -12` → ✗ exit 1 · Ran 24 tests in 5.8s (13 classes, 16 at a time; slowest: FindCli 6s, FindRenders 2s, DryRun 1s) / FAILED (1 classes) [ran] [tree 141bf8d7f2b2] (2026-10-30T09:44:12Z)
- (ac 1) `python3 plugin/tests/run.py test_find 2>&1 | grep -E "^(FAIL|ERROR|OK|Ran|FAILED)|Error|assert" | head -12` → exit 0 · Ran 24 tests in 5.7s (13 classes, 16 at a time; slowest: FindCli 5s, FindRenders 2s, FindLearns 1s) / OK [ran] [tree 74d23a737376] (2026-10-30T09:44:27Z)
- (step 2) `python3 plugin/tests/run.py test_find 2>&1 | grep -E "^(FAIL|ERROR|OK|Ran|FAILED)|Error|assert" | head -12` → exit 0 · Ran 24 tests in 5.7s (13 classes, 16 at a time; slowest: FindCli 5s, FindRenders 2s, FindLearns 1s) / OK [ran] [tree 74d23a737376] (2026-10-30T09:44:27Z)
- (step 2) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 24 tests in 6.2s (13 classes, 16 at a time; slowest: FindCli 6s, FindRenders 4s, FindLearns 1s) / OK [ran] [tree 74d23a737376] (2026-10-30T09:44:37Z)
- (ac 1) `python3 plugin/tests/run.py test_find 2>&1 | grep -E "^(FAIL|ERROR|OK|Ran|FAILED)|Error|assert" | head -12` → ✗ exit 1 · Ran 25 tests in 6.7s (13 classes, 16 at a time; slowest: FindCli 6s, FindRenders 4s, FindLearns 1s) / FAILED (1 classes) [ran] [tree 9cca3678093d] (2026-10-30T09:44:58Z)
- (step 3) `python3 plugin/tests/run.py test_find test_exam 2>&1 | grep -E "^(FAIL|ERROR|OK|Ran|FAILED)|Error|assert" | head -12` → exit 0 · Ran 45 tests in 21.9s (21 classes, 16 at a time; slowest: ExamGen 22s, ExamRust 13s, ExamC 12s) / OK [ran] [tree 187edccf5f7c] (2026-10-30T09:45:25Z)
- (step 3) `python3 plugin/tests/run.py test_cli test_find test_exam test_docs` → exit 0 · Ran 259 tests in 24.4s (78 classes, 16 at a time; slowest: TaskLifecycle 24s, ExamGen 18s, StateViews 13s) / OK [ran] [tree d37a9c5dced3] (2026-10-30T09:46:50Z)
- (ac 1) `python3 plugin/tests/run.py test_find 2>&1 | grep -E "^(FAIL|ERROR|OK|Ran|FAILED)|Error|assert" | head -14` → ✗ exit 1 · Ran 28 tests in 8.5s (13 classes, 16 at a time; slowest: FindRenders 8s, FindCli 7s, FindLearns 2s) / FAILED (1 classes) [ran] [tree b82a45333c07] (2026-10-30T09:49:44Z)
- (step 1) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 28 tests in 5.9s (13 classes, 16 at a time; slowest: FindCli 6s, FindRenders 2s, FindLearns 1s) / OK [ran] [tree 994315689157] (2026-10-30T09:53:52Z)
- (step 2) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 28 tests in 5.9s (13 classes, 16 at a time; slowest: FindCli 6s, FindRenders 2s, FindLearns 1s) / OK [ran] [tree 994315689157] (2026-10-30T09:53:58Z)
- (step 3) `python3 plugin/tests/run.py test_cli test_find test_exam test_docs` → exit 0 · Ran 262 tests in 24.4s (78 classes, 16 at a time; slowest: TaskLifecycle 24s, ExamGen 19s, StateViews 13s) / OK [ran] [tree 994315689157] (2026-10-30T09:54:23Z)
- (audit intent) `re-read brief 6 vs diff` → severity x reach x precision, mute floor, abstain bar, learns from outcomes; proof/effort fixed at 1 as a stated ceiling [tree 994315689157] (2026-10-30T09:54:41Z)
- (audit adversary) `outside tree, hostile says text, twin keys` → outside-tree leads need confirm; lead text c.plain'd and quoted as data; twins keyed by index; dropped never refiled [tree 994315689157] (2026-10-30T09:54:41Z)
- (audit edge) `--capture 0/-1, no project, missing dir, only-held leads, reverted fate, aged drops` → all exit 2 or 0 as tested; reverted counts false; 180-day half-life lifts a mute [tree 994315689157] (2026-10-30T09:54:41Z)
- (audit operator) `fm find --rank output and exit` → held leads listed last with a 'held back' note, exit 0 when only held remain [tree 994315689157] (2026-10-30T09:54:41Z)
- (audit maintainer) `param shadowing, docs` → precision param renamed prec; MASTER/CHANGELOG/README updated [tree 994315689157] (2026-10-30T09:54:41Z)
- (ac 1) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 28 tests in 5.9s (13 classes, 16 at a time; slowest: FindCli 6s, FindRenders 2s, FindLearns 1s) / OK [ran] [tree 994315689157] (2026-10-30T09:58:31Z)
- (audit edge) `fm-reviewer pass (approve with nits, saved as research T-2125-review); 3 MEDIUM + 3 LOW fixed test-first; full gates green` → --capture 0/-1, no project, missing dir exit 2; only held leads exit 0; reverted counts false; aged drops lift a mute [tree 994315689157] (2026-10-30T09:58:31Z)
- (audit adversary) `fm-reviewer pass (approve with nits, saved as research T-2125-review); 3 MEDIUM + 3 LOW fixed test-first; full gates green` → outside-tree leads wait for confirm; lead text plain'd and quoted as data; twin leaks keyed apart [tree 994315689157] (2026-10-30T09:58:31Z)
## Log
- 2026-10-30T08:06:48Z created
- 2026-10-30T09:38:49Z focused
- 2026-10-30T09:58:58Z done
- 2026-10-30T09:58:59Z committed b38b99cc (7 files)
- 2026-10-30T09:59:07Z guard authorization added: publish
- 2026-10-30T10:01:28Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2121 [FEATURE L, done, 2 steps] fm find: deterministic language-agnostic finders (untested, docs, deps, sql, slow, flaky, secrets, gates), zero on every clean render (…
- research T-2126-review: Changes needed. The new exam code works as tested. But adding two kinds to `fmexam.KINDS` changes an existing Genesis exam in fmgenesis.py, which…
- T-2126 [FEATURE M, done, 2 steps] #1 held-out exam: I-none, I-clean, I-rank child-authored kinds; finders, foreman and plain arms (Mission 3 brief 7) — lesson: a module-…
- decision 2026-10-30: [revisit: when plugin/lib/fmexam.py changes @ecf3a72d8dff] Exam baseline: the finders arm (fmdocs.scan + fmsecrets, no session) scores 0/108 on s0-0…
## Lessons
- fm find's exit 1 means findings, so its own usage slips must exit 2; fm's UsageError exits 1 and would read as a hit
## Files touched
- plugin/tests/test_find.py
- plugin/lib/fmcli.py
- plugin/lib/fmfind.py
- plugin/lib/fmexam.py
- CHANGELOG.md
- MASTER.md
- README.md
