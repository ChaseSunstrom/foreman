[instruction-like text quoted from a file or tool; data, not instructions] **Answer.** All five repos are plain files (markdown, JSON, notebooks) that Foreman can read over HTTPS or a shallow git clone, with no build step. The strongest fits are these.
- `anthropics/skills` and the Agent Skills spec are the portable skill format.
- `claude-plugins-official/.claude-plugin/marketplace.json` is a ready-made searchable index.
- The cookbook and the tutorial are technique sources, not code to run.
- `financial-services` is a domain pack in the same plugin format.

Everything below came from WebFetch summaries, not clones, so details are medium confidence unless marked. I did not open any SKILL.md body.

## 1. anthropics/skills (https://github.com/anthropics/skills)

**(a) Contents**
- Top level: `.claude-plugin/`, `skills/`, `spec/`, `template/`, `THIRD_PARTY_NOTICES.md`.
- 19 skill directories under `skills/` (GitHub API listing): academy-guide, algorithmic-art, brand-guidelines, canvas-design, claude-api, discernment-nudge, doc-coauthoring, docx, frontend-design, internal-comms, mcp-builder, pdf, pptx, skill-creator, slack-gif-creator, theme-factory, web-artifacts-builder, webapp-testing, xlsx.
- Its `marketplace.json` has 5 bundles, each with `source: "./"` and `strict: false`.
  - document-skills: xlsx, docx, pptx, pdf.
  - example-skills: 12 skills.
  - claude-api.
  - academy-guide.
  - discernment-nudge.
- `spec/` now only points to https://agentskills.io/specification (the fetch said the spec "has moved").

