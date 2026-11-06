# Brainstorm — lens: self-modification: proof kinds that learn which checks caught real misses and which were theatre, retiring the theatre, measured and reversible

- **Blame-trace every fix to the proofs that blessed the bug** — FEATURE — value 5 — effort M — risk med — category: ground truth
  Why: reopen counts are sparse and self-reported, so the catch ledger starves. assumption: a FIX commit's changed lines can be `git blame`d back to a closed task id.
  Done when: on a fixture repo with a planted bug introduced by T-A and fixed by T-B, `fm proof misses` lists T-A's evidence kinds as "missed by" with the blame lines quoted.

- **Breed a candidate proof kind from each uncaught miss** — FEATURE — value 5 — effort L — risk med — category: self-extension
  Why: the lens covers retiring theatre, but nothing grows a kind when a miss slips past all of them. wild. The candidate is a generated check script that must pass two tests before entering shadow: it fails on the buggy tree and stays quiet on 20 sampled past green closes.
  Done when: given a recorded miss, `fm proof breed T-NNNN` writes a check to `.fm/proof/candidates/`. It reports "caught the miss, fired on k of 20 greens" and refuses to promote it if k > 2.

- **Pre-register each kind's kill criterion at birth** — FEATURE — value 4 — effort S — risk low — category: simplicity
  Why: pre-registering the proof is already an idea, but the kind's own death condition is left to a later judgement call. A kind with no stated kill rule is exactly how theatre survives.
  Done when: `fm proof kinds add` refuses a kind without `retire_if:` and `resurrect_if:` fields, and `fm doctor` names any existing kind that lacks them.

- **Cross-validate every retirement on tasks it didn't learn from** — SECURITY — value 4 — effort M — risk low — category: self-modification safety
  Why: a retirer that scores itself on the same ledger it trained on will overfit to a quiet month. assumption: the ledger has enough closed tasks to split.
  Done when: a retirement decision is recorded only if replaying the held-out half of the ledger without that kind loses no more catches than the user-set floor, and the receipt shows both halves' numbers.

- **Pick the cheapest proof set that would have caught every past miss** — PERFORMANCE — value 4 — effort M — risk low — category: proof economics
  Why: per-kind scores treat kinds as independent, but two kinds often catch the same misses. A set-cover over the ledger shows which kind is redundant even if it catches things.
  Done when: `fm proof diet --cover` prints a minimal kind set with total seconds, and a fixture where kind B duplicates kind A drops B.

- **Keep a silent post-retirement sample so retired kinds keep producing data** — FEATURE — value 4 — effort S — risk low — category: reversibility
  Why: shadow mode runs before retirement, but after retirement the ledger goes dark and a kind can't earn its way back. A retired kind still runs unseen on 1 in N tasks, and N shrinks when the miss rate rises.
  Done when: a retired kind's ledger gains rows at about the configured rate on a simulated 200-task run, and a burst of planted misses lowers N and re-enables the kind.

- **Treat the user's own follow-up edits as soft misses** — FEATURE — value 4 — effort M — risk med — category: ground truth
  Why: the user rarely reopens; they just edit. assumption: a user-authored commit touching a closed task's files within 48h usually means the task's "done" was wrong or incomplete.
  Done when: a fixture user commit within the window logs a soft miss against that task's proof kinds, weighted below hard reopens, and `fm proof ledger` shows both counts separately.

- **Reset trust when the model or host version changes** — FIX — value 3 — effort S — risk low — category: drift
  Why: catch rates depend on the builder. The router already tracks per-model outcomes, but the proof ledger doesn't, so a retirement learned on one model carries over to another. assumption: the model id is recorded per closed task.
  Done when: after a recorded model switch, retired kinds enter probation, running again for K tasks, and the ledger reports rates keyed by model.

- **Make the proof ledger tamper-evident and unwritable by the builder** — SECURITY — value 4 — effort M — risk low — category: integrity
  Why: a model that wants "done" faster profits from making a kind look like theatre. Rows should be hash-chained by a process the builder session can't write to.
  Done when: editing or deleting a ledger row from a builder-session path is denied by the guard, and `fm doctor` fails on a broken chain.

- **Share only a redacted catch-rate table across the user's own repos** — FEATURE — value 3 — effort M — risk low — category: local-first priors
  Why: a new repo starts with no ledger and runs every kind. assumption: the user works in several repos on one machine. Only kind, stack card and counts travel, never task text, and the local ledger overrides the prior after 10 tasks.
  Done when: a fresh fixture repo's first proof diet reflects the imported table, and `fm proof export` output contains no task titles or paths.

- **Hold a weekly retirement tribunal that ends in one forwardable paragraph** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: self-modification the user can't see is self-modification they won't trust. The paragraph names what was retired, promoted or put on probation, with the number behind each and the one command to reverse it.
  Done when: `fm proof report --week` prints at most 6 lines, each ending in a runnable `fm proof revert KIND` command that restores the previous policy file.

- **Build a graveyard page of retired kinds, each with a tombstone** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. Each tombstone shows cost saved, catches over its lifetime, the reason retired and a resurrect button, published on the Genesis site beside the exam scores.
  Done when: `fm genesis live` publishes `site/genesis/graveyard.json` with one entry per retired kind, and the page renders an empty state when there are none.

- **Run a ledger-poisoning lane that tries to make good kinds look useless** — SECURITY — value 3 — effort M — risk med — category: adversarial
  Why: wild. A saboteur lane writes tasks designed to dodge a kind and checks whether the retirer takes the bait. This tests the learner, not the code under test.
  Done when: on a synthetic ledger seeded with 30 dodging tasks, the retirer still keeps the kind or flags the cluster as suspicious, and the run is stored as an exam scenario.

- **Auction a fixed proof-seconds budget between kinds by catch per second** — PERFORMANCE — value 3 — effort L — risk med — category: proof economics
  Why: wild. Each task gets a user-set seconds budget for proof, and kinds win slots by historical catches per second plus an exploration bonus so untested kinds still get tried.
  Done when: with a 60 s budget and three kinds with known rates, the chosen set matches the expected order, and an unseen kind gets at least one slot in 10 tasks.

Next question: When a retired or promoted proof kind later turns out to have been the right call after all, which signal tells Foreman that was a mistake rather than bad luck?
Next question: Which of Foreman's current proof kinds have never once been asked to fail, so their catch rate is zero because nothing ever tested them?
