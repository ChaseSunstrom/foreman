# Brainstorm — lens: simplicity

- **Make the first-run experience one command and one line of output** — FEATURE — value 5 — effort M — risk low — category: simplicity
  Why: New-user evidence A1–A8: abstract README, `fm` not on shell PATH, `fm init` prints a random slug, a fresh install fails its own `fm doctor` and prints 40 lines. Idea pile has many install ideas but none that collapses the whole first run into one verdict line.
  Done when: in a clean HOME, `install.sh` then `fm` (no args) in a new repo prints at most 5 lines, ends with the single next command, and `fm doctor` exits 0 with one line.

- **Collapse the CLI to a "core 8" help and a forwarding table for the rest** — CLEAN — value 4 — effort M — risk med — category: simplicity
  Why: `fm --help` is 231 lines/16 KB with ticket numbers (A4); 108 verbs, 46 never run by Claude in 11 days (C). Prior ideas say "hide long tail" but not the mechanism: a forwarding table so merged verbs (`inspect`, `stats`, `auto`) keep old names working with a one-line "now `fm inspect sym`" hint.
  Done when: `fm --help` is ≤ 20 lines with no `T-` ids, and every previously valid verb still runs (test iterates the old verb list).

- **Let `fm task new` adopt a matching capture and print valid values** — FIX — value 4 — effort S — risk low — category: simplicity
  Why: A6: `capture` then `task new` duplicates; `--help` lists no valid `--type/--tier`.
  Done when: after `fm capture "x"`, `fm task new "x"` reuses the capture (one task, not two), and `fm task new --help` shows allowed types, tiers and an example.

- **Fold child tasks into their parent in digest and grading** — FIX — value 3 — effort S — risk low — category: simplicity
  Why: C: 159 of 370 last-week done tasks show as "ungraded" because they were folded; the digest looks worse than reality.
  Done when: `fm digest` reports folded tasks under their parent's grade and the ungraded count for a fixture with folded children is 0.

- **Stop `fm repeats` suggesting single test modules as gates** — FIX — value 3 — effort S — risk low — category: simplicity
  Why: C: the suggestion is explicitly "bad advice"; the top repeated command is the whole-suite runner.
  Done when: given a ledger with repeated `unittest tests/test_x.py` and a whole-suite command, `fm repeats` suggests only the whole-suite command.

- **Detect the test runner at first `fm check` and offer it as the gate** — FEATURE — value 4 — effort S — risk low — category: simplicity
  Why: A7: no gates configured and no detection of unittest/pytest.
  Done when: in a repo with `tests/` and pytest config, `fm check` with no gates prints the detected command and one yes/no line to save it; answering yes persists it.

- **Merge the seven `_git` helpers and three child launchers into one tested module each** — CLEAN — value 3 — effort M — risk med — category: simplicity
  Why: D: seven copies of `_git`, three `claude -p` launchers; duplicated behaviour drifts (e.g. the lane base and pipe fixes needed in several places).
  Done when: grep finds one `_git` definition and one child-launch function in `plugin/lib`, and the full suite plus `roundtrip.py` pass.

- **Make safe-by-default install: plan, show diff, bypass opt-in** — SECURITY — value 5 — effort M — risk med — category: simplicity
  Why: A2: bypassPermissions, outputStyle, autocompact, statusline wrapper and 20 deny rules applied with one vague line. A trust ask this large blocks adoption; rivals only add commands (B).
  Done when: `install.sh --plan` prints each `~/.claude` change itemised without writing; default install leaves `defaultMode` unchanged unless `--bypass` is passed; uninstall restores the prior values exactly (byte-compare test).

- **Wild: Add `fm one`, the whole interface for week one** — FEATURE — value 3 — effort M — risk med — category: simplicity
  Why: assumption: newcomers need one verb that infers the next action (capture, plan, finish) from state, since 11 jargon terms (A11) are the real barrier. Wild.
  Done when: in a fresh repo, repeated `fm one` calls walk init → capture → plan → finish → done on a fixture without any other verb typed.

- **Wild: Add `fm eject`, leaving plain markdown and no Foreman** — FEATURE — value 3 — effort M — risk low — category: simplicity
  Why: assumption: an easy exit lowers the trust cost of install (A2, A10), and uninstall currently leaves residue. Wild.
  Done when: `fm eject` writes the queue and lessons as readable markdown in the repo, removes all wiring, and a second run reports nothing left behind.

- **Wild: Hold a monthly delete-only round that may not add code** — CLEAN — value 4 — effort M — risk med — category: simplicity
  Why: D: 28k lines, rarely used clusters (~2k bench stack, ~1.5k session layer); rounds 2–3 came back dry for additions, so subtraction is the productive direction. Wild because it constrains the round itself.
  Done when: a round whose diff has net negative lines closes with the suite and doctor green, and the changelog names each removed verb with its replacement.

- **Wild: Print a "quiet because" line whenever Foreman injects nothing** — FEATURE — value 2 — effort S — risk low — category: simplicity
  Why: assumption: silence is indistinguishable from broken hooks for a newcomer; one line makes calm legible. Wild.
  Done when: a hook turn with no injection records one line in the status view stating the reason, and `fm status` shows it.

- **Gloss `fm status` and drop ticket numbers from user-facing text** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: A5/A11: empty-project status shows "Drive: on" unexplained; help text carries `T-` ids.
  Done when: a lint test fails if any CLI help or status output contains `T-\d{4}` or an unglossed term from the jargon list.
