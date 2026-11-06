# Brainstorm — lens: user value

- **Show what the guard saved me, in plain words** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: guard blocked `interpreter-code-driving-foreman` 42x in 7 days, yet the user never sees a story of it; two brief-guard false positives (dict key, `.join(`) read as paths. Staying "safe" is invisible value.
  Done when: `fm doctor` prints a "guard, last 7 days" block listing each block as one line (what was attempted, the safe alternative), and a test feeds the 42-block fixture and sees 42 lines grouped by rule.

- **Fix the two brief-guard false positives and keep a corpus** — FIX — value 4 — effort S — risk low — category: guard
  Why: measured: dict keys and `.join(` calls read as written paths. Each false block costs the user a stop.
  Done when: both strings pass the guard, and a corpus file of real past inputs (blocks and passes) runs in `fm check` with zero regressions.

- **Cap context per reply with named top contributors** — PERFORMANCE — value 5 — effort M — risk med — category: lean
  Why: 387k average context per reply over 5735 replies; SessionStart note ~2k chars x 89 repeats. The user pays this in cost and slowness; nobody can say which source dominates.
  Done when: `fm cost --by-source` prints bytes per injected block per reply, and the SessionStart note after the first turn is a hash-plus-delta of under 300 chars (test asserts it).

- **Pay for every new verb with a deletion** — CLEAN — value 4 — effort M — risk med — category: lean
  Why: gen-0 §6 requires subtraction; T-2503 left growth pending until measured; 1219 stack cards with 5 used.
  Done when: `fm check` fails a task adding a verb unless the same task retires one (or names an existing unused verb), and the 1214 unused cards move to a cold index that loads on demand with a test showing session start loads none of them.

- **Fill the 61 empty coverage cells from probes, not prose** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: the mission is exactly this; the standing rule says templated cells don't count. Each cell should cite a measured number or a file.
  Done when: `fm genesis sweep` reports 0 empty cells for #12 and a lint test rejects any two cells with the same sentence after swapping the area word.

- **Prove the guard fires on every surface (deny-class matrix)** — FEATURE — value 5 — effort M — risk med — category: safety
  Why: surfaces are Claude Code, fm code, Codex, Gemini, opencode, MCP, Desktop, headless; T-0335/0337 show Gemini/Codex gaps (Gemini Stop unwired). The user's bypass-mode safety claim is only as strong as the weakest surface.
  Done when: `fm doctor --guard-matrix` prints a surface x deny-class table with pass, fail or "no hook" per cell, and a gap shows red with the task id.

- **One lean line in `fm doctor`** — FEATURE — value 3 — effort S — risk low — category: lean
  Why: p95 278 ms, 387k context, 89 notes: the user must run three commands to learn them.
  Done when: `fm doctor` ends with `lean: hook p95 Xms · ctx Yk/reply · verbs N · cards used a/b` and each figure matches its producing command in a test.

- **Name the slowest hook and why** — PERFORMANCE — value 3 — effort S — risk low — category: hooks
  Why: p95 278 ms over 13533 runs with no attribution.
  Done when: `fm friction` lists the top 3 hooks by p95 with the event and the dominant step, verified against `bench_hooks.py` output.

- **Wild: Hostile-week replay** — FEATURE — value 4 — effort L — risk med — category: guard — wild
  Why: assumption: replaying a week of real hook inputs plus child-authored evasions against any proposed guard change shows both false blocks and bypasses before it ships.
  Done when: `fm guard replay --candidate RULES` prints newly blocked, newly allowed, and bypassing inputs, and fails on any new bypass.

- **Wild: Lean twin** — FEATURE — value 4 — effort L — risk med — category: lean — wild
  Why: assumption: the user can't tell what the hooks earn. Run the same held-out task with Foreman's optional hooks off and on, comparing cost, time and pass.
  Done when: `fm exam lean-twin` prints a per-hook cost/pass delta and names hooks whose removal changed nothing.

- **Wild: Delete-a-feature Friday** — CLEAN — value 3 — effort M — risk low — category: lean — wild
  Why: assumption: deferred bundles (28 "Later from T-07xx") and rarely used verbs accumulate; a weekly lottery proposes the least-used for removal.
  Done when: `fm burden --propose-delete` lists 5 candidates with last-used dates and one-command soft retirement into `fm lab`, reversible by test.

- **Make the guard's "no" teach the safe command** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: 42 repeated blocks mean the model keeps retrying the same shape; the block text apparently doesn't prevent recurrence.
  Done when: each block message includes one runnable safe alternative, and repeat blocks of the same rule per session drop in a replay of the logged 42.

Next question: Which of the 61 empty cells are surfaces (MCP, Desktop, headless) where no hook exists at all, so "lean and safe" there must be enforced by something other than a hook?
Next question: What does the user actually do when a guard block happens: override, rephrase, or give up, and does any log show it?
