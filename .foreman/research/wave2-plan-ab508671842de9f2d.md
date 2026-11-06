=== T-1069
INTERPRETATION: A task marked race gets two builders in separate worktrees, and the reviewer picks the better diff by tests, size and review. Nothing exists yet: `fm lane` allows one lane per task (`meta["lane"]`, branch `foreman/<id>`, `plugin/lib/fmlanes.py:75-95`). The rest of wild C13 is not built: the bid/lane/plan/lesson/task auctions, standing seats, bus factor, seat library, sprint-review seat, per-library competence, tic atlas, Thompson bandit, RFC round, peer-review round robin and patch tree search. I could not read the cluster file's wording for them, so these are listed by title only.
APPROACH: (a) Overload `fm lane new` with `--race`. (b) A new `fm lane race ID` action plus `fm lane pick ID a|b`. (c) A new module. Choose (b), in `fmlanes.py`: `race()` makes lanes `.lanes/<id>-a` and `-b` on `foreman/<id>-a` and `-b`, and records `meta["race"]={a,b}`. `pick` and a bare `race ID --score` run each lane's criteria, take `git diff --shortstat` against HEAD, and print a table of tests/size/review per side. `pick` merges the winner via `merge()`, removes both lanes and logs `race_pick`. `fm task set ID race=true` marks the task, and `builder_brief` refuses race on L. The C13 remainder is L and goes in later M pieces. Piece 1 is race. Then auctions plus the bandit as `fm route`. Then the seats and the round-robin and RFC rounds.
AC: `fm lane race T` makes two lanes and `fm lane race T --score` prints tests, lines changed and a leader :: python3 plugin/tests/run.py test_race
AC: `pick` merges only the winner, removes both lanes, and refuses an L task :: python3 plugin/tests/run.py test_race
STEP: Failing tests: in a temp repo, race on an S task creates two worktrees, and `--score` output contains "tests" and "lines" for both. `pick a` leaves branch `foreman/T-a` merged, `-b` gone, and a `race_pick` event. Race on an L task, or a second race, raises PolicyError.
STEP: Add the `race` and `pick` actions to the `fm lane` choices (`fmcli.py:4915`), `--score` as a flag, and `race()`, `score()` and `pick()` in `fmlanes.py`.
STEP: Show both lanes in `fm lane list` through the `meta["race"]` mapping.
SCOPE: plugin/lib/fmlanes.py, plugin/lib/fmcli.py, plugin/tests/test_race.py
TIER: L

=== T-1078
INTERPRETATION: The pane's task block shows each stage's time next to the project's typical time, green when under and red when over. Stage times are not stored today. `typical()` (`fmwatch.py:219`) only gives focus-to-done medians per TYPE/TIER, and `story()` (`fmrecall.py:877`) already derives chapter times from the ledger. The other C22 ideas (control-room SPC, eval bar, replay archive, push-to-talk, language server, animatic, mock layouts, README clean-room walk, README pictures in CI, explorers) are not built. I could not read their wording in the cluster file, so I name them by title only.
APPROACH: (a) Compute splits in `fm ui` from the ledger. (b) Compute them in the TS mod. (c) Store a stage event at each transition. Choose (a): `fmwatch.splits(events, act)` maps the active task's events to `{stage, s, typical_s, delta}`. It uses the `CHAPTERS` event sets, and typical is the median over closed same TYPE/TIER tasks (3 or more). It is exposed as `view()["active"]["splits"]`, and the twin is typed in `mods/foreman-ui/types/index.d.ts`. `register.tsx` draws one row per stage in `C.ok` or `C.err`, near the elapsed-time line around `register.tsx:1122`. The rest of C22 is its own pieces: control-room SPC and eval bar, replay archive, and dev tooling.
AC: `fm ui --json` active has splits with typical and a sign per stage :: python3 plugin/tests/run.py test_splits
AC: the pane shows the splits in the task block :: cd mods/foreman-ui && ~/.local/bin/claude plugin test .
STEP: Failing tests: seed a ledger with 3 closed FIX/M tasks and an active one whose executing stage is slow. `splits` has an executing entry with `delta>0`. Stages with fewer than 3 samples have no typical value. Pane test: a split row renders for each stage and the over-typical one uses the err colour.
STEP: Add `splits()` to `fmwatch.py` and wire it into `view()`.
STEP: Add the TS type and the rendering in `register.tsx`.
SCOPE: plugin/lib/fmwatch.py, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/types/index.d.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/lib/ui-demo.json, plugin/tests/test_splits.py
TIER: M

