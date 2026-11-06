# Brainstorm — lens: bold bets

- **Make `fm code` a drop-in `claude` binary** — FEATURE — value 5 — effort L — risk med — category: compatibility
  Why: user asked for "work with anything" and "like claude does"; Agent SDK and IDE extensions only know the `claude` CLI flags (-p, stream-json, --resume, --settings). A facade that speaks those flags and runs Foreman's loop on any runner makes every Claude-shaped tool use Foreman. Listed only as a wild "facade" idea so far; this is the concrete protocol-level version.
  Done when: `claude -p "x" --output-format stream-json` replaced by `fm code --as-claude` emits events a recorded Claude Agent SDK client parses without error, in a test.

- **Run the whole six-repo upstream as one `upstreams.lock` with a coverage ledger** — FEATURE — value 5 — effort M — risk low — category: integration
  Why: user said "integrate all of these too, automatically." Each repo needs a pinned sha, a licence class (open, source-available, ideas-only), and a row per upstream capability marked adopted, hosted, skipped or later, so "automatically" means a nightly diff files briefs for new rows. Assumption: `fm scout` can be generalized beyond Claude Code releases.
  Done when: `fm sources status` prints every upstream capability with a state, and a fixture upstream change adds one "new" row and one queued brief.

- **Execute Agent Skills on any runner through a progressive-disclosure host** — FEATURE — value 5 — effort L — risk med — category: skills
  Why: anthropics/skills defines SKILL.md (about 100 tokens of metadata, body under 5k on activation); only Claude loads them. Foreman can load metadata, pick by description, and inject the body for codex, gemini or a local model, running scripts through the guard only.
  Done when: a seeded SKILL.md with a script runs on a stub non-Claude runner, loads only after description match, and its script call appears in the guard log.

- **Gate every imported asset with a quarantine stage and capability card** — SECURITY — value 5 — effort M — risk low — category: supply chain
  Why: constraint "third-party skills and plugins run nothing unguarded"; claude-plugins-official has 166+ plugins, about half third-party. Unpack into a throwaway HOME, detonate hooks and scripts against canary files, diff observed behaviour against the declared card, then allow or refuse.
  Done when: a fixture plugin whose hook reads `~/.ssh` is refused with the observed read listed, and a benign one is admitted.

- **Turn cookbook notebooks and the prompt tutorial into a model exam that tunes slot prompts** — FEATURE — value 4 — effort M — risk low — category: eval
  Why: the cookbook has evals and patterns; the tutorial has ten technique chapters (XML tags, prefill, "unknown" escape, few-shot). `fm code bench` exists to grade models. Grade each runner per technique and pick the slot-prompt style that actually helps that model. Tutorial has no licence, so ideas only, with the exam written fresh.
  Done when: `fm code bench --techniques` outputs a per-model table and the chosen slot style changes for at least one fixture model.

- **Close the loop on "super recursive" with a bounded mandate file and convergence stop** — FEATURE — value 4 — effort M — risk low — category: autonomy
  Why: the user keeps saying "etc.", "don't stop", "full auto"; ideas above propose a mandate but nothing defines when recursion ends. A `mandate.toml` with a spend cap, round cap and a "two rounds with no new kept idea" stop gives full auto a defined end.
  Done when: a fixture mandate stops after a round whose ideas are all duplicates and writes a receipt naming the stop reason.

- **Make the run directory the entire API** — FEATURE — value 4 — effort M — risk low — category: architecture
  Why: the idea pile has many TUI, web, phone, ACP and MCP surfaces, each a risk of divergent state. If every run is a directory of plain files (plan.json, events.jsonl, diff.patch, receipt.json) and all surfaces are readers, new surfaces cost nearly nothing and crash recovery is trivial.
  Done when: deleting the TUI and rendering a finished run from only its directory with a 30-line script reproduces the receipt.

- **Adopt before authoring: search the six repos when a habit repeats** — FEATURE — value 4 — effort S — risk low — category: reuse
  Why: Foreman has 1,161 skill files; official skills and plugins likely cover some. Local FTS over pinned trees, queried at intake and on repeated manual recipes, offers a one-line match first.
  Done when: asking for "a pdf form filler" at intake surfaces anthropics/skills' pdf skill with its licence class.

- **Run a duel only where it shows a loss, then adopt** — PERFORMANCE — value 4 — effort M — risk low — category: measurement
  Why: T-1231 and the "Where Foreman loses" briefs show the user wants evidence over assertion. Each adoption lands on a branch with a bench before/after, and merges only on a win or a safety gain.
  Done when: an adoption brief cannot close without a bench delta file naming a metric that improved.

- **Wild: Ship a "ghost shift" that spends idle hours on a speculative queue** — FEATURE (wild) — value 4 — effort L — risk med — category: autonomy
  Why: assumption: user's "don't stop until complete" implies unattended time. Work runs only in throwaway worktrees, output is proposals, and the morning page is a tick list Foreman acts on.
  Done when: a night run leaves branches plus a checklist, and ticking one item merges it with proof attached.

- **Wild: Slip a known-answer canary slot at the start of each run to detect a swapped or degraded model** — SECURITY (wild) — value 3 — effort S — risk low — category: integrity
  Why: with endpoints, gateways and fallbacks, the model behind a name can change silently. A cheap deterministic question grades identity and capability before spending.
  Done when: a stub endpoint returning wrong canary answers causes the run to refuse with the reason named.

- **Wild: Generate a cookbook-style notebook from any finished `fm code` run** — FEATURE (wild) — value 3 — effort M — risk low — category: sharing
  Why: the cookbook is the model of shareable agent recipes; a run's plan, slots, evidence and diff are already structured. Exporting a redacted, replayable notebook turns every success into a recipe other users or small models can reuse as few-shot exemplars.
  Done when: `fm code export --notebook RUN` produces a file whose replay against a cassette reproduces the same diff.

- **Wild: Make weak models earn privilege through a promotion curve and an injection exam** — SECURITY (wild) — value 3 — effort M — risk med — category: trust
  Why: "work with anything" includes untuned local models; a planted-injection exam gives each model a gullibility score that sets its write scope, network and unattended eligibility.
  Done when: a stub model that obeys a planted instruction in a fixture gets read-only scope in the next run.
