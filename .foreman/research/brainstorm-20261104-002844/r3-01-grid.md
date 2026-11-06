# Brainstorm — lens: grid

**Grid used.** Surfaces are CLI verbs (`plugin/lib/sampo/cli.py`), hooks, the web UI, the pane and the Smith TUI. Actors are the user, the builder agent, other lanes and the unattended drive. Failure modes are missing, wrong, slow, unsafe and unclear. All assumptions are marked.

- **Pin each open plan step to the base it assumed** — FEATURE — value 4 — effort M — risk low — category: resume
  Cell: resume × builder agent × wrong.
  Why: resume is the worst area. A goal carried over days resumes against a main that may have moved. Assumption: steps don't record what they assumed.
  Done when: after a commit touching a step's recorded files lands in a scratch repo, `fm goal resume` marks that step "premise changed" and lists the files.

- **Stamp plan steps with the steer set they were planned under** — FEATURE — value 3 — effort S — risk low — category: plan
  Cell: unattended drive × wrong.
  Why: steers arrive mid-run, such as the `--pace off` and round-first rules. A multi-day plan can keep obeying a superseded rule. Assumption: no stamp exists today.
  Done when: filing a new steer makes `fm next` list the open steps planned before it, each with a one-line "still valid?" default.

- **Set lease TTL from the task's measured duration** — PERFORMANCE — value 3 — effort S — risk med — category: leases
  Cell: lanes × slow.
  Why: the drive has been miscounting 45-minute subagents (T-2873, T-0575). A fixed TTL treats a slow honest builder as dead. Assumption: a fixed TTL is in use.
  Done when: a fake builder idle for 1.5× its kind's p90 keeps its lease, and one idle for 4× loses it, in a test.

- **Redact secrets at evidence-write time with a local pointer** — SECURITY — value 4 — effort M — risk low — category: evidence
  Cell: evidence store × unattended × unsafe.
  Why: the pack's rule is "keep the full output of any run cited". Evidence now moves between worktrees and the shared object store, and the site publishes data. Assumption: no redaction pass runs on write.
  Done when: a planted token in command output is absent from the stored evidence and the published data, and the full text is still reachable only through the local pointer.

- **Plan once, execute small** — FEATURE — value 5 — effort L — risk med — category: Smith / local models
  Cell: Smith TUI × builder agent × missing.
  Why: the user is pushing hard on local models (qwen3.8-27b, small-model uplift). Goal-to-finish assumes a strong model throughout. Assumption: Smith has no goal decomposition into self-contained steps.
  Done when: a strong model writes clauses and steps that each carry their own context, and `sampo smith` on the 27b local model finishes a 5-step scratch goal with the same clause verdicts.

- **Pin reviewer lanes to the commit they review** — FIX — value 3 — effort S — risk low — category: review
  Cell: other agents × wrong.
  Why: the cold different-model reader may inspect a worktree the builder has since moved. That produces a verdict about code that no longer exists. Assumption: reviews read the live tree.
  Done when: a review records its commit hash, and `fm task finish` rejects a verdict whose hash isn't the final one.

- **Make each goal declare its outward-action envelope** — SECURITY — value 4 — effort M — risk med — category: unattended
  Cell: unattended drive × unsafe.
  Why: multi-day runs under a standing push grant can ship repeatedly. Nothing caps the whole goal; only per-task grants exist. Assumption: grants are per task.
  Done when: a goal files "at most N pushes, $X" at intake, and the drive stops with a plain reason line when either is hit.

- **Print the worktree resolution trace on every state failure** — FIX — value 4 — effort S — risk low — category: worktree
  Cell: CLI verbs × builder agent × unclear.
  Why: the request names evidence and lease commands failing inside the builder worktree. A bare failure leaves the builder guessing which directory it was resolved against. Assumption: failures don't name the path tried.
  Done when: a failing `fm evidence` run in a worktree prints cwd, resolved state dir, and the one command that fixes it.

- **Show a "last verified" age on every clause in the web UI** — FEATURE — value 3 — effort S — risk low — category: web UI
  Cell: web UI × user × unclear.
  Why: the web UI is the pack's only listed surface. "Proven" with no age looks the same on day 1 and day 6. Assumption: clause cards carry no timestamp.
  Done when: a clause proven 3 days ago shows "3d" with a stale tint past a set threshold, and the page works with no JavaScript.

- **Wild: Make a tool-less child say what a clause's evidence proves** — FEATURE — value 4 — effort M — risk low — category: done-gate
  Cell: builder agent × wrong, aimed at the false dones.
  Why: assumption: some of the six false dones were evidence that ran but proved something else. The child sees only the clause and the captured output, never the code, and must name the claim. A mismatch holds done.
  Done when: replaying the six false-done cases, the child's restated claim fails to match the clause on at least one that today passes.

- **Wild: Schedule heavy proofs for predicted quiet quota hours** — PERFORMANCE — value 3 — effort M — risk low — category: scheduling
  Cell: unattended drive × slow.
  Why: the user said to wait out real usage limits. Heavy re-proofs and long-tier runs compete with builders for the same quota. Assumption: usage history exists in the ledgers.
  Done when: in a simulated week of usage, a queued re-proof starts in the lowest-use window and not during a builder burst.

- **Wild: Hold a séance interview for every dead lane** — FEATURE — value 3 — effort M — risk low — category: resume
  Cell: other agents × missing.
  Why: a lane killed mid-run loses beliefs that never reached a ledger. A child reads its transcript tail and writes three lines: what it believed, what it was about to do, and what it left half-done. Resume then shows them. Assumption: the transcript tail survives the kill.
  Done when: killing a scratch builder mid-edit yields a three-line note that names the half-edited file.

- **Wild: Add a "boring goal" mode that refuses cleverness** — FEATURE — value 2 — effort S — risk low — category: plan
  Cell: builder agent × wrong, in the planner's step count.
  Why: assumption: small goals get over-planned because the full machinery engages by default. Under a size threshold it caps the plan at three steps, with one clause and one proof.
  Done when: a one-line fix goal files at most three steps and finishes with fewer ledger records than today.

**Cells left empty.**
- Smith TUI × unattended and web UI × unattended are skipped. The unattended drive reaches the web UI only through the drive's existing status data, so I found no distinct failure there.
- Hooks × user × unsafe is covered by the Ward and the pack's many guard ideas.
- Slow × user in the CLI is skipped. The pack already holds many hook-timing and render-budget ideas.

Next question: which of the six false dones were a wrong claim, which were a missing check, and which were a stale proof? One idea per class would be better than one idea for all six.
Next question: when the user returns after days, which first screen do they open, and does that screen show what changed in main while the goal was paused?
