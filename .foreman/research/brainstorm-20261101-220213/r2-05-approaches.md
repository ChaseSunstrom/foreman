# Brainstorm — lens: approaches

Lens: approaches. The mission is to fill 61 empty "staying lean and safe" coverage cells across 8 stages and 8 surfaces. The distinct ways to do that, best first, are below. Earlier rounds covered many individual lean/guard ideas, so these are about how to fill the grid.

- **Derive cells from probes, not prose** — FEATURE — value 5 — effort M — risk low — category: coverage
  Why: the steers say a cell counts only if it names a concrete capability grounded in a file or a real gap, with no templated phrasing. A probe emits real numbers per surface (hook p95, bytes injected, guard deny-class hit). `fm genesis coverage --probe` writes each cell from that output. Hand-written cells get flagged as templated.
  Done when: running the probe on the 61 cells yields 61 distinct cell texts, each citing a command output or file path, and the templating lint passes.

- **Mark most cells n/a by rule, with a recorded reason** — CLEAN — value 4 — effort S — risk low — category: coverage
  Why: the steers allow "a recorded n/a". Examples: "learn × site", "plan × MCP". Doing less beats inventing 61 capabilities, and it stays consistent with "subtract as you add".
  Done when: every n/a cell carries a one-line reason, and a test shows each n/a cites a surface or stage property rather than a reused phrase.

- **Fill cells by pointing at existing features** — CLEAN — value 4 — effort S — risk low — category: coverage
  Why: the pack shows `fm doctor` hook p95, `fm cost`, `fm burden --by-verb`, `fm friction`, and the guard corpus all exist. Many cells (operate × CLI, verify × headless) likely map to these with no new code.
  Done when: each mapped cell names a verb that exits 0 on a fixture, and `fm genesis sweep` counts it as covered.

- **Use one lean budget file as the single source for all cells** — FEATURE — value 4 — effort M — risk med — category: lean budget
  Why: the idea list suggests per-surface byte and latency budgets. A single `lean-budget` file with one row per surface × stage, checked by CI, makes a cell a budget line and keeps cells from duplicating each other.
  Done when: a test fails when a surface exceeds its row, and the file's rows map one-to-one to filled cells.

- **Reuse the existing guard corpus as the safety proof for every surface** — FEATURE — value 5 — effort M — risk low — category: guard
  Why: the pack shows the guard blocks `core:interpreter-code-driving-foreman` 42x, with 2 brief-guard false positives. A deny-class matrix that replays one corpus across Claude Code, fm code, Codex, Gemini, opencode and MCP fills the "safe" half of many cells with one asset.
  Done when: `fm guard matrix` prints surface × deny-class with pass/fail, and the 2 false positives are fixed with regression tests.

- **Fix the brief-guard false positives first** — FIX — value 4 — effort S — risk low — category: guard
  Why: the pack names 2 false positives, a dict key and a `.join(` call read as written paths. They are evidence-backed and cheap, and they fill the "build × Claude Code" safety cell honestly.
  Done when: the two inputs pass the brief guard, and the red-first tests fail on the old code.

- **Shrink the SessionStart note to a hash plus delta** — PERFORMANCE — value 4 — effort M — risk med — category: context
  Why: the note is about 2k chars × 89 sessions, and context per reply averages 387k. A delta fills "understand × all surfaces" with a measured saving.
  Done when: the second-and-later injection in one session is under 300 chars, and `fm cost` shows the average dropping.

- **Cold-shelve unused stack cards** — CLEAN — value 3 — effort S — risk low — category: subtraction
  Why: only 5 of 1219 cards are used. Moving the rest to an on-demand index pays for new growth under the "subtract as you add" rule, and it fills "find × CLI".
  Done when: the installed footprint drops, and `fm lib show NAME` still resolves a cold card.

- **Get the grid status from a pending-growth ledger, not red rows** — FEATURE — value 3 — effort S — risk low — category: sweep
  Why: T-2503 says growth with no measurement yet is "pending", not red. Cells filled under a pending measurement should be listed as such and not block the sweep.
  Done when: the sweep prints covered, n/a and pending counts, and the sum is 61 more than before.

- **Wild: Prove leanness by an eject round trip** — FEATURE — value 3 — effort M — risk med — category: lean proof
  Why: assumption: "leave no trace" is claimed but unchecked. Install, work a fixture task, eject, and diff the filesystem. The result fills the "ship × Desktop" and "operate × headless" cells.
  Done when: the round-trip diff is empty apart from a listed set of paths.

- **Wild: Run the exam with all optional hooks off** — FEATURE — value 4 — effort M — risk med — category: lean proof
  Why: this answers whether the weight earns its keep, using the free arms and no session spend, which respects the exam-deferral steer.
  Done when: a report shows per-hook pass delta and p95 cost, and any hook with no delta is queued as a subtraction candidate.

- **Wild: Let a tool-less child invent the 61 cells blind, then diff** — FEATURE — value 3 — effort S — risk low — category: coverage
  Why: the steers want signals Foreman didn't author. A child that never sees the code proposes cells, and the overlap with the hand-filled ones shows which are real.
  Done when: the diff lists the cells only one side named, and each is either adopted or recorded as n/a with a reason.

- **Wild: Print a weekly "what the guard stopped" note in plain words** — FEATURE — value 3 — effort S — risk low — category: operate
  Why: the 42x block count exists but is invisible to the user. It fills "operate × Desktop" and "learn × CLI".
  Done when: `fm night`'s digest includes one paragraph with the top blocked class and its safe alternative.

Next question: Which of the 8 surfaces has no way to measure its own hook or context cost today, so that its cells can only be n/a?
Next question: Does the templating lint run before a cell is written, or only at sweep time, and which 61-cell phrasing would it wrongly pass?
