# Not yet — ideas waiting on a blocker

Each item: `## <idea>`, then `- blocker:`, `- tried: <approach>; <another>` (two different ones), `- unblocks-with:`, and
`- added: gen-N …` or `- retried: gen-N …` for the newest generation. `## Removed` lines say proven harm or exact duplicate.
Candidates the user named for the model layer (T-2437) wait here as unevaluated until an exam arm runs them; a candidate
owes two tries only once it has been evaluated.

## selfjev-4b
- blocker: unevaluated: no exam arm has run it against a path it would replace
- unblocks-with: an exam arm (intake tier, lead triage or dedupe) where it beats the current path on accuracy, cost or latency, its probabilities checked against outcomes; reached through the Jev-compatible API at TYPESAFE_BASE_URL
- added: gen-2, a local backend the user named for the model layer
- retried: gen-3, the blocker re-checked: TYPESAFE_BASE_URL is unset on this machine (fmmodels.py reads it), so no exam arm can reach the backend; the user's endpoint is the unblock, asked in the final report

## jeff
- blocker: unevaluated: no exam arm has run it against a path it would replace
- unblocks-with: the same exam arms as selfjev-4b, run on this machine behind the Jev-compatible API; kept only where it beats the path it replaces
- added: gen-2, the second local backend the user named
- retried: gen-3, the same re-check as selfjev-4b: TYPESAFE_BASE_URL unset, so no arm can run it here

## Jevlike
- blocker: unevaluated: no task-specific model has been trained from Foreman's own history yet
- unblocks-with: labelled rows from closed tasks (tier, lead, dedupe decisions), a night-run training job staged as a candidate, and an exam arm where the trained model beats the path it replaces
- added: gen-2, the trainer the user named for task-specific models
- retried: gen-3, the labelled rows grew (1,768 closes with fates; T-2688 starts logging the user's answers), but T-2687 found that nothing in a brief and diff predicts a close's survival past chance (AUC 0.58 at best), so a trained model has no target shown learnable yet; still no training job

## Von
- blocker: unevaluated: intent routing has no exam arm yet
- unblocks-with: an exam arm on held-out requests where Von's routing beats fm code's current planner choice on accuracy, cost or latency
- added: gen-2, the intent router the user named
- retried: gen-3, re-checked fm exam's kinds and arms: none routes intents, so the blocker holds; gen 3's Missions built no routing arm

## Byte-stable goal card in the cached prefix
- blocker: no measurable win: the goal card is about 120 characters (around 30 tokens), and the SessionStart context is cached after its first write in each session, so moving it into the prefix shared across sessions saves about 30 cache-write tokens per new session
- tried: a byte-stable goal line in the SessionStart context (T-2143: the lines before it change every session, so it kept no extra prefix); a goal card in a file Claude Code loads with CLAUDE.md (T-2418: the whole card is ~30 tokens, below anything fm cost can tell apart)
- unblocks-with: a goal card large enough to matter (the Seed's Missions or the gap map's top rows, 2k+ tokens, read by every session), measured by fm cost --by-model before and after
- added: gen-2, from gen-1/critique-finish.md via T-2418
- retried: gen-3, re-measured: the goal card is still about 30 tokens, and fm burden --by-source (T-2667) puts SessionStart at 42.9 characters per turn in all; nothing a session reads is near the 2k tokens that would make a shared cached prefix pay

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

## M-12 · Weight deciders by a scored market on whether a close survives
- blocker: no decider beats chance on whether a close survives 14 days unfixed, so a pool has nothing to weight. On 22 failed and 22 era-matched held closes, the best AUC was 0.58, and the log-weighted pool scored Brier 0.286 against the best single's 0.275 (90% interval of the margin -0.039 to +0.016).
- tried: models reading the work, a Haiku planner and a Sonnet cold rival given the brief and the diff (AUC 0.58 and 0.50); the record, the held rate of settled closes of the same type and tier and of earlier closes that touched the same files (AUC 0.49 and 0.48). Both via bench/moonshot/kill_m12.py (T-2687); an earlier run whose held closes came from an older era only was confounded and set aside.
- unblocks-with: one forecaster that beats chance from what is known at close: the close's verification grade and unproven kinds, its test evidence, or M-16's warranty claims as a denser label; then rerun the same script with it added
- added: gen-3, the moonshot Mission's spike (Mission 8)
