# Brainstorm — lens: approaches

- **Distil the idea pile into a ranked epic roadmap** — FEATURE — value 5 — effort M — risk low — category: planning
  Why: Several hundred ideas already exist across rounds, with heavy overlap (red-team the guard, replay, lane fleets, and cleanup each appear 3-5 times). T-0432 is planned but nothing merges, ranks, or kills them. Without this, the brainstorm is a pile and not a plan.
  Done when: `fm ideas --distill` turns the ideas file into at most 12 epics. Each lists its merged members, its dependencies via `fm relate`, and a one-line kill reason for every dropped idea, and each epic is queued as a task.

- **Add a SPIKE task type with a discard guarantee** — FEATURE — value 4 — effort M — risk low — category: task types
  Why: Approach comparison is currently "race lanes", which is expensive and keeps the code. Assumption: cheap throwaway prototypes of L-sized ideas would settle many "is it feasible" questions, like T-0034 and T-0035 sitting deferred as L.
  Done when: `fm task new SPIKE` runs in a lane, its gate requires a findings note (works, cost, recommendation), and `fm lane rm` removes the code while the note stays in research/ and is returned by `fm recall`.

- **Gate FEATURE L plans on a build-vs-reuse record** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: The Foreman command list is already near 90 verbs, and the user keeps asking for less ("cleanup never got done"). Assumption: some planned features duplicate existing tools or plugins that `fm plugins` could find.
  Done when: an L-tier plan can't be approved until it records one searched existing option (plugin, package, or MCP server) and why it was or wasn't chosen, and `fm gates` shows that requirement.

- **Verify RESEARCH tasks by checking their claims** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: T-0316, T-0336, and T-0432 are RESEARCH tasks, and the done-gate evidence model is built for code. Assumption: research summaries currently close with no check that their claims match their sources.
  Done when: closing a RESEARCH task samples N claims from the saved summary, a separate agent re-fetches or re-reads each cited source, and any claim it can't confirm blocks done and is listed.

- **Open extension points for project-owned gates and lenses** — FEATURE — value 4 — effort L — risk med — category: extensibility
  Why: Mods exist only for the UI. JARVIS-type consumer projects keep needing project-specific checks (T-0275, the cleanup gates), which currently land in Foreman core and grow the guard surface.
  Done when: a project can drop a file in `.foreman/ext/` that defines a gate or review lens, `fm doctor` contract-tests it, and `fm gates` lists it with its source.

- **Promote guard rules from warn to enforce on replay evidence** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: Many recent asks are guard false-positives (T-0403, T-0404, symlink `rm`, `fm focus` in a chain), each found by a downstream project. `fm replay` already exists to measure rules against real commands.
  Done when: a new guard rule ships in log-only mode and flips to enforce automatically only after `fm replay` shows zero disagreements with real bash across the last N sessions. A rule that fails stays in log-only mode with a report.

- **Recall by meaning with a local index** — FEATURE — value 3 — effort M — risk low — category: recall
  Why: `fm recall` matches keywords, and the brief archive is large with similar wording across ideas and tasks. Assumption: local embeddings would find related past work that keyword search misses.
  Done when: `fm recall "<paraphrase>"` returns a brief whose text shares no keywords with the query. The index lives under the project, and no network call is made unless a setting enables one.

- **Answer questions about Foreman's own history** — FEATURE — value 3 — effort M — risk low — category: introspection
  Why: `fm why` and `fm digest` answer fixed questions only. Assumption: the user wants "why did T-0278 take so long" or "what did I decline about budgets" answered with citations.
  Done when: `fm explain "<question>"` answers from the ledger, briefs, and decisions, cites task and event ids for every sentence, and says "not recorded" instead of guessing.

- **Idea futures: bet on which ideas the user will keep** — FEATURE — value 3 — effort M — risk low — category: planning — wild
  Why: assumption: the taste data (kept, dropped, steered) is enough to forecast outcomes. Instead of ranking by gut, each idea carries a predicted keep-probability, and the score is settled when the task closes or is dropped.
  Done when: each distilled epic shows a keep-probability, and a digest shows the forecast's calibration (predicted versus actual) over the last 20 settled ideas.

- **Re-derive a finished task from its brief alone** — FEATURE — value 4 — effort L — risk med — category: verification — wild
  Why: assumption: briefs that can't regenerate their own behaviour are underspecified. A fresh agent in a lane builds from the brief only, and the diff against the shipped change exposes the hidden decisions.
  Done when: `fm audit rederive T-NNNN` runs the lane, runs the original gate on the result, and reports which behaviours the brief didn't determine.

- **Keep a graveyard of removed capabilities with resurrection tests** — CLEAN — value 3 — effort M — risk low — category: cleanup — wild
  Why: the user said cleanup requests never got done, and the likely reason is fear of deleting something needed. A graveyard records each removed thing, why it went, and the one check that would show it's missed, so deleting becomes reversible in a cheap way.
  Done when: removing a command or file under a CLEAN task writes a tombstone with a restore command, and a later task that re-adds a tombstoned name is warned with the original removal reason.
