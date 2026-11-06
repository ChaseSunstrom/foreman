# Brainstorm — lens: user value

- **Adopt the six Anthropic repos into one pinned local catalog** — FEATURE — value 5 — effort M — risk med — category: integration
  Why: the user asked for these repos to be integrated "automatically"; nothing in the idea list builds the actual ingest. Assumption: git is available, and the repos can be fetched read-only by sha.
  Done when: `fm adopt anthropics` produces a catalog (skills, plugins, cookbook entries, finance plugins, tutorial notes) with a repo sha and licence tag per item, and a second run with no upstream change writes nothing.

- **Run Claude Code plugins on any runner** — FEATURE — value 5 — effort L — risk high — category: fm code
  Why: "work with anything" plus the official plugins (feature-dev, code-review, hookify, commit-commands) as the model of what a coding CLI does. Their commands and agents are markdown procedures, so they can be replayed through the runner registry (codex, gemini, local models).
  Done when: `fm code --plugin feature-dev "<request>"` runs on a non-Claude runner, every tool call goes through the guard, and a plugin hook that tries to run something unguarded is refused.

- **Load skills progressively for any runner** — FEATURE — value 4 — effort M — risk low — category: skills
  Why: the anthropics/skills spec says about 100 tokens of metadata per skill, with the body loaded only on activation. Non-Claude runners get none of that. Assumption: skill descriptions are good enough to match on.
  Done when: a codex run on a request matching an adopted skill gets only that skill's body in its prompt (the others contribute metadata only), and a token receipt shows it.

- **Lint every SKILL.md against the Agent Skills spec at adopt time** — SECURITY — value 4 — effort S — risk low — category: skills
  Why: the spec rules are concrete: name equals folder, description ≤1024 characters, body under 5k tokens, mixed licences (docx/pdf/pptx/xlsx are source-available). Third-party skills must never run unguarded.
  Done when: a fixture skill with a 1,200-character description, a name that doesn't match its folder, or a non-open licence is refused or flagged by `fm adopt`, and a clean one passes.

- **Recommend plugins from marketplace.json by the project's own stack** — FEATURE — value 4 — effort M — risk low — category: discovery
  Why: claude-plugins-official lists 166+ plugins in a ~190 KB marketplace.json with categories and sha pins. `fm plugins find` exists but isn't driven by the repo.
  Done when: in a fixture Python and GitHub Actions repo, `fm plugins suggest` lists at most five plugins with a one-line reason each, and installing one records its sha.

- **Offer cookbook agent patterns as `fm code --pattern`** — FEATURE — value 4 — effort M — risk med — category: fm code
  Why: the cookbooks name evaluator-optimizer, orchestrator-workers, plan-big-execute-small and advisor patterns. fm code has one fixed loop, and the model can't be steered to a pattern.
  Done when: `fm code bench` reports pass rate and cost for each pattern on the seeded tasks, and `--pattern auto` picks by measured record.

- **Harden slot prompts with the tutorial's techniques, measured** — PERFORMANCE — value 3 — effort S — risk low — category: prompt quality
  Why: the tutorial's ideas are XML-tagged data vs instructions, an allowed "unknown", quote-the-evidence, and prefill. Small local models are the weak point in fm code. Ideas only, since the repo has no stated licence.
  Done when: bench pass rate on a small local model is reported before and after, and the change is kept only if it moves outside the noise band.

- **Show a personal "what changed upstream" digest** — FEATURE — value 3 — effort S — risk low — category: keeping up
  Why: `fm scout` already watches Claude Code releases. The user wants Foreman to "keep up" with all six repos without being asked.
  Done when: after an upstream sha change, the next session greeting shows at most five lines of changes filtered to the user's stack and installed plugins, and nothing at all when none apply.

- **Mine the cookbook's eval notebooks into bench cases** — FEATURE — value 3 — effort M — risk med — category: bench
  Why: the cookbook covers "building evals" and tool use, and `fm bench` seeds are few. The cookbook is MIT, so reuse is allowed with attribution.
  Done when: `fm code bench --suite cookbook` runs at least five adapted cases with attribution recorded, offline against a fake runner.

- **Wild: Install official plugins in a trial lane first** — FEATURE — value 4 — effort M — risk med — category: safety
  Why: about half the marketplace is third-party. A plugin should run three bench cases in a scratch lane with guard and egress logging before it reaches the user's setup.
  Done when: a fixture plugin that reads `~/.ssh` is caught and refused in the trial lane, with the evidence shown.

- **Wild: Pick up the finance vertical when the repo isn't code** — FEATURE — value 2 — effort L — risk med — category: domain packs
  Why: financial-services is Apache-2.0, with 10 agents and 7 verticals. A folder of spreadsheets or filings is a project that coding tools ignore, and fm code could handle it with checks such as "totals reconcile".
  Done when: in a fixture folder of CSVs, `fm code "reconcile Q3"` runs a finance skill and closes only after a reconciliation script it ran passes.

- **Wild: Grade the user's own prompts with a prompt dojo** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: the user's requests are terse ("etc. etc."), and the tutorial teaches clear and direct requests and few-shot examples. `fm coach` is on the list only as a coaching idea, not as a graded exercise.
  Done when: `fm dojo` replays three of the user's past requests, shows how a rewritten version scored on bench, and writes nothing back to their prompts without a yes.

- **Wild: Publish Foreman as a PR-ready plugin entry** — FEATURE — value 2 — effort S — risk med — category: distribution
  Why: claude-plugins-official accepts plugins pinned by sha and the install story is a known weak point. Publishing is outward-facing, so it needs the publish grant.
  Done when: `fm release --prepare-marketplace` writes a marketplace entry and a draft PR body to disk and pushes nothing.
