# Ideas by round (deduplicated titles; details in the lens files)

## Round 1
- Decompose research into a question tree before fm-recon runs
- Add a fetched-page cache keyed by URL and date
- Require two independent sources for web claims that gate a decision
- Stamp research with a freshness class and re-check on reuse
- Rank sources by tier in the recon brief
- Search the repo and installed plugin docs before the web
- Add a "disconfirm" pass to research
- Wild: Keep a living per-project "knowledge base" of settled questions
- Wild: Make fm-recon a two-model quorum for high-stakes questions
- Wild: Add a "research debt" list that the idle drive works down
- Add a research eval set to catch regressions in fm-recon
- Add an implementation subagent that works only in a lane worktree and returns a patch
- Add a research planner that splits a question into sub-questions before fm-recon runs
- Add a cross-check agent that re-fetches the cited URL for each load-bearing web claim
- Give research notes freshness metadata and a source-quality tier
- Cache fetched pages by URL and date, shared by all recon agents
- Record which playbooks and subagents were used and whether the task closed cleanly
- Make a delegation router that chooses agent, model and scope from the step
- Wild: Add a debate pair of reviewer agents who must disagree before a verdict counts
- Wild: Let the main thread spawn a "future me" agent that writes the handoff and the outcome report from the transcript
- Wild: Add a "skill scout" subagent that reads a newly installed plugin and drafts its stage mapping
- Wild: Run a recon "red herring" self-check where a second recon is told the first one's answer is wrong
- Rank and cross-check web claims in research records
- Stamp research with fetch date and decay it in recall
- Add an fm-verifier subagent that re-fetches the two riskiest claims
- Make playbook loading measurable via a read marker
- Add a playbook "preflight question" header so agents skip irrelevant ones
- Reuse a repeated manual recipe as a draft playbook, with a yes/no
- Wild: Hold an adversarial research duel on contested findings
- Wild: Keep a local web page cache with a hit counter
- Wild: Hold a "gap-hunter" pass that reads a finished research record and lists what it did not ask
- Wild: Run a research "tournament" to pick a source-ranking heuristic from the user's accepted answers
- Add `fm research plan` with question decomposition and a stop rule
- Cache fetched pages with a freshness stamp
- Add an fm-skeptic subagent that attacks a research or root-cause conclusion
- Score each playbook by whether it was read and the task then passed first time
- Run evals as paired, repeated A/B with a variance floor
- Grow the eval set from finished tasks
- Add `fm research ask` as a recall-first escalation ladder
- Wild: Hold a research tournament on L unknowns
- Wild: Let Foreman write a playbook from a solved task by yes/no
- Wild: Keep a "known unknowns" shelf that research fills when idle

## Deepened: research
- Make `fm research` a single verb: ask → plan → run → record
- Tag each claim in research notes with source tier, date and verify status
- Spot-check web claims mechanically with a quote-anchor requirement
- Auto-trigger research on repeated failures and unknown-library errors
- Wild: Run a "premortem" recon that argues the leading answer is wrong
- Wild: Make research notes self-expiring tripwires tied to the files they influenced
- Wild: Make a "research diff" mode that re-runs an old note's queries and reports only what changed
- Measure research yield per note to tune the recon budget

## Deepened: self-improvement
- Log playbook reads and outcomes per task
- Retire or demote playbooks that never get read
- Route `fm next` by measured playbook lift
- Draft playbooks from repeated recipes and solved tasks, one merged flow
- Mine eval cases from finished tasks, with a variance floor
- Wild: Replay old tasks against a candidate change
- Make the improvement loop stop on its own evidence
- Wild: Let friction items auto-close when the fix lands
- Score lessons by whether recall changed an outcome
- Wild: Hold a research tournament over source-ranking rules
- Tag every self-change with a reversible changelog entry and a rollback check

## New ideas per lens
- research and web information finding: 11
- subagents and delegation: 11
- playbooks and procedures: 10
- recursive self-improvement: 10
