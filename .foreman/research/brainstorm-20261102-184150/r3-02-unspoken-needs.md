# Brainstorm — lens: unspoken needs

- **Converge the local tree with main after every live publish** — FIX — value 4 — effort M — risk med — category: shipping
  Why: the user asked twice for "main's tree matches the local tree", and the ship-count steer says `fm genesis live` pushes `site/` commits that HEAD never has. Each `fm ship` therefore starts from a tree that already differs from main in a way the user didn't cause.
  Done when: after a scripted `fm genesis live` then `fm ship` on a scratch repo, `git diff main HEAD` is empty and `fm next` shows no "waiting" ship step.

- **Split a frozen Done-when clause into a successor task** — FEATURE — value 4 — effort S — risk low — category: task flow
  Why: T-2702 was dropped because criterion 3 bundled a user-held deletion and "can't be edited after a failing run", so the user had to drop it and refile only the M-02 check by hand. `fm task split-clause T-#### 3` would file the clause as a linked task and close the parent on the clauses that passed.
  Done when: a task with a failing frozen clause 3 splits so the parent closes on clauses 1 and 2, a new task carries clause 3 with a back-link, and the parent's frozen text is byte-identical.

- **Check the dissent score's horizon against the run's own length** — FIX — value 4 — effort S — risk low — category: measurement
  Why: the carried gap is "dissents scored against outcomes", but M-12-style outcomes use a 14-day close-survival window. A generation may finish in days, so most dissents would end as "never observed". Assumption: generations are shorter than 14 days.
  Done when: `fm outcomes --dissents` prints the share scorable inside the generation's span, and names an in-run proxy (revert or reopen within the run) for the rest.

- **State what each kill sample cannot rule out** — FEATURE — value 3 — effort S — risk low — category: experiments
  Why: the user made scripts print a "Sample" line, and M-02 had 3 modules with 2 blind attempts each. The next need is knowing how far "viable" can be trusted. The line would give the smallest failure rate the sample could have missed, and `test_moonshot_bench` would hold it.
  Done when: every `bench/moonshot/kill_*.py` docstring has a "Cannot rule out:" line with a number, and the test fails when one lacks it.

- **Test the blind moonshot rater against itself** — FEATURE — value 3 — effort S — risk low — category: measurement
  Why: M-01 to M-20 were "rated blind by the strongest model", and the moonshot floor and order depend on those ratings. Nothing shows the ratings repeat. Re-rating a shuffled copy and reporting rank correlation is cheap. Assumption: the rating call is stochastic.
  Done when: `fm genesis moonshot rate --repeat` prints Spearman ρ between two shuffled passes and flags ρ below a stated floor.

- **Seal gen-0 by content hash and name any drift in doctor** — SECURITY — value 4 — effort S — risk low — category: integrity
  Why: the standing steer says gen-0 never changes, and seeds, spec.md and cold reads all quote it. No hash check is visible in the pack. Assumption: only the cold-read charter guards it today.
  Done when: editing one byte of gen-0 turns `fm doctor` red with the hash pair, and `fm genesis sweep` refuses to write a Seed.

- **Show when the unattended drive last read the user's steers** — FIX — value 3 — effort M — risk med — category: trust
  Why: the user has about 40 standing rules and keeps adding steers mid-run ("pause every long-horizon exam run now"). After a compaction or a long unattended stretch, the user can't tell whether the drive holds the newest steer. Assumption: steers reach the drive only at session or tick start.
  Done when: `fm status` prints "steers loaded: N, newest <date>" and the count differs from `fm decide --list` only if a steer arrived after the last load.

- **Run the pack builder's privacy diff before it sends** — SECURITY — value 3 — effort M — risk low — category: privacy
  Why: this pack carries the user's verbatim words, absolute home paths and an account email, and it goes to cloud children. The idea is a zero-token scan of the assembled pack for emails, `/home/<name>` paths and token shapes, with a masked placeholder and a count on the receipt. Assumption: no such scan exists beyond credential redaction.
  Done when: a pack with a planted email and a home path is sent with both masked, and the brainstorm receipt shows "masked: 2".

- **Warn when `fm next`'s Next line would fail in the user's current state** — FIX — value 3 — effort M — risk low — category: correctness
  Why: T-2683 printed ids space-separated where `fm task unblock` takes commas, and T-2722 shipped a rule that never fired in the open-tower state. Both were printed hints that were wrong at first use. The idea is to dry-parse the hint against the live verb table and state, not just the static grammar.
  Done when: a planted wrong-state hint (valid syntax, task already closed) makes the test fail, and a correct hint passes.

- **Time the ship gate and its slowest tests per push** — PERFORMANCE — value 3 — effort S — risk low — category: speed
  Why: the user ships in batches of 3 to 9 commits, each gated by the full suite, with a hook p95 row already tracked. Assumption: suite time is untracked per push. Recording total time and the top five tests would show whether batching is a symptom of a slow gate.
  Done when: each `fm ship` receipt has "gate: Ns, slowest: …", and `fm outcomes` charts the last 20.

- **Wild: Reopen where you stopped** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: assumption: the user reads long Mission pages in pieces across sessions. Foreman would store the heading and content hash at the last read, and open the page there with a ribbon showing which later sections changed.
  Done when: reopening a Mission page after a session restart lands on the stored heading, and edited sections above it are marked.

- **Wild: Title each generation with the user's most repeated phrase** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: the user's words are short and consistent ("main's tree matches the local tree", "approach 2"). A generation labelled with its most frequent verbatim phrase is something they can search for and show others. Assumption: phrase counts come from the intake ledger.
  Done when: `fm genesis status` heads each generation with a quoted phrase that appears at least three times in the user's recorded asks.

- **Wild: Mark the tower files the user has read** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: the user steers from what they have read, but the pack shows no record of which tower files that covers. A one-key "read" would pin the content hash and show later edits as a diff, so "unread edits" becomes a count on the first screen.
  Done when: editing a marked file makes `fm genesis status` print "unread changes: 1" and the diff against the marked hash.

Next question: which of the user's repeated typed asks (the "Ship N commits" family) would disappear if a landed-work boundary fired the ship step itself, and what does the user do in the minute after each one?
Next question: where does the user check Foreman's claims by hand today (rerunning a proof, reading a diff), and which of those checks could Foreman make unnecessary?
