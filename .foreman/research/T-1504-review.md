**Verdict:** changes needed. `run_examples.py` can report a failing example as passing. The scrollytelling snippet doesn't satisfy its own deep-link check.

## lens: correctness / safety
- HIGH — `context/docs.md:56` — `err = r.stderr.strip() if r.returncode else ""` and `if err:` treat a nonzero exit with empty stderr as a pass. A block ending in `sys.exit(1)`, `raise SystemExit(3)`, `os._exit(1)` or a signal kill prints nothing, so the build stays green. Fix: record failure on `r.returncode != 0` or a timeout, and print `err or f"exit {r.returncode}"` — high. Reproduce: a doc with a fenced `python` block `import sys; sys.exit(1)` exits 0.
- MEDIUM — `context/docs.md:34-36` — "fresh, isolated interpreter inside a temporary folder" overstates it. `-I` plus `cwd=tmp` isolates only the import path and the working folder. A block can run `os.system("rm -rf ~")`, write absolute paths, use the network, and read the CI environment's secrets. In CI on fork PRs, running Markdown from the PR is arbitrary code execution. A hang is not possible: POSIX `subprocess.run` kills the child on timeout. Fix: say "not a sandbox, run trusted docs only", pass `env={"PATH": ...}`, and add `stdin=subprocess.DEVNULL` so `input()` can't wait on a terminal — high.
- MEDIUM — `ui/scrollytelling.md:38-52` and step 3 — the observer band is 10% of the viewport and nothing reads `location.hash`. Opening `#step-7` scrolls the step to the top of the viewport. A step shorter than 45% of the viewport then never enters the band, so `render(7)` never runs. A neighbouring step may render instead, and with no hash the initial state is never drawn. This fails the step's own "Pass: opening `#step-7` cold shows state 7". Fix: render the hash target's index on load, call `render(0)` initially, and require step `min-height: 60vh` so a fast scroll can't skip a step — high.
- MEDIUM — `ops/incident.md:21-23` — the mitigation advice covers security events (line 5) but never says to preserve evidence. Rolling back, failing over or rebuilding a compromised host destroys logs and disk state. Fix: add "for a security event, snapshot logs and disks and rotate credentials before wiping" — medium.
- LOW — `ui/sound-design.md:44` — the docstring and the "Cap the volume" step (line 23) say the script checks the family's "loudness", but it compares sample peaks. A sustained tone and a click both peaking at −6 dBFS differ by 10 dB or more in loudness. Fix: add an RMS dBFS spread, or reword to "peak spread" — high.
- LOW — `lang/stdlib-python.md:14-16` — `sys.stdlib_module_names` is absent on a 3.9 floor, so the one-liner raises `AttributeError` on the interpreter the step says to run it on. `filter="data"` (line 48) raises `TypeError` before 3.8.17, 3.9.17, 3.10.12, 3.11.4 and 3.12. Fix: add a version note, or probe with `importlib.util.find_spec` — high.
- LOW — `ops/observability.md:68` and checks line 75 — a `logging.Filter` that sets `record.version` writes nothing unless `"version"` is added to `FIELDS`. The check demands `version` and `service`, which the sample doesn't emit. Step 6's "keep every error and slow trace" also needs tail sampling, which the doc doesn't name. Fix: name both — medium.
- LOW — `context/docs.md:20-23` — "shell examples through a test that executes them" has no runner or snippet, so that step isn't concrete. Fix: add a short runner or say "not provided".

## Acceptance criteria
- Nine playbooks each have "Use when" and a numbered procedure — met. All nine files have the line and `1.`, though `1.` is a weak substring check.
- Reachability — met. Each playbook is listed in its stage `INDEX.md` (`ops`, `ui`, `context`, `release`, `lang`), and `SKILL.md` names each index. The `SKILL.md` ui line doesn't mention charts, scrollytelling or sound (LOW).
- `SKILL.md` under 10,000 characters — met. A regex probe shows 8,000 to 9,000 characters.
- WCAG numbers (3:1 for chart marks, 4.5:1 for text, 24 px / 18.67 px bold for large text, three flashes per second) and the `traceparent` and `rootMargin` usage are correct. The game-feel sound caps match sound-design.

## Implicit decisions
- Plain `-I` Python is the runner. Peak-only audio measurement. Thresholds such as 1,000 series, 30 words and 10 steps are arbitrary but concrete. The `fm lib show` card names were not checked to exist.

## Not checked
- The `fm lib` card names, the `motion.md` token semantics beyond name presence, and the Playwright and VHS specifics.

**Noticed:**
- `INDEX.md` descriptions say "tested run_examples.py", "tested sound_check.py" and "tested JSON logger", but no test in `plugin/tests` covers any of them. Capture a task to add tests for the scripts embedded in the playbooks.
- CHANGELOG has no T-1504 entry in this diff.
- The `SKILL.md` description doesn't mention ops, docs or demos, so triggering on those is weak.
