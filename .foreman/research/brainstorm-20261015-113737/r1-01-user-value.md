# Brainstorm — lens: user value

- **Record every guess as an assumption the user can confirm in one line** — FEATURE — value 5 — effort M — risk low — category: user value
  Why: assumption: terse requests ("fix the login timeout") force silent guesses, and the pack shows corrections and pushbacks but no place where guesses are listed. The ideas so far cover parking questions, not showing the guesses already made.
  Done when: a close-out for a vague request lists at least one `Assumed:` line, a one-line reply to the first one (`fm assume T-x 1 no: use X`) reopens only the affected step, and the correction is stored as a lesson.

- **Land the verified subset when a task is only partly green** — FEATURE — value 5 — effort M — risk med — category: close-out
  Why: assumption: closing is all-or-nothing. The "provisional done" and "landing ladder" ideas cover timing, not splitting. A task with 4 of 5 criteria proven should ship those 4 and carry the fifth forward.
  Done when: `fm task finish --partial` commits only the steps whose criteria have evidence, creates a child task for the rest that links back to the parent and the unproven criterion, and the parent shows "landed 4/5".

- **Add `fm fire`, an incident mode for "prod is broken, now"** — FEATURE — value 4 — effort M — risk med — category: urgency
  Why: assumption: the pack has no path for emergencies. A normal task runs plan, brief and the full done-tail. A real incident needs the queue paused, read-only recon first, the smallest possible diff, and a rollback line printed up front.
  Done when: `fm fire "login 500s"` pauses the queue, makes the first phase read-only, requires a printed rollback command before the first edit, and on close drafts a postmortem stub and resumes the queue.

- **Honour a work cap per task: `--cap 20m` or `--cap $2`, stopping at a shippable checkpoint** — FEATURE — value 4 — effort M — risk low — category: control
  Why: the pack's cap ideas cover children and recursive mandates, not the user's own tasks. The user is leaving an unattended stretch and wants a bounded bet.
  Done when: a task over its cap stops at the last green step, writes "stopped at cap: done X, remaining Y" to the ledger, and the next `fm resume` offers extend, ship, or drop.

- **Plan backwards from a deadline with `fm by <time>`** — FEATURE — value 4 — effort M — risk med — category: scope triage
  Why: assumption: users have real deadlines the ledger can't see. The existing "price every plan in tokens and minutes" and value scoring already supply the inputs.
  Done when: given a deadline and the queue, it outputs "will make: A, B; will cut: C (lowest value); at risk: D" using past duration per tier, and the cut items are parked with reason "deadline".

- **Print a manual acceptance card for criteria no test can prove** — FEATURE — value 4 — effort S — risk low — category: verification
  Why: assumption: UI feel, copy, and "does it read well" criteria currently close with no evidence or a faked check. "Try it yourself" covers one command, not a guided check.
  Done when: a task with a criterion tagged `manual` closes with a 2–5 step card (exact command or click path, expected result), the user answers `pass` or `fail <why>`, and the answer is stored as evidence graded "human-attested".

- **Track review debt: changed files the user has never looked at** — FEATURE — value 4 — effort M — risk low — category: ownership
  Why: `fm tour` ranks one task's or one day's changes, but nothing tracks the backlog across days. In a 688-task ledger the user owns code they may never have opened.
  Done when: `fm debt` lists files changed by Claude with no human read, edit, or `fm tour` view since, sorted by risk, and the SessionStart greeting shows the count only when it passes a set threshold.

- **Turn input/output examples in a request into the first failing tests** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: the pack covers screenshots, logs and URLs as reproduction, but "given X it should return Y" written in the user's own words is the commonest precise spec and isn't mentioned.
  Done when: a request containing two `X → Y` pairs produces a test file with those two cases that fails on the start tree, and the brief cites them as criteria.

- **Ledger Claude's own "I'll also…" promises** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: assumption: final messages say "I'll follow up on X" or "next I'd tidy Y", and intake captures only the user's messages, so those promises evaporate.
  Done when: the Stop hook extracts forward-looking commitments from the final message, each becomes a captured task or is explicitly dismissed within the turn, and `fm status` shows zero orphan promises.

- **Wild: Keep a living Q&A wiki that expires when its files change** — FEATURE — value 4 — effort M — risk low — category: knowledge
  Why: wild. Every "how does X work?" the user asks is answered, then lost. Saving each answer with the hashes of the files it cites turns questions into docs, and a changed hash marks the entry stale instead of wrong.
  Done when: a question answered with file citations is saved, `fm wiki "login"` finds it, and editing a cited file makes the entry show "stale: re-ask" in the listing.

- **Wild: Generate a stakeholder view page in plain language** — FEATURE — value 3 — effort M — risk med — category: sharing
  Why: wild. `fm page` serves the user. A manager or client wants "what shipped, what's next, what's blocked" with no task ids, paths or jargon, and none of the pack's page ideas have that audience.
  Done when: `fm page --stakeholder` writes one self-contained HTML file containing only titles rewritten in plain words and statuses, a test confirms no file paths, T-ids or secrets appear, and the run makes no network requests.

- **Wild: Give each project a weekly token allowance the user sets** — FEATURE — value 3 — effort S — risk low — category: budgets
  Why: wild. The pack has spend envelopes per recursive mandate and per-task budgets, but a person with five repos thinks in "this project gets this much this week". It's pocket money.
  Done when: `fm allowance web 5M` caps that project, the greeting shows "web: 3.1M left, resets Monday", crossing 80% asks once, and exceeding it parks unattended work.
