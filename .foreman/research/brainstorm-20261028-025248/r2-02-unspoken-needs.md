# Brainstorm — lens: unspoken needs

- **Track every promise Foreman makes** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: Redo and dropped items in the pack keep coming back ("recreated with interpretation", "criterion pinned to 235932b8"), so the user is catching follow-ups Foreman said it would do. Assumption: a "next I'll…" line in a reply is a promise the user will hold it to.
  Done when: a reply containing "next I'll" or "then I'll" creates a ledger entry, `fm status` lists it until it closes, and a promise that goes stale is reported as broken.

- **Start a redo from the reason it was dropped** — FIX — value 5 — effort S — risk low — category: redo flow
  Why: The pack lists several drops followed by recreated tasks ("recreated with interpretation and approach", "redo: work done but criterion 2 was pinned"). The first attempt's reason is lost, so the redo repeats the mistake.
  Done when: a task reopened after a drop opens with the drop reason and a diff of what changed since that attempt, and a test shows the reason appears in the redo's pack.

- **Give every receipt an egress line** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: The pack has an outbound-payload scan and a deny-by-default egress idea but no per-run statement. Assumption: the user wants to know what left the machine without checking logs.
  Done when: each closed-task receipt states bytes sent off-machine and to which host, and reads "none" for a fully local run.

- **Put the blast radius on every receipt in plain words** — FEATURE — value 4 — effort S — risk low — category: close receipts
  Why: The user's requests keep weighing what a change could break ("Cut Foreman's usage burn", "fm code app"). Assumption: the user judges a merge by how far it reaches, not by its diff size.
  Done when: each receipt names the files, commands and surfaces a change touches in one line, computed from the diff and not from the model's prose.

- **Show a since-you-looked digest per surface** — FEATURE — value 4 — effort S — risk low — category: return to work
  Why: The user works in bursts across the terminal, pane and web UI, and the pack shows state going stale between visits. Assumption: they want what changed since their last look, not a full status.
  Done when: opening the pane, web UI or `fm status` after a gap shows only the changes since that surface was last opened, with a test for a gap of two days.

- **Print the one command that undoes each change** — DOCS — value 3 — effort S — risk low — category: reversibility
  Why: The pack has undo-a-run and undo-a-part ideas, but no receipt tells the user how to reverse what was done. Assumption: the user wants a reversal path on the page they're already reading.
  Done when: every receipt that changed files ends with an exact, copy-pasteable undo command, and running that command on a clean tree restores the pre-change state (tested).

- **Show disagreement between reviewers instead of averaging it** — AGENTS — value 4 — effort M — risk med — category: multi-agent review
  Why: Brainstorm lenses and reviewers already run in parallel, but the pack shows only the merged slate. Assumption: when two agents disagree, the user needs both positions to decide, and a merge hides the disagreement.
  Done when: when two reviewers return opposing verdicts on the same change, the close shows both positions with their evidence, and a test covers an opposing pair.

- **Route the next change to a file the user objected to through a stricter gate** — FEATURE — value 3 — effort M — risk med — category: learned caution
  Why: The pack shows repeated undo and drop requests on the same areas (the usage budget, the gate lock, the pane). Assumption: a file the user objected to once is risky again.
  Done when: after a recorded objection to a file, the next change touching that file runs the full gate and its receipt names the earlier objection.

- **Give each change a sixty-second manual check** — DOCS — value 3 — effort S — risk low — category: verification
  Why: The user ends up testing by hand (the stall card, the pane keys, the site). Assumption: a short manual check that names one command and one visible result saves them a round trip.
  Done when: each close includes one command and one expected visible result, and the check fits on one line.

- **Keep a regression test for every behaviour the user praised** — CLEAN — value 3 — effort S — risk low — category: regression guard
  Why: The user steers and approves specific outcomes (the pacing fix, the reset deferral), and nothing protects them from later change. Assumption: praise in the user's words marks a behaviour worth pinning.
  Done when: a praised outcome is saved as a named test that fails when the behaviour is removed, and the praise is recorded with the task it came from.

- **Wild: write a correction's sentence into the test's name** — FEATURE — value 3 — effort S — risk low — category: correction memory
  Why: wild — the user's corrections are short and specific ("dont ask me for anything"), and a test named in their own words would show what was corrected long after the session ends.
  Done when: a correction from the user creates a failing test whose name is the user's sentence, and the test goes green only after the fix lands.

- **Wild: a habit mirror that reports one of the user's habits per week** — FEATURE — value 2 — effort M — risk low — category: self-knowledge
  Why: wild — the pack shows recurring habits (repeated re-sends, drops after a long wait, asks for the reset). Foreman could say which habit cost the most last week and what it would cost to change it, without judging.
  Done when: the weekly letter names one recurring habit with its measured cost in tokens and days, and it is omitted when no habit repeats three times.

- **Wild: have a cheap model read the receipt as the user and flag the line they'd skim past** — AGENTS — value 3 — effort S — risk low — category: pre-close review
  Why: wild — the user has pushed back on wording and length in several steers, and a reader-simulation pass could catch an unread or resented line before the user sees it.
  Done when: before close, a reader pass returns at most one flagged line with the reason, and a test shows a planted confusing line is flagged.
