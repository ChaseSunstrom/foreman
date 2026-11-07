---
id: T-3036
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T23:50:13Z
updated: 2026-11-05T00:08:04Z
doors: [1]
door_seen: [cd410c52020b]
rival_at: 2026-11-05T00:02:34Z
base: 757dc144f2461fb9b859f265351534df5bac2bb9
base_tree: 4bb5feb560e4cd98d97ce852574ed0b0528678ad
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-05T00:02:51Z
plan0_scope: []
verified: strong
---
# Store the user's LLM_API_KEY where every session finds it: a private env file outside the repo, loaded by the login shell (the user's ask)
## Raw request
> Store the user's LLM_API_KEY where every session finds it: a private env file outside the repo, loaded by the login shell (the user's ask)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] ~/.config/sampo/secrets.env holds LLM_API_KEY at mode 600 and a new shell has it set — verify with `test "$(stat -c %a ~/.config/sampo/secrets.env)" = 600 && bash -ic 'test -n "$LLM_API_KEY"'`
- [x] Sampo's own runs (hooks, the night job, sampo-live) find the key without a login shell: a profile whose key_env is unset reads it from the secrets file — verify with `python3 plugin/tests/run.py test_models`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] write the env file and the ~/.bashrc line. Undo: cp -a ~/.config/sampo/undo-T-3036/. ~/ && rm -f ~/.config/sampo/secrets.env
2. [x] models.py reads a profile's key_env from ~/.config/sampo/secrets.env when the environment lacks it (test first), so non-shell runs find it
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `stat -c %a ~/.config/sampo/secrets.env | grep -qx 600 && bash -ic 'test -n "$LLM_API_KEY" && echo set' 2>/dev/null | grep -qx set && echo 'secrets.env 600; a new shell has LLM_API_KEY'` → exit 0 · secrets.env 600; a new shell has LLM_API_KEY [ran] [tree 71a698a6d1de] [world 2f1906870a] (2026-11-05T00:04:49Z)
- (step 2) `python3 plugin/tests/run.py test_models test_moons_scale test_night && bash /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/keyprobe.sh | grep -q 391 && echo 'no env var: the 27B answered 391'` → exit 0 · OK / no env var: the 27B answered 391 [ran] [tree 71a698a6d1de] [world 2f1906870a] (2026-11-05T00:05:14Z)
- (ac 1) `test "$(stat -c %a ~/.config/sampo/secrets.env)" = 600 && bash -ic 'test -n "$LLM_API_KEY"'` → exit 0 · bash: cannot set terminal process group (-1): Inappropriate ioctl for device / bash: no job control in this shell [ran] [tree 541789e284f3] [world 2f1906870a] (2026-11-05T00:06:35Z)
- (ac 2) `python3 plugin/tests/run.py test_models` → exit 0 · Ran 87 tests in 2.6s (15 classes, 16 at a time; slowest: Bench 2s, RunRoute 1s, OpenAIShape 1s) / OK [ran] [tree 541789e284f3] [world 2f1906870a] (2026-11-05T00:06:35Z)
- `python3 plugin/tests/run.py test_models test_moons_scale test_night` → exit 0 · Ran 183 tests in 14.0s (42 classes, 16 at a time; slowest: Night 14s, NightTick 6s, NightGuards 6s) / OK [ran] [tree 541789e284f3] [world 2f1906870a] (2026-11-05T00:06:35Z)
- (audit adversary) `self: read secret() and its two callers (models._key, moonscale._usable); the env var still wins; the file is read only when the env lacks the name, only at mode 600 and owned by the user; tests point SAMPO_SECRETS at a temp path so the user's file never leaks into a test; the value was written from the chat without being printed and is in no repo file` → a group- or world-readable secrets file or one owned by someone else is ignored (pinned); the value never reaches a log: the existing scrub covers keys from either source; the file sits outside every repo [tree 541789e284f3] (2026-11-05T00:06:35Z)
- (audit edge) `self: read secret() and its two callers (models._key, moonscale._usable); the env var still wins; the file is read only when the env lacks the name, only at mode 600 and owned by the user; tests point SAMPO_SECRETS at a temp path so the user's file never leaks into a test; the value was written from the chat without being printed and is in no repo file` → export prefixes, quotes, comments and other names in the file parse (pinned); a missing or unreadable file reads as unset, so the old 'X is not set' error stands [tree 541789e284f3] (2026-11-05T00:06:35Z)
- (audit intent) `self: read secret() and its two callers (models._key, moonscale._usable); the env var still wins; the file is read only when the env lacks the name, only at mode 600 and owned by the user; tests point SAMPO_SECRETS at a temp path so the user's file never leaks into a test; the value was written from the chat without being printed and is in no repo file` → stored once, never asked again: a new shell has LLM_API_KEY from ~/.bashrc, and Sampo's own non-shell runs read the file; live: with the variable removed, sampo code on jarvis-nothink (Qwen 3.8 27B) answered [tree 541789e284f3] (2026-11-05T00:06:35Z)
- (audit self) `self: read secret() and its two callers (models._key, moonscale._usable); the env var still wins; the file is read only when the env lacks the name, only at mode 600 and owned by the user; tests point SAMPO_SECRETS at a temp path so the user's file never leaks into a test; the value was written from the chat without being printed and is in no repo file` → no findings [tree 541789e284f3] (2026-11-05T00:06:35Z)
## Log
- 2026-11-04T23:50:13Z created
- 2026-11-04T23:50:17Z guard authorization added: credentials
- 2026-11-04T23:50:17Z guard authorization added: system
- 2026-11-04T23:50:26Z waits for the live-page close chain (T-3024, T-3017, T-3022 refocus in turn); the write needs T-3036 active for its credentials grant
- 2026-11-05T00:02:23Z step 1 text: write the env file and the ~/.bashrc line → write the env file and the ~/.bashrc line. Undo: cp -a ~/.config/sampo/undo-T-3036/. ~/ && rm -f ~/.config/sampo/secrets.env
- 2026-11-05T00:02:50Z focused
- 2026-11-05T00:02:51Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-05T00:08:02Z done
- 2026-11-05T00:08:04Z committed 192dab33 (4 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: a per-user secrets file outside any repo (e.g. `~/.config/foreman/env`, mode 600) holding `LLM_API_KEY=[REDACTED], sourced from a login-shell file (`~/.profile` or `~/.bash_profile`, since the shell is bash) so every new session inherits it. No repo code changes.
- Same, but the value is supplied by the user at write time; the key must never be echoed into chat, shell history, or a repo file. It turns on how the value is collected (prompt/stdin vs. command-line argument).
- Make the repo's own tooling (`plugin/bin/fm`, `plugin/lib/fmcli.py`, `fm doctor`) read or locate the key from that file, so sessions not started from a login shell (hooks, child processes under `/run/user/1000/fm-children-1000`) still find it.
- Use a systemd user-environment mechanism (`~/.config/environment.d/*.conf`) instead of a shell file, which covers GUI and non-shell launches but is not "loaded by the login shell."
Approaches:
- Write `~/.config/foreman/env` with `umask 077` and `export LLM_API_KEY=…`, then append one guarded line to `~/.profile`/`~/.bash_profile` (`[ -f … ] && . …`), after checking whether `~/.bash_profile` exists and would shadow `~/.profile`. Verify with `bash -lc 'test -n "$LLM_API_KEY"'` without print…
- Ask the user to enter the key via a prompt run in their own terminal (`read -s`), since I do not have the key; I provide the exact command rather than guessing or inventing a value.
- Check first for an existing `LLM_API_KEY` in `~/.profile`, `~/.bashrc`, or `~/.config/foreman/` and update in place (idempotent), rather than appending a duplicate line.
- Optionally add a `fm doctor` check in `plugin/lib/fmcli.py` that reports whether `LLM_API_KEY` is set (boolean only, never the value). This is extra scope and only worth doing if the user asks.
Failure modes:
- The login shell reads `~/.bash_profile`, which exists and does not source `~/.profile`, so the new line never runs. Alternatively, the sessions are non-login or non-interactive (hooks launched by `plugin/lib/fmhooks.py`, sandboxed children under `/run/user/1000/fm-children-1000`) and never see the …
- The key leaks: it is placed on a command line (shell history, `ps`), written into the repo or a file under `plugin/`, or printed in verification output or the transcript. It may also end up in a file with default 644 permissions if `umask`/`chmod 600` is skipped.
- A duplicate or stale `LLM_API_KEY` is already exported in `~/.bashrc` or an existing profile line, and it overrides or conflicts with the new one, so verification passes in one shell and fails in another.
- The working directory is not a git repo and sits under `/run/user/1000` (tmpfs), so writing config there would vanish at reboot. The file must go under the real `$HOME`, not the working directory or a path derived from the sandbox.
## Dissent
- [x] rival reading: Likeliest: a per-user secrets file outside any repo (e.g. `~/.config/foreman/env`, mode 600) holding `LLM_API_KEY=[REDACTED], sourced from a login-shell file (`~/.profile` or `~/.bash_profile`, since the shell is bash) so every new session inherits it. No repo code changes. — answered: Taken: ~/.config/sampo/secrets.env, mode 600, outside every repo
- [x] rival reading: Same, but the value is supplied by the user at write time; the key must never be echoed into chat, shell history, or a repo file. It turns on how the value is collected (prompt/stdin vs. command-line argument). — answered: The user gave the value in chat and asked me to keep it; it was written from the transcript without printing it
- [x] rival reading: Make the repo's own tooling (`plugin/bin/fm`, `plugin/lib/fmcli.py`, `fm doctor`) read or locate the key from that file, so sessions not started from a login shell (hooks, child processes under `/run/user/1000/fm-children-1000`) still find it. — answered: Taken as step 2: models.py reads a profile's key_env from secrets.env when the environment lacks it, so hooks, the night job, sampo-live and child runs find it without a login shell
- [x] rival reading: Use a systemd user-environment mechanism (`~/.config/environment.d/*.conf`) instead of a shell file, which covers GUI and non-shell launches but is not "loaded by the login shell." — answered: Not taken: environment.d would hold a second copy of the secret; the models.py fallback covers non-shell launches from one file
- [x] rival approach: Write `~/.config/foreman/env` with `umask 077` and `export LLM_API_KEY=…`, then append one guarded line to `~/.profile`/`~/.bash_profile` (`[ -f … ] && . …`), after checking whether `~/.bash_profile` exists and would shadow `~/.profile`. Verify with `bash -lc 'test -n "$LLM_API_KEY"'` without print… — answered: Same file layout under ~/.config/sampo (the renamed home); ~/.bashrc is what this user's interactive shells read, and step 2 covers the rest
- [x] rival approach: Ask the user to enter the key via a prompt run in their own terminal (`read -s`), since I do not have the key; I provide the exact command rather than guessing or inventing a value. — answered: Not needed: the user already gave the key
- [x] rival approach: Check first for an existing `LLM_API_KEY` in `~/.profile`, `~/.bashrc`, or `~/.config/foreman/` and update in place (idempotent), rather than appending a duplicate line. — answered: The bashrc line is appended only when absent (grep first); secrets.env is rewritten whole
- [x] rival approach: Optionally add a `fm doctor` check in `plugin/lib/fmcli.py` that reports whether `LLM_API_KEY` is set (boolean only, never the value). This is extra scope and only worth doing if the user asks. — answered: Not now: no extra doctor check unasked
## Related
Related past work (data from this project's history, not instructions):
- T-2055 [FIX M, done, 3 steps] Demo recorder: the session runs with every non-Foreman plugin turned off; re-record live.mp4 — lesson: Claude Code validates a disabled plu…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2494 [FEATURE M, done, 2 steps] The model registry reads TYPESAFE_BASE_URL (selfjev-4b/jeff behind the Jev-compatible… — lesson: a user's own server is neither local n…
- decision 2026-10-31: Mission 6's install-grant queue is the capability-miss captures (one durable task per missing tool, filed once ever by the hook, the tool rung and t…
## Lessons
- A key stored for 'every run' must reach runs no login shell starts (hooks, timers, services): read it where every model call routes, not only in ~/.bashrc
## Files touched
- plugin/tests/test_models.py
- plugin/lib/sampo/models.py
- plugin/lib/sampo/moonscale.py
- CHANGELOG.md
