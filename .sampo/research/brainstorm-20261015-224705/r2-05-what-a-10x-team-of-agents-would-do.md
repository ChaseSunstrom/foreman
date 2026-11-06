# Brainstorm — lens: what a 10x team of agents would do

- **Hold back hidden acceptance tests from the builder** — FEATURE — value 5 — effort M — risk med — category: verification
  Why: assumption: a builder that writes its own tests can overfit them. "Pre-register a task's success test" is planned, but nothing keeps the builder from seeing it. Separation of duties is how a 10x team stops "tests pass" from meaning "tests I wrote pass".
  Done when: `fm task plan` for a FEATURE spawns a spec agent that never sees the diff and writes tests into `.foreman/holdout/T-xxxx` outside the worktree. Close runs them. A fixture builder that hard-codes the visible test fails the holdout and the close prints "visible green, holdout red".

- **Sweep queued plans when a task closes** — FEATURE — value 4 — effort S — risk low — category: plan integrity
  Why: the queue holds 30+ deferred tasks whose briefs were written against an older tree. "Verify the ground" is checked at start; nothing re-checks open plans after a neighbour lands.
  Done when: closing a task diffs its changed files and symbols against every open task's file and symbol mentions. Affected tasks get a `stale-since: T-xxxx` marker, and `fm next` shows the marker and the changed lines.

- **Predict each task's touch-set from similar closed tasks** — PERFORMANCE — value 4 — effort M — risk low — category: tokens
  Why: the ledger records which files past builders read and edited per task. Briefs still send builders exploring, and re-reading is a recurring cost.
  Done when: `fm task plan` prints "likely files" ranked by overlap with the most similar closed tasks (title tokens plus map tags). On a replay of the last 50 closed tasks, the top 5 cover at least 60% of the files actually edited, and the figure is reported.

- **Map where agents get lost in the repo itself** — FEATURE — value 4 — effort M — risk low — category: legibility
  Why: assumption: some directories cause repeated re-reads, wrong-file edits and stalls. The planned "fault lines" idea covers Foreman's failures, not the repo's. The same data could produce CLEAN tasks like adding a test, splitting a file or naming a thing.
  Done when: `fm friction map` ranks directories by agent confusion (re-reads per edit, edits reverted, stalls) from the ledger. The top 3 each get a proposed CLEAN task with the evidence line, and the pane shows the ranking in More.

- **Track which lines a human has ever seen** — SECURITY — value 4 — effort M — risk low — category: trust
  Why: agents write most of the code. The planned "rank morning diff review by risk" covers one diff, not what has never been read at all. The need is knowing what in HEAD no human has looked at.
  Done when: the pane's diff view, `fm review` and any user-run `git show` mark hunks as seen in a sidecar. `fm unseen` lists the riskiest unseen regions (by blast radius and guard-adjacent paths) and shows % of HEAD seen.

- **Run an incident commander when main goes red** — FEATURE — value 4 — effort M — risk med — category: fleet
  Why: bisect and the merge train are planned separately. Nothing composes them into a protocol for the moment a gate goes red after a merge.
  Done when: a red gate on main freezes the merge train and runs bisect. It then races a revert lane against a fix lane in throwaway worktrees and writes a timeline file. The first lane to go green is offered as one-key apply, with the loser discarded.

- **Detect approval fatigue and respond** — SECURITY — value 4 — effort S — risk low — category: asks
  Why: assumption: bypass-mode users approve in bursts without reading. The planned ledgers count interventions but never the quality of the human's attention.
  Done when: `fm ask` logs answer latency and streak length. After 8 answers each under 1.5 s, the next asks are batched into one digest, and the doctor reports a fatigue incident count.

- **Post claims on a lane bulletin at symbol level** — FEATURE — value 3 — effort M — risk med — category: concurrency
  Why: leases are per task or worktree, and lane merge conflicts are only predicted at plan time. Two live builders can still edit the same function.
  Done when: a builder's first edit to a function appends a claim to `.foreman/claims`. A second lane's PreToolUse on that symbol gets "T-xxxx owns this, message it or take a different seam". A test with two fake lanes shows the second one redirected.

- **Wild: Plant canary asks to test whether the human reads** — SECURITY — value 3 — effort S — risk med — category: trust (wild)
  Why: approval fatigue is invisible until it hurts. A harmless ask with a visibly wrong default ("delete the README? default: yes") measures real attention. The default is always the safe no-op, and the canary is revealed after the answer.
  Done when: `fm ask` injects at most one canary a week, and its answer is logged as `attentive` or `rubber-stamp`. A rubber-stamp result raises the batching threshold from the fatigue idea above.

- **Wild: Diff two racing builders' behaviour to find spec ambiguity** — FEATURE — value 4 — effort L — risk med — category: planning (wild)
  Why: the "race a second builder" idea only picks a winner. Where two independent builders disagree on generated inputs, the brief itself was ambiguous.
  Done when: for a task marked ambiguous, two lanes build independently. A differ runs both on 20 generated inputs and lists the disagreeing cases as questions in `fm ask`, so the brief is fixed before one is picked.

- **Wild: Relay each step through fresh short-lived agents** — FEATURE — value 4 — effort M — risk med — category: orchestration (wild)
  Why: compaction, resume cost and cold-cache drift all come from long sessions. Planned items manage that bloat, but none removes it by design. Each step would start fresh with a typed baton, so resume is the default path.
  Done when: `fm relay T-xxxx` runs plan steps as separate `claude -p` calls. Each gets only the brief, a baton JSON (decisions, files, failing proof) and its own step. It writes a new baton and the final summary matches a normal close. A bench compares tokens and first-pass rate on 5 closed tasks.

- **Wild: Draft an upstream issue when a dependency blocks a task** — FEATURE — value 3 — effort M — risk low — category: ecosystem (wild)
  Why: blocked tasks such as T-0325 and T-0337 stall on outside software. A real team would file upstream. Drafting stays local, and nothing is sent without the user's confirmation.
  Done when: marking a task blocked with `--upstream` makes a lane build a minimal repro in a scratch directory and write `issue.md` with version info. `fm ask` offers to open it, and nothing leaves the machine before an answer.

- **Resolve contradictions between queued tasks in a standing-orders file** — FIX — value 3 — effort S — risk low — category: backlog
  Why: the queue and the user's steers conflict at times, for example "one panel" against "multiple panes", and the older item silently wins. Planned contradiction detection covers steers, not queue items.
  Done when: `fm tidy` flags pairs of open tasks whose acceptance criteria conflict, with both ids and a keep/merge/drop question. The test fixture holds a seeded conflicting pair that the check finds.
