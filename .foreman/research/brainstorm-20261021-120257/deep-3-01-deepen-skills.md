# Brainstorm — lens: deepen: skills

- **Build a skill host that every runner shares** — FEATURE — value 5 — effort L — risk med — category: skills
  Why: the list repeats "serve skills to any runner" and "progressive disclosure on any model" as separate ideas; they are one capability. Merge them into one host in fm code: the harness keeps ~100-token metadata per skill in the prompt, loads the body (<5k tokens) only when the model's checked JSON slot names the skill, and resolves `scripts/` and `references/` on demand. Runners with native skills (claude) get the files directly, the others get the same content through the host.
  Done when: one test skill (with a script and a reference file) is activated by a claude runner and by a local OpenAI-compatible stub, and both transcripts show metadata-only until activation, then the body, then the script's output.

- **Run every skill script under the guard** — SECURITY — value 5 — effort M — risk med — category: skills
  Why: the constraint is that third-party skills and plugins run nothing unguarded. Skill `scripts/` are the largest new execution path once adopted skills run on any model. Route every script call through the guard's verdicts, with the skill's own folder as the only writable root. Each script is also pinned to the sha it was adopted at.
  Done when: a fixture skill whose script runs `rm -rf ~` or edits `.git/hooks` is refused by the guard, and a script edited after adoption is refused on a sha mismatch.

- **Adopt skills from the six repos on a schedule** — FEATURE — value 5 — effort L — risk med — category: skills, automation
  Why: the user said "integrate automatically" and that Foreman should figure things out without being told. `fm scout` already watches Claude Code releases. Extend it to poll anthropics/skills and the marketplace.json files (sha-pinned) and queue adoption as tasks. Each adoption records its licence (docx/pdf/pptx/xlsx are source-available, not open), lints against the spec, and is gated on `fm skill lint`. Prompt-eng tutorial content is stored as ideas only because it has no licence.
  Done when: with a fixture upstream that adds a skill and bumps a pinned sha, `fm scout` creates one adoption task naming the licence and the sha diff, and a skill with a restricted licence is flagged "reference only".

- **Score skills by whether they changed the outcome** — FEATURE — value 4 — effort M — risk low — category: skills, evals
  Why: T-0217 (lesson confidence) and T-1259–T-1261 (noise bands) point at measuring effects rather than trusting them. Each activation is logged with the run result. `fm code bench` runs seeded tasks with the skill on and off, N times, and reports the delta with its noise band. Skills inside the band are marked "no measurable effect".
  Done when: `fm skill score NAME` prints pass-rate with and without the skill across N runs and a verdict, and it is reproducible from a recorded events file.

- **Draw the skill loadout and overlap as a live pane** — FEATURE — value 4 — effort M — risk low — category: skills, TUI
  Why: this merges the "context loadout" and "trigger overlap constellation" ideas into one TUI pane in the fm code run view. It shows tokens spent on metadata per skill and the trigger-text similarity between pairs. It highlights which skill was activated this turn, and it offers to merge or sharpen two overlapping descriptions.
  Done when: the pane renders from a fixture of 20 skills, two with deliberately overlapping descriptions are linked, and the activated skill lights up in a replayed events file.

- **Bundle skills into role packs that pick themselves** — FEATURE — value 4 — effort M — risk low — category: skills
  Why: anthropics/skills ships 5 bundles, financial-services ships role plugins (10 agents, 7 verticals), and claude-code ships feature-dev and pr-review agents. "Work with anything" means a project should get the right bundle without the user choosing. `fm map` already detects stacks and cards (cc-skills, javascript, github-actions). Map each detected stack to a bundle and propose it once, with the metadata token cost shown.
  Done when: in a fixture repo with xlsx files, `fm skill suggest` proposes the spreadsheet bundle with its cost, and declining it is remembered.

- **Turn the cookbook patterns into skills the harness can invoke** — FEATURE — value 4 — effort L — risk med — category: skills, agents
  Why: claude-cookbooks lists evaluator-optimizer, orchestrator-workers and plan-big-execute-small. fm code already does plan then small steps. Package each pattern as a skill that sets a run's shape: how many workers, which model plans and which executes, and the spend cap. MIT licence allows adaptation with attribution.
  Done when: `fm code --pattern evaluator-optimizer "<request>"` runs a fixture task with a generator slot and a grader slot, and the events file shows both roles.

- **Show a skill's diff before an upstream update is adopted** — SECURITY — value 4 — effort S — risk low — category: skills, supply chain
  Why: the sha-pinned sources make a bump an explicit event. T-0791 covers 18 injection and supply-chain ideas that are deferred. A cheap first slice is a human-readable diff of SKILL.md and scripts, with any new shell, network or path reference flagged, before the pin moves.
  Done when: bumping a fixture skill to a version that adds a `curl` call shows the flagged line, and the pin does not move without approval.

- **Write the skill from the run, with the spec meter live (wild)** — FEATURE — value 4 — effort L — risk med — category: skills, wild
  Why: it combines "hatch a draft skill from a repeated habit", "live spec meter" and "adopt before authoring". When a habit repeats across closed tasks, search the adopted catalogue first. If nothing fits, draft a SKILL.md from the commands that actually passed, and show name/description limits and the activation token cost as it is edited.
  Done when: three fixture tasks with the same command sequence produce one draft that passes `fm skill lint` and names its source tasks.

- **Run a skill from a URL and sha in a throwaway sandbox (wild)** — FEATURE — value 3 — effort M — risk high — category: skills, wild
  Why: assumption: users will want to try something seen online before adopting it. Fetch it by URL and sha into an empty directory, lint it, run it only in a read-only guard profile on a copied project, then show what it did and discard it.
  Done when: `fm skill try URL@sha` leaves the real project byte-identical, prints the files the skill touched in the copy, and removes its temp directory.

- **Let skills teach the model with the tutorial's techniques (wild)** — FEATURE — value 3 — effort M — risk low — category: skills, prompting
  Why: the prompt-eng tutorial gives techniques (XML-tagged data vs instructions, allowing "unknown", quoting evidence, prefill). They are ideas only, as the repo has no licence. Foreman writes its own small "prompt hygiene" skill and applies it to fm code's JSON slots. Small local models gain most from the "unknown is allowed" and quote-your-evidence rules.
  Done when: `fm code bench` shows a lower rate of invented file paths on a weak local model with the hygiene prompts on than off, over N runs.

- **Give each skill a cost and licence label everywhere it appears (wild-ish)** — CLEAN — value 3 — effort S — risk low — category: skills, trust
  Why: licences are mixed (source-available vs Apache-2.0 vs none stated) and a sprawling catalogue hides that. Put licence, pin sha, metadata tokens and last-used date on one line in `fm skill list`, the home screen and the website examples.
  Done when: `fm skill list` prints those four fields for every installed skill and flags any missing a licence.

- **Retire skills that go unused or never helped** — CLEAN — value 3 — effort S — risk low — category: skills, hygiene
  Why: every adopted skill costs ~100 tokens per turn forever. Using the activation log and the score above, `fm skill prune` proposes removing skills never activated in N runs or showing no measurable effect. Removal is reversible, because the pin stays recorded.
  Done when: with a fixture log, `fm skill prune --dry-run` lists the unused skill with its saved tokens, and re-adding it restores the same sha.
