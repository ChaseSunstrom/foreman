# Brainstorm — lens: deepen: intake

- **Capture the goal verbatim, then restate it as a testable "Finished means" paragraph** — FEATURE — value 5 — effort M — risk low — category: intake
  Why: T-0790 (verbatim capture) is deferred, and the user's wrapped Task paragraphs were read as one line (T-2213). Their own words are the source of truth. Assumption: a goal today is stored only in summarized form.
  Done when: `fm goal open "<text>"` stores the raw text unchanged beside a restated acceptance paragraph, and a test shows a later compaction still returns the raw text byte for byte.

- **Run the interview as a ladder: infer from repo, then ask one question with a default and timer, then proceed on the default** — FEATURE — value 5 — effort M — risk med — category: intake
  Why: this merges "ask one friendly question", "interview with defaults and a timer" and "interview the vague goal". Most answers are in the map, the README and the open work already. Assumption: the user would rather be asked once than five times.
  Done when: for a vague goal on a fixture repo, at most one question is asked, an unanswered one lapses to its default after the timer, and the default taken is recorded in the plan.

- **Record every assumption made at intake as a challengeable row with a one-line veto** — FEATURE — value 5 — effort S — risk low — category: intake
  Why: the open question "which parts of a plan can the user veto in one line" has no answer yet, and steers are already standing rules in this project. Assumption: assumptions are currently implicit.
  Done when: `fm goal veto A-3` drops that assumption, marks dependent plan rows stale, and the one-line receipt names the rows it touched.

- **Tell a changed mind from a missing row at intake time by tagging each later reopen with its cause** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: open question on reopens caused by the user changing their mind versus a missing row. Intake is where the original wording sits, so a reopen can be compared against it. Assumption: the ledger records reopens without a cause.
  Done when: a reopen carries the cause "missed" or "changed mind", chosen by comparing the new request to the stored verbatim goal, and the miss rate counts only "missed".

- **Seed intake from the user's past goals so a vague line is read the way this user means it** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: the history shows a consistent pattern: steers become standing rules, "test-first", "through the cold read", "shipped to main". Assumption: closed-task history is searchable by `fm`.
  Done when: opening a vague goal prefills defaults from the last N similar closed goals and cites each source task id, and the user can turn the prefill off.

- **Detect a goal that is really two goals and offer to split it before planning** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: open question on what Stop does with two open goals, and Mission 3 packed 8 briefs under one paragraph (T-2213). Splitting at intake avoids shared ledgers. Assumption: goals with "and", lists or several verbs are common.
  Done when: a goal with two independent outcomes yields a proposed split with two ids, and accepting it opens two goals, each with its own ledger.

- **Size the goal against the baton limit at intake and warn before the plan outgrows a fresh session** — PERFORMANCE — value 3 — effort M — risk low — category: intake
  Why: open question on the largest baton a fresh session can absorb. Intake knows the row count first. Assumption: baton size can be measured in tokens per model tier.
  Done when: intake prints the estimated baton size per tier and, over a threshold, proposes grouping rows into legs.

- **Wild: Turn the vague goal into a dry-run "finished demo" the user approves before any planning** — FEATURE — value 4 — effort L — risk med — category: intake
  Why: wild. Users answer concrete pictures better than abstract questions. Assumption: a mock of the finished state (a README paragraph plus a sample command transcript) is cheap to generate.
  Done when: `fm goal open --demo` writes a mock finished transcript, and approving it copies its lines into the acceptance checks.

- **Wild: Let the user answer the interview by voice or by pasting a screenshot, whatever is closest** — FEATURE — value 3 — effort M — risk med — category: intake
  Why: wild. The user spreads asks across surfaces (CLI, web UI, mail monitor). Assumption: the pasted artifacts are handled as untrusted data.
  Done when: a pasted image or transcript is stored as an attachment on the goal, and the plan cites it in at least one row's rationale.

- **Wild: Hold a "pre-mortem" at intake where a cold Haiku reader says how this goal most likely ends in a false done** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: wild. The cold-read pattern already exists in Genesis (`fm genesis put`), and the missed-asks list (T-2202 to T-2231) is mostly cases of finishing in a wrong state. Assumption: reusing the cold read for goals is cheap.
  Done when: opening a goal runs a cold read that names up to 3 likely false-done modes, and each becomes a check on the plan.

- **Score intake quality from outcomes, so the interview learns when it should ask less** — FEATURE — value 3 — effort M — risk low — category: intake
  Why: reopens are already counted, and the open question on how long the window must run says data is scarce. Assumption: per-question outcomes need pooling across projects.
  Done when: `fm goal stats` shows, per question type, how often its answer changed the plan, and a question that never did stops being asked by default.

- **Make the restated goal a standing contract that Stop checks against, not a note** — FEATURE — value 5 — effort M — risk med — category: intake
  Why: the open question on which file settles "done" across legs, and the user's steer that every rule gets an automatic check. Assumption: the contract lives in one sealed file as with the gen-0 charter.
  Done when: the goal contract is sha256-sealed at intake, and a changed contract without a ledger event fails `fm doctor`.

Next question: What does the user do in the first ten seconds after typing a vague goal, and can intake use that wait to run its free inference work in parallel?
Next question: Which intake answers were later contradicted by the user's own steers, and what would have made the first answer right?
