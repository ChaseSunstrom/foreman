# Brainstorm — lens: what a 10x team of agents would do

- **Fork parallel lanes from a contract commit** — FEATURE — value 5 — effort M — risk med — category: fan-out
  Why: lanes and the Agents graph exist, and "predict file overlap" is planned, but nothing stops two builders from inventing incompatible interfaces. Assumption: most fan-out conflicts are interface drift, not file overlap.
  Done when: `fm plan --contract` commits signature stubs plus contract tests to the base branch before lanes fork. A PreToolUse check blocks a lane's edit to a contract file, and a test shows two lanes merging cleanly against the stubs.

- **Run FIX tasks on a hypothesis blackboard** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: the pack plans "locate the cause mechanically" and "race approaches". Neither makes agents state hypotheses and their discriminating experiments. Assumption: FIX tasks lose time re-trying the same idea.
  Done when: `fm debug` creates `hypotheses.jsonl` (claim, experiment, result, status). Each sub-agent claims one hypothesis, and the close gate fails unless exactly one is `confirmed` with a command that ran.

- **Spawn a provisioner for a builder's "I lack X"** — FEATURE — value 4 — effort M — risk med — category: delegation
  Why: builders stall on missing fixtures, docs, cards or env, as in the folding-trust-prompt stall and the missing-`claude`-on-PATH failures. Assumption: those stalls can be resolved by a second agent while the builder continues.
  Done when: a builder writes `needs/<id>.json`, and a provisioner (Haiku, no edit rights outside `.foreman/provided/`) fills it. The builder's next PreToolUse call sees the result, and a test shows the round trip.

- **Learn fan-out width from rework** — FEATURE — value 4 — effort S — risk low — category: scheduling
  Why: the ledger has lanes, merges and minutes lost, but nothing says whether parallelism paid off. Assumption: merge conflicts and duplicated recon are recoverable from the ledger.
  Done when: `fm fleet --width` prints a recommended lane count per task class, computed from conflicts and redone steps. The dispatcher uses it as the default cap, and a replay test over a fixture ledger reproduces the number.

- **Execute every library card's examples in CI** — CLEAN — value 4 — effort M — risk low — category: cards
  Why: 1,084 cards exist but 6 ever fired, and bulk card growth is in flight (T-1036/T-1037). Unverified drafts will rot as library versions move.
  Done when: `fm lib check` runs each card's fenced example in a throwaway venv or npm temp dir at the project's pinned version. Failing cards get `stale: true` and stop being injected, and a fixture card with a wrong call is demoted.

- **Generate MCP servers and skills on demand** — FEATURE — value 4 — effort M — risk med — category: self-extension
  Why: `plugin/templates/mcp-server/` already has a server and test. A shell recipe repeated three or more times is the signal. Assumption: the ledger can detect "same multi-step recipe" by command shape.
  Done when: `fm smith` drafts a project-local MCP tool or skill from a repeated recipe in a sandbox lane. The template's `test_server.py` must pass, and registration requires an explicit yes.

- **Resolve lane conflicts with an integrator agent** — FEATURE — value 4 — effort M — risk med — category: merging
  Why: the merge train is planned and conflict prediction exists, but the actual resolution is manual. The pack has no integrator role.
  Done when: on a conflicting merge, an agent resolves it in a scratch worktree and both lanes' recorded proof commands are re-run. A resolution that turns either red is rejected, and a fixture of two conflicting lanes lands green.

- **Rehearse the merge of all open lanes nightly** — FEATURE — value 3 — effort S — risk low — category: integration
  Why: lanes diverge unseen until close, and the nightly `fm night` runner exists. Assumption: an octopus merge in a throwaway worktree is cheap.
  Done when: `fm night` merges `main` plus every open lane branch into `integration/canary`, runs the gates, and the morning receipt names the first colliding pair, or reports a clean merge.

- **Order the queue by critical path** — PERFORMANCE — value 3 — effort M — risk low — category: scheduling
  Why: the pack plans file-overlap prediction and task forecasts separately. Combining the map's import graph with forecast durations gives a DAG. Assumption: forecasts are good enough to rank.
  Done when: `fm next --dag` prints parallelizable batches with the longest chain first, and a test on a 6-task fixture picks the expected order.

- **Let a scored user-proxy answer low-stakes asks (wild)** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: the user steers repeatedly and wants not to be asked ("shouldn't need to ask"). Corrections and steers are already logged. Assumption: past steers predict most yes/no answers.
  Done when: for an `fm ask` marked low-stakes, a proxy predicts the answer with a confidence and proceeds, and the user is shown a batch of predictions to confirm or overturn later. The proxy's autonomy widens only after its measured agreement passes a threshold, and `fm proxy score` prints the agreement rate.

- **Soak-test Foreman with a simulated user (wild)** — FEATURE — value 4 — effort M — risk med — category: testing
  Why: real incidents came from harness sessions that the Stop hook drove into the queue and from hook ordering. A simulator that rambles, sends fragments and corrects itself would find these earlier. Assumption: the asks ledger gives enough style data.
  Done when: `fm sim` plays 20 scripted user turns against a sandbox state with the `claude` binary locked out (the shared lockout fixture), and fails on any leaked task, stuck queue or hook crash.

- **Transplant a solution between repos (wild)** — FEATURE — value 3 — effort L — risk med — category: cross-project
  Why: the user wants learning "for any project" and across machines, but fixes travel only as hints. Assumption: cards and error fingerprints are enough to match "same shape of problem".
  Done when: for a new FIX task, `fm transplant` finds a closed task in another local repo with the same fingerprint plus card set. It drafts that diff on a branch (never applies it), and the user sees the source task id.

- **Run an overnight peer-review round robin (wild)** — FEATURE — value 3 — effort M — risk low — category: review
  Why: reviewers see their own team's diffs, and the stale-hint risk grows as the brain is shared. Assumption: cheap models can spot cross-task contradictions.
  Done when: each night, one agent reviews a different closed task's diff against the current `.foreman/` rules. The morning receipt lists contradictions with task ids, and a seeded contradiction in a fixture is caught.
