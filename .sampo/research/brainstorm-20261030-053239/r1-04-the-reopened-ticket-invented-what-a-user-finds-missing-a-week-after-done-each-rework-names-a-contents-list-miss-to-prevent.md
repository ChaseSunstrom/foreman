# Brainstorm — lens: the reopened ticket (invented): what a user finds missing a week after done; each rework names a contents-list miss to prevent

- **Record every reopen against its goal's contents list** — FEATURE — value 5 — effort M — risk low — category: goal ledger
  Why: T-2120 to T-2127 are the user's follow-up asks, each filed after a capability was "done". Nothing stores them as misses in the contents list that should have caught them.
  Done when: `fm reopen G-N "<text>" --class <missing-item|surface|verb|done-when|unverified>` appends a ledger event and adds a row to the goal's contents list. The text is quoted as data, and `fm goal check` fails on that row until it has a verify command.

- **Seed contents lists from a miss taxonomy built on past reopens** — FEATURE — value 4 — effort M — risk low — category: grounded lists
  Why: the "grounded contents lists" gap. Past reopens (exam contract, satellites, surfaces) repeat a few classes. Model boilerplate doesn't cite any.
  Done when: a new goal's contents draft ends with a "usual misses" block, and each entry cites the reopen id that taught it. An entry with no citation is dropped.

- **Hold done in a watch window before it is final** — FEATURE — value 4 — effort M — risk low — category: done verdict
  Why: the missing done-vs-stopped verdict. Verdict states could be `stopped:<reason>`, `done-watching` (N days) and `done-final`. A reopen inside the window counts against the contents list's author.
  Done when: a goal with all criteria green reads `done-watching` in `fm status`, and it flips to `done-final` only after the window with zero reopen events (tested with a faked clock).

- **Catch reopens from the user's own corrections** — FEATURE — value 4 — effort M — risk med — category: hooks
  Why: the user's words show the follow-up asks cluster after a ship. The UserPromptSubmit hook could spot "you forgot", "also needs" or "doesn't work on" within the window and link it to the goal by file or task overlap.
  Done when: a fixture prompt after a done goal creates a pending reopen proposal (not an auto-filed one), the text is quoted data, and the hook stays inside the bench_hooks gate.

- **Run a pre-mortem before declaring done** — FEATURE — value 4 — effort M — risk med — category: done verdict
  Why: the lesson that one reviewer pass per task catches what its own tests didn't. A tool-less cold child gets only the contents list and the diff summary, plus the line "a week later the user reopened this; give the 3 likeliest reasons".
  Done when: each reason must map to an existing criterion or become a new one with a verify command. Unmappable reasons are dropped, and the verdict shows the mapping.

- **Make the miss the next exam scenario** — FEATURE — value 5 — effort L — risk med — category: exam
  Why: the exam grades "done" only on held-out scenarios, but nothing turns a real reopen into one. Each reopen should leave behind a test that would have failed before.
  Done when: `fm reopen --scenario` writes a scenario file in the holdout split (never the train split). The scenario fails on the pre-fix tree and passes on the fixed one.

- **Require a first-use walkthrough per surface** — FEATURE — value 4 — effort M — risk low — category: surfaces
  Why: the MUST says it "works on every surface". A week-later miss is usually "I tried it on X and nothing happened". A recorded first-use run per surface proves it.
  Done when: closing a user-facing goal needs a walkthrough receipt (command, output, surface) for each surface in its contents list. A missing receipt blocks done, with its name in the reason.

- **Compare shipped artifacts to the last five done goals** — FEATURE — value 3 — effort S — risk low — category: simplicity
  Why: assumption: artifact kinds (tests, MASTER, README, CHANGELOG, site, pane, MCP) are derivable from each task's diff. A goal that ships fewer kinds than the median of its predecessors is a cheap, grounded miss signal.
  Done when: the done verdict lists artifact kinds the median shipped and this goal didn't. Each one is either filled or marked "n/a: <reason>".

- **Re-run done-when commands weekly so done can decay** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: docs, pane and site pages drift after later commits. A done goal that quietly breaks is a reopen waiting to happen.
  Done when: a stored done-when command that goes red on a later tree moves its goal to `reopened:decayed` with the failing command and the first bad commit.

- **Map every noun and verb in the user's words to a contents row** — FEATURE — value 4 — effort M — risk low — category: grounded lists
  Why: "Genesis keeps the site live" grew into five asks (export, style, live on, debounce, publish). Each word was a row nobody wrote.
  Done when: `fm goal check` fails on any phrase from the intake text with no row and no "excluded because" line. The phrases are quoted as data.

- **Backtest the contents generator on past reopens** (wild) — FEATURE — value 4 — effort L — risk low — category: exam
  Why: assumption: the intake text for T-2120 to T-2127 and their parent missions are on file. Replay old goals through the new generator and count how many real reopens it would have listed.
  Done when: `fm goal backtest` prints recall over known reopens, and a generator change that lowers it fails the exam gate.

- **Send in a ghost user a week later** (wild) — FEATURE — value 3 — effort L — risk med — category: agents
  Why: assumption: a cold child can use the product from README and `--help` only, with no repo history. It tries the five most obvious tasks and files whatever it can't do.
  Done when: a dry run on one finished capability yields at least one filed gap, or an explicit "nothing missing" receipt listing the tasks it tried.

- **Give every done goal a 14-day warranty** (wild) — FEATURE — value 3 — effort M — risk low — category: delight
  Why: assumption: owning reopens publicly makes the contents-list author care. Reopens inside the warranty jump the queue and show on the site page and pane as "warranty claims: n".
  Done when: a reopen inside 14 days is queued ahead of normal work, and the goal's page shows its claim count and clean-warranty status.

- **Fingerprint classes of miss and alert on repeats** (wild) — FEATURE — value 3 — effort M — risk low — category: observability
  Why: the same miss class (say "no site page") recurring across goals means a process hole, not bad luck. When one appears a third time, the process gets a rule instead of a reopen.
  Done when: a third reopen of one class files a clause proposal for the Stop hook (not self-granted) and shows the class counts in `fm goal status`.

Next question: Which reopen classes are caught by a contents list at all, and which need a post-done signal, such as user corrections or decayed done-when commands?
Next question: How long must the watch window be, and what does a goal cost the user while it sits at `done-watching` and still asks for carry-over each session?
