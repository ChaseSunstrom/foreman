# Brainstorm — lens: deepen: exam

- **Build a seeded fake-clock week harness** — FEATURE — value 5 — effort M — risk low — category: exam
  Why: the gap is "a week of live ticks graded waits on the user's install". A `FOREMAN_NOW`-style clock lets a 7-day tick sequence run in seconds with no systemd. Every other exam idea here depends on it.
  Done when: `fm exam tick --week SEED` runs 672 simulated 15-minute ticks on a fixture repo with no timer installed and prints a per-tick decision log, identical across two runs of the same seed.

- **Grade the tick on a four-arm scoreboard** — FEATURE — value 5 — effort M — risk low — category: exam
  Why: it combines the planted-event, one-line-cron control, oracle and empty arms from the list into one run. This follows the standing rule that exam arms be free and that the free arm beating the session arm is a top gap. Assumption: the tick can be called as a function.
  Done when: the scoreboard shows precision, recall, median lateness and tokens per arm. The one-line-cron arm is shown beside the tick, and a tick that loses to it appears first in `fm exam scorecard`.

- **Have the answer key written by a child that never saw the tick** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: the standing rule says signals Foreman didn't author, and exam scenarios come from a tool-less child blind to the code. The child gets only plain-English trigger descriptions (no tick source) and writes a planted-event timeline plus the expected action at each point.
  Done when: the answer-key file records its author model and the sha of its input. The grader refuses a key whose input contains any tick source path.

- **Auto-twin every planted event and grade invariance** — FEATURE — value 4 — effort S — risk low — category: exam
  Why: it grows the metamorphic-twin idea into a rule. Shifting timestamps by a day, renaming files, reordering simultaneous events or changing the timezone must not change whether the tick fires. Each violation is a bug no hand-written answer key would catch.
  Done when: each scenario auto-generates at least 3 twins, and `fm exam tick` reports an invariance rate. A planted tick bug that depends on the weekday is flagged by it.

- **Mutation-test the tick to measure the exam itself** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: a green exam only means something if it can go red. Flip thresholds, off-by-one the due-ness comparison and swallow an exception in the tick, then count the mutants the week kills. The Brier-style "is this measure honest" worry applies here too.
  Done when: `fm exam tick --mutants` runs 20 or more mutants and prints a kill rate. A kill rate under an agreed floor makes `fm doctor` warn that the exam is blunt.

- **Label ticks with what the user did next** — FEATURE — value 5 — effort M — risk med — category: exam
  Why: it replays this repo's git history and the user's own drops and asks as hindsight labels. A tick that surfaced something the user then did within 24 hours was useful. One whose item the user dropped was noise. Both are signals Foreman didn't author, and the labels feed `fm outcomes`.
  Done when: replaying 30 days produces a useful/noise/missed count per trigger kind, where each label cites a commit sha or an intake line.

- **Run the exam through the session path and check reach** — FEATURE — value 4 — effort M — risk med — category: exam
  Why: the standing reach rule says a capability must be called by a real session path. A tick that fires correctly but whose result never shows up at session start or in `fm next` scores zero for the user. Assumption: tick output lands in a file the session reads.
  Done when: after a planted event, a scripted session start (headless, no live model needed) prints the tick's finding. The exam fails a scenario where the tick fired and the next-session surface stayed silent.

- **Score the tick's own confidence with the bets ledger** — FEATURE — value 3 — effort S — risk low — category: exam
  Why: night ticks already settle bets and the nightly digest names the worst-calibrated bet kind. If each trigger also records a probability that it was useful, the planted week gives the first 20 scored examples without waiting.
  Done when: the week's output includes Brier per trigger kind against its base rate, and `fm outcomes --judgment` lists tick bets under their own kind.

- **Shrink every failure into a permanent scenario** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: it goes beyond the heckler idea. When any adversarial or random week makes the tick misfire, a delta-debugger cuts the event stream to the smallest one that still fails and files it as a named regression scenario.
  Done when: a seeded misfire reduces from a 600-event week to 10 or fewer events and appears in the scenario set, red until fixed.

- **Wild: Chaos clock** — FEATURE — value 3 — effort M — risk low — category: exam
  Why: wild. Inject realistic clock trouble into the simulated week: laptop sleep for 14 hours, DST jump, a timer firing twice, a skipped run, a killed tick mid-write. Grade whether catch-up runs once per missed event and whether state files survive. This is also the only exam of the missed-timer case the user's real install will hit.
  Done when: every chaos kind has a scenario, and no kind causes a duplicate fire or a corrupted state file.

- **Wild: Dream week, a shadow replay every night** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: wild. `fm night` replays the user's actual last 7 days (commits, tasks, mail log) through the tick in shadow mode, and the morning digest shows what it would have done: "would have woken you 3 times; 2 were things you did within a day." The user sees self-triggering earn its place before installing anything.
  Done when: the digest includes a shadow-tick section with counts, and the replay writes nothing outside its sandbox.

- **Wild: Reverse exam, a child reconstructs the project from tick messages alone** — FEATURE — value 3 — effort S — risk low — category: exam
  Why: wild. A tool-less child reads only the week's tick notifications and answers 5 questions about the fixture project's state. If it can't, the messages carry too little (or too much) information. This tests usefulness of the words, which due-ness grading ignores.
  Done when: the exam reports an answer-accuracy percent per week. Replacing the messages with a blank string drops it to chance.

- **Freeze and rotate scenarios when the tick saturates them** — CLEAN — value 3 — effort S — risk low — category: exam
  Why: a scenario the tick passes for 5 straight runs stops measuring anything. The exam should retire it to a regression list and ask the blind child for a harder replacement, without editing existing item pools, which would break comparability (as the BEYOND-row steer found).
  Done when: after 5 passing runs a scenario moves to `regression`, a new child-written one takes its slot, and old run scores stay comparable by version tag.

Next question: Which trigger kind does the user most often ignore or drop today, and would the exam weight its false alarms above its misses?
Next question: If the fake-clock week and the user's real timer disagree on the same day, which one do we trust, and where is that recorded?
