# Brainstorm — lens: sci-fi: the 2030 harness that repairs itself, orchestrates its own lanes on the cheapest capable model, starts work from events and schedules and forecasts the user's next request, worked back to what Python and Foreman can do today

- **Re-run every done-when in a clean room before merge** — FIX — value 5 — effort M — risk low — category: verification
  Why: the dropped "Baseline red" task came from fm ship's scratch run using a different interpreter path than the session, so green in the worktree and green from a fresh checkout already differ.
  Done when: a lane whose test passes only because of an untracked file or its own env is refused at merge. A test with a planted untracked dependency shows this.

- **Mutate the guard with child-written evasions** — SECURITY — value 5 — effort M — risk low — category: guard
  Why: the guard is the product's promise in bypass mode, and your rule says weakness-finding should use signals Foreman didn't author. A tool-less child that never sees the guard's code writes obfuscated variants of blocked commands (base64, env indirection, heredocs, `$(…)`, aliases). Assumption: the child's corpus lands in a held-out file.
  Done when: `fm guard drill` prints a per-class miss rate. Each miss opens a FIX with the command quoted, and the miss rate is in `fm doctor`.

- **Give each lane an attenuated capability token** — SECURITY — value 4 — effort M — risk med — category: orchestration
  Why: unattended lanes from triggers and issue text hold the same authority as the user's session. Assumption: an HMAC token in stdlib is enough. It names allowed paths, verbs, model, budget and expiry, and only the guard can narrow it further.
  Done when: a lane that tries a verb or path outside its token is denied and logged, and an expired token fails closed.

- **Onboard each new model with a bench exam before routing to it** — FEATURE — value 4 — effort M — risk low — category: router
  Why: the T-2291 router learns from past lanes, so a new model ID (the environment lists five) has no history and is either never picked or picked blind. A cold-start exam of small bench tasks seeds its per-tier row.
  Done when: a new model ID in config triggers the exam, and `fm lane brief` shows a seeded row marked "exam, n=…" until real lanes replace it.

- **Cache verification by tree hash and pre-run it in a shadow worktree** — PERFORMANCE — value 4 — effort M — risk med — category: verification speed
  Why: every ship is gated by the full suite (2,000+ files, 396 under tests). Run the verify commands against a snapshot while the agent is still editing, key results by tree hash and co-change impact set, and keep the full suite as the final gate.
  Done when: a finish on an unchanged tree reads the cached result in under a second. A changed file invalidates only its dependents, and a test proves a stale hit is impossible.

- **Run every command in MASTER.md and the README as a test** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: the pack lists docs as thin, and the user had to ask for the website to be updated because it looked stale. Fenced `fm …` examples run in a sandbox nightly, and a mismatch opens a FIX naming the doc line.
  Done when: renaming a flag without updating the docs turns `fm doctor` red and names the file and line.

- **Expose Foreman as an MCP server** — FEATURE — value 4 — effort M — risk med — category: surfaces
  Why: the steer says Foreman isn't Claude-specific, yet T-0335 and T-0337 are blocked because Codex and Gemini lack the hook points. MCP tools (task, prove, guard-check, ask) work on every host. `plugin/templates/mcp-server` already exists as a base.
  Done when: a non-Claude client can open, prove and close a task through MCP, and the guard check returns the same verdict as the hook path.

- **Review the user's hand-made commits in the background** — FEATURE — value 4 — effort M — risk low — category: anticipation
  Why: assumption: much of the user's work happens outside Foreman sessions and is never checked. A post-commit hook starts a cheap lane that runs the tests, blast radius and plan-gate rules on the diff, and writes to the inbox only if something is red.
  Done when: a commit that breaks a co-changed test produces one inbox line within minutes. A clean commit produces nothing.

- **Pin a last-green rescue `fm` that can roll back the live one** — SECURITY — value 4 — effort M — risk med — category: self-repair
  Why: self-repair edits the thing that does the repairing, and T-0798 (blackstart) is only deferred. A single-file stdlib `fm-rescue` is copied at each green ship, outside the repo's reach, and can restore the previous release and report why.
  Done when: with the main `fm` deliberately broken, `fm-rescue` restores the last green release and the suite passes.

- **Shrink lane briefs to the smallest that still lands** — PERFORMANCE — value 3 — effort M — risk low — category: orchestration
  Why: briefs cost tokens on every lane, and the lean ratchet only watches always-on text. Correlate brief sections with outcomes in lane history, drop sections that never predict success, and cut tokens per landed lane.
  Done when: a report shows tokens per brief section and the correlation, and one section is dropped with no rise in re-fix rate across the next N lanes.

- **Serve hooks from a warm local daemon with a cold fallback** — PERFORMANCE — value 3 — effort L — risk high — category: hook latency
  Why: `bench_hooks.py` gates hook p50, and Python startup is the floor. A tiny client talks to a socket daemon, falling back to today's path if it is down or stale.
  Done when: p50 drops by a stated margin in `bench_hooks.py --runs 20`, and killing the daemon changes no verdicts.

- **Wild: Ablate ceremony steps on a sample of tasks** — FEATURE — value 4 — effort M — risk med — category: lean
  Why: wild; the lean ratchet only stops growth. Randomly skip one non-guard ceremony step (a reading, a recall, a cold read) on a few cheap S tasks. Steps whose absence changes no outcome (re-fix, revert, correction) become deletion candidates.
  Done when: `fm ablate report` lists each step with n and outcome delta, and the guard is provably never in the sample.

- **Wild: Re-derive old fixes from scratch as a monthly dojo** — FEATURE — value 3 — effort M — risk low — category: self-improvement
  Why: wild; a cheaper model re-solves a sample of closed FIX tasks from their pre-fix commit and the diffs are compared. A much smaller diff points at over-engineering to delete, and a failing re-derivation points at a test that never pinned the bug.
  Done when: `fm dojo` outputs per-task verdicts (same, smaller, fails, differs) and files at most N follow-ups.

- **Wild: Teleport a rate-limited lane to another vendor or machine** — FEATURE — value 3 — effort L — risk high — category: orchestration
  Why: wild; usage-limit pauses stall lanes while other agent CLIs and machines are idle. Bundle the worktree with the brief and the baton, resume on whichever agent has quota, and merge the result back as a normal lane.
  Done when: a lane paused by a simulated limit resumes on a second backend, and its result passes the same merge gate.

Next question: Which of Foreman's autonomous acts today has no cheap, user-visible way to be undone within a minute, and what would an undo cost for each?
Next question: Where does Foreman's own signal (outcomes, corrections) disagree with what a held-out reader of the same session would conclude, and who checks that gap?
