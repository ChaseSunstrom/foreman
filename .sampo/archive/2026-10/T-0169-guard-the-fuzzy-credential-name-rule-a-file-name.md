---
id: T-0169
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-03T08:54:00Z
updated: 2026-10-03T09:05:51Z
base: 8fb3cb78446c3f7e9904b7920aee3b09c8d7f3ab
base_tree: c025d7b27fcbe3a334a403232c5c5f4c02261d74
verified: strong
---
# Guard: a secret-sounding file name under the scratchpad or /tmp isn't a credential; its real path still is checked
## Raw request
> Guard: the fuzzy credential-name rule (a file named secrets.txt) shouldn't fire for paths strictly under the scratchpad or /tmp; realpath variants keep symlinks into ~/.ssh caught
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] Writing <scratchpad>/secrets.txt is allowed; secrets.txt in the repo or home, and a scratch symlink into home, stay blocked as credentials — verify with `python3 plugin/tests/run.py -k test_a_secret_sounding_name`
- [x] All gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test
2. [x] Skip the name-only rule under scratch roots
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_a_secret_sounding_name` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: ScratchNames 0s) / FAILED (1 classes) [ran] [tree 35ecf5f6c2fc] (2026-10-03T09:04:56Z)
- (step 1) `python3 plugin/tests/run.py -k test_a_secret_sounding_name` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: ScratchNames 0s) / OK [ran] [tree 75f1f09cbe7f] (2026-10-03T09:05:01Z)
- (step 2) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 48 tests in 1.1s (18 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, GitDestructive 0s) / OK [ran] [tree 75f1f09cbe7f] (2026-10-03T09:05:02Z)
- (step 3) `grep -q T-0169 CHANGELOG.md` → exit 0 · (no output) [ran] [tree 485fbccd63d4] (2026-10-03T09:05:51Z)
- (ac 1) `python3 plugin/tests/run.py -k test_a_secret_sounding_name` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: ScratchNames 0s) / OK [ran] [tree 485fbccd63d4] (2026-10-03T09:05:51Z)
- (ac 2) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 09:05 UTC); cached (fm check --fresh reruns) [ran] [tree 485fbccd63d4] (2026-10-03T09:05:51Z)
- (audit adversary) `self: red→green on the same command; only the name-only rule is skipped under scratch roots; .env, key files and credential folders still count anywhere (test); classify_write checks the real path too, so a scratch symlink into home stays blocked (test); the differential test passes` → the exemption needs the path and its realpath both under a scratch root to pass; scratch roots come from the hook payload and fixed system temp dirs, not from the command [tree 485fbccd63d4] (2026-10-03T09:05:51Z)
- (audit self) `self: red→green on the same command; only the name-only rule is skipped under scratch roots; .env, key files and credential folders still count anywhere (test); classify_write checks the real path too, so a scratch symlink into home stays blocked (test); the differential test passes` → no findings [tree 485fbccd63d4] (2026-10-03T09:05:51Z)
## Log
- 2026-10-03T08:54:00Z created
- 2026-10-03T09:04:51Z planned from capture
- 2026-10-03T09:04:52Z focused
- 2026-10-03T09:05:51Z done
- 2026-10-03T09:05:51Z committed 2cba7ef (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- research t0018-r6-r7-adversary-edge: MEDIUM** — EDGE lens — `~/.claude/foreman/plugin/lib/fmhooks.py:360-364` vs `~/.claude/foreman/plugin/lib/fmcore…
- research t0018-r3-adversary: `). `_read` (fmsync.py:31-33) does a plain `open(path)`, which follows the symlink. The `decisions.md` (fmsync.py:109-114) and `research/*.m…
- research T-0161-review: Verdict: changes needed.** `_track_vars` still has bypasses, and one of them is the same class T-0161 set out to close. I traced each through `_s…
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- A name-based heuristic should know where it doesn't apply: in a scratch folder a file's name is the author's label, not a hint about its contents.
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
