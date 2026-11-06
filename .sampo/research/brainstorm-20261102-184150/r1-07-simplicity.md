# Brainstorm — lens: simplicity

- **Collapse outcome and live-state into one `Reads:` line** — CLEAN — value 4 — effort S — risk low — category: briefs
  Why: The carried gap asks for two fields, an outcome measure and a live-state reading, and every extra field is another place for a vacuous pass. One command that prints one number, plus its expected value, serves as both.
  Done when: the brief linter rejects an Exam with no `Reads: <cmd> -> <value>` line, and a brief whose single command prints the same value on the parent commit fails the lint.

- **Restrict live readings to existing `--json` key paths** — CLEAN — value 4 — effort S — risk low — category: safety
  Why: Another idea proposes sandboxing and read-only classification for free-form Exam commands. If a reading can only be `fm <verb> --json` plus a key, the guard question never arises and a cold process can re-run it.
  Done when: filing a brief whose live reading is not an `fm … --json .key` path is refused with the nearest valid verb named.

- **Default the outcome measure to "the user did not re-ask"** — FEATURE — value 4 — effort M — risk med — category: outcomes
  Why: Many briefs have no instrument, and the pack shows the user re-asking (the T-2738 fix of T-2683, the repeated "Ship N commits" asks). The ledger already records asks, so the default needs no new state. Assumption: re-asks can be matched by nearest-words comparison.
  Done when: a brief with no explicit measure gets `Reads: fm reasked T-N -> 0`, and the command reports 1 when a planted near-identical ask lands within 7 days.

- **Score a dissent by one bit from existing records** — FEATURE — value 4 — effort S — risk low — category: dissent
  Why: Dissent scoring is carried over. Earlier ideas add re-score schedules and a "never observed" state, which make a new ledger. Here a dissent counts as right if the dissented path was later dropped or reverted, and as wrong if it closed and nothing was re-asked. Both facts are already in drops, closes and reverts.
  Done when: `fm dissents` lists each dissent with right, wrong or unseen computed only from existing ledgers, and a fixture with one revert prints "right".

- **Replace the grid with six fixed questions** — CLEAN — value 4 — effort M — risk med — category: exhaustive thinking
  Why: The grid has spawned cell ids, history, heat, aging, n/a falsifiers and orphan detection, and that is a lot of machinery for "cover the space". Six questions answered in one line each give most of the coverage: who, where, when it fails, what exists, what is left out, how we will know. Assumption: the questions cover the grid's columns well enough that a cold read can't tell the difference.
  Done when: a Mission page has exactly six answered lines, and a cold read against 5 past requests finds no more omissions than the grid version did.

- **Scale breadth to the task's size** — PERFORMANCE — value 3 — effort S — risk low — category: cost
  Why: Exhaustive thinking on an S task costs more than the task. Assumption: effort labels exist at intake, as the open-work list shows.
  Done when: an S request gets three questions and no canary pass, an L gets all six plus canaries, and `fm` prints the chosen width on the page.

- **Expire a carried gap after two generations** — CLEAN — value 3 — effort S — risk low — category: carry-over
  Why: Gaps are carried generation to generation (dissents, canaries, Exam readings). Without an expiry the list only grows, which contradicts the lean steers. After two carries a gap either becomes a gate or is deleted with a recorded reason.
  Done when: `fm genesis check` fails on a gap carried three times with neither a gate nor a deletion reason.

- **Cap "left out" at five lines, ranked by cost of being wrong** — CLEAN — value 3 — effort S — risk low — category: reporting
  Why: Many left-out ideas add receipts, per-cell lists and site pages. A user reads five lines, so a long list is the same as none. The rest sits behind `fm left --all`.
  Done when: a Mission with 12 omissions shows 5 plus "7 more: fm left --all", and the five are those with the highest stated cost.

- **Add a brief-template toll: adding a field removes one** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: The Exam has grown by carried gaps (outcome, live, canary, blind author, parent-differs). A one-in-one-out check on the template stops the next Mission from adding a sixth.
  Done when: a test fails if the brief template's field count exceeds a recorded ceiling without a matching removal in the same commit.

- **Write the guess before the thinking (wild)** — FEATURE — value 3 — effort M — risk med — category: measurement
  Why: Nothing shows whether exhaustive thinking earns its cost. The child first writes its 30-second left-out list, then thinks, and the diff between the two is the dividend. A dry diff over several Missions is evidence to shrink the pass. Assumption: a tool-less first guess is cheap enough to be worth it.
  Done when: a Mission page shows "added by thinking: N of M items", and the count is stored for `fm outcomes`.

- **Write each brief as one sentence a parser can check (wild)** — FEATURE — value 3 — effort M — risk med — category: briefs
  Why: A brief of the form "After this, <command> prints <X> instead of <Y>" has the measure, the live reading and the parent difference built in, with no separate sections. If a brief can't be said that way, it is probably not ready to file.
  Done when: the linter extracts command, before and after from the sentence, and rejects 3 of 3 planted briefs that have no checkable change.

- **Ban "left out: nothing" and require a number (wild)** — FIX — value 2 — effort S — risk low — category: reporting
  Why: A bare "nothing" can't be told from an unrun check. The line must read "checked N, left out M", so a zero is a measured result with a denominator.
  Done when: a Mission page with the bare phrase "left out: nothing" fails the check, and "checked 6, left out 0" passes.

- **Let the cold reader delete one section from each Mission page (wild)** — CLEAN — value 2 — effort M — risk med — category: legibility
  Why: The tower files hold many sections that no decision reads. A cold child that must name the least useful section of each page gives a steady subtraction signal without a new gauge.
  Done when: each Mission close records one named section, and a section named in 3 consecutive Missions is removed from the template.

Next question: Of the Exam fields briefs carry today, which one has ever changed what the builder did, and which only gets filled in?
Next question: If the six-question form gives the same omissions as the grid on past requests, what is the grid's maintenance costing us?
