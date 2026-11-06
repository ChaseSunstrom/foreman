# Brainstorm — lens: capability map

- **Fetch upstream on every tick and flag queued tasks it just invalidated** — FEATURE — value 4 — effort M — risk low — category: anticipation
  Why: assumption: lanes predict overlap between queued tasks, but nothing in the pack compares the queue with `origin` changes. Merge pain is only found at ship time.
  Done when: with a fixture remote that changes a file named in an open brief, the next tick marks that task "upstream changed: <file>", and `fm next` shows it.

- **Warn when a request names things the current repo doesn't have** — FIX — value 4 — effort S — risk low — category: wrong-target
  Why: assumption: a user with several registered repos will sometimes ask from the wrong cwd. Today that is only caught after the work starts.
  Done when: a request naming a file, verb or symbol found in no tracked file but present in another registered repo prints "did you mean <repo>?" before any task is created.

- **Checkpoint before a predicted compaction** — FEATURE — value 4 — effort M — risk med — category: continuity
  Why: the pack has post-compaction quizzes and lost-work receipts, but nothing that acts before the compaction. Transcript token counts are already read by `fm burden`.
  Done when: a fixture session at 85% of the context window gets a plan, open claims and the last proof written to a baton file, and a post-compaction replay finds it.

- **Raise a mid-flight overrun alarm at a fraction of the median cost** — FEATURE — value 4 — effort M — risk low — category: performance/budget
  Why: the pack has pre-start p90 refusal and `--stall-usd`. The gap between them is a task that starts cheap and drifts.
  Done when: a fixture task that has spent 40% of its kind's median with no red-to-green flip gets one "split or continue?" prompt, and a task that is on track gets none.

- **Keep a change-freeze calendar the guard honours** — SECURITY — value 3 — effort S — risk low — category: scheduling
  Why: assumption: users have release or holiday windows. Grants are time-bound, but nothing models "no pushes Friday after 3pm".
  Done when: with a freeze file listing today, `fm ship` refuses with the window's name and the override command, and does nothing outside the window.

- **Detect the user's recurring rituals and propose them as scheduled tasks** — FEATURE — value 3 — effort M — risk low — category: anticipation
  Why: the pack mines dated TODOs and n-grams, but not periodic closes such as a monthly dependency bump or a release cut.
  Done when: a fixture ledger with the same task title closed four times at roughly 30-day intervals produces one proposed recurring task, and the next due date is shown.

- **Prime session-start caches from the previous session's first reads** — PERFORMANCE — value 3 — effort M — risk low — category: performance
  Why: hook cold-start work is already benchmarked. Nothing uses what the last session turned out to need first.
  Done when: the bench shows first-tool-call latency dropping against a cold baseline on a recorded session, and the cache is dropped when HEAD changes.

- **Serve hash-keyed digests of big files in place of repeat full reads** — PERFORMANCE — value 3 — effort M — risk med — category: performance/privacy
  Why: the pack has dedupe of repeated reads, but not summaries of large files kept across sessions. Digests also mean less file text is sent out.
  Done when: a second read of an unchanged 5k-line file returns a ≤60-line digest plus the offer of a full read, and a changed file never gets a stale digest.

- **Learn per-path sensitivity from the user's own redactions and overrides** — SECURITY — value 3 — effort M — risk med — category: privacy
  Why: egress ledgers, scrubbers and canaries are listed, but nothing learns which paths the user treats as private. Assumption: users scrub the same kinds of file over and over.
  Done when: after the user marks two files in a directory as private, a third file in it is flagged "likely private" in the pack preview, and the label is reversible.

- **Wild: Hold an 02:00 "tomorrow rehearsal" that dry-runs the top queue item to a scratch worktree** — FEATURE — value 3 — effort L — risk med — category: anticipation
  Why: wild. The pack pre-drafts asks and pre-warms environments, but doesn't run the first real step. Success is a measurable "step one already green or already red" in the morning card.
  Done when: the morning card shows the rehearsal's first-step result for the top task, the main tree is untouched, and a discarded rehearsal leaves no files.

- **Wild: Publish a "surprise index" for each week: how much of what the user asked wasn't predictable from the ledger** — FEATURE — value 2 — effort M — risk low — category: measurement
  Why: wild. The pack plans predictors but no summary of where they fail. The weekly dashboard line would feed the next brainstorm's "Next question".
  Done when: `fm digest` prints the share of the week's asks that a recency-and-follow-up baseline missed, with the three biggest misses quoted.

- **Wild: Add a local sensitivity red team that guesses what private facts each new pack section reveals** — SECURITY — value 3 — effort L — risk med — category: privacy
  Why: wild. Pack previews show what is sent, but not what it implies once combined. A tool-less local child could judge each section against the user's privacy settings before it goes out.
  Done when: a fixture pack with a planted employer name and hostname in two separate sections gets a "combined disclosure" warning, and a clean pack gets none.

- **Wild: Brief the user once a month on upstream deprecations and end-of-life dates for their own dependencies, runtimes and CI actions** — FEATURE — value 3 — effort M — risk low — category: anticipation
  Why: wild-ish. Dependency watching and credential-expiry warnings exist. Dated runtime, Python or action EOLs are not mentioned in the pack.
  Done when: for a fixture manifest pinning an EOL runtime, the monthly brief names the runtime, the date and a filed task with the upgrade proof.

Next question: which of these anticipation actions would the user find intrusive enough to switch off, and does the ledger record any "dismissed without reading" signal to measure that?
Next question: which anticipation features need the user's calendar, other machines or upstream network access, and how would Foreman know before building them?
