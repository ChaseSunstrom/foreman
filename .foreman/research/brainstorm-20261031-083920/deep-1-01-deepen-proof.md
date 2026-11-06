# Brainstorm — lens: deepen: proof

- **Proof ledger with a typed strength ladder** — FEATURE — value 5 — effort M — risk med — category: proof
  Why: T-2273 rollup counts "typed or inconclusive" evidence, T-2284/T-2303 measured, T-2288 data. Each proof kind is a separate shape, so "how strong is this?" is not comparable. Combine "unproven as a state", "model-judged is unproven" and "proof that could not have failed" into one rung scale: typed < model-judged < ran-green < ran-red-then-green < measured/mutated < user-owned check.
  Done when: `fm task evidence ID` prints one rung per criterion, and the rollup groups done tasks by lowest rung, with a test per rung.

- **Run a red-capable check on every proof (mutation of the claim)** — FEATURE — value 5 — effort M — risk med — category: proof
  Why: `fm task prove` shows a test fails without the change, but docs, infra and perf proofs have no such control. Generalise: each kind supplies a "break it" mutator (revert hunk, flip flag, drop migration step, inflate benchmark input); a proof with no mutator that turns it red is stamped "could not fail".
  Done when: a task whose verify command is `true` is labelled "could not fail", and one with a real test is labelled "fails when broken" with the mutation named.

- **Unproven items carry an expiry and a one-command upgrade** — FEATURE — value 4 — effort S — risk low — category: proof
  Why: the rollup lists unproven tasks on every surface but nothing tells the user how to cure one. Each row shows the cheapest upgrade (e.g. `fm shot`, `fm prove --migration`, `--bench`) and a re-check date.
  Done when: each rollup row prints a runnable command, and running it moves the task's rung and removes the row.

- **Stale-world detection: proofs record what they leaned on** — FEATURE — value 4 — effort M — risk med — category: proof
  Why: assumption: proofs silently depend on tool versions, env vars, network, DB engine, base commit. Record a fingerprint (interpreter, tool versions, lockfile hash, touched fixtures) at proof time; flag "world moved" when it differs at ship or later.
  Done when: bumping a lockfile marks earlier proofs "stale: lockfile changed" in `fm doctor`.

- **Twin-writer/judge separation check** — SECURITY — value 4 — effort M — risk low — category: proof
  Why: the earlier open question "which verbs have a model on both sides with no user-owned check". Build a static audit that lists each verb in which one model writes and a model judges, and which user-owned check sits between; cold reads and exam scenarios are already steered to use different models.
  Done when: `fm doctor` prints a table of writer/judge verbs, and a new verb lacking a declared owner check fails a test.

- **Declare the effect set before building, diff after** — FEATURE — value 4 — effort M — risk med — category: proof
  Why: Blast radius already writes co-change neighbours into Risks. Take the next step: the plan names files, tables, ports, docs and configs it expects to change; close compares against the actual touched set, and unexpected effects become either evidence or a block.
  Done when: a task touching an undeclared path is held at finish with that path named, and the declared-but-untouched paths are listed.

- **Pre-change false-pass detector** — FIX — value 4 — effort M — risk med — category: proof
  Why: red-first tests prove failure before the change, but not that the failure is for the right reason. Compare failure text to the criterion (assertion names the new behaviour vs import error or typo).
  Done when: a test that fails pre-change with ImportError is rejected as "red for the wrong reason", and a real assertion failure is accepted.

- **Docs-versus-code proof by executed examples** — FEATURE — value 4 — effort M — risk low — category: docs
  Why: Mission 7 lists "docs against code" yet the built proof kinds are perf and data. Extract fenced commands and flags from docs, run them in a sandbox and compare flags to `--help`. Docs claims that can't run are labelled unproven.
  Done when: a doc that names a nonexistent `fm` flag fails `fm prove --docs`, and a correct one passes with the commands listed.

- **Wild: Counterfactual twin repo** — FEATURE — value 4 — effort L — risk high — category: proof
  Why: wild. Build a throwaway twin of the project's start tree with the change applied surgically in reverse (and in a variant with only half the change), then run the whole proof set against all three; a proof that gives the same verdict on every twin proves nothing.
  Done when: the twin run reports per-proof verdicts across three trees and flags any proof that is identical on all.

- **Wild: Claim mutation fuzzer** — FEATURE — value 3 — effort M — risk med — category: proof
  Why: wild. Take the task's final summary, perturb its numbers and nouns ("faster by 40%" to 4%, "all 12 tests" to 13), and check whether any evidence record would catch the change. Claims no evidence contradicts when mutated are decoration.
  Done when: a summary claim with no linked evidence is listed as "uncheckable claim" by `fm task finish`.

- **Wild: Proof replay on a schedule ("proof rot" monitor)** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: wild. Nightly, re-run every cheap recorded proof against main and report which have rotted (green then, red or flaky now), feeding Mission 8's signal-to-fix loop.
  Done when: a deliberately broken old fixture shows up in the morning digest as "proof rot" with the task that vouched for it.

- **Cross-check the numbers Foreman shows** — SECURITY — value 4 — effort M — risk low — category: proof
  Why: the earlier question about numbers never checked by anyone but their producer. Add an independent recomputation (a tiny second implementation reading raw event logs) for the headline stats on the site and rollup, and fail on mismatch.
  Done when: `fm doctor` recomputes site stats from events and flags any disagreement above a tolerance.

- **Proof-of-meaning check: user restates the criterion** — FEATURE — value 3 — effort S — risk low — category: proof
  Why: "does it do what the user meant" is the one proof kind with no mechanism. At close, show the original words beside the criteria and the evidence, and record whether the user confirmed, with unconfirmed ones counted in the rollup.
  Done when: a done task shows a "meant-check: confirmed/unconfirmed" field and the rollup counts unconfirmed.

Next question: Which proofs does the user skip reading entirely, and would a proof they never open be better replaced by a stricter automatic gate?
Next question: When two proofs disagree (test green, `fm shot` shows broken UI), which one wins by rule, and does the user see the conflict?
