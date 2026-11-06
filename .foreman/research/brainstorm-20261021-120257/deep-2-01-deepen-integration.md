# Brainstorm — lens: deepen: integration

- **Build one `fm upstream` engine that owns the lock, the diff and the ledger** — FEATURE — value 5 — effort L — risk med — category: integration core
  Why: the existing list (sources.lock, upstreams.toml, coverage ledger, weekly diff) is five spellings of one thing. `fm scout` already watches Claude Code releases, so the pattern exists. Fold them into one file recording repo, pinned sha, licence, shape (skill / plugin / marketplace / cookbook / tutorial) and per-item status (adopted, trialled, skipped, why).
  Done when: `fm upstream status` lists all six repos with sha, licence and a per-item adopted/skipped count, and a test with fixture repos shows a changed sha producing a diff entry rather than an install.

- **Gate every adoption through a trial that must beat baseline** — FEATURE — value 5 — effort L — risk med — category: adoption safety
  Why: T-0866 and T-0867 are deferred for lack of cases, and `fm code bench` now exists. Each adopted skill or plugin would run on seeded bench tasks with and without it, and promotion would need a measured held-rate gain beyond the noise band (T-1260). Assumption: bench cases can be tagged per capability.
  Done when: `fm upstream trial SKILL` prints a with/without delta and noise band, and a skill with no gain is left unpromoted.

- **Run adopted third-party code only under the guard, with a declared-capability manifest** — SECURITY — value 5 — effort M — risk low — category: supply chain
  Why: the constraint is that third-party skills and plugins run nothing unguarded, and T-0791 holds 18 injection and supply-chain ideas. Each adopted item gets a generated manifest of its hooks, scripts and MCP servers, and `fm code`'s lean claude sessions get only the guard plus the allowed set. A new hook or script in a later sha re-triggers review.
  Done when: a fixture plugin that adds a hook in a new sha is refused until `fm upstream approve`, and the guard test suite still passes.

- **Translate upstream shapes into fm code runner capabilities** — FEATURE — value 4 — effort M — risk med — category: cross-runner
  Why: the user wants it to "work with anything", yet only claude has a verified plan mode. A SKILL.md body is plain markdown, so non-claude runners (codex, gemini, aider) could receive it as a step preamble, honouring the ~100-token metadata and under-5k-body progressive disclosure rule.
  Done when: a seeded task run via the aider runner shows the matched skill's body in its step prompt, in an events file.

- **Harvest the cookbook patterns as `fm code` plan templates** — FEATURE — value 4 — effort M — risk low — category: patterns
  Why: evaluator-optimizer, orchestrator-workers, plan-big-execute-small and spend caps already resemble fm code's slot-filling harness. Make each a named strategy that `fm code --pattern NAME` selects, and let routing-by-record pick one. Licence is MIT, so templates can be shipped.
  Done when: `fm code --dry-plan --pattern evaluator-optimizer "x"` prints a plan with a generator step and a grader step.

- **Ingest the Claude Code CHANGELOG into a feature-gap board** — FEATURE — value 4 — effort M — risk low — category: gap tracking
  Why: the user said to model fm code on the claude-code repo. `fm scout` already reads releases. Parse each release line into candidate capabilities, match them against fm code's feature list (agent view, /rewind, fallback models, worktrees) and open captured tasks for what is missing.
  Done when: running scout against a fixture CHANGELOG creates one captured task per unmatched feature and none for matched ones.

- **Mark licence provenance on every adopted asset and enforce it** — SECURITY — value 4 — effort S — risk low — category: licensing
  Why: the pack says docx/pdf/pptx/xlsx are source-available and the tutorial has no licence ("ideas only"). Record a licence class per item. "Ideas only" items can be summarised in notes but never copied, and source-available items are linked at use time, never vendored.
  Done when: a vendor attempt on the tutorial or on a pdf skill fails with the licence reason, and an MIT cookbook item passes.

- **Show one unified catalog in the fm code app** — FEATURE — value 4 — effort M — risk low — category: app surface
  Why: "full management" means everything from the app. A Catalog view could list skills, plugins and patterns from all six sources with trial results and update flags, with Enter to trial and `a` to adopt.
  Done when: the app's catalog screen renders from a fixture lock in a headless snapshot test, with the key bindings listed.

- **Let a request pull the matching upstream capability on demand** — FEATURE — value 4 — effort M — risk med — category: auto-resolve
  Why: the user said they shouldn't have to ask. At plan time, match request text against the catalog's descriptions (grep-like, stdlib) and suggest at most two trial-passed items, shown in the plan and never silently installed.
  Done when: "make a pdf of this report" surfaces the pdf skill in the plan for a project with the catalog loaded, and a no-match request surfaces nothing.

- **Wild: Keep a pre-adoption sandbox project, a "quarantine ward"** — FEATURE — value 3 — effort M — risk low — category: wild safety
  Why: wild. Every new upstream item first runs in a throwaway copy of a fixture repo, with network off and the guard in strict mode, recording every file it touches and command it tries. The recording becomes its adoption report.
  Done when: running a hostile fixture skill in the ward yields a report listing its blocked commands, and the real project is untouched.

- **Wild: Mine the financial-services marketplace as a live workload corpus** — FEATURE — value 3 — effort L — risk med — category: wild benchmarking
  Why: wild. Ten finance agents and seven verticals are realistic non-code tasks for proving "work with anything". Derive bench cases from them (Apache-2.0 allows it) to show fm code is not only a coding harness.
  Done when: `fm code bench --suite finance` runs at least five derived cases and reports pass rates per runner.

- **Wild: Turn the prompt-tutorial lessons into a lint on Foreman's own prompts** — FEATURE — value 3 — effort S — risk low — category: wild prompt quality
  Why: wild, and licence-safe since only the ideas are used. Rules like "data in XML tags, allow 'unknown', quote evidence" become checks over fm's planner and slot prompts. Foreman reviews its own instructions weekly.
  Done when: `fm doctor` flags a fixture prompt that interpolates user data outside a tagged block.

- **Wild: Publish Foreman's own adopted-and-trialled set as a marketplace.json** — FEATURE — value 3 — effort M — risk med — category: wild distribution
  Why: wild. Foreman already speaks the marketplace shape (cc-marketplaces card, T-0352 publish pipeline). It could emit a sha-pinned marketplace of only the items that passed trials, so others install what it proved.
  Done when: `fm upstream export` writes a valid marketplace.json whose every entry is pinned to a sha and has a trial record.

- **Rank upstream changes by what your own failures needed** — FEATURE — value 3 — effort M — risk med — category: relevance
  Why: the weekly diff will be noisy across about 166 plugins. Cross-reference changed items with the user's recorded lessons and failed checks (T-0217's lesson confidence) so the digest leads with the three most relevant.
  Done when: a fixture digest places the item matching a recorded failure above the unrelated ones.
