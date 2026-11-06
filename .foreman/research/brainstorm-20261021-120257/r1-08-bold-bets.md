# Brainstorm — lens: bold bets

- **Run Agent Skills inside fm code on any model** — FEATURE — value 5 — effort M — risk med — category: skills
  Why: anthropics/skills defines ~100-token metadata per skill and a body under 5k tokens loaded on activation. The pack shows fm code runners but no skill loader for non-Claude models; assumption: it can reuse the existing slot-JSON mechanism.
  Done when: with a local OpenAI-compatible stub, `fm code` lists only the name and description of each skill in `$FOREMAN_HOME/skills`, the stub answers `{"activate":"pdf"}`, the next prompt contains that SKILL.md body, and its `scripts/` run only through the guard.

- **Pin the six repos in an upstream lockfile that files its own work** — FEATURE — value 5 — effort M — risk med — category: ecosystem
  Why: the user wants these repos integrated "automatically" and kept up with. `fm scout` only watches Claude Code releases. A `fm.upstream.lock` would record repo, sha, licence and per-path policy (`vendorable`, `runnable`, `ideas-only`), keep an optional offline mirror, and turn each nightly diff into a parity row or brief. Needs network opt-in (assumption).
  Done when: a fixture upstream gains one new SKILL.md and one CHANGELOG line, `fm upstream sync` moves the pin, and it files two briefs that name the sha and licence tier.

- **Host Claude Code plugins inside fm code for any runner** — FEATURE — value 5 — effort L — risk high — category: plugins
  Why: claude-code/plugins and claude-plugins-official hold 166+ plugins with commands, agents, hooks and `.mcp.json`. The user asked for fm code to "work with anything". Assumption: plugin.json semantics are stable enough to translate; hook commands would be treated as untrusted and mediated by the guard.
  Done when: a fixture plugin's slash command, agent and PreToolUse hook all work under a stub runner, and a hook containing `rm -rf ~` is refused with a guard verdict.

- **Gate diffs on clean-room similarity to restricted sources** — SECURITY — value 4 — effort M — risk low — category: licensing
  Why: the constraints say no leaked source, and prompt-eng-interactive-tutorial has no stated licence while the docx/pdf/pptx/xlsx skills are source-available. Adopting "automatically" risks verbatim copying. The gate would compare diff n-grams against the mirror for paths marked `ideas-only` or source-available.
  Done when: a diff containing 12 verbatim lines from a mirrored restricted file fails `fm check` and names the source file, while a paraphrase of the same idea passes.

- **Look up prior art at intake before planning** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: the cookbooks (registry.yaml), skills and plugin marketplaces are most useful before the plan exists. `fm plugins find` is manual today. Assumption: a stdlib keyword index over the mirror is good enough.
  Done when: `fm code --dry-plan "fill a PDF form"` prints a plan with an XML-fenced `<prior_art>` block listing the pdf skill with its licence tier, and nothing in it is executed.

- **Replay the whole plugin ecosystem through the guard and parsers** — SECURITY — value 4 — effort M — risk low — category: corpus
  Why: 166+ plugins' hook commands, scripts and manifests are a large real-world corpus (marketplace.json is ~190 KB). The pack shows guard replay on Foreman's own commands but not on this corpus.
  Done when: `fm doctor --corpus` runs every mirrored hook or script command through the guard and every manifest through the parsers, prints a verdict table, and fails on any parser crash.

- **Show one process table across every runner** — FEATURE — value 4 — effort M — risk med — category: management
  Why: Claude Code's agent view (attach, logs, stop) is on the user's list, and "full management" is their phrase. The round-1 slate has a process registry that isn't built. This adds uniform `attach`, `logs`, `stop` and `resume` verbs for claude, codex, gemini and fm code runs, one adapter line per runner manifest.
  Done when: with one fake claude run and one fake codex run live, `fm code ps` lists both, `fm code logs ID` tails each, and `fm code stop ID` kills only that process group.

- **Lint Foreman's own prompts against the tutorial's rules** — CLEAN — value 3 — effort S — risk low — category: prompts
  Why: the tutorial's lessons (data in XML tags, an explicit "unknown" escape, quote-evidence fields, prefill) map onto fm code's checked JSON slots. Small models are the likeliest to hallucinate "done". Rules are restated in Foreman's own words because the tutorial has no licence.
  Done when: a test fails if any slot prompt lacks a fenced untrusted-data block or an `unknown` option, and passes on the current prompts after a fix.

- **Export Foreman's discipline as a spec-valid Agent Skills bundle (wild)** — FEATURE — value 4 — effort M — risk med — category: interop
  Why: wild. The user wants Foreman to work with anything. If other CLIs read SKILL.md (assumption), a bundle of guard-first, plan-before-edit and prove-it skills gives them the discipline without per-CLI adapters (T-0335/T-0336/T-0337 are blocked).
  Done when: `fm skills export DIR` writes folders that pass the spec checks (name equals folder, description ≤1024, body <5k tokens) and a stub loader activates one.

- **Run a skill straight from a URL and sha (wild)** — FEATURE — value 3 — effort M — risk high — category: skills
  Why: wild. `fm code --skill github:anthropics/skills@SHA/pdf` would fetch only that folder, verify it against the lockfile and licence policy, cache it, run it jailed, and expire it after the run. This is a zero-install trial.
  Done when: a local file-served fixture repo works, a wrong sha is refused, and the jail denies a script's network call.

- **Give local models cookbook homework while idle (wild)** — FEATURE — value 3 — effort L — risk med — category: bench
  Why: wild. The cookbooks' tool use, evals and agent-pattern notebooks form a free curriculum. Idle time on a local model would attempt each recipe's stated task offline and grade it against the notebook's expected output, giving a per-model score that feeds `fm code bench` routing. Assumption: notebooks can be reduced to prompt, tools and expected output without copying their text.
  Done when: one mirrored recipe is converted to a case, a stub model passes it, and a failing stub lowers that model's routing score.

- **Adopt before authoring when a habit repeats (wild)** — FEATURE — value 3 — effort S — risk low — category: skills
  Why: wild. Combines the "draft a skill from a habit" idea with the mirror. When the user repeats a manual routine, Foreman first offers a matching existing skill or plugin, with licence and token cost, and drafts its own only if none fits.
  Done when: after three captures that mention filling PDFs, a single yes/no offer names the pdf skill, and declining it drafts a local skill instead.
