# Brainstorm — lens: bold bets

- **Make `fm code` a drop-in `claude` binary for the Agent SDK and IDEs** — FEATURE — value 5 — effort L — risk med — category: compatibility
  Why: the pack covers ACP/MCP servers and a local gateway, but nothing that speaks Claude Code's own `-p --output-format stream-json --input-format stream-json` protocol. Agent SDK apps, claude-code-action and IDE extensions that accept a custom binary path would get Foreman's harness on any model with no changes on their side. The pack gives `claude`'s stream-json format only as an input fm code already parses. Assumption: the CLI flag surface is stable enough to emulate for the core subset.
  Done when: the Agent SDK's `query()` pointed at `fm code --as-claude` completes a seeded-bug task on a local model, and a recorded claude stream-json transcript replays through it with identical event shapes.

- **Close the upstream loop with a kill-switched autopilot** — FEATURE — value 5 — effort L — risk med — category: automation
  Why: the user wants the six repos integrated "automatically". The pack lists the pieces separately: scout, release differ, adoption register, canary, `fm release`. The missing part is one loop with an envelope: upstream change → adaptation lane → bench non-regression → canary on a scratch HOME → release → auto-rollback. Each stage declares its own kill criterion, and every halt writes one line to a morning receipt. The user's "keep going, full auto, release anytime" steers show they'd trust this.
  Done when: a fixture upstream bump (a new marketplace entry plus a changelog hook change) runs end to end in a sandbox and produces a release candidate. A second fixture with a planted bench regression halts at the bench stage with a receipt.

- **Escalate slots on logprob entropy** — PERFORMANCE — value 4 — effort M — risk low — category: cost/quality
  Why: fm code already routes by measured pass rate and has an abstention bench. For OpenAI-compatible local endpoints that return logprobs, the harness can see which JSON slot the model is unsure of while it is being filled. Only that slot is re-run on a stronger runner, which is cheaper than escalating whole steps. Assumption: the endpoint exposes `logprobs`; fall back silently if not.
  Done when: on a bench with a small local model, escalating only high-entropy slots matches the pass rate of full-step escalation while using fewer stronger-model tokens, shown in a results file.

- **Let workers call back into Foreman mid-step** — FEATURE — value 4 — effort M — risk med — category: integration — wild
  Why: assumption: the pack has Foreman as a read-only MCP server and a worker contract of "exit code + diff", but control only flows downward. If MCP-capable runners (claude, codex, gemini) could call `foreman.check_my_work`, `foreman.log_assumption`, `foreman.budget_left` and `foreman.i_am_stuck`, then evidence checks and plan revision happen inside the step, not after it. Every callback is guard-checked and logged.
  Done when: a fake MCP-speaking runner calls `check_my_work` mid-step, gets the red criterion back, fixes it in the same step, and the run journal shows one step rather than a retry.

- **Run the whole harness under a deterministic simulator** — CLEAN — value 4 — effort L — risk low — category: reliability — wild
  Why: the pack proposes many separate fault tools (chaos monkey, torn writes, time warp, misbehaving fakes, kill-at-random-points). A single seeded simulator would own the model, clock, filesystem, subprocess and network together. `fm sim --seed N` could run thousands of seeds in CI and print the one seed that violates an invariant. This also covers stalls and orphaned children, which the user kept hitting.
  Done when: a planted lease-leak bug is found by `fm sim` within 500 seeds, and re-running that seed reproduces it byte for byte.

- **Add a pre-receive git remote that only accepts proved pushes** — FEATURE — value 3 — effort M — risk med — category: gatekeeper — wild
  Why: assumption: local git hooks and pre-push checks already exist in the pack, but those can be skipped with `--no-verify`. A local bare repo with a Foreman pre-receive hook cannot be skipped by any tool, because any agent or human that pushes to it hits the same gate. Rejections print the missing evidence and the exact `fm` command to fix it.
  Done when: pushing a branch with an unproved task to the remote is rejected with that message, and pushing after `fm task finish` is accepted.

- **Version behaviour bundles like packages and upgrade them only on a replay win** — FEATURE — value 4 — effort L — risk med — category: ecosystem — wild
  Why: the pack proposes sharing lessons, stack cards, guard feeds and setup codes, and gating self-changes on the bench. Nothing combines them. A bundle would hold guard rules, cards, slot prompts and bench cases, with semver and a lockfile. An upgrade would be proposed like a dependency bump and applied only if it doesn't regress on the user's own replay corpus. Licence class travels with each bundle.
  Done when: `fm bundle upgrade` refuses a bundle whose replay score drops on a fixture corpus, and accepts one that doesn't.

- **Lint workflow graphs for termination and budget bounds** — CLEAN — value 3 — effort S — risk low — category: static analysis
  Why: the pack proposes editable workflow files, cookbook loop shapes and a loop-break detector, but only catches loops at run time. A static pass over the graph can flag cycles with no cap, paths with no budget, steps with no verify, and fan-out with no join. Assumption: the workflow file has a parseable graph form.
  Done when: `fm code graph lint` rejects a fixture with an uncapped evaluator-optimizer loop, naming the edge, and passes the same graph once a cap is added.

- **Record a context manifest per call** — FIX — value 4 — effort S — risk low — category: observability
  Why: users keep reporting "it isn't doing anything" and "why is it slow". The pack has stall classification, but not a record of what each runner call was handed: system prompt bytes, skills and MCP tools loaded, tokens by source. A manifest stored per journal entry would make `fm code why` answer startup tax and wrong-context questions from data.
  Done when: `fm code why` on a finished run prints per-call context bytes split by source, and the totals match the runner's reported input tokens within 5% on a claude fixture.

- **Turn adopted upstream skills into a searchable index on the home screen** — FEATURE — value 3 — effort M — risk low — category: discovery
  Why: the pack covers pinning, licence gating and loadouts, but not finding. With 166+ marketplace plugins and 19 skills, a user can't know what exists. A typed query on the home screen ("xlsx tie-out") should rank skills and plugins by description match and by fit to the project's stack. Adopting one starts a trial lane, never an install.
  Done when: typing a query on the home screen lists matching entries from a cached local index offline, and Enter starts a trial lane with the licence class shown.

- **Bind each claim in the site and README to a rerunnable check with an expiry** — CLEAN — value 3 — effort M — risk low — category: docs
  Why: assumption: the user asked for better website examples, and the pack has README-lint and generated-figures ideas. A claims file adds expiry, so a claim measured on an older Claude Code version greys out automatically instead of silently going stale.
  Done when: bumping the pinned Claude Code version in a fixture greys out claims older than the version and the build prints the list.

- **Reproduce a run bit for bit from a one-file bundle** — FEATURE — value 3 — effort M — risk low — category: debuggability
  Why: the pack has cassettes and journals, but a bug report from another machine still needs the model's replies, the tree, the config and the runner version. A single redacted file holding all four lets a maintainer, or a CI job, re-execute the run offline. This also feeds friction-to-regression-check.
  Done when: `fm code replay bundle.fmrun` on a clean machine reproduces the original final diff and event stream with no network.

- **Close each round with a decision card, not a report** — FEATURE — value 3 — effort S — risk low — category: simplicity
  Why: the user said "stop asking me" and "don't stop until complete", yet each round still ends in prose to read. A one-screen card would show only what was shipped, what changed for them, and at most three yes/no toggles with defaults. Silence means accept, and the card is stored for later review.
  Done when: closing a fixture round produces a card of at most 20 lines with no more than three toggles, and ignoring it leaves the defaults applied.
