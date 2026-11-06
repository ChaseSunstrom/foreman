# Brainstorm — lens: blind spots

- **Stamp every pack section with its age** — FIX — value 3 — effort S — risk low — category: context
  Why: the pack's own map line says "as of an older HEAD", so a brainstormer can't tell stale facts from current ones. The question missed is "which inputs to a decider are older than the decision?"
  Done when: a brainstorm pack prints the age in commits or days beside each section, and a section older than a threshold is marked STALE.

- **Verify every quoted line in a cold-read FAIL exists** — FIX — value 4 — effort S — risk low — category: cold reads
  Why: the steer says a FAIL counts only if it quotes the offending line. Nothing checks that the quote is really in the file, so a fabricated quote could block a filing or pass as grounded.
  Done when: a test feeds a FAIL whose quote isn't a substring of the input and the FAIL is rejected and logged as "ungrounded".

- **Check conservation laws across the ledgers** — FEATURE — value 4 — effort M — risk low — category: ledger integrity
  Why: earlier ideas cover references (`fm fsck`) and missing record classes, but not totals. Bets placed should equal settled + open + voided, and tasks opened should equal closed + open + dropped. A dropped record class leaves every reader error-free and wrong, so only a balance catches it.
  Done when: `fm doctor` fails on a fixture ledger with one settled bet removed, and names the identity that broke.

- **Probe that every pinned model ID still answers** — FIX — value 4 — effort S — risk low — category: unattended
  Why: cold reads, exams and the night tick pin Haiku/Sonnet. A retired or renamed ID would make cold reads abstain quietly, which is the same class as the T-2566 silent abstention. Assumption: IDs are pinned in config.
  Done when: `fm doctor` makes a one-token call per pinned ID and a fixture with a bogus ID shows WARN with the ID and the fallback it would use.

- **Tell a sleeping machine from a dead timer** — FEATURE — value 3 — effort M — risk low — category: unattended
  Why: T-2542 reads the last trigger. On a laptop-style Arch host, a stale trigger may just mean suspend, or missing `loginctl enable-linger`. Without the cause, the WARN gets ignored as noise.
  Done when: a stale-trigger WARN includes "machine was suspended X–Y" from the journal or "linger off", and a fixture covers both.

- **Count the commands the guard couldn't parse** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: the guard decides on command text. An unparseable shape (nested substitutions, heredocs, odd quoting) is an abstention that looks like an allow. This is the silent-abstention question asked of the guard itself.
  Done when: the guard logs "unparsed" with a hash of the shape, `fm doctor` shows the count over 30 days, and a test with an obfuscated command triggers the log.

- **Watch for regret after every subtraction** — FEATURE — value 3 — effort M — risk low — category: lean
  Why: T-2534/35/36 build subtraction by evidence, but nothing measures whether a removal was wrong. A later user ask that matches a removed feature is the evidence.
  Done when: after a removal task closes, a new `fm capture` that matches its clauses (the T-2546 matcher) is tagged "possible regret" and listed in the next lean report.

- **Dedupe the idea ledger and count re-proposals** — CLEAN — value 3 — effort S — risk low — category: brainstorm
  Why: this pack's "Ideas so far" restates the same idea 4–5 times, for example "unproven" receipt states and the restore drill. That wastes pack space, and the repeats are a convergence signal nobody uses.
  Done when: the pack lists clusters with a re-proposal count, ≤1 line per cluster, and the highest-count cluster with no task is flagged first.

- **Audit Foreman state kept on volatile paths** — FIX — value 3 — effort S — risk med — category: durability
  Why: the brainstorm children run under `/run/user/1000`, which is tmpfs and is cleared at logout or reboot. Assumption: some scratch, sockets or caches also live there and are read as durable.
  Done when: `fm doctor` lists every Foreman-written path on tmpfs, marks which are read as durable, and a fixture with a ledger on tmpfs warns.

- **Measure how often injected lines get used** — PERFORMANCE — value 4 — effort M — risk low — category: lean
  Why: the lean work counts injected chars but not whether the model ever acts on a line. Subtraction by evidence needs a use rate, not just a size.
  Done when: for the last 50 sessions, each recurring hook-note and steer line has a "referenced in later turns" rate, and lines at 0% are listed as removal candidates.

- **Bisect an abstain-rate jump to the commit behind it** — FEATURE — value 3 — effort M — risk low — category: deciders
  Why: "dead deciders by abstain rate" is a static snapshot. A step change right after a commit is the real signal (for example the T-2334 and T-2566 class).
  Done when: a fixture decider whose abstain rate jumps from 5% to 90% at a known commit is reported with that commit.

- **Wild: Plant a honeypot in the inbox** — FEATURE — value 3 — effort S — risk med — category: unattended
  Why: wild. Once a night the tower files an obviously wrong Foreman-authored item, such as a task to delete the ledger or a pasted fake key. If the drive picks it up or no reader flags it, a gate has a hole. Assumption: items are filed under a safe prefix and never executed.
  Done when: the honeypot is filed, and it is either refused with a named gate or reported as "swallowed" in `fm doctor`.

- **Wild: Ask the user the question the user model is least sure of** — FEATURE — value 3 — effort M — risk low — category: user model
  Why: wild. The sealed-prediction idea only scores hits. Disagreement between two child predictions marks what the model truly can't guess, and one weekly `fm ask` about exactly that makes the user model learn fastest.
  Done when: a weekly ask is chosen as the prediction pair with the most disagreement, and the answer is stored as a labelled steer.

- **Wild: Print an anti-changelog each morning** — FEATURE — value 4 — effort M — risk low — category: reporting
  Why: wild. The night tick says what it couldn't watch (T-2607), but nothing says what Foreman considered and chose not to do: filed-but-held items (round-first), pace drops, abstaining deciders and skipped timers, each with a reason.
  Done when: the morning note has a "Not done, and why" section, and a fixture night with one held item and one skipped decider shows both reasons.

Next question: which of Foreman's decisions to do nothing (hold, skip, abstain, allow-by-default) leave no record, and which user-visible outcome would reveal each?
Next question: which inputs to Foreman's own models are stale, truncated or self-authored by the time the model reads them, and does the model know?
