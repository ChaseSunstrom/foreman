# Brainstorm — lens: token thrift: same result for far fewer tokens

- **Send the ideas-so-far list as hashed titles, not full text** — FEATURE — value 4 — effort S — risk low — category: brainstorm cost
  Why: The "Ideas so far" block runs to roughly 1,000 lines and is repeated into every lens child, so each round pays for it again. Children only need to know which titles to avoid, and a short hash per title does that.
  Done when: a brainstorm pack with 1,000 prior titles is under 6 KB, and a child given a hashed title that matches a real idea still declines to repeat it in a fixture test.

- **Remove the duplicate sections from the context pack** — CLEAN — value 4 — effort S — risk low — category: context pack
  Why: The pack contains "The user's own words" twice, word for word, and the "Recent commits" and "Open work" sections are also long. Duplicates add tokens with no new information.
  Done when: the builder emits each section once, and a test asserts no heading appears twice in a built pack.

- **Trim search and tool output to a byte budget with a "narrow it" footer** — PERFORMANCE — value 4 — effort S — risk low — category: tool output
  Why: Assumption: long grep and read results are the usual source of wasted context. Capping them and saying how many hits were cut, and which narrower query to use, keeps the model from pulling everything.
  Done when: a grep returning 500 hits prints at most a fixed number of bytes plus one footer line with the hit count and a suggested narrower query.

- **Return subagent results as a file path and a five-line summary** — FEATURE — value 5 — effort S — risk low — category: subagent handoff
  Why: Scout and lens subagents return their full reports into the parent context. Writing the full result to a file and returning only the path and a summary keeps the parent small, and the file stays available if it's needed.
  Done when: a subagent run whose report is 4,000 tokens leaves the parent with under 150 tokens of returned text and a readable file at the path.

- **Ask children for a fixed table schema, not prose** — FEATURE — value 4 — effort M — risk med — category: output shape
  Why: Each brainstorm child writes up to 900 words of prose that the parent then parses. A fixed row schema carries the same fields in far fewer tokens and parses without a model call.
  Done when: a child's output validates against the schema in 100% of fixture runs, and its token count is at most 60% of the prose version on the same pack.

- **Stop a reply once its proof has passed** — FIX — value 3 — effort S — risk low — category: reply length
  Why: Assumption: the model often keeps writing after the gate has already passed, adding commentary the user does not read. Ending the reply at the proof line saves output tokens on every finished task.
  Done when: a finished task's close message contains the proof line and nothing after it, and a fixture with a failing proof still includes the failure detail.

- **Make `fm cost` attribute spend to its source** — FEATURE — value 5 — effort M — risk low — category: cost attribution
  Why: `fm cost` reports context per reply, but not what caused it. Splitting each turn's tokens into rules, the pack, tool results and the model's own output shows which one to cut first.
  Done when: `fm cost` on a session prints one line per source with its share of input tokens, and the lines sum to the session total within 1%.

- **Wild: charge the model per proof, and refuse a reply that proves nothing before it is billed** — FEATURE — value 3 — effort L — risk med — category: spend gate
  Why: Assumption: many replies spend tokens without moving a gate. A pre-billing check that asks whether the reply adds a runnable proof, a diff or a question would stop empty turns before they cost anything.
  Done when: a fixture of 50 replies with no diff, proof or question is held back before billing, and no reply with a passing proof is held.

- **Wild: a prompt compiler that rewrites the rules file into its cheapest equivalent, proven by the duel** — PERFORMANCE — value 4 — effort L — risk med — category: prompt compile
  Why: The rules file and skill bodies are plain prose with redundant phrasing. A compiler could shorten them to an equivalent form, and the existing duel would confirm that task outcomes did not change.
  Done when: the compiled rules file is at least 25% smaller in tokens, and the duel's pass rate on the same tasks matches the uncompiled file within the noise band.

- **Wild: a token bill with a weekly "cut this" offer** — FEATURE — value 4 — effort M — risk low — category: usage digest
  Why: Usage is only visible as a total. A weekly receipt naming the single largest avoidable cost, such as a repeated file read or an oversized pack, gives the user one concrete cut to accept.
  Done when: the weekly digest names one source with its token count and a single command that would cut it, and the command shrinks that source in a test run.

- **Use cheap local grep before any model read** — PERFORMANCE — value 3 — effort S — risk low — category: retrieval
  Why: Assumption: the model reads whole files to find one line. Running a local search first and returning only matching lines keeps reads small without changing what the model can see.
  Done when: a question answerable by a single grep is answered from the grep output with a file read count of zero, in a fixture run.

- **Give each hook a token budget it must report** — CLEAN — value 3 — effort S — risk low — category: hook output
  Why: Hooks inject text into context without any limit or report. A printed budget per hook makes the cost visible in the next run, so the largest injector gets fixed first.
  Done when: every hook's output size appears in `fm doctor`, and a hook that exceeds its budget is flagged in the next run's report.
