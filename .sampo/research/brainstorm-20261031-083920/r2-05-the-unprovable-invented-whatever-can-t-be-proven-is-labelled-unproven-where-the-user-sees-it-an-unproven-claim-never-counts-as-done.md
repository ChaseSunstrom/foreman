# Brainstorm — lens: the unprovable (invented): whatever can't be proven is labelled unproven where the user sees it; an unproven claim never counts as done

Lens: the unprovable. Ideas below avoid the "Ideas so far" list; they go after how an unproven claim is stored, shown, expires, and blocks "done".

- **Make "unproven" a closing state that gates goal finish** — FEATURE — value 5 — effort M — risk med — category: proof state
  Why: T-2273 rolls up unproven tasks, but the pack shows only counting and listing. Assumption: a task can still reach `done` while unproven, so the rollup is a report, not a rule.
  Done when: `fm task finish` on a task whose criteria rest only on typed evidence ends in `closed-unproven`, and `fm goal finish` refuses while any such row is open without a recorded user-run `fm accept-unproven ID "reason"`.

- **Tag each evidence line with its witness class** — FEATURE — value 5 — effort M — risk low — category: provenance
  Why: The earlier question "which numbers have never been checked by someone other than the producing code" has no per-line answer. Assumption: evidence is stored as free text with a kind label.
  Done when: every evidence record carries one of `ran` / `typed` / `model-judged` / `user-run`, and the rollup groups by that class. Only `ran` and `user-run` can satisfy a criterion.

- **Record the "unprovable on purpose" cases at plan time** — FEATURE — value 4 — effort S — risk low — category: plan gate
  Why: Taste, tone, "feels fast" and external-service claims cannot be proven by command. Assumption: the plan gate doesn't ask for this today.
  Done when: a plan row without a runnable check must carry `unprovable: <reason>`, and the plan gate refuses a row that has neither a check nor a reason.

- **Carry the unproven label into the commit and the finish receipt** — FIX — value 4 — effort S — risk low — category: surfaces
  Why: The rollup is shown on surfaces, but commits, `fm ship` output and the site changelog are where a claim gets read later. Assumption: those don't mention it.
  Done when: a commit made from a closed-unproven task has an `Unproven:` trailer naming the criteria, and the ship output prints the same lines.

- **Let a typed claim decay into a visible bet** — FEATURE — value 3 — effort M — risk low — category: expiry
  Why: Typed evidence is true only on the day it was typed. Assumption: no age is displayed today.
  Done when: the rollup shows the age of each unproven item, and after N days (configurable) it moves from "unproven" to "stale-unproven" and sorts first.

- **Add a one-command upgrade path from unproven to proven** — FEATURE — value 4 — effort M — risk med — category: proof upgrade
  Why: A label with no way to act on it is nagging. Assumption: the rollup names the problem but not the fix.
  Done when: each rollup line prints the exact `fm prove ...` or `fm task evidence ...` command that would replace the typed evidence, and running it clears the line only if it exits 0.

- **Check that the label survives every renderer** — CLEAN — value 4 — effort S — risk low — category: consistency
  Why: Foreman has the terminal, the pane, the web UI, the site and the Genesis page, and earlier asks show a number appearing on some surfaces but not others. Assumption: each renders from separate code.
  Done when: one test seeds an unproven task and asserts the same count and ids appear in every renderer's output; adding a surface without it fails the test.

- **Refuse to quote an exam or bench number without its proven fraction** — SECURITY — value 4 — effort M — risk low — category: honest numbers
  Why: Steers say Haiku scores never decide done and the exam is deferred, but the site publishes stats daily (T-2326). Assumption: the stats carry no proof coverage.
  Done when: every published stat on the site is rendered as `N (M of K proven by a run)`, and publish fails if the proven fraction is missing.

- **Detect claims in the final answer that no evidence row covers** — FEATURE — value 5 — effort L — risk med — category: claim audit
  Why: The user's real question is "does it do what I meant"; the unproven part is often a sentence the agent said ("this also fixes X") that no criterion contains. Assumption: the Stop hook reads criteria, not the closing message.
  Done when: sentences in the closing message that assert behaviour (extracted by a cheap pass) and match no criterion are listed as `unclaimed-unproven`, and a planted test sentence is caught.

- **Wild: Run an "unproven court" that turns the oldest unproven claim into a task each night** — FEATURE — value 3 — effort M — risk med — category: unattended proof
  Why: wild; assumption: the lane and routine machinery can run unattended. A nightly lane picks the oldest unproven item, tries to write a runnable check, and either upgrades it or records why it cannot.
  Done when: after a nightly run the item is either proven with a ran record or carries a new `cannot-prove: <reason>` line.

- **Wild: Show a "confidence weather" strip on the status line** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild; a one-glyph strip (solid for ran, hatched for typed, hollow for unprovable) across the last 20 closed tasks, so a streak of hollow ones is visible without opening a report.
  Done when: the status line prints a 20-cell strip whose cells match the witness class of each closed task's weakest evidence.

- **Wild: Pay a bounty to the cold reader for a false "proven"** — FEATURE — value 4 — effort M — risk med — category: adversarial
  Why: wild; the standing rules prefer signals Foreman didn't author. A different-model reader is shown only the proven evidence and asked to name one way it could pass while the claim is false; a credible answer demotes the item to unproven.
  Done when: a seeded task with a test that passes for the wrong reason is demoted to unproven by the reader, and a sound one stays proven.

- **Keep a user-owned list of claim words that can never be proven by prose** — SECURITY — value 3 — effort S — risk low — category: guard
  Why: "robust", "secure", "faster", "works" are the words that slip through typed evidence. Assumption: no such list exists; it follows the user-owned checker idea but is cheaper.
  Done when: a criterion containing a listed word with no measured or ran evidence is flagged unproven at finish, and the list is editable only by the user.

Next question: Today, can any path reach `done` with typed evidence only, and what does the closing code do when it does?
Next question: Which unproven items does the user actually act on, and does acting on them change what the next plan includes?
