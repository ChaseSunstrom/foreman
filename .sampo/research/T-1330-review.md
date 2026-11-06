**Verdict:** changes needed. I read the diff and the working-tree code. I ran no tests, because I had no way to run commands.

## lens: intent
- MEDIUM — plugin/lib/fmcode.py:1360 — `_start_task` stops only on a plan problem starting "refused". The "can't run here" (unrunnable verify) and "already passes before any work" problems are dropped, although the criterion says it refuses a task with no runnable criterion — Fix: raise `CodeError(why)` for any `why`, or at least for the unrunnable one — high.
- LOW — plugin/lib/fmcode.py:1139 — the no-request message was reworded, though the criterion says it is "unchanged" — Fix: keep the old text and put the new hint elsewhere — medium.
- LOW — plugin/lib/fmcodetui.py:2070 — `here` compares roots. A linked worktree's `p.root` is the worktree, but its project's root is the main checkout, so `fm code` opens home instead of the project view. `find_project` returns `Project(m.slug, gr, …)`, so the slug still matches — Fix: compare `x["project"] == p.slug` — high.

## lens: adversary
- Q1, control characters: not exploitable in the TUI. Every project-sourced string (names, roots, titles, reasons, errors, run requests) goes through `Canvas.put`, which draws any non-printable character as a space (fmcodetui.py:334). That covers ESC and C1 controls, and the code has no raw writes of this text.
- Q2, shell reach: no. Project root only reaches `Popen(cwd=…)`, and the task id and slug are argv elements. `--task` also needs the id to equal a real brief id, which comes from the file name regex.
- LOW — plugin/lib/fmcode.py:1368 — in non-JSON mode `run.emit` prints the brief's title and steps raw, so a pasted or synced (`fm sync`) title with ESC sequences reaches the terminal — Fix: strip non-printables in the `--task` plan text — low (plausible).
- LOW — plugin/lib/fmcodetui.py:2059 — opening the app calls `fmcli.resolve(args)` with `create=True`. Running `fm code` in any unregistered git repo silently registers it as a project — Fix: `resolve(args, create=not home)` — medium.

## lens: edge
- MEDIUM — plugin/lib/fmcode.py:1348 and :673 — `_load_task` keeps only criteria that have a verify, so they are renumbered. `verify()` then records evidence with `--ac n` using the new number. If criterion 1 has no check, criterion 2's evidence lands on criterion 1 and criterion 2 gets none — Fix: carry each criterion's original index into the plan and use it, or refuse a brief with an unchecked criterion — high.
- MEDIUM — plugin/lib/fmcode.py:1376 — `--task` on a task with an existing fm code journal (a crashed, blocked or active one, all `r`-able in the project view) appends a second `start` to the same file. `_load` then resumes from `recs[0]`, or reports "nothing to resume" if an `end` record exists — Fix: refuse and say `--resume ID` when `code/ID.jsonl` exists — medium.
- MEDIUM — plugin/lib/fmcodetui.py:1575 — a GONE project (folder missing) can be opened, and `r` or `n` then calls `Popen(cwd=<missing>)`. `FileNotFoundError` is not caught anywhere in `_loop`, so the TUI crashes — Fix: refuse when `not os.path.isdir(root)`, and catch `OSError` in `start` — high.
- MEDIUM — plugin/lib/fmcodetui.py:1459 — `open_project` overwrites `self.root` and `self.history_dir` while browsing. During or after a run in A, pressing `p`, opening B and pressing Esc twice makes `r` (resume) spawn `--resume <A's id>` with cwd B, and `d` diffs B. Task ids repeat across projects — Fix: store the run's root at `start()` and use it for resume and diff; set `root` only when a run starts — high.
- LOW — plugin/lib/fmcodetui.py:1361 — Esc in the prompt goes to "main", so `n` then Esc from a project view drops the project view. At home with no run it leaves an empty run screen — Fix: return to the project view the prompt came from — high.

## lens: operator
- Lock (Q3): `_hold` takes `flock` on an fd that is close-on-exec and held on `run`, so the OS frees it on a crash or kill. This holds.
- LOW — plugin/lib/fmcodetui.py:2756 (`_fm_json`) — a synchronous `subprocess.run` with a 60 s timeout inside the key handler (`show_home`, `open_project`) freezes the screen and run events — Fix: run it on a thread, or add a "loading" row — low.

## lens: maintainer
- LOW — plugin/lib/fmcodetui.py:1749 (`fm_project_state`) — it re-derives the project with `find_project(root)` instead of using the slug. For a missing root it can land on an ancestor repo's project and list its runs — Fix: `fmcore.project_by_slug(slug).dir` — medium.
- LOW — plugin/tests/test_code.py — `--task` has no test for a guard-refused verify, an unrunnable verify or non-contiguous criteria. test_code_tui.py has no test for Esc from the prompt or for a GONE project's `r`/`n`.

## Acceptance criteria
- Terminal opens the app, piped exits 1: met (fmcode.py:1113), though the message text changed.
- Home lists projects, a bad one shows why: met.
- A project's view with past runs, Enter replays: met.
- `r` and `n` run in that project's folder with the runner `m` picks: met for existing roots; not met for a missing root.
- `--task` refuses a task with no check, done or dropped, another project's, or one being worked: partly met. The no-check, done/dropped, another project's and locked cases are refused. The unrunnable verify is not refused, and criteria renumber wrongly (see edge lens).

## Implicit decisions
- `q` quits the app from home and project views, and stops a live run. Other overlays treat `q` as close.
- Home sorts newest first by `updated`.
- `--task` ignores brief steps already marked done.
- Lock file `code/ID.lock` is never deleted.
- `fm focus` is called unconditionally.

## Not checked
Tests, the site and demo assets under `--check/`, and `fm sync`'s trust model.

Noticed: with `fm sync on`, `r` on a mirrored task runs that task's verify command after a single keypress. The guard allows it, so consider a confirmation.
Noticed: `--task t-0003` (lowercase) reports "no task", because `find_brief` uppercases the id but `_load_task` compares it as typed.
