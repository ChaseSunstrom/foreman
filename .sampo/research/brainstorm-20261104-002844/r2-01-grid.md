# Brainstorm — lens: grid

**Grid:** surfaces are the CLI (`fm`/`sampo`), hooks, the web UI, the Smith TUI, and other harnesses (Codex, Gemini, opencode). Actors are the user, the agent, other agents (lanes), and an unattended run. Failure modes are missing, wrong, slow, unsafe, and unclear. Assumption: the goal ledger and clause store exist as the earlier ideas describe.

- **Run the done-gate as a verifier loop for harnesses with no Stop hook** — FEATURE — value 5 — effort M — risk med — category: done-gate
  Cell: other harness × agent × missing.
  Why: T-0337 says Gemini's AfterAgent deny discards the answer, so Stop isn't wired. Smith has no host hook at all. A false done stays free there. `fm run` would verify after the agent exits and re-invoke it with the unmet clauses.
  Done when: a scripted Codex-style agent that claims done with one clause unproven is re-invoked with that clause named. The goal closes only after evidence for it exists.

- **Make clause status writable only by the verdict command** — SECURITY — value 4 — effort S — risk low — category: lanes
  Cell: lane × other agents × unsafe.
  Why: the worktree breakage shows lanes touch goal state, and nothing stops a lane from editing the ledger to mark a clause done. Assumption: status lives in a plain file.
  Done when: a test lane that edits the clause file directly is rejected at merge and the clause stays open.

- **Skip steps whose change already landed on resume** — FIX — value 5 — effort M — risk med — category: resume
  Cell: unattended run × resume × wrong.
  Why: resume is the worst area (2 of 6 needed a later fix). A crash between commit and ledger write makes resume redo work. Match each planned step against `git patch-id` of commits since the checkpoint.
  Done when: killing the run after commit but before the ledger write, then resuming, creates no duplicate commit and marks the step landed.

- **Namespace evidence and leases by goal id** — FIX — value 4 — effort S — risk low — category: concurrent goals
  Cell: CLI × agent × wrong.
  Why: assumption: two goals can touch overlapping files in one repo, and evidence is keyed by task or tree, so one goal's proof could satisfy another's clause.
  Done when: two goals sharing a file each report their own clause status, and proving one leaves the other unproven.

- **Refuse `fm ship` while the goal's done is provisional or unproven** — SECURITY — value 4 — effort S — risk low — category: push safety
  Cell: agent × unsafe.
  Why: the standing push grant lets landed work reach main without asking. Six false dones mean a false done could be pushed.
  Done when: with one clause unproven, `fm ship` exits non-zero and its Next line names the clause.

- **Capture "must still hold" clauses at goal start** — FEATURE — value 4 — effort M — risk med — category: collateral damage
  Cell: agent × wrong.
  Why: assumption: some false dones pass the stated clauses while breaking something else. Snapshot the baseline passing-test set, the public `--json` shapes, and the hook bench numbers, then check them at done.
  Done when: a planted regression outside the goal's files turns done red, naming the baseline item it broke.

- **Require a captured run for user-visible clauses** — FEATURE — value 4 — effort M — risk med — category: evidence
  Cell: web UI × agent × wrong.
  Why: for UI goals, tests passing is not the user's sense of done. Evidence would be an `fm shot` or `fm flow` artifact bound to the tree hash.
  Done when: a UI clause cannot go proven on a unit test alone. It needs an artifact whose hash is stored in the evidence record.

- **Invalidate evidence by the files its command read, not the whole tree** — PERFORMANCE — value 3 — effort M — risk med — category: evidence
  Cell: CLI × agent × slow.
  Why: whole-tree hashes mark everything stale after any edit, so the agent either reruns all proofs or skips them. Record each proof's declared read-set.
  Done when: editing an unrelated file leaves a clause proven. Editing a file in its read-set flips it to stale.

- **Bench resume time-to-first-useful-action** — PERFORMANCE — value 3 — effort S — risk low — category: resume
  Cell: hooks × agent × slow.
  Why: resume cost isn't gauged. The anchor re-inject plus ledger replay on a goal with days of history could be slow enough to be skipped.
  Done when: `bench_hooks.py` has a resume case with a bar, and CI fails past it on a 10k-record ledger.

- **Add "seams" markers to the web goal page** — FEATURE — value 3 — effort M — risk low — category: web UI
  Cell: web UI × user × unclear.
  Why: for a goal carried over days, the user can't see what a crash or compaction cost. Mark each seam with what was re-derived and what could not be recovered.
  Done when: a goal with one compaction and one kill shows two seams, each listing its re-derived and lost items.

- **Turn each reopened goal into a long-tier scenario** — FEATURE — value 5 — effort M — risk low — category: eval corpus
  Cell: user × wrong.
  Why: the long tier is 0/6 and unchanged since gen 2, with six fixed false dones. When the user says "not done," a child writes an autopsy, and the missed clause becomes a new scenario.
  Done when: reopening a goal produces a scenario file that runs in the long tier and currently fails.

- **Wild: Mine the dead session's transcript for unwritten intent on resume** — FEATURE — value 4 — effort M — risk med — category: resume
  Cell: unattended run × resume × unclear.
  Why: a hook-written note only holds what the agent chose to record. A tool-less child reads the dead transcript tail and extracts what the agent was about to do and assumed. The result goes into the resume card marked unverified.
  Done when: after a kill mid-step, the resume card names the interrupted step, and a reviewer judges it correct on at least 4 of 5 kills.

- **Wild: Ask for an "I'll be annoyed if…" line at intake and compile it into a clause** — FEATURE — value 4 — effort S — risk low — category: intake
  Cell: user × missing.
  Why: assumption: the user's real done criteria are unstated tripwires. One optional sentence becomes a clause with a mandatory evidence slot.
  Done when: a goal started with that line shows it as a clause in the pane, and done is refused without evidence for it.

- **Wild: Give each false done a signature and match new claims against it** — FEATURE — value 3 — effort M — risk med — category: done-gate
  Cell: agent × wrong.
  Why: the six known false dones share shapes, such as a proof that passed vacuously or a clause satisfied before any work. The done-gate warns when a new claim matches a stored signature.
  Done when: replaying the six known false dones, the gate flags at least 5 before any model child runs.

**Cells left empty:**
- Site × any actor: the site isn't on the goal path.
- Smith TUI × user × unclear: the existing pane work covers it.
- Unattended × slow: stall detection by clause movement already exists in the ideas so far.
- Any × lease in a worktree: pin state with an env var and the worktree matrix are already listed.
- User × unsafe: the push grant is already standing.

Next question: which of the six false dones were already red on the parent commit, meaning the clause was vacuous, and which were genuinely unmet?
Next question: when resume redoes work, does the ledger or the tree disagree first? Whichever it is should become the source of truth.
