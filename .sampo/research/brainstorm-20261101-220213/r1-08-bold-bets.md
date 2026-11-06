# Brainstorm — lens: bold bets

- **Prove the guard is alive every session** — SECURITY — value 5 — effort S — risk low — category: guard
  Why: assumption: a Claude Code, Codex or Gemini update can change the hook schema and silently disable the guard, and nothing today notices. Session start would fire one harmless canary that the guard must deny, and a miss prints a loud banner and files a task.
  Done when: a test with a stubbed host that ignores hooks makes `fm doctor` and the session-start line report "guard NOT enforcing" and exit non-zero.

- **Fix the brief-guard path false positives with real parsing** — FIX — value 4 — effort S — risk low — category: guard
  Why: the pack shows 2 false positives where a dict key and a `.join(` call were read as written paths. Replace the regex with shlex/AST tokenization and keep every logged false positive as a permanent fixture.
  Done when: both logged inputs pass, and a corpus test of all past blocks still blocks the true positives.

- **Compile one guard rule file into every enforcement point** — FEATURE — value 5 — effort L — risk med — category: guard
  Why: the guard lives in Claude hooks, while T-0335 and T-0337 show other agents lack grants and a Stop gate. A single rule source would emit the Claude hook, a git pre-commit/pre-push hook, an MCP tool filter and a Landlock policy.
  Done when: `fm guard compile` emits all four, and one dangerous-command fixture is denied through each of them.

- **Run any agent inside a kernel jail with `fm jail`** — FEATURE — value 5 — effort L — risk high — category: sandbox
  Why: assumption: hookless agents can't be guarded at the hook layer, and gen-0 says Foreman isn't Claude-only. It launches the agent under Landlock or bubblewrap with the compiled guard policy as filesystem and network rules. Needs a spike first.
  Done when: a Codex or opencode session started with `fm jail` cannot write outside the worktree or read `~/.ssh`, shown by a test that tries.

- **Meter Foreman's share of every reply's context** — FEATURE — value 4 — effort M — risk low — category: context
  Why: context averages 387k per reply and the SessionStart note is ~2k chars × 89, but nothing says how much of that is Foreman's. The meter counts injected bytes per hook per reply and shows the share on the status line. The ratchet fails the sweep when the share rises without a measured gain.
  Done when: `fm cost` prints Foreman's injected tokens and percentage of total per hook, and a test fails when a hook's injection grows past its recorded cap.

- **Cold-store unused cards and skills** — CLEAN — value 4 — effort M — risk low — category: subtraction
  Why: `fm lib stats` shows 5 of 1219 cards used, and plugin/skills holds 1388 files. Move cards unused for N days into a cold archive, keep a name index, restore on first lookup, and let the burden report count the saving.
  Done when: the installed plugin ships under half its current file count and `fm lib show` still restores a cold card in one call.

- **Move verbs unused for 60 days into `fm lab`** — CLEAN — value 3 — effort M — risk med — category: subtraction
  Why: gen-0 §6 says each generation subtracts as much as it adds, and `fm burden --by-verb` already exists. The old name stays as a shim that prints the new path, so nothing breaks, and the next sweep lists the lab verbs for deletion.
  Done when: the sweep moves at least one unused verb, and the old name still works with a one-line notice.

- **Show the minimum dose of Foreman's injection per task kind** (wild) — PERFORMANCE — value 4 — effort L — risk med — category: lean
  Why: wild; assumption: some injected blocks are dead weight. Run the same held-out scenarios at 0%, 50% and 100% of the injection, using free and Haiku arms only per the testing cadence. Publish the curve per task kind.
  Done when: a table shows pass rate and tokens per dose level for at least 3 task kinds, and one block is trimmed where the curve is flat.

- **Hold a monthly lean court that tries to delete the least-used 5%** (wild) — CLEAN — value 4 — effort M — risk med — category: lean
  Why: wild; T-2503 only flags growth that was measured and showed no gain. A prosecutor lane proposes deleting the least-used code, skills and hooks in a scratch copy, and any deletion the zero-token exam arms don't notice becomes a real task.
  Done when: a run files at least one deletion task with exam evidence that nothing regressed.

- **Ship a hot-path guard as a tiny precompiled binary with a Python fallback** (wild) — PERFORMANCE — value 4 — effort L — risk high — category: hooks
  Why: wild; p95 is 278 ms over 13.5k runs and T-0832 (a shell prefilter) is deferred. A static binary generated from the compiled rules would answer the allow or deny decision in a few ms. It needs a spike, with Python as the authority on any disagreement.
  Done when: bench_hooks shows the guard path p95 under 30 ms, and a differential test shows zero disagreements with the Python guard on the logged corpus.

- **Replay all logged guard decisions against every candidate rule change** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the guard blocked the interpreter-code-driving rule 42 times in 7 days, and false positives surfaced only after users hit them. A rule change must first replay the recorded decisions and report which flip.
  Done when: `fm guard replay` prints flipped allow→deny and deny→allow counts, and `fm ship` refuses a guard change without that report.

- **Serve the web UI safely by default for headless and server use** — SECURITY — value 3 — effort M — risk med — category: server
  Why: assumption: "headless/server" is an empty coverage cell and the web UI is the only surface found. Bind to loopback, require a token, rotate it, and refuse to bind publicly without an explicit setting.
  Done when: a test shows a non-loopback request is rejected, and a public bind fails without the flag.

Next question: Which of Foreman's 13 capabilities cost the most injected context per task they help pass, and would the exam still pass with them off?
Next question: When a host updates and its hook behaviour changes, how long does Foreman take to notice today, and who is told?
