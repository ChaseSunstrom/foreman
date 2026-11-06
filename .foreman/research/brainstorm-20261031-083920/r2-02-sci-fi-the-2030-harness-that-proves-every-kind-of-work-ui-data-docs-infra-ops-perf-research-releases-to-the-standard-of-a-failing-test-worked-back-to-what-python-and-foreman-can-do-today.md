# Brainstorm — lens: sci-fi: the 2030 harness that proves every kind of work (UI, data, docs, infra, ops, perf, research, releases) to the standard of a failing test, worked back to what Python and Foreman can do today

- **Compile every proof kind into one "claim → falsifier" record** — FEATURE — value 5 — effort M — risk low — category: proof core
  Why: the pack has separate kinds (unproven rollup T-2273, perf T-2284/T-2303, migration T-2288) and many ideas for more (docs, infra, research, release). The 2030 form is one schema: claim text, the command that would falsify it, the last run's output hash, the witness who ran it. New kinds then become a plug-in that emits the record, not a new verb.
  Done when: `fm prove --list` prints one row per closed task in the same five fields for perf, migration and typed kinds, and a test fails if a kind writes evidence outside the schema.

- **Run a falsifier-first check: the proof must fail on the pre-change tree** — FEATURE — value 5 — effort M — risk med — category: proof core
  Why: T-2284 already times the start tree against the current one for perf. Generalise it: any proof command is run on the task's start tree and must go red there (docs example, migration, UI flow), or the evidence is labelled "could not have failed".
  Done when: closing a task whose verify command also passes on the start tree records "unfalsified" and the unproven rollup counts it.

- **Execute the docs' code blocks and flags against the shipped CLI** — FEATURE — value 4 — effort M — risk low — category: docs proof
  Why: seed row says "docs against code" and the pack's "Plan gate misses an option starting with a flag" shows prose/parser drift is real. Extract fenced `fm ...` commands and `--flags` from MASTER.md and README, run `--help`/dry-run in a scratch dir, and list the ones that no longer exist.
  Done when: a seeded stale flag in a doc makes `fm prove --docs` exit non-zero naming file and line.

- **Prove infra by plan, scratch apply, re-plan-to-empty** — FEATURE — value 4 — effort L — risk med — category: infra proof
  Why: T-0325/T-0352 and install.sh/CI show infra tasks closing on typed text. Python can drive `docker`/`terraform`/`systemd-analyze verify` in a throwaway target and record the second plan being empty, like the migration up/down/up shape of T-2288.
  Done when: a fixture compose or unit file task closes only after a recorded empty second plan, and a broken fixture is refused.

- **Pin research claims to a dated, hashed source and re-fetch on a schedule** — FEATURE — value 4 — effort M — risk low — category: research proof
  Why: RESEARCH tasks (T-0336, T-1331) exist with no proof kind. A claim row carries URL/file, quote, content hash, fetch date; a stale or changed hash flips it to "unproven" in the rollup. Assumption: fetching is allowed by setting only.
  Done when: changing a stored source's content makes the next `fm unproven` list that claim as drifted.

- **Add a user-owned checker file the writer model cannot edit** — SECURITY — value 5 — effort M — risk med — category: trust
  Why: answers the pack's question about verbs with a model on both sides and no user-owned check. Mirror the guard's USER_ONLY_FM (T-2252): checks live in a file whose edits need a user-only verb, and the closer runs them.
  Done when: a session attempting to edit or weaken the checker file is refused by the guard, and a test shows it.

- **Mutate the fix, see the test notice** — FEATURE — value 4 — effort M — risk low — category: test strength
  Why: "proof that could not have failed" is the recurring worry in the ideas list. Flip one operator or delete one changed line in the diff, rerun the task's new test, and record killed/survived.
  Done when: a task whose new test survives all mutants of its own diff is flagged weak in `fm task evidence`.

- **Prove releases by installing the built artifact and running the first-use path** — FEATURE — value 4 — effort M — risk low — category: release proof
  Why: Seed row 10 names releases; install.sh and fm doctor already exist and the standing rule says it must work with no claude on PATH. A clean-venv/clean-HOME run of `install.sh` then `fm doctor` is a concrete, free proof.
  Done when: `fm prove --release` installs into an empty HOME and records doctor's exit code; breaking install.sh makes it fail.

- **Stamp every figure with a stale-if rule and the command that made it** — FIX — value 3 — effort S — risk low — category: numbers
  Why: the site's stats refresh daily (T-2326) and earlier question asks which numbers were never checked by anyone but their producer. Each published stat gets a `produced_by` command and a recompute-and-compare in `fm doctor`.
  Done when: hand-editing a number in site/genesis data makes `fm doctor` name it.

- **Wild: Run a saboteur lane that breaks green work and scores which proofs noticed** — FEATURE — value 4 — effort L — risk med — category: adversarial
  Why: wild. Use the existing lane machinery: a worktree where a child plants a plausible regression in a closed task's area; each proof kind's catch rate is recorded. Gives the "score proof kinds by catch rate" idea real data without waiting for reopens.
  Done when: a saboteur run on one fixture repo prints per-kind caught/missed counts.

- **Wild: Publish a proof ledger on the Genesis site with the denominators visible** — FEATURE — value 3 — effort M — risk low — category: transparency
  Why: wild. The site already follows Genesis (steer 10-30); add a page where each task is proven/measured/typed/unproven with the "what this does not prove" line. Assumption: the user wants this public.
  Done when: site/genesis data includes a proof breakdown whose counts equal `fm unproven` output.

- **Wild: Let an expiring proof decay into a bet with a visible age** — FEATURE — value 3 — effort M — risk low — category: proof decay
  Why: wild. Measured perf and docs claims rot as code changes. A proof records the files it touched; when they change after the proof, its badge goes from "proven" to "stale since N commits".
  Done when: editing a file named in a proof's footprint flips that proof to stale in the rollup.

Next question: Which proof kinds does the user actually trust today, judged by which ones they have overridden or re-run themselves?
Next question: What is the cheapest oracle for "does what the user meant" that doesn't depend on a model reading its own work?
