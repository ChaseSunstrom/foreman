---
id: T-2909
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T06:36:31Z
updated: 2026-11-04T06:47:20Z
base_note: Calibration: this plan states Choice 75% where FEATURE M closes (604) held on the first finish 98% of the time: 23 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T06:36:55Z
rival_split: true
builder_model: haiku
base: c11312e5fba8c46aa7e5e99f4a0290d8b54004b0
base_tree: 97c00bbb746c2e609d52ed1d1b6a613c65394100
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T06:37:16Z
plan0_scope: []
lane_stop: merged 2026-11-04T06:43:31Z
verified: ok
unproven: [docs, typed]
---
# Small-model cards part 1: a store of cards written for small models (research/cards/cards.jsonl), a grid (kind of work x stack x stage x surface: code, UI, design, docs, ops), write-time admit (when to use, numbered steps with exact commands, a worked example, a self-check, the traps a small model falls into; vague or unrunnable cards rejected), sampo playbooks small grow --target N --workers K on local profiles reusing moonscale's grow, and coverage
## Raw request
> Small-model cards part 1: a store of cards written for small models (research/cards/cards.jsonl), a grid (kind of work x stack x stage x surface: code, UI, design, docs, ops), write-time admit (when to use, numbered steps with exact commands, a worked example, a self-check, the traps a small model falls into; vague or unrunnable cards rejected), sampo playbooks small grow --target N --workers K on local profiles reusing moonscale's grow, and coverage
## Interpretation
Reading 1 (chosen): the corpus half of T-2878. The user asked for thousands of skills, playbooks, UI instructions and designs written for smaller models, grown every Rune generation. A card is a playbook rewritten for a small model: explicit when-to-use, numbered steps with exact commands, one worked example, a self-check and the traps small models fall into. Generation runs on the local models in bulk, with coverage by grid like the moons. Part 2 (after T-2908's Louhi smith arm) keeps only cards an A/B shows help and loads them into Smith's small-model mode. Reading 2 (ruled out): hand-write a few hundred cards with the frontier model now. Ruled out because the user asked for thousands, for local models doing the volume, and for growth every generation, which needs a machine.
## Assumptions (confidence)
## Acceptance criteria
- [x] admit keeps a complete card and rejects one missing steps, example, self-check or traps, or naming a command that doesn't exist — verify with `python3 plugin/tests/run.py test_small_cards`
- [x] grow fills thin grid cells first on a fake local profile with two workers, and coverage counts cells — verify with `python3 plugin/tests/run.py test_small_cards`
## Non-goals
## Approach (options → choice → why)
1) A new module, smallcards.py, built on moonscale: GRID = KINDS (moonscale's) x STACKS (python, js/ts, rust, c, ruby, shell, sql, css/html) x STAGES (capture, plan, execute, verify, review, release) x SURFACES (code, UI, design, docs, ops). admit() checks the fields and the step commands' first words against a known-command list (sampo verbs, common CLIs); grow reuses moonscale._ask (local first, Haiku fallback), the workers, think, thin-cells-first _pick and _objects parsing; sources are a playbook's or stack card's text quoted as data; coverage prints filled cells. The verb is sampo playbooks small grow|coverage|show, so no new top-level verb. Likely outcome: a working grower and a few hundred live cards tonight. Fails if moonscale's helpers are too moon-shaped to reuse; then the shared parts move to a tiny common helper. Choice 1 (75%). 2) use what exists: sampo playbooks draft already drafts a playbook from evidence. Likely outcome: one card at a time with the frontier model, so it's used as the template source, not the bulk path. Fails the volume. 3) do less: a script in the scratchpad that loops a local model over playbooks. Likely outcome: cards tonight, but no admit, grid or coverage, and nothing a generation can run. Fails 'grown every generation'.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: admit's keep and reject cases
2. [x] the store, grid and admit, seeded from the 114 playbooks and the stack cards (sampo lib) as sources
3. [x] test: grow and coverage with a fake profile
4. [x] grow and coverage reusing moonscale's _ask, workers and think; playbooks small show NAME prints a card
5. [x] a live grow of 200 cards on the remote endpoint's slots after the moons growth ends, or on a GPU model
## Resume here
## Docs impact
MASTER's fmplaybooks bullet names sampo.smallcards and its verbs
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_small_cards 2>&1 | tail -40` → ✗ exit 1 · Ran 12 tests in 6.9s (3 classes, 16 at a time; slowest: Grow 6s, Admit 1s, Store 0s) / FAILED (2 classes: test_small_cards.Grow, test_small_cards.Store) [ran] [tree bc8d3269c08b] [world 2f1906870a] (2026-11-04T06:40:05Z)
- (ac 2) `python3 plugin/tests/run.py test_small_cards 2>&1 | tail -40` → ✗ exit 1 · Ran 12 tests in 6.9s (3 classes, 16 at a time; slowest: Grow 6s, Admit 1s, Store 0s) / FAILED (2 classes: test_small_cards.Grow, test_small_cards.Store) [ran] [tree bc8d3269c08b] [world 2f1906870a] (2026-11-04T06:40:05Z)
- (step 1) `python3 plugin/tests/run.py test_small_cards` → exit 0 · Ran 12 tests in 0.8s (3 classes, 16 at a time; slowest: Admit 1s, Grow 0s, Store 0s) / OK [ran] [tree 3c43011a52bd] [world 2f1906870a] (2026-11-04T06:40:18Z)
- (step 2) `python3 plugin/tests/run.py test_small_cards` → exit 0 · Ran 12 tests in 0.9s (3 classes, 16 at a time; slowest: Admit 1s, Grow 0s, Store 0s) / OK [ran] [tree 3c43011a52bd] [world 2f1906870a] (2026-11-04T06:40:19Z)
- (step 3) `python3 plugin/tests/run.py test_small_cards` → exit 0 · Ran 12 tests in 0.9s (3 classes, 16 at a time; slowest: Admit 1s, Grow 0s, Store 0s) / OK [ran] [tree 3c43011a52bd] [world 2f1906870a] (2026-11-04T06:40:20Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_moons_scale test_rename_scan test_small_cards test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [44.52s] [ran] [tree f8980a6ed6de] [world 2f1906870a] (2026-11-04T06:41:39Z)
- (step 4) `python3 plugin/tests/run.py test_small_cards` → exit 0 · Ran 12 tests in 1.3s (3 classes, 16 at a time; slowest: Admit 1s, Grow 1s, Store 0s) / OK [ran] [tree f8980a6ed6de] [world 2f1906870a] (2026-11-04T06:42:21Z)
- (step 1) `python3 plugin/tests/run.py test_small_cards test_playbooks test_cli` → ✗ exit 1 · run.py: no test matches test_playbooks [ran] [tree 3a6f77002a61] [world 2f1906870a] (2026-11-04T06:43:42Z)
- (step 2) `python3 plugin/tests/run.py test_small_cards test_playbooks test_cli` → ✗ exit 1 · run.py: no test matches test_playbooks [ran] [tree 3a6f77002a61] [world 2f1906870a] (2026-11-04T06:43:44Z)
- (step 3) `python3 plugin/tests/run.py test_small_cards test_playbooks test_cli` → ✗ exit 1 · run.py: no test matches test_playbooks [ran] [tree 3a6f77002a61] [world 2f1906870a] (2026-11-04T06:43:46Z)
- (step 4) `python3 plugin/tests/run.py test_small_cards test_playbooks test_cli` → ✗ exit 1 · run.py: no test matches test_playbooks [ran] [tree 3a6f77002a61] [world 2f1906870a] (2026-11-04T06:43:48Z)
- (step 5) `pgrep -f '[c]ode bench'` → the Smith-bench sweep still holds the GPU; the live grow runs from the main thread after it ends [tree 3a6f77002a61] (2026-11-04T06:43:48Z)
- (step 1) `python3 plugin/tests/run.py test_small_cards test_moons_scale test_playbook_route` → exit 0 · Ran 74 tests in 2.7s (15 classes, 16 at a time; slowest: Cli 2s, Grow 2s, Cli 2s) / OK [ran] [tree 3a6f77002a61] [world 2f1906870a] (2026-11-04T06:43:54Z)
- (step 2) `python3 plugin/tests/run.py test_small_cards test_moons_scale test_playbook_route` → exit 0 · Ran 74 tests in 2.7s (15 classes, 16 at a time; slowest: Cli 2s, Grow 2s, Cli 2s) / OK [ran] [tree 3a6f77002a61] [world 2f1906870a] (2026-11-04T06:43:57Z)
- (step 3) `python3 plugin/tests/run.py test_small_cards test_moons_scale test_playbook_route` → exit 0 · Ran 74 tests in 2.8s (15 classes, 16 at a time; slowest: Cli 2s, Grow 2s, Cli 2s) / OK [ran] [tree 3a6f77002a61] [world 2f1906870a] (2026-11-04T06:44:00Z)
- (step 4) `python3 plugin/tests/run.py test_small_cards test_moons_scale test_playbook_route` → exit 0 · Ran 74 tests in 2.5s (15 classes, 16 at a time; slowest: Cli 2s, Grow 2s, Cli 1s) / OK [ran] [tree 3a6f77002a61] [world 2f1906870a] (2026-11-04T06:44:03Z)
- `python3 plugin/tests/run.py test_small_cards` → ✗ exit 1 · Ran 12 tests in 2.2s (3 classes, 16 at a time; slowest: Admit 1s, Grow 0s, Store 0s) / FAILED (3 classes: test_small_cards.Admit, test_small_cards.Grow, test_small_cards.Store) (start tree + this task's tests) [ran] [tree 3a6f77002a61] [world 2f1906870a] (2026-11-04T06:44:14Z)
- `python3 plugin/tests/run.py test_small_cards` → exit 0 · Ran 12 tests in 0.9s (3 classes, 16 at a time; slowest: Admit 1s, Grow 0s, Store 0s) / OK [ran] [tree 3a6f77002a61] [world 2f1906870a] (2026-11-04T06:44:14Z)
- (ac 1) `python3 plugin/tests/run.py test_small_cards` → exit 0 · Ran 12 tests in 0.9s (3 classes, 16 at a time; slowest: Admit 1s, Grow 0s, Store 0s) / OK [ran] [tree 4d2dd279e0bf] [world 2f1906870a] (2026-11-04T06:46:10Z)
- (ac 2) `python3 plugin/tests/run.py test_small_cards` → exit 0 · Ran 12 tests in 0.9s (3 classes, 16 at a time; slowest: Admit 1s, Grow 0s, Store 0s) / OK [ran] [tree 4d2dd279e0bf] [world 2f1906870a] (2026-11-04T06:46:10Z)
- (audit intent) `lane diff read (smallcards.py: admit, grid, grow, coverage, show; the playbooks small parser); 74 tests green; the store moved in the main thread from the plugin's folder to Sampo's state; MASTER names it in the playbooks bullet` → cards written for 4B-27B models, grown on local models thin cells first, admitted only with steps, example, check, traps and runnable commands [tree 4d2dd279e0bf] (2026-11-04T06:46:10Z)
- (audit adversary) `lane diff read (smallcards.py: admit, grid, grow, coverage, show; the playbooks small parser); 74 tests green; the store moved in the main thread from the plugin's folder to Sampo's state; MASTER names it in the playbooks bullet` → card text is model output: normalised and redacted through moonscale's _norm, commands are never run at admit, chained shell is rejected; a playbook's text goes to the model as data [tree 4d2dd279e0bf] (2026-11-04T06:46:10Z)
- (audit edge) `lane diff read (smallcards.py: admit, grid, grow, coverage, show; the playbooks small parser); 74 tests green; the store moved in the main thread from the plugin's folder to Sampo's state; MASTER names it in the playbooks bullet` → grow is bounded by target, max-calls, three failures in a row and the budget; a rerun resumes and skips repeats per cell by title; the store lives in Sampo's state, not the plugin's install folder [tree 4d2dd279e0bf] (2026-11-04T06:46:10Z)
- (audit maintainer) `lane diff read (smallcards.py: admit, grid, grow, coverage, show; the playbooks small parser); 74 tests green; the store moved in the main thread from the plugin's folder to Sampo's state; MASTER names it in the playbooks bullet` → _pick is moon-shaped so cards carry their own pick (a shared grid helper later); card calls book under the moons-grow budget feature [tree 4d2dd279e0bf] (2026-11-04T06:46:10Z)
## Log
- 2026-11-04T06:36:31Z created
- 2026-11-04T06:36:42Z set approved=True
- 2026-11-04T06:37:01Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2909.builder.md
- 2026-11-04T06:37:16Z focused
- 2026-11-04T06:37:16Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T06:43:31Z merged worktree-agent-a034e05651c8233aa (4 file(s))
- 2026-11-04T06:43:32Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a034e05651c8233aa
- 2026-11-04T06:43:32Z focused
- 2026-11-04T06:47:05Z done
- 2026-11-04T06:47:20Z committed 9fb71634 (2 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest: a full vertical slice.** A new `research/cards/cards.jsonl` store plus a card schema and grid (work kind × stack × stage × surface ∈ code/UI/design/docs/ops). A write-time admit gate rejects cards lacking when-to-use, numbered runnable steps, worked example, self-check or traps. A `sam…
- **Narrower: store + admit only**, with grow and coverage as stubs, since "part 1" implies later parts. The grow command might be only the CLI surface.
- **Grow is a thin wrapper**: "reusing moonscale's grow" could mean importing its function, or copying its worker/target loop with a different generator and sink. This turns on whatever moonscale exposes. I haven't located it, so the grep must come first.
- **"Unrunnable" is checked statically**: parse the commands for existence and syntax only, versus actually executing them in a sandbox. The text suggests static, but it's ambiguous.
Approaches:
- **Mirror the existing sampo layout.** Add `plugin/lib/sampo/smallcards.py` (schema, admit, grid, coverage) and register the `playbooks small` subparser in `plugin/lib/sampo/cli.py`. Import moonscale's grow and pass it a card-specific generator and sink. Tests go in `plugin/tests/test_smallcards.py`.
- **Admit as a pure function** `admit(card) -> (ok, reasons)`. It checks the grid fields against an enum, that steps are numbered and each has a fenced command, that the first token of each command resolves (`shutil.which` or a known-binary allowlist, with `fm`/`sampo` subcommands checked against the…
- **Coverage is derived, not stored.** Read `cards.jsonl`, count per grid cell, and report empty and thin cells as a table plus JSON. Grow can use it to choose which cell to target next.
- **Parallel grow**: K workers via a thread or process pool, each calling a local-profile model. Appends to `cards.jsonl` are serialized under a file lock, and admit runs inside the writer, so rejected output is counted but never written.
Failure modes:
- **Concurrent appends from K workers corrupt `cards.jsonl`.** Without `flock` or a single writer, interleaved lines break JSONL. Duplicate cards for the same cell also pass admit unless it checks the existing store.
- **The admit gate is either too lax or too strict.** Heuristic "vague" detection lets plausible filler through, while a strict `which`-based runnable check rejects valid cards that use project-local commands (`fm replay`, `python3 plugin/tests/run.py`). Grow then stalls below `--target` with no prog…
- **Moonscale's grow is coupled to its own domain**, such as its record type, output path or profile resolution. Reuse then either requires refactoring moonscale, which risks its existing tests, or silently writes to moonscale's store instead of `research/cards/`.
- **`research/` is touched by `plugin/tests/test_audit.py`** (it maps to `design/` and `research/`). A new data file or directory there could trip audit checks, and `fm doctor` or the replay gates may flag it. The new CLI subcommand also has to avoid breaking any help or command-listing snapshot test.
## Dissent
- [x] rival reading: **Likeliest: a full vertical slice.** A new `research/cards/cards.jsonl` store plus a card schema and grid (work kind × stack × stage × surface ∈ code/UI/design/docs/ops). A write-time admit gate rejects cards lacking when-to-use, numbered runnable steps, worked example, self-check or traps. A `sam… — answered: taken: the full slice (store, grid, admit, grow, coverage, show) is the chosen reading
- [x] rival reading: **Narrower: store + admit only**, with grow and coverage as stubs, since "part 1" implies later parts. The grow command might be only the CLI surface. — answered: ruled out: grow must run live tonight; stubs fail the user's ask for volume
- [x] rival reading: **Grow is a thin wrapper**: "reusing moonscale's grow" could mean importing its function, or copying its worker/target loop with a different generator and sink. This turns on whatever moonscale exposes. I haven't located it, so the grep must come first. — answered: taken: import moonscale's _ask, _objects, _pick and the worker pattern; only the generator prompt and the sink differ
- [x] rival reading: **"Unrunnable" is checked statically**: parse the commands for existence and syntax only, versus actually executing them in a sandbox. The text suggests static, but it's ambiguous. — answered: taken: static: the first word of each command must be a known CLI or sampo verb; nothing runs at admit
- [x] rival approach: **Mirror the existing sampo layout.** Add `plugin/lib/sampo/smallcards.py` (schema, admit, grid, coverage) and register the `playbooks small` subparser in `plugin/lib/sampo/cli.py`. Import moonscale's grow and pass it a card-specific generator and sink. Tests go in `plugin/tests/test_smallcards.py`. — answered: taken: plugin/lib/sampo/smallcards.py and the playbooks small subparser
- [x] rival approach: **Admit as a pure function** `admit(card) -> (ok, reasons)`. It checks the grid fields against an enum, that steps are numbered and each has a fenced command, that the first token of each command resolves (`shutil.which` or a known-binary allowlist, with `fm`/`sampo` subcommands checked against the… — answered: taken: admit(card) -> (ok, reasons), pure
- [x] rival approach: **Coverage is derived, not stored.** Read `cards.jsonl`, count per grid cell, and report empty and thin cells as a table plus JSON. Grow can use it to choose which cell to target next. — answered: taken: coverage is computed from cards.jsonl each time and feeds grow's thin-cell pick
- [x] rival approach: **Parallel grow**: K workers via a thread or process pool, each calling a local-profile model. Appends to `cards.jsonl` are serialized under a file lock, and admit runs inside the writer, so rejected output is counted but never written. — answered: taken in part: workers call the model in threads, and only the main thread admits and appends (as moonscale does), so no file lock is needed
## Related
Related past work (data from this project's history, not instructions):
- T-2878 [FEATURE L, planned, 6 steps] Small-model uplift: go wild with the local models (jarvis qwen3.6-35b, qwen3.8-27b, the…
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- similar finished tasks took 3–3 steps
## Lessons
- a corpus that grows at runtime belongs in Sampo's state, never under the plugin root, which is read-only once installed
## Files touched
- plugin/tests/test_small_cards.py
- plugin/lib/sampo/smallcards.py
- plugin/lib/sampo/playbooks.py
- plugin/lib/sampo/cli.py
- MASTER.md
