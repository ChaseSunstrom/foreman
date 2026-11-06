# Brainstorm — lens: user value

- **Learn the user's taste from their own edits to Foreman's hunks** — FEATURE — value 5 — effort M — risk low — category: learning
  Why: Lessons exist (T-0217) and "watch the human's saves" is proposed, but nothing learns from what the user changes after a close. That is the clearest signal of what they actually wanted. Assumption: commits carry a Foreman trailer or task id, so authorship is attributable.
  Done when: in a fixture, Foreman commits a hunk, a human edit rewrites it, and the next `fm lessons --proposed` lists a candidate lesson quoting the before/after, with nothing auto-applied.

- **Ship the day as a stacked PR series** — FEATURE — value 4 — effort M — risk med — category: delivery
  Why: Round 5 added review-risk ranking via `fm tour`, and PR-description generation is proposed. Neither makes the day's output reviewable in the forge, which is where the user will actually review it (including from a phone). Assumption: the user has a GitHub remote.
  Done when: `fm pr-stack` on three closed tasks creates three chained branches, each with its evidence in the PR body, and dry-run is the default.

- **Rank the repo's own friction in minutes per week** — FEATURE — value 4 — effort M — risk low — category: payoff
  Why: Foreman already times gates and knows flaky reruns and which checks are repeats. It never tells the user what the repo costs them, such as the 4-minute suite run 30 times a week. Assumption: gate wall-clock is logged per run.
  Done when: `fm friction --repo` prints the top 3 time sinks with minutes per week, and `--queue` files the top one as a PERF task.

- **Name the red: classify every failing gate by cause** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: Flaky reruns and stale `.pyc` handling are treated as separate fixes. A failure is really one of code, flake, environment (service down, toolchain changed, disk full) or stale cache. Retries should be spent only on the first kind.
  Done when: a fixture with a stopped dependency produces "environment: <thing> unreachable", with no code-fix attempt and no retry loop.

- **Close RESEARCH tasks with a decision memo, not a ledger line** — FEATURE — value 4 — effort S — risk low — category: close-out
  Why: T-0843 (active) and T-0336 are RESEARCH tasks, and a brainstorm round is one too. Their outputs are long idea piles. The user needs options, a recommendation, what would change it, and a one-line "adopt?" that creates the tasks.
  Done when: closing a RESEARCH task writes a memo of at most 25 lines, and answering yes to its adopt line creates the tasks.

- **Teach a routine by demonstration (`fm record`)** — FEATURE — value 4 — effort M — risk med — category: capture
  Why: Learned routines and runbooks are proposed only from agent history. A human's one-time manual sequence (release steps, local setup) is the highest-trust source. Assumption: shell history can be captured only while recording, and the guard screens the result.
  Done when: record, stop, then `fm run <name>` replays the commands in a scratch lane with a generated verify and a guard review.

- **Promote lessons that recur across the user's projects** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: `fm projects` already spans projects, but lessons stay per-repo. The same correction in three repos ("don't mock the DB") should become one global lesson with its provenance.
  Done when: a lesson matching in 3 project ledgers is offered once as global, and declining it is remembered.

- **Show an interrupt-safe light on the band** — FEATURE — value 3 — effort S — risk low — category: steering
  Why: The user is told to type steers mid-run, but can't tell whether Foreman is at a step boundary (safe) or mid-edit (a steer may land on half-written state). Prior ideas cover step drift, not when steering is safe.
  Done when: the band shows safe or busy, derived from the last tool event, and a test covers both states.

- **Salvage on drop** — FEATURE — value 3 — effort S — risk low — category: queue hygiene
  Why: Dropped tasks appear repeatedly in the user's words, and snapshots exist only for risky commands. Dropping with partial work should keep a ref and a 3-line "learned, remaining" note, so reopening is cheap.
  Done when: `fm task drop` on a dirty lane leaves a refs/foreman ref plus a note, and `reopen` restores both.

- **Let the human claim a region (`fm mine <path>`)** — FEATURE — value 3 — effort S — risk low — category: coexistence
  Why: Snapshots protect the user's uncommitted work after the fact. A claim stops collisions earlier: Foreman lanes around the claimed path, parks conflicting steps, and auto-releases on the user's next commit.
  Done when: an edit by Foreman inside a claimed path is refused with a pointer to the claim, and the claim expires after a commit.

- **Weekly retro letter on how the collaboration is going** — FEATURE — wild — value 3 — effort S — risk low — category: delight
  Why: The user's steers and drops are rich data. A short letter would say things like "tasks with acceptance criteria closed 2x faster; 4 vague requests cost you 40 minutes". That is prompt coaching framed as a retrospective, which the existing "coach shorter forms" idea doesn't cover.
  Done when: `fm retro` prints 5 lines at most, each citing task ids, and refuses to run on less than a week of data.

- **Offer a questions-only rubber-duck mode** — FEATURE — wild — value 2 — effort S — risk low — category: thinking
  Why: Assumption: the user's long, stream-of-thought requests mean they sometimes need to think, not delegate. Foreman asks clarifying questions only, edits nothing, and ends by offering to capture the result as a task.
  Done when: in `fm duck` mode the guard blocks all writes, and exiting offers one captured task.

- **Run a ledger exam: a cold agent quizzes itself on the project** — TYPE FEATURE — wild — value 3 — effort M — risk low — category: proof of memory
  Why: A cold child answers 10 questions about the project ("why is X like this?") using only the ledger, lessons and `fm why`. It scores itself against the code, and the failures become missing-lesson tasks.
  Done when: `fm exam` prints a score and files a task per unanswered question, with no network or cloud access.
