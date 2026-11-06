# Brainstorm — lens: research and knowledge

Lens: research and knowledge, meaning how Foreman finds out what is true, keeps it, and knows when it has gone stale. I read it as a lens of my own because it isn't one of the listed lenses. Ideas below skip the earlier items on provenance, known-unknowns, epistemic tags and dependency-source answers, and build on them instead.

- **Compile research claims into probes** — FEATURE — value 5 — effort M — risk low — category: research
  Why: the pack has "Answer from the installed dependency's source", "Store absence claims as re-runnable queries" and "Verify RESEARCH tasks by checking their claims", but no common unit. Assumption: recon reports are prose today. Each fact an fm-recon agent reports about an API or tool must come with a small executable probe (a REPL snippet, grep or `--help` check) and the version it was observed on. A dependency bump or a model change re-runs the probes and reopens any plan that rested on a failed one.
  Done when: a RESEARCH report without a probe for a load-bearing claim is rejected, and bumping a pinned dependency in a fixture re-runs the stored probes and flags the one that now fails.

- **Detect the knowledge-cutoff gap** — FEATURE — value 5 — effort S — risk low — category: freshness
  Why: the environment states a model cutoff of June 2026 and today is October 2026. Libraries released after the cutoff are exactly where recalled APIs are wrong, and T-0316 and T-0336 show harness surfaces shifting under Foreman. Assumption: version release dates can be read from lockfiles and registries. Compare each dependency's or tool's release date with the running model's cutoff. For anything newer, or with a major bump since, force a docs-or-source lookup before the first edit that uses it.
  Done when: in a fixture whose dependency is newer than the stated cutoff, the first edit using it is blocked until a lookup is recorded, and an older dependency is not blocked.

- **Search the user's own repos for prior art** — FEATURE — value 4 — effort M — risk low — category: recall
  Why: `fm recall` searches only the current project's briefs, and C078 covers cross-project requests but not solutions. The user runs many projects (`fm projects`). At intake for a FEATURE M/L, search the other registered projects' code and git history locally for similar solutions, and attach "you already solved this in X at path:line" to the build-vs-reuse record.
  Done when: a task in project B whose answer exists in project A lists that file in its brief's prior-art line, with nothing sent off the machine.

- **Fingerprint failures and look them up upstream** — FEATURE — value 4 — effort M — risk med — category: debugging
  Why: fm-debugger ranks hypotheses from local evidence only, and "3 failed attempts → block" suggests some failures were already solved publicly. Normalise the error or stack trace into a fingerprint and search the dependency's issue tracker and changelog. Rank hits as suspects with a link and a grade. This sends text out, so redact first and make it an explicit setting.
  Done when: a seeded known upstream bug in a fixture surfaces as a ranked suspect in `fm task hypo`, and the redaction check shows no path or secret leaves.

- **Map release notes onto call sites** — FEATURE — value 4 — effort M — risk low — category: dependencies
  Why: "Automate dependency upgrades" and "Turn Claude Code releases into adaptation tasks" exist, but the core step doesn't: reading the notes and finding which of our usages each breaking change touches. A research agent extracts breaking changes between two versions, greps for affected symbols, and writes a brief listing only the affected sites, each with a proposed edit.
  Done when: for a fixture upgrade with three breaking changes, one of which is irrelevant, the brief lists exactly the two real call-site groups.

- **Keep a source reliability ledger** — FEATURE — value 3 — effort S — risk low — category: research
  Why: the pack grades sources but never learns which ones were wrong. Record which source (docs site, blog, issue thread, README) a claim came from and whether its probe later held. Rank future lookups with that record and warn "this docs page was wrong twice here".
  Done when: after a seeded wrong-docs claim fails its probe, the next recon report on the same domain carries a lowered-trust note.

- **Check citations mechanically** — FIX — value 4 — effort S — risk low — category: answers
  Why: the user asks questions as well as giving commands, and the pack has side-question lanes and plain-language interrogation of project memory. Every `file:line` in a research answer or done summary gets verified: the line exists, and a cheap Haiku pass says whether it supports the sentence. Mismatches are flagged before the answer is shown.
  Done when: a fabricated or shifted line number in a sample answer is caught and the answer is shown with that citation marked unverified.

- **Check the docs against reality** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: "Turn the claims in MASTER.md into executable checks" is for Foreman only. Extend it to the user's projects and their dependencies: run the README's examples and commands in a throwaway worktree, and report which ones no longer work, as briefs for the user's own docs and as warnings about the dependency's docs.
  Done when: a README with one stale command yields exactly one doc-drift finding, and the run leaves no change in the working tree.

- **Compare prior art for FEATURE L** — FEATURE — value 4 — effort L — risk med — category: planning
  Why: C053 and "gate FEATURE L plans on a build-vs-reuse record" only check the local repo. A recon lane surveys the three to five best existing tools or libraries for the problem. It records licence, activity, API shape and the one feature each lacks, and the plan must say adopt, borrow or build with the reason. Assumption: network access is allowed for research.
  Done when: an L brief carries a prior-art table with a licence column and a decision line, and the done-gate rejects one that is missing.

- **Wild: Study dependencies at idle** — FEATURE — value 3 — effort M — risk low — category: idle-time
  Why: assumption: `fm night` and the drive already have idle cycles, and the first brainstorm covers pre-planning. Extend that to reading. An idle recon lane reads the source of the project's top-used dependencies and writes a dossier (hot paths, sharp edges, deprecated calls the repo uses, undocumented behaviour), pinned to the version. Builders and debuggers get the relevant page injected when they touch that dependency.
  Done when: after an idle run, a dependency dossier exists for the most-imported package, and a later task touching it has the matching page injected, shown in the ledger.

- **Wild: Run a curiosity engine on open questions** — FEATURE — value 4 — effort M — risk med — category: research
  Why: "Open a known-unknowns ledger" lists unknowns but nothing answers them. For each open unknown, pair the cheapest experiment that would settle it (a probe, a spike, a benchmark) with an estimated value. At idle, run the cheapest ones in a throwaway lane and close or sharpen the unknown, and a surprising result opens a new task.
  Done when: a seeded unknown with a runnable probe is answered unattended overnight, and the ledger shows the evidence and the plans it affects.

- **Wild: Duel rival researchers** — FEATURE — value 3 — effort M — risk low — category: debate
  Why: assumption: recon agents tend to confirm the first framing they get. For a contested technical question, two fm-recon agents are each assigned one answer and must find the strongest evidence for it. A judge scores only the evidence and writes what each side could not refute.
  Done when: on a question with a known answer in a fixture, the duel's verdict matches it and the report lists each side's strongest unrefuted point.

- **Wild: Compile the repo's tribal knowledge into a Q&A deck** — FEATURE — value 3 — effort M — risk low — category: onboarding
  Why: "Test the handbook with a cold-start agent" and "Interrogate the project's memory" cover testing and querying, but nothing teaches the user. Each week, build 5–10 questions from recent decisions, lessons and surprising diffs ("why does the guard allow X?"), and quiz the user on the ones they haven't read. Wrong answers reveal where their mental model of the project has drifted, and they are filed as notes or briefs.
  Done when: `fm quiz` produces questions that each cite a decision or lesson, and a wrong answer creates a captured note linking that source.
