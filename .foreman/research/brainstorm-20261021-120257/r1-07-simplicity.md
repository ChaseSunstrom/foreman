# Brainstorm — lens: simplicity

- **Add one `fm add <thing>` verb for every upstream capability** — FEATURE — value 5 — effort M — risk med — category: integration
  Why: the user wants the six repos integrated "automatically", and the pack already lists separate paths: `fm plugins find/install`, runner registry, `code.toml`, `models.json`. Assumption: a single detector (GitHub URL, marketplace name, skill folder, binary on PATH, endpoint URL) is enough to route all of them.
  Done when: `fm add anthropics/skills`, `fm add codex` and `fm add http://localhost:11434/v1` each register the right kind in a scratch HOME, pinned and printed on one line.

- **Keep the six repos in one `upstreams.toml`** — CLEAN — value 5 — effort S — risk low — category: integration
  Why: the request names six repos with different shapes (marketplace.json, SKILL.md, registry.yaml, CHANGELOG). A manifest row of repo, kind, path globs, licence class and pinned sha means sync code has no per-repo branches. Fetching can use a blobless sparse `git clone` with no API tokens. Assumption: git is on PATH.
  Done when: adding a seventh repo is a one-line edit with no Python change, and `fm upstream sync` fetches only the globbed paths.

- **Use adopted skills and plugins in place, never vendored** — SECURITY — value 4 — effort M — risk med — category: supply-chain
  Why: the pack says marketplace sources are pinned to a sha, about half are third-party, and "third-party skills and plugins run nothing unguarded". Foreman would write a pointer file plus a guard wrapper and leave the upstream bytes untouched. Assumption: Claude Code can load a skill from a pinned checkout path.
  Done when: bumping a pin changes only the pointer file, and a skill script run through the wrapper is denied by the guard on a dangerous command.

- **Enforce a three-value licence class at the single copy chokepoint** — SECURITY — value 4 — effort S — risk low — category: legal
  Why: the pack records mixed licences. docx/pdf/pptx/xlsx are source-available, and the prompt tutorial has no stated licence, so it is ideas only. The classes would be `open`, `source-available` and `ideas-only`. Any code that copies upstream text checks the class once.
  Done when: attempting to copy `ideas-only` text into the repo fails with a message naming the class, and an `open` skill copies fine.

- **Reduce orchestration to the five cookbook loop shapes** — CLEAN — value 4 — effort M — risk med — category: orchestration
  Why: the cookbooks name evaluator-optimizer, orchestrator-workers, plan-big-execute-small, advisor and outcome-grader. Foreman has many overlapping flows: review, second, audit, duel and bench court. Assumption: each existing flow maps onto exactly one shape.
  Done when: one table maps every orchestrated verb to one of five shapes, a test fails on a verb with no row, and the mapped verbs share one runner.

- **Make SKILL.md the one format for playbooks and cards** — CLEAN — value 4 — effort M — risk med — category: format
  Why: the pack shows `plugin/skills/` holding 1161 files, and anthropics/skills defines name = folder and description ≤1024. Sharing that format means Foreman's own notes and adopted skills go through one loader and one description-length lint. Assumption: the 1161 files include playbook and card material that can be converted.
  Done when: `fm doctor` lints every Foreman playbook with the same checker it uses on an adopted skill, and one loader serves both.

- **Search `marketplace.json` locally with a stat-keyed cache** — PERFORMANCE — value 3 — effort S — risk low — category: discovery
  Why: claude-plugins-official's marketplace file is about 190 KB with 166+ entries, and `fm plugins find` already exists. A cached read of one file avoids cloning anything and covers the official, skills and finance marketplaces with the same code.
  Done when: `fm plugins find pdf` answers offline from the cache in under 100 ms on the second call.

- **Store each `fm code` run as a section of its task brief** — CLEAN — value 3 — effort M — risk med — category: state
  Why: `fm code --task ID` already uses the task's criteria and steps as the plan, with one run per task. A separate run store, journal and history duplicate that. Assumption: briefs tolerate an appended, size-capped runs section.
  Done when: deleting the run-store directory changes nothing about `fm code` history in the TUI, which reads the brief.

- **Lint Foreman's injected strings against eight prompt-tutorial rules** — CLEAN — value 3 — effort S — risk low — category: prompt-quality
  Why: the tutorial's lessons (data in XML tags, an explicit "unknown" allowance, quote evidence before conclusions) are checkable. Because it has no licence, only the ideas are used and the checks are written from scratch.
  Done when: a doctor check flags an injected string that mixes untrusted data into instructions without tags, and passes the fixed version.

- **Wild: Ten-exercise literacy probe replaces the capability profile** — FEATURE — value 4 — effort S — risk low — category: runners
  Why: assumption: ten tiny graded prompts (roles, tagged data, few-shot, JSON output, refusing to invent) score any runner in one number. They are cheaper and simpler than a full conformance suite, and `fm code runners` can show the score beside each runner.
  Done when: `fm code runners --probe` prints a 0–10 score per runner in under a minute on a local model, and a fake runner that ignores the format scores below 3.

- **Wild: Run one financial-services skill end to end per release** — FIX — value 3 — effort S — risk low — category: generality
  Why: "work with anything" is untested outside code. Running one finance skill on a seeded CSV through `fm code` shows quickly if the harness has hidden code-only assumptions. Assumption: the skill can run with a CLI runner and no paid connectors.
  Done when: the release gate runs the scenario on a fake runner, and fails if harness code needs a code-specific branch to complete it.

- **Wild: Offer the matching upstream skill in one line at intake** — FEATURE — value 3 — effort S — risk low — category: user-value
  Why: the user said they "shouldn't even need to ask". Matching the request against the cached catalog and printing "anthropics/skills has `pdf` (open licence, ~100 tokens), run `fm add`" costs nothing until accepted, and never auto-runs.
  Done when: `fm code "extract tables from this pdf"` prints exactly one offer line and installs nothing until `fm add` is run.
