# T-3571 Sampo per-call CPU: Python fixes first, then a Rust fast path

Measured 2026-11-06 on this box (16 cores, load 5-18), niced, against a copy of the state
(`FOREMAN_STATE=scratchpad/rust/state`, so the real state was never written). Scripts live next to this
file: `bench.py` (whole-process CPU, median of 7), `prof_driver.py` (in-process split: import / run /
children / files / rchar / json), `profall.py` (cProfile), `warm.py` (resident process), `procsample.py`
(/proc spawn census, live vs test), `testprof.py` + `runtests.py` (test split), `gen_toy.py` + `incr.py` +
`rxprobe/` (Rust build and regex probes).

## 1. Where the CPU goes today

Rates: events.jsonl for Nov 6 (UTC day; per-hour average, peak hour 4.7x), plus a 4-minute /proc census
for what events.jsonl doesn't log (statusline, `fm ui`). CPU: whole process, cold, median of 7.

| path | calls/h | CPU/call | CPU-s/h | interp+import | state reads / logic | children |
|---|---|---|---|---|---|---|
| `fm ui --json` (one UI pane open) | 1,665 | 486 ms | **809** | 20+20 ms | 413 ms, rchar 130 MB, 692 files | 20 git, 45 ms |
| PreToolUse Bash (taint path*) | 462 | 194 ms | **90** | ~25+14 | 152 ms, of it `state_dict` ~100 | 0 |
| PostToolUse Bash | 462 | 139 ms | **64** | ~25+15 | 100 ms: `active_brief_fast` x4 | 0 |
| statusline | 480 | 36 ms | 17 | ~30 | ~5 | 0 |
| PostToolUse other tools | 316 | 44 ms | 14 | ~25+15 | 10 | 0 |
| UserPromptSubmit | 47 | 274 ms | 13 | ~25+11 | 215 ms, rchar 63 MB | 7 git, 22 ms |
| PreToolUse Edit/Write | 101 | ~70 ms | 7 | ~25+14 | ~44 (prod median); no-task path 120 | 0 |
| PostToolUseValidate | 103 | 57 ms | 6 | ~25+14 | 22 | 0 |
| Stop | 28 | 163 ms | 5 | ~25+14 | 127 ms: `state_dict`, all 2,369 briefs | 0 |
| PreToolUse Read | 106 | 39 ms | 4 | ~25+14 | 4 | 0 |
| SessionStart | 6 | 340 ms | 2 | ~25+11 | 252 ms, rchar 116 MB | 9 git, 40 ms |
| `sampo next` (agents, rate unlogged) | ? | 309 ms | ? | ~25+23 | 234 ms, rchar 61 MB | 7 git, 23 ms |
| **live total** | | | **~1,030** | | | |

