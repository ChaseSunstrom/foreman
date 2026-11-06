# Brainstorm — lens: playbooks and procedures

- **Decompose research into a question tree before dispatch** — FEATURE — value 4 — effort M — risk low — category: research playbook
  Why: fm-recon gets one self-contained brief and returns ≤400 words; the pack lists "no research plan/question decomposition" and the user asked twice for better research. Add a `research/plan` playbook plus `fm research plan NAME` that writes 2–5 sub-questions, each with a stop condition ("two independent sources" or "primary doc found") and a "known already" line from `fm recall`. The main thread dispatches only unanswered leaves.
  Done when: `fm research plan X` on a question that `fm recall` already answers emits zero leaves for that part, and a test asserts the leaf file format.

- **Rank and cross-check web claims in research records** — FEATURE — value 4 — effort M — risk low — category: research quality
  Why: the pack says there is no source-quality ranking or cross-checking of web claims, and `fm research add` only stores text. Extend `--from-agent` parsing to require a per-claim `source tier` (primary/vendor/forum/unknown) and `corroborated: n`. `fm research add` warns when a load-bearing claim has one non-primary source.
  Done when: an agent file with a single-forum claim yields a one-line warning, and a corroborated primary claim yields none.

- **Stamp research with fetch date and decay it in recall** — FEATURE — value 3 — effort S — risk low — category: research freshness
  Why: the pack says there is no notion of freshness, and `fm recall` is BM25 over research. Add `fetched:` and `volatility: low|med|high` frontmatter, and have recall annotate hits older than a volatility-based age with "stale, recheck". This differs from the existing "demote stale recall hits" idea, which concerns lessons, not web facts.
  Done when: a research file with high volatility and an age of 90 days is listed as stale in `fm recall`.

- **Add an fm-verifier subagent that re-fetches the two riskiest claims** — FEATURE — value 3 — effort S — risk low — category: subagents
  Why: today the main thread spot-checks two claims itself, which spends main-context tokens. A Haiku-tier agent with WebFetch and Read only receives claim and URL pairs and returns confirmed/contradicted/unreachable. Add it to the delegation policy as a read-only agent.
  Done when: the agent file exists with the minimal tool list, the delegation policy names it, and `fm doctor` reports its tools as read-only.

- **Make playbook loading measurable via a read marker** — PERFORMANCE — value 4 — effort S — risk low — category: playbooks
  Why: the pack says playbooks are not measured and 46 are never read. Have the PostToolUse hook, which already sees Read events, append `playbook read: NAME` to the task's ledger. `fm doctor` then reports reads per playbook and the task outcome (reworked or not) beside it. This supplies the data for the existing ablation and pruning ideas.
  Done when: reading a playbook file inside a task adds a ledger line, and `fm doctor` lists a per-playbook count.

- **Add a playbook "preflight question" header so agents skip irrelevant ones** — PERFORMANCE — value 3 — effort S — risk low — category: playbooks
  Why: `/foreman:playbooks` is an 84-line index over 40 files, and `fm next` names one static procedure per task type. Give each file a one-line `use-when` and `skip-when` front matter, and have `fm next` print only that line plus the path. The agent reads the full file only when it matches.
  Done when: every playbook file has both lines, and a test fails if one is missing.

- **Reuse a repeated manual recipe as a draft playbook, with a yes/no** — FEATURE — value 3 — effort M — risk med — category: self-improvement
  Why: `fm repeats` finds repeated manual work, and the user wants "recursive improvements" and "playbooks, literally anything". Extend `fm repeats` to emit a playbook draft (steps, preconditions, verify) into a worktree. The user answers one yes/no, and nothing is written under `~/.claude` without it (`plugin` category guard).
  Done when: a run on fixture history with a repeated three-command sequence produces a draft playbook file in a worktree and no file under `~/.claude`.

- **Wild: Hold an adversarial research duel on contested findings** — FEATURE — value 3 — effort M — risk med — category: research subagents
  Why: assumption: a single fm-recon pass can be confidently wrong, and the user wants "super AGI level" research. For findings flagged load-bearing, run two fm-recon children, one told to support the claim and one to refute it, then keep only what survives. The cost is bounded by a flag that applies it only to claims that gate a decision.
  Done when: `fm research duel NAME` writes a record with both sides' citations and a survived/refuted verdict.

- **Wild: Keep a local web page cache with a hit counter** — FEATURE — value 3 — effort M — risk low — category: research cache
  Why: the pack says there is no cache of fetched pages. Store WebFetch results by URL hash in the state dir with a fetch date. Return a cache hit to fm-recon through a `fm fetch URL` wrapper, so a repeat lookup in a later session spends zero network and fewer tokens.
  Done when: a second `fm fetch` for the same URL within its TTL makes no network call, shown by a test that stubs the network.

- **Wild: Hold a "gap-hunter" pass that reads a finished research record and lists what it did not ask** — FEATURE — value 2 — effort S — risk low — category: research recursion
  Why: assumption: the user's "recursive improvements" means research that improves itself. A Haiku child with no tools reads the record and its "not checked" list, then proposes up to three follow-up questions. Those are queued as a research plan leaf only if `fm recall` has no answer.
  Done when: running it on a record with a non-empty "not checked" list yields at most three leaves, each tagged with its parent record.

- **Wild: Run a research "tournament" to pick a source-ranking heuristic from the user's accepted answers** — FEATURE — value 2 — effort L — risk med — category: self-improvement
  Why: assumption: the user will keep giving thumbs on research outputs. Record which source tiers the accepted answers relied on, then tune the tier weights per project with `fm friction` as the trigger. Weights change only through a worktree candidate gated by `claude plugin eval`.
  Done when: after fixture accept and reject records, a rerun changes the tier weights deterministically, and a test pins the result.
