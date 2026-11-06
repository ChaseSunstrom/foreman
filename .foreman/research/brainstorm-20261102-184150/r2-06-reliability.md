# Brainstorm — lens: reliability

Lens "reliability" is read as: what makes Exhaustive thinking (gen 4, Mission 1) hold up when it runs unattended, crashes mid-way, or is read cold later. Round 2 ideas only; I avoid the pile's existing kill-point, torn-tail, fail-open and cold-read items.

- **Make a Mission file atomic with a sentinel footer** — FIX — value 4 — effort S — risk low — category: durability
  Why: pile has "File a Mission's briefs as one transaction" but no check that a half-written `mission-*.md` is detected by readers; assumption: a crash between the page write and brief intake leaves a Mission with fewer briefs than its table lists.
  Done when: killing the writer after the page write but before intake makes `fm genesis check` print "mission incomplete: N of M briefs" and exit nonzero.

- **Pin every Exam reading to a timeout and an exit-class** — FIX — value 4 — effort S — risk low — category: Exam
  Why: the carried gap says every Exam names a live-state reading; a hung or slow reading (service down) would stall a close or be recorded as pass. Pile has "cap runtime" and "reason code" separately; this joins them into three outcomes: ok, failed, unreadable.
  Done when: a reading that sleeps past its cap is recorded as `unreadable (timeout)` and never as a pass in a test.

- **Make dissent scoring idempotent on re-run** — FIX — value 3 — effort S — risk low — category: scoring
  Why: dissents scored against outcomes will be re-scored at +7 and +30 days (pile); assumption: a second scoring run appends a second row and inflates the tally.
  Done when: running the scorer twice on one ledger yields byte-identical output and the same totals.

- **Run a canary's positive control before every "not built" verdict** — FIX — value 4 — effort M — risk low — category: grounding
  Why: "canaries near the idea" is a carried gap; a canary with a broken search (wrong cwd, renamed dir) silently returns zero hits and every idea reads as novel.
  Done when: with the search root pointed at an empty dir, the canary step fails loudly rather than reporting "not built".

- **Snapshot the Exam's inputs at filing, hash them in the brief** — FEATURE — value 4 — effort M — risk med — category: reproducibility
  Why: question left by earlier brainstorms: which Exams are re-runnable cold. Without recorded inputs (HEAD, state dir, command, env allowlist) a later cold reader cannot tell a changed world from a broken measure.
  Done when: `fm exam replay <brief>` on a clean checkout prints the recorded input hash and either the same reading or a named difference.

- **Detect a Mission that ran against a stale pack** — FIX — value 3 — effort S — risk low — category: staleness
  Why: the pack's map says "as of an older HEAD"; a Mission whose pack predates recent commits can call something unbuilt that already landed (pile: the repeated "already built" drops).
  Done when: a Mission filed with a pack older than N commits carries a visible "pack stale by K commits" line and its canaries rerun against current HEAD.

- **Bound the lens fan-out with a partial-result contract** — FEATURE — value 3 — effort M — risk low — category: unattended
  Why: T-0831 (salvage partial results from capped children) is deferred; exhaustive thinking multiplies children, so one capped lens should yield "lens X: no output, reason" in the left-out list, not vanish.
  Done when: a lens child killed mid-run appears in the Mission's left-out section with its reason, and the Mission still files.

- **Make the left-out receipt survive a crash by writing it first** — FIX — value 4 — effort S — risk low — category: durability
  Why: the pile says "write the receipt incrementally"; the stronger form is to write an empty receipt at Mission open and append per cell, so a crash still leaves a truthful "unfinished" file rather than none.
  Done when: killing a Mission at a random point leaves a receipt marked `unfinished` listing the cells not reached.

- **Wild: Run a monthly "stranger replay" of one old Mission on current code** — FEATURE — value 3 — effort M — risk low — category: regression
  Why: assumption: Mission behaviour drifts as readers change; replaying a frozen pack for an earlier Mission and diffing its grid shows drift no unit test names.
  Done when: the replay prints a grid diff against the stored one, and an unchanged pack with unchanged code diffs to empty.

- **Wild: Plant a known gap in the pack and check the Mission finds it** — FEATURE — value 4 — effort M — risk low — category: recall
  Why: no measure says whether "exhaustive" is true; a seeded omission (a fake missing surface) with a recall score gives the first number.
  Done when: a Mission run on a pack with one planted gap lists that gap in its output, or the run reports a recall of 0 for the seed.

- **Wild: Let a Mission refuse to say "exhaustive" without a lens-agreement floor** — FEATURE — value 3 — effort S — risk low — category: honesty
  Why: assumption: lenses from one model family echo each other; the Mission text claims coverage the lenses only repeat. A floor on distinct cells found across lenses keeps the word honest.
  Done when: a Mission where 90% of ideas are duplicated across lenses prints "narrow: N distinct cells" instead of "exhaustive".

- **Version the Exam line format and reject unknown versions** — CLEAN — value 2 — effort S — risk low — category: compatibility
  Why: briefs filed in gen 3 carry older Exam shapes; the new `outcome:`/`live:` lines will be read by old parsers that skip them without a sound.
  Done when: an old reader given a v2 brief fails with "unknown exam version" and not a silent pass.

Next question: what happens to a Mission's briefs when the repo is rebased or a lane lands between filing and the Exam's live reading?
Next question: which of these checks can run with zero tokens inside `fm genesis sweep`, so reliability does not depend on a model being up?
