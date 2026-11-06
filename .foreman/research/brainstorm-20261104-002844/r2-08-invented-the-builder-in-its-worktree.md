# Brainstorm — lens: invented: the builder in its worktree

- **Preflight the closing path at task start** — FEATURE — value 5 — effort M — risk low — category: resume
  Why: Evidence and lease commands fail inside the builder worktree, and the builder only finds out at close. Assumption: finish-gate steps can run against an empty diff without side effects.
  Done when: in a harness-made linked worktree, `fm task start` runs evidence-record, lease-acquire and finish-gate in dry mode. It prints one line per step, "works here" or "fails: <cause>", before any edit.

- **Materialise the brief into the worktree** — FEATURE — value 4 — effort M — risk low — category: resume
  Why: Resume is the worst area (2 of 6 needed a later fix), and a sandboxed builder can't always read the state dir. Assumption: the sandbox lets the builder read inside its own worktree.
  Done when: starting a builder writes `.sampo/context/` (goal clauses, brief, steers, the "where I was" note) into the worktree, git-excluded. A fresh agent with no state-dir access can resume from `cat` alone.

- **Write evidence into the shared git object store** — FEATURE — value 5 — effort M — risk med — category: evidence
  Why: The worktree and the main checkout share one git common dir, so evidence kept as `refs/sampo/evidence/<task>` survives worktree deletion and merges with the work. Assumption: the sandbox allows writes to the common dir, which it must for commits to work.
  Done when: evidence recorded inside a linked worktree is readable by `fm evidence show` from the main checkout after `git worktree remove`, with no copy step.

- **Add an evidence outbox for denied writes** — FIX — value 4 — effort S — risk low — category: evidence
  Why: The sandbox can deny state-dir writes, and the record must not be lost. Assumption: harvesting on the worktree-remove or session-end hook is reliable enough.
  Done when: with the state dir made read-only, `fm evidence add` appends to `<worktree>/.sampo/outbox/` and exits 0 with a "queued" line. The drive's next tick, or the worktree-remove hook, harvests it. A test kills the builder before harvest and the record still arrives.

- **Print a resolution trace on every worktree failure** — FIX — value 4 — effort S — risk low — category: diagnosability
  Why: Failures in the worktree give no cause today. Assumption: the failing step knows which state path it resolved.
  Done when: any evidence or lease failure prints cwd, git common dir, resolved state dir, writable yes/no, and the one command that would work from here.

- **Adopt a foreign worktree on first verb call** — FEATURE — value 4 — effort M — risk med — category: worktree
  Why: The harness, not Sampo, created this worktree, so Sampo's lane records don't know it. Assumption: a `.git` file whose common dir matches a registered repo is enough to bind it.
  Done when: the first `fm` verb in an unregistered linked worktree binds it to its repo and the task on the branch name, and says so once. A second call is silent.

- **Beat the lease with a heartbeat file in the worktree** — FEATURE — value 3 — effort S — risk low — category: resume
  Why: A crashed builder leaves a lease the parent can't tell from a live one. Assumption: the builder can always write inside its own worktree, even when it can't reach the state dir.
  Done when: the lease's liveness is the mtime of `<worktree>/.sampo/heartbeat`, touched by every hook. The drive reclaims a lease whose heartbeat is older than the TTL, and a kill-test proves it.

- **Split-world detector** — FIX — value 4 — effort M — risk low — category: resume
  Why: The builder may think it writes state S while the parent reads S′, so a close looks like it has no evidence. Assumption: parent and child can compare a count cheaply.
  Done when: the drive's tick compares evidence and lease counts the builder reports (last line of its heartbeat) with what it reads from state. A mismatch raises a named "split state" card instead of a false done or a stall.

- **Run a canary builder through the harness's own worktree call** — FEATURE — value 3 — effort M — risk low — category: testing
  Why: Tests build worktrees the way Sampo does, so they miss how the harness does it. Assumption: a scratch repo with a seeded one-line task is enough.
  Done when: a nightly job enters a worktree via the harness's EnterWorktree path, runs a seeded task through prove and close, and fails the doctor line if any worktree-bound verb breaks.

- **Fail finish when .sampo files would be committed** — CLEAN — value 2 — effort S — risk low — category: hygiene
  Why: Materialised context and outbox files in the worktree can leak into the builder's commit. Assumption: `info/exclude` is per-worktree writable.
  Done when: finish refuses a diff that contains any `.sampo/` path and names the file. A test commits one on purpose and sees the refusal.

- **Wild: Message the parent from the worktree with `fm whisper`** — FEATURE — value 3 — effort M — risk low — category: agents
  Why: Assumption: a builder blocked by the sandbox needs a channel that always works, and a file drop inside its own tree always does.
  Done when: `fm whisper "lease denied, need token"` writes a file in the worktree. The parent's next tick shows it in `fm next` and can answer by writing a reply file the builder reads.

- **Wild: Pack a lane as a capsule and resume it on another machine** — FEATURE — value 3 — effort L — risk med — category: resume
  Why: Assumption: if all of a builder's state lives in the worktree plus git refs, a dead terminal stops mattering.
  Done when: `fm lane pack T-id` yields one bundle (branch, outbox, context, handoff note). `fm lane unpack` on a clean clone resumes with the same Next line.

- **Wild: Let a ghost builder try to close a task from inside a worktree with no real work** — SECURITY — value 3 — effort M — risk low — category: done-gate
  Why: 6 false dones are unchanged since gen 2, and a worktree changes where evidence is read from, which may open a new false-done path. Assumption: a scripted adversary is enough to find such a path.
  Done when: a test agent in a linked worktree tries to close a task using stale, copied, or main-checkout evidence. Every attempt is refused, and any success files a regression scenario.

- **Wild: Have a builder write one "where I stood" line before every risky call, and replay it after a kill** — FEATURE — value 3 — effort S — risk low — category: resume
  Why: Assumption: resume fails mostly on lost intent, not lost state.
  Done when: a kill-test at each step of a scripted task ends with the resumed builder's first action matching the last line written.

Next question: Which worktree-bound verbs have never once succeeded from a harness-made worktree, and does any ledger record the attempt?
Next question: When the harness deletes a worktree on exit, what in it, besides commits, had no copy anywhere else?
