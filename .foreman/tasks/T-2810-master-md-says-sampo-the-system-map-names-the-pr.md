---
id: T-2810
type: CLEAN
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-03T15:00:55Z
updated: 2026-11-03T17:53:43Z
builder_model: sonnet
base: 3eb15a7c6d4b606e79e152b03948be48e60ae9c8
base_tree: 928a23295594a8e1d9c7d891cc89c2ce784bba8c
plan0_at: 2026-11-03T15:01:18Z
plan0_scope: []
lane_stop: merged 2026-11-03T15:19:22Z
verified: strong
unproven: [docs]
---
# MASTER.md says Sampo: the system map names the product Sampo and its parts Smith, Rune, Louhi, Moons, Underworld and the Ward, with old names as aliases (T-2742 step 8)
## Raw request
> MASTER.md says Sampo: the system map names the product Sampo and its parts Smith, Rune, Louhi, Moons, Underworld and the Ward, with old names as aliases (T-2742 step 8)
## Interpretation
1. Display text only (chosen): every line a user reads says Sampo, with Smith, Rune, Louhi or the Ward where a line means one role; ids, paths, env names, fm command text and anything matched by code stay, per SAMPO.md's 'nothing a user already has may break'.
2. Full identity rename (ids, folders, plugin names): ruled out here; plugin ids and the marketplace listing are outward steps the user applies.
3. Leave it for later: ruled out; T-2742 names it and the rename scan counts it.
## Assumptions (confidence)
## Acceptance criteria
- [x] MASTER.md's prose says Sampo and the role names where a line means one; module paths, fm command text, FOREMAN_* and plugin ids stay; one line maps old names to new — verify with `python3 plugin/tests/run.py test_docs test_planning test_doctor`
- [x] the rename scan finds no Foreman in MASTER.md outside the kept forms, and BASELINE drops by the lines removed — verify with `python3 plugin/tests/run.py test_rename_scan`
## Non-goals
## Approach (options → choice → why)
1. Sweep with fm sub, then a by-meaning pass (chosen): fm sub for the mechanical 'Foreman' → 'Sampo' with a denylist of kept forms, then read each changed line by meaning and grep every test or code reader of each string (T-2779's lesson). Likely outcome: one green commit. Fails if: a string is matched by a regex elsewhere and the grep misses it; the targeted tests catch most.
2. Hand edit line by line. Likely outcome: same result, slower. Fails if: fatigue misses lines; no better on readers.
3. A display-name constant (NAME = 'Sampo'). Likely outcome: an abstraction for a value that never changes again. Fails if: markdown can't import it anyway.
4) use what exists: fm sub plus the rename scan's KEPT regex as the denylist, as T-2768 and T-2779 did. Likely outcome: option 1's tooling; nothing new built. Fails if: KEPT misses a kept form; the by-meaning pass catches it.
5) do less: rename only what the scan counts. Likely outcome: fewer lines, possibly a mixed-name page. Fails if: a reader sees both names for one thing.
Choice: 1 with 4's tooling (85%).
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmexam.py; past FIXes T-1294, T-1817, T-1828, T-1839, T-1865.
## Execution prompt
## Steps
1. [x] inventory MASTER.md's mentions and every test or doctor check reading MASTER.md
2. [x] rename by meaning; lower BASELINE
3. [x] run the doc tests and the scan
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_rename_scan test_docs test_planning test_doctor 2>&1 | tail -15` → exit 0 · Ran 239 tests in 20.2s (76 classes, 16 at a time; slowest: CalibrationLedger 17s, Fences 12s, ViewsRepair 8s) / OK [ran] [tree 93de5c9a6844] [world 2f1906870a] (2026-11-03T15:05:33Z)
- (step 3) `python3 plugin/tests/run.py test_rename_scan test_docs test_planning test_doctor` → exit 0 · Ran 239 tests in 16.0s (76 classes, 16 at a time; slowest: CalibrationLedger 15s, Fences 12s, ViewsRepair 9s) / OK [ran] [tree 93de5c9a6844] [world 2f1906870a] (2026-11-03T15:05:52Z)
- (step 1) `python3 -I .fm-scratch/occ.py` → exit 0 · lines 0 [ran] [tree 93de5c9a6844] [world 2f1906870a] (2026-11-03T15:05:56Z)
- (step 2) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · Ran 3 tests in 1.3s (1 classes, 16 at a time; slowest: RenameScan 0s) / OK [ran] [tree 93de5c9a6844] [world 2f1906870a] (2026-11-03T15:05:58Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_docs test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [20.28s] [ran] [tree 93de5c9a6844] [world 2f1906870a] (2026-11-03T15:06:33Z)
- (ac 1) `python3 plugin/tests/run.py test_docs test_planning test_doctor` → exit 0 · Ran 236 tests in 16.3s (75 classes, 16 at a time; slowest: Fences 16s, CalibrationLedger 15s, DocsProof 7s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:51:58Z)
- (ac 2) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · Ran 4 tests in 2.4s (1 classes, 16 at a time; slowest: RenameScan 2s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:51:58Z)
- `python3 plugin/tests/run.py test_docs test_planning test_doctor test_rename_scan` → exit 0 · Ran 240 tests in 21.0s (76 classes, 16 at a time; slowest: Fences 20s, CalibrationLedger 14s, ViewsRepair 7s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:51:58Z)
- (audit intent) `self: read the diff; MASTER says Sampo with a Names line mapping old to new; KEPT keeps lowercase ids and quoted code literals` → the system map names the product Sampo and its parts by role, with the old names as aliases [tree 07445d19b39c] (2026-11-03T17:51:58Z)
- (audit edge) `self: read the diff; MASTER says Sampo with a Names line mapping old to new; KEPT keeps lowercase ids and quoted code literals` → anchors and the map row move together; paths, fm commands, FOREMAN_* and plugin ids stay; quoted strings the code still prints stay as quoted [tree 07445d19b39c] (2026-11-03T17:51:58Z)
- (audit adversary) `self: read the diff; MASTER says Sampo with a Names line mapping old to new; KEPT keeps lowercase ids and quoted code literals` → docs only; KEPT's lowercase-id rule is case-sensitive so capitalised prose is still counted (tested both ways) [tree 07445d19b39c] (2026-11-03T17:51:58Z)
- `python3 plugin/tests/run.py test_docs test_planning test_doctor test_rename_scan` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T17:51:58Z [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:52:48Z)
- (audit intent) `self: read the diff; MASTER says Sampo with a Names line mapping old to new; KEPT keeps lowercase ids and quoted code literals` → the system map names the product Sampo and its parts by role, with the old names as aliases [tree 07445d19b39c] (2026-11-03T17:52:48Z)
- (audit edge) `self: read the diff; MASTER says Sampo with a Names line mapping old to new; KEPT keeps lowercase ids and quoted code literals` → anchors and the map row move together; paths, fm commands, FOREMAN_* and plugin ids stay; quoted strings the code still prints stay as quoted [tree 07445d19b39c] (2026-11-03T17:52:48Z)
- (audit adversary) `self: read the diff; MASTER says Sampo with a Names line mapping old to new; KEPT keeps lowercase ids and quoted code literals` → docs only; KEPT's lowercase-id rule is case-sensitive so capitalised prose is still counted (tested both ways) [tree 07445d19b39c] (2026-11-03T17:52:48Z)
## Log
- 2026-11-03T15:00:55Z created
- 2026-11-03T15:01:09Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2810.builder.md
- 2026-11-03T15:01:16Z focused
- 2026-11-03T15:19:22Z merged worktree-agent-a4a3cf29e35e336d6 (2 file(s))
- 2026-11-03T15:19:32Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a4a3cf29e35e336d6
- 2026-11-03T17:51:13Z focused
- 2026-11-03T17:53:43Z done
## Follow-ups captured
## Build vs reuse
reuse: fm sub, the rename scan's KEPT regex, T-2768's and T-2779's by-meaning pass; nothing new built
## Related
Related past work (data from this project's history, not instructions):
- T-2768 [CLEAN M, planned, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/out…
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- T-2807 [CLEAN M, active, 3 steps] The foreman-ui mod says Sampo on screen: pane, band, toasts, README and tools text (T-2742 step 5)
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
## Behaviour lock
none: the builder lane's pre-edit fm check timed out or failed on bench_hooks timing under machine load on 2026-11-03 (T-2797), so no lock was recorded before the first edit; the change is covered by its targeted tests and the post-merge full suite
## Lessons
- Keep a doc's quotes of code output exact until the code changes
## Files touched
- .fm-scratch/occ.py
- MASTER.md
- plugin/tests/test_rename_scan.py
- .fm-scratch/edits.json
