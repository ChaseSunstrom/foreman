# Brainstorm — lens: simplicity

- **Ship Lite mode as a measured claim** — FEATURE — value 5 — effort M — risk med — category: slimming
  Why: T-0794 ("Slim Foreman: Lite mode") is deferred while the verb, gauge and hook counts keep growing.
  Done when: `fm lite on` runs only plan, prove, close and the guard, and a duel run on the same scenarios shows no fewer tasks passed than full mode, with the hook p95 and injected chars printed beside it.

- **Fold the 40-plus steers into a short principles file** — CLEAN — value 4 — effort M — risk med — category: rules
  Why: The steers list is long, overlapping and partly truncated. Several rules say the same thing, such as the "never block on the user" rules and the "wait out usage limits" rules.
  Done when: `fm decide --list` shows at most 12 principle lines, and each old steer maps to one principle and keeps its automatic check passing.

- **Turn `fm doctor` into red-only output** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: The pack describes dozens of gauges and WARNs, and the user keeps having to ask whether one of them is real.
  Done when: `fm doctor` prints only failing or changed lines plus "N green", and `fm doctor --all` restores the full list.

- **Put a backlog cap on brainstorming** — FEATURE — value 4 — effort S — risk low — category: backpressure
  Why: There are over 30 deferred "Later from…" tasks and thousands of brainstorm lines, yet new rounds keep starting.
  Done when: `fm ideas` refuses to start a round while open or deferred tasks exceed a set N, and prints which ones to close first.

- **Retire stale deferrals into `someday.md`** — CLEAN — value 4 — effort S — risk low — category: queue
  Why: Many deferrals read "later: needs evidence…", and the queue lists them next to live work.
  Done when: a deferral with no wake condition, older than 60 days and not touched, moves to `someday.md` with its reason, and `fm next` no longer lists it.

- **Prune `plugin/skills`, which holds 1388 of 2125 files** — CLEAN — value 4 — effort M — risk med — category: footprint
  Why: The map layout puts skills as the largest directory by far.
  Done when: a report lists skills never loaded in the last 60 days of sessions, and the pruned set passes `fm doctor` with unchanged exam results.
  Assumption: most of those files are stack cards and reference text, not hand-written skills.

- **Combine the three gates into `fm gate`** — CLEAN — value 3 — effort S — risk low — category: developer experience
  Why: The map names three separate gate commands (`fm doctor`, `roundtrip.py`, `bench_hooks.py`).
  Done when: `fm gate` runs all three and exits non-zero on any failure, and ship and CI call only it.

- **Hide most verbs from default `fm help`** — FEATURE — value 3 — effort S — risk low — category: discoverability
  Why: The lean ratchet counts verbs, which shows they grow, and a newcomer sees all of them.
  Done when: `fm help` lists at most 10 core verbs with one line each, and `fm help all` lists the rest.

- **Cap output length with a lines-per-verb ratchet** — FEATURE — value 3 — effort M — risk low — category: legibility
  Why: The lean ratchet counts chars injected into sessions but not what verbs print to the user.
  Done when: a test fails if a verb's default output, on a fixture, exceeds its recorded line budget.

- **Wild: write `fm tiny`, a 200-line reference loop used as an oracle** — FEATURE — value 3 — effort L — risk med — category: slimming
  Why: wild. A tiny loop of plan, edit, prove, close, written in plain shell, shows what the other thousands of lines add.
  Done when: the exam runs `fm tiny` as an arm, and `fm doctor` prints the full version's lead over it per scenario kind.

- **Wild: once a week, offer one feature to delete** — FEATURE — value 3 — effort S — risk low — category: subtraction
  Why: wild. The night tick picks the capability with the least use and no measured gain, and asks for one word.
  Done when: Sunday's morning note names one candidate with its use count, and "yes" files a deletion task.

- **Wild: make the whole goal visible on one index card** — FEATURE — value 3 — effort M — risk low — category: goal
  Why: wild. A goal shows at most 7 rows, the done condition and the next row. More rows wait in a hidden backlog, and each is promoted when one closes.
  Done when: `fm goal` prints at most 12 lines for a plan of 40 rows, and closing a row promotes the next hidden one.

- **Echo the finish line instead of asking** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: A vague goal currently needs questions, and the user's repeated steer is "don't block on me".
  Done when: a vague goal prints one line "finished means: X; reply to change" and proceeds, with zero questions asked on the fixture scenario.

Next question: Which of the roughly 60 gauges and 40 steers has the user ever acted on, and can the transcripts show it?
Next question: If Foreman shrank to its core loop, which single regression would the user notice first?
