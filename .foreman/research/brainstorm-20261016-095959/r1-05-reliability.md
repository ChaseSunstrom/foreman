# Brainstorm — lens: reliability

- **Wrap every model call in a slot-schema validator with bounded repair** — FEATURE — value 5 — effort M — risk low — category: agent loop
  Why: the planner note says small models succeed only if the harness fills the loop and the model fills small structured slots; that fails unless malformed output is caught deterministically. Assumption: Foreman Code has its own loop.
  Done when: a test feeds a fake model 3 malformed replies (bad JSON, missing field, wrong enum) then a valid one, and the loop records 3 repair attempts and proceeds; a 4th failure marks the task blocked with the raw replies saved.

- **Make the guard a mandatory choke point for every worker, with a fail-closed self-test** — SECURITY — value 5 — effort M — risk med — category: guard
  Why: "the guard must never fail open"; codex/gemini/opencode adapters are unverified (T-0336, T-0337 blocked, Gemini Stop not wired). Orchestrated CLIs can bypass hooks silently.
  Done when: `fm agents verify NAME` fires a canned forbidden command through each installed adapter and fails loudly if it is not refused, and a worker whose guard probe fails is not given tasks.

- **Add a worker health-probe and circuit breaker per backend** — FEATURE — value 4 — effort M — risk low — category: orchestration
  Why: assumption: multiple backends (claude, codex, Ollama, OpenRouter) will flake, rate-limit or hang; T-0831 already shows capped children losing partial results.
  Done when: a fake backend that times out 3 times is marked open, tasks route to the next backend, and it is retried after a cooldown, all visible in `fm agents status`.

- **Journal every agent-loop step so a crashed run resumes exactly** — FEATURE — value 5 — effort M — risk med — category: recovery
  Why: T-0798 (recovery, crash-loop quarantine, replay) is deferred, and `fm release --resume` shows the user wants checkpointed resumption. A local-model process dies often.
  Done when: killing the loop with SIGKILL mid-edit and rerunning `fm run --resume` completes the task without redoing finished steps or double-applying an edit (test asserts the file content).

- **Record and replay model sessions as deterministic fixtures** — FEATURE — value 4 — effort M — risk low — category: testing
  Why: the pack's gates run with no real model, so the new loop needs cassette tests; `fm replay` and guard_cases.jsonl already establish the replay idiom.
  Done when: `fm code --record` saves the request and response stream, and `fm replay` re-runs it offline with no network and byte-identical tool calls.

- **Build a capability-conformance suite that grades any model before it gets work** — FEATURE — value 4 — effort M — risk low — category: eval
  Why: the user wants small local models to be "super good"; the unknown is which ones can follow slots, so assumption: a 10-case probe sets each model's autonomy tier.
  Done when: `fm model probe URL` runs the cases against an OpenAI-compatible endpoint and writes a tier (e.g. slots-only, edit-capable) that `fm run` honors.

- **Make every edit atomic with a checkpoint and one-command rollback** — FIX — value 4 — effort S — risk low — category: safety
  Why: T-1195 and the "already dirty files" ask show uncommitted user work is at risk; a weaker model raises the chance of damaging it.
  Done when: a test makes a model edit then fail verification, and `fm undo` restores the tree byte-for-byte, including the user's pre-existing dirty files.

- **Detect model loops and stalls and break them deterministically** — FEATURE — value 4 — effort S — risk low — category: agent loop
  Why: assumption: small models repeat the same call; the existing Stop drive has no counterpart for a model's own loop.
  Done when: a fake model issuing the same tool call 4 times triggers a forced replan or escalation to a stronger model, logged as a `stall` event.

- **Fail the gate when a criterion's verify command can't run** — FIX — value 3 — effort S — risk low — category: gates
  Why: T-1208 and the steer on test_lease: criteria that name a nonexistent module silently weaken verification.
  Done when: `fm task add` and `fm check` reject a criterion whose test path is missing, with a message naming the file.

- **Wild: Run a shadow-model audit that re-derives every "done" claim independently** — FEATURE — value 4 — effort L — risk med — category: verification
  Why: wild; a second, different model re-runs the evidence commands and diffs the outcome, so one model's confident lie can't close a task.
  Done when: a task closed with a faked evidence line is reopened by the shadow check, with the mismatch shown.

- **Wild: Chaos mode that injects failures into the harness itself** — FEATURE — value 3 — effort M — risk low — category: resilience
  Why: wild; `fm chaos` randomly kills workers, truncates replies, and delays hooks past 300 ms to prove the loop and the fail-closed guard survive.
  Done when: a 50-run chaos session ends with zero guard fail-opens and zero corrupted state files, per the report.

- **Wild: Checksum and signed-seal the state ledger so tampering is detectable** — SECURITY — value 3 — effort M — risk low — category: integrity
  Why: wild; "fm is the only state writer" is a convention, so a hash chain over events would catch a model editing state files directly.
  Done when: hand-editing one ledger line makes `fm doctor` fail naming the first broken entry.

- **Pin and sandbox the worker environment per lane** — SECURITY — value 4 — effort M — risk med — category: isolation
  Why: T-1196 and T-1203 show builders drifting into the main checkout or reading the wrong worktree; other CLIs will do the same.
  Done when: a lane worker attempting to write outside its worktree is refused by the guard and the attempt is logged.
