# Brainstorm — lens: user value

- **Stop re-asking answered questions** — FEATURE — value 5 — effort M — risk low — category: interruptions
  Why: the user pushed back three times ("no need to ask me", "stop asking me if you can release", "full auto"). Each time they had to say it again, so the decision never became a rule. A prompt answered the same way twice is a question Foreman should stop asking.
  Done when: after the same permission-style question gets the same answer twice in a project, a third occurrence is auto-answered. It writes one `auto-answered (n/n prior)` line to the run log, and `fm code answers` lists and revokes the rules. A test shows the guard's hard refusals are never auto-answered.

- **Hand a stuck run to a live CLI in one key** — FEATURE — value 5 — effort M — risk med — category: escalation
  Why: assumption: when a harness run fails or stalls, the user's real next step is to take over in an interactive `claude`, `codex` or similar. Today they would have to rebuild the context by hand.
  Done when: pressing `e` on a failed or stalled run opens the chosen interactive CLI in the project with a generated handoff file (request, plan, green steps, failing check output, diff). A test confirms the file holds those five parts.

- **Put a time and money box in the request** — FEATURE — value 4 — effort M — risk low — category: budgets
  Why: the user starts runs with the intent "run through it unattended", and the pack's budget ideas cover only per-call caps and the dollar cap. Nothing parses "by 6pm" or "under $2" from the request. Assumption: a stated limit should steer runner choice too.
  Done when: `fm code "fix X, under $1, within 20 min"` stores both limits. The run stops cleanly at either limit with a resumable state and a receipt naming which limit hit. A fake-clock test proves the stop.

- **Review finished runs as a deck, and reopen with a reason** — FEATURE — value 5 — effort M — risk low — category: review
  Why: the home screen (T-1330) lists past runs, but nothing tells Foreman when "proved" and "what I meant" disagree. T-0217 wants lessons to gain confidence from outcomes, and a rejection is the strongest signal there is.
  Done when: in the TUI, `a` accepts, `r` rejects with a one-line reason and reopens the task with that reason added to its criteria, and `j`/`k` move between runs. A rejection creates a lesson linked to the task.

- **Say no early with a fit check** — FEATURE — value 4 — effort M — risk med — category: triage
  Why: assumption: a request that is too big, too vague or unsuited to the weakest available runner currently burns minutes before it fails. The pack has a quote-back and a preflight, but neither judges the request itself.
  Done when: before the first model call, each request gets a `fit / risky / split first` verdict with one reason, computed without a model call. A table test of 20 sample requests matches the expected verdicts.

- **Show it working with a demo artifact** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: the harness proves checks pass, but the user judges by seeing it work (the nixie run was judged by "is it doing anything"). T-0797 touches native verification only for browsers.
  Done when: a closed run's receipt includes a captured output of one declared demo command, such as a CLI invocation or a rendered page text. It is stored with the task and shown by `fm code show ID`.

- **Answer "why is it like this?" from history** — FEATURE — value 4 — effort M — risk low — category: project memory
  Why: questions already get answers from the files; the task ledger, commit messages and lessons are unread by that path. Assumption: users returning to a project (the "what was I doing here?" case) ask why more than what.
  Done when: `fm code "why does X use Y?"` cites at least one task ID or commit hash from history in its answer, or says no history exists. A fixture repo test checks this.

- **Offer three plans with prices** — FEATURE — value 3 — effort M — risk low — category: choice
  Why: assumption: the cost and time of a request vary a lot between a cheap local runner and Claude. The only existing price view is a startup-tax estimate. The user can't trade quality for cost before the run.
  Done when: for requests over a size threshold, the TUI shows cheap, fast and thorough plan cards, each with a runner, an estimated cost and an estimated time. Enter takes the default; with no TTY the default is taken silently.

- **Run standing orders on events** — FEATURE — value 4 — effort L — risk med — category: automation
  Why: the user wants Foreman to act without being asked ("I shouldn't even need to say anything"). Triggers like "when CI goes red, queue a fix" are named separately in the pack (red CI to task, nightly canary) but have no user-defined form.
  Done when: `fm code order add "on red CI in nixie: run the fix task"` persists a rule. A simulated red event queues the task, and `fm code orders` lists, pauses and removes rules.

- **Train a free apprentice by shadowing (wild)** — FEATURE — value 4 — effort L — risk med — category: routing
  Why: wild. A local model plans each request silently alongside the paid runner, and its plan is scored against the plan that passed. Request kinds where it matches reliably get routed to it, so cost falls without the user choosing.
  Done when: with shadow mode on, `fm code stats` prints per-kind agreement rates. A kind crosses a configured threshold only after N matches, and a test shows the switch is logged.

- **Bisect a bug from a sentence (wild)** — FEATURE — value 4 — effort L — risk med — category: debugging
  Why: wild. "This broke recently" is a common request. The harness already has a fail-first check, so it can walk back through commits in a worktree until the check last passed, then fix with the culprit commit in the plan.
  Done when: on a fixture repo with a known breaking commit, the run reports that commit hash and uses it in the plan. The user's working tree is untouched.

- **Play a skeptical user against the result (wild)** — FEATURE — value 3 — effort L — risk med — category: QA
  Why: wild. After closing, a second runner, with no access to the diff reasoning, uses the built thing from its README alone and reports where it got confused or it broke. Passing checks written by the same run are weak evidence.
  Done when: a planted-bug fixture, where the checks pass but the README example crashes, gets flagged by the second runner. The finding appears as a follow-up task and does not block the close.
