# Brainstorm — lens: performance

- **Measure the real hook tax per turn from CC's own timing** — FEATURE — value 4 — effort S — risk low — category: hook latency
  Why: round 1 judged by bench CPU time, but nobody has measured wall-clock added per real turn across the 14 hook events in live sessions; the Read-hook drop was argued from bench alone (assumption: live p50 differs under load).
  Done when: `fm doctor --perf` prints per-event p50/p95 from recorded live invocations over the last 7 days and flags any event above a stated budget.

- **Short-circuit non-Foreman projects in one stat call** — PERFORMANCE — value 4 — effort S — risk low — category: hook latency
  Why: hooks spawn Python even in repos Foreman doesn't manage (assumption: user has other projects open; installed globally via ~/.claude).
  Done when: in a directory with no Foreman state, every hook exits in under 5 ms (measured by bench) without importing the lib.

- **Run non-gating recording hooks as async** — PERFORMANCE — value 4 — effort M — risk med — category: hook latency
  Why: PostToolUse recording (ledger, evidence, step tracking) doesn't need to block the model; round 1 added more PostToolUse work (compact output) on the synchronous path.
  Done when: bench shows PostToolUse blocking time drops by at least half and the roundtrip e2e still passes with ledger entries intact.

- **Shadow-mode compact output with a measured fetch-back rate** — FEATURE — value 5 — effort M — risk low — category: tokens
  Why: it's off pending a yes; saved ~1.04M tokens/30 days is a projection. Run it silently logging what it would have cut, and how often the model later reads the full file, so the yes is evidence-based.
  Done when: `fm cost --compact-preview` reports would-be tokens saved and the count of cases where the full text would've been needed (failure line missed).

- **Cache gate and verify results by tree hash plus command** — PERFORMANCE — value 5 — effort M — risk med — category: gates
  Why: `fm check --affected` narrowed what runs, but task close re-runs verify commands on trees that haven't changed since the last green run (assumption: finish re-runs them).
  Done when: a second `fm task finish` on an unchanged tree skips verify with a "cached, tree abc123" line, and any touched input invalidates it.

- **Stream gates via Monitor and stop at first failure** — PERFORMANCE — value 4 — effort M — risk med — category: gates
  Why: Round 1 made a monitor plugin primitive available; long test suites currently block until completion and the model idles on a full-suite failure it could have seen in 5 s.
  Done when: a gate with a failing first test returns the failure to the model before the suite ends, and the suite is killed.

- **Spill-store with slice reads for big outputs** — PERFORMANCE — value 3 — effort S — risk low — category: tokens
  Why: compact stubs point to a file in state/outputs, but the model must re-read the whole file to find more; a `fm out ID --grep/--lines` makes the stub's recovery cheap (assumption: model currently cats the file).
  Done when: each stub prints an exact `fm out` command and `fm out ID --grep ERR` returns only matching lines with context.

- **Make `fm` startup lazy: import only the verb's module** — PERFORMANCE — value 3 — effort M — risk low — category: startup
  Why: 50 lib modules; hooks and every `fm` call pay import cost (assumption: cli imports eagerly).
  Done when: `fm task show` imports at most a set of modules asserted in a test, and cold start time drops measurably in bench.

- **Prefix-stable child packs for prompt-cache hits** — PERFORMANCE — value 4 — effort S — risk low — category: tokens
  Why: `fm ideas` fans out many children with large shared context packs (this very pack is enormous); ordering the shared stuff first and varying only the lens last lets the cache hit.
  Done when: child prompts share a byte-identical prefix of the pack, verified by a test comparing two lens prompts, and the reported cached-token share rises.

- **Prune the "ideas so far" list to cluster summaries** — PERFORMANCE — value 5 — effort S — risk low — category: tokens
  Why: the pack carries ~3,000 idea titles per child, mostly duplicates; every brainstorm child pays that input cost and Round 3 yields repeats anyway.
  Done when: the pack renders cluster names with counts plus the last round's titles, cutting its size by 80% while a dedupe test still rejects a known repeat.

- **Wild: Warm hot-spare headless child per project** — PERFORMANCE — value 3 — effort L — risk med — category: warm pool
  Why: wild; reviewers, ideas and recon each pay session startup and cache-miss cost (assumption: a kept-open `claude -p` stream-json child can take successive jobs).
  Done when: the second review in a session starts in under a third of the first's time-to-first-token.

- **Wild: Print "seconds Foreman added" at every close-out** — FEATURE — value 4 — effort M — risk low — category: overhead visibility
  Why: wild; the user asked for "faster" repeatedly but has no number; split hooks, gates, idle and ceremony time per task so regressions are visible.
  Done when: `fm task finish` ends with one line splitting added time across hooks, gates and idle, matching ledger timestamps within 5%.

- **Wild: Race the first affected test against the builder's typing** — PERFORMANCE — value 3 — effort L — risk high — category: speculation
  Why: wild; after each PostToolUse edit, a background lane runs the single most-linked test so failures surface mid-step rather than at gate time (builds on deferred T-0214 sentinel).
  Done when: an edit that breaks a linked test produces a failure note within 10 s of the edit, without blocking the next tool call.

- **Wild: Defer heavy gates on battery or thermal throttle** — PERFORMANCE — value 2 — effort S — risk low — category: scheduling
  Why: wild; bench already judges under load, which shows the user's machine varies; gates could wait or narrow when load is high (assumption: laptop use).
  Done when: with a simulated high-load flag, `fm check` runs only affected tests and says why.
