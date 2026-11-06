=== T-1074
INTERPRETATION: A file that keeps being fixed after edits (git fix/revert commits touching it) is flagged at `fm task focus` (the plan record) and in `fm audit prep` pre-audit findings for any task whose scope or diff touches it (wild C18, "hotspots x2"). Already covered: the task-outcome atlas flags files where finished tasks needed a later fix, shown only at focus (`fmoutcomes.py:203` `caution`, called `fmcli.py:2206`); the map's "hot" is plain churn (`fmmap.py:71`) and the tour's "hot file" risk reason (`fmmap.py:368`). Missing: a git-history fix-after-edit count, and any mention in audit prep.
APPROACH: (a) extend `fmoutcomes.caution` only, which gets no signal from untracked history; (b) new module, which is overkill; (c) add `fixy` to `fmmap.build` (files in ≥3 commits with fix/revert/bug subjects in 180 days, VERSION 8→9), print it from `caution` and from `pre_audit`. Choose (c): the map is cached and both callers already load it.
AC: `fm map --json` lists `fixy`, and `fm task focus` prints "Hotspot:" for a scoped file in it :: python3 plugin/tests/run.py test_map
AC: `fm audit prep` pre-audit lists "hotspot" for a diff touching it :: python3 plugin/tests/run.py test_audit
STEP: Failing tests: in a temp repo make 3 "fix:" commits touching a.py and 1 touching b.py; assert `m["fixy"]` has a.py only; focus on a task scoped to a.py prints "Hotspot: a.py"; pre_audit on a diff with a.py returns a line containing "hotspot"; b.py does not.
STEP: `fmmap._fixy(root, files)` using one `git log --name-only --format=%x00%s`, regex `\b(fix|revert|bug|hotfix)`; store in build(); bump VERSION.
STEP: Add the hotspot line to `fmoutcomes.caution` (take the map via `fmmap.load`) and to `fmmap.pre_audit` next to the `pairs` block (`fmmap.py:555`).
SCOPE: plugin/lib/fmmap.py, plugin/lib/fmoutcomes.py, plugin/tests/test_map.py, plugin/tests/test_audit.py
TIER: M

=== T-1066
INTERPRETATION: `fm bench guard --mutate` weakens one guard rule at a time and shows which cases notice. A "case" is a command from the replay corpus plus the fixed deny/allow commands the guard tests use. A rule no case flips is listed as untested (wild C10). Existing parts: `fm replay --candidate` loads a guard module from a file and scores it (`fmreplay.py:90`, `:111`), `verdicts` takes another guard module (`fmreplay.py:67`), and `fm bench` has no `guard` subcommand (`fmcli.py:4704`).
APPROACH: (a) mutate source text with regex edits per rule; (b) AST-mutate `fmguard.py`'s `check` branches (`if` tests become False, one at a time); (c) wrap the module's `CATEGORIES` and drop one category at a time. Choose (c): the guard returns a `category` per block (`fmreplay.py:80`), so a rule is "a category." Dropping one means its verdicts become "allow", which needs no source rewriting. Mutate by patching `check` to return None when `b.category == X`, and run the corpus: a mutant "survives" when no case's verdict changes.
AC: `fm bench guard --mutate --cmds FILE` names a rule with no case as "untested" and one with a case as "caught" :: python3 plugin/tests/run.py test_replay
STEP: Failing tests: with a corpus of `rm -rf /` (and nothing else), the mutate run reports that category caught and every other category in `fmguard.CATEGORIES` untested; exit 1 when any is untested; `--json` has `caught` and `untested` lists.
STEP: `fmreplay.mutate(cmds)` builds `verdicts` once, then per category re-derives from that same table (no re-run, a mutant only changes entries equal to X). Cheap, and needs no module patching.
STEP: Add the `guard` subparser (`--mutate`, `--days`, `--cmds FILE`) near `fmcli.py:4712`, dispatched from `cmd_bench` before `refuse_if_paused`.
SCOPE: plugin/lib/fmreplay.py, plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/tests/test_replay.py
TIER: M

=== T-1067
INTERPRETATION: At close, each hunk of the task's change is reverted in a scratch worktree and the linked tests are run; hunks no test notices are reported as untested (wild C11). Already built: `fm task prove ID --hunks --run CMD` does exactly this (`fmcli.py:1173-1236`, `task_prove_hunks`, tests in `test_hunks.py`). What's missing is the link at close: `--run` is manual, and nothing picks the linked tests or triggers it from `fm task finish`.
APPROACH: (a) new `--ablate` flag on `fm task finish` that builds the command from `affected(p)` (`fmcli.py:3485`) and calls `task_prove_hunks`; (b) a close warning telling the user to run prove --hunks; (c) always run it. Choose (a): it reuses both pieces, is opt-in (slow), and `affected` gives the linked tests (`fmmap.tests_for`).
AC: `fm task finish ID --ablate` reports "N/M hunks proven" and names an untested hunk :: python3 plugin/tests/run.py test_hunks
STEP: Failing tests: reuse `test_hunks._Case`'s repo and add a test that finish with `--ablate` and no `--run` still names the untested hunk, using the linked test command. Another test: no linked tests gives a one-line "no linked tests" and does not fail the close.
STEP: In `task_finish` (`fmcli.py:805`), when `args.ablate`, set `args.run` from `affected(p)` (stop with UsageError if `cmd` is None), `args.hunks=True`, `max=20`, and call `task_prove_hunks`; print its summary into the finish output. Add the flag to the `finish` parser.
SCOPE: plugin/lib/fmcli.py, plugin/tests/test_hunks.py
TIER: M

