# Brainstorm — lens: bold bets

- **Record a failing run before fixing it** — FEATURE — value 5 — effort L — risk med — category: verification
  Why: assumption: FIX tasks today lean on reading code and a hypothesis ledger. Nothing captures what actually executed. Wrap the repro in strace, rr, coverage or py-spy and store the trace slice as evidence. The plan then cites the first divergent call, and "done" requires the same trace to go green.
  Done when: a FIX task with a failing repro stores a trace artifact, its brief cites a line from it, and `fm task done` refuses if the post-fix trace still contains that divergence.

- **Provision a throwaway product stack for smoke** — FEATURE — value 5 — effort L — risk med — category: product checking
  Why: `fm smoke` drives a web UI in a headless browser, and the user asked that Foreman "checks the product the way its user uses it". Assumption: many projects (like JARVIS) need a database, services or seed data before smoke can run. Infer the run recipe from compose files, Makefiles and READMEs, boot it in a disposable network namespace, seed synthetic data, and tear it down.
  Done when: on a repo with a compose file and no smoke config, `fm smoke --auto` boots the stack, loads the page and tears everything down, leaving no containers running.

- **Fuzz what the diff touched** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: the ideas list covers mutation proof and invariant mining but not generated inputs. Pick the changed functions from `fm impact`, synthesize property or fuzz tests (Hypothesis, cargo-fuzz, fast-check), run them for a time budget, and attach any crash as a red repro.
  Done when: introducing an off-by-one into a fixture function makes the done-gate's fuzz step fail with a minimized input, and the unmodified function passes.

- **Forecast file footprints to catch queue conflicts** — FEATURE — value 4 — effort M — risk low — category: orchestration
  Why: JARVIS hit a lane merge blocked by a dirty main checkout (T-0280 versus T-0278), and T-0166 and T-0214 plausibly edit the same files. The idea list has leases and a merge train, but nothing predicts overlap before a plan runs. Estimate each queued task's touched files from `fm impact`, the map and past similar diffs, and flag likely collisions so the drive can sequence or serialize them.
  Done when: for two queued tasks whose previous diffs overlapped, `fm relate` marks them "collision likely" and the drive does not start both as parallel lanes.

- **Mine a hidden-coupling graph from surprises and co-change** — FEATURE — value 4 — effort M — risk low — category: code knowledge
  Why: `fm surprise` logs where the model of the code was wrong, and git history shows files that change together. Join the two into a coupling graph. When Claude edits file A, the hook says "B and test C changed with this in 7 of the last 9 tasks, and 2 surprises involved it."
  Done when: editing a file with a known coupling emits a one-line warning naming the partner, and the warning is absent for files with no recorded coupling.

- **Score and improve how legible a repo is to agents** — FEATURE — value 4 — effort L — risk med — category: repo health
  Why: the ledger and transcripts already record repeated re-reads, surprises and slow gates per file. Compute a legibility score (rereads, surprises, token cost per edit) and open CLEAN tasks for the worst offenders: split a giant file, add a missing test link, document an entry point. Foreman then improves the repo for its own future work. This is a different goal from the existing "ratchet complexity" idea.
  Done when: `fm map --legibility` ranks files by score, and one generated CLEAN task measurably lowers the median tokens-per-task on that file in a later bench replay.

- **Transplant a fix to sibling code across projects** — FEATURE — value 4 — effort L — risk med — category: cross-project
  Why: the user's JARVIS and Foreman repos share patterns, and `fm recall` plus the opt-in share already link projects. When a FIX lands, search other registered projects for the same code shape (AST or semantic match) and queue a brief with the adapted patch as a suggestion, never an auto-edit.
  Done when: fixing a pattern in project A creates a queued brief in project B that cites A's commit and a proposed diff, and nothing is edited in B.

- **Add discipline packs for non-code deliverables** — FEATURE — value 4 — effort L — risk med — category: generalization
  Why: assumption: Foreman is code-centric, but classify, plan, evidence and resume apply equally to data analyses, notebooks, papers and docs. A pack defines its own evidence: notebook re-executes clean, figures regenerate from raw data, citations resolve, numbers match source tables.
  Done when: a task of type ANALYSIS in a notebook repo cannot be marked done until the notebook re-runs top to bottom and its stated headline numbers match the output.

- **Watch model quality with a weather report** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: the roadmap carries T-0316 (re-run a real lane after a Claude Code update) and the list has canary ideas, but these are one-off. Track first-pass rate, guard refusals per task and rework per model and Claude Code version, with changepoint detection. When a new version degrades, `fm digest` says so and suggests pinning.
  Done when: replaying a ledger with a synthetic drop in first-pass rate after a version change makes `fm digest` print a regression warning naming the version.

- **Coach the user's requests from rework statistics** — FEATURE — value 3 — effort S — risk low — category: user feedback
  Why: the user's terse requests ("There's new bug feedback", T-0317) sometimes need follow-up. Correlate request shape (missing repro, no target file, ambiguous scope) with rework or blocked outcomes, then give a one-line hint at capture time, such as "tasks like this needed a clarification 4 of 6 times: name the file".
  Done when: capturing a request matching a historically ambiguous shape prints a specific hint, and a well-formed one prints none.

- **Wild: Run two independent guards and treat disagreement as a bug** — FEATURE — value 5 — effort L — risk med — category: security
  Why: wild. The guard is Foreman's riskiest component, with tests against real bash and a 5000-command replay. N-version programming adds a second guard, written clean-room in another language from the spec only. Both judge every command, and any disagreement is logged as a corpus entry and resolved toward blocking.
  Done when: running the replay corpus through both guards yields a disagreement report, and a seeded bug in one guard shows up as a disagreement.

- **Wild: Film a release** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. `fm smoke` already drives the real product headlessly. Record that run as a short annotated video or GIF per release, covering only what the changelog says changed, and attach it to the release and `fm pr`. Reviewers and the user watch 20 seconds instead of reading a diff.
  Done when: `fm release` outputs a recording whose captions list the changelog entries, each shown on screen.

- **Wild: Pre-build both answers to a blocking ask** — FEATURE — value 3 — effort L — risk high — category: autonomy
  Why: wild. When an `fm ask` waits on the user, the session idles, and idleness is a repeated complaint ("nothing else to do"). Start both candidate branches in throwaway lanes while waiting. When the answer arrives, merge the winner and discard the other, so the user's yes costs no waiting.
  Done when: for an ask with two options, both lanes exist while it is pending, and after the answer the chosen lane is mergeable and the other is removed with nothing leaked into main.

- **Wild: Let Foreman interview a dead session** — FEATURE — value 3 — effort M — risk med — category: recovery
  Why: wild. Resume relies on the brief and checkpoint, but a crashed or compacted session holds knowledge nobody wrote down. Replay its transcript to a fresh model that is asked pointed questions ("what did you believe about X, what was unfinished"), and write the answers into the resume point with the sources cited.
  Done when: for a transcript with an unrecorded half-done edit, the generated resume point names the file and the intended next change, and a check against the transcript confirms it.
