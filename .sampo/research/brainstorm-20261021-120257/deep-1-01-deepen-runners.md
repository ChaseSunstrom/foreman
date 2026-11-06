# Brainstorm — lens: deepen: runners

- **Build one runner probe record and make it the only source of truth** — CLEAN — value 5 — effort M — risk low — category: runners
  Why: the category list has "feed every runner consumer from one probe result" and "one runner address string everywhere"; `fm code runners`, the home, bench and planner each look runners up separately (assumption: that is why `fmcode.py` and `fmcodebench.py` each resolve things on their own). Merge both into a single record per runner: address, binary path and hash, version, login state, plan-mode verified, stream format, context size, automation terms, last probe time.
  Done when: `fm code runners --json` emits that record for every runner, and a test fails if any other module probes a binary or reads `models.json` directly.

- **Add preflight lamps that block a run before it burns tokens** — FEATURE — value 5 — effort M — risk low — category: runners
  Why: the planned slate has "preflight lamps per runner", and the stall detector only names the cause after 120 s of silence. Check binary present, login live, rate-limit headroom, endpoint reachable and model ID not retired before launching; a failed lamp prints its fix command.
  Done when: with a fake runner whose login is expired, `fm code --task ID` refuses in under 2 s, names the lamp and does not start a worker.

- **Park runs on expired login or rate limit, then resume them** — FEATURE — value 5 — effort M — risk med — category: runners
  Why: "park on expired login, don't fail" is in the list, and stalls already carry a likely cause. Make parking a run state: the task keeps its plan and checks, the home shows "waiting on codex login" or "rate limit until 14:20", and the run resumes at the same step once the lamp turns green.
  Done when: a scripted runner that returns a rate-limit error mid-step leaves the run `parked`, and once the fake clock passes the reset time the run finishes from that step without redoing earlier steps.

- **Route steps to runners by their recorded results** — FEATURE — value 5 — effort L — risk med — category: runners
  Why: the slate has "routing by record", and `fm code bench` already grades runners on seeded tasks. Keep a per-runner, per-step-kind pass rate, cost and time (plan, test-writing, edit, review). Pick the cheapest runner whose record clears a threshold, and fall back through the three-line default rule. Show the reason for each choice.
  Done when: after seeded bench data where runner A passes edits at 90% and runner B at 40%, a run's edit step goes to A, and `fm code why STEP` prints that data.

- **Pin binaries and detect swaps in one trust ledger** — SECURITY — value 4 — effort M — risk low — category: runners
  Why: "detect a runner binary replaced mid-run" and "acquire a missing CLI into a private prefix" both depend on knowing what a binary is. Record path, size, sha256 and version on first trust. Compare before each spawn, and re-check hashes after a self-update. Acquired CLIs install only into a Foreman-owned prefix, verified against a published checksum, and run under the guard.
  Done when: replacing a trusted runner binary between two steps makes the second step stop with "binary changed", and the guard's verdicts for the replaced run are unchanged.

- **Give every runner the same worker contract through an adapter shim** — FEATURE — value 4 — effort L — risk med — category: runners
  Why: "give endpoint models the same worker path as CLIs", and codex/gemini stream parsing is still unbuilt. Define one event vocabulary (tool use, file change, message, usage, done) and write a small parser per runner (claude stream-json, codex `--json`, gemini, aider text). An endpoint model gets a minimal in-harness tool loop that emits the same events. The TUI, stall detector and judge then see one shape.
  Done when: recorded outputs from claude, codex and a plain endpoint model replay to identical event sequences for the same scripted task, checked by a fixture test.

- **Add misbehaving fake runners as a conformance suite** — FEATURE — value 4 — effort M — risk low — category: runners
  Why: the slate lists "misbehaving fake runners", and the repo already has a guard, a stall detector and a post-step judge that should hold against hostile output. Ship fakes that edit `.git/config`, commit unasked, ignore SIGTERM, spam output, print prompt-injection text, hang quietly or claim success falsely. Any registered or user-defined runner can be run against the suite.
  Done when: `fm code runners conform NAME` runs 8 or more misbehaviours against a runner's sandbox and prints which ones the harness caught. All pass on the built-in fakes.

- **Hand a stuck run to a live CLI and take it back** — FEATURE — value 4 — effort M — risk med — category: runners
  Why: "hand a stuck run to a live CLI" is in the slate, and the user wants to manage everything from one app. Offer an `h` key that opens the runner's own interactive session in the run's worktree with the plan, failing checks and diff pre-loaded. When the user exits, the harness re-judges the changed files and continues or closes.
  Done when: handing off a failed step to a stub interactive runner that edits one file leads to the guard and checks running on that edit, and the run resumes from the next step.

- **Race two runners on a step and keep the first that passes** — FEATURE — value 3 — effort L — risk med — category: runners
  Why: the user asked for "10x better" and the checks make a winner objectively decidable. Run the same step in two isolated worktrees, such as a cheap local model and a CLI, and accept the first diff that passes the checks and the judge. Cancel the loser, and record both outcomes for routing.
  Done when: with a fast fake that fails and a slow fake that passes, the slow one's diff is applied, the fast one's worktree is discarded, and the record shows both results.

- **Wild: Keep a runner league table that ranks and promotes** — FEATURE — value 3 — effort M — risk low — category: runners wild
  Why: assumption: the benchmarks page and "Where Foreman loses" (T-1261) point toward public rankings. Run the weekly guest-runner task and the bench on a schedule and keep a season table of pass rate, cost and seconds. Promote the leader to default for a task class only after a margin held for N rounds, using the noise-band idea from T-1260.
  Done when: `fm code league` prints a ranked table from stored bench runs, and a change in default routing appears only after the stated margin has held.

- **Wild: Let the runner write its own adapter, then check it** — FEATURE — value 3 — effort L — risk high — category: runners wild
  Why: the user wants it to "work with anything". Given an unknown CLI, a scout subagent reads `--help` and sample output, drafts a `code.toml` entry, then proves it against the conformance suite and a seeded task. The entry stays quarantined until both pass and the user accepts it.
  Done when: on a made-up CLI script with unusual flags, `fm code runners learn PATH` produces a `code.toml` entry that completes the seeded task, or reports which check failed.

- **Wild: Pay in tokens, not minutes, with a runner budget market** — FEATURE — value 3 — effort M — risk low — category: runners wild
  Why: the pack mentions spend caps, per-call cost and recorded automation terms. Give each runner a daily token and dollar allowance. The router "spends" cheap or free allowances first, such as a local model, and saves paid runs for steps where its record shows they matter. The home shows balances.
  Done when: with a $1 cap and two fake runners priced differently, a queue of 5 tasks stays under the cap and the report shows spend per runner.

- **Wild: Record a fallback chain and replay a run on another runner** — FEATURE — value 3 — effort M — risk low — category: runners wild
  Why: runs already write an events file that `--events` can replay. Add `fm code rerun RUN --on RUNNER`, which replays the same task, plan and checks against another runner and shows a side-by-side of time, tokens, diff size and result. This also feeds routing and the league table.
  Done when: rerunning a finished run on a second fake runner yields a comparison file with both results, and the original run record is unchanged.
