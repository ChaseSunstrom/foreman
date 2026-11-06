# Brainstorm — lens: unspoken needs

- **Cap child processes with a resource governor** — PERFORMANCE — value 4 — effort M — risk low — category: performance
  Why: five recent fixes stop two test suites running at once, which treats the symptom. The need behind them is that the machine stays responsive while Foreman works. Assumption: the user's laptop stutters during gates; the pack doesn't say.
  Done when: test runs, `claude -p` children and ambient runs start under `nice`/`ionice` with a configurable memory cap, and a test shows a child that exceeds the cap is killed and named in the output.

- **List the tests that encode old behaviour before editing** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: steers show fixes finding their side effects late ("test_check_paths' writing-gate case now expects…", "ac 1's -k matched no test"). A preflight that greps tests for the message or behaviour being changed would catch these earlier.
  Done when: `fm task start` on a task that changes a message string prints the tests asserting it, and a fixture task shows the right list.

- **Give blocked tasks a machine-checkable unblock condition** — FEATURE — value 4 — effort S — risk low — category: queue
  Why: T-0325, T-0418, T-0335 and T-0336 are blocked on a package, an install or a live CLI. Nothing re-checks them, so they sit blocked after the cause is gone.
  Done when: a task with `UNBLOCK-WHEN: <command>` flips to open on the next `fm doctor` or loop round once the command exits 0, and says so.

- **Detect drift between installed copies and the repo** — FIX — value 3 — effort S — risk low — category: doctor
  Why: T-0418 is a stale installed foreman-ui, and the user dogfoods the live install, so a stale mod or plugin cache makes fixes seem not to land.
  Done when: `fm doctor` names each installed surface (plugin, mod, desktop) whose version or hash differs from the checkout, with the one command that syncs it.

- **Watch remote CI after a ship** — FEATURE — value 4 — effort M — risk med — category: shipping
  Why: "Ship Tn to main" is a frequent request and the README carries a tests badge. Nothing in the pack follows main after the push. Assumption: `gh` is available.
  Done when: after a ship, Foreman polls the workflow run and prints green, or files a FIX task with the failing job's log tail when it's red.

- **Scrub demos, recordings and task records before they leave the machine** — SECURITY — value 4 — effort M — risk low — category: privacy
  Why: `demo/live.svg` and the MP4 are recorded from real sessions in a public repo, and PR bodies and eval cases will be built from task records. Absolute paths, emails and tokens can leak through them.
  Done when: a publish scrub run on a fixture containing an email, a home path and a fake token output redacts all three, and `fm doctor` flags unscrubbed recordings.

- **Learn from the user's hand edits to Foreman's output** — FEATURE — value 4 — effort M — risk med — category: lessons
  Why: T-0217 wants lessons to carry confidence. The strongest signal is a commit by the user that rewrites a line Foreman just closed, and nothing in the pack records that.
  Done when: a user edit to a file within a day of its task closing is recorded as a draft lesson, shown for approval, and counted in the lesson's confidence once accepted.

- **Rewrite a blocked command into its safe equivalent** — FEATURE — value 3 — effort M — risk med — category: guard
  Why: in bypass mode the guard hook only denies, so Claude retries variants. Naming the fix in the denial makes the block useful. This goes beyond the dry-one-liner idea, since it must produce a runnable command.
  Done when: a denied `rm -rf` on a path outside the project returns a suggested scoped command, and a test shows the suggestion passes the guard.

- **Forecast the usage runway against the queue** — FEATURE — value 3 — effort M — risk low — category: budget
  Why: "usage ahead of pace" and "risk budget" already drop optional work, and T-1969 had to rename a reason message. The user sees the drops but not when the budget runs out or what the queue needs.
  Done when: `fm status` prints "usage lasts to <day> at this pace; queue needs ~N%", and the estimate is checked against a recorded day.

- **Wild: Notice a hardening phase and propose a release cut** — FEATURE — value 3 — effort M — risk low — category: release
  Why: the last 20 asks are almost all FIX or PERF paper cuts from dogfooding. That mix says the project is in a stabilizing phase, and a release is the natural next move. The pack shows a `cc-plugin-release` card.
  Done when: after a configurable run of FIX-heavy closes with green gates, Foreman proposes a version bump with notes built from the closed tasks, and does nothing until approved.

- **Wild: Run the discipline on non-code work (dotfiles, configs, docs)** — FEATURE — value 3 — effort L — risk med — category: scope
  Why: assumption: the user runs a hardened Arch system with a lot of hand-tuned config. Plan, prove and one-task-at-a-time would apply there too, and "proof" there means a command that shows the config took effect.
  Done when: `fm` in a dotfiles directory plans a change, records the verifying command's output, and offers a one-step revert.

- **Wild: Rehearse protected-core changes in a disposable clone and prove Foreman can still ship itself** — SECURITY — value 4 — effort L — risk med — category: self-hosting
  Why: Foreman fixes its own gates, doctor and ship path all the time. A bad edit could block the very command needed to repair it. The core-integrity warning shows this edge is already felt.
  Done when: a core change runs in a throwaway worktree where the new Foreman closes and ships a canned dummy task, and the real tree isn't touched unless that passes.
