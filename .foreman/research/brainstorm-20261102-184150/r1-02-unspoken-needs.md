# Brainstorm — lens: unspoken needs

- **Ship at Mission close under the standing push grant** — FEATURE — value 5 — effort S — risk med — category: autonomy
  Why: 7 of the user's last 20 asks are "Ship N commits to main", and a standing grant says to push without asking. T-2722 only made `fm next` name the ship step, so the user still has to type the ask.
  Done when: a Mission-close fixture with green gates and a set grant runs `fm ship` unprompted and the receipt shows grant spent; with no grant it only prints the step.

- **Trace every clause of the request to a brief or a stated omission** — FEATURE — value 5 — effort M — risk low — category: exhaustiveness
  Why: this Mission's request has three carried gaps (dissents, canaries, Exam lines). Nothing shows the user that each was taken up. Assumption: they can't currently tell without reading every brief.
  Done when: the Mission page opens with a clause table in which each clause links to a brief id or a "left out: reason"; a test fails if any clause is missing a link.

- **Keep a carried-gap register with a closing test** — FEATURE — value 4 — effort M — risk low — category: continuity
  Why: gaps arrive as prose ("Carried gaps: …") and no record shows when one closed. Earlier ideas carry left-out cells forward but don't record closure.
  Done when: each carried gap has an id, an origin generation and a command that tests it; `fm genesis check` lists gaps open for 2 or more generations first.

- **Require a typed wait on every block** — FIX — value 4 — effort S — risk low — category: queue
  Why: on the real pile of 44 blocked tasks the asks/depends_on grouping "found nothing: waits are written in block reasons", and the fix was a regex over free text.
  Done when: `fm task block` without `--waits user|T-id|host|time` is refused, and the unblock-line grouping on a fixture of 10 blocked tasks matches the declared waits exactly.

- **Keep user-held steps out of Done-when** — FIX — value 4 — effort S — risk low — category: briefs
  Why: a brief was dropped because "criterion 3 bundled the user-held deletion (T-2702) and can't be edited after a failing run". One user-owned step poisoned the whole task.
  Done when: filing a Done-when with a step marked or detected as user-held is split into a separate "user step" line, and a failing user step leaves the other criteria's verdicts intact (test).

- **Flag truncated evidence at record time** — FIX — value 4 — effort S — risk low — category: evidence
  Why: "the recorded M-02 output was only its tail (kill.txt, 301 bytes)" forced a rerun. Steers are already stored verbatim, but result files are not held to that.
  Done when: any recorded result file stores its full byte count and sha256 beside the text, and `fm doctor` names a result whose stored length is less than the captured length.

- **Run each Exam as a script-and-result pair** — FEATURE — value 4 — effort M — risk low — category: measures
  Why: the user asked for kill scripts, results beside them, and a "Sample" line, all held by a test (T-2720, T-2721, T-2724). Briefs' Exam lines are the same kind of claim but have no such pair.
  Done when: every new brief's Exam is a file under `exams/` plus a stored result, and a cold process can re-run it with no session state (test).

- **Lift every number in an ask into a checked Done-when line** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: the asks carry counts: "first 20 moonshots", "two blind attempts each", "3 of 3 rebuilt", "9 or fewer scenarios", "5 commit(s)". They read as acceptance criteria.
  Done when: filing the ask "file the first 20 moonshots" produces a Done-when line "count == 20", and closing with 19 fails it.

- **Record who left a cell out, the user or Foreman** — FEATURE — value 3 — effort S — risk low — category: omissions
  Why: the user narrowed scope: "scoped to the volatile-path audit; ledger conservation is left out". That is a deliberate user exclusion and shouldn't read like a Foreman gap.
  Done when: the left-out receipt separates "excluded by you (quote)" from "not reached", and the not-reached list drives the next pack.

- **Learn the user's habit of narrowing scope** — FEATURE — value 3 — effort M — risk med — category: scope
  Why: recent steers narrow ("scoped to…"), re-aim ("approach 2") or extend after the fact. Assumption: Foreman files wider than the user wants, then they trim it by hand.
  Done when: over the last 30 filed briefs, a precision measure shows the first brief covers the narrower reading, with wider siblings as a tail the user can promote; the measure is checked on a fixture of past steers.

- **Keep a wish list of instruments for unmeasurable outcomes** — FEATURE — value 3 — effort S — risk low — category: measures
  Why: this Mission's brief requires an outcome measure for every Exam, and some outcomes will have no reading available. Assumption: they currently end as "unmeasured" with no way to see what would measure them.
  Done when: `fm genesis check` prints unmeasurable outcomes grouped by the instrument each needs, ranked by briefs blocked.

- **Wild: Open a hunch box for the user's doubts** — FEATURE — value 4 — effort M — risk low — category: dissent
  Why: assumption: the user's one-line "I bet you missed X" is the best dissent source and is currently lost in chat. wild
  Done when: `fm hunch "X"` files a dissent, and the next outcome review scores it hit or miss and prints the user's running hit rate.

- **Wild: Require one unasked brief per Mission** — FEATURE — value 3 — effort M — risk med — category: surprise
  Why: exhaustive thinking should sometimes produce something no clause or steer asked for; a forced slot makes its survival rate measurable. wild
  Done when: each Mission has one brief tagged "unasked" with no clause trace, and the generation report prints how many of these the user kept or dropped.

- **Wild: Map the repo areas no pack ever mentioned** — FEATURE — value 3 — effort M — risk low — category: blind spots
  Why: the map counts 2176 files, 1388 of them under `plugin/skills`, but the pack names few. Assumption: whole areas are never brainstormed about. wild
  Done when: a command lists directories with zero mentions across the last 10 packs, and a Mission page shows it as the empty region of a map.

Next question: which of the user's repeated typed asks ("Ship N commits") has Foreman never automated because a grant or gate hides the need, and what is the next such ask?
Next question: when the user narrows or redoes a brief, is the cause the request's wording, the pack's scope, or the brief writer, and can that be told apart from the ledger?
