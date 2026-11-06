# Brainstorm — lens: capability map

- **Hook flame budget per event** — FEATURE — value 5 — effort M — risk low — category: performance
  Why: p95 is 278 ms over 13,533 runs, but nothing shows which hook or step spends it. Hyperfine and py-spy do this per call.
  Done when: `fm doctor --hooks` prints per-hook p50/p95 and the top cost step, and fails if one event's summed p95 exceeds a settings budget.

- **Context ledger by injected block** — FEATURE — value 5 — effort M — risk low — category: context
  Why: replies average 387k context and the SessionStart note is ~2k chars x 89. No per-block attribution is shown.
  Done when: `fm cost --context` lists each injected block's bytes per reply and its share, and a test fails when a block grows without a settings bump.

- **Brief-guard false-positive corpus** — FIX — value 4 — effort S — risk low — category: guard
  Why: two false positives read a dict key and a `.join(` call as written paths.
  Done when: both strings are fixtures that the guard allows, and a replay of 7 days of blocks lists any other benign block.

- **Block-reason receipts with the safe alternative** — FEATURE — value 4 — effort M — risk low — category: guard
  Why: `core:interpreter-code-driving-foreman` blocked 42 times in 7 days. Repeat blocks mean the agent doesn't learn the safe path. Semgrep-style rules ship fix hints.
  Done when: each guard deny prints the one runnable replacement command, and the repeat-block count drops in `fm friction`.

- **Dead-verb and dead-card sweeper** — CLEAN — value 4 — effort M — risk med — category: subtraction
  Why: 5 of 1219 stack cards are used, and gen-0 §6 requires subtraction. knip and vulture do this for code.
  Done when: `fm burden --dead` lists verbs and cards with zero calls in 60 days, and moving one to `archive/` is a single reversible command.

- **Lazy card loading with a size cap** — PERFORMANCE — value 4 — effort M — risk med — category: context
  Why: 1219 cards with 5 used suggests most never earn their place, and loading them has a cost.
  Done when: a session that touches no stack loads zero card bytes, and a test asserts the index stays under N KB.

- **Guard rule coverage map** — FEATURE — value 4 — effort M — risk low — category: security
  Why: the guard has a deny list, but nothing shows which rules ever fire, which never do, and which commands pass untested.
  Done when: `fm guard coverage` prints per-rule fire counts plus child-written evasions run against it, with uncaught ones listed.

- **Hook-bypass tripwire across hosts** — SECURITY — value 4 — effort M — risk med — category: security
  Why: Codex, Gemini and opencode have no Stop wiring (T-0337), so the guard may be absent there.
  Done when: `fm doctor` prints a per-host row "guard live: yes/no/unverified", each backed by a probe command that really ran.

- **Lean ratchet in CI with a substance baseline** — FEATURE — value 4 — effort M — risk low — category: ratchet
  Why: T-2503 holds substance growth as pending until a measurement exists, so it never goes red.
  Done when: CI fails on hook p95, injected bytes, verb count or dependency count above the baseline file unless a task id and its measured gain are cited.

- **Dependency and supply-chain diff on ship** — SECURITY — value 3 — effort M — risk low — category: supply chain
  Why: T-0791 lists 18 deferred injection and supply-chain ideas. gitleaks, osv-scanner and Socket cover this, and `fm ship` is the choke point.
  Done when: `fm ship` blocks on a new dependency or a secret-pattern hit in the diff and prints the line.

- **Offline-only mode proof** — FEATURE — value 3 — effort S — risk low — category: privacy
  Why: the standing rule says Foreman works with no `claude` on PATH. Nothing proves it also works with no network.
  Done when: a test run under network namespace isolation passes the core loop (`fm next`, task, check, finish).

- **Wild: Hook cold-start race against a Rust shim** — PERFORMANCE — value 3 — effort L — risk med — category: performance
  Why: wild. The shell prefilter (T-0832) is deferred pending a bench. A compiled or warm-daemon fast path could take p95 below 50 ms with a cold fallback.
  Done when: `bench_hooks.py` shows p95 at least 3x lower, and killing the daemon still lets every hook pass.

- **Wild: Footprint budget as a visible fuel gauge** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. Hook ms, context KB and verb count appear as one bar in the statusline that shrinks when a task deletes more than it adds.
  Done when: the statusline shows the gauge, and a task that deletes code moves it.

- **Wild: Guard red-team lane overnight** — SECURITY — value 4 — effort L — risk med — category: security
  Why: wild. A tool-less child that never sees the guard code writes bypass attempts, replayed against the guard each night.
  Done when: the morning digest lists attempts tried, how many passed, and a failing-first test per bypass.

- **Wild: Forget-a-feature trial week** — CLEAN — value 3 — effort M — risk med — category: subtraction
  Why: wild. Each week one low-use verb is disabled for a trial and auto-restored if a session asks for it.
  Done when: `fm trial-off VERB` disables it, restores it on first demand, and records whether anyone missed it.

- **Per-surface byte allowance in the coverage grid** — DOC/FEATURE (FEATURE) — value 3 — effort S — risk low — category: coverage
  Why: the 61 empty cells include lean cells for Desktop, site, MCP and headless, with no shared way to state "lean" for them.
  Done when: each cell in `coverage.md` names a measurable budget (ms, bytes or count) and the command that reads it.

Next question: Which of the 61 empty cells have a measurement command already, and which need a new probe before they can be non-templated?
Next question: Does any hook cost land on the user's first prompt in a fresh session, and who measures that cold path?
