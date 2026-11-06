# Brainstorm — lens: reliability

Reading the pack for reliability signals: T-2967 (guard misses symlinked real path), T-2966 (loop breaker), T-3185 (core.bare=true leaked into real git config), T-3053 (lane merge failure), CI deploy timeout, T-1217 (pane background), and the user's steer "manage all of that across sessions too... even without direct access... not only one machine." The biggest unspoken reliability need: **the model and the tower are new single points of failure the user will hit at 3am with no one to ask.**

- **Verify the serving endpoint at every session start, before any model call** — FIX — 5 — M — risk low — category: serving
  Why: T-2953/T-2958 show the funnel and exam arms depend on a local endpoint that can be cold, busy, or on the wrong model. `think:false`/`reasoning_effort` not reaching Ollama (user words) means settings silently don't apply. A model that answers as the wrong size or with reasoning on is a silent reliability failure.
  Done when: `samo doctor` runs a canary prompt at start, asserts the returned `model_id`, `reasoning` flag, and a golden token, and prints the verified profile (or "unverified, using rules arm").

- **Fence every decider call with a hard time budget and a typed stall fallback** — FIX — 5 — S — risk low — category: serving
  Why: A local model can hang on a 4B context or OOM mid-token; the pack has no evidence any model slot has a wall-clock bound or a named fallback. Today the drive would just stall (T-3296-class "Sampo shouldn't eat the whole CPU").
  Done when: every `decide()` call returns within a configured budget or emits a typed `stall:<cause>` ledger line and falls back to the rules arm; a test forces a hang and asserts the fallback fired.

- **Never write host git config from Sampo; resolve state via git common dir** — FIX — 5 — S — risk med — category: state
  Why: T-3185: `core.bare=true` leaked into the real `.git/config` and broke every merge. This is exactly the class of "Sampo's self-edit breaks the user's repo" that a reliability lens must catch. Every verb/hook should resolve paths from `git rev-parse --common-dir`, never assume `$PWD/.git`, and never mutate host config.
  Done when: a test runs `samo task finish` and `samo ship` with a polluted/absent `.git/config` and a worktree, and no host-config write occurs (verified by config diff).

- **Reconcile the model registry from disk at wake, not from memory** — CLEAN — 4 — M — risk med — category: state
  Why: The champion/challenger registry and pinned weights (ideas above) assume a persisted source of truth. Across machines ("not only one machine") and after a crash, an in-memory registry can point at a deleted or half-written weight file. Rebuild it from the content-hash manifest on disk at session start; refuse to serve a slot whose pinned hash is missing.
  Done when: killing the process mid-registry-write and restarting yields the last-complete registry (hash-verified), with a ledger line "registry reconciled from disk, dropped N in-flight slots."

- **Two-phase grant spend so a crash can't double-ship or lose a grant** — FEATURE — 5 — M — risk med — category: state
  Why: The user pushes to main "at any time" under the standing push grant, spent "on use." A crash between "decide to push" and "push landed" either loses the grant or, on resume, double-pushes. Make grant spend atomic (reserve → apply → commit, journaled), resumable after SIGKILL.
  Done when: a kill-point sweep SIGKILLs the drive between reserve and apply, resumes, and pushes exactly once with the grant reconciled.

- **Ledger kill-point sweep on every writer** — PERFORMANCE — 4 — M — risk low — category: state
  Why: The whole decider trains on the outcome lake; a torn ledger row on crash silently poisons retraining (a "silent cut" the user explicitly asks to be counted). Run a kill sweep: SIGKILL each writer mid-append in a scratch tree, then verify the reader returns either the last complete row or a tombstone, never a half-row.
  Done when: the sweep over all ledger writers finds zero torn rows readable, and a test asserts a torn append is fenced to the trash.

- **Pin and verify the serving stack by digest, and rehearse "model gone"** — SECURITY — 4 — S — risk low — category: serving
  Why: T-2953/T-2958 and the rename (T-2745) show the endpoint identity is mutable. A model file that changes on disk under the funnel is a silent behaviour change. Verify weight digests before any funnel/exam run, and keep a permanent "no-model" arm so a missing endpoint degrades to retrieval, not a stall.
  Done when: swapping the weight file's digest mid-run fails the funnel loud; pointing the endpoint at nothing routes to the kNN arm with a ledger line.

