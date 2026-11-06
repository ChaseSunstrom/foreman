**Verdict:** changes needed. The commands/hooks listing meets both acceptance criteria on a read of the code. The note's delivery channel and its 1500-character cap both undercut the "name hostile files" intent.

I could not run the tests, so the criteria below rest on reading the code.

## lens: intent
- MEDIUM — plugin/lib/fmhooks.py:401-402 — The note is meant for the user ("review before trusting the repo") but goes only into `additionalContext`, which is model context. The user sees it only if the model repeats it, and the digest is recorded either way, so it is never shown again. Fix: also send it as `systemMessage`, joined with `news` near line 417, or tell the model to relay it. — medium
- LOW — plugin/lib/fmhooks.py:346-356 — A headless `fm run` session (`_headless`) gets the note and records the digest, so the user's interactive session never sees it. Fix: skip the repo note and the digest write when `_headless()`. — medium

## lens: adversary
- MEDIUM — plugin/lib/fmplugins.py:267 — `c.fit(note, 1500)` cuts from the end, and "not read" and "malformed JSON" come last. The header is about 235 characters, commands up to about 400, MCP servers up to about 400, allow rules up to 8×90 = 720. A hostile repo pads a small readable `settings.json` with long entries and an oversized `settings.local.json`, and the warning that its hooks were never read is truncated away. Reproducer: 4 commands of 90+ characters, 4 MCP servers, 8 long allow rules and a 300 KB `settings.local.json` push the warning past the cap. `test_many_entries_stay_under_the_cap` checks only the length. Fix: put unread and malformed first, or cap each group so the total fits. — high
- MEDIUM — plugin/lib/fmplugins.py:245-247, :254-258 — The credential-bearing commands (`apiKeyHelper`, `awsAuthRefresh`, `statusLine`) and the `enableAllProjectMcpServers` line are appended after the event hooks. A repo with 4 or more ordinary hooks pushes them into "and N more". The `enableAll…` line is also counted as a "command". Fix: add the settings-level entries before the hook events, or give them their own group. — high
- LOW — plugin/lib/fmplugins.py:205-250 — Not covered: project `env` (for example `ANTHROPIC_BASE_URL`), `fileSuggestion` command, `enabledPlugins` and `extraKnownMarketplaces`. These are the same class as the `apiKeyHelper` just added. Fix: list them, or document the gap in the CHANGELOG. — medium

## lens: edge
- LOW — plugin/lib/fmhooks.py:353-358 — The digest is written before the note is delivered. If a later step raises, for example `session_context` with no try/except, the note is lost and never repeated. Fix: write the digest only after `out` is built. — medium
- LOW — plugin/lib/fmplugins.py:223 — For unread or malformed files the hash includes `mtime_ns`, so a `git checkout` or touch re-notes unchanged hostile files. This is acceptable; I mention it only for awareness.

## lens: operator
ok. CHANGELOG.md:4 matches the code.

## lens: maintainer
- LOW — plugin/tests/test_cloned_config.py — No test covers `awsAuthRefresh`, `awsCredentialExport`, `otelHeadersHelper` or `statusLine`. The comment "same files back are named again" (fmhooks.py:352) has no test for deleting and restoring the files. Fix: add one parametrised case and one delete-then-restore case. — high
- LOW — plan hygiene — The fmhooks.py hunk and the test file serve no named step; only step 2 (fmplugins.py) is named. Add a wiring step to the plan.

## Acceptance criteria
- Committed hooks and an MCP server give one note, not again until the files change: met in code, fmhooks.py:349-353, hash at fmplugins.py:228. Not executed.
- Symlink out of the repo, oversized file and malformed JSON are named, never read: met in code. `_spec_file` confines the path (fmplugins.py:184-186) and `isfile` comes first, so a FIFO cannot block. Not executed. Caveat: the naming can be truncated (see adversary).

## Implicit decisions
- Notes go in `additionalContext`, appended after the budgeted context.
- The hash is of parsed JSON, so whitespace edits do not re-note.
- 256 KB cap, 1500-character note cap, 90 characters per item, 4 commands, 4 servers, 8 allow rules shown.
- The digest is stored in `meta["repo_config"]`, and it becomes None when the files disappear.
- `p.root` is the git root, and a worktree shares one meta with the main tree.

## Not checked
Whether a `.claude` folder in a subdirectory of the git root is missed. I did not run the tests or confirm Claude Code's visibility of `additionalContext`.

**Noticed:** none
