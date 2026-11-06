# Brainstorm — lens: user value

- **Undo a landed task in one command** — FEATURE — value 5 — effort M — risk med — category: trust
  Why: assumption: the pack shows many ways to prove work and none for taking it back. A user who sees a bad result has to find the commits by hand. `fm task undo T-NNNN` would revert the task's own id-prefixed commits, reopen the ask and record why.
  Done when: after undoing a closed fixture task, the tree matches the pre-task commit, the task is open again with an "undone" note, and the unrelated commits after it are untouched.

- **Batch the user's decisions with timed safe defaults** — FEATURE — value 5 — effort M — risk med — category: attention
  Why: the steers say "never block on the user for process questions", and `fm ask` is still a blocking interrupt. One queue could hold every pending question with a recommended default and a deadline. At the deadline Foreman takes the default and records it as `fm decide --kind costly`.
  Done when: three pending asks appear in one `fm asks` list, and one unanswered ask auto-resolves to its default after its deadline with a ledger entry. An ask marked irreversible never auto-resolves.

- **Forecast duration and cost before starting, then score the forecast** — FEATURE — value 4 — effort M — risk low — category: expectations
  Why: bets already exist for outcomes (T-2610, T-2611), but nothing tells the user "this takes about 25 minutes and about $2". The data from closed tasks is already there.
  Done when: `fm next` shows a range per task, and after the close `fm outcomes` reports the share of tasks that landed inside their range.

- **Order the diff for a one-minute human review** — FEATURE — value 4 — effort M — risk low — category: review
  Why: assumption: the finish receipt proves the work but doesn't say which hunks a person should read. Ranking hunks by risk (touches the guard, auth, deletes, no covering test) with a plain sentence each would let the user skip the rest.
  Done when: `fm task finish` prints at most 7 ranked hunks. On a fixture with a planted risky hunk, that hunk ranks first.

- **Draft release notes and PR text from closed tasks** — FEATURE — value 4 — effort S — risk low — category: output
  Why: the repo has about 2600 tasks with ids, proofs and commit messages, but the user writes changelogs by hand. This is a cheap output that reuses the data and shows the work to other people.
  Done when: `fm notes --since <tag>` outputs grouped, user-readable lines. Each line links its task id, and no internal ledger vocabulary appears.

- **Learn queue order from what the user actually picks** — FEATURE — value 4 — effort M — risk low — category: ranking
  Why: the inbox has about 30 deferred "Later from…" items, and `fm next` ranks by Foreman's own rules. The user's real choices (started, skipped, deferred) are a signal Foreman didn't author, as the steers ask for.
  Done when: after 20 recorded picks, `fm next` order matches the user's picks more often than the old order does on held-out history, and `fm next --why` names the signal.

- **Park and resume cards for interrupted work** — FEATURE — value 3 — effort S — risk low — category: continuity
  Why: assumption: the user switches tasks mid-flight, and compaction or a crash loses the thread. A card holds the goal, the last green command, the next step and the open question.
  Done when: after killing a session mid-task, the next session start prints a card of 5 lines or fewer that names the next step correctly.

- **Show why a line exists** — FEATURE — value 3 — effort M — risk low — category: provenance
  Why: `fm why path:line` would walk from blame to the task, the original ask in the user's words and the proof run. The project is large (2117 files) and mostly written by agents, so the question "who decided this?" will keep coming up.
  Done when: on a fixture line, it prints the task id, the ask text and the proof command in under 2 seconds. A line with no task says "no record".

- **Spend idle usage on speculative drafts of the top queue items (wild)** — FEATURE — value 5 — effort L — risk med — category: initiative
  Why: wild; the request itself says usage is at 0%. Foreman could draft the top 3 queue tasks overnight in separate worktrees, each with its proof, unmerged. The user would accept a draft with one command or discard it for free.
  Done when: after a night tick, `fm next` shows "draft ready" on a task. `fm draft accept` lands it through the normal gate, and a discarded draft leaves no trace in main.

- **Run the same ask on two models and show a diff of diffs (wild)** — FEATURE — value 4 — effort L — risk med — category: choice
  Why: wild; `fm code` already runs on any model, and the duel exists as a bench. Turning the duel into a user-facing choice on hard asks lets the user compare two proven answers and pick.
  Done when: `fm try --models a,b "<ask>"` yields two worktrees, each with a receipt, and a side-by-side summary of where they differ. Only the chosen one is landed.

- **Dictate asks and hear the morning brief from your phone (wild)** — FEATURE — value 3 — effort L — risk med — category: voice
  Why: wild; the web UI exists but the user's own words are typed intake. A voice note could go through `fm intake` with the transcript kept verbatim. A spoken 30-second brief would cover overnight results and the decisions waiting.
  Done when: a posted audio file becomes a captured ask with its transcript, and the brief reads in under 30 seconds with every waiting decision named.

- **Teach a newcomer the repo from its task history** — FEATURE — value 3 — effort M — risk low — category: onboarding
  Why: the history records why things are the way they are (steers, decisions, reversals). `fm tour` could turn that into a reading order of ten tasks that explain the architecture, which beats a generic tutorial (T-0862, deferred).
  Done when: `fm tour` lists at most 10 tasks with a one-line reason each. Every listed task id exists, and the list is stable across two runs on the same HEAD.

- **Show the ask the diff actually answered** — FIX — value 4 — effort S — risk low — category: fidelity
  Why: assumption: scope drift is the most common unseen mismatch. At close, Foreman could restate the user's ask and list each changed file as "asked for", "needed for it" or "unexplained".
  Done when: on a fixture with one unrelated edit, the receipt marks that file "unexplained" and the finish needs one acknowledgement.

Next question: which of Foreman's outputs has the user never acted on in the last 30 days, and would they miss it if it disappeared?
Next question: what would make the user hand Foreman an ask they currently do themselves, and what does it cost them to check the result?
