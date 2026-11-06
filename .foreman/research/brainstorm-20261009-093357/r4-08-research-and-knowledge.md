# Brainstorm — lens: research and knowledge

- **Pin each research answer to a re-runnable evidence recipe** — FEATURE — value 4 — effort M — risk low — category: research provenance
  Why: fm-recon returns prose findings, and "Verify RESEARCH tasks by checking their claims" and "Store absence claims as re-runnable queries" are listed only as separate pieces. Assumption: recon output has no uniform structure. A recipe per claim (command, file range, URL plus fetched hash) makes a finding refreshable instead of a memory.
  Done when: `fm recon` output carries a `claims[]` list where each claim has a runnable `recheck` command, and `fm research recheck <task>` replays them and reports which claims changed.

- **Build a question-first research plan before any reading** — FEATURE — value 4 — effort M — risk low — category: research planning
  Why: fm-recon is "bounded research", but the pack shows only "Decompose RESEARCH into a question tree" and "Open a known-unknowns ledger" as separate ideas, with no stop rule joining them. Assumption: recon currently starts by reading. Writing the decision the research serves, the 3–5 sub-questions, and what answer would change the decision gives the pass a defined end.
  Done when: a RESEARCH task cannot start recon until its brief holds a `decision:` line and sub-questions, and recon's return maps one finding to each sub-question or marks it unanswered.

- **Keep a project knowledge base of verified facts with dependency tags** — FEATURE — value 5 — effort L — risk med — category: knowledge base
  Why: fm recall is BM25 over briefs, lessons and failures, so it stores what happened, not what is true of the code. The same questions get re-researched ("how does X work here"). Each fact is stored with the files and versions it rests on, and is marked stale when they change (assumption: the tree hash is available from fm map).
  Done when: `fm know add "claim" --from path:lines` stores a fact, touching those lines marks it stale in `fm know list`, and recon consults it first and cites hits.

- **Check the installed dependency's behaviour with a throwaway probe before trusting docs** — FEATURE — value 4 — effort M — risk low — category: dependency truth
  Why: Foreman targets a fast-moving Claude Code, and T-0316, T-0336 and T-0337 are all blocked on "does the real harness behave as assumed". Docs and the model's memory can disagree with the installed version. A tiny sandboxed probe turns an assumption into an observation with the version stamped on it.
  Done when: `fm probe <lib> "<behaviour>"` runs a generated snippet in a temp dir with `python3 -I`, records output plus the version in the knowledge base, and a version bump re-queues it.

- **Run a "what is this question really asking" literature pass for RESEARCH asks that names prior art** — FEATURE — value 3 — effort M — risk low — category: prior art
  Why: the pack's idea list has "Compare tools in the space before building a FEATURE L" and "Compare prior art for FEATURE L", but both are single ideas with no shared output format. Assumption: the feature-vs-reuse record they feed is not yet built (T-0053-style build-vs-reuse line exists only as a plan requirement). Produce a comparison table (tool, capability, cost to adopt, what it lacks) that the build-vs-reuse line must cite.
  Done when: an FEATURE L plan fails its gate unless its build-vs-reuse line references a stored prior-art table with at least three entries.

- **Grade every research source and show the grade next to each claim** — FEATURE — value 3 — effort S — risk low — category: source quality
  Why: "Keep a source reliability ledger" and "answer from the installed dependency's source, with sources graded" appear separately. A fixed ladder (ran it, read the source, vendor docs, blog, memory) shown on each claim lets the main thread know how much to lean on it. Assumption: today recon returns undifferentiated confidence.
  Done when: every claim in a recon return carries a grade from the ladder, and a claim graded "memory" cannot be the sole basis of an accepted acceptance criterion.

- **Ask the research question twice from two framings and diff the answers** — FEATURE — value 3 — effort M — risk low — category: research reliability
  Why: "Sample a claim several times before trusting it" exists for claims, not for whole research briefs. Two recon children get the same question in different words (one given the hypothesis, one blind) and disagreements become the follow-up questions. Assumption: recon runs cost little relative to a wrong plan.
  Done when: `fm recon --twin` returns agreed findings and a list of divergences, and divergences are listed in the brief under open questions.

