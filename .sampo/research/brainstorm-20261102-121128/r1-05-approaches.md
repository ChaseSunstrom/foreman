# Brainstorm — lens: approaches

- **Spend idle usage on a whitelist of measurement-only runs** — FEATURE — value 4 — effort M — risk low — category: capacity
  Why: the request is "usage is 0%, go wild", but the steers fence session arms (only `--final` or `--regressing N`) and `--pace off` drops no work. Reusing `fm drive` with an allowlist (free arms, `fm bench duel --ablate`, guard-arm runs, cold reads) is cheaper than new machinery. Trade-off: it fills the window but spends nothing on features. Assumption: `--ablate` counts as a bench run, not an exam session arm.
  Done when: with usage at 0%, `fm drive --spend-down` picks only allowlisted tasks, and the spend per task is logged in `fm doctor`.

- **Run a restore drill on a blank HOME** — CLEAN — value 4 — effort S — risk low — category: resilience
  Why: the earlier question "when the host is wiped, what must be rebuilt by hand?" is unanswered. The cheapest approach is a throwaway directory running `install.sh` and `fm doctor`, then listing what is red. Do not build a backup tool first.
  Done when: a script run with an empty HOME and fresh clone prints a "needs hand rebuild" list that matches a checked-in expectation.

- **Mark every overridden or unrun proof as "unproven" in a third state** — FIX — value 5 — effort M — risk med — category: proof honesty
  Why: two earlier questions ask how a headless UI check, or a user's hand override, avoids reading as a pass. The approach is a tri-state receipt (proven / unproven-with-reason / overridden-by-user) with no proof bundle. Doing less beats a bigger bundle when we don't know what the user opens.
  Done when: a finish with no display writes `UNPROVEN: ui check not run (no display)`, and `fm outcomes` counts it outside the held rate.

- **Audit past "proven" labels read-only** — RESEARCH-as-CLEAN — value 4 — effort S — risk low — category: calibration
  Why: the open question is which "proven" labels were later reversed. Scan finished tasks against later reverts, reopens and fix commits, and count those with no run record. No new verb, just a one-off script whose result decides whether anything is worth building.
  Done when: one report gives reversed share and no-run-record share, with task ids.

- **Mine the transcript's bash-input records for the user's hand checks** — FEATURE — value 3 — effort S — risk low — category: user model
  Why: the question "what does the user type to check verdicts, without reading shell history?" has a local answer. The dropped item `fm night --print-timer` shows `!` commands already appear in the session record. Approach: read those, not shell history. Local-first, nothing new is captured.
  Done when: `fm intake` lists the top five repeated hand-run commands over the last 30 days.

- **Cross-check each ops gauge against a second source** — SECURITY — value 4 — effort M — risk low — category: ops trust
  Why: timer liveness (T-2542), bet settlement and canary state are trusted because Foreman wrote them. Approach: pair each with an outside signal (systemd journal, CI run API, git log) and show disagreement in `fm doctor`.
  Done when: killing a timer's journal entry in a test fixture makes `fm doctor` WARN with "gauge says alive, journal disagrees".

- **Delete one ledger record class at a time and watch the readers (wild)** — FIX — value 4 — effort M — risk low — category: ledger integrity
  Why: "which reader gives a wrong answer, not an error, if a record class is missing?" Approach: chaos testing on a copy of the ledgers. For each class, drop it, run every reader, and flag those that return a plausible number instead of failing. Wild: nobody asked, but it finds silent bugs.
  Done when: a test matrix lists each (class, reader) pair as errors, degrades loudly, or answers silently, and the silent ones file tasks.

- **Mutate each finished task's fix to see whether its proof notices (wild)** — FEATURE — value 4 — effort L — risk med — category: proof strength
  Why: `fm task prove` already shows the test fails without the change. Approach: run a cheap mutation pass on the touched lines and report survivors, which are proofs that pass on broken code. Trade-off: it is slow, so use idle usage and sample.
  Done when: a task with a vacuous test gets "proof survived 3 of 5 mutants" on its receipt.

- **Convene a cross-harness jury on disputed "proven" rows (wild)** — FEATURE — value 3 — effort L — risk med — category: cold review
  Why: the steers want signals Foreman didn't author, and T-0336 and T-0335 are blocked on live codex, gemini and opencode. Approach: when a row is disputed or overridden, ask a different harness or model for a cold verdict. Assumption: at least one non-Claude CLI is installed.
  Done when: a disputed row records two independent verdicts, with each harness named in the bet's harness field.

- **Run blind-language scenario generation overnight** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: a steer wants `fm find` recall reported per language and bug type, from child-authored scenarios. A night tick can queue tool-less scenario writers in languages `fm find` wasn't built for. It's cheap and uses free arms first.
  Done when: `fm exam` prints recall per language for at least five languages not in the finder's list.

- **Add a "gap-only" first-hour check instead of a tutorial** — FEATURE — value 2 — effort S — risk low — category: onboarding
  Why: T-0862 and T-0863 are deferred pending evidence. The do-less approach is a single `fm doctor --first-hour` line naming the one missing setup step, not a tour.
  Done when: a fresh install prints exactly one next step, and it vanishes once done.

- **Split foreman-ui `register.tsx` while the budget is idle** — CLEAN — value 2 — effort M — risk low — category: maintainability
  Why: T-0166 has been deferred as M. Idle usage makes it free to try, with the existing `foreman-ui.test.tsx` as the safety net. The standing lean rule is satisfied if line count doesn't grow.
  Done when: band and pane live in their own files, and the mod tests pass unchanged.

- **Stage a self-writing "cheat sheet of unopened proofs" (wild)** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: assumption: the user rarely opens proof bundles. Approach: log opens first, then replace the bundle with a one-line, one-click receipt for the kinds nobody opens.
  Done when: `fm doctor` shows an open rate per proof kind over 30 days.

Next question: which of Foreman's own gauges has never disagreed with an outside source, so we don't yet know whether it can?
Next question: if usage stays at 0% for a week, which single deferred task would the user most regret not having had measured?
