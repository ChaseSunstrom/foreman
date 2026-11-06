# Brainstorm — lens: simplicity

- **Run one command for all three self-gates** — CLEAN — value 3 — effort S — risk low — category: developer experience
  Why: The map lists three separate gates (`fm doctor`, `roundtrip.py`, `bench_hooks.py --runs 20`), each with its own invocation and output shape. Forgetting one is easy.
  Done when: `fm gates` runs all three and prints one line per gate plus a single pass/fail exit code, and MASTER.md names only that command.

- **Default `verify` from the test map instead of hand-written commands** — FEATURE — value 4 — effort M — risk low — category: developer experience
  Why: Round 1 had a task whose verify grepped the queue and broke when the task left it (T-0775). The map already has tests→src, and builders already run `fm check --affected`. Hand-written verifies are where mistakes get in.
  Done when: `fm task new` with no verify fills in `fm check --affected` for the planned files, and a task that touches no mapped file is asked for an explicit verify.

- **Normalise every id, list and path argument in one place** — CLEAN — value 3 — effort M — risk low — category: cli design
  Why: `fm task set` just learned `a,b` and `[a, b]` (T-0810). `fm page` needed home paths in any spelling and plain cluster ids (T-0786). The same leniency fixes keep being made one verb at a time.
  Done when: one function parses `T-817`, `817`, `t-0817`, comma and bracket lists, and `~`/relative paths. Every verb calls it, and a table test covers all spellings across all verbs.

- **Give every on-disk store one retention table** — CLEAN — value 3 — effort S — risk low — category: state
  Why: Recent commits added separate pruning rules: compact-output full texts at 7 days, snapshots skipping `by-pid`. Retention is now spread across several modules. Assumption: there are more such rules than the two I can see.
  Done when: one `retention` table lists each state directory with its age and keep rule, `fm tidy` reads only that table, and a test fails if a state directory is not in it.

- **Turn compact output on for a named noisy-command list and remove the global question** — PERFORMANCE — value 4 — effort S — risk med — category: tokens
  Why: Round 1 shipped it off pending the user's yes, with an estimated ~1.04M tokens/30 days saved. A global on/off is one more decision for the user. A fixed list (test runners, installs, builds) with the stub always naming where the full text is would settle it.
  Done when: listed commands compact by default, and any other Bash output passes through untouched. A test confirms failure lines are always kept, and one setting disables the list.

- **Collapse task statuses to now, next and later, with a reason field** — CLEAN — value 3 — effort M — risk med — category: simplicity
  Why: The open list shows `deferred`, `blocked`, `planned`, `captured` and `active`. The `deferred` tasks mostly differ in their reason text, not their behaviour.
  Done when: `fm task list` shows three groups, existing statuses map onto them losslessly, and the reason appears beside each item.

- **Install optional skill packs on first need, not by flag** — FEATURE — value 3 — effort M — risk low — category: install
  Why: The installer has about eight flags (`--security`, `--docs`, `--no-mod`, …). Assumption: most users never choose them correctly up front.
  Done when: the first request needing a security or docs skill offers a one-line install. The installer's flag list shrinks to `--no-wiring`/`--no-bypass`, and the old flags still work for scripts.

- **Add a doctor probe that names the one thing to fix, not a report** — CLEAN — value 3 — effort S — risk low — category: developer experience
  Why: Round 1 left "known gaps" as prose: the monitor's live arming and the opt-in state. Prose gaps never get re-checked.
  Done when: each known gap is a doctor probe, and a clean `fm doctor` prints one line.

- **Wild: Make each feature a removable bundle with `fm unship <feature>`** — FEATURE — value 4 — effort L — risk high — category: simplicity
  Why: Each round-1 feature (monitor, title, push, compact, page) touches a hook entry, a lib module, a doctor check, a doc line and a test. Deleting one is a manual hunt, so nothing ever gets deleted.
  Done when: `fm unship compact-output --dry-run` lists every file and line it would remove from one manifest. The real run leaves the test suite and doctor green.

- **Wild: Put a "why is this here" link on every injected line, with a delete button** — FEATURE — value 3 — effort M — risk med — category: transparency
  Why: Whispers, titles, hints and pushes all come from different places. The user's repeated "etc. etc." suggests they want less friction but can't see where each piece comes from.
  Done when: `fm why <text>` prints the file and rule line that produced a string, and `--disable` turns that source off with a note in the ledger.

- **Wild: Let a round close with five yes/no toggles and nothing else** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: The user asked for recursion repeatedly, and nobody has ticked the round-1 board. A round that ends in a short list of keep, tune or revert decisions needs no other report.
  Done when: finishing a round writes a page or prompt with at most five items, pasted answers update the queue, and unanswered items default to "keep" with an expiry.
