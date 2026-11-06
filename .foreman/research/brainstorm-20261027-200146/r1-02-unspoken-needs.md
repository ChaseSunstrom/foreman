# Brainstorm — lens: unspoken needs

- **Make Foreman notice its own usage burn and tune itself** — FEATURE — value 5 — effort M — risk med — category: usage budget
  Why: The user asked for usage to be handled without being told ("foreman should've figured it out itself"), and the pack shows manual fixes: compact at 200k, Sonnet for builders. Assumption: the journal already records per-reply context size.
  Done when: a fixture run whose replies exceed 140k context triggers compaction and a cheaper builder model with no flag set, and the journal records both decisions with their reason.

- **Run unattended to a spend cap with no permission prompts** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: The user said "don't ask me for anything… just go, full force, but efficient." Assumption: the queue and spend ledger exist, but a cap is not enforced across the whole queue.
  Done when: a queue of three fixture tasks with a $0.50 cap runs without prompting, stops before the cap is exceeded, and prints the spend and the tasks left.

- **Release edit leases when their run dies** — FIX — value 4 — effort S — risk low — category: code leases
  Why: The pack says leases outlive the run (drop_session only ran for worker runs), so the next run is refused for 20 minutes.
  Done when: killing a model run mid-edit frees its leases, and a second run on the same files starts within 1 s in a test.

- **Make `fm check --affected` skip the machine-wide gate lock** — PERFORMANCE — value 4 — effort S — risk low — category: gate lock
  Why: The pack reports that affected and evidence runs wait behind other builders' full checks.
  Done when: with a full check holding the lock, `fm check --affected` finishes on a fixture repo while the lock is still held.

- **Explain any stalled run with `fm code why <id>`** — FEATURE — value 4 — effort S — risk low — category: run diagnosis
  Why: The user asked for this directly (T-1373): status, the stop point, the stall's cause and the next command.
  Done when: a fixture run stalled at a known step prints its status, stop point, cause and the next command.

- **Read stdin in `fm quiet`** — FIX — value 3 — effort S — risk low — category: CLI stdin
  Why: The user reported that a heredoc fed to `fm quiet` does nothing and exits 0.
  Done when: `fm quiet <<'EOF' … EOF` runs the script, and a case with no stdin exits nonzero with a message.

- **Cut playbook routing to a shortlist at 10,000 entries** — PERFORMANCE — value 4 — effort L — risk med — category: playbook routing
  Why: The user asked for tens of thousands of playbooks, optimized and actually used. Assumption: routing scans every entry today.
  Done when: `fm playbooks route` over 10,000 synthetic entries returns in under 100 ms and picks the expected playbook for 20 of 20 fixture queries.

- **Have the doctor flag an over-budget rules file and propose a trim** — FEATURE — value 3 — effort S — risk low — category: rules budget
  Why: The rules file has been 16 chars over the 6,400 budget since T-1520 (6,416).
  Done when: `fm doctor` reports the overage, and a trimmed draft under 6,400 chars is printed as a diff.

- **Carry a handoff ledger across a compaction** — FEATURE — value 4 — effort M — risk med — category: context continuity
  Why: Assumption: compaction at 200k drops decisions and open steps, which makes the next turn re-derive them, and that costs tokens.
  Done when: after a forced compaction in a fixture run, the next turn restates the open steps from the ledger without re-reading any file.

- **Save a repeated request as a playbook when it appears a third time** — FEATURE — value 3 — effort S — risk low — category: repeat detection
  Why: The user's words repeat across sessions (the usage-burn ask came up several times), so Foreman could turn repeats into a saved playbook. Assumption: request history is stored.
  Done when: a fixture with the same request three times offers one playbook, and declining it stops the offer.

- **Wild: spend the reset window on brainstorms** — FEATURE — value 3 — effort M — risk med — category: idle capacity — wild
  Why: wild. When quota is near zero, Foreman defers work. After the weekly reset it could run the next brainstorm lens children with the fresh allowance and file their ideas.
  Done when: at zero quota the queued lens runs wait, and after a simulated reset one lens child runs and its ideas land in the task list.

- **Wild: a usage weather strip above the prompt** — CLEAN — value 2 — effort S — risk low — category: glanceable status — wild
  Why: wild. The user keeps asking about usage, so one glanceable line could show the burn rate, time to reset and the cap. Assumption: the usage numbers are available locally.
  Done when: the status line shows burn, reset time and cap in one line of under 60 chars in a fixture.
