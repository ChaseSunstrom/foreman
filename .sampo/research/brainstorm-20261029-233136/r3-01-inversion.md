# Brainstorm — lens: inversion

- **Authenticate the auto-start trigger** — SECURITY — value 4 — effort S — risk low — category: auto-start
  Why: the queue running dry starts the tower, and the queue can be emptied or filled by text the user didn't write (issue titles, imported tasks, a repo's TODO file). Assumption: the dry-queue check reads task state without recording where each item came from.
  Done when: a fixture where only an untrusted-origin task was closed, or a hostile TODO file was added, does not start the tower, and a locally authored empty queue still proposes it.

- **Freeze grid axes per generation so the tower must end** — FEATURE — value 4 — effort S — risk low — category: termination
  Why: "no empty cells" is unbounded if each pass can add axes. Assumption: the sweep may add rows and columns while it runs.
  Done when: axes are written at generation start, adding one needs a logged expansion with a cap of 2 per generation, and a test with an always-expanding stub writer still halts.

- **Meter spend from outside the tower** — SECURITY — value 4 — effort M — risk med — category: cost
  Why: the budget caps in earlier ideas read a ledger the tower writes, and a rewrite that touches its own accounting passes its own cap. Assumption: the cost ledger is a tower file.
  Done when: the fuse reads usage from session transcripts or the API log, and a fixture that zeroes the tower's own ledger still trips the fuse.

- **Cap child fan-out and recursion depth** — SECURITY — value 4 — effort S — risk low — category: runaway
  Why: Genesis spawns brainstormers, critics, lanes and exam children, so a loop in the orchestrator is a fork bomb that dollars alone stop too late. Assumption: no live-process or depth counter exists.
  Done when: a stub orchestrator that respawns itself stops at the depth and concurrency caps and files an incident note.

- **Run exam code with the network off and log egress** — SECURITY — value 5 — effort M — risk med — category: sandbox
  Why: the exam runs generated and stranger-repo code, and a hostile test or install script could reach the network. Assumption: exam runs inherit the host's network.
  Done when: a fixture scenario that curls an external host fails offline and appears in the egress log, and the real exam suite still passes.

- **Keep towers per-user and uncommitted; promote to a team only by PR** — SECURITY — value 3 — effort S — risk low — category: team repos
  Why: in a shared repo, one developer's self-written MUSTs could bind every teammate's agents. The pack's rule that tower files live only in `fm genesis` storage points the same way.
  Done when: `git status` shows no tower paths after a run, and `fm genesis share` produces a diff for review rather than writing into the repo.

- **Reconcile a self-written gen-0 with the user's standing rules, with the user winning** — FIX — value 4 — effort S — risk low — category: precedence
  Why: gen-0 is written from the project and history but must not contradict the user's global CLAUDE.md or the protected routing rules. Assumption: nothing compares them.
  Done when: a gen-0 draft that contradicts a fixture user rule is rejected with the conflicting pair shown, and the rule text is unchanged.

- **Trip a breaker when the user reverts Genesis work** — SECURITY — value 4 — effort S — risk low — category: outside signals
  Why: the standing steer is weakness-finding by outside signals only, and a user reverting commits is the plainest one. Assumption: revert and reset events aren't read today.
  Done when: reverting 2 Genesis-authored commits pauses auto-start, writes a "what did you dislike" note to not-yet, and the next generation starts only after a yes.

- **Check planted-gap fixes generalize** — FEATURE — value 4 — effort M — risk med — category: overfit
  Why: the Mission 2 exam closes "planted gaps", and a tower can learn the planter's tells and patch the marker instead of the defect. Assumption: one planting per gap.
  Done when: each gap has a second, differently planted variant that stays hidden, and a fix that closes the first but not the variant counts as open.

- **Quota and collect exam sandboxes** — FIX — value 3 — effort S — risk low — category: resources
  Why: this machine's working directory sits under `/run/user/1000`, which is tmpfs, and 6 languages × 11 kinds × arms of workdirs can fill it. Assumption: there is no cleanup.
  Done when: a 200-scenario run stays under a set byte cap, old workdirs are removed on success, and failed ones are kept for N days.

- **Add `fm genesis forget` for a project** — SECURITY — value 3 — effort M — risk med — category: privacy
  Why: carry-over, the site export and published history all keep what a project taught the tower. Assumption: there is no per-project erase.
  Done when: after `forget`, a grep for the project's identifiers finds nothing in defaults, templates or `site/genesis`, and a re-export is clean.

- **Wild: dead-hand switch** — FEATURE — value 3 — effort S — risk low — category: unattended
  Why: wild; an unattended tower on a user who left for two weeks is the worst case for runaway spend. Assumption: no check reads user presence.
  Done when: with no interactive session for N days, auto-start and spending stop and one line says why, and the next session resumes it with a yes.

- **Wild: pay a rollback bond each generation** — FEATURE — value 4 — effort M — risk med — category: reversibility
  Why: wild; a rewind command is only worth anything if the restore actually works. Assumption: restores are untested.
  Done when: a generation can't close until a fresh scratch copy restored to its start point passes the repo's gates.

- **Wild: mirror-universe selector test** — FIX — value 4 — effort S — risk low — category: selection
  Why: wild; run selection on a fixture with a deliberately worse rewrite and the exam grade inverted, to prove the selector and exam can be wrong in the direction that matters.
  Done when: the worse rewrite loses under honest grading, wins only when grades are flipped, and the test fails if the selector ever favors it.

Next question: What does Genesis do when an outside, honest signal (user revert, 30-day survival) says a winning rewrite was bad? Does that reopen the lineage entry, or only add a not-yet item?
Next question: Which of Genesis's own writes (tower files, site export, carry-over defaults, queue items) can a hostile project cause, and which of those does a later session trust without re-checking?
