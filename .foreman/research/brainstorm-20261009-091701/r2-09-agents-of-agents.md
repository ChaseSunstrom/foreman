# Brainstorm — lens: agents of agents

- **Fake the agents to test the orchestrator** — FEATURE — value 5 — effort M — risk low — category: testing
  Why: T-0316 (re-run a real fm-builder lane after a Claude Code update) and T-0336 are blocked on live runs, and recent drive bugs (T-0401, idle sessions) were found in the field. Needs: a scripted `claude -p` double that replays behaviours (lies "done", ignores the brief, times out, edits CHANGELOG, stalls mid-lane).
  Done when: `fm doctor` runs a suite where each scripted misbehaviour makes the drive, lane merge or done-gate react as specified, with no network.

- **Cascade budgets through a delegation tree** — FEATURE — value 4 — effort M — risk med — category: orchestration
  Why: "super recursive" brainstorming means agents spawning agents, but `fm budget` is flat. Each spawn gets a slice of its parent's pace allowance, a depth limit and cycle detection. Unused slices flow back up. Per T-0320 it never caps by tokens, only by pace.
  Done when: a test spawns a 3-level tree, the 4th level is refused with a named reason, and the ledger shows per-node spend that sums to the root's.

- **Make handoffs typed receipts** — FEATURE — value 4 — effort M — risk low — category: protocol
  Why: sub-agents return prose that the main thread has to trust. Each role returns a schema (claims, each with an evidence pointer, plus files touched and open questions). Prose without a resolvable pointer is bounced. Builds on T-0034's findings file.
  Done when: a reviewer reply with an unresolvable evidence path is rejected and re-requested, and `fm tour` shows claims linked to their evidence.

- **Unblock blocked tasks with scouts** — FEATURE — value 4 — effort M — risk low — category: autonomy
  Why: T-0316, T-0325, T-0335, T-0336, T-0337, T-0352 and T-0418 sit blocked. A scout per blocked task tries the unblock (checks if the dependency now exists, drafts the install command, tests the adapter) and leaves a one-question card for what truly needs the user.
  Done when: running it on the blocked list either moves a task to queued with proof or attaches a single yes/no card to it.

- **Share recon across agents by tree hash** — PERFORMANCE — value 3 — effort S — risk low — category: cost
  Why: reviewers, scouts and builders each re-read the same files. Cache recon and outline answers keyed by tree hash and the question, and reuse them across lanes. Invalidate only the files that changed.
  Done when: two reviewers on one diff make one `fm impact` scan, and the cache hit rate shows in `fm cost`.

- **Force diverse retries when a gate fails repeatedly** — FEATURE — value 4 — effort M — risk med — category: debugging
  Why: after the same gate fails 3 times, spawn N debuggers. Each gets the failures plus a forbidden-approach list built from the earlier attempts' diffs, so the retries can't converge on the same fix. The gate chooses the winner.
  Done when: on a seeded-failure fixture, retries produce at least 2 materially different diffs and the passing one lands.

- **Turn repeats into tested project tools** — FEATURE — value 3 — effort M — risk med — category: self-extension
  Why: `fm repeats` already names what each repeated procedure "could become" but nothing builds it. A tool-smith lane writes the script, its test and a registered `fm` shortcut, then the guard learns it as an allowed verb.
  Done when: a repeat flagged 3+ times gets a lane that lands a script with a failing-then-passing test and `fm usage` shows it used.

- **Offer Foreman as a delegate to other orchestrators** — FEATURE — value 4 — effort L — risk med — category: interop
  Why: `fm mcp` is read-only and adapters exist for Codex, Gemini and opencode. Add a write-side tool, `delegate(brief)`, that returns a proven result (diff, evidence, verdict) so other agents can hand Foreman a task. Assumption: an `fm ask` grant is required per caller.
  Done when: an MCP client submits a brief and receives a receipt with gate evidence, and an ungranted caller is refused.

- **Enforce information barriers between roles** — SECURITY — value 3 — effort M — risk med — category: verification
  Why: an "independent" reviewer who reads the builder's summary isn't independent. Guard rules per role decide what a sub-agent may read (the diff and the spec, never the builder's transcript or notes).
  Done when: a reviewer lane reading the builder's brief notes is refused, and the event is logged with the role.

- **Wild: Shadow every expensive agent with a cheap predictor** — FEATURE — value 3 — effort L — risk high — category: routing
  Why: assumption. A small model predicts the big agent's next tool call at each step. High agreement lets the cheap model take over the rest of routine stretches; divergence marks the novel, uncertain steps worth a second read.
  Done when: on 20 replayed tasks the agreement score predicts which steps later needed correction better than chance, with the numbers shown.

- **Wild: Discover new specialist roles from failure clusters** — FEATURE — value 3 — effort L — risk med — category: self-improvement
  Why: assumption. Cluster past corrections and blocked tasks. If a cluster has no matching reviewer lens (say "symlink semantics" or "wait loops"), generate a specialist, bench it, and retire any lens that finds nothing over 50 tasks.
  Done when: a proposed role ships only if `fm bench` shows it catches a case the existing lenses missed, and an idle lens gets a retirement proposal.

- **Wild: Run a pre-mortem with a council of past users** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: before an L plan, spawn personas built from `fm taste` and `fm vetoes` (the user at their pickiest, the JARVIS maintainer who hit the bug, the release-day user). Each lists how the plan will annoy them. Surprises feed the brief.
  Done when: an L plan's brief gains a "pre-mortem" section whose items each cite a real veto, steer or consumer report.

- **Interview the main thread before compaction** — FEATURE — value 4 — effort M — risk low — category: resume
  Why: `PreCompact` saves the checkpoint but not the tacit state: rejected hypotheses, hunches, "don't touch X, it looks wrong but isn't". An interviewer agent extracts these into the brief so the resumed session doesn't redo dead ends.
  Done when: after a forced `/compact`, the resumed session's first action avoids an approach listed as rejected in the brief.
