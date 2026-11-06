# Brainstorm — lens: research and web information finding

- **Decompose research into a question tree before fm-recon runs** — FEATURE — value 4 — effort M — risk low — category: research
  Why: the pack notes fm-recon gets "a self-contained brief" but there is "no research plan/question decomposition". `fm research plan NAME` would store 3–6 sub-questions, each with a stop condition (what answer ends it) and a source type (code, docs, web). The brief is cut into one recon pass per cluster, never open-ended.
  Done when: `fm research plan X` writes sub-questions with stop conditions to the research file, and `fm research add --from-agent` fails if any sub-question has neither an answer nor a "not found" mark.

- **Add a fetched-page cache keyed by URL and date** — PERFORMANCE — value 4 — effort M — risk low — category: research cache
  Why: "no cache of fetched pages". Usage-sensitive user, and recon passes re-fetch the same docs across tasks. A cache under the state dir holds a ≤2 KB extract per URL plus fetched-at. `fm research fetched URL` lets the next brief say "already read, 3 days old".
  Done when: a second recon brief naming a cached URL has the extract injected and the agent is told to skip the fetch; a test shows the cache hit.

- **Require two independent sources for web claims that gate a decision** — FEATURE — value 4 — effort S — risk low — category: source quality
  Why: "no cross-checking of web claims". `fm research add` parses each finding's confidence and citations, then flags any "high" finding with a single URL, or with two URLs on the same domain, as "single-source" in the saved file. The main thread's spot-check targets those first.
  Done when: a saved research file with a one-URL "high" finding shows a "single-source" marker, and `fm recall` output carries it.

- **Stamp research with a freshness class and re-check on reuse** — FEATURE — value 3 — effort S — risk low — category: freshness
  Why: "no notion of freshness"; the pack's "Stamp remembered facts with a source" idea covers memory, not web research. Each finding is tagged stable (language semantics), versioned (library API; stores the version string) or volatile (pricing, CLI flags). `fm recall` demotes volatile hits past a TTL and annotates versioned ones when the installed version differs.
  Done when: a volatile finding older than its TTL is returned by `fm recall` with a "stale" tag, and ranks below a fresh one.

- **Rank sources by tier in the recon brief** — FEATURE — value 3 — effort S — risk low — category: source quality
  Why: no source-quality ranking. A small table in fmplugins or a new fmresearch module maps domains to tiers: official docs and repo source first, issue trackers second, blogs and forums last. It is injected into the recon brief and used to order citations on save.
  Done when: the generated recon brief contains the tier order, and a saved file lists citations tier-first.

- **Search the repo and installed plugin docs before the web** — FEATURE — value 3 — effort M — risk low — category: research routing
  Why: the pack shows local `fm recall` and context7 exist but nothing orders them. `fm research route "<question>"` returns a cheapest-first ladder: recall hit, then context7 or `fm api`, then repo grep, then a web search. It stops at the first sufficient hit, which saves WebSearch tokens.
  Done when: for a question already answered in a past brief, `fm research route` returns the recall hit and no web step.

- **Add a "disconfirm" pass to research** — FEATURE — value 3 — effort S — risk low — category: research quality
  Why: recon reports "not checked" but never hunts for counter-evidence. For decision-bearing findings, a second fm-scout-priced query searches for "X deprecated", "X bug" or "X alternative". Results go in a "contrary evidence" section.
  Done when: a research file for a decision-tagged question has a "contrary evidence" section, even if it only says "none found, queries: …".

- **Wild: Keep a living per-project "knowledge base" of settled questions** — FEATURE — value 3 — effort M — risk med — category: research memory
  Why: assumption: research files pile up unmerged and conflict over time. A bounded `fm research digest` compiles them into one Q→A sheet with sources and dates, and flags contradictions between files. Intake reads the sheet first.
  Done when: two research files with opposite answers produce a "conflict" line in the digest.

- **Wild: Make fm-recon a two-model quorum for high-stakes questions** — FEATURE — value 2 — effort M — risk med — category: subagents
  Why: assumption: one Sonnet pass can hallucinate a citation. For security or irreversible-choice questions, a Haiku fm-scout re-fetches each cited URL and confirms the quoted claim appears in it. This is cite-checking at the URL level, which is cheap.
  Done when: a fabricated URL or quote planted in a test agent output is flagged "unverified" by the checker.

- **Wild: Add a "research debt" list that the idle drive works down** — FEATURE — value 3 — effort M — risk low — category: research autonomy
  Why: the user steered "recursive improvements… don't stop", and the standing preference is to finish the queue unattended. Every "not checked" item and every low-confidence finding becomes a queued micro-question. Drive spends leftover budget on them when economy mode is off.
  Done when: after a research add with 2 "not checked" items, `fm queue` shows 2 research-debt entries that disappear when answered.

- **Add a research eval set to catch regressions in fm-recon** — CLEAN — value 2 — effort M — risk low — category: evals
  Why: the pack says the evals cover 5 cases, none for research. Fixed questions with known answers and URLs (stored offline) score citation validity and "not checked" honesty, so changes to the recon prompt are measurable.
  Done when: `claude plugin eval` has a research case that fails when the recon agent's citation requirement is removed.
