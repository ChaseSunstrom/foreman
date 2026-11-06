# Brainstorm — lens: simplicity

- **Turn mechanical skills into one-line stubs over `fm` commands** — CLEAN — value 4 — effort S — risk low
  Why: the pack says skills are long markdown and a weak spot for context cost. Status, tidy, doctor, resume and next are procedures the code already knows (assumption: their skill text mostly restates the command's steps). Each skill body becomes "run `fm X --apply`, relay the summary", and the command owns the logic.
  Done when: those five skill files are ≤ 300 chars each, and a replayed status/tidy/doctor session gives the same state changes with fewer tokens.

- **Add `fm gates TYPE TIER` as the single gate matrix** — CLEAN — value 4 — effort M — risk med
  Why: the required evidence, audits, docs impact and lesson rules are spread across `fm task done`, the rules text (~5.2k of 6k chars) and the skills. One table in code drives the enforcement, the `fm gates` output and the rules, which then say only "run `fm gates`".
  Done when: rules text has no per-tier gate prose, and a test asserts that the `done` checks equal the table row for every TYPE×TIER pair.

- **Hide the long tail of the CLI behind `fm help --all`** — CLEAN — value 3 — effort S — risk low
  Why: the pack lists about 20 commands, and Claude pays tokens whenever it reads help output. Default help shows the 6 loop commands (focus, check, done, ideas, status, next) at ≤ 600 chars. The rest show under `fm help --all`.
  Done when: `fm` with no args prints ≤ 600 chars, and every command is still reachable and documented in `--all`.

- **Add `fm step` to run the next deterministic transition in one call** — FEATURE — value 4 — effort M — risk med
  Why: the loop sequence (focus → check → audit prep → done) costs a turn per command, and the user wants fewer turns and tokens. `fm step` reads the same Next function as the hooks and runs any purely mechanical step. It stops at the first step that needs judgment and prints a ≤ 5-line result. (Assumption: several transitions are mechanical.)
  Done when: on a fixture S task, focus through done takes ≤ 3 tool calls where it took ≥ 6, and `fm step` never runs a step that needs judgment.

- **Derive queue, inbox and status from brief frontmatter with no index files** — CLEAN — value 3 — effort M — risk med
  Why: the pack says only `fm` writes state and that a crash-safety/fsck idea is pending. Each derived index is another thing that can drift. Deriving views on read, with the mtime cache used only as a speedup, removes a whole class of desync bugs. (Assumption: index or order files exist separately from the briefs.)
  Done when: deleting every non-brief state file, other than logs, leaves queue order and status unchanged, and hook p50 stays ≤ 30 ms with 500 briefs.

- **Add a complexity ratchet test for Foreman itself** — CLEAN — value 3 — effort S — risk low
  Why: at ~8,000 lines and the many ideas queued for implementation, the plugin will grow. A committed `ratchet.json` holds line counts, command count, skill bytes and rule chars. A test fails when any value rises without the file being edited in the same change. Lowering a value is free.
  Done when: adding an undeclared command makes `fm check` fail with the exact ratchet line to update.

- **Add one `profile` setting (lean/standard/strict) read by every gate and injection** — FEATURE — value 3 — effort M — risk med
  Why: token spend is the user's main complaint, and the knobs for audits, recall, related sections, brainstorm rounds and pack size are scattered. A single profile table replaces them, with `lean` as the default for S/M. `fm run` can pick the profile per task.
  Done when: switching profile changes the audit, recall and brainstorm settings from one table, and a `lean` run of a fixture task uses measurably fewer tokens than `strict`.
