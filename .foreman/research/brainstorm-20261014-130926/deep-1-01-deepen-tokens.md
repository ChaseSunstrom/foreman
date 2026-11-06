# Brainstorm — lens: deepen: tokens

- **Build a token ledger that every Foreman surface writes to** — FEATURE — value 5 — effort M — risk low — category: tokens
  Why: the pack's existing ideas are all "measured ~1.04M tokens/30 days" claims from one-off scripts, and several ideas ("count tokens not characters", "report biggest outputs", "fetch-back rate") each need the same measurement. assumption: transcripts or hook payloads expose usage so per-source attribution is possible.
  Done when: `fm tokens` prints a 30-day table by source (Bash output, Read, brainstorm children, lane briefs, hook injections, recall) with tokens, not chars, and a test feeds a fixture transcript and checks the totals.

- **Run compact output in shadow mode and log what it would have cut** — FEATURE — value 5 — effort S — risk low — category: compact-output
  Why: round 1 shipped compact output off, waiting on the user's yes. The listed ideas converge on shadow first, then ask with evidence. Shadow mode writes the full text to state/outputs and the would-be stub to a log, and sends the model nothing different.
  Done when: with `compact: shadow` set, a Bash output of 20k chars reaches the model unchanged, and `fm tokens --shadow` reports the chars and tokens a rewrite would have saved, per command family.

- **Gate the compact-output switch on measured fetch-backs, per command family** — FEATURE — value 4 — effort M — risk med — category: compact-output
  Why: the fetch-back list ("re-fetch tripwire", "expandable", "per command family") describes one mechanism. Enable compaction for a family such as pytest, build or git log only when the shadow data show the model rarely reads the spill file afterwards, and disable it automatically when it does.
  Done when: a fixture log with 20% fetch-backs for `npm test` leaves it uncompacted, a 1% family is compacted, and `fm doctor` shows each family's state and rate.

- **Add runner-specific failure digesters with golden tests** — FEATURE — value 4 — effort M — risk med — category: compact-output
  Why: the generic head, failure lines and tail rewrite can drop the one line that matters, and the pack's own bug history is about failure formats (`✗ exit N` vs `exit N`). A digester per runner (pytest, cargo, go test, tsc, eslint) keeps the failing test name, assertion and file:line.
  Done when: golden fixtures from each runner compact to under 1,500 chars, every failing test id is still present, and a lossless-for-failures property test passes.

- **Give each stub a one-line recovery command and keep the spill alive while cited** — FEATURE — value 4 — effort S — risk low — category: compact-output
  Why: the listed ideas "self-recoverable stubs" and "keep pointers alive" are the same fix. The stub ends with `fm out ID --grep PATTERN | --lines A-B`, and `fm tidy` skips any file whose id appears in the current transcript or an open task. Today tidy prunes compact full texts after 7 days, which may orphan a pointer.
  Done when: a stub names a working `fm out` command, a 10-day-old spill cited by an open task survives `fm tidy`, and an uncited one is pruned.

- **Build the brainstorm pack from a budgeted, prefix-stable template** — PERFORMANCE — value 4 — effort M — risk low — category: brainstorm-cost
  Why: this pack repeats "The user's own words" in full, twice, and the tokens list repeats entries verbatim (for example "Ship runner-specific failure digesters" and "Make compact-output stubs self-recoverable" each appear twice). Dedupe blocks, put static material first so the prompt cache hits, and cap each section by token count.
  Done when: a lint test fails on a pack with a duplicated block, and two consecutive brainstorm spawns show a cache-read share above 80% of input tokens in the ledger.

- **Send each lens only the slice of the pack it needs** — PERFORMANCE — value 3 — effort M — risk med — category: brainstorm-cost
  Why: the "ideas so far" list, the commit log and the file map matter differently per lens; "unspoken needs" wants user words and not the map, and "capability map" wants the map and not the history. assumption: a per-lens section allowlist loses little quality.
  Done when: `fm ideas --dry-run` prints the token size per lens, the average drops at least 30% against the full pack, and a test checks that the allowlist never removes the request or the lens text.

