# Brainstorm — lens: token thrift: same result for far fewer tokens

- **Dedupe repeated tool errors within a session** — PERFORMANCE — value 4 — effort S — risk low — category: tool output
  Why: assumption: retry loops re-send identical stderr each time, so the same failure costs full tokens again on every attempt. Send the full error once, then "same as turn N, exit 1" with a hash.
  Done when: a replayed 5-retry failing Bash fixture sends the full error once and each repeat under 40 tokens.

- **Offload large pastes and logs to files** — FEATURE — value 4 — effort S — risk low — category: context intake
  Why: assumption: a pasted log or CI dump lands inline in context. Store it as a file, give the model the path, a 10-line head and the error lines, and let it read ranges on demand.
  Done when: a 200 KB pasted log enters context as a path plus at most 40 lines, and the reply can still cite a line from the file.

- **Memoize read-only shell commands by tree hash** — PERFORMANCE — value 4 — effort M — risk med — category: repeat calls
  Why: assumption: `git status`, `grep` and `ls` run again and again on an unchanged tree. Cache the result keyed by a tree hash that covers untracked files, and say "cached at tree abc123".
  Done when: a repeated grep on an unchanged tree returns the cached result with no process spawn, and touching one file invalidates it.

- **Strip framework frames from failing stack traces** — CLEAN — value 3 — effort S — risk low — category: test output
  Why: assumption: a failing test prints 40 frames from site-packages or node_modules, and only the project frame and the assertion matter. Keep those and collapse the rest into a count.
  Done when: a 40-frame fixture renders at most 6 lines, and the project frame and the assertion line both survive.

- **Inject each hook reminder once per session and re-send only on change** — PERFORMANCE — value 4 — effort S — risk med — category: hook output
  Why: assumption: the same reminder text is injected on every tool call, so a 30-turn session pays for it 30 times. Re-inject after a compaction or when the rule's text changes.
  Done when: a 30-turn fixture session's hook output drops by at least 80%, and a changed rule re-injects exactly once.

- **Show the model its remaining turn budget** — FEATURE — value 3 — effort S — risk low — category: self-limiting
  Why: assumption: the model can't see how much of its turn budget is left, so it spends it without noticing. A one-line counter each turn lets it stop early on its own.
  Done when: each turn's injected context includes a "budget left" line, and it reaches zero before the runtime ceiling fires.

- **Measure the rules file's budget in tokens, not characters** — CLEAN — value 3 — effort S — risk low — category: budget accounting
  Why: the doctor's 6,400-character budget is already exceeded by the 6,416-character rules file. Characters don't track what the model pays. Count with a tokenizer and fail on the token budget instead.
  Done when: `fm doctor` reports a token count for the rules file and fails over the token budget, and the character-budget test is replaced by a token test.

- **Show cost per green gate on the Today chart** — FEATURE — value 3 — effort S — risk low — category: spend visibility
  Why: assumption: spend is shown in total, so a cheap run that proves nothing looks the same as a costly one that proves a fix. Dividing spend by green gates shows the real efficiency.
  Done when: the Today chart shows a cost-per-green-gate figure, and a run with zero green gates shows "no proof" instead of a number.

- **Wild: Write status lines from the journal, not from the model** — FEATURE — value 3 — effort M — risk low — category: narration
  Why: wild: the model's between-tool-call narration is mostly restating what the journal already records. Generate those lines from the journal at zero tokens, and let the model speak only when it has a decision.
  Done when: a 10-step fixture run produces no model-written status sentences between tool calls, and the user-visible log matches the journal entries.

- **Wild: Prune reply sentences that no acceptance check cites** — FEATURE — value 3 — effort M — risk med — category: reply trimming
  Why: wild: a reply's sentences that aren't tied to an acceptance check or a proof can be cut before they reach the user. Keep anything that cites a check.
  Done when: a 10-sentence fixture reply with 4 uncited sentences is cut to 6, and every cited proof still appears.

- **Wild: Cite pack sections by ID instead of restating them** — FEATURE — value 3 — effort M — risk med — category: referencing
  Why: wild: replies and child outputs repeat text from the context pack. Give each pack section a short ID, like [F3], and let the model cite the ID. Readers expand it only if they need it.
  Done when: a fixture child reply that quoted a 300-token section now cites its ID, and the expanded text round-trips to the original section byte for byte.
