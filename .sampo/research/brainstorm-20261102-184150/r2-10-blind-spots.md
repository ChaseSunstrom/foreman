# Brainstorm — lens: blind spots

The eight misses fall into four classes. I took each class's question and asked it of the whole project.

1. **Key too narrow** (T-2691, T-2693): "What key does each record or line use, and what two distinct things collide under it?"
2. **Evidence away from its claim** (T-2720, T-2724): "Where does each result live relative to its claim, and was the method fixed before the run?"
3. **Rule keyed on a state that never occurs** (T-2722): "In which real modes does each state-keyed rule actually fire?"
4. **Output or paraphrase that disagrees with its source** (T-2729, T-2738): "What does this say that its source, or its consumer, does not?"

- **Report the dimensions each summary collapsed** — FEATURE — value 4 — effort S — risk low — category: legibility
  Why: T-2691 and T-2693 were lines that hid generation and agent. Any `fm outcomes`, exam, burden or lineage line that aggregates can do the same. (assumption: other aggregate lines hide dimensions too)
  Done when: a test feeds two rows differing only in one dimension to each aggregate reader, and the line either shows both or ends with `(collapsed: <dim>)`.

- **Find silent key collisions in real ledgers** — FIX — value 4 — effort M — risk low — category: integrity
  Why: both lineage misses were same-key rows that differed in another field. `fm fsck` has no data-driven scan for this, only `Mutate every dedupe key` as a synthetic test.
  Done when: `fm fsck --collisions` lists, per ledger, groups of rows sharing the identity key but differing elsewhere. It reports 0 on a clean fixture and 1 on a planted collision.

- **Snapshot `fm next` across canonical states** — FEATURE — value 5 — effort M — risk low — category: state coverage
  Why: T-2722 never fired because the tower's stage is `genesis`, never `idle`. Rules are tested in the states their authors imagined.
  Done when: a golden file holds `fm next` and `fm status` output for at least 10 fixture states (tower open, queue closed, only blocked items, lane, grant held, no `claude` on PATH). A rule that changes any of them fails until the golden is updated.

- **Detect dead-end states** — FIX — value 4 — effort S — risk low — category: workflow
  Why: the ship step was invisible in a stage that had no outgoing line. The same may hold for other stages.
  Done when: over the fixture states, each output contains a runnable `Next:` or a line `nothing to do: <reason>`. A planted state with neither fails the test.

- **Check progress on Next chains** — FIX — value 3 — effort M — risk med — category: loops
  Why: T-2738 printed a command the parser refuses. Parsing is checked elsewhere, but not whether running the command moves the state on.
  Done when: in a scratch home, running the printed `Next:` command and then `fm next` again yields a different state or a different command within 3 hops, never the same pair twice.

- **Embed gen-0 text into seeds by quotation** — CLEAN — value 3 — effort S — risk low — category: docs drift
  Why: T-2729's seed paraphrased gen-0 §3 on #13 and contradicted it. A quote with a hash cannot drift quietly.
  Done when: a seed section on a gen-0 rule is an include with the source hash. `fm genesis check` fails when the hash stops matching or when a paraphrase of a MUST/NEVER carries no include.

- **Bind each result file to its script's hash** — FEATURE — value 3 — effort S — risk low — category: evidence
  Why: T-2720 and T-2724 were found only after the fact. A result beside a script says nothing about whether it came from this script version or a prior run.
  Done when: each `bench/moonshot/kill_*.py` result carries the script hash and run date, and the tests fail when the script is newer than its result.

- **Run a cold complaint pass before closing a gauge** — FEATURE — value 5 — effort M — risk med — category: review
  Why: every miss in the pack was a complaint about a newly printed line, made after it shipped. A tool-less child that sees only the printed output on the real state, as the user would, can raise them first.
  Done when: `fm task finish` on a task that adds printed output stores a "first 3 complaints" file. Replaying T-2691's pre-fix output through the child names the missing generation.

- **Commit a golden fixture of the real ledger's shape** — CLEAN — value 3 — effort M — risk low — category: tests
  Why: the real pile (44 blocked) showed that the asks/depends_on grouping found nothing, and toy fixtures did not. (assumption: fixtures are mostly synthetic)
  Done when: a redacted, size-capped ledger sample is checked in. The readers run against it in tests and have to find at least one instance of each class they claim to detect.

- **Wild: Show what the old key hid** — FEATURE — value 3 — effort M — risk low — category: regression
  Why: a keying fix has no visible effect on the data it changes. (wild)
  Done when: when a reader's key changes, a one-off report diffs its output on the real ledgers before and after, and the commit message cites the differing row count.

- **Wild: Mutate printed lists** — FIX — value 2 — effort S — risk low — category: tests
  Why: T-2738 was a comma-versus-space error in one printed command. (wild)
  Done when: a test swaps the separator in every printed id list, feeds it back to its parser, and reports each refusal. The T-2683 bug is caught as a regression.

- **Wild: Keep a "pairs never entered" shelf** — FEATURE — value 3 — effort L — risk med — category: coverage
  Why: the misses show that rules and states meet in combinations nobody tried. (wild)
  Done when: a static scan lists (rule, mode) pairs that no test enters, ranked by the user's recent verb use, and the top 5 appear in `fm doctor --verbose`.

Next question: of the verbs that print ids, commands or counts, which ones have a consumer (a parser, a skill, a hook) that has never read their output in a test?

Next question: when the user types a one-line correction (keying, location, ordering), what other places share that decision, and does anything list them?
