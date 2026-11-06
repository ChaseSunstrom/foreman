# Brainstorm — lens: unspoken needs

- **Pin the builder to the last exam-passed release** — FEATURE — value 5 — effort M — risk med — category: self-hosting
  Why: assumption: the tower edits Foreman while its own drive, hooks and gates run from the working copy. One bad self-change then degrades the thing that would catch it (T-2605 shows gates already flake on the self-change path). Run unattended drives from a pinned copy (the last release that passed the zero-token arms), and promote the pin only after the gates pass.
  Done when: a planted breaking change in the working copy leaves a running `fm drive` unaffected, and `fm doctor` prints the pinned and working-copy versions.

- **Declare "done" against a pinned frame** — FEATURE — value 5 — effort M — risk low — category: done-ness
  Why: steers say `fm genesis grow` only adds and never removes, and "no empty cells" is the end condition. That makes the target move forever. Freeze frame.md at version N, let the goal be finishable against it, and queue growth as frame N+1.
  Done when: a goal closes with "done against frame N" while a newly grown cell appears only under N+1, and the finish receipt names both.

- **Show what each standing rule costs** — FEATURE — value 4 — effort M — risk low — category: steers
  Why: there are 30+ steers, each added in one line, and none shows its price. Count, per steer, the refusals, held tasks, gate seconds and blocked asks it caused, from existing ledgers. A steer that caused nothing in 30 days is flagged as possibly enforced by nothing.
  Done when: `fm decide --list` shows a cost column, and the round-first steer shows the number of items it held.

- **Add a gen-0 amendment path with an impact preview** — FEATURE — value 4 — effort M — risk med — category: intent
  Why: gen-0 is immutable by steer, but the user's mind will change over days. With no sanctioned path they will either edit around it or live with a wrong gen-0. A user-only `fm genesis amend` should show which MUSTs, cells and shipped capabilities the change touches, seal the diff, and never auto-run.
  Done when: an amendment shows a rows-affected list before the user's yes, and an unconfirmed amendment changes nothing.

- **Digest costly decisions mid-run, with reversal cost** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: the "never block on the user" steer routes decisions to `fm decide --kind costly`, which lands in the final report. For a multi-day run that is too late to reverse cheaply. Roll them into the morning note and rank them by cost to undo. After N unseen ones or 3 days, ask once.
  Done when: after 3 costly decisions, the next session start lists them with an undo cost, and acknowledged ones drop out.

- **Re-verify the claims in a final report** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: the user keeps pushing for non-self-authored signals and real cells. Extract the checkable sentences from a final report ("N tests pass", "file X exists", "gate Y green"), re-run them cold, and print agree or disagree per claim.
  Done when: a report with one planted false count yields exactly one DISAGREE line, naming the command that disproved it.

- **Census the skill files and retire dead ones** — CLEAN — value 3 — effort M — risk low — category: simplicity
  Why: the map shows 1388 files under plugin/skills against 131 in lib. Count which skills ever loaded in recorded sessions and which are only reached through the 40-odd deferred bundles. List those never loaded in 60 days as retirement candidates, without deleting.
  Done when: `fm doctor` prints a skills-never-loaded count with a per-skill list behind `--json`.

- **Publish a "what Foreman is bad at" page** (wild) — FEATURE — value 3 — effort S — risk low — category: honesty
  Why: the steer says a capability whose free arm beats the session arm is a top gap and is printed first. Publish that list, with denominators, on the Genesis site next to the strengths. It is the strongest reply to the proof-before-presentation steer, and no one asked for it.
  Done when: site/genesis lists every capability where the free arm beats the session arm, and the page regenerates from the exam lines.

- **Fork the tower with one steer removed** (wild) — FEATURE — value 3 — effort L — risk med — category: counterfactual
  Why: assumption: the user can't tell whether a steer is helping or just inherited. Run one generation's free arms in a scratch clone with steer k off, then compare. The steer cost ledger above says what a steer costs; this says what it buys.
  Done when: `fm decide --ablate ID` yields a table of exam deltas with the steer on and off.

- **Test whether a cheap model plus Foreman beats a big model alone** (wild) — PERFORMANCE — value 4 — effort M — risk low — category: discipline value
  Why: the product claims to be a discipline layer, but the pack has no cross-model evidence. On the same held-out scenarios, run Haiku with Foreman against Sonnet plain. Report pass and cost, and publish it only when it holds.
  Done when: one exam table shows both arms' pass rates and dollars, and a README claim cites it or is absent.

- **Turn the user's cut-line into a stored default** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: the user corrects thresholds ("7+ characters, not 8") and drops whole classes of self-filed work. Learn their usual cut line (S/M-only at night, no CLEAN before FIX) from the dropped ledger. Apply it as the default ordering with a one-line reason, and let a single reply override it.
  Done when: with 5 dropped CLEAN tasks on record, `fm next` ranks CLEAN last and prints why.

Next question: Which of the user's standing steers have never once changed what Foreman did, and would anyone notice if they were removed?
Next question: What is the first moment the user would regret having left Foreman running unattended, and does any current gauge show that moment before it happens?
