# Brainstorm — lens: approaches

- **Probe unbuilt claims with the parser's own did-you-mean** — FEATURE — value 4 — effort S — risk low — category: grounding
  Why: T-2735 made an unknown `list`/`ls` action point at the parser's listing action, so the parser already knows its nearest neighbours. Reusing that beats writing more grep canaries. The cost is that it only sees verbs and flags, not docs or skills.
  Done when: for a brief claiming "no verb does X", a planted existing verb with a different name is surfaced as the nearest match by `fm`'s parser, and a test fails without the probe.

- **Make the Exam's live reading a named `fm doctor` check** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: free-text live commands can be unsafe, and a cold process may be unable to re-run them. The doctor registry is already read-only and re-runnable. The trade-off is a constrained menu, with new readings added as doctor checks.
  Done when: filing a brief whose `live:` names a nonexistent doctor check is refused, and one naming a real check records its value at filing.

- **Pick the outcome measure from the `fm outcomes` classes** — FEATURE — value 4 — effort S — risk low — category: exam
  Why: the carried gap is "outcome measure", and Foreman already scores close survival, so a menu avoids vacuous inventions. The trade-off is that exotic outcomes need a new class first.
  Done when: a brief's `outcome:` must resolve to an existing outcomes class or a filed new one, and a vacuous string is rejected by test.

- **Write each Exam as a tests/ file with a `live` marker** — FEATURE — value 4 — effort M — risk med — category: exam
  Why: red-first tests are already Foreman's discipline, and a pytest file can be re-run cold by CI. A live-marked test that can't reach state reports "unmeasured", not pass. The trade-off is heavier than a one-line command.
  Done when: a Mission brief links `tests/exam/<brief>.py`, it fails on the parent commit, and with no state dir it reports unmeasured.

- **Write dissents as a runnable predicate** — FEATURE — value 4 — effort M — risk med — category: dissent
  Why: scoring dissents against outcomes needs a settle rule, and prose can't be settled at zero token cost. Forcing "if X then command Y reads Z by date D" makes the score mechanical. The trade-off is that a dissent about taste can't be written this way and must stay unscored.
  Done when: a dissent is filed as `{claim, command, expect, by}`, and `fm outcomes` settles one planted dissent hit and one miss with no model call.

- **Sweep the request's nouns across the repo and history** — FEATURE — value 3 — effort S — risk low — category: omission
  Why: this is the cheapest reuse of existing tools, with no children. List files, tasks and drops that mention each request noun, and flag any not covered by a brief or n/a. Its weakness is that synonyms slip past it.
  Done when: the Mission page prints "noun → files/tasks → covered by", and a noun with hits but no brief is listed under left out.

- **Pre-register the Mission report as a skeleton with blanks** — FEATURE — value 3 — effort S — risk low — category: report
  Why: doing less than a new ledger. A skeleton generated from the request's nouns forces each blank to be filled or marked n/a, and unfilled blanks are the left-out list.
  Done when: closing a Mission with an unfilled blank is refused, and with all blanks filled the left-out section is auto-generated.

- **Carry the left-out list as a git note on the Mission commit** — FEATURE — value 2 — effort S — risk low — category: provenance
  Why: it travels with `fm ship` and survives the tower files being rewritten. It is an alternative to a new ledger file. Notes are easy to lose on rebase.
  Done when: after ship, `git notes show <mission-commit>` lists the left-out cells, and a test covers a rebase.

- **Score dissents with the existing 14-day close-survival signal only** — FEATURE — value 3 — effort S — risk low — category: dissent
  Why: the do-less option. It adds no new outcome machinery and attributes a reverted or refixed close within 14 days to the overruled dissent when the dissent named a touched file. It is coarse, and silent successes score nothing.
  Done when: `fm outcomes` prints per-dissent hit, miss and unobserved counts from existing ledgers, and a planted refix registers a hit.

- **Run the live reading as a snapshot pair at filing and close** — FEATURE — value 3 — effort M — risk med — category: exam
  Why: it is the alternative to a single reading, and it directly proves the Exam notices a change. When a snapshot can't be taken, the Exam says "unmeasured" and carries forward.
  Done when: a brief that closes with identical before/after readings is flagged "no movement", and an offline snapshot is recorded as unmeasured.

- **Wild: Run the Mission request through a deliberately dumb child and diff** — FEATURE — value 3 — effort M — risk low — category: omission
  Why: assumption: a tool-less Haiku child that answers "what would you build" with no pack makes a baseline. Whatever the Mission covers that the baseline also covers is generic, and what only the baseline mentions may be an obvious thing left out.
  Done when: the Mission page lists "obvious ideas from the dumb child not in any brief" and a planted obvious item shows up.

- **Wild: Hold the exhaustiveness claim hostage to a recall quiz** — FEATURE — value 3 — effort M — risk med — category: exam
  Why: before a Mission may say "covered", a cold child is shown only the final brief set and asked to name ten things the request could mean. Any that no brief addresses count as left out, and the recall score goes on the page.
  Done when: the Mission file carries a recall figure, and a planted brief-set hole lowers it.

- **Wild: Treat each canary hit as a vote on the idea's novelty** — FEATURE — value 2 — effort M — risk low — category: grounding
  Why: instead of binary "already built", the nearest three existing things (verb, task, drop) are scored by similarity, and a high-similarity neighbour demotes the idea to "extend X". This differs from showing the non-match: it changes the verdict.
  Done when: a brief with a near-duplicate neighbour is filed as an extension of that neighbour's id.

Next question: Of the Exam forms (doctor check, tests file, outcome class, or free command), which could a cold process re-run a month later without the filing session's state?
Next question: When the user opens a Mission page, what is the first line they read, and is it the left-out list or the brief set?
