# Brainstorm — lens: user value

Most of the remaining ground is marginal, so this is 6 ideas rather than 8. Ideas 1 and 3 are the ones I'd rank above the rest.

- **Audit the session's fixed context overhead beyond Foreman** — FEATURE — value 4 — effort M — risk low
  Why: the user reports one session burning 20% of weekly usage. Every turn re-reads CLAUDE.md files, MCP tool schemas, other plugins' skills and hooks, and memory, and Foreman only measures its own rules. Assumption: these can be sized from config files, and unused MCP servers can be found from tool names in transcripts.
  Done when: `fm doctor --overhead` lists each source with estimated tokens per turn and last-30-day use, and proposes trims as one yes/no per item, changing nothing without a yes.

- **Collect a one-tap verdict on selected finished tasks as ground truth** — FEATURE — value 3 — effort S — risk low
  Why: the ideas so far on tuning gates, profiles and A/B rule tests rely on rework detection as the only outcome signal. Assumption: an occasional yes/no is acceptable if kept rare.
  Done when: for L tasks and weak-grade tasks the outcome report ends with "did this land? yes/no", the answer is stored on the brief, and `fm digest` shows verdict rate by tier and grade.

- **Nudge parallel and batched tool calls from observed serial patterns** — PERFORMANCE — value 3 — effort S — risk low
  Why: every turn re-reads the whole context, so cost grows with turn count. Existing ideas cut output size or add macros (`peek`, `step`), but nothing targets the model issuing independent reads or edits one turn at a time. Assumption: this pattern is common in transcripts.
  Done when: a replay of a recorded transcript with 4 consecutive independent Reads emits one note per task, and `fm cost` shows turns per task before and after.

- **Park tasks on machine-checkable external waits and auto-resume** — FEATURE — value 3 — effort M — risk med
  Why: "park approvals" covers only user yes/no. Tasks also block on an API key, a deploy, a CI run or a file appearing, and today that stalls the drive loop or gets a nagging question. Assumption: most waits reduce to env, file or command-exit checks.
  Done when: `fm task wait --until "<check>"` parks the task, `fm run` proceeds to the next queued item, and the SessionStart line lists waits whose check now passes.

- **Spend leftover weekly budget on queued low-risk work** — FEATURE — value 3 — effort M — risk med
  Why: the throttle idea only lowers ceremony as the budget drains; nothing uses unspent budget before the weekly reset. Assumption: the weekly cap is user-entered or inferable from `fm cost` history.
  Done when: with a cap set and more than 30% headroom in the last 24 h before reset, and after one standing yes, `fm run` executes only the queue's S/M CLEAN and idle-time items and stops at a spend ceiling. A test with fake cost data covers this.

- **Serve installed-dependency API facts locally with `fm api`** — FEATURE — value 3 — effort S — risk low
  Why: "check imported names after edit" catches wrong calls late, and nothing lets the model look up the real signature first without web fetches or reading site-packages. Assumption: Python-first via `inspect` in a subprocess.
  Done when: `fm api requests.get` prints the signature and the first docstring lines from the installed version in under 500 chars, and reports "not installed" or "unknown" instead of guessing.
