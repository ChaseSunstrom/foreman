# Brainstorm — lens: relay race (invented): a fresh session with zero memory must resume mid-goal exactly; the plan on disk is the only memory

**Answers to earlier questions (relay lens):**
- Stage-level blame needs a per-stage checkpoint file, as the Initiative pipeline would need for `fm find step`. A killed run then resumes at the exact stage, and a regression is blamed on the stage whose checkpoint changed.
- A crashed hunt must score as an error, not as "none". The leg that died must leave a typed stop record the next leg reads.

**Ideas:**

- **Pin `fm goal step` as a pure function of files** — FIX — value 5 — effort M — risk low — category: determinism
  Why: the pack says the plan on disk is the only memory, and "step" is read-only. Nothing proves two fresh processes agree. Locale, HOME, cwd, clock or dict order could change the "next action" between legs.
  Done when: a test runs step in two fresh `python3 -I` interpreters with different env, cwd and faked clock over one frozen goal dir, and the outputs are byte-identical.

- **Record each criterion's input footprint and re-verify only stale ones on resume** — PERFORMANCE — value 4 — effort M — risk med — category: resume speed
  Why: assumption: re-proving every "done" item at resume costs the full verify suite per session. At ~4400 tests, a fresh leg would burn minutes on unchanged work.
  Done when: evidence stores a hash of the files each verify command read, and a resume after touching one file re-runs only the criteria whose footprint includes it. A test asserts the others are skipped and still shown as "fresh, hash unchanged".

- **Write the baton behind, so SessionStart only reads** — PERFORMANCE — value 4 — effort M — risk low — category: hook latency
  Why: hooks must stay fast (bench_hooks gate) and context over ~10 KB turns into a preview. Assembling the goal card at SessionStart means gathering the ledger, briefs and map under the gate.
  Done when: Stop and PreCompact write a ready-to-inject card (≤10 KB, stamped with tree identity). SessionStart does one file read plus a staleness check, and a bench shows it under the gate with a 200-event ledger.

- **Add a tail index so resume never replays the whole hash chain** — PERFORMANCE — value 3 — effort M — risk med — category: ledger scale
  Why: goals span days, so the ledger grows. Reading from the start on every resume is O(history). Sealed epochs are a separate idea, and this one is only an offset sidecar.
  Done when: a sidecar of offsets plus the last verified hash lets resume read only the tail. `fm goal check` still verifies the full chain lazily, and a corrupted sidecar falls back to a full read with a warning.

- **Gate the resume bench: time to first correct action** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: the exam grades outcomes, not how fast a cold session gets productive. A baton that is correct but bulky costs real tool calls.
  Done when: a goal-resume exam scenario records the tool calls and tokens a fresh arm needs before its first edit on the true next step. The score is compared against a stored baseline, and a regression fails the scenario.

- **Take steers from a synced drop folder** — FEATURE — value 4 — effort S — risk med — category: devices
  Why: the user is autonomous-run oriented and never asked mid-run, but they steer by text. Phones can already write a text file to any synced folder (Syncthing, iCloud and so on), which needs no server and fits local-first. Assumption: a path is configurable.
  Done when: a file dropped in `goal/inbox/` is journaled at the next UserPromptSubmit or step as quoted data (`c.plain`), then moved to `seen/`, and never executed as an instruction.

- **Emit a paste-in baton for surfaces with no hooks** — FEATURE — value 4 — effort S — risk low — category: Desktop / other agents
  Why: Desktop and other agents get no SessionStart injection, yet every capability must work on every surface. A self-contained card the user pastes is the floor.
  Done when: `fm goal paste` prints ≤8 KB of plain text with goal, next step, dead ends and the verify commands, and a tool-less child given only that text names the correct next step in an exam scenario.

- **Run a surface relay matrix as a conformance test** — CLEAN — value 4 — effort M — risk low — category: surfaces
  Why: Claude Code hooks, `fm code`, the MCP server, the Codex/Gemini/opencode shims and the pane each build the resume text separately. They can drift.
  Done when: one frozen goal fixture goes through every surface's injection path. A test asserts the same step, same goal id and same progress line appear in each, and a surface that omits one fails.

- **Make the baton portable to another checkout** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: assumption: the user works on a laptop and a desktop, and state lives at an absolute path under `state/projects/<id>`. Hand-off already exists for agents, but not for a different path or commit.
  Done when: `fm goal pack` and `unpack` move the goal with relative paths. Unpack compares tree identity and prints "base differs by N files; steps X, Y need re-check" rather than resuming blind.

- **Add the baton to the statusline and terminal title** — FEATURE — value 2 — effort S — risk low — category: devices
  Why: a pane exists for Claude Code only. Terminal and tmux users, and `fm code`, need a glance at the leg number, next step and distance.
  Done when: `fm goal line` prints one ≤80-char line from files in under the hook gate, and the pane, `fm code` and a documented tmux snippet all use it.

- **Fail over mid-goal to another agent at a usage limit (wild)** — FEATURE — value 4 — effort L — risk high — category: continuity
  Why: relaunch at the reset waits hours. The shims already exist, so when the Stop hook sees a usage limit it could hand the baton to `fm code` or Codex and carry on. The no-self-grant rule applies: it needs an explicit standing grant, so no.
  Done when: with a grant, a simulated limit moves the goal to a second agent. It makes one verified step from the baton, logs a lease takeover, and without the grant it parks with the stop cause recorded.

- **Nudge a wrist or phone when a goal hits a typed wait (wild)** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: autonomy forbids asking mid-run, yet a wait on a grant or a usage reset is where goals stall silently. A notification sends content outward, so it needs a grant, off by default.
  Done when: with the grant set, one notification names goal, wait type and the single command that releases it. Without it, nothing is sent and the pane shows the wait, tested on both paths.

- **Speak the baton as one deterministic sentence (wild)** — FEATURE — value 2 — effort S — risk low — category: voice
  Why: car and voice assistants (a shortcut over ssh) need a brief answer to "where are we on the goal?" that uses no model and no screen.
  Done when: `fm goal say` returns ≤30 words from files only, covering step, progress and any blocker. It is identical across runs and contains no quoted untrusted text.

Next question: What is the largest goal baton a fresh session can absorb and still make a correct first move, and does that limit differ by model tier or surface?
Next question: When two legs disagree on what "done" means for an item, which file settles it, and who checks that file wasn't edited between legs?
