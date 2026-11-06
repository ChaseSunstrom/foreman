# Brainstorm — lens: user value

- **Let the user force a re-think mid-task with `fm doubt`** — FEATURE — value 5 — effort M — risk low — category: control
  Why: assumption: the user often senses a build going wrong before any gate does, and no verb lets them say so. Today a doubt becomes a chat correction that is only handled as a steer.
  Done when: `fm doubt` on a task with a diff re-runs readings and options against the current diff, prints "keep / switch to B / ask", and records the call in the ledger.

- **Break one ask into separately tiered items before planning** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: gen-0 #2 says an S task shouldn't pay an L task's cost, but a mixed message currently gets one tier. The user's own asks often bundle a trivial fix with a large change. Assumption: tier is assigned per task, not per clause.
  Done when: a message holding a typo fix and a new verb yields two tasks, S with no readings and L with the full path, and a test asserts both tiers.

- **Carry assumptions across tasks with an expiry date** — FEATURE — value 4 — effort M — risk low — category: memory
  Why: the same facts get re-derived per plan (Python version, setuptools present, no `claude` on PATH). T-2529 failed on exactly such an assumed fact. Assumption: plans list assumptions only per task today.
  Done when: a plan lists live assumptions from earlier tasks, each re-probed if its age or a changed file voids it, and a stale one is shown as "re-checked: changed".

- **Show "what exhaustive thinking does for you" generated from the filled cells** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: the standing rule requires proof before presentation. A README or site paragraph written by hand will drift from the 58 cells.
  Done when: the paragraph is rendered from cells that each cite an exam line or an outcome, and the sweep goes red if it names a cell that is empty or unmeasured.

- **Report minutes lost to a replaced first approach, before and after the gate** — FEATURE — value 4 — effort M — risk med — category: outcomes
  Why: the user keeps asking for measured value (outcomes, Brier, subtract-by-evidence), yet nothing prices the failure that deliberation exists to prevent. Assumption: the ledger holds enough reverted-first-attempt tasks to show a rate.
  Done when: `fm outcomes --thinking` prints the share of closed tasks whose first diff was reverted or replaced, split by deliberation depth, with n shown.

- **Show only the cells that changed since the user last looked** — FEATURE — value 3 — effort S — risk low — category: review
  Why: 58 cells filled across lanes is too many to re-read. T-1344 already asks for a "changed-since" line elsewhere.
  Done when: the checklist page and `fm status` list only cells added or edited since the last view, each with its evidence link, and a viewed cell stops appearing.

- **Learn a regret-free fast lane from the user's own history** — FEATURE — value 4 — effort M — risk med — category: tiering
  Why: the user never wants ceremony on rename, version bump or typo tasks. Closed tasks that were never reopened or reverted are the evidence.
  Done when: an ask pattern with at least 10 closed, unreopened S tasks skips readings and options, logs the skip, and any later reopen removes the pattern from the lane.

- **Give a plan waiver with receipts: `fm trust-me 1h <path>`** — FEATURE — value 3 — effort S — risk med — category: control
  Why: assumption: the user will sometimes want depth off for a stretch of work. A release valve for the guard exists, but plan depth has none, so they would have to fight the gate or abandon it.
  Done when: the waiver is scoped, expiring and never covers one-way doors, and `fm outcomes` later reports whether waived tasks were reopened more often.

- **Wild: Let the user ask "what if we'd picked B?" after close** — FEATURE — value 3 — effort L — risk med — category: counterfactual
  Why: wild. Races pick a winner, but the user never sees the road not taken unless it won. Assumption: the runner-up is stored with its brief.
  Done when: `fm what-if T-xxxx B` builds the runner-up in a scratch lane and prints diff size, test result and cost beside the shipped version, touching nothing on main.

- **Wild: Notice when the user has stopped reading plans** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: wild. If the user accepts 20 plans in a row with no edit and no scroll, the ceremony may be wasted, or the plans may be unreadable. Foreman never asks which.
  Done when: after 20 untouched accepts, one question offers "shorter plans / keep as is", and the answer is recorded as a decision.

- **Wild: Give the user a daily budget of deep-think coins** — FEATURE — value 2 — effort M — risk med — category: cost
  Why: wild. Depth competes with usage-limit headroom, and today it spends invisibly. A visible coin makes the trade the user's, not Foreman's.
  Done when: each L task shows its coin price at plan time, the balance shows in `fm status`, and an empty balance degrades depth to a named floor rather than stopping work.

Answering the earlier question on steers that assume a live session: the standing rules that say "ask once with `fm ask`" and "state the plan for approval" both assume someone present. The unattended default per ask class should live in one file, and `fm doubt` and the waiver above should read it.

Next question: Which of the 58 empty cells would the user, shown only its one-line symptom, call "never happens to me", and does the ledger agree?
Next question: When the user overrides or skips deliberation, how often does the task come back, and has anything recorded that rate?
