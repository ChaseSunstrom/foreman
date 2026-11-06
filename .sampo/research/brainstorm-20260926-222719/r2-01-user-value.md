# Brainstorm — lens: user value

Round three: the remaining gaps are mostly in checks on the *code Claude writes* and in closing loops outside the local session. Most other angles are already covered by the ~200 ideas above, so I'm proposing 6 and marking assumptions.

- **Check imported names and attributes against installed packages after each edit** — FEATURE — value 4 — effort M — risk low
  Why: assumption: wrong-API and hallucinated-symbol errors are a common cause of failed runs and wasted turns. Nothing above catches them before tests run, and there is no `fm api` lookup. A PostToolUse note could resolve imports with `ast` and `importlib.util.find_spec`, and check `from x import y` names statically. It would say "`requests.get_json` not found in installed requests 2.x" in one line.
  Done when: a fixture edit that imports a nonexistent name from an installed module produces a one-line note naming the symbol, and a valid edit produces none.

- **Close the loop with CI and PR review results after a push** — FEATURE — value 4 — effort M — risk med
  Why: assumption: `gh` is on PATH and the user pushes. "Mirror CI" only derives gates from the CI config. Nothing reads what CI or reviewers said afterwards. `fm ci` (a CLI call, not a hook) would fetch status and failing-job log tails for finished tasks' commits. It would reopen the task as a FIX brief with the log excerpt attached, behind one yes/no.
  Done when: with a stubbed `gh` returning a red run for a task's commit, `fm ci` queues a FIX brief linked to that task containing the failing excerpt.

- **Cite-check research answers** — FEATURE — value 3 — effort S — risk low
  Why: RESEARCH is a task type, and "check the final message's claims against evidence" covers only claims about the work done. A mechanical pass would resolve every `path:line` and backticked symbol in a research brief or final answer: the file exists, the line is in range, and the symbol appears near it. Unresolvable citations block done.
  Done when: a research brief citing a missing file or a symbol absent from the cited line fails `fm task done` and names the bad citation.

- **Add polyglot adapters for outline, symbol lookup and test↔source links** — FEATURE — value 4 — effort L — risk med
  Why: assumption: `fm outline`, `fm where` and `fm map` links rely on Python `ast`. Most user projects are JS/TS, Go or Rust, so the token-saving read tools may degrade to whole-file reads there. Use per-language signature regexes and naming conventions (`*_test.go`, `*.test.ts`) behind one adapter table.
  Done when: `fm outline` on a TS file and a Go file lists their functions, classes and types with line numbers, and `fm impact` maps a `.test.ts` to its source.

- **Sweep the queue for briefs made obsolete by later work** — CLEAN — value 2 — effort S — risk low
  Why: "short-circuit already done" runs only at intake, and "re-ground by scope delta" runs only at focus. Briefs queued for days can be satisfied or moot by then. A SessionStart-adjacent `fm tidy` step would run each queued brief's criteria checks, and propose closing those that pass or whose scope files are gone, as one batched yes/no.
  Done when: a queued brief whose criteria already pass is listed as "likely done" in the tidy output and is closed on approval.

- **Add recurring standing orders checked at session start** — FEATURE — value 3 — effort M — risk low
  Why: assumption: users want periodic hygiene (dependency sweep, sentinel run, docs check) but never run commands. Ideas above cover idle-time and sweep queues, but there is no user-stated "every week do X". Store recurrence in a template brief. Enqueue when due at SessionStart or `fm run`, with no daemon, so uninstall stays clean.
  Done when: a brief with `every: 7d` is enqueued once when 7 days have passed, and not again until 7 more days.

- **Queue a PERFORMANCE brief when gate time dominates task time** — PERFORMANCE — value 3 — effort S — risk low
  Why: `fm check` already times gates and prints slow-gate notes. Nothing acts on them, and slow gates cost wall time and turns on every task. When a gate exceeds a threshold share of the task's elapsed time across three tasks, queue a brief naming the slowest tests.
  Done when: replayed timing data with a gate over the threshold on three tasks yields exactly one queued PERFORMANCE brief listing the slowest tests.

Beyond these, I'd call further ideas marginal.