=== T-1080
INTERPRETATION: One daily autonomy budget counts destructive asks, reverts and failed closes. When it is spent, autonomy slows: the drive stops starting side work and tasks wait for the user. The rest of C8 is: consent envelope, auditable ladder, quarantine after a bad outcome, capability chains, secrets broker, sterile cockpit, load-shedding order, turnaround contract and hold/witness points. Only the USD and usage budget exists (`fmbudget.py`, with `degrade()` at `fmbudget.py:168`). `fmoutcomes.py:40` already finds reverted tasks, and the ledger already has `guard_block` and `enforce` events.
APPROACH: (a) Extend `fmbudget` with a risk ledger. (b) A new `fmrisk` module. (c) Put the count in `meta`. Choose (b), because C8 has many ideas. `fmrisk.spent(p)` counts today's ledger events by weight: guard_block category git-destructive, revert, `done_blocked`. `fm risk` prints the budget, what is spent and a consent envelope (what is allowed at which level). `fmrisk.slow(p)` is wired into `fmbudget.degrade()` and `c.waits_on_user`. Split into M pieces: 1. budget, `fm risk` and slowing, plus the ladder view and quarantine. 2. envelope, capability chains, secrets broker and hold/witness points. 3. sterile cockpit, load-shedding order and turnaround contract.
AC: `fm risk --json` reports spent, cap and slowed, and the slowing rises once the cap is reached :: python3 plugin/tests/run.py test_risk
AC: when spent, `degrade()` returns a reason and `fm risk set --day N --because` changes the cap :: python3 plugin/tests/run.py test_risk
STEP: Failing tests: log 3 weighted events, set a cap of 2, and `fm risk` shows "slowed". `fmbudget.degrade()` is non-empty. The ledger-day boundary resets the count.
STEP: Create `plugin/lib/fmrisk.py` and a lazy `risk` command in `fmcli.py`.
STEP: Hook `slow()` into `degrade()` in `fmbudget.py`.
SCOPE: plugin/lib/fmrisk.py, plugin/lib/fmbudget.py, plugin/lib/fmcli.py, plugin/tests/test_risk.py
TIER: L

=== T-1081
INTERPRETATION: The pane gets a colourblind-safe palette and a time scrubber. The palette is one fixed object, `C` (`kit.ts:4-20`), with ok green and err red. `motion` is the only setting today (`state.ts:32`). The scrubber needs history: `view().history` (`fmwatch.py:107`) and `done_days` exist, but no per-time snapshots do.
APPROACH: (a) A `palette` option (`default` or `cb`) that swaps `C` through a getter. (b) Add a scrubber that replays `history`. (c) Both in one pass. Choose (c). `kit.ts` gets `PALETTES` (blue/orange instead of green/red, plus a glyph on every ok/err state so colour is not the only cue). `cfg.palette` is read from the plugin options in `register.tsx` near line 537. The scrubber is a `[` and `]` key pair that moves a cursor over `v.history` (the last 60 events), and the task block shows the state "as of" that event. An `@live` key returns to now.
AC: the option `palette: 'cb'` swaps ok/err colours, and the error state still carries a glyph :: cd mods/foreman-ui && ~/.local/bin/claude plugin test .
AC: the scrubber shows the earlier event, and the live key restores now :: cd mods/foreman-ui && ~/.local/bin/claude plugin test .
STEP: Failing tests in `foreman-ui.test.tsx`: with `options.palette 'cb'` the rendered ok/err colours differ from the default, and every err row has a glyph. After the scrubber key the pane shows the previous history entry's id. The live key restores the latest.
STEP: Add `PALETTES` and `cfg.palette` in `kit.ts` and `state.ts`.
STEP: Add the key handling and "as of" rendering in `register.tsx`, and declare the option in `.claude-plugin/plugin.json`.
SCOPE: mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/state.ts, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/.claude-plugin/plugin.json, mods/foreman-ui/tests/foreman-ui.test.tsx
TIER: M

