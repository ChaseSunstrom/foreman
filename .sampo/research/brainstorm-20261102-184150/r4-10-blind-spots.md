# Brainstorm — lens: blind spots

- **Drill the generation boundary** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: T-2691 and T-2693 were both found by hand, and both happened where one run was graded by two generations. The class is "a record that sits on a boundary". assumption: `fm drill` has no boundary fault today.
  Done when: `fm drill --fault gen-boundary` builds a ledger where one run carries gen N and N-1 grades, and it fails if any reader (cold-read tail, lineage line, scorecard) drops or mislabels either.

- **Order-check kill results against scripts** — CLEAN — value 3 — effort S — risk low — category: experiments
  Why: T-2720 and T-2724 both came after a result existed. Nothing proves the Sample line was committed before the result.
  Done when: a test fails if a file in `bench/moonshot` has a result whose first commit is earlier than its script's Sample line. A planted reversed-order fixture fails it.

- **Replay "stage × rule" over real stage history** — FIX — value 4 — effort M — risk low — category: rules
  Why: T-2722's rule never fired because the tower's stage was 'genesis', not 'idle'. The question is whether each rule has ever fired in any stage the ledger recorded. This differs from checking that the stage exists: it counts firings per stage.
  Done when: a command prints, for each `fm next` rule, the stages it fired in over the last 60 days. Any rule with zero real firings is listed, and T-2722's rule would have been listed before the fix.

- **Treat "too/also/still/again" in an ask as a sibling-sweep trigger** — FEATURE — value 3 — effort S — risk med — category: intake
  Why: T-2722's "too" and T-2738's "the form fm task unblock takes" were both about a second surface that a first fix missed.
  Done when: filing an ask containing one of those words adds a "sibling surfaces" line listing other printers or consumers of the same value. Run against the 8 asks in the "missed" list, it flags at least 5.

- **Give each missed-ask class a named, checkable card** — CLEAN — value 4 — effort M — risk low — category: brainstorm
  Why: the pack's misses fall into about four classes: boundary records, never-fired rules, printed forms that a consumer refuses, and results kept without their method. Today they live as task titles.
  Done when: `class-cards/*.md` exists, each card names its question and one zero-token detector. Every new "asks no idea predicted" entry must cite a card or add one.

- **Hold a dissent as "pending" until its horizon fits the run** — FIX — value 3 — effort S — risk low — category: scoring
  Why: the carried gap is dissents scored against outcomes, and the survival window is 14 days. A generation can close before that, which scores dissents on data that doesn't exist yet.
  Done when: a dissent filed less than 14 days before the run's end reads "pending (due DATE)" and is excluded from the score. A fixture proves it.

- **Make the Exam's live reading a one-field `--json` path** — FEATURE — value 4 — effort M — risk low — category: exams
  Why: the gap is that briefs need a live-state reading, and free-form shell is gameable and unrerunnable. assumption: most existing verbs already emit `--json`.
  Done when: the Exam line is `live: <verb> --json .path` and a cold `fm exam brief T-id` re-runs it. A brief with no resolvable path is refused at filing.

- **Name which readers a summary line cannot see** — FEATURE — value 3 — effort M — risk low — category: legibility
  Why: T-2693 was a one-line-per-run summary that hid a second line. A caveat saying what was merged would have exposed it.
  Done when: any summary that dedupes by a key prints "(N folded by run+agent)". A test shows the count is nonzero on the T-2693 fixture.

- **Wild: Run a "stranger regrader" on every filed result** — FEATURE — value 3 — effort M — risk med — category: evidence
  Why: assumption: results kept as a tail (301 bytes) or beside a confounded criterion were not wrong, but nobody else could check them. A tool-less child gets only the script and the full output, and says what it would have concluded.
  Done when: a disagreement between the child's verdict and the filed verdict is recorded for the 3 existing kill results, and at least one case is shown for review.

- **Wild: Keep a "what I would have asked next" file per Mission, sealed at filing** — FEATURE — value 3 — effort S — risk low — category: anticipation
  Why: the same brainstorm that missed 8 asks is asked to predict the next 3. assumption: a sealed list scored against the next 3 typed asks gives a real hit rate, not a self-graded one.
  Done when: the file exists before the first brief is built, and `fm outcomes` reports hits against the user's next three asks.

- **Wild: Let the user's "premise already met" drops teach the canary** — FEATURE — value 3 — effort M — risk low — category: grounding
  Why: the guard-hint drop (fmguard.py:292) was a premise already met, which the canary should have caught before filing. assumption: the canary searches code but not the message text of existing refusals.
  Done when: the canary also greps string literals for the brief's quoted wording, and refiling the dropped brief is refused with the matching line.

- **Pair every new tower rule with the repo state it was tested in** — CLEAN — value 3 — effort S — risk low — category: rules
  Why: T-2722 says the rule "never fired here". It passed in a fixture but not in the repo that has a Genesis tower open.
  Done when: each rule's test names the state it ran in, and one rule per Mission also runs against a copy of the live state dir.

- **Add a "consumer must accept it" test for each printed command form** — FIX — value 4 — effort S — risk low — category: CLI
  Why: T-2738 (commas vs spaces) was printed by T-2683 and refused by the verb itself. This is narrower than checking that "Next:" parses: it feeds the printed id-list to the real verb in dry-run.
  Done when: each printed command that has a list form is run with `--dry-run` in a scratch home, and the test fails on the old space-separated form.

Next question: which of the eight missed asks would a state-history replay (stage by day) have caught, and which only a user could have caught?
Next question: if a class card detects nothing for a whole generation, is the class gone or just unvisited?
