---
id: T-0984
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-15T22:26:16Z
updated: 2026-10-15T22:33:32Z
base: 111e539ba0496fb27e817b22e1be8524ce3f09f7
base_tree: 342e98701553a2eac95e270b243ffd252fdcf235
verified: strong
---
# Failure hint: 'No such file' on plugin/bin/fm*.py says Foreman's modules are in plugin/lib
## Raw request
> Failure hint: 'No such file' on plugin/bin/fm*.py says Foreman's modules are in plugin/lib/
## Interpretation
When a command fails with 'No such file' on a plugin/bin/fm*.py path, the failure hint should say Foreman's modules are in plugin/lib/ (plugin/bin holds only the fm launcher).
## Assumptions (confidence)
## Acceptance criteria
- [x] A 'No such file' failure naming plugin/bin/fm*.py gets the plugin/lib hint — verify with `python3 plugin/tests/run.py test_round_f`
## Non-goals
## Approach (options → choice → why)
Options: take the fix the recorded demo session made in its clone (fmrecall.note_failure, with a test) after review (chosen: real, tested work from the recording); write it again by hand (duplicate effort).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Bring in the recorded session's commit; run its test
## Resume here
## Docs impact
none: a failure hint
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_lib_hint_when_a_bin_module_path_is_missing` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: RoundF 0s) / FAILED (1 classes) [ran] [tree 5e5339f76a66] (2026-10-15T22:32:14Z)
- (ac 1) `python3 plugin/tests/run.py test_round_f` → exit 0 · Ran 10 tests in 4.4s (1 classes, 16 at a time; slowest: RoundF 4s) / OK [ran] [tree 4a0050eed891] (2026-10-15T22:33:21Z)
- (step 1) `python3 plugin/tests/run.py test_round_f test_recall` → exit 0 · Ran 24 tests in 22.8s (6 classes, 16 at a time; slowest: Recall 23s, RoundF 5s, RedGreen 4s) / OK [ran] [tree 4a0050eed891] (2026-10-15T22:33:21Z)
- (audit self) `self: the recorded demo session's fix (T-0979), reviewed line by line and re-applied here; red then green` → a 'No such file' on plugin/bin/fm*.py gets the plugin/lib hint; other missing files don't [tree 4a0050eed891] (2026-10-15T22:33:21Z)
- (step 1) `python3 plugin/tests/run.py -k test_lib_hint_when_a_bin_module_path_is_missing` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: RoundF 0s) / OK [ran] [tree 4a0050eed891] (2026-10-15T22:33:30Z)
- (audit self) `self: the recorded demo session's fix (T-0979), reviewed line by line and re-applied here; red then green` → a 'No such file' on plugin/bin/fm*.py gets the plugin/lib hint; other missing files don't [tree 4a0050eed891] (2026-10-15T22:33:30Z)
## Log
- 2026-10-15T22:26:16Z created
- 2026-10-15T22:31:58Z focused
- 2026-10-15T22:33:31Z done
- 2026-10-15T22:33:32Z committed 26c8ac5 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- T-0262 [FEATURE M, done, 4 steps] Smarter nudges: already-covered requests, decision revisit triggers, quieter ignored hints — lesson: Text Foreman later parses for tags…
- T-0413 [FIX M, done, 3 steps] Audit diffs leave out secrets — lesson: A frozen copy of the working tree is a second place secrets live: redact at the point it's written,…
- decision 2026-10-15: Update Claude Code with its native installer (claude install latest → ~/.local/bin, which updates itself without root) and put ~/.local/bin first on…
## Plan gaps
- failed first: step 1 Bring in the recorded session's commit; run its test
## Files touched
- plugin/tests/test_round_f.py
- plugin/lib/fmrecall.py
