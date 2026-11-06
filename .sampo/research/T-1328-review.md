**Verdict: changes needed.** One crash, one silent fallback that sends code to a cloud CLI, one unguarded command-bearing config file, and a gap against the acceptance criteria. I read the code only and ran nothing.

The security rule you asked about holds. A command comes only from `RUNNERS` or `$FOREMAN_HOME/code.toml`:
- `code_runner` lives in `meta.json`, in the state directory, not the repo.
- `pick_runner` (fmcode.py:808) and `_runners --use` (fmcode.py:1409) both reject any name that isn't in `all_runners()` with a `work` template.
- `rm -rf ~ {prompt}` can't get through.

## lens: intent
- MEDIUM — plugin/lib/fmcode.py:1429 — The acceptance criterion says `fm code runners` lists "models and CLIs", but it builds rows only from `all_runners()`, and the JSON has no models. A user with ollama or a keyed cloud model sees none of them. — add model profiles (`m.profiles()`) as rows, or a "models:" section, marking which one a no-flag run uses. — high
- MEDIUM — plugin/lib/fmcode.py:1472 (the `pick_runner` loop) — The criterion says "the first installed CLI that can plan read-only". The code requires `verified`, so only claude is ever auto-picked. A machine with only codex or gemini, which have read-only modes, gets "No runner installed…", not a pick. It's documented in the README but is a narrower default than the user asked for. — user's call. Either accept it, or auto-pick an unverified planner with the existing note, since the tree check already stops a run whose plan writes a file. — medium

## lens: adversary
- MEDIUM — plugin/lib/fmguard.py:458-466 (`_is_core`) and :517-530 (`_protected_roots`) — `$FOREMAN_HOME/code.toml` is now a file that turns text into commands, but it is not a protected path. Foreman's own sources are listed there; `code.toml` isn't. A prompt-injected agent, or a worker CLI that can write outside the repo (such as gemini `auto_edit`), can write `runner = "x"` and `[runners.x] work = "sh -c '…' {prompt}"`. The next `fm code` then runs it. — add `os.path.join(fh, "code.toml")` to `_is_core` and `_protected_roots`. The same gap exists for `tui.toml` (noticed, not part of this change). — medium (I confirmed it isn't protected; I did not run a write)
- MEDIUM — plugin/lib/fmcode.py:812-816 — `pick_runner` treats any `ModelError` from `m.resolve(None)` as "no model set up" and picks claude. That also catches an unreadable `models.json` (fmmodels.py:136), and a named default whose server is down or whose name is a typo (fmmodels.py:182-185). Repro: `models.json` with `"default": "local-typo"` (or corrupt JSON), then `fm code "x"`. The repo's code goes to the claude CLI instead of a loud error. Only a `note` event is emitted, and sensitive repos are still refused. — auto-pick only when `m.configured()` shows no default and no profiles; let a config error propagate. — high

## lens: edge
- HIGH — plugin/lib/fmcode.py:1407, 1429 — With a malformed `code.toml` and no `--use`, `all_runners()` raises `CodeError` inside the `try`, so `rs` is never bound. The `except` sets `problem`, then `for n, r in rs.items()` raises `UnboundLocalError`. Repro: `echo 'runner =' > $FOREMAN_HOME/code.toml; fm code runners`. A traceback appears at the moment the user needs the diagnostic. — set `rs = {}` before the `try`, or print the problem and return. Add a test with a bad file. — high
- LOW — plugin/lib/fmcode.py:1419 — `--use` rewrites the first line starting with `runner =` anywhere in the file. A `runner` key under a table, or inside a multi-line string, would be edited instead of the top-level key. Nothing re-parses the result, and there's no lock around the read-and-write. — parse with `tomllib` and verify after the write, or document that the line must be top-level. — medium
- LOW — plugin/lib/fmcode.py:1403 — `--here` without `--use` is silently ignored. A project pin set with `--use X --here` can't be cleared from the CLI, and it overrides the global default. — error on `--here` alone; add `--use ""` or `--unset`. — medium

## lens: operator
- LOW — plugin/lib/fmcode.py:804-814, 1454 — A no-flag run probes local servers (up to 0.3 s each) in `pick_runner`, again in `choose_profile`, and `fm code runners` probes twice more. — resolve once and pass the result along. — medium

## lens: maintainer
- LOW — plugin/lib/fmcode.py:783-790 (`all_runners`) — A `work` or `plan` template without `{prompt}` is silently dropped. The user then sees only "isn't one fm code can run". — raise `CodeError` naming the key. — high
- LOW — plugin/tests/test_code_worker.py:405 — The by-name test covers `--use "rm -rf ~"`. It doesn't cover a hand-edited `meta.json` with `code_runner: "rm -rf ~ {prompt}"` going through `pick_runner`, and it doesn't cover a broken `code.toml` (the HIGH above). — add both tests. — high

## Acceptance criteria
- `fm code runners` lists models and CLIs: partly met. CLIs are listed (claude, codex, gemini, aider, opencode, qwen, cursor-agent, goose, amp, plus custom ones) with installed/works/plans/verified. Models are not listed.
- With no model set, the first installed CLI that can plan read-only is used, and it says so: partly met. It is restricted to verified planners (claude only). The `note` event says which runner was chosen (test at test_code_worker.py:383).
- `runner = NAME` in the config (global or per project) picks it: met. See `code_config`, `pick_runner`, and tests at lines 393 and 405.
- Verify with `python3 plugin/tests/run.py test_code test_code_worker`: not run.

## Implicit decisions
- Auto-pick requires `verified`, so only claude qualifies.
- A configured runner (global or project) overrides a working model, and the project's wins over the global one.
- Any `ModelError` counts as "no model".
- `--use` rewrites `code.toml` with a regex.
- A user's `[runners.X]` can override a built-in, and it keeps `verified` only if `plan` is untouched.
- A missing or unreadable `code.toml` fails every `fm code` run, even `--model`, because `choose_profile` and `worker_argv` always read it.
- `fm code runners` needs a project to resolve.

## Not checked
The CHANGELOG, `fmcore` `_GRANTS`, the canary and the firewall (skipped as you said). The TUI's rendering beyond `_on_note`. Test hermeticity (whether `CodeCase` hides real ollama or API keys). Python 3.12.7 or later is required by install.sh, so `tomllib` is fine.

**Noticed:** `$FOREMAN_HOME/tui.toml` (extensions) is likewise outside the guard's protected paths. `fm code --use` and `--here` can be written to the wrong place when the project's meta is missing, which I did not check.
