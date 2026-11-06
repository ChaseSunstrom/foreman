# Brainstorm — lens: bold bets

Assumptions are marked inline. The CC capabilities I name that the pack doesn't list (prompt/agent hooks, the native task list, plan mode, native memory, `permissionMode` in agent frontmatter) are not confirmed here, so each idea starts with a probe.

- **Make the native task list the step pointer** — FIX — value 5 — effort M — risk med — category: step tracking
  Why: T-0759 says work starts on other steps without the step being updated. Foreman's pointer is its own file, so nothing forces the model to touch it. The `TaskCompleted` hook is already used. Assumption: the host's task list (TaskCreate/TaskUpdate or similar) is reachable and visible to the model.
  Done when: a plan with 4 steps appears as 4 native tasks. A scripted run that edits step 3's files while step 2 is open gets a PostToolUse nudge, and the pointer only advances when the matching native task is completed.

- **Judge "done" with a native prompt/agent hook on Stop** — FEATURE — value 4 — effort M — risk med — category: done-gate
  Why: Foreman's gates are all shell and Python, so semantic checks like "does the close-out claim what the diff shows?" cost a spawned `claude -p` child. Assumption: the host supports hook type `prompt` or `agent` with a haiku model.
  Done when: a close-out that claims an unrun test is blocked by the semantic hook. The deterministic gate still decides when the hook times out. `bench_hooks.py` shows no added latency on non-Stop events.

- **Run every L plan through a plan-mode dry-run subagent** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: plan reviews today are prose critiques. Assumption: an agent can be spawned read-only (`permissionMode: plan` or a read-only tool list). That agent walks the plan step by step, naming the exact file, symbol and command for each step and where it cannot proceed.
  Done when: a plan referencing a nonexistent function returns "step 3 unexecutable: symbol not found" before any edit. A seeded-bad-plan fixture is caught.

- **Back up the ledger through ArtifactData, with an explicit opt-in** — FEATURE — value 4 — effort L — risk med — category: sync
  Why: "fleet across machines" ideas assume a server or git ref. The Artifact shared db is a free, authenticated store that the CLI can write to. Assumptions: ArtifactData has size limits, and sending ledger data to claude.ai counts as publishing. It needs an off-by-default setting and redaction first.
  Done when: with the setting on, task state written on machine A is readable on machine B within a minute, with secrets redacted. With the setting off, no network call is made, which a test asserts.

- **Verify "done" in a remote clean-room session** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: every gate today runs on a machine carrying uncommitted state, a warm cache and ambient credentials. The Agent tool's `isolation: "remote"` runs on a fresh checkout. That makes a distinct evidence type: green on a pushed commit with nothing local. Assumption: the repo is pushed, so it fits Foreman's release tasks (T-0431 and the 1.2.x releases).
  Done when: a seeded commit that passes locally only because of an untracked file fails the remote verify. The evidence line is labelled `clean-room`.

- **Bridge lessons and vetoes into native memory files** — FEATURE — value 3 — effort S — risk low — category: memory
  Why: Foreman's lessons only reach sessions where Foreman's hooks inject them. The native memory directory is loaded by every session in the project. Assumption: a lesson with a confidence score can be written as a one-fact file in the host's memory format.
  Done when: a lesson promoted at confidence ≥ N appears as a native memory file. Retiring it deletes the file. A plain `claude` session without the plugin recalls it.

- **Switch output style by phase** — FEATURE — value 3 — effort S — risk low — category: tokens
  Why: Foreman already ships an output style, but one style serves both execution and close-out. Execution wants near-silent output and close-out wants evidence tables. Assumption: a hook can set or alter the style per turn. If it can't, inject the equivalent through additionalContext.
  Done when: output tokens per execution turn drop on a replayed task, measured by the existing bench. Close-out content is unchanged.

- **Adopt stray Claude sessions** — FEATURE — value 3 — effort M — risk med — category: fleet
  Why: Foreman only governs sessions with its hooks. A stray session in another terminal is uncontrolled and unseen. ListAgents and SendMessage could find strays and offer adoption, but only on user consent, since messaging another session is outward-facing. Assumption: ListAgents sees local sessions without Foreman.
  Done when: with a stray session running, `fm doctor` lists it with project and age. Only after a one-time grant does it send an adoption message.

- **Refuse to exit a turn while any step is unaccounted for** — FEATURE — value 5 — effort M — risk med — category: idle control
  Why: T-0758 reports the drive sitting idle. Earlier ideas schedule wakeups. This one makes the Stop contract explicit: every turn must end in one of three states (a step advanced, a blocker recorded, or a handoff scheduled with a wake time), and Stop checks for a ledger event proving it.
  Done when: a scripted session that ends a turn with the queue non-empty and no recorded state is blocked once. After the nudge, the next turn records one of the three states.

- **Publish the discipline as a marketplace plugin with a native update channel** — CLEAN — value 3 — effort M — risk med — category: distribution
  Why: install.sh curls a script and clones into `~/.claude/foreman`, and the 1.2.x releases are done by hand. The `claude plugin` CLI already installs and evaluates plugins. Assumption: the marketplace flow can carry the hooks, subagents and skills Foreman ships.
  Done when: a fresh machine gets the same working Foreman from `claude plugin install` plus `fm doctor`, with the wiring step reduced to settings only.

- **Wild: Make a cheap sentinel agent the second-opinion guard** — SECURITY — value 3 — effort M — risk med — category: guard
  Why: the guard is heuristic and its refusals are costly (see the dropped heredoc and `fm task new` cases). A haiku PermissionRequest-time agent that reads the command and the active brief could break ties only in the cases the heuristic marks "unprovable". It would never loosen a hard block.
  Done when: on the recorded corpus of "couldn't prove" refusals, the sentinel's allow/deny matches the user's later verdicts above a stated rate, with zero loosened hard blocks.

- **Wild: Open each session with an Artifact "last night" page and let comments drive the queue** — FEATURE — value 3 — effort M — risk med — category: cockpit
  Why: the Artifact cockpit is already proposed, but only as a status board. The twist is that each comment on a task card becomes a captured steer or a reorder with a confirmation echo. This also covers T-0757's need to group and reorder from one place.
  Done when: a comment "do this before T-0759" on a card reorders the queue and the page shows the new order. The ledger records the comment as the source.

- **Wild: Spawn lower-model workers by contract, not by tier** — FEATURE — value 4 — effort M — risk low — category: delegation
  Why: T-0755 asks whether Foreman can spawn haiku or sonnet agents. It already does for scout and S-tier lanes. The gap is a per-step worker contract: allowed files, one observable, and an automatic retry on a stronger model after one failure. The pack doesn't show this.
  Done when: a mechanical step runs on haiku and its diff passes the gate. A seeded hard step fails once on haiku and succeeds on a stronger model, and the ledger shows both model attempts.
