# Brainstorm — lens: capability map

- **Host Claude Code plugins on any runner** — FEATURE — value 5 — effort L — risk med — category: compat
  Why: the ask is "work with anything" plus integrating claude-plugins-official (166+ plugins) and claude-code/plugins (hookify, ralph-wiggum, security-guidance). The pack lists many ideas for taking Foreman's own pieces to other harnesses, but none where `fm code` is the host that loads a plugin's `plugin.json`, slash commands, agents, hooks (stdin/stdout JSON contract) and MCP servers for a local model or codex.
  Done when: a fixture plugin with a PreToolUse hook that denies `rm -rf` blocks the call under `fm code --runner <fake>`, and its slash command expands.

- **Run Agent Skills with progressive disclosure on any model** — FEATURE — value 5 — effort M — risk med — category: skills
  Why: anthropics/skills specifies ~100-token metadata, a body under 5k tokens on activation, and `scripts/` and `references/` loaded on demand. Existing ideas route skills for Claude only. A runtime-side loader lets small models use them, with scripts executed through the guard (scrubbed env, process-group, no network).
  Done when: a seeded skill with a `scripts/` helper runs under a non-Claude runner, with only metadata in the prompt until activation. A script with a planted `curl` is refused by the guard.

- **Pin the six upstreams in a licence-aware lockfile with a coverage ledger** — FEATURE — value 5 — effort M — risk low — category: upstream
  Why: "integrate automatically, recursive until dry" needs a stopping signal, and the pack has none. Add `upstream.lock` (repo, sha, ETag) fetched by stdlib `urllib` tarball into an empty dir and read with `python -I`. Each path carries a licence class: Apache/MIT vendorable, source-available (docx/pdf/pptx/xlsx) local-only, no-licence (the tutorial) ideas-only and never copied. `fm upstream status` shows items seen, adopted, trialled and declined with reasons.
  Done when: bumping a pinned sha in a fixture produces a diff brief, and a vendor attempt on a no-licence path is refused.

- **Require a verbatim quote or "unknown" in every fact slot** — FEATURE — value 4 — effort S — risk low — category: reliability
  Why: the tutorial's "allow unknown, quote evidence" is not applied to `fm code`'s JSON slots (the research quote-anchor idea covers only web claims). Any slot asserting something about the repo carries `evidence_quote`, which the harness checks by substring match against the named file. A mismatch triggers a bounded reprompt.
  Done when: a scripted model returning a fabricated quote is rejected and reprompted, and a valid quote or `unknown` passes.

- **Recommend marketplace plugins from repo signals, trial before adopting** — FEATURE — value 4 — effort M — risk low — category: discovery
  Why: `fm plugins find` is query-driven. The map already knows languages, databases and CI, and the official marketplace has categories (database, monitoring, security). A stdlib lexical match over a cached `marketplace.json` proposes entries, shows the capability card, and runs a 3-case bench trial before anything is enabled.
  Done when: a fixture Postgres repo surfaces a database plugin with its sha pin, and nothing is installed without a yes.

- **Observe what a third-party hook actually does, and diff it against its declared card** — SECURITY — value 4 — effort M — risk med — category: security
  Why: the guard constraint is that third-party plugins run nothing unguarded. Existing ideas are static cards. Run hooks once in a no-network sandbox lane, record files, execs and hosts touched, and trip on later deviations.
  Done when: a fixture hook that adds a network call after an "update" is blocked with a diff against the recorded card.

- **Probe which prompting techniques move a given model** — FEATURE — value 4 — effort M — risk low — category: models — wild
  Why: the tutorial's ladder (role, XML tags, prefill, few-shot, step-by-step) is the right ablation set. Run it per model on slot tasks and store only the techniques that measurably help in that model's profile. `fm code bench` already grades models but does not choose prompt dialect.
  Done when: `fm code bench --dialect` writes a per-model technique list, and a changed list changes the slot prompt.

- **Phase-compile slash commands into harness state graphs** — FEATURE — value 4 — effort L — risk med — category: workflows — wild
  Why: feature-dev's phases (discover, explore, ask, design, implement, review, summarise) are prose the model must follow. If the harness owns the phases, small models can run them. Convert a command's markdown into a phase graph, one slot per phase, with the cookbook's evaluator-optimizer as an optional loop.
  Done when: a fixture command runs through all phases on a scripted model, and skipping a phase is impossible.

- **Serve a curated private marketplace of vetted entries** — FEATURE — value 4 — effort M — risk low — category: supply chain — wild
  Why: official entries are pinned to shas, about half are third-party, and renames exist. Foreman emits its own sha-locked `marketplace.json` containing only entries that passed vetting, following renames and deprecations. The user adds that, not the upstream catalogue.
  Done when: `claude plugin marketplace add` against the generated file lists only the approved entries, and an upstream rename updates the mirror.

- **Use local servers' KV cache and keep-alive** — PERFORMANCE — value 3 — effort S — risk low — category: local models
  Why: a prefix-stable prompt only pays off locally if llama.cpp `cache_prompt` and Ollama `keep_alive` are set. No pack idea covers this, and local-model slow starts match the "it isn't doing anything" complaints.
  Done when: the second slot call on a local fixture server reports a cache hit and a lower first-token time.

- **Differential-test the plugin host against recorded Claude Code hook traces** — FEATURE — value 3 — effort M — risk low — category: compat
  Why: the compat claim in the host idea needs proof. Replay recorded real-CC payloads for hookify and security-guidance and diff the decisions.
  Done when: CI fails on any verdict difference against the recorded corpus.

- **Lint xlsx and docx deliverables with stdlib zip/XML** — FEATURE — value 3 — effort S — risk low — category: finance pack
  Why: financial-services shows spreadsheet and document outputs, and `fm code` can make them. A `zipfile` and ElementTree check can flag `#REF!`/`#DIV/0!` cells, hardcoded values where formulas are expected, and unit mismatches, without openpyxl.
  Done when: a seeded workbook with an error cell fails the check, and a clean one passes.
