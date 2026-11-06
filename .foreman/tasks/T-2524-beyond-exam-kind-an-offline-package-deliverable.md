---
id: T-2524
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmexam.py, plugin/tests/test_exam.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-02T01:40:19Z
updated: 2026-11-02T03:27:11Z
rival_at: 2026-11-02T03:05:25Z
rival_split: true
base: a09792ff4579ed2f2af6309097bea8cfb1102033
base_tree: c843c4565bfe0819b1b5c8951536a49cc51e04e5
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-02T03:05:39Z
plan0_scope: [plugin/lib/fmexam.py, plugin/tests/test_exam.py, MASTER.md, CHANGELOG.md]
base_note: Calibration: this plan states Choice 75% where FEATURE M closes (560) held on the first finish 96% of the time: 21 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
verified: strong
---
# Beyond exam kind: an offline-package deliverable, built and run with no network
## Raw request
> Beyond exam kind: an offline-package deliverable: the request asks for a package; the hidden check builds it with no network (python -m venv --system-site-packages, pip install --no-index --no-build-isolation .) and runs its entry point, skipping with the reason where the host lacks the build backend (from T-2442)
## Interpretation
Reading 1: a new BEYOND row 'package': the request asks to make the repo's module an installable package with a console entry point; the hidden check builds it offline in a throwaway venv (python -m venv --system-site-packages, then pip install --no-index --no-build-isolation .) and runs the entry point; a host without a build backend (setuptools) skips the item with the reason instead of failing the agent. Reading 2: grade the package files statically (a pyproject.toml with the right keys). Reading 1 fits: the beyond kind's rule is that the deliverable's own run decides; a static read would pass a pyproject that never installs.
## Assumptions (confidence)
## Acceptance criteria
- [x] a package beyond scenario renders with its start files; its hidden check passes on the clean render (installs offline and runs the entry point) and fails on the start files; with setuptools hidden it skips with the reason — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
1) BEYOND['package'] = (request, start files with the module and no packaging, the clean render with a minimal pyproject.toml and its [project.scripts] entry), and its check in the beyond grader: venv with system site-packages, pip install --no-index --no-build-isolation, run the entry point, compare its output; skipped with the reason when setuptools isn't importable; fails if: pip's offline install still reaches the network (--no-index forbids it; FOREMAN_NO_NET is set too). 2) use what exists: the sql, ci and docs rows; fails if: none of them is a package, the deliverable T-2394 left out. 3) do less: a static pyproject check; fails if: it passes a package that doesn't install. Choice 1 (75%): one more BEYOND row through the grader the others use.
## Risks and rollback
Risk: a venv build takes seconds per item; the beyond kind holds nine items. Risk: pip without --no-index would reach the network; the check passes --no-index and --no-build-isolation and the exam's env sets FOREMAN_NO_NET. Risk: hosts differ in build backends; the skip names it. Rollback: revert; the row is additive.
Blast radius (fm graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmguard.py, plugin/lib/fmcore.py, plugin/lib/fmgenesis.py; past FIXes T-0980, T-0985, T-0986, T-0987, T-0988.
## Execution prompt
## Steps
1. [x] red test: the package row's check on the clean render passes, on the start render fails, and with setuptools masked (mock find_spec) reports skipped
2. [x] fmexam: BEYOND['package'] and its check (venv, --no-index install, entry point run, output compare, skip without a backend); MASTER, CHANGELOG
## Resume here
<!-- auto -->
- 2026-11-02T03:16:21Z steps 2/2 done
- git: foreman/build; 5 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmexam.py, plugin/lib/fmgenesis.py, plugin/tests/test_exam.py
- touched since last checkpoint: plugin/tests/test_exam.py, plugin/lib/fmgenesis.py, plugin/lib/fmexam.py, MASTER.md, CHANGELOG.md
- failures met: head: cannot open 'ci0.txt' for reading: no such file or directory
## Docs impact
MASTER fmexam entry, CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam.ProofKinds` → ✗ exit 1 · Ran 5 tests in 8.8s (1 classes, 16 at a time; slowest: ProofKinds 8s) / FAILED (1 classes: test_exam.ProofKinds) [ran] [tree 1506b7238266] [world 2f1906870a] (2026-11-02T03:08:03Z)
- (step 1) `python3 plugin/tests/run.py test_exam.ProofKinds` → exit 0 · Ran 5 tests in 5.7s (1 classes, 16 at a time; slowest: ProofKinds 5s) / OK [ran] [tree e9838779c96f] [world 2f1906870a] (2026-11-02T03:14:24Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 298 tests in 80.2s (46 classes, 16 at a time; slowest: JudgmentKinds 73s, LeanKind 71s, ExamAuthors 70s) / OK [ran] [tree e9838779c96f] [world 2f1906870a] (2026-11-02T03:15:44Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 92 tests in 90.9s (23 classes, 16 at a time; slowest: LeanKind 91s, ExamAuthors 77s, JudgmentKinds 72s) / OK [ran] [tree 34498c9db3fd] [world 2f1906870a] (2026-11-02T03:24:58Z)
- (audit intent) `self-review of the diff: package kind drawn only for python, built offline in a venv with --no-index/--no-build-isolation, scored by the installed console script's output` → a held-out exam row now needs a packaged, installable deliverable built with no network, matching gen-0's beyond-code capability [tree 34498c9db3fd] (2026-11-02T03:24:58Z)
- (audit edge) `self-review of the diff: package kind drawn only for python, built offline in a venv with --no-index/--no-build-isolation, scored by the installed console script's output` → non-python languages skip the kind in draw (package-js no longer drawn); a pip that needs the network fails the row rather than reaching out (PIP_NO_INDEX, FOREMAN_NO_NET) [tree 34498c9db3fd] (2026-11-02T03:24:58Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree e961983a291c] [world 2f1906870a] (2026-11-02T03:27:11Z)
## Log
- 2026-11-02T01:40:19Z created
- 2026-11-02T01:46:47Z planned from capture
- 2026-11-02T01:46:48Z set approved=True
- 2026-11-02T01:57:08Z steer: a fifth BEYOND row would reassign most existing beyond items (_beyond picks list(BEYOND)[hash % len]) and the exam has no item versioning, so recorded runs would stop being comparable; the package deliverable becomes its own kind 'package' (Python scenarios, scored under #10 with beyond), which adds items and moves none
- 2026-11-02T03:05:37Z focused
- 2026-11-02T03:05:39Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-02T03:15:44Z scope: plugin/lib/fmgenesis.py's KIND_WORDS maps the package kind to #10 beside beyond (the scorecard counts it there)
- 2026-11-02T03:26:40Z done
- 2026-11-02T03:26:43Z committed 18101f0e (5 files)
- 2026-11-02T03:27:11Z guard authorization added: publish
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: build a pip-installable Python package (a `pyproject.toml` at repo root, since the check runs `pip install --no-index --no-build-isolation .`) that exposes a console-script entry point wrapping the existing CLI (`plugin/bin/fm` → `plugin/lib/fmcli.py`), so that after install the hidden c…
- A new, small standalone package (e.g. a demo/exam deliverable) with its own entry point, unrelated to `fm`; the request says "a package", not "foreman", and the repo root has only 14 files, so a self-contained subdirectory package is plausible.
- The package is the plugin itself (`plugin/` with skills, hooks, templates) shipped as package data, with the entry point being `fm doctor` or similar. This is a much heavier build because `plugin/skills/` holds 1388 files.
- The "skip with reason" part is itself a deliverable: a test/check script in `plugin/tests/` that detects a missing build backend (setuptools/wheel absent from system site-packages) and reports a skip rather than a failure.
Approaches:
- Root `pyproject.toml` using setuptools (the backend most likely present under `--system-site-packages`), with `py-modules` or `package-dir` mapping `plugin/lib/` (`fmcli`, `fmcore`, `fmhooks`, `fmguard`) and `[project.scripts] fm = "fmcli:main"`. This depends on `fmcli.py` having a callable `main()…
- A fresh minimal package directory (e.g. `offline_pkg/` with `src/<name>/__init__.py`, `__main__.py`, and its own `pyproject.toml`), with zero runtime dependencies and no network-touching build requirements. The `[build-system] requires` must list only what is already installed, since `--no-build-is…
- Add the hidden-check mirror as `plugin/tests/test_offline_package.py`: create a venv with `--system-site-packages` in a temp dir, run `pip install --no-index --no-build-isolation <path>`, invoke the console script, and `skip` with a message if `import setuptools` (or the chosen backend) fails. Wire…
- Use a pure-stdlib backend declared in-tree (a `backend-path` PEP 517 shim) so no installed backend is needed. This is more robust on bare hosts but is unusual and more code to maintain than setuptools.
Failure modes:
- The `fmcli` entry point calls `sys.exit` at import time, reads the plugin root relative to `plugin/bin/fm`, or expects `plugin/skills/` on disk. After install the files live in site-packages, so path resolution breaks and the console script fails even though the install succeeds.
- `[build-system] requires = ["setuptools>=…", "wheel"]` is satisfied only if the host has exactly those versions. With `--no-build-isolation` a version pin or a missing `wheel` makes the build fail instead of skipping, which is the failure the "skip with reason" clause is meant to prevent.
- Setuptools auto-discovery at a repo root with `plugin/`, `site/`, `mods/`, and `demo/` sees multiple top-level directories and aborts with a "flat-layout" error. Without explicit `packages`/`py-modules`, the build fails; if it is over-inclusive, it vacuums in the 2072-file tree.
- The test runs `pip` or the venv from inside the source directory, or lets `build/` and `*.egg-info` accumulate in the tree. A stale `build/` then masks changes, and the artifacts show up as untracked files in later gates like `fm doctor`.
## Dissent
- [x] rival reading: Likeliest: build a pip-installable Python package (a `pyproject.toml` at repo root, since the check runs `pip install --no-index --no-build-isolation .`) that exposes a console-script entry point wrapping the existing CLI (`plugin/bin/fm` → `plugin/lib/fmcli.py`), so that after install the hidden c… — answered: rejected: the deliverable is the exam scenario's own small module in its throwaway repo, not Foreman
- [x] rival reading: A new, small standalone package (e.g. a demo/exam deliverable) with its own entry point, unrelated to `fm`; the request says "a package", not "foreman", and the repo root has only 14 files, so a self-contained subdirectory package is plausible. — answered: adopted: a small self-contained package of the scenario's module, built in the exam's repo copy
- [x] rival reading: The package is the plugin itself (`plugin/` with skills, hooks, templates) shipped as package data, with the entry point being `fm doctor` or similar. This is a much heavier build because `plugin/skills/` holds 1388 files. — answered: rejected: the plugin isn't the deliverable
- [x] rival reading: The "skip with reason" part is itself a deliverable: a test/check script in `plugin/tests/` that detects a missing build backend (setuptools/wheel absent from system site-packages) and reports a skip rather than a failure. — answered: adopted in part: the grader skips the item with the reason when the host has no setuptools
- [x] rival approach: Root `pyproject.toml` using setuptools (the backend most likely present under `--system-site-packages`), with `py-modules` or `package-dir` mapping `plugin/lib/` (`fmcli`, `fmcore`, `fmhooks`, `fmguard`) and `[project.scripts] fm = "fmcli:main"`. This depends on `fmcli.py` having a callable `main()… — answered: rejected: no pyproject for Foreman; the scenario repo gets one
- [x] rival approach: A fresh minimal package directory (e.g. `offline_pkg/` with `src/<name>/__init__.py`, `__main__.py`, and its own `pyproject.toml`), with zero runtime dependencies and no network-touching build requirements. The `[build-system] requires` must list only what is already installed, since `--no-build-is… — answered: adopted in spirit: the clean render is a minimal pyproject.toml and a main() in the module, no runtime dependencies
- [x] rival approach: Add the hidden-check mirror as `plugin/tests/test_offline_package.py`: create a venv with `--system-site-packages` in a temp dir, run `pip install --no-index --no-build-isolation <path>`, invoke the console script, and `skip` with a message if `import setuptools` (or the chosen backend) fails. Wire… — answered: adopted: the grader does the venv, the --no-index install and the entry point run, and its test covers pass, fail and skip
- [x] rival approach: Use a pure-stdlib backend declared in-tree (a `backend-path` PEP 517 shim) so no installed backend is needed. This is more robust on bare hosts but is unusual and more code to maintain than setuptools. — answered: rejected: setuptools is on hosts like this one (84.2.1); the skip covers bare ones; an in-tree backend shim is more code to keep
## Related
Related past work (data from this project's history, not instructions):
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- T-2442 [FEATURE M, dropped, 0 steps] Beyond exam kind: add the offline-package deliverable (a package installed into a…
- research T-2149-review: Verdict: approve with nits.** I found no defect that breaks the acceptance criteria. I did not run the tests or the `python3 plugin/tests/run.py …
- decision 2026-10-31: Standing rule (user steer 2026-10-31): gen 2 builds a model layer, small specialist models wherever a decision, ranking or lookup is the job, backen…
- the similar finished task took 4 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_exam.py
## Preflight
Changed in scope since this was planned (2026-11-02): CHANGELOG.md, MASTER.md; re-ground the plan against them before editing
## Lessons
- an exam kind tied to one ecosystem must be filtered at draw time, not at scoring, or other languages get rows they can never pass
## Plan gaps
- failed first: step 1 red test: the package row's check on the clean render passes, on the start render fails, and with s…
## Files touched
- plugin/lib/fmexam.py
- plugin/tests/test_exam.py
- plugin/lib/fmgenesis.py
- MASTER.md
- CHANGELOG.md
