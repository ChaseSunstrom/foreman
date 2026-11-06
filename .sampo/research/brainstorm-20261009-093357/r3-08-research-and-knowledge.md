# Brainstorm — lens: research and knowledge

- **Pin a verified-facts cache with expiry triggers** — FEATURE — value 4 — effort M — risk low — category: knowledge
  Why: Recon (fm-recon) re-derives the same repo and dependency facts per task; recall indexes briefs and lessons but not researched facts. Existing ideas cover "sources graded" and "absence claims as re-runnable queries" but not a shared fact store reusable across tasks. Assumption: recon outputs are currently free text in briefs.
  Done when: a recon fact stored with its probe command and the file hashes it read is served to a second task, and editing a read file marks it stale and reruns the probe.

- **Answer "how does X work here" with a cited walkthrough** — FEATURE — value 4 — effort M — risk low — category: research
  Why: Users steer toward questions as well as orders (intake has to split them); there is no read-only explain capability producing a path through code with file:line citations. Assumption: such questions currently go through the main thread unstructured.
  Done when: `fm explain "how does resume pick a step"` outputs an ordered trace where every claim cites file:line and a checker confirms each cited line exists and contains the named symbol.

- **Build a per-project glossary of internal terms from code and ledger** — FEATURE — value 3 — effort S — risk low — category: knowledge
  Why: Foreman's own vocabulary (lane, tripwire, veto, band, pane, drive) is dense; "learn the user's vocabulary" exists, but a code-derived glossary that builders and children get injected is not listed. Assumption: children lose terminology without it.
  Done when: `fm glossary` lists terms with definition, defining file, and usage count, and a brief containing a term gets its definition in the builder prompt.

- **Run a research-to-decision memo pipeline with a recommendation and an explicit "what would change it"** — FEATURE — value 4 — effort M — risk low — category: research
  Why: RESEARCH tasks exist (T-0316, T-0336) but are verified only by claim checks; the output shape is undefined. A fixed memo (question, options, evidence, recommendation, reversal trigger) would feed decisions with revisit triggers directly.
  Done when: finishing a RESEARCH task writes a memo file with all five sections and registers its reversal trigger as a decision tripwire.

- **Detect a stale-knowledge hazard before using a library API** — FEATURE — value 3 — effort M — risk low — category: knowledge
  Why: Model knowledge lags installed versions (Claude Code and harnesses change often; T-0316 is a re-check after an update). Existing "knowledge-cutoff gap" idea is a detector; this adds the action: compare the installed version's changelog against the call being written.
  Done when: editing a call into a dependency whose installed version is newer than a pinned knowledge date emits a one-line note citing the installed source signature.

- **Maintain a cross-project "how I solved X before" index across the user's repos** — FEATURE — value 4 — effort M — risk med — category: recall
  Why: User runs many projects (fm projects, cross-project requests T-0443); recall is per-project BM25. Prior-art search is listed for FEATURE L, but a standing local index of solved problems by project would make it instant. Assumption: central state already spans projects.
  Done when: `fm recall --all "retry with backoff"` returns hits labelled by project with the commit that landed them.

- **Score recall quality against the ledger** — CLEAN — value 3 — effort S — risk low — category: recall
  Why: fm recall is BM25 with no measurement of whether the right memory surfaced. Replaying past tasks as queries and checking if their own lessons rank top-5 gives a number to tune against.
  Done when: `fm recall --eval` prints recall@5 over finished tasks and fails the doctor gate below a set floor.

- **Wild: Keep a "known world" map of what Foreman has never looked at** — FEATURE — value 3 — effort M — risk low — category: knowledge
  Why: assumption: wild. A coverage heat map of files and docs ever read by any agent, so plans can say "this area is unexplored" and recon targets it first.
  Done when: `fm map --seen` shows per-directory read counts from the ledger and a plan touching a zero-read area gets a flagged assumption.

- **Wild: Hold a nightly "read the changelog of the world" job** — FEATURE — value 3 — effort M — risk med — category: research
  Why: assumption: wild. Overnight, fetch release notes for the harnesses and dependencies in use (opt-in, allowlisted hosts) and write briefs where a note names something the repo uses.
  Done when: with one allowlisted feed configured, a release note mentioning a used API produces a captured task citing the note line.

- **Wild: Interview the codebase's git blame authors' style from history** — FEATURE — value 2 — effort M — risk low — category: knowledge
  Why: assumption: wild. Mine commit messages and review reverts to extract "why we do it this way" rationale and attach it to files, supplying Chesterton-fence answers automatically.
  Done when: `fm why <file>` returns rationale sentences with commit hashes, and deletion tasks on that file cite them.

- **Wild: Give every lesson a footnote trail to the evidence that taught it** — FEATURE — value 3 — effort S — risk low — category: knowledge
  Why: lessons are recorded at finish, but there are many ideas about lifecycle and confidence; none make each lesson one hop from the originating ledger events and diff.
  Done when: `fm recall <lesson>` prints the source task, the failing evidence, and the fixing commit, and a lesson lacking them is flagged unsourced.

- **Compare tools in the space before building a FEATURE L** — FEATURE — value 3 — effort M — risk low — category: research
  Why: plan-time build-vs-reuse is in the queue (C053) but limited to Foreman's own modules; external comparison (existing CLI, library) is the "doing less" approach. Assumption: web access is available to recon.
  Done when: an L plan includes a table of at least two external alternatives with fetched-source citations and a recorded reason each was rejected.
