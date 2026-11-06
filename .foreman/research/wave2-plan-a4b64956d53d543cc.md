=== T-1058
INTERPRETATION: `fm backtest` replays recent real sessions against one proposed self-change and says where it would have fired and how those sessions went. The change is a rule (`--rule PATTERN --on bash|path`), a known fix (`--fix ID`), a library card (`--card NAME`) or a hint. The guard-only replay already exists (`fmreplay.py:139` `cmd_replay`, `fmreplay.py:111` `score` for a candidate guard). That covers none of the other four kinds, and it doesn't report how sessions went.
APPROACH: (a) extend `fm replay` with flags; (b) new `fmbacktest.py` that reuses `fmreplay.corpus`; (c) a bench-style LLM replay. Choice (b). `fmreplay.corpus` is bash-only, so add `fmreplay.events(days)`, which yields tool calls (Bash command, Edit/Write path) with session id and whether the next result errored. Add `fmbacktest.py` with `fires(kind, spec, call)`. A rule goes through the regex logic of `c.rule_hits` (`fmcore.py:2185`) on a temp rules list. A fix goes through `fmfixes._relates`/`_norm` (`fmfixes.py:47-66`). A card goes through `fmlib.cards_for`'s signals (`fmlib.py:717`). Hints are listed under Risks: the T-1058 text names them but no hint matcher was read. The outcome per session is the share of fired calls followed by an error result, plus the session's `correction` ledger events. Register `backtest` in `fmcli.py` next to `replay` (~L4524) with `--days`.
AC: a rule that matches 2 of 3 fixture session commands reports "would have fired 2 times in 1 session(s)" with a count of fired calls followed by errors :: python3 plugin/tests/run.py test_backtest
AC: `fm backtest --card NAME --json` has the keys fires, sessions and errored :: python3 plugin/tests/run.py test_backtest
STEP: Failing tests: fixture jsonl logs under `self.home/.claude/projects` (the layout `fmreplay._logs` reads). Assert counts for `--rule`, `--fix` and `--card`, the empty-corpus message, and that `--rule` with a bad regex gives a UsageError.
STEP: Add `fmreplay.events()` and `fmbacktest.py`; read-only, nothing is written.
STEP: Add the `backtest` parser entry and register the command.
SCOPE: plugin/lib/fmbacktest.py, plugin/lib/fmreplay.py, plugin/lib/fmcli.py, plugin/tests/test_backtest.py
TIER: M

=== T-1059
INTERPRETATION: Each self-change (an `fm evolve` kept candidate, `fm rule add`, an adopted fix, a card edit) records a trial: the metric it should move, the direction and size, and the start date. After N days `fm digest` grades each trial by comparing the metric's per-day rate before and after. A trial that didn't move it is listed as "propose revert". Nothing like this exists. `fmevolve.py:181` logs only `kept/branch/target/why`. `fm digest` is `fmcost.cmd_digest` (`fmcost.py:340`).
APPROACH: (a) fields on the existing ledger events; (b) a `trials.jsonl` per project plus a small module; (c) `meta` entries. Choice (b), in new `fmtrials.py`. It has `register(p, kind, ref, metric, by, days)` and `grade(p, now)`. Metrics are ledger-derived rates per day, such as `corrections`, `guard_blocks`, `stalls` and `escapes` (all event names that exist: `fmfriction.py:182-195`, `fmhooks.py:615,623`), plus task "held" rate via `fmoutcomes.outcomes`. Add `--moves METRIC --by PCT` to `fm rule add` (`cmd_rule`) and `fm evolve`. `cmd_evolve` calls `register` when `res["kept"]`. Add a "Trials:" section to `cmd_digest` that calls `fmtrials.lines(p)`, and add `fm trial list|grade`.
AC: a trial registered 10 days ago with fixture ledger events (corrections 5/day before, 5/day after) grades "no movement: propose revert"; a halved rate grades "moved" :: python3 plugin/tests/run.py test_trials
AC: `fm rule add X --moves corrections --by 30` writes a trial and `fm digest` prints it :: python3 plugin/tests/run.py test_trials
STEP: Failing tests: use `c.log_event` with backdated ts; check grade verdicts, an ungraded trial before N days ("pending, N days left"), and a rule add without `--moves` records none.
STEP: Write `fmtrials.py` and wire it into `cmd_rule`, `cmd_evolve` and `cmd_digest`.
STEP: Add the `trial` parser entry.
SCOPE: plugin/lib/fmtrials.py, plugin/lib/fmcli.py, plugin/lib/fmevolve.py, plugin/lib/fmcost.py, plugin/tests/test_trials.py
TIER: M

