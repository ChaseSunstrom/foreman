# Brainstorm — lens: bold bets

- **Run Foreman on a weight budget enforced by deletion** — FEATURE — value 5 — effort L — risk med — category: lean
  Why: Measured p95 278 ms over 13533 hook runs, 387k context per reply, 5 of 1219 cards used; gen-0 §6 says each generation must subtract at least what it adds.
  Done when: `fm lean` prints one budget (hook p95, injected bytes, verb count, cards, lines); a new verb fails `fm check` unless the same task deletes or merges one; the check passes on a seeded repo.

- **Ship a hot-path guard as a startup-free binary with a Python fallback** — PERFORMANCE — value 4 — effort L — risk high — category: hooks
  Why: Hook p95 is 278 ms; the guard runs on every tool call. Assumption: interpreter startup dominates, which `bench_hooks.py` can confirm.
  Done when: `bench_hooks.py --runs 20` shows guard-event p95 under 50 ms, and a differential test of the guard corpus gives identical allow/deny verdicts on both implementations.

- **Attribute every reply's context to its source** — FEATURE — value 5 — effort M — risk low — category: context
  Why: 387k average context per reply and a SessionStart note of ~2k chars × 89 are measured, but nothing says which block earns its bytes.
  Done when: `fm cost --by-source` lists bytes per injected block (note, steers, lessons, skills, MCP schemas) over the last N replies, and the sum matches the total within 2%.

- **Withhold one injected block per session and compare outcomes** — FEATURE — value 4 — effort M — risk med — category: lean substance
  Why: T-2503 says growth with no measurement waits, but no capability has an ablation arm. Assumption: outcomes from `fm outcomes` are enough signal at N≥30.
  Done when: a seeded run withholds a random block, records it, and `fm lean --ablation` reports per-block held-rate difference with an interval; a block with no measured gain is listed as a deletion candidate.

- **Move unused stack cards and skills to a cold shelf loaded on demand** — CLEAN — value 4 — effort M — risk low — category: library
  Why: `fm lib stats` shows 5 of 1219 cards used; 1388 files sit under plugin/skills.
  Done when: cards unused for 90 days move to a cold index, `fm lib show NAME` still resolves them, the install size drops measurably, and no existing test regresses.

- **Fix the brief-guard path false positives with a corpus** — FIX — value 3 — effort S — risk low — category: guard
  Why: Two false positives read a dict key and a `.join(` call as written paths.
  Done when: both strings are in a committed false-positive corpus, the guard allows them, and the real-block corpus still denies all prior cases.

- **Replay a week of logged guard decisions against every candidate rule change** — SECURITY — value 5 — effort M — risk low — category: guard
  Why: The `core:interpreter-code-driving-foreman` rule blocked 42× in 7 days; any rule edit risks silently loosening the guard that bypass mode relies on.
  Done when: `fm guard replay --candidate` prints every verdict that flips against the log, and a change that flips a prior deny to allow fails the gate.

- **Prove the guard fires on every surface with a deny-class matrix** — SECURITY — value 5 — effort M — risk med — category: guard
  Why: The empty cells span Claude Code, Codex, Gemini, opencode, MCP, Desktop and headless; T-0335/T-0337 show host hooks differ and some paths (Gemini Stop) aren't wired.
  Done when: `fm guard matrix` runs each deny class on each installed host and prints allowed/denied/not-wired; every not-wired cell is an honest labelled gap, none blank.

- **Kill the SessionStart note after the first turn: inject a hash and a delta** — PERFORMANCE — value 4 — effort S — risk low — category: context
  Why: ~2k chars repeated across 89 sessions measured; unchanged state is re-sent.
  Done when: a second turn with unchanged state injects under 200 bytes, and a changed state injects only the changed lines; a test asserts a standing rule is never truncated.

- **Wild: Run an overnight "lean twin" that does the same task with Foreman's hooks off** — FEATURE — value 4 — effort L — risk med — category: lean proof
  Why: wild; assumption: the duel harness (T-1231) can run a matched pair, and only a twin shows what the weight actually buys in cost and time.
  Done when: a morning card shows cost, time and pass for foreman vs bare on N replayed tasks, labelled Haiku-smoke, not final.

- **Wild: Plant a harmless forbidden command weekly to prove the guard is alive** — SECURITY — value 4 — effort S — risk low — category: guard liveness
  Why: wild; a guard that silently stopped firing after a host update looks identical to one with nothing to block.
  Done when: a canary command is blocked in each host session once a week, and `fm doctor` goes red if any canary passes through or isn't attempted.

- **Wild: Hold a monthly lean court that tries to delete the least-used 5% of verbs** — CLEAN — value 4 — effort M — risk med — category: subtraction
  Why: wild; `fm burden --by-verb` exists and §6 demands net subtraction, but nothing proposes the deletions.
  Done when: the court files one task per candidate verb with its use count and a one-command restore; the user approves, and a soft-moved verb to `fm lab` still runs.

- **Wild: Prove "leave no trace" with an install-then-eject round trip** — FEATURE — value 3 — effort M — risk low — category: safety
  Why: wild; T-0794 mentions eject and fuses but the lean/safe claim has no observable proof.
  Done when: install, run a task, eject in a scratch HOME leaves a file diff of zero outside the user's own repo changes.

- **Charge MCP tool schemas and skill descriptions to the context budget** — PERFORMANCE — value 3 — effort S — risk low — category: MCP
  Why: The MCP and skills cells are empty; schemas load every turn like the note. Assumption: schema bytes are a noticeable share of the 387k.
  Done when: the source attribution lists MCP schema bytes, and a budget test fails if they grow without a matching cut.

Next question: Which of the 61 empty cells are n/a by nature (e.g. "operate" on a static site) and which are real gaps hiding behind that label?
Next question: What does the guard do on a host that has no hook API at all, and who is told?
