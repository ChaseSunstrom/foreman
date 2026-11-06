# Brainstorm — lens: simplicity

- **Shelve catalogue clusters as one file, not thirteen tasks** — CLEAN — value 3 — effort S — risk low — category: queue
  Why: T-0787 to T-0799 are 13 "Later from T-0760" tasks, each a full queue row with a cluster of ideas behind it. The drive loop walks the queue, so deferred clusters add noise and risk being driven by accident.
  Done when: `fm ideas` keeps deferred clusters in a single `shelf` file with a one-line `fm shelf promote <cluster>` to make a task, and the queue shows zero "Later from" rows after migration.

- **Keep task titles short and move CONTEXT to a linked field** — FIX — value 3 — effort S — risk low — category: intake
  Why: the user's own captures show titles that carry the whole brief ("FIX!: One-off headless claude -p sessions … CONTEXT: T-0760 catalogue, cluster …"). The queue list truncates them mid-sentence, so rows are unreadable.
  Done when: capture splits any request over 12 words into a title and a context field, and `fm task list` never shows a row containing "CONTEXT:".

- **Reject verify commands that read Foreman's own queue** — FIX — value 3 — effort S — risk low — category: verification
  Why: a dropped task's check grepped the queue for T-0775, which stopped matching once the task finished, so the task had to be recreated with a durable check. Round 1 already refuses unrunnable verify commands at plan time; this is the same lint with one more rule.
  Done when: `fm task plan` refuses a verify command that greps queue or state files for a task id, and the refusal says to check the artifact instead.

- **Let toggles flip themselves from evidence and tell the user once** — FEATURE — value 4 — effort M — risk med — category: settings
  Why: compact output measured about 1.04M tokens saved per 30 days but stays off until the user says yes, and nobody has acted on it. Each "ask the user to opt in" is a decision the user didn't want to make ("smarter, faster").
  Done when: an opt-in feature with a measured saving above a threshold turns itself on after a shadow period, prints one line saying so with the `fm off <name>` undo, and never asks again. Compact output is the first user.

- **Merge wake, push and title into one attention emitter** — CLEAN — value 3 — effort M — risk med — category: attention
  Why: round 1 added the mail monitor, the Stop-hook PushNotification ask and sessionTitle, alongside the existing drive nudges and the tmux wake. They are separate code paths that each decide when the user is needed.
  Done when: one `emit(kind, payload)` function in the lib is the only caller of those channels, and a test lists every call site that bypasses it as empty.

- **Auto-demote close warnings the user never acts on** — FEATURE — value 3 — effort S — risk low — category: close-out
  Why: round 1 fixed two false-positive close warnings (tier-drift size counting non-diff lines, empty `.claude/worktrees/` reported as left behind). Warnings that turn out to be noise stay in the output until someone files a task.
  Done when: each warning kind keeps a "shown / followed by an edit" count in the ledger, and a kind shown 10 times with no follow-up drops to a ledger-only line, with `fm doctor` listing what was demoted.

- **Lower the Python floor so the installer never installs Python** — CLEAN — value 3 — effort M — risk med — category: install
  Why: the README requires 3.12.7 or newer, and the installer carries a Homebrew and `uv` branch to get it, which is the largest piece of install logic. Assumption: the code uses few 3.12-only features; this needs a measurement first.
  Done when: a scan lists the 3.12-only constructs in `plugin/lib`, and either the suite passes on 3.9 or the floor change is rejected with the list as the reason.

- **Replace "known gaps" prose with a doctor probe** — FEATURE — value 3 — effort S — risk low — category: self-check
  Why: the round 1 summary lists gaps in prose: monitor arming unverified in live interactive sessions, compact output off, nobody has ticked the board. Prose gaps are never re-checked.
  Done when: `fm doctor` reports "mail monitor armed: yes/no/unknown" from a fresh heartbeat file, and the gap drops out of the notes once it reads yes.

- **Prune the brainstorm pack: archive unseen ideas and print clusters, not lines** — PERFORMANCE — value 4 — effort S — risk low — category: tokens
  Why: this pack is dominated by thousands of "ideas so far" lines, and "The user's own words" appears twice. Every child pays for that and it adds no signal.
  Done when: the pack builder dedupes repeated sections, collapses ideas to cluster counts plus the last two rounds' titles, and a test caps the pack at a fixed size.

- **Derive task status from facts instead of storing it** — CLEAN — value 4 — effort L — risk med — category: state (wild)
  Why: the queue carries captured, planned, active, deferred and blocked as stored fields, and T-0759 shows the stored step pointer drifting from the work. wild: status becomes a pure function of whether the task has a plan, a start point, evidence and a blocker.
  Done when: no status field is written, `fm task list` renders the same states from facts, and a round-trip test over existing state shows no task changes state.

- **End every recursive round by deleting the least-used round-1 feature** — FEATURE — value 4 — effort M — risk low — category: recursion (wild)
  Why: the user steered that "recursively improve" means repeating review and brainstorm, and each round only adds. wild: a round closes only with a prune proposal naming the previous round's feature with the lowest measured use.
  Done when: closing a round prints the lowest-use feature from the last round with its usage count and a one-key delete task, and the round stays open until that is accepted or declined.

- **Make `fm` answer "what is Foreman doing this turn" in one line** — FEATURE — value 3 — effort S — risk low — category: legibility (wild)
  Why: round 1 added hooks that rewrite Bash output, retitle sessions and push to the phone. Nothing tells the user which of them fired on the current turn. wild: a single line such as `compact-output ✓ title ✓ push –`.
  Done when: the band or `fm now` prints one line listing only the round-1 mechanisms that acted in the last turn, and it is empty on a turn where none did.
