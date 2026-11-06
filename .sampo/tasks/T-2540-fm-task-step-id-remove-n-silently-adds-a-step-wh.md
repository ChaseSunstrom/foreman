---
id: T-2540
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_cli.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-02T04:35:54Z
updated: 2026-11-02T05:14:07Z
base: cba920d7b2d98ae34a14984da9eeff5254de43e4
base_tree: b4d27b50776a99b1d77301464c1a936077e17320
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T04:58:19Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_cli.py, CHANGELOG.md]
verified: strong
---
# fm task step/ac: an action synonym (remove, delete, del) is the action it names, and an implied add with a second word refuses instead of dropping it
## Raw request
> fm task step ID remove N silently adds a step whose text is 'remove' (the action-less shorthand takes the unknown word as text, dropping N); a one-word action synonym (remove, delete, del, edit-like) should be refused with 'did you mean rm'
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task step ID remove 2 removes step 2; fm task step ID WORD EXTRA (implied add) refuses naming the quoting, and no step is added; a lone word still adds (T-1903) — verify with `python3 plugin/tests/run.py test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_cli beside T-1903's: remove 2 removes step 2; 'foo bar' as two words refuses; CHANGELOG still adds
2. [x] fmcli's task argv normaliser maps remove/delete/del to rm and refuses an implied add followed by another bare word
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 144 tests in 23.8s (44 classes, 16 at a time; slowest: TaskLifecycle 23s, CaptureAndIntake 12s, StateViews 12s) / FAILED (1 classes: test_cli.CaptureAndIntake) [ran] [tree 648a84661b3a] [world 2f1906870a] (2026-11-02T04:58:52Z)
- (step 2) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 144 tests in 24.4s (44 classes, 16 at a time; slowest: TaskLifecycle 24s, CaptureAndIntake 10s, StateViews 10s) / OK [ran] [tree a28564d84670] [world 2f1906870a] (2026-11-02T04:59:48Z)
- `python3 plugin/tests/run.py test_cli.CaptureAndIntake` → ✗ exit 1 · Ran 21 tests in 8.2s (1 classes, 16 at a time; slowest: CaptureAndIntake 7s) / FAILED (1 classes: test_cli.CaptureAndIntake) (start tree + this task's tests) [ran] [tree a28564d84670] [world 2f1906870a] (2026-11-02T05:00:08Z)
- `python3 plugin/tests/run.py test_cli.CaptureAndIntake` → exit 0 · Ran 21 tests in 7.6s (1 classes, 16 at a time; slowest: CaptureAndIntake 7s) / OK [ran] [tree a28564d84670] [world 2f1906870a] (2026-11-02T05:00:08Z)
- (ac 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 144 tests in 20.3s (44 classes, 16 at a time; slowest: TaskLifecycle 20s, CaptureAndIntake 8s, StateViews 8s) / OK [ran] [tree a452a4909a68] [world 2f1906870a] (2026-11-02T05:06:42Z)
- (audit edge) `self-review: synonyms map only when the subcommand's actions include rm (fm task ac has none, so its words still add); the implied add now needs a lone word, so two bare words fall to argparse's invalid-choice error` → 'remove 2' removes step 2; 'fix it' refuses and adds nothing; 'CHANGELOG' still adds (T-1903); a lone word followed by an option still adds; 'DONE', '3' and '--json' alone stay errors [tree a452a4909a68] (2026-11-02T05:06:42Z)
- (audit self) `self-review: synonyms map only when the subcommand's actions include rm (fm task ac has none, so its words still add); the implied add now needs a lone word, so two bare words fall to argparse's invalid-choice error` → no findings [tree a452a4909a68] (2026-11-02T05:06:42Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree a452a4909a68] [world 2f1906870a] (2026-11-02T05:08:56Z)
## Log
- 2026-11-02T04:35:54Z created
- 2026-11-02T04:37:45Z planned from capture
- 2026-11-02T04:58:17Z focused
- 2026-11-02T04:58:19Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T05:00:09Z scope: fmcli's task argv normaliser maps ACT_SYNONYMS (remove/delete/del → rm) when the subcommand has rm, and takes the implied add only for a lone word with no second bare word; test in test_cli.CaptureAndIntake
- 2026-11-02T05:07:17Z done
- 2026-11-02T05:07:20Z committed 8629bace (3 files)
- 2026-11-02T05:08:56Z guard authorization added: publish
- 2026-11-02T05:14:07Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1510-review: Verdict: changes needed.** One terminal-escape hole (it is the key question you asked) and one injection path in the slash command. Nothing was r…
- research T-1924-review: Verdict: changes needed.** One adversary finding is real and new. The relative-`cd` change lets a line pass that was refused before. I ran nothin…
- research T-2335-review: Changes needed, but only for the MEDIUM items. I read the code and could not run it; no shell was available. The 9 PlanContent tests are green in…
- decision 2026-10-22: T-1585: the guard refuses commands that name CLAUDECODE or CLAUDE_CODE_ENTRYPOINT to unset or override them, not a whole fresh environment (env -i, …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py
## Why not caught
T-1903's implied add tested one lone word and a near typo; a far synonym (remove vs rm: difflib ratio 0.5) followed by a number fell through to add, and argparse's optional text positional swallowed the number without an error.
## Lessons
- an implied default action must refuse leftover words rather than let an optional positional swallow them
## Plan gaps
- failed first: step 1 red test in test_cli beside T-1903's: remove 2 removes step 2; 'foo bar' as two words refuses; CHAN…
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- CHANGELOG.md