- **Replace the "ideas so far" list with cluster summaries plus a nearest-neighbour check afterwards** — PERFORMANCE — value 4 — effort M — risk med — category: brainstorm-cost
  Why: the pack's category list is long and heavily repeated, and the pile saturates, so children burn tokens reading what not to say. Send cluster titles with counts, then dedupe returned ideas against the full catalogue locally.
  Done when: the pack's idea section drops below 1,500 tokens at 500+ ideas, and a returned duplicate is flagged by the local check with the id of its match.

- **Scale the number of lenses to the saturation of the pile** — PERFORMANCE — value 3 — effort S — risk low — category: brainstorm-cost
  Why: round 2 asks for ideas past every earlier idea, and the category list shows the same idea reproduced by several children. Track the share of new ideas per lens over the last rounds, and skip lenses below a threshold.
  Done when: after a fixture round where one lens returns 90% duplicates, the next `fm ideas` run reports that lens as skipped with its yield.

- **Make successful `fm` verbs print one line** — PERFORMANCE — value 3 — effort S — risk low — category: tokens
  Why: the model reads every `fm` result, and the pack's own idea list calls for silent success. Failures and `--verbose` keep the full text. assumption: fm's success output is multi-line today.
  Done when: `fm task set` and `fm bus send` print at most one line on success, and the existing tests that read their output still pass.

- **Let the ledger set a per-task token budget, and warn when a task is on track to exceed its tier** — FEATURE — value 4 — effort M — risk med — category: budgets
  Why: lane briefs already carry tier-based effort and `--max-budget-usd`, but nothing ties spend to the S/M/L tier the task was planned at, and tier drift is already measured for diff size. assumption: the ledger can attribute tokens to a task id.
  Done when: finishing a task prints its tokens against the median for its tier, and a task at 3x the median triggers a close-time warning listed in the receipt.

- **Wild: Let the model ask for a command's output ahead of time ("output contracts")** — FEATURE — value 3 — effort L — risk med — category: wild
  Why: wild. Before a noisy command the model states what it needs ("failures only", "counts"), and a PreToolUse hook rewrites the command, for example adding `-q --tb=short`, instead of compacting afterwards. assumption: a hook can rewrite tool input.
  Done when: a test running pytest with the contract "failures only" shows the rewritten command and an output at least 80% smaller with the same failing test ids.

- **Wild: Grow a per-project "noisy command" dictionary from the ledger and ship it as a shareable file** — FEATURE — value 3 — effort M — risk med — category: wild
  Why: wild. The ledger learns that `make all` in this repo emits 90k chars of which only the last 40 lines are ever read, writes a rule file (command pattern, keep rules), and users can share rule files across projects like `.gitignore` templates.
  Done when: after replaying a fixture history, `fm tokens --learn` writes a rule file that, applied in shadow mode, cuts that command by over 80% with no failure lines lost.

- **Wild: Add a "token weather" line in the status bar that turns red when a runaway loop is burning budget** — FEATURE — value 3 — effort S — risk low — category: wild
  Why: wild. The ledger gives a live rate. Show tokens per minute and the top source in the status line, and push a one-time notification when the rate is three times the 30-day median for 5 minutes, which catches loops like repeated failing retries.
  Done when: a simulated burst in the ledger flips the status output to the warning state and sends exactly one push request.

- **Wild: Replay a finished task offline with and without each optimisation to prove what it saved** — FEATURE — value 3 — effort L — risk med — category: wild
  Why: wild. The 1.04M-token claim is an estimate. Replaying recorded tool outputs through the compactor, the pack linter and the lens slicer gives exact before/after numbers per task, which makes the next "ask for a yes" evidence and not a forecast.
  Done when: `fm tokens replay T-ID` prints saved tokens per optimisation and the sum matches a hand-computed fixture.
