# Brainstorm — lens: simplicity

- **Retire the foreman-ui mod for an Artifact cockpit** — CLEAN — value 4 — effort L — risk med — category: ui
  Why: the mod patches a host bundle and is a standing maintenance cost (T-0418 is blocked on updating it, T-0166 is deferred, and the band/pane live in register.tsx). An Artifact is a private page with ArtifactData (a shared db), live data and "ask Claude", so the plan tree, fleet and queue (Frontier 11) can be one page the CLI writes to. Assumption: ArtifactData is writable from the CLI side as the pack says.
  Done when: the plan tree, queue and fleet render from an Artifact, and `install.sh --no-mod` loses no capability in a smoke check.

- **Replace the tmux send-keys bus with SendMessage and ListAgents** — CLEAN — value 4 — effort M — risk med — category: orchestration
  Why: `fm bus` types into tmux panes, which only works inside tmux and races with whatever the user is typing. SendMessage reaches local, cloud and Remote Control sessions natively, so the tmux dependency can go.
  Done when: an idle session is woken by a bus message in a non-tmux terminal, and the tmux code path is deleted.

- **Fix the idle drive with ScheduleWakeup and Monitor instead of polling** — FIX — value 5 — effort M — risk low — category: reliability
  Why: T-0758 is "make sure it doesn't sit idle". A drive waiting on a gate or lane should arm a ScheduleWakeup, and stream long gates through Monitor so the next step starts on the event. No custom wait loops.
  Done when: a 5-minute background gate finishes and the next step starts within one wake interval, with no manual nudge and no custom sleep loop.

- **Replace `fm night` scheduling with CronCreate and cloud routines** — CLEAN — value 3 — effort M — risk med — category: scheduling
  Why: Foreman owns its own scheduler and runner for unattended work. Session crons cover in-session recurrence, and RemoteTrigger/`/schedule` covers overnight runs without the user's machine staying up. `fm night` shrinks to "create the routine".
  Done when: `fm night` creates and lists a native cron or routine and no longer runs its own timer.

- **Make ReportFindings the only reviewer output, and finish T-0034 as `/code-review`** — CLEAN — value 4 — effort S — risk low — category: review
  Why: the deferred `fm audit run` (L) would build headless lens reviewers plus a findings file. `/code-review` at low…max, `/security-review` and typed ReportFindings already render in the host UI, so the audit becomes a thin wrapper that maps findings to briefs.
  Done when: T-0034 closes as a wrapper under 100 lines, and reviewer lanes emit ReportFindings that the queue ingests.

- **Declare model and effort in the agent frontmatter and delete the routing code** — CLEAN — value 3 — effort S — risk low — category: agents
  Why: T-0755 asks whether Foreman can spawn lower models, and it already can (scout=haiku, S-tier lanes pass "sonnet"). The choice is scattered through code. Moving it to subagent frontmatter plus per-call `model`/`effort` makes it one readable table.
  Done when: grep finds no hardcoded model strings in plugin/lib, and `fm doctor` prints the role→model→effort table.

- **Track native-overlap in `fm doctor`** — CLEAN — value 4 — effort S — risk low — category: simplicity
  Why: past rounds dropped delta reads because Claude Code already returns a stub, which was found only by measurement. Tagging each custom feature with the native one that could replace it makes that check systematic. Assumption: a hand-kept table is enough and needs no runtime probing.
  Done when: `fm doctor` lists every Foreman feature with an overlapping native tool, and each is either justified in one line or opened as a removal task.

- **Derive the current step from tool activity instead of requiring step updates** — FIX — value 4 — effort M — risk med — category: reliability
  Why: T-0759 reports work starting on other steps without updating the step in the state. Pre/PostToolUse already sees every edit. Matching the touched files to each step's declared footprint removes a manual obligation. Assumption: steps declare footprints.
  Done when: editing a file owned by step 3 while step 2 is marked current moves the marker, or flags the mismatch, without any `fm` call.

- **Use LSP references in place of regex symbol-linking in `fm map`** — CLEAN — value 3 — effort M — risk med — category: map
  Why: `fm map` links tests to sources by filename convention (the test→src pairs in the pack). LSP definitions and references are exact. This would also make T-0214 (the edit-time test sentinel) cheaper.
  Done when: for a Python project with an LSP, test→source links come from references, and the regex fallback runs only when no LSP is available.

- **Run `/skill-doctor` over Foreman's 73 skills and prune** — CLEAN — value 3 — effort S — risk low — category: skills
  Why: 73 skills in plugin/skills is large surface and context cost. The built-in doctor reports overlap and dead skills without any new tooling, and fewer-permission-prompts can trim the settings Foreman writes.
  Done when: the skill count drops, `fm doctor` records the doctor run, and no eval case regresses.

- **Wild: Make the queue drive a saved named Workflow** — FEATURE — value 4 — effort L — risk high — category: orchestration — wild
  Why: Workflow gives deterministic multi-agent scripts, but it needs the user's opt-in. One user request, "save the drive as the foreman-drive workflow", would let Foreman invoke it by name afterwards. Classify→plan→execute→verify would then be a script, not prose rules. Assumption: named workflows can be re-invoked without a fresh opt-in each time.
  Done when: the user asks once, then `fm run` executes a queued S task through the saved workflow with no further prompt.

- **Wild: Take steers and asks through Artifact comments from a phone** — FEATURE — value 4 — effort M — risk med — category: devices — wild
  Why: ArtifactComments are sent to Claude. Combined with PushNotification, an ask becomes a push, and answering is a tap and a comment. That replaces the custom notify, ask and approval transport for remote devices.
  Done when: a pending `fm ask` appears as a push, and a comment on the Artifact resolves it in the ledger.

- **Wild: Replace MASTER.md with a shared Claude Doc that the user edits live** — FEATURE — value 2 — effort M — risk med — category: docs — wild
  Why: `fm doctor` fails its self-docs check whenever MASTER.md omits a command (T-0686). A shared editable doc, generated from the CLI definitions, ends the drift, and the user's edits come back as steers.
  Done when: the doc is regenerated from the CLI and the self-docs check passes with no hand edit.

- **Wild: Move the main thread into a worktree per task via EnterWorktree and ExitWorktree** — FEATURE — value 3 — effort M — risk med — category: isolation — wild
  Why: lanes get isolation, but the main thread edits the live tree, and a bad task can leave it dirty. If the whole task runs in a native worktree, revert becomes "exit and discard" (T-0751 task revert), and the merge happens only at done.
  Done when: a failed task is discarded with ExitWorktree and the main tree is byte-identical to before.
