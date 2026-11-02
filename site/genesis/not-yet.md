# Not yet — ideas waiting on a blocker

Each item: `## <idea>`, then `- blocker:`, `- tried: <approach>; <another>` (two different ones), `- unblocks-with:`, and
`- added: gen-N …` or `- retried: gen-N …` for the newest generation. `## Removed` lines say proven harm or exact duplicate.
Candidates the user named for the model layer (T-2437) wait here as unevaluated until an exam arm runs them; a candidate
owes two tries only once it has been evaluated.

## selfjev-4b
- blocker: unevaluated: no exam arm has run it against a path it would replace
- unblocks-with: an exam arm (intake tier, lead triage or dedupe) where it beats the current path on accuracy, cost or latency, its probabilities checked against outcomes; reached through the Jev-compatible API at TYPESAFE_BASE_URL
- added: gen-2, a local backend the user named for the model layer

## jeff
- blocker: unevaluated: no exam arm has run it against a path it would replace
- unblocks-with: the same exam arms as selfjev-4b, run on this machine behind the Jev-compatible API; kept only where it beats the path it replaces
- added: gen-2, the second local backend the user named

## Jevlike
- blocker: unevaluated: no task-specific model has been trained from Foreman's own history yet
- unblocks-with: labelled rows from closed tasks (tier, lead, dedupe decisions), a night-run training job staged as a candidate, and an exam arm where the trained model beats the path it replaces
- added: gen-2, the trainer the user named for task-specific models

## Von
- blocker: unevaluated: intent routing has no exam arm yet
- unblocks-with: an exam arm on held-out requests where Von's routing beats fm code's current planner choice on accuracy, cost or latency
- added: gen-2, the intent router the user named

## Byte-stable goal card in the cached prefix
- blocker: no measurable win: the goal card is about 120 characters (around 30 tokens), and the SessionStart context is cached after its first write in each session, so moving it into the prefix shared across sessions saves about 30 cache-write tokens per new session
- tried: a byte-stable goal line in the SessionStart context (T-2143: the lines before it change every session, so it kept no extra prefix); a goal card in a file Claude Code loads with CLAUDE.md (T-2418: the whole card is ~30 tokens, below anything fm cost can tell apart)
- unblocks-with: a goal card large enough to matter (the Seed's Missions or the gap map's top rows, 2k+ tokens, read by every session), measured by fm cost --by-model before and after
- added: gen-2, from gen-1/critique-finish.md via T-2418

## Proofs expire when the thing proved changes
- blocker: its kill test found no stale proof. Of the last 10 done tasks, 3 had a later commit on their files (T-2610, T-2605, T-2601), and the full gate at that commit reran every test their proofs rest on; a non-test proof (a shot, a bench) going stale after a later change has no case on record
- tried: a green run clears a proof kind only when it came after the task's last edit (within a task); tree and world stamps on every evidence line, so a run says which tree it proved
- unblocks-with: a done task whose `fm shot` or `--bench` proof predates a later commit that changed the screen or code it measured
- added: gen-3, from the #6 brainstorm (research/brainstorm-20261102-081535)

## Plan-time example confirmation
- blocker: its kill test needs the user present (mock one sheet for one task; drop it if only the summary line is read), and this run is unattended
- tried: fm spec's concrete assertions from a wish, keeping the user's own examples (fmchange.cmd_spec); the meaning class binding each request clause to a failable criterion (T-2393)
- unblocks-with: one session with the user, who reads a mocked example sheet for one task and says whether the pairs changed what they'd accept
- added: gen-3, from the #6 brainstorm (research/brainstorm-20261102-081535)
