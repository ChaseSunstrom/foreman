# foreman (plugin)

The Foreman plugin: hooks, the `fm` state CLI, skills, read-only agents and the visibility layer. It loads in place from this repo through the local `foreman` marketplace, so edits apply on `/reload-plugins`.

- **Hooks** (`hooks/hooks.json` → `hooks/hook <Event>`): SessionStart / UserPromptSubmit inject short factual state; PreToolUse runs the guard (fails closed) and scope notes; PostToolUse(+Failure) and subagent events feed the ledger and `fm watch`; PreCompact checkpoints; Stop runs the evidence gate and drive mode; MessageDisplay adds the reply badge; Notification and Stop emit terminal titles and notifications; SessionEnd records activity.
- **CLI** `bin/fm` (Python 3 stdlib): the only writer of `~/.claude/foreman/state/`. `fm --help`. Consent: `fm ask` (raises Claude Code's permission prompt; only the user's approval there grants it); audits: `fm task audit`; autonomy: `fm autonomy standard|full`; tool-less brainstorm children: `fm ideas`; headless: `fm serve` (Remote Control under systemd) and `fm run` (fresh session per task).
- **Skills**: `/foreman:intake`, `brainstorm`, `next`, `resume`, `reflect`, `playbooks`, `status`, `tidy`, `doctor`, `improve` (Claude starts these itself when you ask in plain words) and `capture` (you only), plus `/foreman:build`.
- **Agents**: `foreman:fm-recon`, `foreman:fm-reviewer` (read-only; the reviewer runs one audit lens per brief).
- **Protected core**: everything in `lib/`, `bin/`, `hooks/`, `evals/` and `rules/foreman.md`; edits need the user's yes to `fm ask ID core`.
- **Rules**: `rules/foreman.md`, symlinked into `~/.claude/rules/` by `fm install-user`.

Tests: `python3 -m unittest discover -s tests -t tests` · hook latency: `python3 tests/bench_hooks.py` · live scenarios: `python3 tests/e2e/scenarios.py` · install round trip: `python3 tests/e2e/roundtrip.py` · evals: `evals/README.md`.

Full system map: `../MASTER.md`. Remove: `./uninstall.sh`. Ported material and licenses: `THIRD_PARTY_LICENSES.md`.
