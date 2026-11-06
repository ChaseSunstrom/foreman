# Brainstorm — lens: sci-fi: the 2030 harness that takes one line and works for weeks to a finished best-in-class result, worked back to what Python and Foreman can do today

- **Collect a grant manifest before day one** — FEATURE — value 5 — effort M — risk med — category: security
  Why: the spec says "never ask me anything mid-run" and "never grant yourself anything". Both hold only if every permission the plan needs is requested once, up front. A tool the plan will need, such as network, push or a toolchain install, is predicted from the contents list. The user approves or denies the batch. A denied permission turns its items into recorded "blocked: no grant" lines, not stalls.
  Done when: a goal whose plan includes a push item lists that grant in the manifest at open, and a run with the grant denied finishes every other item and ends with the blocked item named.

- **Cite precedent in every `fm decide`** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: weeks of autonomy means hundreds of decisions, and they drift. Before deciding, retrieve the 3 closest past decisions for this project, and record which were cited and whether the new answer agrees. A disagreement must say why. Assumption: the decide records are searchable by word overlap, as `fm clauses` is.
  Done when: a decide record carries a `precedent:` list, and a planted contradictory decision is flagged.

- **Schedule by critical path** — PERFORMANCE — value 4 — effort M — risk low — category: scheduling
  Why: `depends_on` and the topological order give a sequence but no weight. Weighting by effort estimates from past task durations lets parallel lanes take off-path items while the longest chain gets the first lane. This also gives the "time to finish" estimate a real basis.
  Done when: `fm queue` on a diamond-shaped graph with known durations puts the longest chain first, and prints the projected finish as chain length.

- **Pin a baseline at goal open and report deltas per task** — PERFORMANCE — value 4 — effort M — risk low — category: developer experience
  Why: hooks must stay under the bench_hooks gate and the suite has about 4400 tests. Record the test count, hook p95 and doc build state at open. At each task close, write the delta. A weeks-long goal's latency creep is then blamed on the task that caused it, not found at the end.
  Done when: a task that adds a 20 ms hook cost has that delta in its close record, and goal finish prints the net table.

- **Match review depth to risk** — SECURITY — value 4 — effort S — risk low — category: review
  Why: "one reviewer pass per task catches what its own tests didn't". A docs tweak and an edit to the Stop hook or the protected core don't need the same depth. Classify each task by the paths it touches. Protected-core and hook paths get two independent reviewers, and docs-only gets none beyond the tests.
  Done when: a task touching `fmhooks.py` cannot close with fewer than two review records, and a README-only task closes with zero.

- **Limit work in progress per goal** — FEATURE — value 3 — effort S — risk low — category: discipline
  Why: "everything finishes completely" is the user's rule. A cap of N open tasks per goal makes the agent finish a task before starting another, so a kill leaves one half-done item, not six. Assumption: parallel lanes are the exception and declare themselves.
  Done when: opening the (N+1)th task on a goal is refused with the list of open ones.

- **Compact the goal ledger into sealed epochs** — PERFORMANCE — value 4 — effort M — risk med — category: scale
  Why: a goal that lives for weeks outgrows the roughly 10 KB hook budget. Seal each week's events into an epoch summary that keeps the hash-chain anchor, and archive the raw events. Resume then reads only the current epoch plus the epoch summaries.
  Done when: a synthetic 5000-event goal re-injects under 10 KB, and `fm ledger verify` still passes across the epoch boundary.

- **Check each steer against sealed clauses** — SECURITY — value 4 — effort S — risk low — category: user value
  Why: the user steers mid-goal, for example "drop the site page", while MUST clauses demand one. Silent obedience breaks a MUST. Silent refusal ignores the user. Detect the conflict at UserPromptSubmit and write a decide record naming both. The user's later word wins, and the amendment is logged so finish does not fail on the dropped item.
  Done when: a steer contradicting a sealed MUST yields a conflict record and a logged amendment, and the finish audit passes against the amended list.

- **Publish decisions as an ADR page** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: the MUST list includes docs and a site page. Autonomous decisions are the one thing the user never saw being made. At goal close, render the decide records (question, options, choice, reason, precedent) as a "why it is this way" page under the site and as MASTER rows.
  Done when: closing a goal with 3 decide records emits an ADR page with 3 entries, and the site build links it.

- **Serve a read-only goal page to the phone, with a steer box** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: `fm serve` already exists, and the pack's surfaces include everywhere the user meets it. A token-gated page shows distance, the last 5 events and the stop-cause. A one-line box appends to an amend queue that is read at the next UserPromptSubmit and never executed directly. Assumption: LAN only, no outward action.
  Done when: a phone-sized fetch shows goal status, and a posted steer appears in the next session's context quoted as data.

- **Add a research librarian sub-agent** — FEATURE — value 3 — effort M — risk med — category: agents
  Why: with many lanes, each re-researches the same question. One specialist owns the goal's research notes and answers lane questions with citations to note lines. If it has no note it files a research task instead of guessing, and the lane waits on it.
  Done when: two lanes asking the same question cause one research task, and each answer cites a note line.

- **Rehearse the goal on a miniature clone (wild)** — FEATURE — value 4 — effort L — risk med — category: harness
  Why: assumption: weeks of budget should not be the first test of a goal's harness path. Generate a 5-file synthetic project with the same toolchain and run plan, one task, kill, resume and finish audit at toy scale. A harness fault (a missing runner, an oversized card) surfaces before real spend.
  Done when: a planted missing test-runner is reported by the rehearsal and not discovered on day 3 of a real run.

- **Export a finished goal as a replayable heirloom (wild)** — FEATURE — value 3 — effort L — risk med — category: sharing
  Why: assumption: a finished goal is the most expensive artifact Foreman makes. Bundle the contents list, ordering, decisions and ruleset hash, with the user's literals scrubbed. Another project imports it as a seed contents list, marked "from heirloom, ungrounded until checked".
  Done when: importing a bundle into an empty project creates a goal whose lines all carry the heirloom provenance tag, and none holds the exporter's paths.

- **Stage tomorrow's first hour before the usage window resets (wild)** — PERFORMANCE — value 3 — effort M — risk low — category: continuity
  Why: relaunch at the limit reset exists as an idea, but the relaunched session still spends its first minutes re-reading. A read-only prep pass builds the context packs for the next 3 tasks, with the files and criteria, so the first edit needs no orientation.
  Done when: a relaunch after a simulated limit starts its first edit within a set number of tool calls, measured against a cold start.

Next question: which of the ideas above change what a "stopped" session writes at its last second (grants, epochs, staged packs), and does one stop-cause schema cover all of them?
Next question: what does a goal cost in total tokens and calendar days on a repo the size of Foreman, and at what point does the user prefer plain Claude over a weeks-long plan?
