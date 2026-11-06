# Brainstorm — lens: bold bets

- **Own the turn loop through the Agent SDK** — FEATURE — value 5 — effort L — risk high — category: runtime
  Why: T-0758 (the user's "make sure it doesn't sit idle") and T-0759 (steps advancing without the pointer updating) both come from Foreman steering a session it doesn't own. It nudges with tmux `send-keys` and Stop-hook blocks. An SDK streaming-input client could run `fm drive` as a work-conserving scheduler: `canUseTool` callbacks, in-process guard and step-gate, and `setModel` and effort per turn. Idle-while-queued becomes impossible by construction. Assumption: the SDK exposes streaming input and `setModel`, and the TUI can still be attached. Not the same as the seen ScheduleWakeup/Monitor patches.
  Done when: a 2-hour queue run launched through the SDK driver shows no ledger gap over 30s while the queue is non-empty, and the tmux send-keys path isn't used.

- **Answer status questions with zero model tokens** — PERFORMANCE — value 4 — effort S — risk low — category: speed
  Why: assumption: much of the user's traffic is "where are we / what's queued / what's blocked", and each one burns a full model turn plus hook context. A UserPromptSubmit hook can match exact status-shaped prompts, render the answer from STATE, and block the prompt with that text as the reply. This differs from the seen "answer side questions from a read-only lane", which still calls a model.
  Done when: the prompt `status` returns the queue and step in under 150ms and the transcript shows no model call for that turn.

- **Run cheap workers on a patch protocol with no tools** — FEATURE — value 4 — effort M — risk med — category: tokens/models
  Why: T-0755 asks whether Foreman can spawn lower-model agents. Today S-tier lanes pass `model: "sonnet"` but still pay for tool-call round trips and tool schemas. For mechanical steps, Foreman assembles the context bundle itself from `fm map` and the step's footprint. It runs `claude -p --tools "" --json-schema` on haiku or sonnet, receives a unified diff, applies it, and runs the gates. Failures escalate with the gate output as the brief.
  Done when: on 10 replayed S steps, patch-protocol workers pass the same gates as the current lanes at under half the tokens, and the failures escalate automatically.

- **Gate every cloud feature behind a per-project consent matrix with schema-first payloads** — SECURITY — value 4 — effort M — risk low — category: privacy
  Why: the focus list proposes Artifacts, ArtifactData, PushNotification, remote isolation, RemoteTrigger and Claude Docs, and every one sends project data off the machine. Proposed: each surface is off per project by default. Each payload is built from a typed allowlist schema (ids, titles, counts, never free-text bodies) and passes the redactor. `fm egress` prints what each surface would send. This is a per-surface switch tied to adoption, not the generic seen "scan all outbound data".
  Done when: with Artifact consent off, the publisher refuses and writes nothing. With it on, a fixture containing a planted secret produces a payload that is a schema-valid subset with the secret absent.

- **Hot-swap the main thread's model at step boundaries** — FEATURE — value 4 — effort M — risk med — category: models
  Why: user-visible need behind T-0755. Planning steps deserve a strong model and mechanical edit steps don't, but today the main thread keeps one model for the whole task. The driver switches the model at declared step boundaries, using `/model` or the SDK's `setModel`. Risk: a switch invalidates the prompt cache, so it should fire only when the expected saving beats the re-read cost. That cost estimate belongs to the idea, not an assumption.
  Done when: on a replayed 6-step task, the model changes only at boundaries where the estimate favoured it, and the ledger records each swap with its estimated and actual cost.

- **Classify and redact captured messages locally before any cloud call** — SECURITY — value 3 — effort M — risk med — category: privacy
  Why: raw captures (T-0756 to T-0760) go verbatim through the cloud model before any classification, and pasted messages can contain secrets. A small local model, or a rules-only fallback, could do tier and type classification, title generation and secret redaction. The cloud model would then see only the cleaned brief. Assumption: a local engine is installed; without one, rules-only keeps today's behaviour.
  Done when: with a planted token in a captured message, the cloud-bound brief contains no token, and the classifier makes no network calls (checked with the network blocked).

- **Make skill descriptions pass a trigger-precision bench** — CLEAN — value 3 — effort M — risk low — category: skills/quality
  Why: 73 skills load by description match, and a skill that triggers on the wrong prompt (or fails to) wastes tokens or silently skips discipline. `plugin/evals/` (21 files) and `claude plugin eval` already exist. Add a set of positive and near-miss prompts per skill. The release gate reports precision and recall, and a skill below the threshold gets its description tuned or the skill is demoted to manual invoke.
  Done when: `fm doctor` lists per-skill trigger precision/recall from the bench, and one deliberately mis-described skill makes the gate fail.

- **Anchor the guard in managed settings the agent can't edit** — SECURITY — value 4 — effort M — risk med — category: security
  Why: in bypass mode the agent can in principle rewrite `~/.claude/settings.json` and drop the guard hooks. Claude Code's managed-settings location is root-owned, so a one-time optional install step there could lock the guard hooks. Assumption: the one-time elevation fits the user's no-handing-commands rule only if the installer runs it itself after consent; otherwise this stays opt-in. A PreToolUse tripwire on settings writes is the fallback.
  Done when: with managed settings installed, an attempted edit of the user-level settings to remove a Foreman hook leaves the hook active in the next session.

- **Reload hooks on save and diff their behaviour against recorded payloads** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: 149 test files and a latency-gated hook surface mean plugin changes need fast feedback. `fm dev` watches `plugin/lib` and, on save, replays the last 50 recorded real hook payloads through the old and new code. It prints only the changed decisions and the latency delta against the `bench_hooks.py` budget.
  Done when: editing a guard rule prints a diff listing exactly the recorded commands whose verdict changed, within 3 seconds of saving.

- **Wild: Make the autonomy dial calendar-aware** — FEATURE — value 3 — effort M — risk med — category: user value — wild
  Why: assumption: a calendar MCP or ICS file is available. Before a meeting Foreman writes a two-minute "where things stand" card. During it, it keeps to quiet lanes and queues all asks. After it, it replays the digest. Deadlines in the calendar become the time box that cut-line planning uses.
  Done when: with a fixture calendar showing a 14:00 meeting, asks raised at 13:50 are held and delivered as one digest at the meeting's end.

- **Wild: Drive Foreman from a hardware button** — FEATURE — value 2 — effort M — risk low — category: delight — wild
  Why: assumption: the user would use a USB macro pad, a Stream Deck or a phone shortcut. Four mapped keys do approve-default, defer, pause-everything and show-next, all through the existing `fm ask` and `fm pause` commands. A pause button the user can hit without looking at the terminal is the cheapest kill switch there is.
  Done when: pressing the mapped pause key flips `fm pause` state within one second, and the press and resulting state show in the ledger.

- **Wild: Mint an end-of-day "token tax return"** — FEATURE — value 3 — effort M — risk low — category: tokens — wild
  Why: the user keeps asking for more token savings and speed but has no single view of what Foreman itself costs. Each day, split spend into real work, Foreman overhead (injected context, reviewers, replans) and waste (retries, idle re-reads), then list three proposed deductions, each a rule or skill that would have cut spend. Make overhead share a release metric.
  Done when: `fm tax` prints the three-way split for a day from transcripts and the ledger, with the three deductions tied to the sessions they came from.