=== T-1062
INTERPRETATION: When the user is away, or at `fm night`, the top queued S task that is planned enough gets drafted by a builder-style `claude -p` in a throwaway worktree. The draft is on a `draft/<id>` branch, ready to review. If the queue's top item or that task's spec changes, the draft is discarded. Nothing like this exists: grep found no speculative, draft or prefetch code. `fm lane` builders are launched by the main thread (`fmlanes.py:139`), and `fmnight.jobs` (`fmnight.py:48`) has no such job.
APPROACH: (a) a new night job only; (b) `fm draft` command plus a night job; (c) a hook on idle. Choice (b); hooks are unproven for idle. New `fmdraft.py` with `pick(p)` using `c.order_queue(...)`, tier S, `c.plan_gaps(b, autonomy)` empty and a verify command. `fingerprint` is a hash of the ordered queue ids plus the task file. `start` makes the worktree like `fmevolve.py:126`, runs `claude -p` with the brief text and a budget (`fmbudget.check`), and commits. State goes in `p.dir/draft.json`. `fm draft [--status|--drop]` first runs `sweep`, which removes the worktree and branch if the fingerprint no longer matches. Add `("draft", ["draft", "--if-idle"], est)` to `jobs()`. Never merge; the output names `git diff HEAD...draft/<id>`.
AC: with a fake `claude` on PATH, `fm draft` creates `draft/T-x`; changing the queue top and running `fm draft --status` removes it :: python3 plugin/tests/run.py test_draft
AC: `fm night --dry-run` lists a "draft T-x" job when an S task is ready :: python3 plugin/tests/run.py test_draft test_night
STEP: Failing tests: use the fake-claude pattern from `test_night.py:30`; assert the branch exists, `draft.json` has the fingerprint, a stale sweep removes both, and no S task gives "nothing to draft".
STEP: Implement `fmdraft.py` and the parser entry.
STEP: Add the night job.
SCOPE: plugin/lib/fmdraft.py, plugin/lib/fmnight.py, plugin/lib/fmcli.py, plugin/tests/test_draft.py
TIER: M

=== T-1063
INTERPRETATION: Steers and interrupts get a type: scope, style, safety or wrong approach. A type that recurs is compiled into an enforced check. A repeated "no" steer becomes a block or warn rule (`fm rule add`) with its type as `--why`. A recurring interrupt (`escape` events) becomes a plan-time note or a gate. Already present: vetoes (`fmcore.py:2112`), `proposals()` from repeated steers (`fmideas.py:234`), `fm taste adopt` (`fmideas.py:305`), and `STANDING_STEER` (`fmcore.py:2094`). T-1042 (planned in the state ledger, not built) adds `correction_clusters` with a ready `fm rule add` line. Not covered: typing, and compiling to a pattern rather than a veto.
APPROACH: (a) build only on T-1042's output; (b) classify in `fmideas.py` and compile in `fm taste compile`; (c) an LLM classifier. Choice (b): keyword classifier, no model. Add `classify(text)` in `fmideas.py` (safety: force/delete/secret/push; scope: only/also/outside/just; style: format/name/comment/lint; else wrong-approach). Add `type` to each proposal. `fm taste compile N` writes a rule via `c.add_rule` with the pattern from `_key_words`. A style steer is a path rule on `--on path`; a safety steer is a block on bash. Log `steer_compiled`. T-1042 should merge first; the builder re-uses its `correction_clusters`.
AC: three "no/never" steers about force push give a proposal typed "safety"; `fm taste compile 1` adds a rule that blocks `git push --force` :: python3 plugin/tests/run.py test_steer_compile
AC: after compile the proposal disappears from `fm taste` :: python3 plugin/tests/run.py test_steer_compile
STEP: Failing tests: log note events "steer: ..." with `c.log_event`; assert the type of each of four fixtures, the pattern and `action`, that a declined or covered proposal doesn't compile, and that the `rules.json` entry is valid via `c.rules(p)`.
STEP: Add `classify` and the pattern builder in `fmideas.py`; add the `compile` action to the `taste` parser and `cmd_taste`.
SCOPE: plugin/lib/fmideas.py, plugin/lib/fmcli.py, plugin/tests/test_steer_compile.py
TIER: M

