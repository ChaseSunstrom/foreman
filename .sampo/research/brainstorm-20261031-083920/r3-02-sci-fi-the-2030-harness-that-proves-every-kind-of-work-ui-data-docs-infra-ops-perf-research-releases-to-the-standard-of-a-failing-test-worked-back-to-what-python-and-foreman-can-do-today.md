# Brainstorm — lens: sci-fi: the 2030 harness that proves every kind of work (UI, data, docs, infra, ops, perf, research, releases) to the standard of a failing test, worked back to what Python and Foreman can do today

- **Route proof from the diff with one verb** — FEATURE — value 5 — effort M — risk low — category: proof router
  Why: proof kinds exist as separate flags (`--bench`, `--migration`, `fm shot`, `fm flow`), so the user has to know which to ask for. Evidence: T-2284, T-2288, and the "missing a capability" asks. Assumption: a path/extension classifier is enough to pick kinds.
  Done when: `fm prove ID` on a diff touching a migration file and a template runs the migration proof and a UI shot, and prints which kinds it skipped and why.

- **Chain the evidence so it can't be rewritten** — SECURITY — value 4 — effort M — risk low — category: evidence integrity
  Why: assumption: evidence is stored as editable task text, and the open question "which numbers were never checked by someone other than the producer" has no answer for rewritten lines. Each record would carry a hash of the previous record plus the command's output hash.
  Done when: editing one stored evidence line makes `fm doctor` name the task and the broken link.

- **Print the fidelity gap between proof environment and target** — FEATURE — value 4 — effort M — risk med — category: unproven rollup
  Why: the migration proof runs on a throwaway database copy, and the perf proof runs on one machine. Neither says "proven on sqlite 3.45, target is postgres". Assumption: stack cards or the manifest declare the target.
  Done when: a receipt for a migration proved on SQLite with a declared Postgres target contains "not proven on: postgres" and the unproven rollup counts it.

- **Put proof recipes in stack cards** — FEATURE — value 4 — effort M — risk low — category: cards
  Why: cards (python, tailwind, cc-plugin-release…) exist via `fm lib show`, but none say how to prove a change in that stack (terraform plan then re-plan to empty, openapi diff, lighthouse budget). This is how the proof kinds spread beyond code without hand-writing each one.
  Done when: `fm lib show terraform` lists a "prove" section, and `fm prove --suggest` on a `.tf` change quotes it.

- **Audit a verify command's side effects** — SECURITY — value 4 — effort M — risk med — category: footprint
  Why: the guard stops bad commands but nothing records what a passing proof wrote outside scope (home dir, network, other repos). The `.fm-scratch/` lane-rm failure (T-2289) is one case. Assumption: strace or an inotify watch is available, otherwise it falls back to a before/after listing.
  Done when: a verify command that writes `~/x` is reported as "wrote outside scope: ~/x" in the evidence.

- **Scale proof depth with blast radius** — FEATURE — value 4 — effort M — risk low — category: risk-weighted
  Why: the plan already writes blast-radius neighbours into Risks (Mission 5). A typo fix and a billing change get the same ceremony. Assumption: co-change count and past FIX history are a usable risk signal.
  Done when: a task whose scope has 5 or more past FIXes requires two proof kinds to close, and a docs-only S task requires one.

- **Memoize proofs by content hash** — PERFORMANCE — value 3 — effort S — risk low — category: proof cache
  Why: `fm ship` is gated by the full suite and each push re-runs every proof. Input-hash expiry is on the list, but its flip side, skipping an unchanged proof, isn't.
  Done when: a second `fm task finish` with unchanged inputs reuses the recorded proof and says "reused, same inputs", and changing one input file reruns it.

- **Run UI proof across a viewport, zoom and locale matrix** — FEATURE — value 3 — effort M — risk low — category: UI proof
  Why: `fm shot` and `fm flow` prove one rendering. The web UI's real failures are at 200% zoom, narrow width and long strings. Assumption: `fm flow` can be parameterised by viewport.
  Done when: `fm flow NAME --matrix` writes N shots and fails the task if any has horizontal overflow or an element clipped off-screen.

- **Fuzz the changed functions for a counterexample** — FEATURE — value 3 — effort M — risk med — category: attack proof
  Why: a mutation check exists as an idea, but nothing tries to break the new code from the outside. Assumption: stdlib-only random inputs from type hints find enough, with `hypothesis` used when installed.
  Done when: `fm prove --attack` on a function with a planted off-by-one prints a failing input and saves it as a regression test.

- **Redact proof receipts before they leave the machine** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: the site publishes Genesis data (T-2326) and ledger pages are proposed. Receipts contain commands, paths, hostnames and output. Nothing is said about secrets in them. Assumption: the guard's secret patterns can be reused.
  Done when: publishing a receipt containing a planted token and `~` writes neither, and a test fails if the redactor is skipped.

- **Wild: Fast-forward the clock to prove ops tasks** — FEATURE — value 3 — effort M — risk med — category: ops proof
  Why: wild. Cert expiry, log rotation, cron and cache TTL bugs only show up over months, and the ops/incident work in Mission 7 has no way to see them. The wrapper would run the verify command under `faketime` stepped 400 days.
  Done when: a cron job with a planted 90-day-expiry bug passes today but fails the soak, naming the simulated date.

- **Wild: Emit a self-contained `proof.pyz` per task** — FEATURE — value 4 — effort M — risk med — category: portable proof
  Why: wild. A stranger, or the user's other machine, re-verifies a closed task offline with `python3 -I proof.pyz`. It holds the commands, the pinned inputs and the expected hashes, so trust doesn't depend on Foreman's own ledger.
  Done when: running `proof.pyz` in a clean directory reproduces the recorded pass, and flipping one byte of the fixture makes it fail.

- **Wild: Replay a proof in the browser on the site** — FEATURE — value 2 — effort L — risk med — category: site
  Why: wild. A reader of the Genesis page presses "re-run" on a claim and watches the evidence command execute in Pyodide. Assumption: only the stdlib-only proofs are replayable, and the rest are labelled "needs a machine".
  Done when: one published proof re-runs in a browser with no server and shows the same output hash as the ledger.

- **Wild: Let a lane try to upgrade each unproven task overnight** — FEATURE — value 3 — effort M — risk med — category: unproven upgrade
  Why: wild. The unproven rollup (T-2273) counts tasks but nothing works the list down. A lane picks the oldest, tries the proof kind its type allows, and files "upgraded" or "cannot be proven because X". Assumption: a read-only lane can run proofs without editing code.
  Done when: after a night's run the rollup count falls by the number upgraded, and each remaining item has a recorded reason.

Next question: Which proof records today could a cold reader accept as "proven" while the command only ran on the author's machine and was never replayed elsewhere?
Next question: What do the user's own `fm shot` and `fm flow` runs show that no proof kind currently asks the next question about (for example, what the user inspects by eye first)?
