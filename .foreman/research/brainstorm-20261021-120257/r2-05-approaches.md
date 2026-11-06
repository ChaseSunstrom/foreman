# Brainstorm — lens: approaches

- **Adopt only where a duel shows a loss** — FEATURE — value 5 — effort L — risk med — category: adoption
  Why: the pack has "Where Foreman loses" (T-1261), a duel bench (T-1231) and a planned upstream catalog, but nothing joins them. The loss is the trigger: the failing case's text is matched against the pinned catalog, the best candidate runs in a trial lane, and it is adopted only if the paired re-run wins. This answers "automatically" without pulling in hundreds of assets nobody needs.
  Done when: a seeded losing bench case yields a trial-lane run of one named upstream asset, and the report shows pass/fail deltas and an adopt/skip verdict.

- **Give each upstream repo a depth dial: reference, index, host or emulate** — FEATURE — value 4 — effort S — risk low — category: scope
  Why: the user named six repos, but their value and licences differ (the tutorial has no licence, the financial plugins are niche, claude-code is a spec). One `upstreams.toml` row per repo sets how deep Foreman goes. Defaults: tutorial = reference, financial-services = index, skills = host, claude-code = emulate.
  Done when: changing a repo's depth changes what `fm sources` lists, and a "reference" repo never produces an installable or executable entry.

- **Emulate only the gap with a runner × capability matrix** — FEATURE — value 4 — effort M — risk med — category: portability
  Why: the claude CLI already supports hooks, skills, subagents and plugins natively, so Foreman shouldn't re-implement them there. A generated matrix, probed per runner, marks each capability native, emulated or absent. Foreman emulates only where a runner lacks it. Assumption: the probes are cheap, such as `--help` parsing plus one scripted fake-run check.
  Done when: `fm code runners --caps` prints the matrix, and a skill run through claude uses zero Foreman emulation code (shown by a trace counter).

- **Sniff repo shape for a generic `fm adopt URL`** — FEATURE — value 4 — effort M — risk low — category: adoption
  Why: "work with anything" and "integrate all of these" are the same problem. A deterministic classifier recognises SKILL.md trees, `.claude-plugin/marketplace.json`, notebooks plus registry.yaml, and prompt-lesson folders. It then runs lint, licence class and card generation with no model call. The six repos become fixtures, and the next repo costs nothing extra.
  Done when: four fixture repos of different shapes classify correctly offline, and an unknown shape returns "unrecognised" without writing files.

- **Watch upstreams with `git ls-remote` and sparse fetch** — PERFORMANCE — value 4 — effort S — risk low — category: upstream sync
  Why: "keeps up automatically" doesn't need the GitHub API or full clones. A cached `ls-remote` sha per repo is one cheap call and works with no token on stdlib subprocess. Only on a sha change does Foreman sparse-fetch the changed paths. Assumption: git is on PATH, which `fm doctor` can verify.
  Done when: with unchanged shas the watcher makes zero fetches and finishes under 2 s per repo. After a seeded upstream commit it fetches only the changed paths.

- **Rank plugin recommendations by backtest against the user's own ledger** — FEATURE — value 3 — effort M — risk low — category: recommendation
  Why: stack signals are a weak predictor. The ledger has 688+ tasks, so local TF-IDF can say "this skill would have matched 14 of your past tasks". The recommendation arrives with evidence and is never auto-installed.
  Done when: `fm plugins recommend` prints a top-5 with match counts and example task ids, computed offline from the ledger.

- **Build evidence-backed deterministic twins of the official git plugins** — FEATURE — value 4 — effort M — risk low — category: native verbs
  Why: commit-commands, code-review and pr-review-toolkit are mostly prompts around git. Foreman already holds the diff, the proofs and the criteria, so it can produce a commit message, a PR body and a review checklist with zero model tokens. This is a distinct route from hosting the plugins.
  Done when: `fm commit` on a closed task writes a message that cites its criteria and proof ids, with no model call (verified by a call counter at 0).

- **Add an `fm code shell` REPL** — FEATURE — value 3 — effort M — risk low — category: DX
  Why: users asked for "full management", and the TUI is the only interface. A line-oriented shell (`ls`, `cd proj`, `run T-12`, `runner use codex`, `why`) shares the same verbs, so it works over ssh, on dumb terminals and with screen readers. Assumption: the TUI's verb layer is separable. T-0166 suggests it is not fully separated yet.
  Done when: a piped script of five commands (`ls`, `cd`, `run --dry-plan`, `runner use`, `why`) runs under TERM=dumb and exits 0.

- **Land each adoption as a branch with its bench result attached** — FEATURE — value 3 — effort M — risk low — category: review
  Why: adoption and upgrade decisions need a review surface that isn't another TUI panel. A bot-style branch in the user's own checkout carries the card diff, the licence verdict and a bench before/after in the commit body. Merging means adopting and reverting means un-adopting, with no new UI.
  Done when: an upstream sha bump produces one branch, and merging it activates the item while `git revert` deactivates it.

- **(wild) Ask a pinned repo, citation or "unknown"** — FEATURE — value 3 — effort M — risk low — category: knowledge
  Why: `fm sources ask "does claude-code have X?"` answers only from the local pinned index. Every claim carries a path and quote, or the answer is "unknown". This applies the prompt tutorial's own anti-hallucination rule to Foreman's research. Assumption: a local full-text index exists.
  Done when: a question with no matching text returns "unknown" and no invented path. A matching question returns at least one verifiable file:line quote.

- **(wild) Make `fm code` a `claude`-compatible facade** — FEATURE — value 5 — effort L — risk med — category: compatibility
  Why: the user wants it to work with anything and to be modelled on Claude Code. If fm code accepts `-p`, `--output-format stream-json`, `--resume` and `--settings`, then the Agent SDK, IDE extensions and CI actions can drive any model through it. Assumption: stream-json is documented well enough to match. Only the flags in the pack are in scope.
  Done when: a script written for `claude -p … --output-format stream-json` runs unchanged against `fm code` with a local model, and a stream-json parser accepts the output.

- **(wild) Make plans cite the loop pattern they follow** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: the cookbook names a small set of loop shapes (evaluator-optimizer, orchestrator-workers, plan-big-execute-small). If the plan slot must name its pattern or "none", the harness can pick the matching gates. "None" gets extra gating and a flag in the run view.
  Done when: a plan without a pattern field is rejected by the slot validator, and a "none" run shows the added gate in its checks list.