- **Wild: Keep a "known world" fog map of the codebase and docs** — FEATURE — value 3 — effort M — risk low — category: coverage — wild
  Why: assumption: Foreman has no model of which parts of the repo it has never opened. Track every file or doc read across sessions, and draw the unread parts as fog on the project map. Before an L plan, the fog over its footprint is shown, and recon is offered for the blank patches.
  Done when: `fm map --fog` lists files never read in any recorded session, and an L plan's footprint section reports what share of its files lie in fog.

- **Wild: Hold a nightly "read the world's changelog" job** — FEATURE — value 4 — effort M — risk med — category: staleness — wild
  Why: the user is on a harness that changes often, and "Turn Claude Code releases into adaptation tasks" is only one source. Broaden it to the changelogs and releases of every dependency in the user's repos. The scout reads each, matches entries to call sites the project uses, and files a brief only for those that hit. Assumption: network access is allowed by a setting, off by default.
  Done when: with the setting on, `fm night` writes a digest listing new upstream releases, with each entry mapped to a file:line call site or marked "no hit".

- **Wild: Grow a "questions I had to look up" deck from the ledger** — FEATURE — value 3 — effort M — risk low — category: learning — wild
  Why: the same lookups recur. Mine every recon and scout call for the questions asked and the answers found, cluster repeats, and offer the top ones as one-line cards the model sees at session start (budget capped). Assumption: ledger entries record the question text.
  Done when: `fm know deck` shows the top repeated lookups with counts, and a repeated question in a new session is answered from the deck without a recon call.

- **Wild: Interview the user's own repos for prior solutions before researching outward** — FEATURE — value 4 — effort M — risk low — category: prior art, cross-project
  Why: "Search the user's own repos for prior art" is listed, but not as the mandatory first step of research. The user has many projects (fm projects exists), and a solved look-alike is cheaper than any web search. Assumption: the repos are local and indexable by fm map.
  Done when: any recon starts with a local multi-project search whose hits (project, path, commit) appear at the top of the return, ahead of outside sources.

- **Write a decision memo with "what would change this" from each research pass** — FEATURE — value 4 — effort S — risk low — category: research to decision
  Why: research output feeds decisions (fm decide, with revisit triggers) but the link is manual. Assumption: the memo is written by the main thread today, if at all. The memo has recommendation, rejected options with the evidence against each, and one concrete trigger that would reverse it, auto-registered as a decision tripwire.
  Done when: finishing a RESEARCH task produces an `fm decide` entry with a revisit trigger copied from the memo, and the trigger fires in a test when its watched condition changes.

- **Detect the knowledge-cutoff gap on API use and force a look-up** — FEATURE — value 4 — effort M — risk low — category: staleness
  Why: the pack lists "Detect the knowledge-cutoff gap" and "Detect hallucinated APIs at edit time" separately. Combine: when an edit calls a library symbol whose installed version is newer than the model's likely knowledge, or that doesn't resolve, the sentinel asks the scout to read the installed source for it and attaches the signature. Assumption: version and symbol resolution is feasible for Python and TS.
  Done when: editing in a call to a nonexistent symbol in an installed package yields a note with the real signature (or "not found") before the next tool call, tested with a fixture package.

- **Wild: Hold a monthly "what do I believe that is probably false" audit** — FEATURE — value 3 — effort M — risk low — category: belief hygiene — wild
  Why: facts, lessons and decisions accumulate with no check that they still hold. Sample the oldest, most-cited items, generate a one-command test for each, run them, and list the ones that fail or can't be tested. Assumption: the knowledge base above exists, or lessons carry enough text to derive a test.
  Done when: `fm know audit` samples N entries, runs their rechecks, and files a task for each failed or untestable one.
