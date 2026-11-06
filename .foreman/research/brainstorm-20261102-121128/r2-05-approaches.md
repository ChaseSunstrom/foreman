# Brainstorm — lens: approaches

- **Plan the idle spend as a budget, not a loop** — FEATURE — value 5 — effort M — risk med — category: budget
  Why: the request is "usage 0%, go wild", the budget is $200, and the steer rules say never stop for pace (`--pace off`). Nothing ranks work by value per dollar. This approach is knapsack selection from the open queue and the exam backlog, with a reserve and a hard stop. The trade-off is that it needs cost estimates per task kind, which only exist roughly in the duel data.
  Done when: `fm burn --plan` prints a ranked list whose estimated total is at most budget minus reserve, and a later `fm burn --report` shows planned vs actual cost per item.

- **Probe every blocked task against today's world** — FIX — value 4 — effort S — risk low — category: queue hygiene
  Why: T-0335, T-0336, T-0337, T-0418 and T-0352 have sat blocked for a long time. The Genesis rule says each Seed retries items a new capability may unblock. A cheap unattended probe (does `codex`, `gemini` or `opencode` exist now, did the CLI hooks change, is the package installed) beats a human rereading each blocker.
  Done when: each blocked task carries a "blocker re-tested on <date>: still true / cleared" line, and a cleared one moves to open.

- **Run a cold newcomer persona against the README** — FEATURE — value 5 — effort M — risk low — category: user value
  Why: T-0862 and T-0863 (tour, start ladder) are deferred because they "need evidence". A tool-less or Haiku child holding only the README and `install.sh` output attempts the first hour and logs each place it stalls or guesses. That supplies the evidence and costs pennies. The trade-off is that a model's confusion only approximates a human's.
  Done when: `fm newcomer` writes a stall list with a README line per stall, and a docs fix closes at least one.

- **Test install on clean distros with no `claude` on PATH** — FIX — value 4 — effort M — risk low — category: reliability
  Why: a standing rule says `install.sh`, `fm`, `fm doctor` and the task loop work without `claude`, but the blocked items are Arch-specific (`libappindicator-gtk3`). Nothing shown proves another distro. The approach is throwaway containers for Debian, Fedora and Alpine that run install, `fm doctor` and `fm demo`.
  Done when: a matrix report lists pass or fail per distro, and a failure files a task.

- **Run the fenced command blocks in README and MASTER nightly** — FEATURE — value 4 — effort M — risk med — category: docs
  Why: the docs proof kind (T-2616) checks only doc lines a task landed, and there is a rule that public claims must match evidence. Executing the documented commands in a sandbox catches drift (like the `fm night --print-timer` flag removed on purpose) that line checks can't.
  Done when: a doc block naming a removed verb or flag turns the nightly run red with the file and line.

- **Replay the credential-redaction path against a public secret-format corpus** — SECURITY — value 4 — effort S — risk low — category: security
  Why: T-2624 fixed one pasted key reaching the inbox. The class is "formats the redactor doesn't know". Reusing a gitleaks-style rule set as test input sweeps the siblings, as the "sweep a whole class" idea asks, and no new detector gets written.
  Done when: a test feeds every corpus format through intake, ledgers and the web UI, and none reaches stored text unredacted.

- **Add `fm why` for any verdict, hook note or refusal** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: there are 30+ steers, checks, ratchets and guard rules, and the user keeps asking for an automatic check, a ratchet or an explanation. Tracing one output back to its rule, steer id and record is what a person debugging Foreman needs. The approach is to read what is already stored, with no new data.
  Done when: `fm why <hook-note|refusal id>` prints the rule, the steer it came from and the evidence record, and exits non-zero when none is found.

- **Auto-bisect an exam regression to a commit** — FEATURE — value 4 — effort M — risk med — category: reliability
  Why: the self-change gate compares wall time and exam arms exist, but a drop is only reported, not located. Using a failing scenario as the `git bisect run` predicate is a reuse of git.
  Done when: a seeded regression yields a named commit and a draft fix task.

- **Fetch a ceremony-per-task-kind table from a Haiku-vs-Sonnet replay of finished tasks** — PERFORMANCE — value 4 — effort L — risk med — category: cost
  Why: T-1266 and T-1231 (cost and time vs Claude Code) are deferred on duel data. Idle budget can generate that data by replaying past task prompts under light, full and guard-only ceremony. Trade-off: replay isn't the same as live use.
  Done when: a table of kind × ceremony with pass rate and cost per cell exists, and `fm next` reads it.

- **Wild: Hold a constitution court** — FEATURE — value 3 — effort M — risk low — category: simplicity
  Why: wild. Three cold models read gen-0, the standing steers and MASTER clauses and argue contradictions: two rules that can't both hold, or a steer with no remaining check. Rulings become decisions via `fm decide`.
  Done when: a run lists at least the rule pairs flagged, each quoting both lines, and a human-confirmed one is recorded.

- **Wild: Run a read-only status page that works over a local network and nothing else** — FEATURE — value 3 — effort M — risk low — category: devices
  Why: wild; assumption: the user checks the queue away from the desk. A static `status.json` plus a one-file page served only on the tailnet or LAN reuses the genesis site data pipeline and sends nothing to a third party.
  Done when: a phone on the LAN loads the queue, blockers and last receipt with the server's outbound network blocked.

- **Wild: Run a "dream" pass that picks random old closed tasks and re-derives them from the current repo** — FEATURE — value 3 — effort L — risk low — category: agents
  Why: wild. If a cold agent can't re-solve a closed task from its brief, the brief, tests or docs were carrying hidden knowledge. This tests whether Foreman's memory is in the repo or only in history.
  Done when: a sample of 10 closed tasks produces a report of re-solved or not, with the missing context named for each failure.

Next question: Which of these can run unattended inside the pace-off steer without needing a cap only the user can raise?
Next question: What does one idle dollar currently buy in verified outcomes, and has that ever been measured?
