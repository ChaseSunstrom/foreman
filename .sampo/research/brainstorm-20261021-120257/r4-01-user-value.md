# Brainstorm — lens: user value

- **Tag every user message by why it was needed** — FEATURE — value 5 — effort M — risk low — category: unspoken needs
  Why: the stated north star is "I shouldn't even need to ask", yet recent asks include repeated release permission, "keep going", and a re-asked brainstorm. Nothing counts these as a class. Assumption: the intake log can label each message as repeat, permission, nudge, new or correction.
  Done when: `fm asks` over a fixture transcript prints each message with its label and the weekly avoidable-ask count, and a test asserts the labels.

- **Back-test the auto-notice trigger on whether its rounds were wanted** — FEATURE — value 4 — effort M — risk low — category: self-improvement
  Why: the "Foreman notices friction on its own" rule shipped, but there is no check that the rounds it opens are kept. This is the second-order step on "friction receipt" and "track whether friction fixes stay fixed". Assumption: a kept result can be inferred from later user messages and reverts.
  Done when: a replay over stored friction phrases reports precision and recall for the trigger, and the threshold is changed only through that report.

- **Keep a polarity corpus of the user's own phrasings** — FIX — value 4 — effort S — risk low — category: intake
  Why: "don't stop until complete, full auto" was recorded as a veto, and "stop asking me if you can release" is the same trap. Assumption: the classifier is regex or keyword based.
  Done when: a table-driven test of at least 30 real steers (veto, continue, grant, drop) passes, and the classifier cannot be edited without it running.

- **Close deploy tasks only when the live URL answers** — FEATURE — value 3 — effort M — risk med — category: capability
  Why: the Pages site and the `site/build.py` slip (the stray `--check/` folder) show that built is not the same as live. Assumption: the user's projects often deploy to a static host.
  Done when: a task with `deploy:` criteria stays open until a stdlib fetch of the URL matches the expected text, and fails over to a recorded rollback command if it doesn't.

- **Localize the user's own project** — FEATURE — value 3 — effort M — risk low — category: work with anything
  Why: "work with anything" is the stated goal, and no request type covers i18n. Assumption: users ship apps with hardcoded UI strings.
  Done when: on a fixture app with 10 hardcoded strings, `fm code "add German"` extracts a catalog, translates it, and a test renders the app in both locales.

- **Retry a rejected run on a different runner with the rejection as a hard constraint** — FEATURE — value 4 — effort M — risk low — category: delight
  Why: reopening with a reason is covered, but nothing says the second attempt should also change runner. Assumption: runner choice is a real variable in outcome.
  Done when: rejecting a fixture run with "too big a diff" starts a new run on a different runner whose plan carries that line as a criterion.

- **Keep a living architecture diagram for any project** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: `fm map` already knows layout and tests→src links, but only for Foreman's own postcard. Assumption: a Mermaid file under `.foreman/` is enough for most users.
  Done when: `fm map --diagram` writes a Mermaid graph, and a test fails when a new top-level module is missing from the committed copy.

- **Wild: Hand the user a morning quiz of three things Foreman built while they slept** — FEATURE — value 3 — effort M — risk low — category: wild
  Why: the user said "I shouldn't even need to say anything", but reports are skimmed. A three-question check ("did the TUI start before the model answered?") finds what they didn't absorb without a long report. Assumption: skimming is the failure mode.
  Done when: after an unattended stretch, the return card has three generated questions with one-key answers, and wrong answers file a task to explain that change better.

- **Wild: Let the user's accepted wording stand as the spec for the next release notes** — FEATURE — value 3 — effort S — risk low — category: wild
  Why: the release asks (1.2.43 to 1.2.48) are the user's own one-line summaries of what matters. Assumption: those lines are a better changelog voice than the generated one.
  Done when: `fm release` drafts notes by reusing the user's wording where it matches closed tasks, and a test shows that wording in the output verbatim.

- **Wild: Run a nightly "new user, old repo" rehearsal of the headline demo** — TEST/CLEAN — value 4 — effort M — risk low — category: wild
  Why: first-launch silence ("why can't I launch fm code like claude") was the original complaint. A scripted clean-HOME run of the demo request catches regressions before the user does. Assumption: a stub runner can stand in for the model.
  Done when: a nightly job runs `fm code "<request>"` in a clean HOME with a fake CLI, and fails if no first event appears within the sign-of-life budget.

- **Wild: Make mandates expire into a decision card, not silence** — FEATURE — value 4 — effort S — risk low — category: wild
  Why: "etc.", "recursive until dry" and "full auto" are open-ended, and a pile of thousands of ideas shows they never end on their own. Assumption: a hard stop with a one-key "continue / done / narrow" is welcomed.
  Done when: a mandate older than N rounds or $X stops itself, and the card offers three keys that each have a test.

- **Rank each shipped round-1 slate item by what the user did next** — FEATURE — value 3 — effort S — risk low — category: prioritization
  Why: 29 briefs are planned but unbuilt, and nothing says which one the user would notice. Assumption: telemetry from `fm code` runs (home screen, runner picker, `--task`) shows what is used.
  Done when: `fm code roadmap` lists the 29 with a use-count column, and it is the default order for the next build round.
