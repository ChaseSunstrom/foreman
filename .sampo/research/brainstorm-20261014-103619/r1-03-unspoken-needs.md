# Brainstorm — lens: unspoken needs

- **Replace tmux send-keys wakeups with ScheduleWakeup and SendMessage** — FIX — value 5 — effort M — risk med — category: idle/orchestration
  Why: T-0758 ("make sure it doesn't sit idle like it is"), and `fm bus` types into tmux panes, which breaks when the pane is busy or gone. Self-paced wakeups (ScheduleWakeup) and typed delivery (SendMessage/ListAgents) are native. Assumption: both are callable from a session Foreman controls.
  Done when: a session with a queued task and no user input resumes by itself after a forced idle, with no tmux involved, and the ledger shows the wake source.

- **Diff the tool list against Foreman's usage at every session start** — FEATURE — value 4 — effort S — risk low — category: CC integration
  Why: The user keeps asking to "integrate better with new CC features". The pack's "0 references" list was built by hand on 2026-10-14. Hash the tool and hook names the session offers, compare with a committed `used.json`, and capture one task per newly seen capability. The need behind the request is never having to ask again.
  Done when: adding a fake tool name to the session's tool list produces exactly one captured task, and a second session produces none.

- **Block step drift in PostToolUse** — FIX — value 4 — effort M — risk med — category: discipline
  Why: T-0759 ("starts working on different steps without updating the step"). Map each edit's file to the plan step whose footprint contains it. If it is a different step than the current one, advance the step or warn with the step id.
  Done when: a test editing a step-2 file while step 1 is current yields an auto-advance or a warning naming both steps, and the step pointer always matches evidence.

- **Route model and effort per Agent call from a learned table** — FEATURE — value 5 — effort M — risk low — category: orchestration/cost
  Why: T-0755 asks for lower-model agents. The Agent tool now takes per-call `model` and `effort`, and today only S-tier lanes pass "sonnet". Key a table on (step type, tier), seeded haiku for scouting, sonnet for S, and opus at high effort for L review. Update it from gate pass rates already in the ledger. Assumption: ledger results carry enough lane and model detail.
  Done when: `fm lane` logs the model and effort it chose and why, and a bench replay shows lower cost at an equal pass rate.

- **Render reviewer output through ReportFindings** — FEATURE — value 3 — effort S — risk low — category: review UX
  Why: Reviewers return markdown that Foreman parses. Typed findings drop the parsing, show severity in the host UI, and give T-0034's audit lenses a ready findings file shape.
  Done when: a reviewer run produces host-rendered findings with file and line, and `fm` reads the same objects into the ledger without a regex.

- **Publish a live cockpit Artifact the user can comment on** — FEATURE — value 5 — effort L — risk med — category: UI/phone
  Why: Frontier 11 asks for a cockpit that "sees, steers and rewinds". Artifact gives a private page on claude.ai, so it works from a phone. ArtifactData holds the plan tree, fleet and asks. ArtifactComments become captured tasks, and a button answers a pending `fm ask`. Assumption: the CLI side can write ArtifactData while unattended.
  Done when: a comment typed on the page appears as a captured T-id within a minute, and an ask answered on the page unblocks the session.

- **Stream night runs with Monitor and wake on patterns** — PERFORMANCE — value 4 — effort M — risk low — category: unattended
  Why: Night and drive runs poll or wait on gates. Monitor streams a background command's output as events, so a gate failure or a stalled log line wakes the session immediately, and silence costs zero tokens.
  Done when: a failing test line in a background gate triggers a reaction within 10 seconds, with no polling calls in the transcript.

- **Send a deadline-defaulted push digest** — FEATURE — value 4 — effort S — risk low — category: user attention
  Why: The user never wants to be handed commands, and `fm notify` only runs a shell command. PushNotification reaches the phone. Send one message per block saying what's needed and what Foreman will do by default if there's no reply.
  Done when: a blocked task sends one push naming the default action and its deadline, and silence past the deadline executes the default and records it.

- **Run nightly bench and canary as cloud routines** — FEATURE — value 3 — effort M — risk med — category: schedule
  Why: Evals, bench holdout and flywheel jobs run only when the laptop is on. RemoteTrigger and /schedule run on a cron in the cloud, with isolation "remote" for lanes. Assumption: the repo is reachable from the routine, and the redactor runs before upload (see the privacy lens).
  Done when: a scheduled routine writes a bench scorecard to the ledger with the machine off.

- **Use built-in /code-review levels as the reviewer lane** — CLEAN — value 3 — effort S — risk low — category: do-less
  Why: Foreman keeps its own reviewers, `/simplify` and `/security-review` already exist, and the user dropped features that duplicated built-ins (delta reads). Map tier to level: S low, M medium, L high or ultra. Keep Foreman's reviewers only for the lenses nothing built-in covers.
  Done when: a bench comparison shows equal catch rates, and at least one in-house reviewer is deleted or demoted.

- **Wild: Try a risky task in a worktree with a keep/discard verdict** — FEATURE — value 3 — effort M — risk med — category: safety
  Why: assumption: EnterWorktree/ExitWorktree lets the main thread try a change without a lane. The task ends with an explicit KEEP or DISCARD and the evidence behind it, so nothing half-done reaches the tree.
  Done when: a DISCARD leaves the main tree byte-identical, and a KEEP lands one commit.

- **Wild: Hand a session between local, remote and a second machine without losing the step** — FEATURE — value 4 — effort L — risk high — category: devices
  Why: Combine ListAgents/SendMessage with the resume-at-exact-step machinery. When the laptop closes, the task continues in a cloud session with its plan and step pointer, and returns with a diff.
  Done when: closing the lid mid-step results in the same step completing remotely, with one ledger lineage.

- **Wild: Give Foreman an idle-cost meter that sleeps to the cache TTL** — PERFORMANCE — value 3 — effort S — risk low — category: tokens
  Why: Self-paced wakeups can be timed. Waking just inside the prompt-cache window keeps context warm, and sleeping through long gates avoids paying for empty turns.
  Done when: a 20-minute gate wait shows no more than one wake per cache window and no lost cache read.

- **Wild: Let the user answer from the Artifact by drawing on an approval deck** — DELIGHT — value 2 — effort M — risk low — category: delight
  Why: Combine the cockpit and the push digest. Pending asks show as swipeable cards (approve, default, skip) and answers write back to ArtifactData, so away-from-keyboard decisions take seconds.
  Done when: three pending asks are cleared from a phone in under 30 seconds.
