# Brainstorm — lens: simplicity

- **Retire verbs with zero runs in 90 days behind `fm prune`** — CLEAN — value 4 — effort M — risk med — category: surface area
  Why: the pack shows a very wide verb set (settings log/macro/duel/replay/words, dojo, séance, bisect, xray) and a 'Slim Foreman' T-0794 deferred. Round 5 added about ten more verbs; the user's complaints are about burn and fixed overhead, not missing verbs. Assumption: the journal records verb invocations.
  Done when: `fm prune` lists verbs with zero invocations in 90 days, and `--apply` moves them to an `extras` group that help hides by default, with a test that the hidden verbs still run.

- **Generate help positions from one registry** — CLEAN — value 3 — effort S — risk low — category: help
  Why: the user asked "fm dojo shares help position 306 with another command, so test_help fails". Hand-assigned positions collide whenever a verb is added.
  Done when: positions derive from a single table, adding a verb needs no number, and test_help passes after adding a dummy verb.

- **Make `fm` with no arguments print one next command** — FEATURE — value 4 — effort S — risk low — category: onboarding
  Why: the first-hour ladder, newcomer tour and settings newcomer are all deferred (T-0862/0863) because bare `fm` is not the entry point. Assumption: one rule on status picks the next step (blocked-on-you, else the next queued task, else init).
  Done when: bare `fm` prints at most 3 lines, the last being a runnable command, across 5 fixture states.

- **Fold the four triage surfaces into `fm triage`** — CLEAN — value 4 — effort M — risk low — category: backlog
  Why: the round-5 review found first, swipe TTY, swipe --serve and app view I, with no single entry. `fm triage` picks TTY or served from the environment and `--serve` stays as an override.
  Done when: `fm triage` opens the right surface in a TTY and in a no-TTY fixture, and the old verbs print a one-line pointer to it.

- **Fail `fm` commands that exit 0 having done nothing** — FIX — value 4 — effort M — risk low — category: reliability
  Why: the user reported "fm quiet runs its command with no stdin... reports exit 0". A no-op that reports success is the worst kind of complexity, because the user must verify it. Assumption: a no-op can be detected as no journal write and no output.
  Done when: `fm quiet` fed a heredoc either runs it or exits non-zero with a sentence naming the problem, and a test covers it.

- **Cap files at 300 lines with a shrinking ratchet** — CLEAN — value 3 — effort M — risk low — category: code health
  Why: T-0166 is deferred because register.tsx is too large, and the review noted each served page duplicates its own style block. A ratchet only lets the offender list shrink.
  Done when: `fm check` fails if any file grows past its recorded size, and the ratchet file shrinks after splitting register.tsx.

- **Share one stylesheet across all served pages** — CLEAN — value 3 — effort S — risk low — category: web UI
  Why: the review noted each served page (settings serve, swipe serve) duplicates its own style block, which also blocks the missing `fm serve` index.
  Done when: one CSS source is inlined into every served page, the diff shows net-negative lines, and a test confirms a token change reaches all pages.

- **Fold the finish verbs into `fm done`** — CLEAN — value 4 — effort M — risk med — category: workflow
  Why: prove, finish, check --affected and evidence are separate steps the model must chain. The user's repeated complaints are about gate waits and about the model not following the steps. Assumption: `fm done` can run them in order and stop at the first failure.
  Done when: `fm done T-x` proves, finishes and prints one receipt line, and the old verbs remain as aliases for a release.

- **Print the guard refusal as the literal-path rewrite** — FIX — value 4 — effort S — risk low — category: guard
  Why: the review says the risk budget tripped 6 times from the model's own `$VAR` and `rm /tmp/*` collisions, and a retry succeeds first time if the refusal names the rewrite.
  Done when: refusals for `$VAR` paths and rm globs include the exact safe command, and a test checks the text.

- **Wild: Show the whole product on one index card and fail the build on overflow** — CLEAN — value 3 — effort M — risk low — category: docs. Wild.
  Why: assumption: the README and help have grown by accretion. A fixed 24x80 card forces a choice about what the product is.
  Done when: `fm card` prints one 24x80 screen listing the top verbs, and CI fails if it overflows.

- **Wild: Let the bare queue be one markdown file a person can edit** — FEATURE — value 3 — effort L — risk high — category: state. Wild.
  Why: assumption: the state is spread across ledgers, journals and per-file JSON, while the user keeps asking for plain reads like `cat` and `grep`. A QUEUE.md as the source of truth with the journal derived from it would make every surface trivial.
  Done when: editing QUEUE.md reorders `fm status` within one second, with a round-trip test.

- **Wild: Delete a feature and keep an obituary line** — CLEAN — value 2 — effort S — risk low — category: history. Wild.
  Why: the pack shows nothing is ever removed, only deferred. Each deletion appends one line (what it was, why it went, and how to restore it) to a CHANGELOG-style graveyard file, which makes deleting cheap.
  Done when: `fm prune --apply` writes the obituary line and `fm restore NAME` brings the verb back from git.

- **Close the deferred 'Later from' piles with a single yes/no sweep** — CLEAN — value 4 — effort S — risk low — category: backlog
  Why: about 25 deferred 'Later from T-07xx/08xx' items share the same stalled state, and the user's own words show they favour finishing over adding. Each item gets a build or drop mark on a checklist page, and the dropped ones are deleted.
  Done when: the open list has no deferred item older than 30 days without an explicit keep mark.
