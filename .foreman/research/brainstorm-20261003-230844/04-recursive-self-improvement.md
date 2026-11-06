# Brainstorm — lens: recursive self-improvement

- **Add `fm research plan` with question decomposition and a stop rule** — FEATURE — value 5 — effort M — risk low — category: research
  Why: the user steered twice toward research and web search; fm-recon takes one self-contained brief and has no question tree. Pack states "no research plan/question decomposition". Plan = 3–6 sub-questions, each with a source type and "answered when" test, stored in the research file.
  Done when: `fm research plan NAME` writes sub-questions with a status per item, and `fm research add --from-agent` marks which were answered and which remain open.

- **Rank and cross-check web claims in fm-recon output** — FEATURE — value 5 — effort M — risk low — category: research
  Why: pack says "no source-quality ranking, no cross-checking of web claims". Tag every finding with a source tier (primary docs, repo, forum, blog) and require two independent sources for any claim marked high confidence; `research add` rejects high-confidence findings with a single source.
  Done when: a fixture agent output with one high-confidence finding citing one URL is downgraded or rejected by `fm research add`.

- **Cache fetched pages with a freshness stamp** — PERFORMANCE — value 4 — effort S — risk low — category: research
  Why: pack says "no cache of fetched pages, no notion of freshness". Usage-sensitive user pays tokens again for repeat fetches. Store the extracted text under a URL hash with a fetch date; `fm recall` indexes it and flags hits older than N days. Assumption: WebFetch results can be saved through `fm research add` (the agent can't write files itself).
  Done when: a second `fm research` lookup of the same URL is answered from the cache, and `fm recall` shows the age of a stale hit.

- **Add an fm-skeptic subagent that attacks a research or root-cause conclusion** — FEATURE — value 4 — effort S — risk low — category: subagents
  Why: only recon, reviewer and scout exist; reviewers audit diffs, none challenge findings. A read-only Sonnet agent given only the conclusion and its citations tries to falsify it and lists the checks that would settle it. Bounded to one pass, run only for L tasks or when the user asks.
  Done when: `agents/fm-skeptic.md` exists, `fm doctor` lists it, and the delegation policy names the trigger.

- **Score each playbook by whether it was read and the task then passed first time** — FEATURE — value 4 — effort M — risk low — category: self-improvement
  Why: pack says "playbooks are not measured" and 46 were never read. Log the reference named by `fm next` per task, whether the transcript Read it, and the outcome (gate failures, rework). A weekly line in the friction digest ranks playbooks, with an on-demand cut for those never read.
  Done when: `fm friction` prints a per-playbook table with reads and outcomes drawn from at least one real task.

- **Run evals as paired, repeated A/B with a variance floor** — FEATURE — value 4 — effort M — risk med — category: self-improvement
  Why: `/foreman:improve` compares with 5 single-run, noisy evals. Run baseline and candidate on the same cases N times; accept only if the delta exceeds the baseline's own spread. Without this the "recursive improvement" the user keeps asking for can't tell progress from noise.
  Done when: the improve flow reports mean and spread per case for both builds and refuses a merge when the difference is inside the spread.

- **Grow the eval set from finished tasks** — FEATURE — value 4 — effort M — risk low — category: self-improvement
  Why: only 5 eval cases exist while hundreds of real briefs with verify commands sit in state. Promote a brief (request, criteria, verify command) to an eval case by yes/no, with secrets redacted. Assumption: the evals runner accepts a case directory format.
  Done when: `fm evals add T-NNNN` produces a runnable case and `claude plugin eval` executes it.

- **Add `fm research ask` as a recall-first escalation ladder** — FEATURE — value 4 — effort M — risk low — category: research
  Why: recall, context7, recon and web are separate tools the model must choose among. One entry point tries `fm recall` (fresh hits stop), then context7, then a recon brief, and records which rung answered. This saves tokens by ending at the cheapest rung.
  Done when: asking a question already answered in a past research file returns it with no subagent spawned, and the rung used is logged.

- **Wild: Hold a research tournament on L unknowns** — FEATURE — value 3 — effort L — risk med — category: subagents
  Why: assumption: the user wants "super AGI level" depth. Two recon agents get different framings of one question (supporting vs refuting); the main thread reconciles disagreements into the confidence list. It is gated to L tasks and costs two passes.
  Done when: `fm research duel NAME` produces one note listing agreed claims and disputed claims, each with sources.

- **Wild: Let Foreman write a playbook from a solved task by yes/no** — FEATURE — value 3 — effort M — risk low — category: self-improvement
  Why: the user said "playbooks, literally anything"; `fm repeats` finds repeated work but the ideas stop at queueing codemods. At task done, if the approach is reusable, draft a ≤30-line playbook from the brief's steps and lessons, then land it in `playbooks/` behind the plugin-category yes.
  Done when: finishing a flagged task offers a drafted playbook file, and acceptance adds it to the playbooks index.

- **Wild: Keep a "known unknowns" shelf that research fills when idle** — FEATURE — value 3 — effort M — risk low — category: research
  Why: tasks record "not checked" lists from fm-recon, which are then lost. Collect them per project into a shelf; when leftover weekly budget exists (economy mode already reads usage), run one bounded recon on the top item and save the answer to recall.
  Done when: `fm research shelf` lists carried-over open questions, and an idle pass moves one to answered with a citation.
