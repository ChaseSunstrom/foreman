# Brainstorm — lens: research and knowledge

- **Open a known-unknowns ledger before planning** — FEATURE — value 5 — effort M — risk low — category: planning
  Why: assumption: intake records assumptions with confidence but doesn't list what Foreman doesn't know. A ledger of open questions would each carry the cheapest way to resolve it (read, probe, run, ask) and a note on which plan decision it changes. Plans for M/L tasks wait on the blocking ones.
  Done when: `fm task plan` on an L task refuses to finalize while a ledger entry marked "blocks decision" is unresolved, and a resolved entry cites the command output that closed it.

- **Settle approaches with discriminating experiments** — FEATURE — value 5 — effort M — risk med — category: approach choice
  Why: the brief already requires 3+ options for M/L, but nothing says how to choose between them. Each option would get a "wins if…" condition and a cheap test (a spike, a grep count, a timing probe). Foreman runs those tests and picks on results, not on prose.
  Done when: a brief's chosen approach cites at least one experiment result that ruled out each rejected option, or says "not testable" with a reason.

- **Block deletion until the fence's origin is found (Chesterton gate)** — FEATURE — value 4 — effort M — risk low — category: research
  Why: the user's cleanup requests "never got done", and cleanup gates are on the idea list. Deleting or rewriting unfamiliar code is where cleanup goes wrong. The gate would auto-research blame, the commit message, any linked task and the tests that touch the code, then record why it exists before approving removal.
  Done when: a CLEAN task that deletes a function with no recorded origin is blocked at done. With an origin note attached (even "orphaned since commit X"), it passes.

- **Tag every claim with its epistemic status** — FEATURE — value 4 — effort S — risk low — category: reasoning
  Why: assumption: briefs, plans and done summaries mix things Foreman read, ran, inferred, remembered from training or guessed. Tagging each claim read/ran/inferred/remembered/assumed would let the done-gate and reviewers focus on the weak tags.
  Done when: `fm task done` lists counts per tag and flags any acceptance-relevant claim tagged "remembered" or "assumed" with no later upgrade.

- **Answer from the installed dependency's source, with sources graded** — FEATURE — value 4 — effort M — risk low — category: knowledge
  Why: assumption: models misremember library APIs and versions. A per-project local cache would be built from the lockfile: installed source, changelogs and docstrings, indexed for recon. Sources would be ranked (installed source, then official docs, then web, then model memory), and plan claims about APIs would cite the tier.
  Done when: asking recon "does X.foo take a timeout?" returns the answer with a file:line from the installed version, and a mismatch against the pinned version is reported.

- **Accumulate domain pitfall packs** — FEATURE — value 4 — effort M — risk low — category: knowledge
  Why: assumption: recurring domains (time zones, auth flows, file locking, Unicode, shell quoting) have well-known traps. When a task touches a domain, recon would write or load a short "ways this goes wrong" pack. Plan and review checks would be run against it, and packs grow from finished tasks' failures.
  Done when: a task touching timezone code gets a pitfall list in its plan, and at least one plan step or criterion addresses an item from it.

- **Route tasks to a named problem-solving method** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: Foreman has per-type skills but no catalogue of methods. The catalogue would cover bisect, minimal repro, characterization first, strangler, differential vs reference, spike, invariant-first and others, with a selector that matches task shape to method and records whether it paid off. Bench history would tune the selector.
  Done when: intake of "slow query regression" selects bisect plus profile, writes the method into the brief, and the finish record scores whether it was used.

- **Choose the next debugging probe by how well it splits the hypotheses** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: fm-debugger returns ranked hypotheses with probes. A hypothesis-by-evidence matrix would score each probe by how many hypotheses its outcomes eliminate, so the cheapest high-split probe runs first and each result prunes the matrix.
  Done when: a FIX with 4 hypotheses runs the probe with the highest split score first, and the ledger shows each probe's outcome and which hypotheses it ruled out.

- **Stop researching when the decision stops moving** — FEATURE — value 3 — effort S — risk low — category: research
  Why: fm-recon is bounded, but the bound is a budget, not a signal. After each finding, a cheap re-ask ("does the plan change?") would count consecutive no-change findings and end the research at a threshold, with a note on what was left unread.
  Done when: a recon run ends early with "decision stable after N findings" and lists the unexplored areas.

- **Split questions from orders at intake** — FIX — value 3 — effort S — risk low — category: understanding
  Why: assumption: "can it do X?" or "why does Y happen?" can be misread as a build order. The classifier would add a speech-act label (question, wish, order, complaint, exploration), and a question gets an answer, optionally followed by an offer to capture a task.
  Done when: "does the guard handle zsh -ic?" creates no task and answers with evidence, while "make the guard handle zsh -ic" creates a FEATURE.

- **Generate the worst plausible misreading (wild)** — FEATURE — value 4 — effort M — risk low — category: understanding
  Why: wild: at intake an adversary child writes the three most plausible wrong interpretations of the request and the diff each would produce. If the brief's interpretation can't be told apart from a wrong one by its acceptance criteria, Foreman adds a criterion or asks.
  Done when: a brief includes a "misreadings ruled out" section with at least one criterion tied to each.

- **Calibrate predictions to earn reading budget (wild)** — FEATURE — value 3 — effort M — risk low — category: reasoning
  Why: wild: before probing, Foreman states numeric predictions such as how many files the change touches or whether a test will fail. Its record shows how well they match. Good calibration lets it skip confirming reads on that kind of question, and poor calibration forces them.
  Done when: `fm friction` shows a calibration score per prediction type, and recon depth changes when the score crosses a threshold.

- **Rehearse the plan with the repo's past authors (wild)** — FEATURE — value 3 — effort L — risk med — category: knowledge
  Why: wild: for areas with deep history, a read-only child reconstructs the original design intent from blame, commit messages and old briefs. It then critiques the plan as that author would, flagging violated intentions before any edit is made.
  Done when: a plan touching a heavily-blamed module produces an "intent from history" note citing commits, and a reviewer can trace each objection to a specific commit.