=== T-1082
INTERPRETATION: Two parts: a ledger index so `fm ui` and `fm recall` stop re-reading the ledger, and a pane that wakes on a state change instead of a 2 s poll. Today `view()` reads `ledger_tail(5000)` plus a full-file `_closes_since` scan (`fmwatch.py:460,541`). `recall` reads `ledger_tail(p, 50000)` (`fmrecall.py:432`). `fm ui --follow` already waits on mtimes (`_follow`, `fmwatch.py:611`), but the mod still polls `fm ui --json` every 2 s (`register.tsx:553`). The wake pipe is the only part still to build.
APPROACH: (a) A sidecar `ledger.idx` of byte offsets by event, plus `task_done` days. (b) A per-process cache keyed on the ledger's `(mtime, size)`. (c) Both. Choose (a) plus the mod change. `fmcore.ledger_index(p)` stores `{size, offsets by task and event}` and extends incrementally from `size` to the new end (a chain break or a shrink rebuilds it). `ledger_tail` is unchanged in meaning, and `_closes_since` and `fmrecall` use the index. In the mod, switch the poll to a long-lived `fm ui --follow` process whose lines replace `tick`, falling back to the 2 s poll if it exits.
AC: the index gives the same events as a full scan, extends after an append, and rebuilds after a tidy roll :: python3 plugin/tests/run.py test_ledger_index
AC: the mod uses `--follow` lines and falls back to polling :: cd mods/foreman-ui && ~/.local/bin/claude plugin test .
STEP: Failing tests: build the index, append two events, and the extension returns exactly those two. Truncating the file forces a rebuild with equal results. `_closes_since` with the index equals a plain scan. Mod test: a stdout line from the follow process updates the view without a 2 s tick.
STEP: Add `ledger_index` to `fmcore.py` and use it in `fmwatch._closes_since` and `fmrecall.lessons`.
STEP: Replace the poll in `register.tsx` with the spawned follow process.
SCOPE: plugin/lib/fmcore.py, plugin/lib/fmwatch.py, plugin/lib/fmrecall.py, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_ledger_index.py
TIER: M

=== T-1086
INTERPRETATION: Builders run under Claude Code's sandbox where the host has one, and every outbound request a session makes is logged per task. A sandbox exists only for `fm run --sandbox`, opt-in (`fmserve.py:379`, `_sandbox`). Subagent builders (`plugin/agents/fm-builder.md`) get nothing. For the outbound ledger, `post_tool_validate` already sees WebFetch, WebSearch and `mcp__` results (`fmhooks.py:1913`) but logs only injection flags.
APPROACH: (a) Make `--sandbox` the default for `fm run` where available. (b) Add an `outbound` ledger event. (c) Both. Choose (c). In `fmserve.py`, `_sandbox_available()` (bwrap or sandbox-exec on PATH) makes `--sandbox` the default, with `--no-sandbox` to opt out, and `fm lane brief` prints "sandbox: on|off". In `fmhooks.py`, `post_tool_validate` logs `c.log_event(p, "outbound", task, {tool, target})`, where target is the URL host for WebFetch, the query for WebSearch, the server/tool for `mcp__`, and the host of curl/wget/git-push in Bash. A new `fm outbound [ID] [--json]` command lists them per task. I would put it in `fmledger.py`, next to `fm verify-ledger`.
AC: a WebFetch hook logs `outbound` with the host for the active task, and `fm outbound T` lists it :: python3 plugin/tests/run.py test_outbound
AC: `fm run` sandboxes by default when bwrap is present and not under `--no-sandbox` :: python3 plugin/tests/run.py test_outbound
STEP: Failing tests: `self.hook("PostToolUse", WebFetch payload)` produces an `outbound` ledger line with the host and task. Bash `curl https://x.test/a` logs host `x.test`. `fm outbound` output has the host and a count. `_claude_cmd` includes `--settings` when `_sandbox_available` is patched true, and does not with `--no-sandbox`.
STEP: Add `_outbound()` to `fmhooks.py` and call it from `post_tool_validate`. Redact via `log_event`.
STEP: Add `_sandbox_available` and `--no-sandbox` to `fmserve.py` and `fmcli.py`. Add `cmd_outbound` to `fmledger.py` with a lazy `outbound` entry in `fmcli.py`.
SCOPE: plugin/lib/fmhooks.py, plugin/lib/fmserve.py, plugin/lib/fmledger.py, plugin/lib/fmcli.py, plugin/lib/fmlanes.py, plugin/tests/test_outbound.py
TIER: M
