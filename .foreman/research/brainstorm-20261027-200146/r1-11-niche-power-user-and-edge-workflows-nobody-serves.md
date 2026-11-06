# Brainstorm — lens: niche: power-user and edge workflows nobody serves

- **Read stdin in `fm quiet`** — FIX — value 4 — effort S — risk low — category: CLI input
  Why: A heredoc fed to `fm quiet` does nothing and still exits 0, so a failing script looks like a pass (user report).
  Done when: `fm quiet bash <<'EOF' … exit 3 EOF` runs the script and `fm quiet` exits 3.

- **Release edit leases when the run ends** — FIX — value 5 — effort S — risk low — category: fm code leases
  Why: `drop_session` runs only for worker runs, so a model run's edit leases outlive it and block the next run on the same code for 20 minutes (user report).
  Done when: a model run killed mid-edit frees its leases, and the next run on that code starts without a refusal.

- **Let affected and evidence checks skip the machine-wide gate lock** — PERFORMANCE — value 4 — effort S — risk low — category: gate concurrency
  Why: `fm check --affected` and `--evidence` steps queue behind every other builder's run (user report).
  Done when: two `fm check --affected` runs in two different projects overlap in wall time and both finish without waiting on each other.

- **Cap the gate-lock wait and say when running beside another** — FEATURE — value 3 — effort S — risk low — category: gate concurrency
  Why: A hung check in another project held the lock for over 40 minutes; the user wants at most 15 and an honest note when running in parallel.
  Done when: with a fake lock held past 15 minutes, a full `fm check` proceeds after 15 minutes and its output names the concurrent run.

- **Skip empty "catch it earlier" follow-ups** — FIX — value 3 — effort S — risk low — category: task finish
  Why: `fm task finish` creates a follow-up for why-not-caught answers like "new playbook" or "n/a", which have nothing to catch (user report).
  Done when: finishing a task with why-not-caught "n/a" creates no follow-up, and a real answer still does.

- **Probe headless rendering in `fm doctor`** — FEATURE — value 3 — effort S — risk low — category: doctor
  Why: the user asked for doctor to report whether headless rendering works, and why not when it doesn't.
  Done when: `fm doctor` prints "headless render: available" on a machine with the renderer and a reason line when it is missing.

- **Turn the rules-file budget into a doctor check with a trim suggestion** — CLEAN — value 3 — effort S — risk low — category: doctor budget
  Why: The rules file has been over the 6,400-char budget since T-1520 (6,416 chars), and nothing flagged it until the user asked.
  Done when: `fm doctor` fails at 6,401 chars and lists the lowest-value lines to cut, and passes at 6,400.

- **Index playbook routing so 10,000+ entries stay fast** — PERFORMANCE — value 4 — effort M — risk med — category: playbook routing
  Why: The user wants tens of thousands of playbooks routed, optimized, and actually used; the route has to stay fast and accurate at that size.
  Done when: `fm playbooks route` on a 10,000-entry fixture returns in under 100 ms and picks the same top-3 as a full linear scan on 50 sample queries.

- **Show the usage reset clock in the status line** — FEATURE — value 3 — effort S — risk low — category: usage visibility
  Why: Deferrals and budget decisions hinge on the weekly reset (T-1802 was a midnight-vs-02:00 bug), so the reset time should be visible without a command.
  Done when: the status line shows the next reset in local time, and it matches `fm cost` output.

- **Night shift: run queued brainstorms only in idle time with usage headroom** — FEATURE — value 4 — effort M — risk med — category: unattended runs — wild
  Why: assumption: the user wants unattended work that doesn't burn the weekly budget, and the pack shows repeated concern about usage. A morning report would close the loop.
  Done when: with the machine idle and headroom above a set threshold, a queued brainstorm starts; with the threshold unmet, it stays queued and the morning report says why.

- **Replay a finished task as a text movie to audit its reasoning** — FEATURE — value 2 — effort M — risk low — category: audit — wild
  Why: assumption: reviewers need to see how a change was reached, not just the diff. The transcript and journal already exist.
  Done when: `fm task replay ID` prints steps with timing in order, and its step count equals the journal's event count for that task.

- **Sneakernet evidence bundle that verifies offline** — FEATURE — value 3 — effort M — risk med — category: local-first, proof — wild
  Why: assumption: a task's proof should travel with it to a machine with no network, and the existing `fm task prove` can rerun commands from a bundle.
  Done when: `fm task bundle ID` writes one file, and on a clean machine `fm task verify bundle.tgz` reproduces the pass/fail result with no network calls.
