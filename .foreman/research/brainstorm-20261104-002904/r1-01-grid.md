# Brainstorm — lens: grid

- **Turn spec examples into runnable criteria at plan time** — FEATURE — value 5 — effort M — risk med — category: meaning proof
  Cell: agent × CLI × missing. Why: meaning is the largest unproven class (599), and a spec's `input → output` examples are already near-executable. Done when: filing a task whose spec holds 3 fenced examples yields 3 `criterion:` lines, each a command plus an expected-output check, and `sampo task finish` lists each as proved, failed or unproven.

- **Label every close with a three-valued meaning verdict** — FEATURE — value 5 — effort S — risk low — category: unproven labels
  Cell: user × web UI × unclear. Why: the request says whatever can't be proven is labelled unproven, but a green close card still reads as fully proven. Done when: the web UI card and the `--json` close record show `meaning: proved|unproven|failed`, with a reason when unproven. A close with no criteria shows unproven, never blank.

- **Add a public-surface vocabulary lint** — SECURITY — value 4 — effort S — risk low — category: naming
  Cell: user × site/README × wrong. Why: the steers ban "jarvis" and Claude-as-orchestrator, and the Models section and scenes are public. Done when: a test over `site/`, `README.md` and the pane/TUI strings fails on a banned-term list (endpoint names, vendor model IDs, the user's hostnames, "Claude" in an orchestrator role). It passes on role words (planner, decider, embedder, "any agent"), and a planted `jarvis` makes it red.

- **Classify the 421 flagged doc claims by how they can be checked** — FEATURE — value 4 — effort M — risk low — category: docs
  Cell: agent × docs × unclear. Why: 421 docs flag claims no run has checked, and one blanket "unchecked" tells the user nothing. Done when: each claim gets a kind (command output, file exists, number from a reader, behaviour, opinion). `sampo docs claims` prints a count per kind, runs the mechanical kinds, and leaves the rest labelled unproven with the kind named.

- **Run example criteria in a scratch home under the guard** — SECURITY — value 4 — effort M — risk med — category: safe proof
  Cell: unattended × CLI × unsafe. Why: criteria lifted from specs and docs are untrusted text, and the drive would execute them unattended. Done when: every extracted criterion is classified by the Ward before it runs and executes with a scratch `HOME` and no network. A criterion containing `rm -rf ~` is refused and recorded as "refused", not "failed".

- **Mark proof results that timed out as unproven, not passed** — FIX — value 3 — effort S — risk low — category: slow proofs
  Cell: unattended × CLI × slow. Why: a slow criterion under a drive tick has to end as something, and a skipped one silently reading as pass defeats the mission. Done when: each criterion has a time cap, and a timeout records `unproven: timed out at Ns` in the close record and on the card.

- **Derive a counter-example for each spec example** — FEATURE — value 4 — effort M — risk med — category: meaning proof
  Cell: agent × CLI × wrong. Why: an example criterion that passes on any non-empty output proves little. Done when: for each example, a second criterion asserts that a mutated input does not produce the stated output. A stub that always prints the expected string fails the counter-example.

- **Hand an orchestrator-neutral criteria block to every harness** — FEATURE — value 3 — effort M — risk med — category: other agents
  Cell: other agents × hooks × missing. Why: the standing rule is that Sampo isn't Claude-specific, but plan-time criteria are only injected by Claude Code hooks. Done when: `sampo task criteria --md` emits the block that `AGENTS.md` and `GEMINI.md` are pointed at, and a Codex session sees the same criteria as a Claude one.

- **Add an Unproven shelf to the web UI** — FEATURE — value 4 — effort M — risk low — category: observability
  Cell: user × web UI × missing. Why: the gap counts (599, 421) exist only in a prompt. Done when: a page lists unproven counts by class, shaded the same way everywhere (a hatched "unproven" fill), with each row naming the command that would prove it.

- **Wild: Expire a verified doc claim when the code it cites changes** — FEATURE — value 4 — effort M — risk med — category: staleness — wild
  Cell: unattended × docs × wrong. Why: assumption: a claim proved once rots silently. Each proof records the files it read, and a commit touching them flips the claim back to unproven. Done when: editing a file a proved claim cites turns that claim unproven on the next sweep.

- **Wild: Have a cold child guess who the orchestrator is from the rendered site** — FEATURE — value 3 — effort S — risk low — category: naming — wild
  Cell: user × site × unclear. Why: a text lint can pass while the scene still implies a vendor. A tool-less child gets only the rendered text and alt text and must name the orchestrator; "any agent" passes. Done when: the exam fails on a page where the child names a vendor or a machine.

- **Wild: Record each mechanical doc claim as a dated terminal cast** — FEATURE — value 3 — effort L — risk med — category: docs — wild
  Cell: user × docs × unclear. Why: assumption: a recording with a date beats "verified" as evidence on the public site. Done when: a doc example links a cast replayable in a scratch home, and the claim's stamp shows its run date.

- **Make the pane's work bar show proved against unproven** — FEATURE — value 3 — effort S — risk low — category: ui
  Cell: user × pane × unclear. Why: the pane is where the user glances during a run. Done when: the bar shows a hatched segment for unproven criteria, in the same style as the web UI shelf, with an accessible text twin.

- **File criteria for unplanned drive tasks at pickup** — FIX — value 3 — effort S — risk low — category: coverage
  Cell: unattended × hooks × missing. Why: the drive picks up tasks that skipped plan time, so no criteria exist. Done when: a task with no criteria at `task start` gets them extracted then, or is marked "no criteria: unproven".

Cells left empty: user × CLI × slow (the hook bench already covers it), other agents × site (not applicable, they don't read it), and agent × pane × unsafe (read-only surface).

Next question: Which of the 599 meaning-class gaps have a spec example at all, and how many have only prose?
Next question: When a criterion is derived from a spec, who confirms the spec example itself is right?