*11,079 of 11,082 production Bash calls on Nov 6 came from a session that carries a `taint.json`
(subagents share the parent's session id), so the taint path *is* the production Bash path; without it
the same call costs 91 ms.

The interpreter is not the problem: `python3 -c pass` is 10.7 ms CPU (`-S` 7.3), Sampo's imports 10-23 ms
(`sampo.core` self 7.4 ms, `fmguard` 2.5 ms). The guard itself (`fmguard.check_bash`) is ~19 ms with its
regex compiles. **70-85% of every expensive call is re-reading state**: `load_briefs` (listdir + 2,369
stats + 1.29 MB `briefs-index.json` + parse of every open brief), `active_brief_fast` (~88 brief reads,
called up to 4x per hook with no memo), and full scans of `ledger.jsonl` (14.7 MB) and `events.jsonl` (24 MB).

**Tests outweigh live work.** In the census window test runs spawned 5,523 Sampo processes vs 627 live
(8.8x): test PreToolUse hooks alone ran at 17,130/h x ~90 ms = ~1,540 CPU-s/h, git at 64k/h. Last full
suite (`/tmp/fmtest-times-...65499c205a.json`): 10,101 job-seconds over 5,458 jobs. Per module:

| module (sample) | wall | waiting on Sampo children | direct git | in-process | git calls, all levels |
|---|---|---|---|---|---|
| test_hooks.PreToolUse (28) | 64 s | 134 hook spawns 31 s (12.1 s CPU, 90 ms each) + 148 fm forks 27 s | 3.5 s | 1.7 s | 612 (22/test) |
| test_lane_train.Train (15) | 62 s | 97 fm forks 58 s (600 ms each) | 3.5 s | 0.1 s | 1,864 (124/test) |
| test_diff_gates (9 short) | 20 s | 68 fm forks 18 s | 0.6 s | 1.2 s | 496 (55/test) |
| test_cli.CaptureAndIntake (26) | 20 s | 131 fm forks ~20 s | 1.9 s | ~0 | 167 (6/test) |
| test_guard_diff (3) | 45 s | 671 bwrap sandboxes 33 s | 4.7 s | 6.8 s | 344 |

So 88-97% of test wall is the same per-call Sampo cost as above, multiplied. A faster hot path speeds
the suite as much as the live hooks.

## 2. Python-side wins, ranked (do these first)

| # | change | where | saves CPU-s/h (avg; peak x4.7) | owner |
|---|---|---|---|---|
| 1 | `fm ui` cadence: watch list includes the project dir (any atomic write changes its mtime) and `ledger.jsonl` (appended per tool call), so the 2 s tick refreshes almost every tick (1,665/h measured). Watch one view-stamp file writers touch only on view-relevant changes; minimum 10 s between refreshes while busy | `mods/foreman-ui/hooks/register.tsx` tick(), `watch.py` `watch` list | ~630 | **none: new task** |
| 2 | `fm ui` per call: 20 git subprocesses (3x `rev-parse HEAD`, 4x `rev-list --count`, `worktree list`, per worktree); `events.jsonl` + `ledger.jsonl` each read twice (130 MB rchar); `_budget` scans events; `_skills`, `_worktrees` recomputed. Cache git answers keyed on `.git/HEAD` + refs mtimes; seek ledgers from an offset; memo sections by input mtimes. Target 486 -> ~100 ms | `watch.py` `view`, `_guarded`, `_budget`, `_worktrees`, `_skills`; `budget.ledger` | ~140 more (after #1) | **new task**; T-3573 covers the brief/ledger part |
| 3 | taint check builds the whole `state_dict` (~100 ms) to read one autonomy value, before it knows any line matched: evaluate `deny` only on a hit, read autonomy via `effective_autonomy`/meta | `hooks.py:3415` `_taint_check` | 46 (peak ~215) | T-3577 (name it: one-line change) |
| 4 | `active_brief_fast` has no per-process memo and is called from 18 sites (4x per PostToolUse Bash, ~35 ms each): memo per (tasks-dir mtime, lane); then serve it from the index | `core.py:4708`, callers in `hooks.py` | ~40 | T-3577 now, T-3573 for the index |
| 5 | hot-path state from an index instead of `load_briefs` / `state_dict` / ledger scans: `_guard_ctx`, Edit no-task `_first_brief`, Stop, UserPromptSubmit, SessionStart, `next_for`, `miss.open_misses` -> `ledger_events` | `core.load_briefs`, `state_dict`, `next_for`, `ledger_events`, `_seek_since` | ~35 hooks + every `sampo next`/CLI call (209-309 -> ~50 ms) | T-3573 |
| 6 | tests' `self.hook()` spawns a fresh interpreter while `self.fm()` goes through the fork server: route hooks through `forkcli` too (keep a few true-subprocess tests for the entry script) | `tests/helpers.py:378` | 25-35 ms x every test hook call (~1/3 of hook CPU in test_hooks) | T-3572 |
| 7 | one test is 88 s of its module's 106 s: `test_diff_gates.DiffGates.test_run_py_repeats_p` | tests | 88 s of every full suite | T-3572 / T-3576 |
| 8 | lane_train tests make 124 git calls each; fixtures could clone a template repo instead of `git init` + config + commit per test (5 git calls in `helpers.git_repo` alone) | `tests/helpers.py:288` | test wall | T-3572 |
| 9 | imports: `sampo.core` self 7.4 ms; split the cold parts out of the hook's import path | `core.py` | ~10 | T-3577 |

Flagged, not covered by any running task: **#1 and #2 (`fm ui`, ~770 CPU-s/h, more than all live hooks
together)**. Smaller: #7, #8 if T-3572 doesn't own fixtures. Statusline (17 CPU-s/h) is fine in Python.

After #1-#5 the live total drops from ~1,030 to ~150 CPU-s/h; what remains per hook is the ~40 ms of
interpreter + imports + regex compile that no Python change removes. That remainder is the Rust case.

## 3. Daemon vs Rust, measured

`warm.py` runs each call in a warm process (imports done, regexes compiled), in-process and as a fork of
the warm process (forkcli's model):

| call | cold today | warm, in-process | warm, fork per call |
|---|---|---|---|
| PreToolUse Bash (taint) | 194 ms | 105 | 119 |
| PreToolUse Bash (clean) | 91 | 31 | 37 |
| PostToolUse Bash | 139 | 84 | 90 |
| `sampo next` | 309 | 215 | 248 |
| `fm ui --json` | 486 | 474 | 541 |

A resident process saves only the 25-60 ms start, import and regex compile; the state reads stay. That's
why the index (T-3573) comes before either. After the index, both options save about the same per hook
(~35-40 ms: daemon needs a native client anyway plus ~6 ms fork; Rust ~1-3 ms total). The daemon covers
every event and verb with zero porting and zero equivalence risk, but has to re-exec when any of 143 lib
files changes (lanes edit them all day), runs one per checkout, and stays resident at ~80 MB. Rust gives the
lowest floor and no lifecycle, but only for what it ports. Choice stands (Rust fast path); the hook entry
binary is built so a forkserver can sit behind its "defer" later without changing hooks.json.

**Rust regex trap (measured):** compiling the guard's 346 patterns takes 70-86 ms with `regex`, 54-89 with
unicode off, 28-42 with `regex-lite`, against 10.3 ms in Python's `sre`. A toy binary that runs every rule
costs 80 ms CPU per exec, no faster than Python. 48 patterns need lookaround or backrefs (`fancy-regex`).
So the port must not be "every rule as a regex compiled at start".

## 4. Rust fast path: what, ranked

Rule: **Rust only ever says "allow, silently" or "defer"**. It never blocks, never writes briefs, meta or
the ledger (it only appends events.jsonl lines in Python's format), never emits notes. Blocks are rare (390 `guard_block` in 4 days), so nothing is lost; equivalence
reduces to one property: wherever Rust allows silently, Python exits 0 with empty stdout too.

| order | slice | handles | expected saving after the Python fixes |
|---|---|---|---|
| 1 | entry binary + index reader + PreToolUse Read/Agent/SendMessage/other matched tools | ~140 calls/h | ~5 CPU-s/h; proves the pipeline end to end |
| 2 | PreToolUse Bash fast-allow: a hand-written tokenizer (no regex) accepting a conservative grammar: simple commands and pipelines of known read-only programs (`grep sed -n cat ls head tail wc find rg git status/log/diff/show`), no expansion, redirect, `fm`/`sampo`, or path in state/core; session has no matching taint line; cwd inside a known project. 31% of recorded Bash commands fit a crude version | ~150-230 calls/h | ~8 CPU-s/h, ~40 at peak, plus the share it covers of test hook spawns (~1,540 CPU-s/h in all while suites run) |
| 3 | PostToolUse for tools with nothing else to record (Read/Grep/Glob): appends the same `tool` line to events.jsonl | ~300 calls/h | ~12 CPU-s/h |
| 4 | statusline | 480/h | ~16 CPU-s/h |

Not ported: CLI verbs, Stop/SessionStart/UserPromptSubmit/PreCompact (rare, rich, high churn), every
state writer, `fm ui` (fix it in Python, #1-#2), model calls, the full guard's block/ask logic.

## 5. Interface

- `plugin/hooks/hooks.json` (protected core) points at `hooks/fast` instead of `hooks/hook`, args unchanged.
- `hooks/fast` is `#!/bin/sh`: `B="$CLAUDE_PLUGIN_ROOT/native/$(uname -sm | tr ' ' -)/sampo-fast"`;
  `[ -x "$B" ] && exec "$B" "$@"`; `exec "$CLAUDE_PLUGIN_ROOT/hooks/hook" "$@"`. Users without the binary
  run exactly today's path (the shim measured 1.3 ms CPU; /bin/sh is bash here).
- `sampo-fast <Event>` reads stdin once. To defer it puts the payload on a pipe (memfd when over 64 KB) as
  fd 0 and `execv`s `hooks/hook <Event>`: one process, same argv, env and stdin, no second interpreter.
- It defers on: an event it doesn't handle; any parse error; a panic (`catch_unwind`; `panic = "abort"` is
  forbidden here); `SAMPO_FAST=0`; a stale binary; an index whose stamp doesn't match; anything outside its
  grammar. On allow it appends the same `hook_ms` line to events.jsonl with `"fast": true` and exits 0.
- **Staleness:** the build embeds the size+mtime+sha256 of `fmguard.py`, `sampo/hooks.py` and the index
  format version; at start the binary compares size+mtime (two stats) and defers on any mismatch. A lane
  that edits the guard without rebuilding gets Python, never stale Rust rules.
- `sampo-fast --decide <Event>` prints its verdict (`allow` / `defer:<reason>`) without side effects;
  Python gains `hooks.decide_only(event, raw)` returning (exit code, stdout) with no writes, for diffing.

## 6. Keeping the guard exactly equivalent

`plugin/tests/test_fast_equiv.py` plus a local `sampo fast diff` verb run every input through both:
1. `tests/fixtures/guard_cases.jsonl` (40) and `guard_allow.jsonl` (102);
2. test_guard_diff's FORMS x PAYLOADS x MUTATIONS, plus its fuzzer with a fixed seed and 10k cases;
3. every literal command in the 15 `test_guard*.py` tables (collected by AST, as `extract_patterns.py` does);
4. locally only: every recorded PreToolUse input in `~/.claude/projects/**/*.jsonl` (2,642 transcripts,
   5.4 GB: 168,945 unique Bash commands, ~47k Edit/Write), deduplicated and cached by hash. Private, so it
   never goes to CI; the run reports coverage (share Rust decided) and every difference.

A difference is any input where Rust says `allow` and Python's `decide_only` is not (0, ""). Any
difference fails the gate. Rust saying `defer` is never a difference. The selfgate's guard-replay job adds
the Rust verdict next to the Python one.

## 7. State index (T-3573), read by both

The existing `briefs-index.json` (T-2022) still costs listdir + 2,369 stats + 1.29 MB parse per load. New:
`<project>/index/hot.json`, ~50 KB, rewritten atomically (tmp + rename) under the project lock by the
writers that already exist (`write_brief`, `log_event`, `set_meta`), never by Rust:

```json
{"v": 1, "stamp": {"tasks_mtime_ns": 0, "ledger_size": 0, "meta_mtime_ns": 0},
 "autonomy": "full", "open": {"T-3577": {"status": "captured", "title": "...", "tier": "M", "lane": null,
 "allow": [], "steps": [0, 3], "updated": "..."}}, "active": {"<lane or main>": "T-3572"},
 "sessions": {"<sid>": {"task": "T-3572", "taint": true}},
 "ledger": {"day_offsets": {"2026-11-06": 14000000}, "counts": {}}, "events": {"day_offsets": {}}}
```

Readers check the stamp with three `stat`s; on a mismatch Python rebuilds it (one `load_briefs`) and Rust
defers. JSON over SQLite: both languages parse 50 KB in well under 1 ms, writes stay atomic renames like
every other state file, and 100 concurrent writers don't contend on one database lock. Closed briefs stay
in `briefs-index.json` for the cold paths. Ledger and events readers seek from `day_offsets`.

## 8. Cargo workspace and build loop

```
native/Cargo.toml            # workspace; Cargo.lock committed; [profile.release] lto="thin", panic="unwind"
native/crates/index/         # hot.json reader + stamp check (serde, serde_json)
native/crates/ward-fast/     # the fast-allow tokenizer and grammar; no regex in v1
native/crates/sampo-fast/    # the binary: events, defer/exec, --decide
plugin/native/<os>-<arch>/sampo-fast   # binaries (gitignored locally; release artifacts)
plugin/native/SHA256SUMS     # committed in each release commit
```

Toy workspace of the planned size (8.6k lines, the guard's real 346 patterns, serde, regex, fancy-regex),
measured with `incr.py`:

| build | wall | CPU |
|---|---|---|
| clean debug / clean release (thin LTO) | 10.3 s / 13.3 s | 15.8 s / 48 s |
| no-op (`cargo build`, nothing changed) | 0.04 s | 0.02 s |
| one guard file changed: debug / `test --no-run` | 0.50 s / 0.56 s | 0.42 / 0.61 s |
| one guard file changed: `--profile lane` (opt 2, no LTO, incremental, 256 CGUs) | 1.6 s | 1.1 s |
| one guard file changed: release with thin LTO | 10 s | 26 s |
| only the binary crate changed: debug | 0.29 s | 0.19 s |

Lanes and tests share one `CARGO_TARGET_DIR=$XDG_CACHE_HOME/sampo/cargo-target` (cargo locks it; with
0.5 s rebuilds the queue stays short) and build `--profile lane`; release LTO only in CI. sccache is not
installed and doesn't cache incremental crates; it isn't worth adding. Tests find the binary through
`SAMPO_FAST_BIN`; the test engine (T-3572) runs `cargo build --profile lane` once per run (a 40 ms no-op
when nothing changed), never per test.

## 9. Release and distribution

- CI on tag: matrix `x86_64`/`aarch64` x `linux-musl` (static) / `apple-darwin`; `cargo build --release
  --locked`; uploads binaries + `SHA256SUMS` to the GitHub release. The release commit carries
  `plugin/native/SHA256SUMS`, so trust anchors on the checkout, not on the download host.
- `install.sh` / `sampo doctor --repair` download the matching binary, check it against the committed sums,
  install it 0755. When cargo exists and no prebuilt matches: `cargo build --release --locked` (~45 s CPU).
  Neither: Python only, no behaviour change.
- The guard treats `native/`, `plugin/native/` and `hooks/fast` as `core`, like `fmguard.py`.

## 10. Risks

- Fail-open bypass in the tokenizer: bounded by "allow only inside a conservative grammar, differential
  gate on 170k real commands, defer on doubt". A Python guard change can only widen what defers.
- Stale binary after a guard edit: the embedded size+mtime check defers (section 5).
- Panic or crash: exit code 101 would read as a hook failure; `catch_unwind` around everything plus a test
  that fuzzes the payload parser.
- Regex compile cost: no regex in v1; if needed later, `regex-lite` compiled lazily, or DFAs
  precompiled at build time with `regex-automata` for the non-fancy patterns.
- Two languages to maintain: kept to ~3 crates under 5k lines, no state writes, and every slice must show
  its CPU-s/h in `sampo cost` or come out again.
