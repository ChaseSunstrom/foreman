# Brainstorm — lens: user value

- **Ship with the batch's readings beside the push** — FEATURE — value 4 — effort S — risk low — category: ship
  Why: "Ship N commits to main" is among the user's most frequent asks (about 8 times in the pack), and the receipt says what shipped but not what it did.
  Done when: `fm ship` output lists each shipped task with its Exam outcome reading (value at filing → value now, or "unmeasured"), and a test with one unmeasurable task prints "unmeasured", not a blank.

- **Parse every outcome measure for unit, direction and threshold** — FIX — value 4 — effort S — risk low — category: exam
  Why: the carried gap is that outcome measures can be vacuous. A line like "improves hook p95" passes an `outcome:` presence check but can never fail. Assumption: the filing check only tests that the line exists.
  Done when: filing rejects `outcome: improves X` and accepts `outcome: hook p95 ms, lower is better, ≤ 40`. A fixture of 10 real gen-3 Exam lines shows the count rejected.

- **Store each Exam reading as a diffable file beside its brief** — FEATURE — value 3 — effort S — risk low — category: exam
  Why: a live-state reading that exists only in session output can't be re-read by a cold reader. Assumption: readings aren't persisted next to the brief today.
  Done when: filing writes `readings/T-####.txt`, and a second reading appends a line. `git log -p` on the file shows the trend, and a cold process reads it with `cat`.

- **Add a "wrong-brief symptom" line to every brief** — FEATURE — value 3 — effort S — risk low — category: briefs
  Why: dissents need an outcome to be scored against, but nothing says what a wrong brief would look like. One observable symptom gives the dissent score a target and doubles as an alarm.
  Done when: a brief without `if wrong:` is refused, and one dissent is scored in a test using only that line.

- **Show pending dissents with a day counter in `fm next`** — FEATURE — value 3 — effort S — risk low — category: dissent
  Why: scoring against the 14-day close-survival signal needs waiting, and a dissent that waits silently is forgotten. Assumption: pending dissents aren't surfaced anywhere.
  Done when: `fm next` prints "dissent D-12: day 9 of 14, scores on survival", and the line disappears once scored.

- **Ask once for the user's walk-away condition** — FEATURE — value 4 — effort S — risk low — category: intent
  Why: the user drops ideas for ambition-neutral reasons ("by design", "gap") but never states what would make them stop caring about a capability. A stated quit condition becomes a measurable steer.
  Done when: Mission open asks "what would make you cancel this?" once, with a default of "none". The answer is stored via `fm decide --check` and `fm doctor` names a missing one.

- **Sum the Exam readings' runtime before filing** — PERFORMANCE — value 3 — effort S — risk low — category: speed
  Why: every brief now adds a live reading, and the Mission cost isn't shown. A slow reading makes the cold reproduction timeout.
  Done when: the filing report prints total reading seconds and the three slowest, and a reading over a named cap is flagged.

- **Offer a paraphrase tier for steers on the public Genesis site** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: steers carry the user's verbatim words, and `fm genesis live` publishes site data to main on its own (standing rule). Assumption: some verbatim text, such as the push-grant quote, reaches the public page.
  Done when: published data holds a short paraphrase plus a local-only pointer for each steer. A test plants a verbatim sentence and an email address, and neither appears in `site/genesis`.

- **Show the Mission's wall-clock per stage** — PERFORMANCE — value 2 — effort S — risk low — category: speed
  Why: the user sees "about two minutes" in the demo but gets no timing for brainstorm, grounding and filing. Assumption: the Mission report shows only spend.
  Done when: the report lists seconds for the brainstorm, grounding, filing and cold-read stages, summing within 5% of the total.

- **Wild: Promote a hand check into an Exam reading** — FEATURE — value 4 — effort M — risk med — category: exam (wild)
  Why: users re-run commands by hand to distrust-check a verdict, and those commands are already in the transcript. Assumption: the bash-input channel can be read.
  Done when: `fm exam adopt` turns the user's last hand-typed check on a task into its live reading, and a replay in a cold shell gives the same value.

- **Wild: Let the user countersign a dissent with one key** — FEATURE — value 3 — effort S — risk low — category: dissent (wild)
  Why: a dissent the user also doubts is stronger evidence than one the model raises alone, and it is cheap to record.
  Done when: the countersign key records "user-backed" on the dissent, the scorecard shows a separate hit rate for user-backed dissents, and a test covers both.

- **Wild: Compile repeated asks into a zero-token `fm again`** — FEATURE — value 4 — effort M — risk med — category: rituals (wild)
  Why: "Ship N commit(s) to main" recurs verbatim-ish; the need behind it is not having to say it.
  Done when: `fm again ship` runs the same gated flow as the last identical ask, refusing without the grant, and the n-gram miner flags at least one real repeat in the user's history.

- **Wild: Open each session with a "previously on Foreman" card** — FEATURE — value 3 — effort S — risk low — category: delight (wild)
  Why: the tower runs on its own across generations and the user returns to a pile. Three lines: what closed, what the last dissent was, and what waits on them.
  Done when: session start prints at most 3 lines drawn from the ledgers (no model call), none when nothing changed, and a test pins the output.

Next question: Which gen-3 briefs would pass a unit-and-direction check on their outcome measure today, and how many of those has the user ever re-read?
Next question: Does the user read the public Genesis site's steer text, and would a paraphrase lose the meaning they care about?
