# Brainstorm — lens: simplicity

- **Ship one thin mod that replaces the statusline wrapper and `fm watch` with a single Pane + AbovePrompt band** — FEATURE — value 5 — effort M — risk med
  Why: the pack shows three overlapping UIs (statusLine wrapper script, cached line/badge files, curses `fm watch` in a second terminal). One mod reading `fm state --json` covers all of them. Assumption: `fm state --json` already has the needed fields.
  Done when: with the mod installed, `claude plugin test` mounts the Pane and AbovePrompt band showing the active task, stage and steps, and the classic statusline is not needed. Classic path is unchanged when mods are unavailable.

- **Make the mod a pure renderer with no logic of its own** — CLEAN — value 4 — effort S — risk low
  Why: the constraint says mods must call `fm` via `$.process.run`. Keeping all rules in Python avoids two implementations drifting apart. Assumption: one `fm state --json` call per redraw is cheap enough.
  Done when: `register.tsx` contains no stage or gate logic. A grep finds only `$.process.run` calls to `fm`, and a mock-driven test passes.

- **Fix `fm task show --json` and the `--section` bugs (T-0076, T-0075, T-0080)** — FIX — value 5 — effort S — risk low
  Why: a mod UI needs complete JSON (criteria, steps, depends), and the planning friction is listed as a known limitation. Fuzzy section-name matching also removes the exact-name errors.
  Done when: `show --json` returns criteria, steps and depends, and `set --section Approach` fills the existing 'Approach (options → choice → why)' section while keeping evidence links.

- **Collapse planning into one `fm task plan` call that takes all sections at once** — FEATURE — value 4 — effort M — risk med
  Why: planning currently takes several `fm` calls with exact section names, which costs tokens and causes errors. Assumption: the sections can be passed as one JSON or markdown blob.
  Done when: a single call fills every planning section and the stage moves to ready. A test checks the result against the same fixture built via the old calls.

- **Drop the cached state.line, progress.line and badge.txt files in favour of rendering from one state snapshot** — CLEAN — value 3 — effort M — risk med
  Why: three cached derived files plus the title and OSC output are redundant. Assumption: no external script reads them besides the statusline wrapper.
  Done when: only the one snapshot remains, the statusline, title and badge are derived from it, and the full test suite passes.

- **Use `tool.call` in the mod to enforce the guard and scope in-process, skipping the Python hook when the mod is active** — PERFORMANCE — value 3 — effort L — risk high
  Why: each classic hook costs a Python process (~29 ms), and Bash edits are invisible to scope. The mod sees every tool call. Assumption: classic hooks can detect that the mod is active without double-firing.
  Done when: with the mod active, a dangerous Bash command is denied once, with no duplicate hook run, and the hook bench shows fewer process spawns.

- **Fix scoping bugs T-0074, T-0078 and T-0079 so gates look only at the task's own changes** — FIX — value 4 — effort M — risk low
  Why: false positives on the tree-wide scope check and on Foreman's own regex literals add noise to a UI that should show only real signals.
  Done when: a fixture with unrelated dirty files and a regex literal produces no scope or security flag for the task.

- **Delete `fm watch` curses code once the Pane reaches parity** — CLEAN — value 3 — effort S — risk med
  Why: the Pane duplicates the curses dashboard. Assumption: the classic fallback (`claude -p`, older builds) can use the statusline alone.
  Done when: fmwatch is removed or reduced to a thin `fm state` printer, and `fm doctor` and the tests pass.
