**Verdict:** changes needed (one MEDIUM, easy to fix). The data-not-code question comes out clean.

## lens: adversary
- MEDIUM — mods/foreman-ui/tools/replay.py:186-194,252,308 — A crafted fixture can put raw escape sequences on the user's terminal. The pane draws titles uncleaned (register.tsx:1098,1633,1715), and `_words` and `text()` pass the characters through to `sys.stdout.write` (also the diff and the `why` error tail). Repro: `fm ui --json` output with `"title":"\u001b]0;x\u0007\u001b[2J"`, then `replay.py render f.json`. — Fix: strip ESC sequences, C0/C1 and bidi characters from leaf strings in `_words` and from `why`, keeping `\n` for the split; the regex at hooks/kit.ts:586-591 is the model. `--json` is already safe, since JSON escapes the bytes. — confidence 80%

## lens: intent
- LOW — mods/foreman-ui/tools/replay.py — Plugin parity: there is no `fm` verb, `/foreman:` command or skill, or doc line for it, and the diff has no CHANGELOG or MASTER entry. It is reachable only by file path. — Add a one-line entry and a command or skill pointer, or record that other tasks own parity. — confidence 60%
- Not verifiable here: "replay beside the task timeline" and "visual QA in a forked skill context" appear nowhere in the diff. I couldn't see which steps belong to T-1534.

## lens: edge
- LOW — replay.py:153 — `subprocess.run(text=True)` decodes with the parent's locale, but the child prints non-ASCII box characters. Fix: `encoding="utf-8", errors="replace"`. — confidence 55%

## lens: maintainer
- LOW — plugin/tests/test_ui_replay.py:438-444 — `test_the_kit_test_draws_the_pane…` only greps the .tsx source for strings. It passes even if the kit test is broken. The mod's own gate in meta.json (`claude plugin test mods/foreman-ui`) is the real proof. — Keep it as a wiring check, or drop it. — confidence 70%

## Your four questions
- **Fixture as data, never as code.** Yes.
  - `load` (replay.py:255-268) uses a regex and `json.loads`. A .ts with extra code after the JSON is refused, not run.
  - `options` (127-130) passes the view as a `JSON.parse("…")` string with `ensure_ascii`, so quotes, template literals, `</x>` and `__proto__` stay data.
  - Only the in-repo synthetic `pane-busy.ts` is ever imported, by the mod's own test.
  - A crafted .ts cannot run code.
- **What replay.py runs.**
  - The argv is fixed: `["claude","plugin","test",<mkdtemp path>]`, with no fixture text on any command line and no `shell=True`.
  - The environment is the caller's own (HOME, PATH and so on) minus FOREMAN_*, CLAUDE_* and CLAUDECODE, plus TZ, LANG and LC_ALL. `claude` still reads the real `~/.claude`, so "nothing reads Foreman's state" holds only for FOREMAN_*.
  - The 120 s timeout kills `claude` itself but not any children it started.
  - The marker line is safe: the tree is JSON on one line, so a title cannot forge a second `FM-REPLAY` line.
- **Weakest link.** The criterion is met, but only as a pair. The unittest proves the tool, the layout, the data-only wiring and the diff logic, not the engine. The rendering and the determinism check run in replay.test.tsx under the `claude plugin test mods/foreman-ui` gate (meta.json:10,44). `test_settings.py:548` already follows this pattern.
  - The matrix is a regression guard, not a current proof. The pane has no TZ or locale-dependent calls, and the clock is mocked.
  - I did not run either command, so no run output supports "met".
- **Rename.** Yes, to `ui_replay.py` or `pane_replay.py`. `fm replay` (the guard verb, fmreplay.py) already owns "replay" in MASTER and CHANGELOG. The test file is already `test_ui_replay`. Do it before docs cite the path.

## Acceptance criteria
- Pane renders from a fixture with no live session, and two runs are identical: met by the mod's gated kit test plus the twin tool. The verify command alone does not reach the engine. Not run here.

## Implicit decisions
- The fixture format is JSON after `export default`.
- The environment is UTC and C.UTF-8, with Kiritimati and de_DE for the matrix.
- The text render is approximate; `--json` is exact.
- `press` objects are dropped from the frame, so changes inside them are not compared.

## Not checked
Running claude or the tests, and the engine's own escape handling.

**Noticed:** none
