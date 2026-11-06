# Brainstorm — lens: self-modification

- **Lock the judge before any self-change** — SECURITY — value 5 — effort M — risk low — category: guard
  Why: assumption: a self-modifying Genesis can drift toward easier exams. Pack: exam keys, held-out third and the selection rule are all files Genesis could touch.
  Done when: a test where a candidate self-change edits an exam key, the held-out split or the selection rule in the same generation is refused, and the refusal names the locked file.

- **Keep a self-change ledger with a revert command** — FEATURE — value 5 — effort M — risk low — category: lineage
  Why: lineage.md covers rewrites of tower docs but not Genesis's own templates, lenses and rules. Without a ledger, a self-change has no parent, no measured delta and no undo.
  Done when: `fm genesis self log` lists each self-change with parent, exam delta, cost, and `fm genesis self revert ID` restores the prior file byte-for-byte (tested).

- **Make templates win on held-out projects before they become defaults** — FEATURE — value 5 — effort M — risk med — category: carry-over
  Why: the request says to carry over winning Seed and mission templates. Nothing yet shows a template beat its parent on projects it was not tuned on.
  Done when: a template promoted to default has recorded wins on at least 3 generated projects it never saw, and a tied or losing template stays a candidate.

- **Pin the user's MUSTs and NEVERs as a hashed charter** — SECURITY — value 5 — effort M — risk low — category: drift
  Why: steers such as "no idea killed for ambition" and "tower files only in genesis storage" are standing rules. Self-changes could quietly erode them.
  Done when: every self-change diff runs through `fm second` against the charter, and a seeded change that contradicts a NEVER is blocked while a neutral change passes.

- **Gate exam edits with the oracle/empty/finders canary** — SECURITY — value 4 — effort S — risk low — category: exam integrity
  Why: fm exam already has oracle, empty and finders arms. They can show whether a modified exam still tells good from bad.
  Done when: an exam change is rejected unless oracle scores 100%, empty scores 0% and finders land strictly between them.

- **Measure the train-versus-holdout gap per self-change** — FEATURE — value 4 — effort M — risk med — category: overfitting
  Why: inversion lens names overfitting the held-out third. A self-change that gains on seen scenarios and nothing on hidden ones is overfit.
  Done when: each ledger entry records train delta and holdout delta, and a change with a gap above a set threshold is flagged and not promoted.

- **Retire and revive lenses by payoff, with an exploration floor** — FEATURE — value 3 — effort M — risk low — category: lenses
  Why: T-0829 (lens scaling from lens_rates) sits deferred. Genesis could own that rule, with a floor so a dry lens still runs occasionally.
  Done when: a lens that produced no accepted ideas over N rounds drops to a low run rate but never to zero, and a test shows it can come back.

- **Cap self-change to one class per generation, with a dollar budget** — SECURITY — value 4 — effort S — risk low — category: budget
  Why: assumption: when templates, lenses, exam and selection change together, a gain can't be attributed to any of them.
  Done when: a generation that proposes two self-change classes runs only the first, queues the rest, and stops at its stated spend.

- **Trim winning templates sentence by sentence** — PERFORMANCE — value 3 — effort M — risk low — category: simplicity
  Why: templates only grow unless something prunes them. Deleting a sentence that ties on the exam is a free win in cost and clarity.
  Done when: after a template win, a pass tries removing each sentence and keeps every removal that ties or beats the exam, with the shorter text in lineage.

- **Replay alternative selection rules on past towers** (wild) — FEATURE — value 4 — effort L — risk med — category: meta-selection
  Why: assumption: "closes more scenarios than its parent" may be a weak rule. Old towers plus fm outcomes' 30-day survival offer an outside signal to compare rules against.
  Done when: `fm genesis self replay RULE` reports which old rewrites the new rule would have kept or dropped, and how that matches their 30-day survival.

- **Let a tool-less red-team child attack the current Genesis** (wild) — FEATURE — value 4 — effort M — risk med — category: adversary
  Why: the pack's rule is that exam authors are tool-less children. The same idea can aim at Genesis itself, writing scenarios where its self-written gen-0 would miss a MUST.
  Done when: a red-team run produces at least 3 new scenarios the current Genesis fails, each added to the exam with a hidden key.

- **Keep a hall of fame of pinned Genesis vintages** (wild) — FEATURE — value 3 — effort L — risk med — category: regression
  Why: assumption: self-improvement can silently regress an old strength. A standing zoo of generated projects, run against every earlier vintage, would catch it.
  Done when: a new Genesis version is promoted only if it matches or beats every pinned vintage on the zoo, and a seeded regression blocks promotion.

- **Dream in idle time on a scratch copy** (wild) — FEATURE — value 3 — effort L — risk high — category: overnight
  Why: assumption: the user would like to wake to a measured proposal. Genesis already starts itself when the queue runs dry.
  Done when: an idle run mutates a copy of Genesis, measures it, and leaves only a candidate diff with its delta and cost, and the live files are byte-identical afterward.

- **Write a plain-English reason for every self-change** — CLEAN — value 3 — effort S — risk low — category: archaeology
  Why: tower archaeology needs the files alone to say why a rewrite lost. The user asked for per-generation decisions readable on the page.
  Done when: each ledger entry has a "why changed, what was tried, why it won or lost" block, and `fm genesis export` shows it on the generation's page.

Next question: Which self-changes should need the user's yes versus run unattended, and where is that line written so Genesis cannot move it?
Next question: How do we tell a template that truly helps from one that just matches the generated exam's quirks, when both exams come from the same authors?
