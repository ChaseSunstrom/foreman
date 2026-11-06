# Brainstorm — lens: setup and configuration

- **Add `fm code setup` as a one-screen first-run wizard that is also the doctor** — FEATURE — value 5 — effort M — risk low — category: setup
  Why: user hit `fm` not on PATH, `fm code` erroring with "needs a request", and no model until pressing `m`. Assumption: a wizard fits stdlib-only curses/ANSI.
  Done when: in an empty HOME, `fm code setup --yes` detects installed CLIs/endpoints, writes one config file, fixes the PATH link, and a following `fm code "question"` answers with no prompts.

- **Put every setting in one layered config with `fm code config` get/set/explain** — FEATURE — value 5 — effort M — risk low — category: config
  Why: T-1328 wants "one config line picks the default"; `models.json` is resolved in two places; themes, motion, keys and runners are scattered. Assumption: user, project, and env layers are all needed.
  Done when: `fm code config explain runner` prints the winning value and which layer (env, project, user, default) set it, and a project value overrides the user one in a test.

- **Detect and refuse duplicate Foreman when run as a Claude plugin worker** — FIX — value 5 — effort M — risk med — category: dedupe
  Why: user asked to "prevent duplicate things when FM is installed as a claude plugin"; nested Claude loads Foreman's hooks and rules (66k–133k tokens/call), which T-1327 only partly covers.
  Done when: a nested `claude -p` launched by fm code shows exactly one Foreman hook chain, tested by counting hook invocations with the plugin installed and fm code running.

- **Run a preflight "can this runner work here?" probe per project and runner** — FEATURE — value 4 — effort S — risk low — category: reliability
  Why: the nixie run "just isn't doing anything" for minutes. Assumption: a 5-second smoke call (tiny prompt, token count, auth check) catches most stalls.
  Done when: with a runner whose binary hangs, `fm code` reports "claude: no output in 8s, probable cause X" before planning begins.

- **Store per-project overrides in `.foreman/code.toml`, committed or ignored by choice** — FEATURE — value 4 — effort S — risk low — category: projects
  Why: the user manages multiple projects needing different runners, gates, and budgets. Assumption: they want nixie on a local model and Foreman on Claude.
  Done when: two sample projects with different runners each launch the right one from the home screen, with no flags.

- **Import runner config from other tools (Claude settings, Aider config, Codex config, env API keys)** — FEATURE — value 4 — effort M — risk med — category: onboarding
  Why: "works with no setup" across ANY CLI or model. Assumption: keys are only read, never copied, unless the user opts in.
  Done when: with only `OPENAI_API_KEY` exported, `fm code runners` lists an OpenAI runner marked "from env", and no key appears in any written file.

- **Validate config at load with line-accurate errors and a safe fallback to last-good** — FIX — value 4 — effort S — risk low — category: reliability
  Why: a typo in `models.json` or a theme must not make `fm code` fail to open the app. Assumption: today it raises or fails silently.
  Done when: a broken config opens the app with a banner naming file:line and runs on the last-good copy.

- **Add `fm code install-check` that audits shell integration (PATH, completions, tmux, terminal capability)** — FEATURE — value 3 — effort S — risk low — category: setup
  Why: `fm` was missing from the user's shell because of a missing link.
  Done when: the check detects a missing `~/.local/bin/fm`, offers the fix, and passes on re-run.

- **Wild: Let Foreman notice setup friction itself and repair it unprompted** — FEATURE — value 5 — effort L — risk med — category: self-healing — wild
  Why: the user says "foreman should be able to figure it out" without being asked. Assumption: friction phrases and silent stalls are detectable from the event log.
  Done when: a replayed log of a 3-minute silent planner produces a proposed fix task (e.g. "slim nested context") with no user request.

- **Wild: Offer a "token diet" profile that reports and trims what nested workers load** — PERFORMANCE — value 4 — effort M — risk med — category: cost — wild
  Why: 66k–133k input tokens per call came from loading all plugins and rules.
  Done when: `fm code diet` shows a per-source token breakdown and a run with the lean profile cuts input tokens by at least 50%, measured.

- **Wild: Support a shareable setup as one pasteable code (runners, theme, defaults, no secrets)** — FEATURE — value 3 — effort S — risk low — category: sharing — wild
  Why: assumption: users move between machines and want identical setups.
  Done when: `fm code config export` yields a short string that `import` restores byte-identically, and it contains no keys or paths.

- **Add a "which runner for which task" router with learned defaults from bench grades** — FEATURE — value 4 — effort M — risk med — category: routing
  Why: `fm code bench` already grades models. Assumption: bench results can pick a cheap runner for docs and a strong one for fixes.
  Done when: with two benched runners, a docs request picks the cheaper one and `fm code why-runner` states the bench numbers behind it.