=== T-1064
INTERPRETATION: Under standard autonomy, an `fm decide --ask` identical to one the user answered in the ask digest is answered at once from that precedent. The answer is labelled "proxy answer" and a decision row is written. It is gated: a proxy is allowed only if enough precedents agree and the proxy's own track record is good. Present today: `_decide_ask` (`fmcli.py:2689`) queues asks with a taste default; it never uses past user answers. `_answer` (`fmcli.py:2763`) records user answers in `decisions.md` with why "the user's answer (ask digest)". Guard-category asks are never pre-answered (`fmcli.py:2693`); that stays.
APPROACH: (a) match on `decisions.md` rows; (b) a `precedents` ledger event; (c) fuzzy match. Choice (a) plus event: in `_answer`, add `c.log_event(p, "ask_answered", data={"q": norm(q), "a": answer})`. Add `fmideas.precedent(p, q)`, which returns the answer when at least 2 normalized-identical past asks have the same answer and none disagree. Gate on the proxy's record: log `proxy_answer`, and when the user later changes it (`_answer` on a proxied n), log `proxy_overruled`. Refuse a proxy when overruled/total is above 20% once at least 3 proxies exist, reusing the calibration style of `fmoutcomes.calibration`. Wire it into `_decide_ask` before the standing-autonomy queueing. Text: "Proxy answer (from N earlier answers): …".
AC: after two user answers to the same ask, a third `fm decide --ask` returns `proxy: true` with that answer :: python3 plugin/tests/run.py test_proxy
AC: two proxied answers overruled stop proxying; guard-named asks never proxy :: python3 plugin/tests/run.py test_proxy
STEP: Failing tests: drive `fm decide --ask` and `--answer N` through `self.fm_json`; cover single-precedent (no proxy), disagreeing precedents (no proxy), overruled gate, guard-named ask.
STEP: Implement `precedent` and the gate in `fmideas.py`; update `_decide_ask` and `_answer` in `fmcli.py`.
SCOPE: plugin/lib/fmideas.py, plugin/lib/fmcli.py, plugin/tests/test_proxy.py
TIER: M

=== T-1068
INTERPRETATION: Parallel builders announce the files and symbols they will change before they edit. A second builder claiming an overlapping file or symbol gets a warning at claim time. Existing: edit-time leases in `fmbus.py` (`after_edit` L404, `conflict` L427, `cmd_lease` L475, `fm lease take|drop`), already hooked at `fmhooks.py:1119,1867`. Task `scope` globs exist (`fmcore.py:1581` already compares scopes). The gap is claims made up front, from the plan and not from landed edits, and a warning when a claim overlaps.
APPROACH: (a) make `fm lease take` warn; (b) auto-claim from `scope` at `fm lane brief`; (c) a separate claims file. Choice (a)+(b), reusing the lease store. `fm lease take` today refuses another session's lease on the same key only. Add `fmbus.claim_overlaps(p, rel, sym)`, which flags any live lease on the same file where a symbol is `*` or equal. `cmd_lease take` with several targets (`FILE[::SYM]...`) prints "overlaps session X (T-y)" and, with `--warn`, still takes it. In `builder_brief` (`fmlanes.py:139`) add a CONTRACT line telling the builder to run `fm lease take` for the files/symbols it plans, and have the brief itself pre-claim the concrete (non-glob) scope paths under task id. The `conflict` hook then needs no change.
AC: session A claims `a.py::f`; session B's `fm lease take a.py::f` fails naming A and its task; `a.py::g` succeeds :: python3 plugin/tests/run.py test_claims
AC: `fm lane brief T-x` pre-claims the task's non-glob scope paths and its CONTRACT mentions `fm lease take` :: python3 plugin/tests/run.py test_claims
STEP: Failing tests: use `self.fm` with two `FOREMAN_SESSION`-style ids (see `test_bus.py`); cover the file-wide `*` vs symbol overlap, expiry and drop.
STEP: Add `claim_overlaps`, the multi-target `take` and the `--warn` flag in `fmbus.py` and `fmcli.py`.
STEP: Pre-claim in `builder_brief` and extend `CONTRACT`.
SCOPE: plugin/lib/fmbus.py, plugin/lib/fmlanes.py, plugin/lib/fmcli.py, plugin/tests/test_claims.py
TIER: M

**Noticed:** none for the wider repo, but a risk for the plan: the working tree has unfinished edits to `fmcli.py`, `fmhooks.py` and `fmlanes.py`, so T-1058, T-1059, T-1063, T-1064 and T-1068 all touch `fmcli.py` and will collide at merge. Serialise them or put each parser entry in a distinct hunk.
