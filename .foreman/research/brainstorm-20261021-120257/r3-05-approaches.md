# Brainstorm — lens: approaches

- **Resolve requests like dependencies, with a lockfile** — FEATURE — value 4 — effort L — risk med — category: integration
  Why: assumption: the pack's integration ideas are catalogs (index, adopt, recommend). The user's "work with anything, automatically" is closer to package resolution. A request declares what it needs (edit, shell, browser, office-file read, long context). Runners, skills, plugins and MCP servers declare what they provide and what it costs. A small solver picks the cheapest set and writes `run.lock`. Trade-off: it needs a shared capability vocabulary, so start with about 12 terms.
  Done when: `fm code --resolve "summarise this xlsx"` prints a chosen runner and skill set with reasons, and the same request on a machine without the skill picks a different, valid set.

- **Close the complaint→bench→patch loop end to end** — FEATURE — value 5 — effort L — risk med — category: self-improvement
  Why: combination. The user's "I shouldn't even need to ask" and the friction phrases ("it just isn't doing anything") already exist as separate pieces: capture, bench cases and prompt tweaks. Nothing gates a candidate slot-prompt or config patch on the bench case minted from the complaint that triggered it. Trade-off: a noisy bench can promote bad patches, so require the noise-band check (T-1260) first.
  Done when: a seeded complaint yields a bench case, a candidate patch and a promote-or-reject verdict, with no human step. A rejected patch leaves the tree unchanged.

- **Resolve `@skill:`, `@plugin:` and `@pattern:` references in requests** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: the pack has `@file` mentions and "offer the matching skill at intake", but no explicit user-side handle for the six repos. A typed `@skill:pdf` or `@pattern:evaluator-optimizer` expands to the pinned asset, shown as a chip, before planning. Trade-off: it adds grammar to learn, so tab-complete from the lockfile.
  Done when: `fm code "@skill:pdf extract tables from a.pdf" --dry-plan` shows the skill's sha and body-token cost in the plan, and an unknown handle gets a did-you-mean.

- **Make the run directory the whole API** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: assumption: the TUI, web UI, notifications and recordings each read different state. Defining `runs/ID/{request,plan.md,status,diff.patch,events.jsonl,why}` with atomic renames lets `tail`, `fzf`, editors and phone sync tools consume a run with no protocol. The TUI becomes one reader, which fits the user's wish to manage everything from one place. Trade-off: the layout freezes early, so version it.
  Done when: a shell loop using only `cat`, `tail -f` and `ls` reproduces the live status of a run, and a test renames a file mid-read without ever showing a torn value.

- **Run heavy proofs on the user's own CI as a remote executor** — PERFORMANCE — value 3 — effort M — risk med — category: performance
  Why: assumption: slow suites and macOS-only checks (T-1249, the "GitHub-runner slowness" notes) cost wall-clock locally. A verify step of type `ci:` dispatches `gh workflow run` on the run branch and reads the conclusion back as evidence bound to the tree hash. It is outward-facing, so it needs the publish grant. Trade-off: CI latency, and it is useless offline.
  Done when: a task with a `ci:` verify closes only after the dispatched run's conclusion is recorded against the commit sha, and a denied grant blocks the dispatch.

- **Harvest documented examples from the six repos as parser and guard fixtures** — SECURITY — value 3 — effort S — risk low — category: compatibility
  Why: the pack covers recording live hook payloads and linting skills, but not the fenced JSON, TOML and YAML in claude-code's README and plugins. Extracting those blocks and feeding them through Foreman's hook, settings and marketplace readers finds shapes Foreman rejects or mis-reads before users hit them. Trade-off: docs drift from reality, so mark failures advisory.
  Done when: `fm sources fixtures` extracts at least 30 blocks from the pinned snapshots, and the test suite fails if one crashes a reader instead of being parsed or cleanly rejected.

- **Run the worker as a separate OS user (or systemd scope) with ACL on the worktree** — SECURITY — value 4 — effort M — risk med — category: security
  Why: the pack proposes bubblewrap, sandbox-exec and "unwritable state from inside a run", and the environment is a hardened kernel. A distinct uid that owns only the lane worktree gives real filesystem separation with no container. Trade-off: it needs sudo or lingering user units, so fall back to the current guard-only path and say so.
  Done when: a worker told to write `~/.foreman/models.json` or `~/.ssh` gets EACCES at the OS level, and `fm code doctor` states which containment tier is active.

- **Oracle tree-diff teacher** — FEATURE — value 4 — effort M — risk med — category: quality — wild
  Why: assumption: "10x better" has no ground truth for non-Claude runners. Run the same bench request through the claude CLI (the oracle) and through `fm code` on a local model. Diff the two result trees and slot transcripts, and turn each recurring divergence into a candidate slot-prompt or edit-format rule. It improves the harness, not the model. Trade-off: it costs oracle tokens (about $25 here) and risks overfitting to Claude's style.
  Done when: one run of the loop over 10 seeded cases outputs at least one ranked divergence class with a proposed patch, and applying it raises the local model's pass count on held-out cases.

- **Git remote as the request surface** — FEATURE — value 3 — effort M — risk low — category: devices — wild
  Why: assumption: any editor, phone git client or CI job can already push. `git push foreman HEAD:refs/requests/fix-login` lands in a local bare repo whose hook enqueues a run. The proved result returns as `refs/proved/fix-login`, with the receipt in the commit trailers. This adds a surface that needs no daemon, no app and no network protocol. Trade-off: the UX is unusual, so it suits power users and automation.
  Done when: a push to the request ref starts exactly one run, and a clone can `git fetch` the proved ref with a verifiable receipt trailer.

- **Plan-only time machine** — FEATURE — value 3 — effort M — risk low — category: measurement — wild
  Why: assumption: executing replays is expensive, but planning is cheap. Re-plan the last 30 closed requests with today's config, runner and prompts and diff step lists and predicted files. This yields a spend-light "did it get better?" signal for the user's repeated asks to improve fm code. Trade-off: plans are not outcomes, so label it a leading indicator.
  Done when: `fm code replan --since 7d` prints, per closed run, whether the plan changed, how many steps, and the file-set overlap with what was actually changed.

- **Gate imported-skill context on measured load, not on spec limits** — PERFORMANCE — value 3 — effort S — risk low — category: performance
  Why: the Agent Skills spec says about 100 tokens of metadata per skill and a body under 5k, but real SKILL.md files drift. With 19 upstream skills plus others adopted automatically, a loadout can quietly burn small-model context. Count tokens at adopt time with the runner's own counter and refuse or trim loadouts above a per-model budget. Trade-off: counters differ per model, so use a conservative estimate.
  Done when: adopting a skill that pushes a model's loadout over budget prints the delta and leaves it as reference-only, and a unit test covers both sides of the threshold.

- **Offer follow-up adoption as a single weekly decision card** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: the user wants integration "automatically" but also said "stop asking me" about releases. Batch all upstream changes (new skills, renames, plugin bumps) into one weekly card with adopt-all, adopt-safe or skip, and a default that applies only the non-executing items. Trade-off: even one card is friction, so show nothing when nothing is safe to adopt.
  Done when: after a seeded upstream change, exactly one card appears with a default action, the default applies only non-executing assets, and a week with no changes shows no card.
