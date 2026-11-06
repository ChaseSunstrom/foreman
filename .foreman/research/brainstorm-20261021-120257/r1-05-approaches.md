# Brainstorm — lens: approaches

- **Pin the six repos in one `sources.lock`** — FEATURE — value 5 — effort M — risk low — category: integration
  Why: the user wants all six repos integrated "automatically", and a seventh should cost one line, not another bespoke adapter. Design: one entry per repo with URL, pinned sha and licence class (`copy` MIT/Apache, `index-only` source-available, `ideas-only` no licence). Sync uses `git ls-remote` plus the codeload tarball (stdlib `urllib`, no API rate limit), extracted into an empty directory with path-traversal and size caps. Moving a pin needs a yes and shows the changed-file list. Trade-off: less magic than live-following, but supply-chain-safe. Assumption: tarball access works offline-first with a cache.
  Done when: `fm sources sync` on a fixture with a tampered tarball (`../` member) refuses to extract, and a licence-class `ideas-only` source never writes a file outside the index.

- **Index all sources in local SQLite FTS5 as `fm sources find`** — FEATURE — value 4 — effort M — risk low — category: local-first
  Why: builders and `fm code` children currently can't ask "how does Anthropic do X" without re-reading repos. This is the do-less alternative to routing every pattern by hand. A lookup returns snippets with source, sha and licence class, which an offline small model can cite. Assumption: the system `sqlite3` has FTS5.
  Done when: `fm sources find "tool_choice parallel"` returns a cookbook hit with its sha and runs with the network off.

- **Serve skills to any runner via `fm skill index|load|run`** — FEATURE — value 4 — effort M — risk med — category: skills
  Why: SKILL.md is progressive disclosure (about 100 tokens of metadata, a body under 5k on activation), but only Claude loads it natively. Instead of per-CLI adapters, put the metadata index into the runner's rules file and let any CLI call `fm skill load NAME` through a shell. `scripts/` entries run only through `fm skill run`, under the guard, on a path declared in the skill. Trade-off: costs one shell call per activation, and works on codex, gemini and aider unchanged.
  Done when: a fixture skill with a `scripts/` file is loaded by a scripted fake CLI, and `fm skill run` of an undeclared path is refused by the guard.

- **Grade every model with a technique exam written from the tutorial's technique list** — FEATURE — value 4 — effort M — risk low — category: models
  Why: the tutorial's lessons (XML-tagged data vs instructions, prefill, few-shot, "unknown" escape, quote-the-evidence) each have a checkable answer, and `fm code` fills small checked JSON slots on arbitrary models. The tutorial has no licence, so write original exercises and take ideas only. The result is a per-model technique profile (takes prefill? obeys XML fences? hallucinates instead of "unknown"?) that picks the slot-prompt style. Trade-off: needs about 40 cheap calls per model, cached by model id.
  Done when: `fm code bench --exam MODEL` writes a profile and a slot prompt changes style for a model that failed the XML-fence item.

- **Turn cookbook notebooks into `fm code bench` cases** — FEATURE — value 3 — effort M — risk low — category: bench
  Why: `.ipynb` is JSON, so stdlib can pull out prompts, tool schemas and expected shapes, and `registry.yaml` needs only a line parser. Result: structured-output, tool-use and eval cases that exercise runners on Anthropic's own patterns. MIT licence permits copying. Assumption: notebooks keep their current cell layout.
  Done when: `fm code bench --from-cookbook` generates at least 10 cases from a pinned fixture notebook set and runs them against a fake runner.

- **Ship a hostile-skill and schema-drift zoo for the ingestion path** — SECURITY — value 4 — effort S — risk low — category: supply chain
  Why: the constraint is that third-party skills and plugins run nothing unguarded. Write about 30 synthetic bad inputs: a `source` with `..`, a description carrying instructions, `curl|sh` in `scripts/`, a marketplace sha mismatch, name≠folder, an over-long description. Also add golden fixtures of valid shapes so a new upstream frontmatter key fails loudly instead of being misparsed.
  Done when: every zoo item is refused with a named reason, and a fixture with an unknown top-level key is reported as drift.

- **Verify office deliverables with a stdlib OOXML asserter** — FEATURE — value 3 — effort M — risk low — category: verification
  Why: anthropics/skills includes docx/xlsx/pptx and financial-services produces spreadsheets, so "work with anything" needs proof beyond code. xlsx, docx and pptx are zip plus XML, which `zipfile` and `ElementTree` can read. Criteria become checks like cell B7 equals 42, sheet count, slide count, heading present. Trade-off: no rendering fidelity.
  Done when: a verify command `fm check office report.xlsx --cell Sheet1!B7=42` fails red on a fixture with a wrong value and passes green after the fix.

- **Follow marketplace renames and yanks on installed plugins** — FEATURE — value 3 — effort S — risk low — category: plugins
  Why: claude-plugins-official carries renames and per-plugin sha pins. `fm plugins` can compare the installed set to the pins and offer a one-yes migration for renamed entries, and warn on a pin that vanished. Cheaper than the full diff-on-update idea already listed. Assumption: the `renames` key stays in the schema.
  Done when: a fixture marketplace with a rename makes `fm plugins check` print the old→new line and the migrate command.

- **Recommend the top three plugins per project, never auto-install** — FEATURE — value 3 — effort S — risk low — category: plugins
  Why: 166+ plugins is a catalogue, not a decision. Score each entry against `fm map` (stack, existing MCP, hook overlap) and show three with reasons. Install goes in as probation under the guard. Trade-off: a heuristic score, so label it as one.
  Done when: for a Python fixture repo, `fm plugins suggest` lists exactly three with a reason each and installs nothing.

- **Wild: Synthesize "strategy cards" from cookbook patterns, accepted only on a bench win** — FEATURE — value 4 — effort L — risk med — category: agents
  Why: evaluator-optimizer, orchestrator-workers and plan-big-execute-small are prose today. Have a model draft each as a data card (stages, who runs them, stop rule) and keep it only if `fm code bench` beats the default plan shape at equal budget. Trade-off: slow overnight spend, but the harness's own routing improves with evidence. Assumption: bench noise is controlled (see T-1260).
  Done when: one accepted card appears in the registry with its bench delta and noise band, and a rejected one is logged with its score.

- **Wild: Run a rival-hook arena on the claude-code repo's hook examples** — SECURITY — value 3 — effort M — risk low — category: guard
  Why: the repo ships example hooks (the bash validator, security-guidance, hookify rules). Run each against Foreman's guard corpus, in a scratch HOME and with no network, and list every command where they disagree with `fm guard`. Disagreements become reviewed corpus entries, and the guard only tightens. Trade-off: it finds rule gaps, not new features.
  Done when: `fm guard arena` prints a disagreement table for the pinned examples and a fixture disagreement lands as a corpus case.

- **Wild: Generate a cookbook-style notebook from any `fm code` run** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: the user asked for better real examples on the site. A run's event stream (replayable via `--events FILE`) can become an `.ipynb` of request, plan, red checks, diff and green proof, written with stdlib `json`. It is a shareable artifact and a regression fixture for the site build.
  Done when: `fm code export --ipynb RUN` writes a notebook that parses as valid nbformat 4 and the site build lists it.
