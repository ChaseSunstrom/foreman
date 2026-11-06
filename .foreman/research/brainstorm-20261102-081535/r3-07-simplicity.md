# Brainstorm — lens: simplicity

- **Derive "unproven" as a set difference** — FEATURE — value 5 — effort S — risk low — category: proof
  Why: assumption: today "unproven" is something the model must remember to write. Changed files and changed symbols that no ran command or test path ever touched can be computed from the diff plus the tool log, with no model involved.
  Done when: a task that edits two files but runs tests covering only one finishes with the other file listed under "Unproven" without the agent saying so.

- **Entry-point smoke as the universal floor** — FEATURE — value 4 — effort S — risk low — category: proof
  Why: the map already names entry points (`plugin/bin/fm`, `app.py`, `index.html`). A cheap check that the thing starts (run it with `--help`, or serve it and fetch `/`) applies to every project and needs no per-kind prover.
  Done when: a finish on a fixture project whose entry point is broken shows a red "starts: no" line even though no unit test touches it.

- **Print each unproven item once, then carry it as one standing line** — CLEAN — value 4 — effort S — risk low — category: legibility
  Why: assumption: repeating the same "unproven: perf" at every finish teaches the reader to skim it. A per-project dedupe that shows an item only when it is new or changed keeps the label meaningful.
  Done when: three consecutive finishes with the same unproven item print it in the first and carry it in a single "still unproven (3)" line in the others.

- **Stay silent when the existing gate already proved it** — CLEAN — value 4 — effort S — risk low — category: legibility
  Why: assumption: extra proof output on a change fully covered by a green `fm check` is noise that crowds out the real gaps. Zero extra lines is the simplest correct answer here.
  Done when: a change covered entirely by a passing gate run adds no proof lines beyond the gate's verdict, and a change with an uncovered file adds exactly one line.

- **Lint hedge words in the finish text** — SECURITY — value 3 — effort S — risk low — category: honesty
  Why: the pack's number lint checks figures against the tool log. "Should work", "likely fixed" and "appears to" are the other way unproven claims slip through, and a word list is cheap and mechanical.
  Done when: a finish containing "should work" with no adjacent proof id is flagged, and the same sentence next to a proof id passes.

- **Prefix unproven commits so `git log` is the register** — FEATURE — value 3 — effort S — risk low — category: ledger
  Why: trailers are already proposed. A visible `[unproven]` marker in the commit subject needs no new store and `git log --grep` answers "what haven't we checked".
  Done when: `git log --grep '^\[unproven\]'` lists exactly the commits whose finish had unproven claims, and the marker is absent on fully proven ones.

- **Time-box the whole verification, not just each prover** — PERFORMANCE — value 3 — effort S — risk low — category: proof
  Why: per-prover timeouts are already proposed, but a finish with many slow provers can still stall. One total budget (assumption: 60 s default) turns "ran out of time" into explicit unproven lines.
  Done when: a fixture with three 30-second provers finishes at the budget with the unrun ones listed as unproven and the reason "time".

- **Decay unproven items nobody asks about** — CLEAN — value 3 — effort M — risk med — category: ledger
  Why: assumption: a register that only grows becomes the next thing nobody reads, which the pack already fears for other gauges. After 30 days with no touch to the covered files and no user mention, the item moves to an archive file.
  Done when: a 31-day-old untouched item leaves the active list and `fm` can still show it with an "archived" flag.

- **On a red proof, print the command and the last five lines, nothing else** — CLEAN — value 3 — effort S — risk low — category: legibility
  Why: assumption: explanations of failures are where the model hides and pads. The rerun command plus the real tail is checkable by the user in seconds.
  Done when: a failing prover output contains exactly the command line and at most five raw output lines, with no model-written paragraph.

- **Wild: run a "verifier-diet week" experiment** — FEATURE — value 4 — effort M — risk low — category: measurement — wild
  Why: assumption: many provers earn their keep by habit. For one week only the repo's gate plus the entry-point smoke may run, and reopen rates are compared with a normal week to show which provers changed a verdict.
  Done when: the week's report lists each prover as "changed a verdict" or "never did", and at least one is retired or kept on evidence.

- **Wild: end every finish with one "try to break it" command** — FEATURE — value 4 — effort S — risk low — category: meant
  Why: "does it do what the user meant" is the hardest claim to prove. Rather than a verdict, give the user the single command most likely to expose a mismatch, with the expected output in one line, and let their eyes decide.
  Done when: a finish carries exactly one runnable command with a stated expected result, and running it on a deliberately wrong build shows a visible difference.

- **Wild: make `ls` the proof dashboard** — FEATURE — value 2 — effort S — risk low — category: ledger — wild
  Why: assumption: a task directory holding an empty file named `PROVEN`, `PARTIAL` or `UNPROVEN` is readable in any terminal, file manager or sync folder with no tooling.
  Done when: `ls .foreman/tasks/*/` shows exactly one of the three marker names per closed task, and it flips when the covered files change.

- **Wild: write the finish as a three-line receipt, then ask a cold child to find the lie** — FEATURE — value 3 — effort M — risk med — category: honesty — wild
  Why: assumption: the shortest receipt is the easiest to attack. A tool-less child sees only those three lines and the evidence tail and must name any line the evidence does not support.
  Done when: on a fixture with one planted inflated line, the child flags it, and on an honest receipt it returns "none".

Next question: Which proof lines would the user have read, acted on or ignored in the past month, and can their reading behaviour alone set how much output a finish shows?
Next question: What is the smallest set of provers that would have caught every reopened task in the history, and is it smaller than what exists now?
