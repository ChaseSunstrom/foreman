---
id: T-0260
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T05:50:48Z
updated: 2026-10-04T05:51:02Z
batch: [T-0253, T-0254, T-0255]
---
# Evidence quality: inconclusive runs, assumed vs verified facts, surprise log
## Raw request
> T-0253: FEATURE: surprise log — fm surprise "<expected> → <observed>" records where the model of the code was wrong; fm friction and recall surface them
> CONTEXT: plugin/lib/fmresearch.py (claims, verify, note); budgets from fm budget; foreman-ui shows the note's agreement and conflicts
> CONTEXT: plugin/lib/fmcli.py cmd_audit, fmplugins skill index (T-0205), references/audit.md
> CONTEXT: plugin/lib/fmbench.py build/validate need tests today; fmideas.taste for preferences
> CONTEXT: fm audit prep briefs (T-0216 split), foreman:fm-reviewer agent, fm research add for replies
> CONTEXT: L plans get only a self-critique today (references/planning.md); child pattern from fmideas; budget from fm budget
> CONTEXT: fm lane (fmlanes.py) makes worktrees with their own active task; fm run --parallel merges lanes; the delegation reference says the main thread does all edits — this adds a bounded exception
> CONTEXT: fm friction digests ledgers; transcripts under ~/.claude/projects; capture --source self
> CONTEXT: fm run/serve (systemd user units, guard category system/remote), fm evolve, fm bench, economy mode usage windows
> CONTEXT: research/harness-landscape-20261003.md; fmresearch
> CONTEXT: stdlib urllib to PyPI/npm/crates JSON APIs (public https only, like fmresearch.fetch)
> CONTEXT: fmresearch.fetch/verify
> CONTEXT: fm bench run uses --setting-sources project,local and --plugin-dir; a second --plugin-dir adds the contender
> CONTEXT: fm evolve's HEAD worktree helper (fmbench._worktree); fm bench gate
> CONTEXT: fmideas.taste (steers, corrections, drops); bench judge
> CONTEXT: fmbench replay machinery, fmideas.taste
> CONTEXT: bench replay machinery; the README
> CONTEXT: stdlib JSON-RPC over stdio; registering an MCP server is guard category plugin (user's yes)
> CONTEXT: fm cost counts next followed/ignored (fmcost.py)
> CONTEXT: corrections in the ledger (fmideas.taste), PreToolUse notes in fmhooks
> DONE-WHEN: stubbed researchers that disagree produce a note with the conflict flagged, and a single-source claim marked as such
> DONE-WHEN: with a fake installed security skill, audit prep's brief and output name it for the adversary lens
> DONE-WHEN: a docs-only finished task becomes a judged case and a stubbed judge's score lands in the results and in fm bench show
> DONE-WHEN: audit prep --debate writes a rebuttal brief that embeds the first review and the output says how to run it; references/audit.md documents it
> DONE-WHEN: with a stub, fm plan-review writes a Plan review section with objections and a verdict line
> DONE-WHEN: the agent file exists with a lane-only contract, fm lane gives a builder brief, and delegate.md documents when and how to merge
> DONE-WHEN: with a stub, a session start after a session with an unanswered request captures it as a self item, once
> DONE-WHEN: fm night --dry-run lists what it would run within the budget and refuses when usage is above the threshold
> DONE-WHEN: with stubbed research, fm landscape writes a dated note and a diff against the previous one
> DONE-WHEN: with a fake registry response, fm deps lists an outdated major and offers the migration research
> DONE-WHEN: a second verify of the same URL the same day reads the cache; a two-question file yields two notes
> DONE-WHEN: with a stub, fm bench duel records both arms and prints the gate between them
> DONE-WHEN: fm bench versions REV runs both arms and prints the gate
> DONE-WHEN: fm bench court builds judged cases from recorded steers and runs them on a plugin
> DONE-WHEN: with stubs, fm bench soak runs a two-turn conversation and records the user-child's complaints
> DONE-WHEN: with a stub, fm bench stranger records the session's guard blocks and failed fm calls as findings
> DONE-WHEN: an initialize + tools/list + tools/call round trip over stdio returns the state
> DONE-WHEN: fm export agents writes a file under a size cap with those sections
> DONE-WHEN: a decision with a path trigger shows in fm next after that file changes
> DONE-WHEN: a two-file diff where one imports the other lists the imported one first
> DONE-WHEN: fm proof on a finished task prints those sections
> DONE-WHEN: after N ignored hints of one kind the injected Next line drops that hint's detail
> DONE-WHEN: after a recorded "never push without asking" correction, a git push command gets the note
> DONE-WHEN: fmplugins and cmd_audit read the JSON and fm evolve accepts it as a target
> DONE-WHEN: a recorded surprise appears in fm friction's digest and in recall for a related query
> DONE-WHEN: fm task assume/verify set the tags and done warns on unverified assumptions in M/L
> DONE-WHEN: an inconclusive run leaves the step open and the done gate refuses
> DONE-WHEN: a request matching an existing fm command's help text gets the note
> T-0254: FEATURE: assumed vs verified facts — the brief's Assumptions lines carry [assumed] or [verified: <evidence>], and fm next asks to verify assumptions a step depends on
> CONTEXT: plugin/lib/fmresearch.py (claims, verify, note); budgets from fm budget; foreman-ui shows the note's agreement and conflicts
> CONTEXT: plugin/lib/fmcli.py cmd_audit, fmplugins skill index (T-0205), references/audit.md
> CONTEXT: plugin/lib/fmbench.py build/validate need tests today; fmideas.taste for preferences
> CONTEXT: fm audit prep briefs (T-0216 split), foreman:fm-reviewer agent, fm research add for replies
> CONTEXT: L plans get only a self-critique today (references/planning.md); child pattern from fmideas; budget from fm budget
> CONTEXT: fm lane (fmlanes.py) makes worktrees with their own active task; fm run --parallel merges lanes; the delegation reference says the main thread does all edits — this adds a bounded exception
> CONTEXT: fm friction digests ledgers; transcripts under ~/.claude/projects; capture --source self
> CONTEXT: fm run/serve (systemd user units, guard category system/remote), fm evolve, fm bench, economy mode usage windows
> CONTEXT: research/harness-landscape-20261003.md; fmresearch
> CONTEXT: stdlib urllib to PyPI/npm/crates JSON APIs (public https only, like fmresearch.fetch)
> CONTEXT: fmresearch.fetch/verify
> CONTEXT: fm bench run uses --setting-sources project,local and --plugin-dir; a second --plugin-dir adds the contender
> CONTEXT: fm evolve's HEAD worktree helper (fmbench._worktree); fm bench gate
> CONTEXT: fmideas.taste (steers, corrections, drops); bench judge
> CONTEXT: fmbench replay machinery, fmideas.taste
> CONTEXT: bench replay machinery; the README
> CONTEXT: stdlib JSON-RPC over stdio; registering an MCP server is guard category plugin (user's yes)
> CONTEXT: fm cost counts next followed/ignored (fmcost.py)
> CONTEXT: corrections in the ledger (fmideas.taste), PreToolUse notes in fmhooks
> DONE-WHEN: stubbed researchers that disagree produce a note with the conflict flagged, and a single-source claim marked as such
> DONE-WHEN: with a fake installed security skill, audit prep's brief and output name it for the adversary lens
> DONE-WHEN: a docs-only finished task becomes a judged case and a stubbed judge's score lands in the results and in fm bench show
> DONE-WHEN: audit prep --debate writes a rebuttal brief that embeds the first review and the output says how to run it; references/audit.md documents it
> DONE-WHEN: with a stub, fm plan-review writes a Plan review section with objections and a verdict line
> DONE-WHEN: the agent file exists with a lane-only contract, fm lane gives a builder brief, and delegate.md documents when and how to merge
> DONE-WHEN: with a stub, a session start after a session with an unanswered request captures it as a self item, once
> DONE-WHEN: fm night --dry-run lists what it would run within the budget and refuses when usage is above the threshold
> DONE-WHEN: with stubbed research, fm landscape writes a dated note and a diff against the previous one
> DONE-WHEN: with a fake registry response, fm deps lists an outdated major and offers the migration research
> DONE-WHEN: a second verify of the same URL the same day reads the cache; a two-question file yields two notes
> DONE-WHEN: with a stub, fm bench duel records both arms and prints the gate between them
> DONE-WHEN: fm bench versions REV runs both arms and prints the gate
> DONE-WHEN: fm bench court builds judged cases from recorded steers and runs them on a plugin
> DONE-WHEN: with stubs, fm bench soak runs a two-turn conversation and records the user-child's complaints
> DONE-WHEN: with a stub, fm bench stranger records the session's guard blocks and failed fm calls as findings
> DONE-WHEN: an initialize + tools/list + tools/call round trip over stdio returns the state
> DONE-WHEN: fm export agents writes a file under a size cap with those sections
> DONE-WHEN: a decision with a path trigger shows in fm next after that file changes
> DONE-WHEN: a two-file diff where one imports the other lists the imported one first
> DONE-WHEN: fm proof on a finished task prints those sections
> DONE-WHEN: after N ignored hints of one kind the injected Next line drops that hint's detail
> DONE-WHEN: after a recorded "never push without asking" correction, a git push command gets the note
> DONE-WHEN: fmplugins and cmd_audit read the JSON and fm evolve accepts it as a target
> DONE-WHEN: a recorded surprise appears in fm friction's digest and in recall for a related query
> DONE-WHEN: fm task assume/verify set the tags and done warns on unverified assumptions in M/L
> DONE-WHEN: an inconclusive run leaves the step open and the done gate refuses
> DONE-WHEN: a request matching an existing fm command's help text gets the note
> T-0255: FEATURE: inconclusive evidence — fm task evidence --inconclusive records a run that neither proves nor disproves; it never counts as passing and fm next asks for a sharper check
> CONTEXT: plugin/lib/fmresearch.py (claims, verify, note); budgets from fm budget; foreman-ui shows the note's agreement and conflicts
> CONTEXT: plugin/lib/fmcli.py cmd_audit, fmplugins skill index (T-0205), references/audit.md
> CONTEXT: plugin/lib/fmbench.py build/validate need tests today; fmideas.taste for preferences
> CONTEXT: fm audit prep briefs (T-0216 split), foreman:fm-reviewer agent, fm research add for replies
> CONTEXT: L plans get only a self-critique today (references/planning.md); child pattern from fmideas; budget from fm budget
> CONTEXT: fm lane (fmlanes.py) makes worktrees with their own active task; fm run --parallel merges lanes; the delegation reference says the main thread does all edits — this adds a bounded exception
> CONTEXT: fm friction digests ledgers; transcripts under ~/.claude/projects; capture --source self
> CONTEXT: fm run/serve (systemd user units, guard category system/remote), fm evolve, fm bench, economy mode usage windows
> CONTEXT: research/harness-landscape-20261003.md; fmresearch
> CONTEXT: stdlib urllib to PyPI/npm/crates JSON APIs (public https only, like fmresearch.fetch)
> CONTEXT: fmresearch.fetch/verify
> CONTEXT: fm bench run uses --setting-sources project,local and --plugin-dir; a second --plugin-dir adds the contender
> CONTEXT: fm evolve's HEAD worktree helper (fmbench._worktree); fm bench gate
> CONTEXT: fmideas.taste (steers, corrections, drops); bench judge
> CONTEXT: fmbench replay machinery, fmideas.taste
> CONTEXT: bench replay machinery; the README
> CONTEXT: stdlib JSON-RPC over stdio; registering an MCP server is guard category plugin (user's yes)
> CONTEXT: fm cost counts next followed/ignored (fmcost.py)
> CONTEXT: corrections in the ledger (fmideas.taste), PreToolUse notes in fmhooks
> DONE-WHEN: stubbed researchers that disagree produce a note with the conflict flagged, and a single-source claim marked as such
> DONE-WHEN: with a fake installed security skill, audit prep's brief and output name it for the adversary lens
> DONE-WHEN: a docs-only finished task becomes a judged case and a stubbed judge's score lands in the results and in fm bench show
> DONE-WHEN: audit prep --debate writes a rebuttal brief that embeds the first review and the output says how to run it; references/audit.md documents it
> DONE-WHEN: with a stub, fm plan-review writes a Plan review section with objections and a verdict line
> DONE-WHEN: the agent file exists with a lane-only contract, fm lane gives a builder brief, and delegate.md documents when and how to merge
> DONE-WHEN: with a stub, a session start after a session with an unanswered request captures it as a self item, once
> DONE-WHEN: fm night --dry-run lists what it would run within the budget and refuses when usage is above the threshold
> DONE-WHEN: with stubbed research, fm landscape writes a dated note and a diff against the previous one
> DONE-WHEN: with a fake registry response, fm deps lists an outdated major and offers the migration research
> DONE-WHEN: a second verify of the same URL the same day reads the cache; a two-question file yields two notes
> DONE-WHEN: with a stub, fm bench duel records both arms and prints the gate between them
> DONE-WHEN: fm bench versions REV runs both arms and prints the gate
> DONE-WHEN: fm bench court builds judged cases from recorded steers and runs them on a plugin
> DONE-WHEN: with stubs, fm bench soak runs a two-turn conversation and records the user-child's complaints
> DONE-WHEN: with a stub, fm bench stranger records the session's guard blocks and failed fm calls as findings
> DONE-WHEN: an initialize + tools/list + tools/call round trip over stdio returns the state
> DONE-WHEN: fm export agents writes a file under a size cap with those sections
> DONE-WHEN: a decision with a path trigger shows in fm next after that file changes
> DONE-WHEN: a two-file diff where one imports the other lists the imported one first
> DONE-WHEN: fm proof on a finished task prints those sections
> DONE-WHEN: after N ignored hints of one kind the injected Next line drops that hint's detail
> DONE-WHEN: after a recorded "never push without asking" correction, a git push command gets the note
> DONE-WHEN: fmplugins and cmd_audit read the JSON and fm evolve accepts it as a target
> DONE-WHEN: a recorded surprise appears in fm friction's digest and in recall for a related query
> DONE-WHEN: fm task assume/verify set the tags and done warns on unverified assumptions in M/L
> DONE-WHEN: an inconclusive run leaves the step open and the done gate refuses
> DONE-WHEN: a request matching an existing fm command's help text gets the note
## Interpretation
Do T-0253, T-0254, T-0255 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0260.
## Assumptions (confidence)
## Acceptance criteria
- [ ] T-0253: stubbed researchers that disagree produce a note with the conflict flagged, and a single-source claim marked as such
- [ ] T-0253: with a fake installed security skill, audit prep's brief and output name it for the adversary lens
- [ ] T-0253: a docs-only finished task becomes a judged case and a stubbed judge's score lands in the results and in fm bench show
- [ ] T-0253: audit prep --debate writes a rebuttal brief that embeds the first review and the output says how to run it; references/audit.md documents it
- [ ] T-0253: with a stub, fm plan-review writes a Plan review section with objections and a verdict line
- [ ] T-0253: the agent file exists with a lane-only contract, fm lane gives a builder brief, and delegate.md documents when and how to merge
- [ ] T-0253: with a stub, a session start after a session with an unanswered request captures it as a self item, once
- [ ] T-0253: fm night --dry-run lists what it would run within the budget and refuses when usage is above the threshold
- [ ] T-0253: with stubbed research, fm landscape writes a dated note and a diff against the previous one
- [ ] T-0253: with a fake registry response, fm deps lists an outdated major and offers the migration research
- [ ] T-0253: a second verify of the same URL the same day reads the cache; a two-question file yields two notes
- [ ] T-0253: with a stub, fm bench duel records both arms and prints the gate between them
- [ ] T-0253: fm bench versions REV runs both arms and prints the gate
- [ ] T-0253: fm bench court builds judged cases from recorded steers and runs them on a plugin
- [ ] T-0253: with stubs, fm bench soak runs a two-turn conversation and records the user-child's complaints
- [ ] T-0253: with a stub, fm bench stranger records the session's guard blocks and failed fm calls as findings
- [ ] T-0253: an initialize + tools/list + tools/call round trip over stdio returns the state
- [ ] T-0253: fm export agents writes a file under a size cap with those sections
- [ ] T-0253: a decision with a path trigger shows in fm next after that file changes
- [ ] T-0253: a two-file diff where one imports the other lists the imported one first
- [ ] T-0253: fm proof on a finished task prints those sections
- [ ] T-0253: after N ignored hints of one kind the injected Next line drops that hint's detail
- [ ] T-0253: after a recorded "never push without asking" correction, a git push command gets the note
- [ ] T-0253: fmplugins and cmd_audit read the JSON and fm evolve accepts it as a target
- [ ] T-0253: a recorded surprise appears in fm friction's digest and in recall for a related query
- [ ] T-0253: fm task assume/verify set the tags and done warns on unverified assumptions in M/L
- [ ] T-0253: an inconclusive run leaves the step open and the done gate refuses
- [ ] T-0253: a request matching an existing fm command's help text gets the note
- [ ] T-0254: stubbed researchers that disagree produce a note with the conflict flagged, and a single-source claim marked as such
- [ ] T-0254: with a fake installed security skill, audit prep's brief and output name it for the adversary lens
- [ ] T-0254: a docs-only finished task becomes a judged case and a stubbed judge's score lands in the results and in fm bench show
- [ ] T-0254: audit prep --debate writes a rebuttal brief that embeds the first review and the output says how to run it; references/audit.md documents it
- [ ] T-0254: with a stub, fm plan-review writes a Plan review section with objections and a verdict line
- [ ] T-0254: the agent file exists with a lane-only contract, fm lane gives a builder brief, and delegate.md documents when and how to merge
- [ ] T-0254: with a stub, a session start after a session with an unanswered request captures it as a self item, once
- [ ] T-0254: fm night --dry-run lists what it would run within the budget and refuses when usage is above the threshold
- [ ] T-0254: with stubbed research, fm landscape writes a dated note and a diff against the previous one
- [ ] T-0254: with a fake registry response, fm deps lists an outdated major and offers the migration research
- [ ] T-0254: a second verify of the same URL the same day reads the cache; a two-question file yields two notes
- [ ] T-0254: with a stub, fm bench duel records both arms and prints the gate between them
- [ ] T-0254: fm bench versions REV runs both arms and prints the gate
- [ ] T-0254: fm bench court builds judged cases from recorded steers and runs them on a plugin
- [ ] T-0254: with stubs, fm bench soak runs a two-turn conversation and records the user-child's complaints
- [ ] T-0254: with a stub, fm bench stranger records the session's guard blocks and failed fm calls as findings
- [ ] T-0254: an initialize + tools/list + tools/call round trip over stdio returns the state
- [ ] T-0254: fm export agents writes a file under a size cap with those sections
- [ ] T-0254: a decision with a path trigger shows in fm next after that file changes
- [ ] T-0254: a two-file diff where one imports the other lists the imported one first
- [ ] T-0254: fm proof on a finished task prints those sections
- [ ] T-0254: after N ignored hints of one kind the injected Next line drops that hint's detail
- [ ] T-0254: after a recorded "never push without asking" correction, a git push command gets the note
- [ ] T-0254: fmplugins and cmd_audit read the JSON and fm evolve accepts it as a target
- [ ] T-0254: a recorded surprise appears in fm friction's digest and in recall for a related query
- [ ] T-0254: fm task assume/verify set the tags and done warns on unverified assumptions in M/L
- [ ] T-0254: an inconclusive run leaves the step open and the done gate refuses
- [ ] T-0254: a request matching an existing fm command's help text gets the note
- [ ] T-0255: stubbed researchers that disagree produce a note with the conflict flagged, and a single-source claim marked as such
- [ ] T-0255: with a fake installed security skill, audit prep's brief and output name it for the adversary lens
- [ ] T-0255: a docs-only finished task becomes a judged case and a stubbed judge's score lands in the results and in fm bench show
- [ ] T-0255: audit prep --debate writes a rebuttal brief that embeds the first review and the output says how to run it; references/audit.md documents it
- [ ] T-0255: with a stub, fm plan-review writes a Plan review section with objections and a verdict line
- [ ] T-0255: the agent file exists with a lane-only contract, fm lane gives a builder brief, and delegate.md documents when and how to merge
- [ ] T-0255: with a stub, a session start after a session with an unanswered request captures it as a self item, once
- [ ] T-0255: fm night --dry-run lists what it would run within the budget and refuses when usage is above the threshold
- [ ] T-0255: with stubbed research, fm landscape writes a dated note and a diff against the previous one
- [ ] T-0255: with a fake registry response, fm deps lists an outdated major and offers the migration research
- [ ] T-0255: a second verify of the same URL the same day reads the cache; a two-question file yields two notes
- [ ] T-0255: with a stub, fm bench duel records both arms and prints the gate between them
- [ ] T-0255: fm bench versions REV runs both arms and prints the gate
- [ ] T-0255: fm bench court builds judged cases from recorded steers and runs them on a plugin
- [ ] T-0255: with stubs, fm bench soak runs a two-turn conversation and records the user-child's complaints
- [ ] T-0255: with a stub, fm bench stranger records the session's guard blocks and failed fm calls as findings
- [ ] T-0255: an initialize + tools/list + tools/call round trip over stdio returns the state
- [ ] T-0255: fm export agents writes a file under a size cap with those sections
- [ ] T-0255: a decision with a path trigger shows in fm next after that file changes
- [ ] T-0255: a two-file diff where one imports the other lists the imported one first
- [ ] T-0255: fm proof on a finished task prints those sections
- [ ] T-0255: after N ignored hints of one kind the injected Next line drops that hint's detail
- [ ] T-0255: after a recorded "never push without asking" correction, a git push command gets the note
- [ ] T-0255: fmplugins and cmd_audit read the JSON and fm evolve accepts it as a target
- [ ] T-0255: a recorded surprise appears in fm friction's digest and in recall for a related query
- [ ] T-0255: fm task assume/verify set the tags and done warns on unverified assumptions in M/L
- [ ] T-0255: an inconclusive run leaves the step open and the done gate refuses
- [ ] T-0255: a request matching an existing fm command's help text gets the note
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] T-0253: Surprise log — fm surprise "<expected> → <observed>" records where the model of the code w  <- CURRENT
2. [ ] T-0254: Assumed vs verified facts — the brief's Assumptions lines carry [assumed] or [verified: <e
3. [ ] T-0255: Inconclusive evidence — fm task evidence --inconclusive records a run that neither proves
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-04T05:50:48Z created
- 2026-10-04T05:51:02Z dropped: rebuilt: members' requests carried every item's criteria (pre-T-0259 intake); cleaning them first
## Follow-ups captured
