# Brainstorm — lens: blind spots

- **Write the injection ledger at emit time** — FIX — value 4 — effort M — risk low — category: measurement
  Why: T-2667 found `fm burden` missed SessionStart context sent as `hook_success` stdout, because the gauge infers channels from the transcript. Each hook already knows what it emitted.
  Done when: every hook appends `{hook, channel, chars}` when it emits, and a test fails if `fm burden`'s total differs from the sum of those rows for a fixture session.

- **Harvest a slow-input corpus from real hook timings** — FEATURE — value 4 — effort M — risk low — category: guard performance
  Why: T-2668 had to ask for a pathological-input timing test, and the inputs were hand-picked. Real slow calls are better test cases.
  Done when: any hook call over a set ms bar stores its input shape (hashed, length-classed) in a corpus file, and the next `fmguard` timing test replays that corpus and fails on any case over the bar.

- **Stop a retry loop by its error fingerprint** — FEATURE — value 4 — effort M — risk med — category: runaway spend
  Why: T-2669 stops a run on dollars with no close. A loop that repeats the same failing command spends the same dollars before that fires (assumption: loops show up as repeated identical failures).
  Done when: a fixture run repeating one command and error 3 times stops with "same failure ×3" named in the receipt, and a run with varied errors isn't stopped.

- **Build a grounding lexicon from help strings and MASTER anchors** — FEATURE — value 4 — effort M — risk low — category: brainstorm quality
  Why: T-2659 had to ask for three phrasings and for the verbs' own help strings to be checked before "new". Hand-written phrasings only cover the words someone thinks of.
  Done when: `fm lib` or the brainstorm skill expands an idea title into synonyms drawn from verb help text, and a test finds an existing verb for 3 known-reworded duplicates from the drop list.

- **Feed every "already built" drop back into the lexicon** — FEATURE — value 3 — effort S — risk low — category: brainstorm quality
  Why: the drops cite verbs that already existed (e.g. `fm usage --prune`, `check_predictions`). Each is a search miss that could be fixed once.
  Done when: filing an "already built" drop requires the existing verb or file, and the next grounding run for the same phrase finds it.

- **Collapse the repeated Mission request into one command** — FEATURE — value 4 — effort M — risk med — category: process automation
  Why: T-2666, T-2671 and T-2677 are the same sentence for Missions 5, 6 and 7 (brainstorm, ground, record, file, intake). The user retypes the pipeline each time.
  Done when: `fm genesis mission N --capability X` runs all stages and writes one receipt listing each stage's ledger record, and rerunning it is a no-op.

- **Carry follow-up measurements into the next Mission's brief automatically** — FEATURE — value 3 — effort S — risk low — category: continuity
  Why: T-2677 asked to "report Mission 6's two use counts". That's a measurement owed from one Mission to the next, and only the user's memory carried it.
  Done when: a Mission close can write `owes: <metric>` lines, and the next Mission's brief opens with their values, or "unmeasured" if absent.

- **Mine other agent trackers for bug classes Foreman hasn't asked about** — FEATURE — value 3 — effort M — risk low — category: blind spots
  Why: assumption: the gaps found here (output-channel undercounts, regex blowup, runaway spend) also show up in public issues for Claude Code, Codex, opencode and aider.
  Done when: a stored digest of 30+ real issues, clustered by class, lists each class with the Foreman test covering it or "none", and each "none" is filed.

- **Report ask-debt: asks Foreman now handles unprompted** — FEATURE — value 3 — effort M — risk low — category: legibility
  Why: the pack lists many user asks that were later made automatic. Nothing shows whether the number of manual asks per class is falling.
  Done when: `fm digest` prints, per blind-spot class, asks last 30 days against the prior 30, and each ask is linked to its task.

- **Wild: Run a "stranger's first PR" drill against the guard's timing** — FEATURE — value 2 — effort M — risk low — category: guard performance
  Why: assumption: real repos contain command shapes (generated shell, minified heredocs) nobody on this project types. A child invents commands from other ecosystems' build logs, and the slowest 10 join the corpus.
  Done when: a nightly run adds at least the top slow cases to the corpus and reports the worst ms.

- **Wild: Fail a gauge's tests unless it knows its own zero** — FIX — value 3 — effort S — risk low — category: measurement
  Why: the burden gauge counted zero for a channel it couldn't see and looked healthy. This extends the undercount class (assumption: other gauges can also read zero silently).
  Done when: each gauge declares `expect_nonzero_when:` and `fm doctor` reds any gauge reading 0 while that condition holds in the ledgers.

- **Wild: Hold a monthly "what did the user have to say twice" report** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: asks that repeat, such as the Mission sentence and the "ground it" step, mark missing defaults. The user can't see how often they repeat themselves.
  Done when: a report clusters near-identical user asks across 30 days, names the top three, and each links to a task or a recorded "intentional".

- **Wild: Name the blind-spot class on every user-filed FIX at intake** — CLEAN — value 2 — effort S — risk low — category: process
  Why: T-2659, T-2667 and T-2668 are three classes (grounding, channel gauge, hostile input). Naming the class is what lets a sibling sweep run (assumption: a classifier from title words is enough).
  Done when: intake writes a `class:` field on each user-filed FIX, and a test shows the three tasks above get three distinct classes.

Next question: Which of Foreman's own readers still infer from a transcript what their writer could have recorded directly, and what does each undercount today?
Next question: When the user repeats a pipeline sentence three times, does Foreman notice by itself, and who gets told?
