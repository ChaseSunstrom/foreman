# Brainstorm — lens: observability and trust

- **Reconcile two independent ledgers at done** — FEATURE — value 5 — effort M — risk med — category: trust
  Why: assumption: today the evidence trail mixes what hooks observed with what the model reported. Hooks would append a fact-only ledger (commands run, exit codes, files changed, tree hash) that the model cannot write to. The model's claims ("tests pass", "only touched X") go in a second ledger. `fm task done` diffs the two, and any claim with no matching fact becomes a finding.
  Done when: a test where the model records "pytest passed" with no matching hook-observed run makes `fm task done` refuse and name the unmatched claim.

- **Bind evidence to the tree it proved** — FEATURE — value 5 — effort M — risk low — category: evidence
  Why: assumption: evidence is recorded per step but not tied to file content. Stamp each piece with the tree hash of the files it covers (via `fm map` test links). A later edit to those files marks the evidence stale on the board and in `fm sentinel`, so "done" shows as "done, proof stale since commit X".
  Done when: editing a file after a task closes flips that task's proof to stale in `fm ui --json`, and `fm sentinel` re-runs only the stale ones.

- **Attest that the guard was in the loop** — SECURITY — value 5 — effort M — risk low — category: hooks
  Why: evidence: the `bash -lc`/`zsh -ic` miss showed the guard can silently fail to see a command shape, and T-0316 shows Claude Code updates can change hook behaviour. Each session records a heartbeat per expected hook event. A per-session coverage line says "N tool calls, N guard-judged, 0 unseen". A mismatch (tool calls with no PreToolUse record) raises a loud doctor finding.
  Done when: disabling the PreToolUse hook in a test session makes `fm doctor` and the statusline report an uncovered-calls count above zero.

- **Publish a live-tested enforcement matrix per harness** — FEATURE — value 4 — effort M — risk low — category: multi-agent
  Why: evidence: T-0335, T-0336 and T-0337 are blocked or unverified, so the claim that Foreman guards Codex, Gemini and opencode is partly unproven. `fm agents matrix` runs a fixed battery of probes (dangerous command, edit with no task, stop attempt) on each installed harness. It prints enforced / advisory / absent per guard category with the date last proven.
  Done when: the command prints a harness×category table and marks the Gemini Stop gate "absent" until T-0337 lands.

- **List what was not verified on every done** — FEATURE — value 4 — effort M — risk low — category: honesty
  Why: assumption: a pass on a gate says nothing about untested surface. At done, compare the diff against `fm map` test links and the gates run. Print "changed with no linked test: …" and "behaviour claimed with no evidence: …" on the proof card. The user sees the gaps instead of discovering them later, as with JARVIS's band stuck on step 1/5.
  Done when: a task that edits an untested file ends with that file listed under "unverified" in the receipt.

- **Meter the user's attention cost** — FEATURE — value 4 — effort S — risk low — category: metrics
  Why: evidence: the repeated asks include "JARVIS idled", "refused twice in a row", "budget limits shouldn't block until 75%", and Foreman's `fm ask` prompts. Track per task: interruptions, refusals before first success, time blocked on the user, ask-then-yes rate. `fm digest` trends it. The self-improvement pass is aimed at the worst offenders.
  Done when: `fm digest` shows interruptions per finished task for the week and names the top refusal category.

- **Audit grants with expiry and usage** — SECURITY — value 4 — effort M — risk low — category: permissions
  Why: evidence: `fm ask`, `standing`, `trust on` and `sensitive` all grant power, and approval in one context shouldn't silently extend to the next. `fm grants` lists every live grant with the actions that used it. Unused standing yeses auto-expire after a configurable window and are re-asked on next need.
  Done when: a standing grant unused for the window disappears from `fm standing`, and the next matching action asks again.

- **Track version skew across projects** — FEATURE — value 4 — effort S — risk low — category: fleet
  Why: evidence: the user ships a release and relays it to GitHub main and JARVIS by hand each time (1.2.8 to 1.2.16). `fm projects` already enumerates projects. Add each project's installed Foreman version, wiring health and last hook activity, and flag stale or half-wired ones with the one-line upgrade command.
  Done when: `fm projects --json` includes a `version` and `wired` field per project, and a project on an older version is flagged.

- **Bundle an incident on any stuck or confused session** — FEATURE — value 3 — effort M — risk low — category: debugging
  Why: evidence: many fixes originate as "JARVIS hit X" relayed by hand. `fm incident` auto-collects, with redaction, the guard decisions, hook latencies, ledger tail, resume point and Claude Code version into one file. It also offers to turn the bundle into an eval case.
  Done when: running it in a session with a recorded guard block produces a redacted bundle containing that block's command fragment, and `fm secrets` finds nothing in it.

- **Guard playground with a differential against real bash** — FEATURE — value 3 — effort M — risk low — category: guard
  Why: evidence: the guard has real-bash differential tests and a 5000-command replay, yet users still need to ask why a command was refused (T-0404, T-0423). `fm guard try "<cmd>"` prints the parse tree, matched categories and rule, which part tripped, the real bash expansion, and the minimal rewrite that would pass.
  Done when: `fm guard try "fm focus T-1; sed -i x f"` prints the split-the-focus hint and the matched rule id.

- **Wild: Publish a trust passport for each project** — FEATURE — value 3 — effort S — risk low — category: reputation
  Why: wild; assumption: the proof data (verified-done rate, sentinel pass rate, mutation-checked proof share) exists locally. Generate a README badge and a one-page passport from it. The data is aggregate and redacted, and nothing is sent unless the user opts in.
  Done when: `fm passport` writes a badge file and page whose numbers match `fm digest` for the same period.

- **Wild: Run a pre-flight and canary task before every night run** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: wild; evidence: `fm night` and `fm serve` run unattended on trust alone. Before the user leaves, a pre-flight checks hook coverage, budget pace, a green sentinel and a disposable canary task through a headless session. It prints a go/no-go "trust forecast" and refuses unattended mode on no-go.
  Done when: `fm night --preflight` returns no-go when the guard heartbeat is missing and go after it is restored.

- **Wild: Keep a witness that only observes** — FEATURE — value 4 — effort L — risk med — category: oversight
  Why: wild; assumption: a separate read-only process tails each session's transcript and writes its own notebook of what happened, with no ability to intervene and no access to the agent's reasoning summary. At done, the notebook is compared with the agent's final report. Disagreements go on the receipt as "the witness saw differently". Unlike a supervisor, it never steers, so it can't be argued out of its record.
  Done when: in a seeded session where the agent's summary omits a file it edited, the receipt lists that file as witness-only.

- **Wild: Fire randomized trust drills at the observers themselves** — SECURITY — value 3 — effort M — risk med — category: assurance
  Why: wild; assumption: nobody tests whether the checks would notice failure. Occasionally inject a fault into a sandbox lane: drop a hook event, corrupt a ledger line, plant a stale proof. Then confirm that doctor, sentinel or the done-gate catches it, and record the detection rate over time.
  Done when: a drill that deletes a ledger line is detected by `fm doctor` and logged as "caught", and one that goes undetected opens a FIX task.
