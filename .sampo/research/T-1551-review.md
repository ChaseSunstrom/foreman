**Verdict: changes needed.** There are two ways to crash `fm lsp` with crafted input, and one test that cannot fail. I could not run anything (read-only tools only), so every finding comes from reading the code in `~/.claude/foreman/.claude/worktrees/agent-a39aca9847c6a08bc`.

## lens: adversary
- MEDIUM — plugin/lib/fmintegrations.py:253 — `send()` calls `json.dumps(..., ensure_ascii=False).encode("utf-8")`. A lone surrogate from the client (`"uri":"file:///\ud800"`, an `"id":"\ud800"` on an unknown method, or one in a brief's `id:`) makes `.encode` raise `UnicodeEncodeError`. `publish()` only guards `gaps()`, not `send`, so `serve()` dies. — Fix: use the default `ensure_ascii=True` on the wire, or encode with `errors="replace"`. — high
- MEDIUM — plugin/lib/fmintegrations.py:237 — `int(v)` on a Content-Length of more than 4300 digits (`Content-Length: 1111…` at 5000 digits, under the 64 KB readline cap) raises `ValueError`. `_frames` has no guard, so `fmcli.main` reports it as "state looks corrupt" and exits 4. — Fix: require `len(v.strip()) <= 10` before `int`, or wrap the parse in a try. — high
- MEDIUM — plugin/lib/fmintegrations.py:205,212 — `c._AC_RE` and `c._STEP_RE` (fmcore.py:1082-1083) end in a lazy `(.*?)` followed by `\s*$`, which backtracks quadratically. A document with `## Steps` and a line `1. [ ] ` plus 100k spaces plus `x` ties up the stdio server for minutes. A frame may be up to 32 MB and nothing bounds the work. — Fix: cap the line length that `gaps()` examines (for example `line[:2000]`), or strip the line before matching. — plausible (derived, not run)
- LOW — plugin/lib/fmintegrations.py:139 — `fm timeline` prints with `ensure_ascii=False`, so a C1 character (U+009B) in a ledger command string reaches the terminal raw. `fm glance` already uses `ensure_ascii=True`. — Fix: use the same setting here. — medium

## lens: edge
- LOW — plugin/lib/fmintegrations.py:49 — `t0` and `t1` are the first and last events in ledger order. If timestamps are not monotone across sessions, the task span can be shorter than its children. — Fix: use `min` and `max` over the timestamps. — medium
- LOW — `fm glance` and `fm timeline` — `fmcli.main` runs `_sync_in` first, which writes under a lock when `fm sync` has incoming changes, so "read-only" is not strictly true. Separately, a corrupt brief makes `state_dict` raise and `glance` print nothing (exit 4) where a bar expects a line. — Fix: have `glance` catch `ValueError` and print `class: "error"`. — medium

## lens: maintainer
- MEDIUM — plugin/tests/test_integrations.py:37-83 — The comment says the fixture is an unredacted older line, but it writes `Authorization: [REDACTED] which is already redacted. `abc123secretvalue` appears nowhere except `assertNotIn`, and `assertIn("[REDACTED]")` passes from the fixture alone. Deleting `c.redact` from `_clean` would not fail the test. — Fix: write `curl -H 'Authorization: [REDACTED]'` into the fixture. — high
- LOW — plugin/tests/test_integrations.py (outside-project glance test) — It lists only the top level of `$HOME`, so a write under `state/` would go unnoticed. — Fix: compare an `os.walk` snapshot. Also add LSP tests for a surrogate uri and a huge Content-Length. — high
- LOW — plugin/lib/fmcli.py:5428 — `add("wiring",lazy(` lost its space, and its continuation lines are now misaligned. — Fix: restore the space. — high
- LOW — CHANGELOG.md — There is no T-1551 entry, though every neighbouring task has one and MASTER.md changed. — Fix: add the line. — high

## lens: intent
- MEDIUM — plugin/lib/fmintegrations.py:152-163 — `glance` prints the title (and the tooltip) in a sensitive project. `fm timeline` hides words there, and `fm mcp` serves nothing from it (fmmcp.py:151). The glance text is meant for status bars, which get screen-shared. — Fix: in a sensitive project, blank the title and tooltip, keeping the id and counts. — medium

## Acceptance criteria
- Perfetto JSON valid, `glance` prints one JSON line, LSP answers `initialize` and publishes a diagnostic: met on a read of the code and tests, but not run. The tests cover all three paths.
- Desk card and SVG charts (step 4): not built, and MASTER.md says so. The request asked for five integrations, so this leaves it two short.

## Your specific questions
- **Secret-looking value:** it is a fake negative-assertion string, not a real secret. Output redaction is real in the code (`_clean` and `c.redact`), but the test does not exercise it (see the maintainer finding).
- **`fm lsp` and ports:** no socket or http imports, and a test asserts that. It does not survive hostile input, per the two adversary crashes and the regex stall.
- **Timeline and glance state:** private mode drops all words except the project slug in `process_name` and `foreman.project` (LOW). Outside a project both use `resolve(create=False)` and create nothing.

## Implicit decisions
- Stdlib only; `fm lsp` runs on stdio.
- Tracks are named after session ids.
- The OTLP trace id is a hash of project and task.
- `lsp` exits 1 when no shutdown was received.
- Diagnostic severities: warning for a ticked item with no evidence, info for an unticked one.

## Not checked
I did not run the tests or the full suite, the Perfetto UI import, or any other `fm` verb.

**Noticed:** capture a follow-up task for the unbuilt desk card and animated SVG charts (b094 a096). Separately, `c._AC_RE` and `c._STEP_RE` (fmcore.py:1082) backtrack quadratically on every brief parse.
