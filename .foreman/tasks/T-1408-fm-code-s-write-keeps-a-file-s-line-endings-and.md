---
id: T-1408
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-10-21T19:57:59Z
base: 7f6098f3c5b0e0c816d966f40612f5ee7a60b81a
base_tree: 4e954045e1103b1706bd8a2ef3dc2b9bed295793
plan0_at: 2026-10-21T19:43:59Z
plan0_scope: []
verified: strong
---
# fm code's write and edit keep a file's line endings and refuse a non-UTF-8 target; option-shaped paths are refused cleanly
## Raw request
> FIX: fm code's write keeps a file's line endings and refuses a non-UTF-8 target instead of rewriting it; option-shaped values fuzzed through fm's path options (S21, B24)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: the model writing LF text over a CRLF file leaves it CRLF; a write over a binary file is refused; '--x' and '-' given as paths are refused cleanly
## Interpretation
fm code's write opens the target in text mode and rewrites it as UTF-8 with LF, so a CRLF file becomes LF throughout (a diff of every line) and a binary file is silently corrupted; edit reads with universal newlines and writes LF back, same problem. Option-shaped paths ('--x', '-') can confuse tools later in the run (git, the verify).
## Assumptions (confidence)
## Acceptance criteria
- [x] the model writing or editing LF text over a CRLF file leaves it CRLF; a write or edit over a binary or non-UTF-8 file is refused with the reason; '--x' and '-' given as an action path are refused cleanly — verify with `python3 plugin/tests/run.py test_code_write_hygiene`
## Non-goals
## Approach (options → choice → why)
Options: (A) detect from the existing bytes: refuse non-UTF-8/NUL, preserve CRLF when the file's lines use it (chosen: matches what an editor does, small); (B) .gitattributes-driven eol (heavier, most repos have none); (C) normalise everything to LF (rewrites unrelated lines). A new file keeps LF. Paths: refuse '-' and leading '-' in Run.path, the one place every action resolves a path.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests in plugin/tests/test_code_write_hygiene.py driving Run.write/Run.edit through a fake model run (see test_code.py's model fixtures)
2. [x] in fmcode Run.write/Run.edit: read the existing file as bytes; refuse when it doesn't decode as UTF-8 (or holds NUL); when it uses CRLF, write the new text with CRLF (newline='' and explicit conversion; edit matches old text with endings normalised); Run.path refuses a path that starts with '-' or is '-'
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_code_write_hygiene 2>&1 | tail -15` → ✗ exit 1 · Ran 1 tests in 9.1s (1 classes, 16 at a time; slowest: WriteHygiene 6s) / FAILED (1 classes) [ran] [tree a4b6e75d86f1] (2026-10-21T19:45:13Z)
- (step 1) `python3 plugin/tests/run.py test_code_write_hygiene` → ✗ exit 1 · Ran 1 tests in 7.0s (1 classes, 16 at a time; slowest: WriteHygiene 7s) / FAILED (1 classes) [ran] [tree a4b6e75d86f1] (2026-10-21T19:45:23Z)
- (ac 1) `python3 plugin/tests/run.py test_code_write_hygiene 2>&1 | tail -15` → exit 0 · Ran 1 tests in 5.5s (1 classes, 16 at a time; slowest: WriteHygiene 5s) / OK [ran] [tree 7db1620042b9] (2026-10-21T19:45:42Z)
- (step 2) `python3 plugin/tests/run.py test_code_write_hygiene` → exit 0 · Ran 1 tests in 6.9s (1 classes, 16 at a time; slowest: WriteHygiene 6s) / OK [ran] [tree 4fb90d92b45f] (2026-10-21T19:46:00Z)
- (step 1) `python3 plugin/tests/run.py test_code_write_hygiene test_code_envelope` → exit 0 · Ran 4 tests in 8.0s (2 classes, 16 at a time; slowest: Envelope 8s, WriteHygiene 5s) / OK [ran] [tree 8e167b40eb67] (2026-10-21T19:54:13Z)
- (step 2) `python3 plugin/tests/run.py test_code_write_hygiene test_code_envelope` → exit 0 · Ran 4 tests in 8.7s (2 classes, 16 at a time; slowest: Envelope 8s, WriteHygiene 5s) / OK [ran] [tree 8e167b40eb67] (2026-10-21T19:54:22Z)
- (ac 1) `python3 plugin/tests/run.py test_code_write_hygiene` → exit 0 · Ran 1 tests in 5.1s (1 classes, 16 at a time; slowest: WriteHygiene 5s) / OK [ran] [tree 8e167b40eb67] (2026-10-21T19:54:36Z)
- (audit intent) `self: read Run.path, Run.existing, Run.edit, Run.write — existing() decides before the guard runs (binary/NUL, non-UTF-8, non-regular, over READ_BYTES refused; CRLF by majority), write keeps an existing file's endings with newline='', edit converts the model's LF old/new text to CRLF for a CRLF file` → LF text written or edited over a CRLF file leaves it CRLF; a binary or non-UTF-8 target is refused with the reason; '-' and '--x' are refused cleanly (test_code_write_hygiene) [tree 8e167b40eb67] (2026-10-21T19:54:36Z)
- (audit edge) `self: read Run.path, Run.existing, Run.edit, Run.write — existing() decides before the guard runs (binary/NUL, non-UTF-8, non-regular, over READ_BYTES refused; CRLF by majority), write keeps an existing file's endings with newline='', edit converts the model's LF old/new text to CRLF for a CRLF file` → a mixed-ending file goes by majority, so an edit spanning its LF part reports 'not found' rather than corrupting; a file over READ_BYTES can't be rewritten (the model couldn't read it either); lone '\r' left as is [tree 8e167b40eb67] (2026-10-21T19:54:36Z)
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-21T19:43:43Z planned from capture
- 2026-10-21T19:43:45Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1408.builder.md
- 2026-10-21T19:43:58Z focused
- 2026-10-21T19:51:38Z merged worktree-agent-ae9663578f3d7a0c0 (2 file(s))
- 2026-10-21T19:51:54Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae9663578f3d7a0c0
- 2026-10-21T19:54:03Z focused
- 2026-10-21T19:57:59Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-fm-anthropic-catalogue: Source: research/brainstorm-20261021-120257 (fm ideas, 10 lenses, 4 rounds, 3 deepened, --seen every earlier ideas.md: 520 ne…
- research T-1089-review: Verdict: changes needed.** I found no guard bypass. I could not run anything, because this audit is read-only, so everything below is from readin…
- T-0702 [FEATURE M, dropped, 3 steps] Frontier 02 — Context firewall and cheap reader
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
## Why not caught
none: text-mode writes were never tested against CRLF or binary targets
## Lessons
- A tool that rewrites files must read the existing bytes first and keep their encoding and line endings, or every edit becomes a whole-file diff
## Plan gaps
- failed first: step 1 failing tests in plugin/tests/test_code_write_hygiene.py driving Run.write/Run.edit through a fake …
## Files touched
- plugin/tests/test_code_write_hygiene.py
- plugin/lib/fmcode.py
- CHANGELOG.md
- plugin/tests/test_code.py
- plugin/tests/test_code_truncation.py