=== T-1043
INTERPRETATION: `fm export cursor` writes `.cursor/rules/foreman.mdc` and `fm export gemini` writes `GEMINI.md`, with the same learned brain as AGENTS.md. `fm export agents` also gains a "Known fixes" section (trusted fixes only, via `fmfixes.known`). Existing: `agents_md` and `cmd_export` (`fmcost.py:543`, `:592`) with the write-inside-project, mark and --force protections; the parser accepts only `agents` (`fmcli.py:4488`). `fmagents.py:195` is Gemini's hook wiring, not an export.
APPROACH: (a) three copies of cmd_export; (b) one writer parameterised by target (path, header wrapper); (c) templates. Choose (b): the `what` choice picks the default path and the wrapper (Cursor needs `---\nalwaysApply: true\n---` front matter before the mark). The guard of `AGENTS_MARK` (`fmcost.py:605`) must be tolerant of the front matter, so scan the first 1000 chars, which it already does.
AC: `fm export cursor|gemini` write their files with the mark, corrections and a "Known fixes" section :: python3 plugin/tests/run.py test_fixes test_cli
STEP: Failing tests: after `fm fix add "boom" --do "retry"`, `fm export agents` contains "Known fixes" and "boom"; `export cursor` creates `.cursor/rules/foreman.mdc` starting with "---"; `export gemini` creates GEMINI.md; a non-fm-written file is refused without `--force`; a repo-sourced untrusted fix is left out. (`cmd_export` refuses `.claude`/`.git` parents, and `.cursor` is fine.)
STEP: In `agents_md(p, target="agents")` add the fixes section from `fmfixes.known(p)` (trusted only, redacted, ≤15) and the front matter for cursor; extend `choices` and `cmd_export`'s default path.
SCOPE: plugin/lib/fmcost.py, plugin/lib/fmcli.py, plugin/tests/test_fixes.py
TIER: M

=== T-1045
INTERPRETATION: A "What Foreman learned" block: fixes new, worked and missed (from `fmfixes` stats), user corrections that became rules, and interventions (corrections and steers) per closed task. It's in `fm digest` and in the pane's idle line (C2, C12, C9). Existing: `cmd_digest` (`fmcost.py:340`) has lessons, outcomes and failures, and nothing on fixes; stats are `fmfixes._load(_stats_path())["fixes"][id]={worked,misses,offered,last}` (`fmfixes.py:217`); corrections are ledger `correction` events (`fmfriction.py:184`), rules are `c.rules(p)` (`fmcore.py:2096`); the pane idle branch is `register.tsx:939/983/1676`.
APPROACH: (a) compute in the pane (TSX); (b) one Python function `learned(p, since)` that returns a dict and a line, used by digest and exposed in `--json` for the pane; (c) a new `fm learned` command. Choose (b): digest is the one report, and the pane only renders a string.
AC: `fm digest` prints "Learned:" with fixes new/worked/missed, rules and interventions per task :: python3 plugin/tests/run.py test_learning test_fixes
AC: the pane shows it when idle :: cd mods/foreman-ui && npm test
STEP: Failing tests: seed fixes.md plus stats (worked 2, misses 1) with `correction` ledger events on a done task, then `fm digest --json` has `learned` with `fixes_new`, `worked`, `missed`, `interventions_per_task`; the text contains "per closed task".
STEP: `fmfixes.learned(p, since)` (counts from stats `last` and records) plus an interventions helper in fmcost; add to `cmd_digest` output and the JSON.
STEP: Render `v.learned` as the dim idle line in `register.tsx` (the field is added to the pane's view type). The pane's data source was not traced, so the builder must find where `FmView` is filled.
SCOPE: plugin/lib/fmcost.py, plugin/lib/fmfixes.py, plugin/tests/test_learning.py, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/types/index.d.ts, mods/foreman-ui/tests/foreman-ui.test.tsx
TIER: M

=== T-1047
INTERPRETATION: Foreman mines git history, meaning revert commits and "fix:" commits, into lessons recall can find, and into known fixes where the commit body carries an error and its remedy. It runs in `fm adopt` and on demand with `fm adopt --history` (C2, C13). Existing: `fmoutcomes.reverts` (`fmoutcomes.py:16`) lists Revert commits; recall indexes `research/*.md` (`fmrecall.py:90`); `fmfixes.add` stores fixes (`fmfixes.py:139`); `adopt()` (`fmeco.py:~60-148`) mines no history.
APPROACH: (a) write lessons into briefs (invasive); (b) write one `research/git-history-lessons.md` and add fixes with `fmfixes.add`; (c) a separate command. Choose (b) with the flag on the existing `adopt` command: recall already reads research notes, and re-running is idempotent (the note is rewritten, `add` dedups by id).
AC: after `fm adopt` in a repo with a revert and a "fix:" commit, `fm recall` finds the lesson :: python3 plugin/tests/run.py test_ecosystem test_fixes
STEP: Failing tests: a temp repo with `Revert "x"` and `fix: crash on empty input` (body "error: IndexError → guard len"); `fm adopt` writes `research/git-history-lessons.md` listing both; `fm fix list` shows the body-pair as a fix; second run adds nothing; a repo with no such commits writes no note.
STEP: `fmeco.seed_history(p)`: `git log -n 300 --format=%H%x00%s%x00%b`, subjects matching `^(fix|revert)`, each with its files; the body regexp `error: (.+?) → (.+)` feeds `fmfixes.add`. Call from `adopt()` and from `cmd_adopt` when `--history` is set, redacting with `c.redact`/`c.defang`.
SCOPE: plugin/lib/fmeco.py, plugin/lib/fmcli.py, plugin/tests/test_ecosystem.py
TIER: M
