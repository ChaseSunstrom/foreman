# Brainstorm — lens: reliability

- **Run a ledger kill-point sweep on the real writers** — FIX — value 5 — effort M — risk low — category: durability
  Why: the pack's earlier questions ask which side wins and what happens after torn writes; fm drill has a dropped-class fault (T-2648) but I see no evidence of SIGKILL between append and fsync across every ledger writer. assumption: some writers aren't torn-tail tolerant.
  Done when: a test SIGKILLs a child at each write step of every ledger writer and every reader then loads the file and names the torn line without raising.

- **Make grant spending two-phase** — FIX — value 5 — effort M — risk med — category: durability
  Why: pushes run through fm ship under a push grant spent on use; a crash between push and grant-spend can double-push or lose the grant. assumption: spend is a single-step write today.
  Done when: a fault-injection test kills `fm ship` after the push and before the spend record, and the next run reports "push done, grant unspent" and does not push twice.

- **Print a degraded line after any fail-open** — FEATURE — value 5 — effort S — risk low — category: visibility
  Why: the open question "what does the user see in the first minute after a silent fail-open" is unanswered. assumption: hooks swallow errors and print nothing.
  Done when: forcing a hook import error makes the next prompt show one "Foreman running degraded: <reason>" line, and a test asserts it.

- **Precedence table for hand vs Foreman edits** — CLEAN — value 4 — effort M — risk med — category: consistency
  Why: the earlier question about which side each reader trusts when the user's hand and Foreman's both change tree, queue or ledger. The hand-edit-mining asks (c14) show the case is real.
  Done when: one table in MASTER.md lists tree, queue, ledger and steers with the winning side, and a test per row edits by hand mid-task and checks the reader follows the table.

- **Soak the unattended drive through real suspend and network loss** — FIX — value 4 — effort L — risk med — category: unattended
  Why: the earlier question about unattended paths never run end-to-end on a real clock while the machine slept. FOREMAN_NOW (T-2645) fakes time but doesn't suspend anything.
  Done when: a scripted run on a scratch repo suspends the machine or its VM mid-task, drops the network, resumes, and the drive finishes or reports a named stop with no duplicated commit.

- **Detect refile livelock in the self-advancing tower** — FIX — value 4 — effort S — risk low — category: loops
  Why: the standing rule makes the tower file its own fix tasks and re-run; nothing in the pack caps a fix that reopens itself.
  Done when: a fixture where a sweep re-files the same fix three times stops after the third with a named "livelock" item, and a test proves it.

- **Open a landing breaker after a red main** — FEATURE — value 4 — effort M — risk med — category: shipping
  Why: the push grant lets the tower ship to main; no evidence of a stop after a failed CI run on a Foreman push. assumption: ship checks only before the push.
  Done when: after a simulated red CI on the pushed sha, `fm ship` refuses further pushes for the cooldown and names the sha.

- **Report alive-but-idle timers** — FEATURE — value 3 — effort S — risk low — category: unattended
  Why: nothing tells a dead timer from a sleeping machine, and T-2542 covers liveness only in part. assumption: doctor reads the last tick time only.
  Done when: fm doctor separates "last tick N hours ago, machine was asleep" from "timer unit inactive" using the journal and the unit state.

- **Wild: Pull-the-plug day** — FEATURE — value 4 — effort L — risk med — category: chaos — wild
  Why: reliability claims stay untested until the real drive is killed at random. assumption: a scratch repo and a kill switch are enough to make this safe.
  Done when: a seeded random SIGKILL schedule over a 4-hour drive on a scratch repo ends with `fm fsck` clean and no lost closes.

- **Wild: Run the guard in two independent implementations and block on disagreement** — SECURITY — value 3 — effort L — risk med — category: guard — wild
  Why: a single regex guard has silent failure modes, such as pathological input (T-2668) and parser gaps. assumption: a second shell-parser-based implementation can stay small.
  Done when: on the guard exam corpus the two implementations disagree on no more than a listed handful of cases, each of which blocks.

- **Wild: Fall back to the last good install generation when a hook fails to import** — FEATURE — value 4 — effort M — risk med — category: self-repair — wild
  Why: a broken edit of plugin/lib on a self-modifying tower can take every hook down at once. assumption: installs are overwritten in place today.
  Done when: a test plants a syntax error in the installed hook, and the next hook call runs the previous generation and writes a "fell back" record.

- **Rehearse a reboot in a throwaway VM** — FIX — value 3 — effort M — risk low — category: durability
  Why: state under /run/user (the tmpfs working directory in this environment) vanishes on logout; the earlier audit of volatile paths is scoped narrowly.
  Done when: after a VM reboot, fm doctor lists exactly which state was lost and which unit units came back.

Next question: which Foreman verbs write state in more than one file, and what does a crash between those writes leave for each reader?
Next question: what does the drive do when `git` itself is locked or the index is mid-rebase by the user's hand?
