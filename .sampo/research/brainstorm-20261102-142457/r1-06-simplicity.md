# Brainstorm — lens: simplicity

- **Lint every outward effect to one chokepoint** — SECURITY — value 4 — effort M — risk low — category: safety
  Why: pushes already go through `fm ship` with a spendable grant, but nothing shows that no other path can push, publish or curl. assumption: some `plugin/lib` modules call `git push`, `gh` or `curl` directly.
  Done when: a test greps every subprocess and network call in `plugin/lib`. It fails on any outward call outside the grant module, and a planted `subprocess.run(["git","push"])` turns it red.

- **Turn unused verbs into a pre-proven deletion patch** — CLEAN — value 4 — effort M — risk med — category: subtraction
  Why: the dropped note on `fm tidy --verbs` says `fm usage --prune` (fmcost.py:1480) only lists unused verbs and files a CLEAN capture. Nobody does the cut, so the list is read and ignored.
  Done when: `fm usage --prune --draft VERB` writes a branch that removes the verb, its tests, docs and completion entries. The full suite passes on it and the output ends with net lines removed.

- **Prove the zero-config install is safe** — SECURITY — value 4 — effort S — risk low — category: defaults
  Why: the standing rule says `install.sh` and `fm` work with no `claude` on PATH. Nothing shows that an install with no config file still blocks the dangerous commands.
  Done when: a test runs a clean `$HOME` with no settings and replays the red-team set through the guard. Every dangerous command is blocked and `fm doctor` has no red row.

- **Put a deadline on each pending-measurement lean row** — FIX — value 3 — effort S — risk low — category: lean
  Why: T-2503 lets capabilities with no exam or outcome measurement sit as "pending", not red, with no task. Nothing ends that wait, so growth can stay unmeasured indefinitely. assumption: the sweep stores no age for pending rows.
  Done when: the sweep stamps the first-seen date on each pending row. After 21 days it files a "measure or default-off" task, and a fixture row aged 22 days produces that task.

- **Keep a list of the external programs Foreman may run** — SECURITY — value 3 — effort S — risk low — category: dependencies
  Why: Foreman claims to be harness-agnostic, but the set of binaries it shells out to (git, gh, systemctl, claude, codex and others) is implicit. assumption: no single list exists today.
  Done when: `plugin/lib/allowed-exec.txt` lists the programs, and a test fails when a new program is invoked that isn't on it. `fm doctor` prints which listed programs are present on this host.

- **Write an install manifest and uninstall from it** — SECURITY — value 3 — effort M — risk low — category: reversibility
  Why: the idea list has eject and uninstall rehearsals but no record of exactly what the installer wrote. Without a hashed manifest, "remove Foreman" is a guess.
  Done when: `install.sh` writes `manifest.tsv` with path and hash for every file, unit and hook it adds. `fm uninstall` removes only those paths, and a post-uninstall tree diff against the pre-install snapshot is empty.

- **Cap the default install at 40 skills and load the rest by name** — PERFORMANCE — value 3 — effort M — risk med — category: footprint
  Why: `plugin/skills` holds 1388 of 2125 files, and `cc-skill-descriptions` is already a stack card, so descriptions cost context at every session start. assumption: most sessions trigger fewer than 40.
  Done when: a fresh session loads at most 40 skill descriptions. `fm skill load NAME` fetches any other, and a bench shows session-start injected tokens dropped.

- **Wild: Nightly deletion race on the costliest 20% of code** — CLEAN — value 4 — effort L — risk med — category: subtraction — wild
  Why: the idea list has many subtraction ideas, but none go after the specific code behind the most ceremony cost. assumption: `fm cost` can attribute time and tokens to modules.
  Done when: a nightly lane ranks modules by ceremony cost and tries removing the top one on a branch. The branch is offered to the user only if the zero-token exam arms hold, and one such branch has merged.

- **Wild: "What runs on your machine" one-pager** — FEATURE — value 3 — effort M — risk low — category: transparency — wild
  Why: users who run in bypass mode have no single view of what Foreman installs and runs. That view is also the cheapest trust-builder for a lean tool.
  Done when: `fm where` prints hooks, timers, written paths, programs run and network hosts contacted, with counts and a diff since last week. A new hook added in a test shows up in the diff.

- **Wild: Publish a lean ledger on the Genesis site** — FEATURE — value 3 — effort S — risk low — category: accountability — wild
  Why: the user publishes Genesis to `site/genesis` on every tower change, yet growth gets more attention than removal. A public net-lines, net-verbs and net-steers figure per generation makes subtraction visible.
  Done when: `fm genesis live` writes `lean.json` with per-generation net lines, verbs and skill files. The site draws it, and a generation that only adds is shown in red.

- **Accept a pasted verdict from another agent only as a claim to re-run** — SECURITY — value 3 — effort S — risk low — category: injection
  Why: "Check pasted claims from another AI against the repo" is in the list, but the safety side isn't. A pasted "all tests pass" must never become a ledger record.
  Done when: a pasted block containing "tests passed" produces no `task_done` or proof line. It produces only a `claim` row that `fm prove` has to confirm.

- **Fail the ship gate when a fix adds a flag or env var** — CLEAN — value 3 — effort S — risk low — category: knobs
  Why: the c08 tombstones show flags get removed. The gate that would stop new ones is missing, and each knob adds a state to test.
  Done when: `fm ship` diffs the argparse and env-var surface. A new option without a `--justify` line in the task fails the gate, and a test adding a dummy flag shows the failure.

Next question: Which of Foreman's currently shipped capabilities would the user delete first if shown only its cost and its last-use date, with no description?
Next question: What is the smallest set of files that must exist for the guard to keep working when everything else in the install is broken or removed?
