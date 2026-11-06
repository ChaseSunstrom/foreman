# Brainstorm — lens: unspoken needs

- **Diff the machine's facts on the first red** — FIX — value 4 — effort S — risk low — category: reliability
  Why: PATH lacking `~/.local/bin`, the native `claude` install, and tests reaching the paid binary were all "environment differs from yesterday" failures. The planned env matrix tests combinations but doesn't record what changed.
  Done when: SessionStart stores a hash of PATH, binary locations and versions, and a failing gate prints "changed since last green: PATH lost ~/.local/bin" from a test that alters PATH.

- **Detect contradictory steers and record which wins** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: the pane steers swing between "drop the small bars" and "every More line gets a bar", and between "liked the old plot chart" and "one bigger graph". Each swing costs a reload-and-complain cycle. Assumption: steers are tagged by area (pane, chat, etc.).
  Done when: logging a steer that conflicts with an earlier one in the same area prompts "this replaces T-xxxx's rule X?", and the answer is stored with precedence.

- **Approve a look once, then lock it as a golden** — FEATURE — value 4 — effort M — risk med — category: ui
  Why: the user repeatedly says "still cluttered", "graphs too big", "panel must be filled". The planned layout sweep checks invariants, not what the user actually approved.
  Done when: `fm ui approve` stores pane frames at 5 sizes, and a later change that alters a frame fails the gate unless re-approved with a reason.

- **Alarm on spend that no Foreman call explains** — SECURITY — value 4 — effort M — risk low — category: cost
  Why: T-0990 let test runs reach the paid binary, and the harness session got driven by the Stop hook. Daily caps don't say which process spent the money. Assumption: Claude usage logs or per-call stats can be read locally.
  Done when: a test that spawns `claude -p` outside Foreman's wrapper makes `fm doctor` and the digest report "unattributed call, origin pid/cwd".

- **Regenerate README pictures in CI and fail when stale** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: the user asked to re-record the demo and refresh the pictures after each UI change. Planned "README claims into checks" covers text, not images.
  Done when: bumping the pane version without refreshing the `demo/*.svg` frames fails `fm doctor`, and `fm docs shots` rebuilds them from the harness.

- **Make deferred items start-ready** — FEATURE — value 4 — effort M — risk low — category: backlog
  Why: about 30 "Later from T-07xx/08xx" items sit deferred. The planned triage decides drop/do/ask but leaves "do" items cold.
  Done when: `fm tidy --prep T-0788` writes draft acceptance criteria, a file list and a failing test stub into the task, and the item then starts without a planning stage.

- **Search neighbouring local repos for how a similar error was fixed** — FEATURE — value 3 — effort M — risk med — category: learning
  Why: the user wants fixes to travel across "any project". Git-history seeding only mines the current repo. Assumption: the user has sibling repos under one root and opts in with a path list.
  Done when: an error fingerprint with no known fix surfaces a commit hit from a listed sibling repo, labelled "unverified, from <repo>@sha".

- **Forge a tool from a repeated tool-call sequence** — FEATURE — value 4 — effort M — risk med — category: autonomy — wild
  Why: steer: "the user shouldn't need to ask for any of it". Planned routines come from repeated *asks*; this mines the ledger for repeated *tool sequences* (e.g. the same four Bash steps in a harness run).
  Done when: after a sequence recurs in 3 sessions, `fm forge` proposes a script plus a test and a skill stub, and the user accepts it with one key.

- **Hold a plan auction before big builds** — FEATURE — value 3 — effort M — risk med — category: orchestration — wild
  Why: L tasks risk wrong scope and merge conflicts. Three cheap planners each bid files touched, steps and risk, and the orchestrator picks the smallest-blast-radius plan that satisfies the criteria. Planned speculative builders race code; this races plans, which is cheaper.
  Done when: for an L task `fm plan --auction 3` stores the bids and the winner's reason, and the chosen plan touches ≤ the median file count.

- **Hill-climb Foreman's own skill prompts against captured cases** — FEATURE — value 4 — effort L — risk high — category: self-improvement — wild
  Why: the user's core complaint is "why have you not really improved". T-0035 eval capture is deferred; once it lands, mutate one skill's text, score it on stored cases with a cheap model, and keep only wins with a rollback tag. Assumption: T-0035 ships first.
  Done when: `fm improve prompt <skill>` runs N mutations offline, reports a before/after pass rate, and applies none without `--accept`.

- **Predict next week's asks and score the guess** — FEATURE — value 3 — effort S — risk low — category: foresight — wild
  Why: the brief asks for predictive work and live telemetry of intent. A weekly cheap-model forecast of the user's top 3 themes (from the asks ledger) is graded against what they actually asked, so the digest can pre-stage work that is hit more often than chance.
  Done when: the digest shows "predicted 3, hit 2" for last week, and stores a hit-rate series.

- **Generate synthetic worlds to test every surface** — CLEAN — value 3 — effort M — risk low — category: developer experience
  Why: the pane has been tuned by eyeball on the author's real state. Layout fuzz varies size, not data. Fixture worlds (empty, 500 tasks, mid-crash worktrees, corrupt ledger, long titles) feed the pane, digest and resume.
  Done when: `fm world <name>` builds an isolated state dir, and the pane test runs over all worlds with no overflow or exception.
