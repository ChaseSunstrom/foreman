---
id: T-1908
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmwhich.py, plugin/lib/fmrecall.py, plugin/lib/fmcli.py, plugin/tests/test_which.py, plugin/tests/test_help.py, CHANGELOG.md]
depends_on: [T-1907]
source: discovered
created: 2026-10-29T03:51:46Z
updated: 2026-10-29T04:29:51Z
base: e60f9b341c120eda159943fcbe79cc0582f23eb7
base_tree: d0119cec50b205aacb0a0b126547744c69a91df7
plan0_at: 2026-10-29T04:19:03Z
plan0_scope: [plugin/lib/fmwhich.py, plugin/lib/fmrecall.py, plugin/lib/fmcli.py, plugin/tests/test_which.py, plugin/tests/test_help.py, CHANGELOG.md]
verified: strong
---
# FIX: fm which misses subcommands and the rules' own phrases: 'drop a task', 'defer a task'
## Raw request
> FIX: fm which misses subcommands and the rules' own phrases: 'drop a task', 'defer a task', 'record evidence' never name fm task drop/defer/evidence (only top-level verbs are indexed); 'stop auto-continuing' matches nothing though foreman.md maps it to fm drive off; and the best-scoring kind (fm cost 11.8) prints last, under 3.9-score playbooks
## Interpretation
fm which and fm help only see top-level verbs: index nested subcommands with a one-line help each, fold the rules' plain-words table into each command's text, print the best-scoring kind first, and let fm help NAME print that command's help (T-1909 folded in).
## Assumptions (confidence)
## Acceptance criteria
- [x] a task subcommand is found by its verb (drop a task → fm task drop), a rules phrase names its command (stop auto-continuing → fm drive), the strongest kind prints first — verify with `python3 plugin/tests/run.py test_which`
- [x] fm help with a command's name (task, task drop) prints its help (T-1909) — verify with `python3 plugin/tests/run.py test_help -k command_name`
## Non-goals
## Approach (options → choice → why)
Complete: subcommands indexed with summaries, fm task --help lists them, curated phrases reach their commands, best match first. Approaches: (A) help on each tadd + verb_docs recursion — chosen, fm task --help gains them too; (B) an alias table in fmwhich — rejected, a second list to keep in step; (C) embeddings — rejected, stdlib only; (D) index foreman.md's '"phrase" → command' pairs — chosen with A, the table is already kept for the agent.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] each fm task subcommand gets a one-line help; verb_docs indexes nested subcommands as 'task drop'
3. [x] the rules' plain-words table folds each phrase into its command's document
4. [x] kinds print strongest first
5. [x] CHANGELOG
6. [x] fm help with a command path prints its argparse help
## Resume here
<!-- auto -->
- 2026-10-29T04:27:19Z steps 6/6 done
- git: foreman/build; 6 uncommitted: CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmrecall.py, plugin/lib/fmwhich.py, plugin/tests/test_help.py, plugin/tests/test_which.py
- touched since last checkpoint: plugin/tests/test_help.py, CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmwhich.py, plugin/lib/fmrecall.py, plugin/tests/test_which.py
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_which test_help` → red as expected (exit 1) · Ran 21 tests in 3.4s (6 classes, 16 at a time; slowest: Which 3s, Help 2s, PromptApprovals 1s) / FAILED (2 classes) [ran] [tree 5013e26e5e47] (2026-10-29T04:19:20Z)
- (step 2) `python3 plugin/tests/run.py test_which test_help` → exit 0 · Ran 21 tests in 4.1s (6 classes, 16 at a time; slowest: Which 4s, Help 2s, PromptApprovals 1s) / OK [ran] [tree bcb90f284ece] (2026-10-29T04:19:39Z)
- (step 3) `python3 plugin/tests/run.py test_which test_help` → exit 0 · Ran 21 tests in 4.3s (6 classes, 16 at a time; slowest: Which 4s, Help 2s, PromptApprovals 1s) / OK [ran] [tree bcb90f284ece] (2026-10-29T04:19:44Z)
- (step 4) `python3 plugin/tests/run.py test_which test_help` → exit 0 · Ran 21 tests in 4.3s (6 classes, 16 at a time; slowest: Which 4s, Help 2s, PromptApprovals 1s) / OK [ran] [tree bcb90f284ece] (2026-10-29T04:19:49Z)
- (step 6) `python3 plugin/tests/run.py test_which test_help` → exit 0 · Ran 21 tests in 4.1s (6 classes, 16 at a time; slowest: Which 4s, Help 2s, PromptApprovals 1s) / OK [ran] [tree bcb90f284ece] (2026-10-29T04:19:53Z)
- (step 5) `grep -c 'T-190[89])' CHANGELOG.md` → exit 0 · 2 [ran] [tree bcb90f284ece] (2026-10-29T04:19:54Z)
- (step 3) `python3 plugin/tests/run.py test_which test_help` → exit 0 · Ran 21 tests in 2.5s (6 classes, 16 at a time; slowest: Which 2s, Help 1s, PromptApprovals 1s) / OK [ran] [tree f76c78cd4931] (2026-10-29T04:22:43Z)
- (step 6) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmrecall.py, plugin/lib/fmwhich.py — commit it through a task, or git checkout it back / fm doct; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                42.6    43.8     150  [0] / SessionEnd                  37.8    39.7     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree f76c78cd4931] (2026-10-29T04:27:31Z)
- (ac 1) `python3 plugin/tests/run.py test_which` → exit 0 · Ran 15 tests in 2.6s (3 classes, 16 at a time; slowest: Which 2s, Snapshots 0s, Extract 0s) / OK [ran] [tree f76c78cd4931] (2026-10-29T04:28:46Z)
- (ac 2) `python3 plugin/tests/run.py test_help -k command_name` → exit 0 · Ran 8 tests in 1.3s (5 classes, 16 at a time; slowest: Help 1s, PromptApprovals 1s, Rules 0s) / OK [ran] [tree f76c78cd4931] (2026-10-29T04:28:46Z)
- (audit intent) `fm-reviewer pass: approve with nits, all fixed` → subcommands (task defer/drop) and the rules' plain words found by fm which [tree f76c78cd4931] (2026-10-29T04:28:46Z)
- (audit edge) `fm-reviewer pass: approve with nits, all fixed` → unreadable rules file gives empty text; a one-word command name prints its -h [tree f76c78cd4931] (2026-10-29T04:28:46Z)
- (audit adversary) `fm-reviewer pass: approve with nits, all fixed` → rules text never printed; exact dict lookup only [tree f76c78cd4931] (2026-10-29T04:28:46Z)
- (audit maintainer) `fm-reviewer pass: approve with nits, all fixed` → verb_docs docstring states its shape [tree f76c78cd4931] (2026-10-29T04:28:46Z)
## Log
- 2026-10-29T03:51:46Z created
- 2026-10-29T03:51:50Z set type=FIX
- 2026-10-29T03:57:01Z set scope=['plugin/lib/fmwhich.py', 'plugin/lib/fmrecall.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_which.py', 'CHANGELOG.md'], depends_on=['T-1907']
- 2026-10-29T03:57:02Z planned: it has criteria and steps
- 2026-10-29T04:10:26Z set scope=['plugin/lib/fmwhich.py', 'plugin/lib/fmrecall.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_which.py', 'plugin/tests/test_help.py', 'CHANGELOG.md']
- 2026-10-29T04:10:27Z steer: folds in T-1909 (fm help task refused): same discovery surface, one gate run
- 2026-10-29T04:19:02Z focused
- 2026-10-29T04:29:15Z done
- 2026-10-29T04:29:17Z committed 6e128b9d (6 files)
- 2026-10-29T04:29:51Z includes T-1909: Fm help task refuses ('nothing to look up in task, only words like can, do and it') becaus
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1397 [FEATURE M, done, 1 steps] Intake offer: fm code prints one line when an indexed skill matches the request (name, lic — lesson: Stack cards name tools (cargo) mor…
- T-1699 [FEATURE M, done, 3 steps] fm which TASK: route a task in plain words to the Foreman skill, playbooks and fm verbs that fit — lesson: Relative score floors pass n…
- research wave1-plan-a2475fc5d2263de06: === T-1049 [stale: plugin/lib/fmcli.py, plugin/lib/fmdeps.py, plugin/lib/fmhooks.py changed since it was written]
- decision 2026-10-28: T-1838 step 3: the per-turn hint still does not name the top routed book
- similar finished tasks took 1–3 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_recall.py, plugin/tests/test_which.py
## Why not caught
fm which tests only asked top-level verbs
## Lessons
- an index built from top-level verbs misses nested subparsers: walk them
## Files touched
- plugin/tests/test_help.py
- plugin/tests/test_which.py
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/lib/fmrecall.py
- plugin/lib/fmwhich.py
