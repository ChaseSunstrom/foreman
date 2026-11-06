# Brainstorm — lens: bold bets

- **Mine external benchmarks into `fm bench`** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: `fm bench` only has 8 cases from Foreman's own history, so A/B results on `/foreman:improve` are thin and noisy. Local repos already hold hundreds of fix commits. `fm bench mine REPO` would walk `git log` for commits that touch both source and a test, keep those where the test fails at the parent and passes at the commit, and add them as cases with the commit message as the prompt. This is a stdlib `git` walk using the existing case builder.
  Done when: `fm bench mine <repo> --limit 20` adds ≥10 cases that each pass a red-at-parent, green-at-commit check, and `fm bench list` shows the repo as a case source.

- **Run a variance-aware promotion gate for self-changes** — FEATURE — value 5 — effort M — risk med — category: self-improvement
  Why: the pack says evals are "single runs, noisy" and the user wants recursive improvement that really improves. `fm bench compare` would run each case k times per arm (adaptive: stop early on a clear win or loss) and promote a candidate only when the lower confidence bound of the pass-rate delta is >0 and cost isn't worse by more than X%. Assumption: pass/fail per case is cheap enough to repeat at about $0.16 per run.
  Done when: `fm bench compare A B` prints delta with an interval, exits non-zero when the interval spans zero, and a test with a stubbed runner covers win, loss and tie.

- **Build a reflexive "improve the improver" cycle** — FEATURE — value 4 — effort M — risk med — category: self-improvement
  Why: the user asks for "recursively improving… and yourself". Today `/foreman:improve` targets rules and plugin files. Add a meta pass that treats the improver's own inputs (friction digest thresholds, brainstorm lens set, STAGE_REFERENCE routing) as candidates and scores them with bench pass rate and cost. Bounded to depth 2 and one reviewer pass, matching the usage constraints.
  Done when: `fm improve --meta` produces a candidate that edits the friction or routing config in a worktree, and a bench comparison result is saved with it.

- **Add a skill-as-hypothesis tournament** — FEATURE — value 4 — effort L — risk med — category: problem-solving
  Why: debugging today runs one line of attack, and a ledger of hypotheses exists. For an L FIX with ≥2 open hypotheses, `fm race` would launch lane worktrees, each given one hypothesis and a tests-only objective. The first lane that turns the failing test green with a smaller diff wins, and the rest are discarded. This builds on `fmlanes` and the hypothesis ledger, and `fm bench` can measure it against the single-thread baseline.
  Done when: on a seeded two-cause bug, `fm race` leaves the winning lane merged, the losing lane reaped, and the ledger marks hypotheses confirmed and ruled out.

- **Compile the user's standing preferences into the bench judge** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: bench scores only pass/fail, but the user's real criteria include quiet output, no commands handed to the user, and few tokens. Add rubric checks over the replay transcript: no "run this" instructions, output length cap, turn count, token cost. A candidate that passes tests but violates these counts as a regression.
  Done when: a replayed transcript containing "please run `x`" fails the preference check, and bench output shows a per-rubric column.

- **Add `fm landscape`, a recurring harness-feature scout** — FEATURE — value 4 — effort M — risk low — category: research
  Why: the user said "research other great plugins/things people want harnesses to do". The one-time landscape study went stale the moment it finished. A standing command would use `fm research ask` to fetch changelogs and READMEs of a short watchlist, with quote verification, diff them against the last run, and file only new features as captures.
  Done when: running it twice with unchanged sources files zero captures, and a changed fixture page files one capture with a verified quote.

- **Wild: Let Foreman ship its own releases through a shadow-user gauntlet** — FEATURE — value 4 — effort L — risk high — category: release
  Why: wild. Before a version bump, the candidate replays bench cases, the guard replay corpus and recorded hook traces, then emits a go/no-go card for one yes/no. This chains three existing gates into one release ritual, so the user stops hand-validating releases.
  Done when: `fm release check` runs all three, prints one verdict, and blocks the version bump on any red.

- **Wild: Synthesize new tasks from adversarial mutation of finished ones** — FEATURE — value 3 — effort L — risk med — category: measurement
  Why: wild. Bench cases are finite and Foreman may overfit them. A generator would take a finished case and have a no-tools `claude -p` child rewrite the request with a different but equivalent symptom, or inject a sibling bug, then keep only variants where the red→green check holds. That gives a held-out set.
  Done when: `fm bench mutate CASE` yields ≥1 variant that fails at the base and whose reference patch makes it pass.

- **Wild: Make Foreman a harness-agnostic MCP skill server** — FEATURE — value 3 — effort L — risk med — category: interop
  Why: wild. Exposing `fm recall`, `fm research ask`, `fm bench` and `fm why` as a stdlib stdio MCP server would let other agents and plugins use Foreman's best parts without adopting its loop. This pairs with the earlier "export as MCP" idea but names the concrete verbs and a read-only first cut.
  Done when: an MCP client can list and call `recall` and `why` against a fixture project and get cited results.

- **Add a "skill diet" ablation via bench** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: the pack says 46 playbooks are never read and nothing measures lift. Run bench cases with a playbook or skill removed from `STAGE_REFERENCE` and compare pass rate and cost. Items with no lift get demoted or merged, which saves tokens for a usage-sensitive user.
  Done when: `fm bench ablate PLAYBOOK` reports the pass-rate and cost delta, and the output names at least one removal candidate.
