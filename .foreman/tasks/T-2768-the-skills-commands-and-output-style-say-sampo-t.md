---
id: T-2768
type: CLEAN
tier: M
status: done
priority: normal
scope: [plugin/skills/**, plugin/commands/*.md, plugin/output-styles/*, plugin/tests/test_rename_scan.py, plugin/tests/test_skills*.py, plugin/tests/test_docs.py, plugin/tests/test_playbooks*.py]
depends_on: []
source: user
created: 2026-11-03T04:36:55Z
updated: 2026-11-03T17:19:31Z
builder_model: sonnet
base: 2fce8278847fa9990e74449cea415037a3849aec
base_tree: 80b1f2e4d667a97fee360c79543e13f3ebfd221c
plan0_at: 2026-11-03T04:52:04Z
plan0_scope: [plugin/skills/**, plugin/commands/*.md, plugin/output-styles/*, plugin/tests/test_rename_scan.py, plugin/tests/test_skills*.py, plugin/tests/test_docs.py, plugin/tests/test_playbooks*.py]
lane_stop: merged 2026-11-03T05:20:35Z
verified: strong
unproven: [docs, ui-unshot]
---
# The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output-styles becomes Sampo, Smith, Rune, Louhi, Moons, Underworld or Ward as the text means, and fm verbs in prose become their sampo spelling; plugin ids (foreman:intake, foreman:fm-builder …) stay until the plugin-id step renames them with aliases
## Raw request
> The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output-styles becomes Sampo, Smith, Rune, Louhi, Moons, Underworld or Ward as the text means, and fm verbs in prose become their sampo spelling; plugin ids (foreman:intake, foreman:fm-builder …) stay until the plugin-id step renames them with aliases
## Interpretation
Reading 1 (chosen): SAMPO.md says no user-visible Foreman remains. Skills, commands and the output style are text that Claude and the user read, so their prose says Sampo and its role names: the product is Sampo; the task loop or executor is Smith (sampo smith); Genesis is Rune; the exam or Inspector is Louhi; moonshots are Moons; the not-yet ledger is the Underworld; the guard is the Ward. Commands in prose take the sampo spelling (sampo task new …). That needs T-2766's verb map, which this lane builds on. What stays: plugin ids and agent ids (foreman:intake, foreman:fm-builder, /foreman:…), since they rename only with the plugin-id step and its aliases; FOREMAN_* env names; ~/.claude/foreman; Foreman-Task. That matches test_rename_scan's KEPT. About 330 Foreman mentions and 69 'Foreman:' across 184 files. Reading 2 (ruled out): a blind regex replace. 'Foreman:' is also the hook-note prefix the skills quote, which renames with the library strings (step 5a), and 'the foreman' can name a role in examples.
## Assumptions (confidence)
## Acceptance criteria
- [x] no prose Foreman is left in plugin/skills, plugin/commands or plugin/output-styles outside the kept forms (foreman:ID plugin ids, FOREMAN_*, ~/.claude/foreman), and the rename ratchet's BASELINE drops by at least the lines changed — verify with `python3 plugin/tests/run.py test_rename_scan`
- [x] the skill and doc suites stay green, and every command a skill names still runs (fm and sampo spellings both) — verify with `python3 plugin/tests/run.py test_docs test_skills test_rename_aliases`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: fm sub (regex codemod with per-file counts) for the safe forms ('Foreman' as the product name in prose), then read and hand-fix each file the counts flag for role names and quoted output; test_rename_scan as the ratchet. Likely outcome: 184 files, BASELINE down by about 300. Fails if: a skill quotes a hook note ('Foreman: …') that the library still prints; leave those for step 5a, and the ratchet counts them.
2. Rewrite each skill by hand. Fails if: 184 files cost far more for the same result.
3. Do less: only SKILL.md front matter and descriptions. Fails if: bodies stay Foreman, and the cold review would flag them.
Choice 1 (80%).
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, MASTER.md, site/pages.py, site/build.py, README.md; past FIXes T-1239, T-1371, T-1569, T-1714, T-2266.
## Execution prompt
## Steps
1. [x] a red check: test_rename_scan counts skills/commands/output-styles lines; lower BASELINE to the target
2. [x] the sweep, by meaning (product → Sampo; the loop → Smith; Genesis → Rune; exam → Louhi; guard → Ward), each file read, not a blind replace
3. [x] fm help and a sample of skill commands run under both names
## Resume here
<!-- auto -->
- 2026-11-03T16:42:09Z steps 3/3 done
- git: foreman/build; 0 uncommitted
- failures met: timed out after 0s; posttoolusefailure 0.0 0.0 0 [0]
## Docs impact
plugin/skills, plugin/commands, plugin/output-styles
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_rename_scan test_docs test_skills test_rename_aliases` → exit 0 · Ran 117 tests in 14.6s (28 classes, 16 at a time; slowest: Fences 13s, RenameAliases 9s, DocsProof 8s) / OK [ran] [tree 60b3c644084d] [world 2f1906870a] (2026-11-03T04:56:31Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 2 of 6 failed: python3 plugin/tests/bench_hooks.py --runs 20 → ✗ exit 1 · SessionEnd                  53.3    84.0     150  [0] / machine busy (load 2.0 per core): judged by each hook's CPU time, not wall time (T-0805) (flaky again (failed first in 3+ recent runs): treated as a failure; find the race); python3 plugin/tests/run.py → ✗ exit 124 (timed out after 600s) · timed out after 600s [ran] [tree b3eb410e32c8] [world 2f1906870a] (2026-11-03T05:04:06Z)
- (ac 1) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: RenameScan 1s) / OK [ran] [tree 981c9f062662] [world 2f1906870a] (2026-11-03T16:28:32Z)
- (ac 2) `python3 plugin/tests/run.py test_docs test_skills test_rename_aliases` → exit 0 · Ran 117 tests in 8.4s (27 classes, 16 at a time; slowest: Fences 8s, RenameAliases 3s, DocsProof 2s) / OK [ran] [tree 981c9f062662] [world 2f1906870a] (2026-11-03T16:28:32Z)
- (step 1) `python3 plugin/tests/run.py test_rename_scan test_docs test_skillroute test_rename_aliases` → exit 0 · Ran 123 tests in 8.3s (28 classes, 16 at a time; slowest: Fences 8s, RenameAliases 3s, DocsProof 2s) / OK [ran] [tree 981c9f062662] [world 2f1906870a] (2026-11-03T16:28:32Z)
- (step 2) `python3 plugin/tests/run.py test_rename_scan test_docs test_skillroute test_rename_aliases` → exit 0 · Ran 123 tests in 8.3s (28 classes, 16 at a time; slowest: Fences 8s, RenameAliases 3s, DocsProof 2s) / OK [ran] [tree 981c9f062662] [world 2f1906870a] (2026-11-03T16:28:32Z)
- (step 3) `python3 plugin/tests/run.py test_rename_scan test_docs test_skillroute test_rename_aliases` → exit 0 · Ran 123 tests in 8.3s (28 classes, 16 at a time; slowest: Fences 8s, RenameAliases 3s, DocsProof 2s) / OK [ran] [tree 981c9f062662] [world 2f1906870a] (2026-11-03T16:28:32Z)
- (audit intent) `self: sampled the swept lines and the by-meaning pass; product mentions say Sampo, role lines Smith/Rune/Louhi/Ward` → skills, commands and the output style say Sampo and its role names; plugin ids, paths and fm spellings stay [tree 981c9f062662] (2026-11-03T16:28:32Z)
- (audit edge) `self: sampled the swept lines and the by-meaning pass; product mentions say Sampo, role lines Smith/Rune/Louhi/Ward` → the output style id 'Foreman' stays (setup reads it); third-party attribution headers keep their meaning [tree 981c9f062662] (2026-11-03T16:28:32Z)
- (audit adversary) `self: sampled the swept lines and the by-meaning pass; product mentions say Sampo, role lines Smith/Rune/Louhi/Ward` → prose only; no command text changed, so no guard pattern is affected [tree 981c9f062662] (2026-11-03T16:28:32Z)
- `python3 plugin/tests/run.py test_rename_scan test_docs test_skillroute test_rename_aliases` → exit 0 · Ran 123 tests in 8.4s (28 classes, 16 at a time; slowest: Fences 8s, RenameAliases 3s, DocsProof 2s) / OK [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T16:42:17Z)
- (audit intent) `self: sampled the swept lines and the by-meaning pass; product mentions say Sampo, role lines Smith/Rune/Louhi/Ward` → skills, commands and the output style say Sampo and its role names; plugin ids, paths and fm spellings stay [tree 398b4aa61509] (2026-11-03T16:42:17Z)
- (audit edge) `self: sampled the swept lines and the by-meaning pass; product mentions say Sampo, role lines Smith/Rune/Louhi/Ward` → the output style id 'Foreman' stays (setup reads it); third-party attribution headers keep their meaning [tree 398b4aa61509] (2026-11-03T16:42:17Z)
- (audit adversary) `self: sampled the swept lines and the by-meaning pass; product mentions say Sampo, role lines Smith/Rune/Louhi/Ward` → prose only; no command text changed, so no guard pattern is affected [tree 398b4aa61509] (2026-11-03T16:42:17Z)
- `python3 plugin/tests/run.py test_rename_scan test_docs test_skillroute test_rename_aliases` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T16:42:17Z [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T16:45:22Z)
- (audit intent) `self: sampled the swept lines and the by-meaning pass; product mentions say Sampo, role lines Smith/Rune/Louhi/Ward` → skills, commands and the output style say Sampo and its role names; plugin ids, paths and fm spellings stay [tree 398b4aa61509] (2026-11-03T16:45:22Z)
- (audit edge) `self: sampled the swept lines and the by-meaning pass; product mentions say Sampo, role lines Smith/Rune/Louhi/Ward` → the output style id 'Foreman' stays (setup reads it); third-party attribution headers keep their meaning [tree 398b4aa61509] (2026-11-03T16:45:22Z)
- (audit adversary) `self: sampled the swept lines and the by-meaning pass; product mentions say Sampo, role lines Smith/Rune/Louhi/Ward` → prose only; no command text changed, so no guard pattern is affected [tree 398b4aa61509] (2026-11-03T16:45:22Z)
- `python3 plugin/tests/run.py test_rename_scan test_docs test_skillroute test_rename_aliases` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T16:45:22Z [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T16:48:13Z)
- (audit intent) `self: sampled the swept lines and the by-meaning pass; product mentions say Sampo, role lines Smith/Rune/Louhi/Ward` → skills, commands and the output style say Sampo and its role names; plugin ids, paths and fm spellings stay [tree 398b4aa61509] (2026-11-03T16:48:13Z)
- (audit edge) `self: sampled the swept lines and the by-meaning pass; product mentions say Sampo, role lines Smith/Rune/Louhi/Ward` → the output style id 'Foreman' stays (setup reads it); third-party attribution headers keep their meaning [tree 398b4aa61509] (2026-11-03T16:48:13Z)
- (audit adversary) `self: sampled the swept lines and the by-meaning pass; product mentions say Sampo, role lines Smith/Rune/Louhi/Ward` → prose only; no command text changed, so no guard pattern is affected [tree 398b4aa61509] (2026-11-03T16:48:13Z)
- `python3 plugin/tests/run.py test_rename_scan test_docs test_skillroute test_rename_aliases` → exit 0 · Ran 124 tests in 8.4s (28 classes, 16 at a time; slowest: Fences 8s, RenameAliases 3s, DocsProof 2s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:13:12Z)
- (audit intent) `self: sampled the swept lines and the by-meaning pass; product mentions say Sampo, role lines Smith/Rune/Louhi/Ward` → skills, commands and the output style say Sampo and its role names; plugin ids, paths and fm spellings stay [tree 07445d19b39c] (2026-11-03T17:13:12Z)
- (audit edge) `self: sampled the swept lines and the by-meaning pass; product mentions say Sampo, role lines Smith/Rune/Louhi/Ward` → the output style id 'Foreman' stays (setup reads it); third-party attribution headers keep their meaning [tree 07445d19b39c] (2026-11-03T17:13:12Z)
- (audit adversary) `self: sampled the swept lines and the by-meaning pass; product mentions say Sampo, role lines Smith/Rune/Louhi/Ward` → prose only; no command text changed, so no guard pattern is affected [tree 07445d19b39c] (2026-11-03T17:13:12Z)
## Log
- 2026-11-03T04:36:55Z created
- 2026-11-03T04:37:07Z set approved=True
- 2026-11-03T04:37:08Z blocked: waits on T-2766 (the sampo verb map) so prose can name sampo verbs that run; launch its lane after that merges
- 2026-11-03T04:51:39Z unblocked
- 2026-11-03T04:51:40Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2768.builder.md
- 2026-11-03T04:51:59Z focused
- 2026-11-03T04:57:05Z steer: fm command spellings in skill prose stay fm in this task: hook patterns may match only fm, so converting them waits for a follow-up that checks every hook regex for both names; test_playbooks doesn't exist, the second criterion drops it
- 2026-11-03T04:57:12Z criterion 2 text: the skill, doc and playbook suites stay green, and every command a skill names still runs (fm and sampo spellings both) → the skill and doc suites stay green, and every command a skill names still runs (fm and sampo spellings both) — verify with `python3 plugin/tests/run.py test_docs test_skills test_rename_aliases`
- 2026-11-03T05:09:06Z criterion 2 verify: `python3 plugin/tests/run.py test_docs test_skills test_rename_aliases` — verify with `python3 plugin/tests/run.py test_docs test_skills test_playbooks test_rename_aliases` → `python3 plugin/tests/run.py test_docs test_skills test_rename_aliases`
- 2026-11-03T05:20:35Z merged worktree-agent-a356b2ee5d2fcd861 (176 file(s))
- 2026-11-03T05:20:45Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a356b2ee5d2fcd861
- 2026-11-03T15:07:38Z focused
- 2026-11-03T15:07:39Z paused: focus moved to T-2774
- 2026-11-03T16:28:12Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T16:28:12Z focused
- 2026-11-03T16:28:51Z paused: focus moved to T-2814
- 2026-11-03T16:42:07Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-03T16:42:07Z focused
- 2026-11-03T16:51:04Z paused: focus moved to T-2774
- 2026-11-03T16:51:11Z scope: .fm-scratch/rows.py, sub.py and meaning.py are the builder's throwaway rename helpers in the lane's scratch folder, not shipped code
- 2026-11-03T17:13:01Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T17:13:01Z focused
- 2026-11-03T17:19:31Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- T-2748 [CLEAN M, planned, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.p…
- T-2766 [FEATURE M, active, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as…
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_audit.py, plugin/tests/test_backlog.py, plugin/tests/test_board_surfaces.py, plugin/tests/test_brainstorm_skill.py, plugin/tests/test_cli.…
## Preflight
Changed in scope since this was planned (2026-11-03): plugin/commands/backlog.md, plugin/commands/build.md, plugin/commands/looks.md, plugin/commands/settings.md, plugin/output-styles/foreman.md, plugin/skills/brainstorm/SKILL.md, plugin/skills/brainsto…; re-ground the plan against them before editing
## Behaviour lock
none: the builder lane's pre-edit fm check timed out or failed on bench_hooks timing under machine load on 2026-11-03 (T-2797), so no lock was recorded before the first edit; the change is covered by its targeted tests and the post-merge full suite
## Lessons
- A blind replace needs a by-meaning pass after it
## Files touched
- .fm-scratch/rows.py
- .fm-scratch/sub.py
- plugin/commands/backlog.md
- plugin/commands/build.md
- plugin/commands/looks.md
- plugin/commands/settings.md
- plugin/output-styles/foreman.md
- plugin/skills/brainstorm/SKILL.md
- plugin/skills/brainstorm/references/ideas-prompt.md
- plugin/skills/capture/SKILL.md
- plugin/skills/debug-test/SKILL.md
- plugin/skills/design-extract/SKILL.md
- plugin/skills/directions/SKILL.md
- plugin/skills/directions/references/cards.md
- plugin/skills/doctor/SKILL.md
- plugin/skills/genesis/SKILL.md
- plugin/skills/improve/SKILL.md
- plugin/skills/initiative/SKILL.md
- plugin/skills/intake/SKILL.md
- plugin/skills/intake/references/debugging-condition-based-waiting.md
- plugin/skills/intake/references/debugging-defense-in-depth.md
- plugin/skills/intake/references/debugging-root-cause-tracing.md
- plugin/skills/intake/references/debugging.md
- plugin/skills/intake/references/delegate.md
- plugin/skills/intake/references/language.md
- plugin/skills/intake/references/planning.md
- plugin/skills/intake/references/regression-test.md
- plugin/skills/intake/references/verification.md
- plugin/skills/intake/references/writing-good-tests.md
- plugin/skills/library/SKILL.md
