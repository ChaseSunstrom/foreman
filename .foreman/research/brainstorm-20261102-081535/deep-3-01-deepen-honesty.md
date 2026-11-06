# Brainstorm — lens: deepen: honesty

- **Proof-debt ledger with conversion price** — FEATURE — value 5 — effort M — risk low — category: honesty
  Why: the request says unproven things get labelled, but nothing keeps them; the three "unproven" ideas in the category are one register. Merge them: each entry holds claim, task id, reason code, age, and the cheapest probe that would convert it (a command, a cost in seconds/tokens). `fm next` ranks by age × cost-to-prove.
  Done when: `fm unproven` lists entries sorted by that score, and closing a task with an unproven criterion adds a row that a later passing probe removes.

- **Closed verdict set with closed reasons** — FEATURE — value 5 — effort S — risk low — category: honesty
  Why: free-text "unproven" lets anything hide. Verdicts: proven / refuted / unproven. Reasons: no-env, no-oracle, too-costly, ambiguous-intent, sampled-only. Anything else fails `fm task finish`.
  Done when: finishing with a reason outside the list exits non-zero and names the allowed list.

- **Sample disclosure on every proof** — FEATURE — value 4 — effort S — risk low — category: honesty
  Why: "Disclose the sample" is listed; a proof of 3 of 40 files reads as a proof of 40. Each proof record stores n_checked / n_in_scope, and the finish text prints "3 of 40".
  Done when: a proof that ran on a subset prints the fraction, and `fm task prove` fails to write a proof without both numbers.

- **Footer enforced by the Stop hook** — FEATURE — value 4 — effort S — risk med — category: honesty
  Why: the Stop hook already gates done. If the final message claims success but lacks an "Unproven:" line while the ledger has open rows for this task, the hook appends the footer from the ledger rather than trusting the model's wording.
  Done when: a session ending with open rows for its task shows a footer that matches `fm unproven --task`, byte for byte.

- **Claim-to-proof binding at write time** — FEATURE — value 5 — effort M — risk med — category: honesty
  Why: the "make the model unable to write a proof label" idea. Labels like "verified" and "passes" are rendered by Foreman from a run record (command, exit code, hash of output), never typed by the model. A label with no record id is stripped and replaced with "unproven (no record)".
  Done when: a finish message containing "verified" without a matching record id is rewritten, and a test shows that.

- **Hedge and weasel lint on finish text** — FEATURE — value 3 — effort S — risk low — category: honesty
  Why: "should work", "looks correct", "likely" in a done message mean an unrun check. The lint maps each phrase to a missing probe and offers to open a row in the ledger.
  Done when: a finish text with "should work" yields a ledger row tagged `hedge` pointing at that sentence.

- **Proof decay and re-proof by drift** — FEATURE — value 4 — effort M — risk low — category: honesty
  Why: a proof is true for a commit. Store the file set each proof touched; when any changes, the label becomes "stale" and the row returns to the ledger. This extends your public-claims check (site/README vs exam lines) to every past "proven".
  Done when: editing a file under a proven criterion turns it to stale in `fm unproven` without a rerun.

- **Honesty scorecard per harness and model** — FEATURE — value 4 — effort M — risk low — category: honesty
  Why: bets now carry a harness. Add a second ledger of claims versus later outcome: how often "proven" was reversed within 30 days, split by harness. Same like-for-like window rule as T-2610.
  Done when: `fm outcomes --honesty --by harness` prints a reversal rate with counts, and refuses a rate under 20 settled.

- **Wild: Rubber-stamp detector on the human** — FEATURE — value 3 — effort M — risk med — category: honesty — wild
  Why: assumption: the user approves quickly under standing rules. Track time-to-approve and approvals with no diff opened; when the median falls under a floor, `fm ask` says "the last 6 approvals took under 5s; here is what you approved" with a one-line summary each.
  Done when: six approvals under the floor trigger one summary, and a slower one doesn't.

- **Wild: Degraded-truth drill** — FEATURE — value 3 — effort M — risk low — category: honesty — wild
  Why: plant a fault in a scratch copy (a test that always passes, a stale doc, a lying verify command) and see whether the agent labels it unproven. An exam kind whose score is detection, run in the zero-token arms where possible, per the testing cadence.
  Done when: `fm exam` has a drill kind with N planted lies, reporting caught / missed per lie class.

- **Wild: Confession diff at session end** — FEATURE — value 3 — effort S — risk low — category: honesty — wild
  Why: assumption: users trust a short comparison. At close, show three columns from records, not prose: asked, ran, never ran. The "never ran" column is computed from the criteria minus the run log, so the model can't soften it.
  Done when: the close-out prints the computed "never ran" list, identical to the ledger diff.

- **Unproven count in public claims** — FEATURE — value 3 — effort S — risk low — category: honesty
  Why: the proof-before-presentation sweep checks numbers; it doesn't check whether the site discloses what is open. Add the open-ledger count and oldest age to the README and site/genesis data.
  Done when: the sweep goes red if the published count differs from `fm unproven --count`.

- **Reason-specific unlock hints** — FEATURE — value 3 — effort M — risk low — category: honesty
  Why: with a closed reason set, each reason has a known fix: no-env queues an install through the dependency path, no-oracle asks for an example via `fm ask`, too-costly proposes a sampled probe with its disclosed fraction.
  Done when: each of the five reasons produces a distinct next action in `fm next`, covered by a test per reason.

Next question: Which "proven" labels in past finished tasks were reversed later, and what share had no run record at the time?
Next question: When the user overrides an unproven row by hand, who records that the override isn't proof?
