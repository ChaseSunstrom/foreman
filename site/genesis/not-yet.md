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
