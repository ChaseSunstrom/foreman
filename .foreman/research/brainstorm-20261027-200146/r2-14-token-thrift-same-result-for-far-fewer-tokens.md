# Brainstorm — lens: token thrift: same result for far fewer tokens

- **Read one symbol, not the whole file** — PERFORMANCE — value 4 — effort M — risk low — category: context reads
  Why: the pack's ~140k-per-reply target is hard to hit when edits pull in whole files. assumption: most edits touch one function in a file over 400 lines.
  Done when: a read of one function in a 2,000-line fixture returns under 200 lines, and an edit to it still applies in a test.

- **Escalate the model only when the proof fails** — FEATURE — value 5 — effort M — risk med — category: model cascade
  Why: builders already moved to Sonnet (T-1796). assumption: most small tasks pass a first gate on the cheaper tier, so the costlier retry is rare and can be triggered by evidence rather than guessed up front.
  Done when: a task that passes its first gate records zero escalations, and a task that fails reruns once on the next tier, with both steps shown in `fm cost`.

- **Send tool schemas only for the tools this task kind uses** — PERFORMANCE — value 4 — effort S — risk low — category: tool definitions
  Why: assumption: every turn carries every tool definition, though the skill listing is already routed. A docs-only task has no use for the edit or shell schemas.
  Done when: a docs-only task's request omits the shell and edit tool schemas, and the prompt-size bench drops by the size of those schemas.

- **Warn when an edit busts the prompt cache** — FEATURE — value 4 — effort S — risk low — category: cache hits
  Why: assumption: editing the rules file or a system prompt mid-session invalidates the cached prefix. The rules file is 6,416 chars and was trimmed for budget (T-1520), so it changes often.
  Done when: editing the rules file mid-session prints a one-line cache-cost warning, and `fm cost` reports the cache hit rate before and after.

- **Report a green gate in one line** — PERFORMANCE — value 4 — effort S — risk low — category: output size
  Why: the compact output rollout (T-0828) is still in shadow mode and covers failures first. assumption: a passing test run sends its full log to the model, which buys nothing once it has passed.
  Done when: a fixture run with 300 passing tests reaches the model as one line with the count and duration, and a failing run still shows the failing test names and first traceback line.

- **Stop a brainstorm lens when its next idea repeats an earlier one** — FEATURE — value 3 — effort S — risk low — category: brainstorm cost
  Why: lenses produce overlapping ideas, and every extra idea costs output tokens the round then has to dedupe. assumption: a lens that repeats itself has nothing left to add.
  Done when: a lens whose new idea matches a prior idea's title stops early, and the round's journal records the stop reason.

- **Park an idle session as a 500-token card** — FEATURE — value 4 — effort M — risk med — category: session memory — wild
  Why: wild: when a session sits idle, save its state as one short card with the open decisions, the files touched and the next step, then rebuild from the card on resume. assumption: a resumed session re-reads more than it needs.
  Done when: a session idle for 30 minutes resumes with under 2,000 tokens of replayed context, and the resumed run finishes the same test it was on.

- **Compress tool output with a local model before it leaves the machine** — PERFORMANCE — value 4 — effort M — risk med — category: local compression — wild
  Why: wild: a small model running on the owner's hardware cuts a 50 KB log to the lines that matter before the cloud model reads it, which also keeps the raw log off the network. assumption: most tool output is noise around one or two decisive lines.
  Done when: a 50 KB failing build log reaches the model as under 2 KB, and the failing line and its file:line survive in a test.

- **Answer "where is X" with a file:line, not prose** — FEATURE — value 3 — effort S — risk low — category: answer shape — wild
  Why: wild: a locate question that the repo can answer gets a `file:line` reply and nothing else, instead of an explanation that restates it. assumption: many questions to the agent are locate questions, and the prose around the answer is most of the cost.
  Done when: a "where is X" query on the fixture returns one `file:line` string under 30 tokens, and a "why" query still returns a full answer.

- **Wild: find the smallest context that still fails** — FEATURE — value 3 — effort M — risk med — category: context pruning — wild
  Why: wild: when a run fails, halve its context and re-run the failing check to find the few paragraphs it needs, then keep only those for the retry. assumption: the context pack carries blocks the failing check never reads.
  Done when: on a fixture with one needed paragraph among 40, the search keeps that paragraph and drops at least 80% of the others, and the retry passes.
