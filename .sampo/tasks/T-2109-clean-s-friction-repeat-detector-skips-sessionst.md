---
id: T-2109
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-30T06:31:05Z
updated: 2026-10-30T07:57:59Z
base: 5c8443563fd76509e27c1a42695a683198a2d0e0
base_tree: 1fc34cb7c2a0fe4796500a3ee2da8bebd0a144fa
plan0_at: 2026-10-30T07:46:07Z
plan0_scope: []
verified: strong
---
# CLEAN S: friction repeat detector skips SessionStart/UserPromptSubmit…
## Raw request
> CLEAN S: friction repeat detector skips SessionStart/UserPromptSubmit (fmfriction.py:240) so the biggest injection (~1.9k chars x 47 runs) is never flagged; add a digest line for keys averaging over ~1500 chars per injection from budget (fmfriction.py:229)
## Interpretation
fm friction's digest never flags a big per-turn injection: the repeat line skips SessionStart/UserPromptSubmit (they fire every turn). Add a line naming any hook note averaging over 1,500 characters per injection, any event.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm friction lists a note averaging over 1,500 chars per injection (SessionStart included) and not one under it — verify with `python3 plugin/tests/run.py test_friction`
## Non-goals
## Approach (options → choice → why)
chosen: one digest line from the existing budget dict (count, chars) — avg = chars/count > 1500. rejected: lifting the SessionStart/UserPromptSubmit skip (every-turn notes would all read as repeats); a size cap in the hooks (hook-context limit already covers >10 KB).
## Risks and rollback
## Execution prompt
## Steps
1. [x] test first, then the digest line, docs
## Resume here
<!-- auto -->
- 2026-10-30T07:50:07Z steps 1/1 done
- git: foreman/build; 4 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmfriction.py, plugin/tests/test_friction.py
- touched since last checkpoint: CHANGELOG.md, MASTER.md, plugin/lib/fmfriction.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/critique-genesis.md, ~/.claude/projects/-home-<user>--claude-foreman/memory/github-ssh-443.md
## Docs impact
MASTER.md fm friction line, CHANGELOG Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_friction` → ✗ exit 1 · Ran 16 tests in 4.9s (5 classes, 16 at a time; slowest: Friction 5s, UserPromptSubmit 1s, BoardIdeas 0s) / FAILED (1 classes) [ran] [tree 1fc34cb7c2a0] (2026-10-30T07:45:53Z)
- (step 2) `python3 plugin/tests/run.py test_friction test_docs` → exit 0 · Ran 96 tests in 8.2s (26 classes, 16 at a time; slowest: Fences 8s, Friction 5s, TaskLifecycle 1s) / OK [ran] [tree b45b93ae6b4a] (2026-10-30T07:46:25Z)
- (step 1) `python3 plugin/tests/run.py test_friction test_docs` → exit 0 · Ran 96 tests in 8.2s (26 classes, 16 at a time; slowest: Fences 8s, Friction 5s, TaskLifecycle 1s) / OK [ran] [tree b45b93ae6b4a] (2026-10-30T07:46:48Z)
- (ac 1) `python3 plugin/tests/run.py test_friction` → exit 0 · Ran 16 tests in 4.9s (5 classes, 16 at a time; slowest: Friction 5s, UserPromptSubmit 1s, BoardIdeas 0s) / OK [ran] [tree b45b93ae6b4a] (2026-10-30T07:55:21Z)
- (audit edge) `self-review of a 3-line digest addition: the average uses integer division only for display; zero-count keys skipped; MAX_LINES caps it; the new test pins a 1,900-char every-turn note named and a 300-char one not` → n=0 guarded by 'if n'; exactly 1,500 avg not named (strict >) [tree b45b93ae6b4a] (2026-10-30T07:55:21Z)
- (audit self) `self-review of a 3-line digest addition: the average uses integer division only for display; zero-count keys skipped; MAX_LINES caps it; the new test pins a 1,900-char every-turn note named and a 300-char one not` → no findings [tree b45b93ae6b4a] (2026-10-30T07:55:21Z)
## Log
- 2026-10-30T06:31:05Z created
- 2026-10-30T06:31:09Z set type=CLEAN, tier=S
- 2026-10-30T07:25:40Z planned: it has criteria and steps
- 2026-10-30T07:46:06Z focused
- 2026-10-30T07:55:23Z done
- 2026-10-30T07:55:25Z committed e9654d20 (3 files)
- 2026-10-30T07:55:34Z guard authorization added: publish
- 2026-10-30T07:57:59Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1800 [PERFORMANCE M, done, 3 steps] Foreman reasons ahead: names why usage burns, unasked (session start, fm doctor, fm digest) — lesson: Account-wide scans hung on a …
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- T-1797 [FEATURE M, done, 3 steps] CC 2.1.305-2.1.312 adoption: give fm-reviewer/fm-recon an autoCompactWindow; fm doctor poi — lesson: Subagent transcripts carry their p…
- decision 2026-10-06: Desktop app architecture: no daemon — the Tauri app drives fm --json locally or over ssh (Tailscale SSH) per device; agent sessions are supervised b…
## Plan gaps
- failed first: step 1 test first, then the digest line, docs
## Files touched
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmfriction.py
