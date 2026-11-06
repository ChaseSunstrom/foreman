# Brainstorm — lens: the second opinion (invented): a cold rival that sees only the request designs it differently; every place the plans differ is a reading or approach the first one missed

- **Run a blind rival planner and diff the readings** — FEATURE — value 5 — effort M — risk low — category: second opinion
  Why: the request asks for "the readings of the request" and "several candidate designs", but plan_gaps only counts options in text. Nothing shows a reading the first planner never thought of. Prior ideas touch blind-rival diffs (paraphrase rejection, missing-rows list), but none say how the rival is kept honest. Here the rival sees only the user's verbatim request, not the repo's plan, the steers or the tier. Each place its readings, approach list or "finished" definition differs becomes a named row in the plan: "rival read this as X; we didn't."
  Done when: a test feeds a planted request with two valid readings, where the first plan names only one, and `fm task focus` writes a "Rival differs" section that names the missed reading.

- **Give the rival a different model family and a different prompt shape** — FEATURE — value 4 — effort S — risk low — category: diversity
  Why: assumption: a rival from the same model with the same prompt tends to agree for the wrong reasons. A fixed rule picks the vendor or model that wrote neither the plan nor the code. The prompt asks for a design, not a review, so it can't just praise the plan.
  Done when: `fm plan rival` records the rival's model and the planner's, and refuses to run when they match unless a flag allows it and says why.

- **Count disagreement as the ambiguity signal for stopping** — FEATURE — value 5 — effort M — risk med — category: calibrated judgment
  Why: the request says to stop for the user "only when something is irreversible and ambiguous". Today ambiguity is a judgement made by the same writer. Rival and first plan agreeing on the reading means decide and record. Disagreeing on a reversible step means race. Disagreeing on an irreversible step means the one question to the user, with both readings quoted.
  Done when: a fixture with a disagreeing irreversible step produces exactly one `fm ask` with both readings, and a disagreeing reversible one produces a lane race and no ask.

- **Score the rival against outcomes, not taste** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: nothing in the pack says whether a rival is worth its tokens. At close, record whether any rival-only reading or option matched a reopen, a revert or a stuck ladder. Report per-tier "rival caught something" rates, and stop running it at tiers where it never does.
  Done when: `fm triggers` or a sibling lists rival runs, the hits and the hit rate by tier, and a tier with 10 or more runs and no hits drops to off by default.

- **Show the diff as a three-column table: both plans and the user's words** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the user's steers repeatedly say "show, don't claim". A table of reading, first plan, rival, with the user's quoted clause in the margin makes the difference readable in ten seconds in the terminal and the web UI.
  Done when: `fm plan diff ID` prints the table, and a snapshot test covers a row where only the rival covers a quoted clause.

- **Make the rival read the request, then the repo, in that order** — FEATURE — value 3 — effort M — risk low — category: reading depth
  Why: assumption: a rival that sees the repo first inherits its framing. Two passes: request alone, then request plus `fm graph blast`. The second pass is diffed against the first, so every place the code changed the reading is visible and the reason given.
  Done when: the rival output has two labelled sections, and a test shows a planted file that flips one reading and is named.

- **Fence the rival from the first plan's text in code, not in the prompt** — SECURITY — value 3 — effort S — risk low — category: independence
  Why: the standing steers require checks the code can't be talked out of. A child run gets a scratch directory with only the request, so it can't peek at the plan or the steers. That makes the "cold" claim checkable.
  Done when: a test runs the rival with a planted marker in the task file and the marker is absent from the child's input.

- **Let the rival propose the "do less" option first** — FEATURE — value 3 — effort S — risk low — category: approaches
  Why: the request lists "do less" and "use what exists" explicitly, but plan gates only count options. The rival is told to start from the cheapest approach that could satisfy the request, so the first plan's omission of it shows up as a diff.
  Done when: a fixture task with an existing tool that solves the request gets a rival option citing that tool, and the plan gate flags the first plan's lack of it.

- **Wild: Hold a debate round where each plan must kill the other in one paragraph** — FEATURE — value 3 — effort M — risk med — category: adversarial
  Why: wild. After the diff, each side writes the strongest single objection to the other's chosen approach, with a falsifier. Objections with a runnable falsifier go to a lane race. The rest are noted and dropped.
  Done when: a fixture with a flawed first plan produces a falsifier command that fails on the flawed approach in a lane.

- **Wild: Publish "where the rival disagreed" as a weekly page on the site** — FEATURE — value 2 — effort S — risk low — category: transparency
  Why: wild. The site already publishes Genesis data. Selected disagreements, with the user's consent setting and redaction, show what the second opinion bought. They also feed back as test cases.
  Done when: `fm genesis live` includes a rival-disagreements file and no row is published without the consent setting on.

- **Wild: Keep a standing rival that re-reads the user's steers as a stranger** — FEATURE — value 3 — effort M — risk med — category: steers
  Why: wild. Many steers are paraphrased into rules by the same model that acts on them. A cold reader that sees only the user's verbatim message and the stored rule says where the rule drifted from the words.
  Done when: a planted steer with a distorted rule is flagged with the user's quoted words as the reason.

- **Wild: Race the two plans' "finished" definitions against the same held-out scenario** — FEATURE — value 4 — effort L — risk med — category: evidence
  Why: wild. The pack asks whether "finished" ever needs to change. If the two plans define done differently, run each definition's check on a deliberately half-done fixture. The one that passes the half-done work is the weaker definition.
  Done when: for a planted half-done fixture, the report names which plan's criteria passed it.

- **Skip the rival when the first plan is trivially S-tier, and log the skip** — PERFORMANCE — value 3 — effort S — risk low — category: scaling depth
  Why: the request says to scale depth to risk, so an S task shouldn't pay an L task's cost. The rival is mandatory at L, on at M when blast radius lists past FIXes, and off at S. Every skip is recorded so the scoring idea can check it later.
  Done when: tests cover S, M and L, and the skip record appears for S.

- **Bind the rival's cost to the same budget as the plan's** — FEATURE — value 2 — effort S — risk low — category: cost
  Why: assumption: a second planner roughly doubles planning tokens, and the user doesn't want a surprise. The plan shows the rival's price before it runs, and a budget-exceeded case falls back to a cheaper model rather than skipping silently.
  Done when: the rival run writes its tokens to the task, and an over-budget fixture shows the fallback model name.

Next question: When the rival and the first plan agree, how often is it because they share a blind spot rather than because they are right, and what independent signal could tell the two apart?
Next question: Which readings of a request has the user historically corrected only after the build, and would a rival have seen them at plan time?