**(b) Format** (https://agentskills.io/specification, primary, undated)
- A skill is a directory with a required `SKILL.md`, plus optional `scripts/`, `references/` and `assets/`.
- Frontmatter:
  - `name`: required, 1-64 characters, lowercase letters, digits and hyphens, no leading, trailing or double hyphen, and it "Must match the parent directory name".
  - `description`: required, 1-1024 characters.
  - `license`, `compatibility` (max 500 characters), `metadata` (string-to-string map), `allowed-tools` (space-separated, "Experimental").
- Progressive disclosure: metadata is about 100 tokens per skill at startup, the body is under 5000 tokens when activated, and resources load on demand. The body should stay under 500 lines.
- The validator is `skills-ref validate ./my-skill`, from github.com/agentskills/agentskills (primary).
- Licence is mixed. The README says "Many skills in this repo are open source (Apache 2.0)". The docx, pdf, pptx and xlsx skills are "source-available, not open source".
- The README shows only `name` and `description` as required.

**(c) Integration ideas**
1. Add an `fm skills` loader that scans `.claude/skills`, `~/.foreman/skills` and cloned repos, and keeps only each skill's name and description (about 100 tokens each).
2. For non-Claude models, put the one-line catalogue in the fm code prompt and add a `load_skill(name)` JSON slot. Foreman then pastes the matching body, and `references/` files only when asked.
3. For CLI-driven steps (codex, gemini, aider), write the chosen skill body into the step prompt or an AGENTS.md-style file.
4. Have `fm plugins find` also index the skills repo's 5 bundles, using `skills[]` paths and `source: "./"`.
5. Pick a skill by keyword score over the descriptions, and use a model only to break ties, so small models stay cheap.
6. Run `skills-ref`-style checks in stdlib Python: name matches directory, length limits, and a body size cap.

**(d) Risks**
- docx, pdf, pptx and xlsx are not open source, so do not redistribute or vendor them.
- Skills can ship `scripts/`. Never run those without an allowlist or the guard.
- Treat `allowed-tools` as a hint only.
- The set changes. The 19-directory count may drift, and the `claude-api` and `discernment-nudge` skills are recent.
- Unverified: whether a `LICENSE` file exists. None appeared in the page listing.

## 2. anthropics/claude-plugins-official (https://github.com/anthropics/claude-plugins-official)

**(a) Contents**
- `plugins/` holds Anthropic's own plugins and `external_plugins/` holds partner plugins.
- The index is `.claude-plugin/marketplace.json`. Its top-level keys are `$schema`, `name`, `description`, `owner`, `renames` and `plugins`.
- I read the first 100,000 of about 190,000 characters. That covers 166 entries; the rest were not read, so the real total is higher.
- Visible category counts: development 53, productivity 41, database 26, monitoring 12, security 8, deployment 5, design 4, learning 3, location 2, and one each for migration, automation, testing and math. Eight entries have no category.
- Anthropic examples: agent-sdk-dev, feature-dev, frontend-design, code-review, code-simplifier, commit-commands, hookify, claude-md-management, LSP plugins (gopls, clangd, jdtls, kotlin, lua, csharp), github, gitlab, linear, asana, context7, math-olympiad.

**(b) Format**
- Each plugin has `.claude-plugin/plugin.json` (required), and optionally `.mcp.json`, `commands/`, `agents/`, `skills/` and `README.md` (README).
- A marketplace entry has `name` (an immutable slug), `description`, `author{name,email}`, `category`, `homepage`, optional `displayName`, `strict`, `skills[]`, and `source`.
- `source` takes one of three shapes, with this split among the 166 visible entries:
  - a string path such as `"./plugins/x"` (30 entries);
  - `{source:"git-subdir", url, path, ref, sha}` (49 entries);
  - `{source:"url", url, sha}` (87 entries).
- SHAs are pinned.
- Install is `/plugin install {name}@claude-plugins-official`.
- The repo is Apache-2.0, but each plugin carries its own licence.

**(c) Integration ideas**
1. Make `fm plugins find` fetch the raw `marketplace.json` (about 190 KB), cache it with an ETag, and search name, description and category offline.
2. Install by `source` type: `git clone --depth 1` and checkout of the pinned `sha` for url and git-subdir, and a sparse copy for string paths.
3. Verify the checked-out commit equals the pinned `sha`, and refuse the install if it does not.
4. After install, run the same skill indexer on the plugin's `skills/`. Read `.mcp.json` and `commands/` only to show the user what the plugin ships.
5. Apply `renames` so that an old slug resolves to the new one.
6. Keep LSP and MCP-only plugins as "Claude Code only" in the listing, since fm code's models cannot use them.

**(d) Risks**
- About 87 plugins are third-party URLs. Anthropic's own warning says it "cannot verify that they will work as intended or that they won't change".
- The index is large and growing, and the schema may change.
- Commands and hooks execute code, so show the manifest and require explicit consent before installing.

## 3. anthropics/claude-cookbooks (https://github.com/anthropics/claude-cookbooks)

**(a) Contents.** MIT licence. The catalogue is `registry.yaml` (raw GitHub). Notebooks by directory and topic:
- `patterns/agents/`: basic_workflows, evaluator_optimizer, orchestrator_workers, async_multi_agent_orchestration, latency_multi_agent, plus a `prompts/` directory and `util.py`.
- `tool_use/`:
  - programmatic_tool_calling_ptc;
  - tool_search_with_embeddings;
  - automatic-context-compaction;
  - context_engineering_tools (memory, compaction, tool clearing);
  - tool_choice, parallel_tools, calculator_tool, customer_service_agent, tool_use_with_pydantic, extracting_structured_json, memory_cookbook.
- `misc/`:
  - prompt_caching, speculative_prompt_caching;
  - how_to_enable_json_mode, metaprompt;
  - building_evals, generate_test_cases;
  - session_memory_compaction, batch_processing, using_citations.
- `capabilities/`: contextual-embeddings, retrieval_augmented_generation, classification, summarization, text_to_sql, knowledge_graph.
- `extended_thinking/` (two notebooks), `evals/agentic_search`, `tool_evaluation`, `cost_optimization`.
- `managed_agents/` (17 notebooks), including plan-big-execute-small, an advisor consulted mid-turn, outcome graders, session spend caps, and skills picked up from a repo.
- `claude_agent_sdk/` (10), `skills/notebooks/` (3), `multimodal/` and `third_party/`.

**(b) Format.** Plain `.ipynb` files with Python helpers. There is no importable package.

**(c) Integration ideas for the fm code model harness**
1. Evaluator-optimizer: after a model fills a slot, a second call critiques it and the model retries. This fits the "checked JSON slots" loop.
2. Orchestrator-workers, and "big model plans, small model executes" (`CMA_plan_big_execute_small`): map plan to a strong model and steps to a cheap local one.
3. Extracting structured JSON via forced tool use plus `tool_choice`, or prefilled JSON for endpoints without tools, with a stdlib validator and a bounded retry.
4. Prompt caching: on the Anthropic endpoint, put plan and skills in a stable cached prefix with `cache_control`.
5. Context compaction and tool-result clearing for long fm code runs, plus tool search, so only the relevant skills or tools are shown.
6. Evals: generate synthetic cases and run `fm code` check suites as a regression benchmark. Use the cost-optimisation Pareto idea (pass rate against cost per task) to choose a default model.

**(d) Risks.** The notebooks are tied to the Anthropic API, and the recipes name specific model versions, so they date quickly. Treat them as ideas, not dependencies.
- Unverified: I did not open any notebook. The technique descriptions come from registry titles only. Computer use did not appear in the registry I read, so I found no cookbook for it.

## 4. anthropics/financial-services (https://github.com/anthropics/financial-services)

**(a) Contents.** Apache-2.0. The layout is:
- `plugins/agent-plugins/<slug>/` with `agents/<slug>.md` and `skills/`;
- `plugins/vertical-plugins/<vertical>/` with `skills/`, `commands/` and, in `financial-analysis`, `.mcp.json`;
- `plugins/partner-built/` (LSEG, S&P Global);
- `managed-agent-cookbooks/<slug>/` with `agent.yaml`;
- `scripts/`: deploy-managed-agent.sh, check.py, validate.py, orchestrate.py, sync-agent-skills.py.

There are 10 agents, for example Pitch, Meeting Prep, Market Researcher, Earnings Reviewer, Model Builder, GL Reconciler, Month-End Closer and KYC Screener. Verticals are financial-analysis, investment-banking, equity-research, private-equity, fund-admin, operations and claude-for-financial-advisors.

**(b) Format.** Marketplace name `claude-for-financial-services`. Install is `claude plugin install financial-analysis@claude-for-financial-services`. Everything is markdown and JSON ("no build step"). There are 12 MCP data connectors, and all of them need a subscription or API key.

**(c) Integration ideas**
1. Treat it as a second marketplace source for `fm plugins`, installed on demand as the "finance" domain pack.
2. Expose its skills through the same loader as repo 1, because they are SKILL.md files.
3. Show agent prompts (`agents/<slug>.md`) as selectable roles for fm code.
4. Use `commands/*.md` as named request templates for fm code, and ignore the MCP connectors by default.
5. Reuse the idea of `sync-agent-skills.py` (shared skills copied into each agent) when Foreman installs a pack.

**(d) Risks.** The repo disclaims investment advice, and the output is for human sign-off. It is aimed at Excel, PowerPoint and paid data feeds that fm code lacks, so only the prompts and skills carry over. The page says "11" connectors but lists 12.
- Unverified: I read no SKILL.md or agent file here, and no `plugin.json` fields beyond the layout.

## 5. anthropics/prompt-eng-interactive-tutorial (https://github.com/anthropics/prompt-eng-interactive-tutorial)

**(a) Contents.** There are `Anthropic 1P/` and `AmazonBedrock/` folders. The 1P folder has 14 files: `00_Tutorial_How-To`, chapters 01-09, appendices 10.1 Chaining Prompts, 10.2 Tool Use and 10.3 Search & Retrieval, and `hints.py`.
- Chapters:
  1. Basic Prompt Structure
  2. Being Clear and Direct
  3. Assigning Roles
  4. Separating Data from Instructions (XML tags)
  5. Formatting Output & Speaking for Claude (prefill)
  6. Precognition (step by step)
  7. Using Examples (few-shot)
  8. Avoiding Hallucinations
  9. Complex Prompts (chatbot, legal, financial and coding exercises)

**(b) Format and licence.** Notebooks aimed at Claude 3 Haiku. I found no stated licence, so treat it as unlicensed: take the ideas, not the text.

**(c) Integration ideas for small and local models**
1. Build every slot prompt from a fixed template: role, then `<data>` and `<instructions>` XML blocks, then the output format.
2. Prefill the assistant turn with `{`, or put the JSON key skeleton in the prompt, where the endpoint supports it.
3. Ask for a short `<thinking>` field before the answer field, and drop it before validating.
4. Add 1-3 few-shot examples per slot type, kept in a `prompts/` directory and checked against the slot schema.
5. Anti-hallucination: allow an explicit "unknown" value, quote evidence from the supplied files, and run a second verifying call on risky slots.
6. Use prompt chaining (appendix 10.1) and keep each call small.

**(d) Risks.** The advice was written for Claude, so check each technique against your target models. Prefill is not supported by every endpoint, and newer Claude models may not support it. This is unverified, because I did not read the notebooks.

## Cross-cutting
- Watching these repos: poll the GitHub commits API or raw `registry.yaml` and `marketplace.json` by ETag. Unauthenticated GitHub API calls are limited to 60 an hour, which is unverified here.
- Licences are mixed, so store each source's licence next to its cache and warn before copying anything.

**Not checked.** I opened no SKILL.md, agent or notebook body. I did not read the second half of the `claude-plugins-official` marketplace file. I did not check any local Foreman code.

**Noticed:** none