- **A 3am "Sampo is degraded" card that survives fail-open** — FEATURE — 4 — M — risk low — category: observability
  Why: The user's unattended drive runs with no one to ask. When the Ward, the endpoint, or a hook fails open (the guard over-refusal / fail-open class in the pack), the user is left a week later with a mystery. Print a one-line, persisted "running degraded: <named cause>" at session close and in the morning card, and make fail-open *visible* rather than silent.
  Done when: forcing a hook import failure produces the degraded line in the morning card and a typed stall in the ledger; a "clean" night omits it.

- **Fence the model out of the Ward's decision path; the Ward stays rule-based and the model may only tighten** — SECURITY — 5 — S — risk low — category: safety
  Why: A trained risk head in the guard's hot path is a new failure mode: a wrong model verdict either blocks safe work (T-2967-class over-refusal, now model-induced) or, worse, allows a refused command. Keep the Ward deterministic; let the model only add *tightening*, with every model-tightened block attributed and reversible.
  Done when: a test drives a poisoned model to "allow" a Ward-refused command and the Ward still refuses; a model-tightened block logs which model clause fired and reverts when the model is disabled.

- **Hold "done" as provisional and re-run the close-holds proof from a cold worktree** — FIX — 5 — M — risk med — category: reliability
  Why: The first decider slot the pack implies is "will this close hold?" (T-0035, T-0217, the distil-from-verified-runs asks). A close that passes now but reverts in 14 days is the false-done the user has to catch by hand. Run the close verifier again on a fresh worktree after a delay; flip the verdict and file the regret as a training row.
  Done when: closing a task whose later-committed change breaks its own test flips the ledger to "reverted" and emits a regret row; the web UI shows proven vs. provisional distinctly.

- **Detect model drift per slot from live agreement, and alarm on silent divergence** — FEATURE — 4 — M — risk med — category: observability
  Why: With many slots and per-project adapters, a slot can silently degrade (the "measured wrong" class in the cross-cutting cold review). Track agreement between the model slot and the rules arm on the same inputs; a drop below floor files a regression task and, per the standing rule, runs the full arm for that capability.
  Done when: injecting drift into one slot (swap its weights) is detected within a generation, filed, and the morning card names the slot and the delta.

- **wild — A "pull-the-plug" drill: a scheduled random SIGKILL of the live drive on a scratch repo, every ship** — FEATURE — 4 — M — risk low — category: reliability
  Why: The user's words ("even without direct access," "not only one machine") mean the drive will die in ways no test covers. A standing, *randomized* crash drill — kill the drive at a random tick on a scratch repo, resume, and assert the queue, grants, and registry reconcile — catches the torn-state bugs the deterministic tests miss. This is the "reboot rehearsal in a throwaway VM" the earlier pack gestured at, made permanent and cheap.
  Done when: each ship runs one randomized-kill drill on a scratch clone; a failure blocks the ship and files the resume bug; a clean resume is logged with the kill point.

- **wild — Keep a frozen "last-good Sampo" twin that over-rules by strictness when the live build fails a canary** — FEATURE — 4 — L — risk med — category: safety
  Why: A self-edit to the guard, hook, or injection (Sampo edits Sampo nightly) can silently break the discipline loop — T-2967 is exactly a self-introduced regression. Keep an out-of-tree, hash-pinned frozen twin of the last-verified guard + hook set; if the live set fails its own canary at start, fall back to the twin and file the regression, rather than running degraded.
  Done when: mutating the live hook set to be permissive makes the canary fail, the twin takes over the guard path, and the morning card names the broken commit; rolling forward restores the live set.

- **wild — A "Sampo is gone" morning: once a week, disable the entire decider and model layer for one live session and log every ask the user had to make** — FEATURE — 3 — M — risk low — category: observability
  Why: The reliability question that matters to *this* user is not "does the model work?" but "does the user even need it, and does the machine hold up without it?" (Their standing lean rule and the "Sampo's last day" themes.) A scheduled ablation produces the ground truth for the model's marginal value *and* exercises the no-model fallback path in production, on the user's real work. It is the honest reliability test for "it improves every Rune generation."
  Done when: a weekly session runs with the model layer off; the ledger records every ask, fallback, and stall the user hit; the morning card prints "Sampo-less: N asks, M stalls," feeding the model's retirement probe.

Next question: Which of the new failure surfaces — the model endpoint, the grant push, or the guard self-edit — does the user most *fear* hitting at 3am, so I can set the first alarm on the one that would actually wake them?
Next question: When the decider abstains or falls back, does *any* slot currently leave a ledger trace the user can find, or is there a silent path (like the model endpoint degrading) that the "measure the fallback" bench still can't see?
