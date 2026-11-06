# Brainstorm — lens: simplicity

- **Merge four review items into one `fm second` primitive** — CLEAN — value 4 — effort M — risk low — category: consolidation
  Why: the inbox has installed-skill lenses, debate pair, shadow plan review, and daily second-Foreman review. Each differs only in who reviews and what it reads. Pass 2's two HIGH proof-tool bugs show the reviewer path is the part worth building once, well.
  Done when: `fm second --by <lens|skill|model> --of <plan|diff|session>` runs one reviewer path and records findings. Cut the other three inbox items with a note pointing here.

- **Make the guard's git channels a data table** — CLEAN — value 4 — effort M — risk med — category: guard
  Why: pass 1 added exec/write channels (--output, -c keys, rebase -x, archive targets, and more) as parser code. The follow-up adversary pass still found a whole missed class. Each new channel should be a row, not a branch.
  Done when: the channels live in one table read by fmguard, and replaying the 5,000-command corpus gives identical verdicts. Adding a channel means adding one row plus one test row.

- **Cap output at one fm whisper per turn** — FEATURE — value 3 — effort S — risk low — category: nudges
  Why: capture notes, revisit triggers, assumption asks, re-tier warnings, and veto notes were all added in a day, and hints are already being quieted for being ignored. A hard cap with ranking is simpler than tuning each kind.
  Done when: a test firing five eligible notes emits only the highest-ranked one. The rest are logged as suppressed, not lost.

- **Show only ten verbs in `fm --help`** — FEATURE — value 3 — effort S — risk low — category: discoverability
  Why: more than 20 modules and dozens of verbs, with "did you mean" needed for typos. That suggests the surface is too big for a newcomer. The stranger test in the inbox would stall here first. Assumption: the 10 core verbs are picked from usage counts.
  Done when: `fm --help` lists ≤10 verbs, and `fm help all` lists the rest.

- **Sunset unused verbs with a warn, hide, remove lifecycle** — CLEAN — value 3 — effort M — risk low — category: deprecation
  Why: the pack shows many features built in a day with no feedback on use. Existing pruning covers rules, not commands.
  Done when: a verb with zero invocations in 60 days of hook and ledger logs shows in `fm doctor` as a sunset candidate, and a hidden verb prints a one-line notice when run.

- **Run every README command as a suite test** — CLEAN — value 3 — effort S — risk low — category: docs
  Why: the stranger test is open, and "wrong commands" is its first failure mode. Cheap, deterministic doctests catch most of that before any child spends tokens.
  Done when: a fenced `fm ...` block in the README that names a nonexistent verb or flag fails `test_suite_hygiene`.

- **Wild: Hold a monthly delete-only pass** — CLEAN — value 4 — effort M — risk med — category: pruning
  Why: every pass adds code, and 704 tests are now a safety net for removal. Assumption: the dead-code finder is trustworthy once tests plus hook logs define "used".
  Done when: a pass finds functions never reached in tests or 30 days of logs, removes them on a branch, and shows that tests and bench are unchanged. The user approves the diff.

- **Wild: Generate a one-page architecture postcard that fails when it overflows** — CLEAN — value 2 — effort S — risk low — category: legibility
  Why: simplicity needs a number. Modules, verbs, and hooks are auto-listed into one page capped at about 60 lines.
  Done when: `fm doctor` fails or warns if the generated page exceeds the cap, and names the module that pushed it over.

- **Wild: Add a "complexity ledger" where each new command must name one it replaces or justify itself** — FEATURE — value 3 — effort S — risk low — category: governance
  Why: the user wants "better better better" but also said savings and speed should not sacrifice quality. Growth needs a counterweight that the brief itself enforces.
  Done when: a brief that adds a CLI verb without a `replaces:` or `justify:` line is rejected at `fm check`.

- **Count ceremony per closed task** — PERFORMANCE — value 3 — effort S — risk low — category: overhead
  Why: Foreman should be cheap on S tasks, and the user pushed back on token overuse. Today there is no per-task count of fm calls and hook notes.
  Done when: `fm cost` prints fm calls and note tokens per closed S, M, and L task, and flags an S task above a threshold.

- **Wild: Default every new setup to "calm mode" with three visible behaviours** — FEATURE — value 3 — effort M — risk med — category: onboarding
  Why: assumption: a first-time user only needs brief gate, evidence, and next-step. The rest unlocks by use, such as the first review, first drive, and first budget cap. This also gives the stranger test a smaller surface to learn.
  Done when: a fresh install shows only those three behaviours, and each further feature announces itself once on first relevant use.
