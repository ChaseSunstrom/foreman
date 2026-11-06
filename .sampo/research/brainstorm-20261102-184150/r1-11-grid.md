# Brainstorm — lens: grid

Lens: grid. Surfaces are CLI/hooks, the docked pane, the web UI and the Genesis site. Actors are the user, the building agent, other agents (parallel lanes and cold children) and the unattended tower. Failure modes are missing, wrong, slow, unsafe and unclear. Each idea names its cell.

- **Snapshot live-state readings per lane** — FIX — value 4 — effort M — risk med — category: lanes
  Why: cell = other agents × wrong. Missions 5-8 build in parallel `fm lane`s, and one lane's change can move the number another lane's Exam reads. Assumption: nothing isolates the readings today.
  Done when: a test runs two lanes whose changes alter each other's reading, and each Exam reads the value from its own worktree snapshot.

- **Record the user's verdict on each dissent from the web card** — FEATURE — value 5 — effort M — risk low — category: web, calibration
  Why: cell = web UI × user × missing. Dissent scoring needs ground truth Foreman didn't author, and the user's "upheld" or "overruled" is the cheapest such label. Without it, scores come only from outcomes that may never be observed.
  Done when: a dissent card has two buttons, a click appends a ledger row, and `fm outcomes` shows the user-labelled share beside the outcome-scored share.

- **Tag each dissent with its author's model family and score echo** — FEATURE — value 3 — effort S — risk low — category: dissent
  Why: cell = other agents × wrong. A dissent from the same family as the brief's writer may add little. Assumption: the dissenter's model is not yet stored on the dissent.
  Done when: `fm outcomes --dissent` prints a hit rate split by same-family and cross-family.

- **Cap each live-state reading's runtime and log it** — PERFORMANCE — value 3 — effort S — risk low — category: exam
  Why: cell = hooks × unattended run × slow. A reading that shells out to a slow command can stall the close path or a hook, and unattended nobody sees it hang. Assumption: no per-reading timeout is required today.
  Done when: filing a brief whose reading declares no timeout, or one over the cap, is refused, and each close records the reading's seconds.

- **Reject outcome measures that count the brief's own artifacts** — FIX — value 4 — effort M — risk low — category: exam, gaming
  Why: cell = CLI × agent × wrong. "Parent-differs" catches a measure that doesn't change, but not one that rises only because the diff wrote the thing it counts, such as grep for the new function name. This answers the earlier question about vacuous measures.
  Done when: a planted brief measuring "lines matching the new verb's name" fails filing, and one counting a pre-existing ledger class passes.

- **Search for the opposite of each "not built" claim** — FEATURE — value 3 — effort S — risk low — category: grounding
  Why: cell = agent × wrong. Canaries look for the idea, but standing steers and the dropped list hold its contradiction. The pack's drops include "by design: the guard refuses..." items that a counter-canary would surface.
  Done when: grounding prints "counter-evidence: none | <drop or steer id>" for each brief, and a planted brief that contradicts a steer gets a hit.

- **Hand the builder the overruled dissent inside the brief** — FEATURE — value 4 — effort S — risk low — category: briefs
  Why: cell = agent × missing. The objection that lost sits in the Mission file, but the builder works from the brief. Assumption: briefs don't carry it.
  Done when: a brief with an overruled dissent shows an "Overruled:" line with the reason and what to watch, and a test fails if the line is absent.

- **Report the effective number of independent lenses per brainstorm** — FEATURE — value 3 — effort M — risk low — category: brainstorm quality
  Why: cell = unattended run × wrong. Many lenses can converge on the same ideas, and the ideas-so-far list shows heavy repetition across titles. Assumption: no lens-overlap statistic exists.
  Done when: a brainstorm receipt prints "N lenses, M effectively distinct" from overlap of their titles, with zero tokens.

- **Give a user-facing reason code when a reading can't be taken** — FEATURE — value 3 — effort S — risk low — category: unattended, clarity
  Why: cell = unattended run × user × unclear. When the tower can't measure, the user sees a blank. The earlier question about "unmeasured vs block" needs a visible reason.
  Done when: an unmeasured Exam row shows `unmeasured: <reason>, fixable by <actor>`, and `fm doctor` counts them.

- **Poll the user on how much a broken cell would annoy them** — FEATURE — value 3 — effort M — risk low — category: grid weighting
  Why: cell = CLI × user × unclear. Cells are weighted by guesses, and `fm ask` already exists. One yes/no per week on an empty cell gives a signal Foreman didn't author.
  Done when: one weekly `fm ask` question picks an empty cell, and the answer reorders the next Seed's empty-cell list.

- **(wild) Rebuild the grid from the final diff alone** — FEATURE — value 4 — effort M — risk low — category: exhaustiveness
  Why: cell = agent × missing. A cold child sees only the landed diff and writes the grid it implies. Cells in the diff but absent from the filed grid show what the thinking missed.
  Done when: a Mission close prints "diff touched N cells the grid did not name" with their names.

- **(wild) Give the dissenter a points stake and let the user cash it** — FEATURE — value 3 — effort M — risk med — category: dissent
  Why: cell = other agents × unclear. A dissent that must bet points reads as a prediction with a price. The user can see the accumulated payoff per lens.
  Done when: each dissent records a stake, and settlement at the outcome date moves the lens's balance.

- **(wild) Run the same request's grid on a stranger's small repo** — FEATURE — value 3 — effort L — risk low — category: generality
  Why: cell = unattended run × wrong. Cells that fill identically on a foreign repo are generic. Ones that don't are Foreman-specific, so the check reveals which "covered" cells depend on its own quirks.
  Done when: a command prints the cells that held on the foreign repo and the cells that went empty.

- **(wild) Give the hard-hat a "what I haven't looked at" blink in the pane** — FEATURE — value 2 — effort S — risk low — category: delight, clarity
  Why: cell = docked pane × user × unclear. A small, honest marker that N grid cells are still empty fits the pane's role as state at a glance.
  Done when: the pane shows the count, and it drops when a cell fills.

**Cells left empty:**
- Site × unsafe: the publish-time leak scan and the redaction ideas already cover it.
- Hooks × user × unsafe: the guard's existing remit.
- Web UI × agent × slow: nothing in the pack shows an agent loading it.
- Pane × other agents × missing: no evidence either way.

Next question: which of these dissent-and-outcome labels has the user actually supplied unprompted in the last 30 days, and would a web button change that?
Next question: when two parallel lanes' Exams share one live reading, which lane closes first in practice, and does the loser's reading come out stale?
