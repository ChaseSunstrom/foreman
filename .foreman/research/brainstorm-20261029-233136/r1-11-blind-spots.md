# Brainstorm — lens: blind spots

## Blind-spot reading of the pack

The misses fall into four classes. For each, the question a brainstorm should have asked:
- **T-2080, T-2087, T-2088, T-2090 (tower page, styling, auto-publish):** "Where will the user look to judge this, and who keeps it true, consistent and safe while they're away?"
- **T-2073 (surface lag):** "Which things drift out of date silently when the code moves?"
- **T-2076 (learning from misses):** "How does the system find out it was wrong without being told?"
- **T-2077, T-2079 (tower run, exam):** "What proves the result to someone who didn't watch it?"

Below, those questions are asked of Genesis as a whole.

- **Scan every auto-publish for secrets and private content** — SECURITY — value 5 — effort M — risk low — category: publish safety
  Why: T-2090 pushes `site/genesis` to main on every tower change under a standing grant, and the tower holds gen-0 verbatim plus user corrections. Assumption: the repo or site can be public.
  Done when: a planted fake API key or `/home/<user>` path in a tower doc blocks the export, names the file and line, and leaves the live site untouched.

- **Turn every steer and drop into an exam scenario** — FEATURE — value 5 — effort M — risk med — category: regression exams
  Why: steers like "I don't want foreman hardcoded to that" and the stale-finding drops are the user's real NEVERs. Nothing asserts them later.
  Done when: `fm exam gen` emits at least one scenario per recorded steer, and a build that reintroduces a hardcoded face list fails it.

- **Keep a ledger of standing grants** — SECURITY — value 4 — effort S — risk low — category: autonomy
  Why: "standing grant" to ship to main appears in T-2088, and approval in one context must not extend to another. Assumption: grants are currently only in task text.
  Done when: `fm grants` lists each grant with scope, date, use count and last use, and a use outside its scope is refused.

- **Verify before raising, and fingerprint what was dropped** — FIX — value 4 — effort M — risk low — category: false positives
  Why: two of five drops were stale ("already fixed in ee98a137", "no longer reproduces").
  Done when: a scout finding is reproduced on HEAD before it is queued, and a dropped finding with the same fingerprint is not re-raised.

- **Add a publish circuit breaker and one-command revert** — FEATURE — value 4 — effort S — risk low — category: publish safety
  Why: `fm genesis live on` publishes detached and unattended, so a bad export or a push loop has no stop.
  Done when: three failed or reverted publishes switch live off with a status note, and `fm genesis publish --revert` restores the previous site commit.

- **Cap what auto-start spends per project** — FEATURE — value 4 — effort M — risk med — category: economics
  Why: the request has Genesis starting itself when the queue runs dry. The pack shows no per-project ceiling, and a run is billed ($35 budget here).
  Done when: auto-start refuses to begin past a configured dollar or wall-clock cap, writes why, and resumes after a reset.

- **Show what changed since the user last looked** — FEATURE — value 4 — effort M — risk low — category: tower legibility
  Why: the user asked for every doc and per-generation detail readable on the page, so they are reading it repeatedly.
  Done when: the tower page marks docs and generations changed since the user's last visit, and a "since" filter shows only those.

- **Lint every site page for shared chrome** — CLEAN — value 3 — effort S — risk low — category: site consistency
  Why: the favicon, header and footer misses (T-2087 and the favicon FIX) were each found by the user, one page at a time.
  Done when: a test fails if any `site/**/index.html` lacks the shared header, footer, nav link, current favicon, or `style.css` tokens.

- **Show how far the tower page lags tower storage** — FEATURE — value 3 — effort S — risk low — category: freshness
  Why: T-2073 measures surface lag for the other surfaces, but the Genesis export is not among them.
  Done when: `fm genesis status` prints "site behind by N changes" and the loop queues a publish when N is over zero for a set time.

- **Backtest brainstorms against the user's real asks** — FEATURE — value 4 — effort M — risk low — category: idea quality
  Why: T-2076 feeds misses forward but never measures the predicted fraction.
  Done when: `fm ideas backtest` replays the last N user asks and reports the share that an earlier idea list covered, and the figure is stored per lens.

- **Carry miss classes across projects as standing questions** — FEATURE — value 3 — effort M — risk med — category: carry-over
  Why: the "where does the user look to judge this" question applies to any project, and gap map #13 wants carried-over defaults.
  Done when: a fresh project's gen-0 writer includes the generalized questions from earlier misses and cites their source tasks.

- **Run a simulated user against the idea list** — FEATURE — wild — value 4 — effort M — risk med — category: prediction
  Why: assumption: a tool-less child given only the user's words can write the next ten asks.
  Done when: the predictions are stored, scored a week later against the real asks, and the score appears in `fm ideas` output.

- **Trace each surprise ask to the stage that missed it** — FEATURE — wild — value 3 — effort L — risk med — category: retro-attribution
  Why: assumption: the Seed, Mission, critique and sweep stages each leave a record that can be searched.
  Done when: for a given miss, Genesis names the earliest tower stage that could have caught it and adds a scenario to that stage's exam.

- **Add a time-scrub slider to the tower page** — FEATURE — wild — value 3 — effort M — risk low — category: tower view
  Why: the user wants depth by generation, and a scrubber shows lineage, winners and losers as one motion.
  Done when: dragging the slider re-renders the graph at each generation, and reduced-motion users get stepped buttons instead.

Next question: What does the user see, and what can they undo, when Genesis does something outward-facing (publish, push, auto-start) while they are away?
Next question: Which of the user's recurring corrections ("smarter, not hardcoded", "verify, don't assume") can be tested mechanically, and which are still only prose?
