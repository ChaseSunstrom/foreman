# Brainstorm — lens: simplicity

- **Collapse six task types into "change" and "question"** — CLEAN — value 4 — effort M — risk med — category: mental model
  Why: the newcomer audit lists jargon everywhere, and `fm task new --help` names no valid `--type` or `--tier` values. Gates already key on proof kind elsewhere in the pile. Proposal: users see only `change` or `question`, and FIX/FEATURE/PERFORMANCE/SECURITY become tags derived from the request words. Old values still parse.
  Done when: `fm task new "login times out"` needs no type argument, `fm task new --help` lists exactly two kinds, and a replay of the 688 finished tasks maps each to a kind with no unmapped ones.

- **Publish a "Not building" page answering the rival survey** — FEATURE — value 4 — effort S — risk low — category: positioning
  Why: survey B lists missing items (spec stage, Issues sync, vector memory, Windows, marketplace). The pile mostly proposes building them. A one-line "not doing this, because X, use Y instead" per item makes the surface a choice.
  Done when: the README links a page with one line per surveyed rival feature, each naming a reason and the substitute, and a test checks every named verb exists.

- **Add an `fm x` namespace where new verbs live until they earn promotion** — FEATURE — value 4 — effort M — risk low — category: surface control
  Why: 108 verbs, 46 never run by Claude in 11 days. Brand-new verbs go to `fm x <verb>`, hidden from help. They graduate to the front door after N real uses in 14 days, or the registry deletes them.
  Done when: a verb added under `fm x` with zero fires is removed by the registry's expiry check in a test, and one with enough fires is promoted and appears in `fm help`.

- **Replace capture, task new and batch with one `fm add`** — CLEAN — value 4 — effort M — risk med — category: verb merge
  Why: finding 6 shows capture then `task new` creates a duplicate. One verb checks open captures, adopts a match, and takes optional `--type` and `--tier`.
  Done when: `fm capture X` followed by `fm add X` yields one item, and the three old spellings forward to `fm add` with a one-time note.

- **Prove derived state is disposable** — CLEAN — value 3 — effort S — risk low — category: state
  Why: the pile proposes marking files "source or derived", but nothing proves it. A test or `fm doctor` step deletes every derived file in a copy of the state dir, rebuilds, and byte-compares the user-visible views.
  Done when: the test deletes all files tagged derived, `fm status` and `fm task show` output is identical afterwards, and an untagged state file fails the test.

- **Move the 46 unused verbs into one lazily imported `labs` module** — PERFORMANCE — value 3 — effort M — risk med — category: footprint
  Why: the usage data names the unused verbs, and `fm --help` is 231 lines. A lazy module cuts startup, shrinks help and keeps every feature. This is the consolidate-and-hide step the audit asks for, before any deletion.
  Done when: `fm status` imports none of the labs code (checked by import trace), and `fm help --all` still lists and runs those verbs.

- **Keep the guard core to one auditable page** — SECURITY — value 4 — effort M — risk med — category: trust
  Why: install defaults to bypass mode, a large trust ask. A skeptic can't audit a 28k-line codebase. Split a fail-closed guard core of at most ~400 lines, readable in 10 minutes and size-ratcheted in CI, from the workflow gates.
  Done when: a CI check fails if the core file passes its line budget, and the README links the file as "read this before you trust bypass".

- **Treat every "Foreman off for this task" escape as a free control group** — FEATURE — value 4 — effort M — risk low — category: proof of value (wild)
  Why: the bench has 1 case and there is no published evidence of lift. If a user runs a task bare, record its outcome (rework within 24h, hotfixes) next to Foreman-run tasks. This builds the comparison from real use. Assumption: the user will use the escape at all.
  Done when: `fm digest` prints held-rate for escaped and non-escaped tasks side by side, with counts.

- **Show which verbs a cold agent can't discover** — FEATURE — value 3 — effort M — risk low — category: discoverability (wild)
  Why: finding 4 shows help is a brace blob. Give a no-tools child only `fm help` and ten sample requests. Verbs it never reaches become candidates to merge or hide, so removals come from findability data.
  Done when: running it writes a ranked list of unreached verbs, and a re-run after hiding a verb changes the list.

- **Let doc sections expire unless re-verified** — CLEAN — value 3 — effort M — risk low — category: docs rot (wild)
  Why: MASTER.md is 18k words and nothing keeps it true. Each section carries a "verified" stamp checked by a command. Sections unverified for 60 days drop out of `fm docs` and the default context until re-checked.
  Done when: a section with a failing check is hidden from `fm docs` and listed by `fm doctor` as stale.

- **Add `fm doctor --one` that prints a single line** — FIX — value 4 — effort S — risk low — category: first run
  Why: a fresh install fails its own doctor and prints 40 lines of passes. One line, either "ok" or the first failing check with its fix command, with full output behind `--all`.
  Done when: a clean-HOME install runs `fm doctor` and prints exactly one line ending in a result, and a seeded failure prints one line naming the fix.

- **Fold ungraded folded tasks into their parent's grade** — FIX — value 3 — effort S — risk low — category: honest metrics
  Why: 159 of the last 370 tasks show as "ungraded" in `fm digest`, which makes the held-rate look thin. Folded children inherit the parent's grade, so the number shown is one a user can read.
  Done when: `fm digest` for the last 7 days shows zero ungraded folded tasks, and a test covers a parent with two folded children.
