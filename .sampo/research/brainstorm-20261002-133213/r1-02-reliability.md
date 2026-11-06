# Brainstorm — lens: reliability

- **Enforce gates in-process via tool.call, with classic-hook fallback** — FEATURE — value 5 — effort M — risk med
  Why: Known limitation: "only gates are enforced" and Bash edits are invisible to scope/tripwires because only Edit/Write hooks see them. A mod `tool.call` sees every tool call, including Bash, before it runs.
  Done when: a mod test shows a Bash `sed -i` on an out-of-scope file is denied or recorded as a scope event, and the same session under `claude -p` still passes through the classic hooks unchanged.

- **Make hook failure fail-safe and visible** — FIX — value 4 — effort S — risk low
  Why: Every event spawns a Python process (p50 ≈ 29 ms). Assumption: a crash or timeout in fmhooks currently either silently allows or blocks, and nothing tells the user which. The pack mentions `fm doctor` but no hook-error ledger.
  Done when: a unit test injects an exception into each of the 13 hooks. The guard hooks fail closed, the advisory hooks fail open, and each failure writes a ledger event that `fm doctor` reports.

- **Fix T-0075/T-0076/T-0080 so state round-trips losslessly** — FIX — value 4 — effort M — risk low
  Why: `task set --section` drops the evidence↔criterion link, `show --json` omits criteria, steps and depends, and `--section Approach` creates a duplicate section. A mod UI built on `fm --json` would read incomplete state, and drive mode would trust it.
  Done when: a round-trip test (set section → show --json → compare) preserves criteria, links, steps and depends, and section aliases resolve to the canonical name.

- **Scope audit and security triggers to the task's own diff** — FIX — value 4 — effort M — risk med
  Why: T-0078/T-0079 show these checks look at the whole tree. False positives block "done", and T-0074 shows sensitive() flagging Foreman's own regex literals. Repeated false blocks teach users to bypass the gates.
  Done when: with an unrelated dirty file in the tree, the gates pass. Touching a sensitive path inside the task still trips them, and a test covers both cases.

- **Add a schema version and atomic writes with a crash-recovery test for the record** — FIX — value 4 — effort M — risk low
  Why: The single per-project record of markdown briefs, cached line files and the ledger is written from many short-lived processes. With mods in-process alongside the CLI, concurrent writers become more likely. Assumption: writes aren't yet atomic and locked everywhere.
  Done when: a test kills a writer mid-write and runs two concurrent writers, the record stays parseable, and `fm doctor` detects and repairs a torn file.

- **Define a mod/classic handoff so events aren't double-handled** — FEATURE — value 5 — effort M — risk med
  Why: Mods are additive, and `classic.<Event>` observes the same settings hooks. If both the mod and the classic hooks inject "Next:" or enforce gates, the effects duplicate or conflict. Assumption: no coordination exists yet.
  Done when: a session with the mod loaded shows each gate and "Next:" injection firing once, via a state flag the classic hooks check. The same test with the mod absent shows the classic path active.

- **Expose a `fm state --json` snapshot contract and test the mod against it** — CLEAN — value 3 — effort S — risk low
  Why: Mods must call `fm` through `$.process.run`, so the mod UI depends on CLI output shape. T-0076 shows that shape has already drifted. `claude plugin test` supports mocked processes.
  Done when: a versioned JSON schema is checked in, a Python test validates the CLI output against it, and a `*.test.ts` mounts the pane using the same fixture.

- **Make `fm check` timeouts and environment failures distinguishable** — FIX — value 2 — effort S — risk low
  Why: T-0081 notes the timeout message is unclear, and the previous round added environment failure labels. A timeout is currently easy to mistake for a test failure, which wrongly blocks evidence recording.
  Done when: a test with a sleeping command yields a "timeout" status distinct from "failed", with a message naming the limit, and the status is not recorded as red evidence.
