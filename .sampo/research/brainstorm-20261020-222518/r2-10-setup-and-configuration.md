# Brainstorm — lens: setup and configuration

- **Explain config with provenance** — FEATURE — value 5 — effort M — risk low — category: config
  Why: the user asks for "better config/setup", and the pack plans a registry (T-1328) but no way to see why a value won. `fm code config explain KEY` would print the winning value and each layer that set it (flag, env, project `.foreman`, user `models.json`, default, auto-detected), plus the shadowed values.
  Done when: with a project override and an env var both set, `fm code config explain runner` lists both layers, marks the winner, and a test asserts the output.

- **Run a first-launch wizard that is also the doctor** — FEATURE — value 5 — effort M — risk low — category: setup
  Why: the user hit a missing `fm` on PATH, no model so the first request failed until `m` was pressed, and a silent planner. One screen could check PATH, detect runners, probe each with a one-token call, and write one config line.
  Done when: in an empty HOME with only `claude` installed, `fm code setup --yes` writes the default runner, exits 0, and a following `fm code "question"` answers without a prompt.

- **Probe every runner for its real startup tax** — FEATURE — value 5 — effort M — risk low — category: runners
  Why: the nixie run showed 66k–133k input tokens per nested call. Setup should measure each runner's launch cost (tokens, seconds to first event) once, store it, and show it in the picker with a "slim profile available" hint.
  Done when: `fm code runners` prints a tokens-at-launch column per runner, and a fake-CLI test shows the measured value is stored and re-measured only when the CLI version changes.

- **Detect duplicate Foreman installs and choose one owner** — FIX — value 4 — effort M — risk med — category: install
  Why: the user asked to "prevent duplicate things when FM is installed as a claude plugin". Setup should find every Foreman copy (plugin dir, `~/.local/bin` link, pip or clone), name which one answers `fm`, and warn when two hook sets would both fire.
  Done when: with a fixture holding a plugin copy and a linked clone, `fm doctor` reports both with paths, names the active one, and a nested worker session registers hooks exactly once.

- **Write layered project config that travels with the repo** — FEATURE — value 4 — effort M — risk low — category: config
  Why: multiple projects need different defaults (nixie may want codex, another a local Ollama). `.foreman/code.toml` should hold the runner, test command, step caps and spend cap, with a committed or git-ignored choice offered at creation.
  Done when: two fixture projects with different runner lines each launch their own runner from the home screen, and removing the file falls back to the user default.

- **Validate config with line-accurate errors and a last-good copy** — FIX — value 4 — effort S — risk low — category: reliability
  Why: `models.json` is read by two call sites, and a typo there would break every run. Parse errors should name the file and line, and `fm code` should fall back to the last good atomically written copy and say so.
  Done when: a corrupted `models.json` produces an error naming the line, the run still starts on the last-good copy, and a test covers both.

- **Import runners from the tools already on the machine** — FEATURE — value 4 — effort M — risk med — category: onboarding
  Why: the user wants it to manage ANY CLI or model with no setup. Setup should read env keys (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`), Aider and Codex config files, and local Ollama or LM Studio ports, proposing entries without copying secrets into the file (it stores a reference to the env var).
  Done when: with a fake Ollama listening and a key in the environment, `fm code runners --import` lists both, and the resulting file holds no key value.

- **Learn an unknown CLI from its help text** — FEATURE — value 3 — effort L — risk med — category: runners
  Why: the user said "ANY CLI". Today a `CMD {prompt}` template is hand-written. Setup could read `--help`, find the prompt flag, the JSON-output flag and the non-interactive flag, and propose a template that it then verifies with a harmless probe.
  Done when: given a fake CLI with a nonstandard prompt flag, `fm code runners add ./fakecli` produces a working template and its probe passes.

- **Run setup friction through the self-notice loop** — FEATURE — value 4 — effort M — risk low — category: self-improvement
  Why: the user said "I shouldn't even need to ask". Setup failures (command not found, no model, silent planner) should be logged locally as friction events, and a repeated one opens a diagnostic task with the evidence attached.
  Done when: three simulated "no model configured" failures create one task naming the cause, and a fourth does not create a duplicate.

- **Wild: Accept a pasteable setup code** — FEATURE — value 3 — effort M — risk low — category: sharing
  Why: wild; assumption: users run several machines. One short string encodes runners, default, theme and caps (never secrets) so a new machine takes one paste.
  Done when: `fm code setup --export` followed by `--import <code>` on a clean HOME reproduces the same `config explain` output minus secrets.

- **Wild: Hold a "rehearsal" run before trusting a new runner** — FEATURE — value 4 — effort M — risk low — category: setup
  Why: wild; assumption: a runner can pass a probe yet fail real work. Setup would run a tiny seeded task from `fm code bench` in a scratch repo and show a grade before the runner becomes the default.
  Done when: adding a fake runner triggers the rehearsal, a failing fake is not made default, and the grade is saved with the runner entry.

- **Wild: Ask for config in plain words** — FEATURE — value 3 — effort M — risk med — category: config
  Why: wild; the user writes loosely ("use codex for nixie"). A command box turns that sentence into a proposed config diff, shown and applied only on confirm, through the same validator as hand edits.
  Done when: typing "use codex for nixie" yields a diff to nixie's project config and nothing is written until confirmed, with a test for both paths.

- **Wild: Offer a "token diet" profile for nested Claude** — PERFORMANCE — value 5 — effort M — risk med — category: performance
  Why: wild; the nixie stall came from nested Claude loading every plugin and rule. A named profile launches workers with only the guard and the chosen project settings, and reports the tokens saved against the full load.
  Done when: a nested planner call under the diet profile measures at least 50% fewer input tokens than the default in a recorded fixture, and the guard still refuses a forbidden command.
