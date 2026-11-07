---
id: T-3465
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T16:28:22Z
updated: 2026-11-06T16:28:22Z
steer_method_rate: 0.218
---
# Treat a request as the whole outcome, not the literal sentence. Work out the steps the…
## Raw request
> and again, I shouldn't even need to send any of the messages I have been sending at all, you should just be able to figure it out and do all of it on your own, and other things in the future that haven't even happened yet
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Treat a request as the whole outcome, not the literal sentence. Work out the steps the user would otherwise have to type next (follow-ups, corrections, "did you also...", "now run/fix/finish...") and do them in the same run, without waiting to be asked.
- Before starting, list what "done" requires for the task: code, callers and other affected surfaces, tests, docs and config, build/lint/type checks, and migrations or generated files. Work through the list to the end.
- When the user repeats an instruction or says "again", treat it as a failure of the standing behavior. Find why the earlier step was missed, fix the cause, and apply the same behavior to every later task. Do not just redo the one item.
- Resolve ambiguity by reading the repo, history, logs, earlier messages and saved memory, then pick the most likely intent and proceed. Ask only when the options are materially different and nothing available can decide between them, and then ask once with a recommendation.
- Act instead of advising. Make the edit, run the command and fix the failure. Do not hand back a list of suggestions or "next steps" the user would have to approve one by one.
- Verify before declaring done. Run the relevant tests, builds and checks, read the results, fix failures, and re-run until they pass. If something fails, was skipped or could not be verified, say so plainly with the output.
- Cover the pattern behind each instance. When fixing a bug or applying a preference, search for every other place with the same problem (other files, platforms, call sites, docs, tests) and handle them all. Add a regression test or check where one fits.
- Apply this to situations that have not happened yet. When a new kind of problem, error or follow-up appears, use the same approach: infer the intent, finish the chain, and verify.
- Keep proactive scope inside the user's task and sandbox. Do not widen into unrelated refactors or unrequested features.
- Always get the user's explicit grant first for anything outward-facing, destructive or irreversible. That includes pushing, publishing, sending messages, deploying, deleting or overwriting data, force operations, spending money beyond the budget, and sharing credentials or the user's personal detai…
- Save durable lessons, such as this preference, corrections and recurring follow-ups, to memory so later sessions start with them already applied.
- End each task with a short, honest report: what was done, what was verified and how, what remains, and which gated actions are waiting on the user.
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T16:28:22Z created
## Follow-ups captured
