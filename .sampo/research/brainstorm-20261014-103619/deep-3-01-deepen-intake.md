# Brainstorm — lens: deepen: intake

- **Publish the intake queue as a live Artifact board** — FEATURE — value 5 — effort M — risk low — category: intake
  Why: the pack shows Artifact is unused (0 references), and T-0755 to T-0760 are six fragments of one rambling message that sit as separate S-tier captures the user can't see grouped. A private claude.ai page with the raw message, the folded milestone, and each derived task lets the user drag, merge or split items from a phone.
  Done when: `fm intake board` publishes a page listing every captured item with its verbatim source, and an ArtifactData edit (merge T-0756 into T-0757) is applied to the task store on the next `fm` call.

- **Read Artifact comments as intake messages** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: ArtifactComments sends comments to Claude. A comment like "this one first" or "drop that" becomes a steer without the user typing into the terminal. Assumption: comments arrive as a readable event the CLI side can hook.
  Done when: a comment on a board card reorders the queue and the change is logged with the comment text as provenance.

- **Fold bursts into one milestone with a single dependency-ordered plan** — FEATURE — value 5 — effort M — risk med — category: intake
  Why: T-0757 asks for exactly this ("put them into one task/milestone… reordering of operations"). Bursts such as T-0755 to T-0760 arrive within minutes. Group by time gap and topic overlap, then order by dependency (a model-choice task before one that uses it).
  Done when: replaying the T-0755 to T-0760 messages yields one milestone with six ordered steps, and the original six captures link to it as sources.

- **Route intake classification to a haiku subagent with a confidence score** — PERFORMANCE — value 4 — effort S — risk low — category: intake
  Why: T-0755 asks about spawning lower-model agents, and scout already runs on haiku. Classification, titling and fragment-gluing are cheap judgments. The Agent tool takes a per-call `model` and `effort`. Low confidence escalates to sonnet.
  Done when: `fm capture` on a vague message calls a haiku child, records model and confidence on the task, and the main session spends no tokens on titling. A bench shows hook latency is unchanged.

- **Keep a verbatim intake ledger that replays into any later plan** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: T-0756 stored a truncated first message ("also, the …"), so the original ask is lost. An append-only ledger of raw text, timestamp, session and pasted spans makes every later rewrite auditable and re-derivable.
  Done when: a truncated capture can be expanded to its full original text via `fm intake show T-0756`, and rewriting a title never changes the ledger entry.

- **Detect "step drift" at intake by matching new work to the active step** — FIX — value 4 — effort M — risk med — category: intake
  Why: T-0759 reports it starts steps without updating the step. A PreToolUse check that compares the edited paths to each step's declared scope can capture "unplanned work" as an item, or prompt a step update.
  Done when: an edit outside the active step's files triggers a one-line capture or step switch, and a test replays the T-0759 scenario.

- **Wake the idle queue from intake by scheduling a self-paced loop** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: T-0758 says "make sure it doesn't sit idle". ScheduleWakeup and Monitor exist, but fm bus relies on tmux send-keys. A capture that lands while the session is idle can arm a wakeup so the item starts without a nudge.
  Done when: a capture made during an idle session starts work within a configured interval, with no tmux dependency, and the wakeup is cancelled once the queue is empty.

- **Push a phone notification when intake needs one decision** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: PushNotification is unused and fm notify only runs a shell command. When a fold is ambiguous (merge or split?), ask once with a default and a timeout rather than blocking the queue.
  Done when: an ambiguous merge sends a push containing both options, and with no reply the default applies after the timeout and is marked as defaulted.

- **Generate acceptance criteria at intake from the user's earlier corrections** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: the "dropped" and "steered" entries show recurring corrections (don't duplicate built-ins, measure first, no handing commands). Attaching the relevant ones as criteria turns past steers into automatic checks on new tasks.
  Done when: a new FEATURE task carries 1 to 3 criteria cited from earlier steer records, each with a source link.

- **Wild: Let the user speak intake to a phone and have a cloud routine fold it** — FEATURE — value 3 — effort L — risk med — category: intake
  Why: RemoteTrigger and /schedule run cloud routines, and SendMessage reaches sessions on other machines. A dictated ramble on a phone becomes a folded milestone waiting on the desktop. Assumption: the user rambles by voice or mobile, as the six-fragment message suggests.
  Done when: a message sent from a remote session appears as a folded, titled milestone in the local queue before the user sits down.

- **Wild: Show "ghost tasks" before committing a ramble** — FEATURE — value 3 — effort M — risk low — category: intake
  Why: a dry-run preview of what a message would become (tasks, order, cost estimate) lets the user veto before the queue changes, and it avoids junk like T-0317 ("There's new bug feedback") and T-0756.
  Done when: `fm intake preview` prints the proposed tasks and order without writing anything, and confirming writes exactly that set.

- **Wild: Replay a week of intake to find where the folding misjudged** — FEATURE — value 3 — effort M — risk low — category: intake
  Why: the learning work already has eval cases and a holdout. Treat captured messages and the user's later merges, splits and drops as labelled data, so each change to the folding heuristic is scored on how often it would have matched what the user did.
  Done when: `fm intake eval` reports merge and split agreement against the stored history, and a heuristic change that lowers it fails the gate.

- **Wild: Let intake answer "did I already ask this?" across all history** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: the dropped items (Delta reads, Frontier 02) were rediscovered after measurement, and `recall` already exists. Checking a new capture against the ledger and dropped decisions surfaces "you dropped this on 10-xx because…" before work starts.
  Done when: capturing a message similar to a dropped task shows the earlier reason and links to it, and the user can override.
