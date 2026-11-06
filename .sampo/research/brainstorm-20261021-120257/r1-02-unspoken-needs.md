# Brainstorm — lens: unspoken needs

- **Close sweeping mandates with a per-clause ledger** — FEATURE — value 5 — effort M — risk low — category: mandate
  Why: the user said "fully featured/implemented", "don't stop until complete" and "recursive until dry", but no check says when "complete" has been reached. Assumption: a clause-level stop is what lets them stop supervising.
  Done when: `fm mandate show` lists each clause of the verbatim request (six repos, "10x", "work with anything", "full management") with an evidence link or an open state, and the drive ends only when every row is closed or deferred with a reason.

- **Pin the six repos as an offline knowledge pack** — FEATURE — value 4 — effort M — risk low — category: knowledge
  Why: the user wants these repos integrated "automatically", and today every round re-researches them from the web. The pack would be sha-stamped excerpts of the READMEs, CHANGELOG, the marketplace.json schema and the SKILL.md spec, queried with `fm know "<q>"` and cited with sha.
  Done when: with the network off, `fm know "hook defer"` returns a cited excerpt with the repo sha, and `fm know --stale` flags a pack older than the pinned upstream sha.

- **Gate upstream imports by licence class** — SECURITY — value 4 — effort S — risk low — category: licence
  Why: the pack states mixed licences: docx/pdf/pptx/xlsx skills are source-available, financial-services is Apache-2.0, cookbooks are MIT, and the tutorial has no licence ("ideas only"). Nothing enforces that today. Assumption: ported text is currently unchecked.
  Done when: `fm upstream import` refuses a docx skill and the tutorial text, accepts an MIT cookbook snippet with an attribution line, and a test covers all three.

- **Import cookbook eval patterns as bench cases** — FEATURE — value 4 — effort M — risk med — category: bench
  Why: T-0866 and T-0867 are deferred because the bench has no real case corpus, and the cookbooks include "building evals" and outcome-grader patterns. Only MIT-licensed material would be used, rewritten as seeded-bug cases.
  Done when: `fm code bench --suite cookbook` runs at least 5 imported cases against one runner and writes a result file with per-case pass and cost.

- **Offer cookbook agent shapes as `fm code --shape`** — FEATURE — value 4 — effort L — risk med — category: fm code
  Why: the request is "10x better, work with anything". Evaluator-optimizer, orchestrator-workers and plan-big-execute-small are the named patterns, and `fm code` today has one fixed loop. Each shape would carry bench numbers so the user can choose by evidence.
  Done when: `fm code --shape evaluator-optimizer "<req>"` runs on a fake runner and logs distinct events for generator and critic turns, and bench results record the shape used.

- **Add an unknown escape and evidence quote to every slot prompt** — PERFORMANCE — value 4 — effort M — risk low — category: prompts
  Why: the tutorial's lessons (allow "unknown", quote evidence, XML-separate data from instructions, prefill) map directly onto the model-fills-one-small-JSON-slot design. The risk is that weak local models invent answers.
  Done when: a bench ablation on one local model shows a measured hallucinated-slot rate with and without each technique, and the winning set becomes the default.

- **Run a prompt-sensitivity exam on each runner** — FEATURE — value 3 — effort M — risk low — category: runners
  Why: runners differ in how they handle role framing, few-shot examples and format discipline. A 10-item exam of original exercises, written in the tutorial's spirit with no copied text, would pick the prompt tier per model.
  Done when: `fm code runners --exam` writes a per-runner prompt-tier record that `fm code` reads, and a rerun on an unchanged runner gives the same tier.

- **Trace a third-party plugin install in a throwaway HOME** — SECURITY — value 5 — effort M — risk med — category: supply chain
  Why: about half of the 166+ official-marketplace plugins are third-party, and the constraint is that third-party plugins run nothing unguarded. A dry install would record every file, hook, MCP server and command before the plugin is enabled.
  Done when: `fm plugins install --trace X` prints the added hooks and MCP servers, refuses on hook-event collision or an unguarded command, and leaves the real `~/.claude` untouched.

- **Keep an adopt/skip/later register for upstream features** — CLEAN — value 3 — effort S — risk low — category: scope
  Why: the user keeps getting the same ideas re-proposed, and dropped and steered items show they care about not repeating them. Each Claude Code feature would get a decision and a reason, and intake and brainstorm would read the register.
  Done when: the brainstorm pack builder drops any idea matching a "skip" row, and `fm upstream decisions` lists each row with its reason.

- **Lint Foreman's own skills against the Agent Skills spec** — FIX — value 3 — effort S — risk low — category: skills
  Why: the spec says name equals the folder, description at most 1024 characters, body under about 5k tokens, and about 100 tokens of metadata each. Foreman ships roughly 73 skills, and `fm doctor` does not check this. Assumption: some violations already exist.
  Done when: `fm doctor` fails a skill with a mismatched name or an over-long description, and it prints the total metadata token budget.

- **Wild: Add a numeric tie-out evidence kind for finance-style work** — FEATURE — value 3 — effort M — risk med — category: evidence
  Why: financial-services shows agents doing reconciliations, and Foreman's evidence is currently test-shaped only. A verify kind would assert that two sources reconcile within a tolerance, with both figures printed (wild).
  Done when: a task whose verify is `fm tieout a.csv b.csv --tol 0.01` fails with both totals shown, and passes once the totals match.

- **Wild: Run a nightly reading lane over upstream changelog entries** — FEATURE — value 4 — effort M — risk med — category: scout
  Why: the user said "I shouldn't even need to ask", and `fm scout` already watches Claude Code releases. A read-only lane would take one new entry per night and write an adopt, skip or later decision with a draft brief (wild).
  Done when: after a fake changelog entry is added, the next run produces a register row and a queued brief with no source edits.

- **Wild: Recommend plugins from the user's own friction** — FEATURE — value 3 — effort M — risk low — category: discovery
  Why: `fm plugins find` exists, but it matches keywords rather than the user's real complaints. It would rank marketplace entries against the stack card and recent friction phrases, showing the evidence for each match (wild).
  Done when: `fm plugins find --for-friction` lists at least one plugin with the quoted user phrase that triggered it, and nothing is installed without a yes.

- **Wild: Publish Foreman's skills as a pinned, marketplace-schema-valid feed** — FEATURE — value 3 — effort M — risk low — category: ecosystem
  Why: the official marketplace.json pins each plugin to a sha and supports git-subdir sources. Publishing in that shape lets others consume Foreman's guard and resume skills, and lets Foreman validate its own feed against the same rules it applies to others (wild).
  Done when: `fm plugins publish --dry-run` emits a marketplace.json whose entries each carry a sha and pass the same validator used for imports.
