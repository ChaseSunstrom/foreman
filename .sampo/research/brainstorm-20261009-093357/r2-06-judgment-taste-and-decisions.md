# Brainstorm — lens: judgment, taste and decisions

- **Write a decision-quality rubric the judge applies before any merge or approve** — FEATURE — value 4 — effort M — risk low — category: judgment
  Why: Main thread "plans, judges and merges" but the pack shows no explicit criteria for judging; prior ideas grade decisions after the fact (regret ledger, outcome labels), none define the pre-decision bar. Assumption: judging is currently prose-guided.
  Done when: `fm judge T-xxxx` prints a scored rubric (reversibility, evidence strength, blast radius, fit to brief and vetoes) and the done-gate fails if it is absent on M/L tasks.

- **Keep a taste exemplar set the user curates by ranking pairs of real diffs** — FEATURE — value 4 — effort M — risk low — category: taste
  Why: T-0439 (taste model) is only captured; the user steers on UI beauty, cleanup and "don't block until 75%", which are taste calls. Pairwise rankings of Foreman's own past diffs give grounded data rather than a self-written portrait.
  Done when: `fm taste rank` shows two past diffs, stores the choice, and `fm recall --taste` returns the top exemplars for a given area.

- **Make every judgment call cite which of the user's words it rests on** — FEATURE — value 5 — effort M — risk low — category: judgment
  Why: The pack lists dropped requests like cleanup that "never got done" and corrections such as "budget limits shouldn't block until 75%". Forcing each non-trivial decision to quote a source steer, veto or decision exposes the decisions resting on nothing.
  Done when: `fm decide` rejects entries with no cited source id or an explicit "no precedent" flag, and the brief shows the flag.

- **Detect when a rule was applied rigidly against the user's evident intent** — FEATURE — value 4 — effort M — risk med — category: judgment
  Why: The user steered "budget limits shouldn't block anything until 75%" and dropped YAGNI guard refusals; those are cases where correct rule application was still wrong. Assumption: such overrides are visible in friction logs.
  Done when: `fm friction` lists "rule-correct, user-overruled" events with the rule and the override message, and each proposes a threshold or exception draft.

- **Price each decision by cost of being wrong and spend care in proportion** — FEATURE — value 4 — effort M — risk low — category: decisions
  Why: Prior ideas cover one-way doors and deliberation caps separately; none produce a single number joining reversibility, blast radius and user-irritation cost that sets how many passes and which agents run.
  Done when: the intake brief carries a `stakes` score with its inputs, and the number visibly changes the planned review lenses on two fixture tasks.

- **Keep a "when to stop asking" ledger of asks the user answered identically** — FEATURE — value 4 — effort S — risk low — category: autonomy
  Why: The user complains about being blocked and wants Foreman to keep going. Counting repeated same-answer asks yields concrete standing defaults without a full taste model.
  Done when: after the same ask is approved 3 times, Foreman proposes a standing order and `fm ask` auto-answers it with a logged citation once accepted.

- **Record the default-versus-deliberate split in every plan** — CLEAN — value 3 — effort S — risk low — category: decisions
  Why: Plans bury choices Foreman made by habit among ones it reasoned about. Marking them lets the user spot where taste was never actually applied.
  Done when: M/L briefs list each decision tagged `default` or `weighed`, and a test fails when the section is missing.

- **Audit "which taste call did this review comment represent" over time** — FEATURE — value 3 — effort M — risk low — category: taste
  Why: User corrections are mined for rules only as isolated steers. Clustering them by underlying value (brevity, polish, safety, speed) shows which values conflict and how the user resolves tradeoffs.
  Done when: `fm taste values` prints ranked values with supporting steer quotes and the observed winner in each conflict pair.

- **Run a tie-break protocol that falls back to the user's past resolutions** — FEATURE — value 4 — effort M — risk med — category: decisions
  Why: Panel and debate ideas exist, but when options tie nothing says how to resolve toward the user's pattern rather than a coin flip or an interrupt.
  Done when: a tied approach choice cites the nearest earlier decision by similarity and logs it; a fixture of tied options resolves deterministically.

- **Wild: Hold a "would they frame it" test: render the close-out as the user's likely screenshot reaction** — FEATURE — value 3 — effort M — risk low — category: taste
  Why: wild. Assumption: the user judges work largely by glancing at output. A cheap model predicts the reaction (delight, shrug, wince) to the final card and flags winces before presenting.
  Done when: finished tasks carry a predicted reaction later compared with the user's actual next message, with accuracy shown in `fm friction`.

- **Wild: Keep a "judgment diary" in which Foreman writes the one call it is least sure of each day** — FEATURE — value 3 — effort S — risk low — category: judgment
  Why: wild. Surfacing one daily uncertain call, with the alternative taken, invites cheap user correction and produces labelled taste data.
  Done when: a daily entry exists with the call, the alternative and a one-key agree/disagree reply that is stored.

- **Wild: Seat an "ex-user" persona built from the user's rejected ideas who vetoes new ones that resemble them** — FEATURE — value 3 — effort M — risk med — category: taste
  Why: wild. The pack records many dropped items; a persona built from drop reasons checks new briefs and brainstorm output against them before they reach the user.
  Done when: a new idea matching a prior drop is flagged with the earlier drop reason quoted, on a fixture of three known drops.
