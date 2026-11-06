# Brainstorm — lens: deepen: research

- **Make `fm research` a single verb: ask → plan → run → record** — FEATURE — value 5 — effort M — risk low — category: research
  Why: the pack's research category has plan, ask, cross-check, cache and freshness as separate ideas, and `fm research` today has only `add`. Combine them into one `fm research ask "Q"` that runs recall first, and answers from past notes if they are fresh. If not, it writes a question tree with a stop rule, dispatches recon, then saves the result in one call. This saves the main thread several turns per research task.
  Done when: `fm research ask "<Q>"` on a question already answered by a fresh note returns that note with zero recon spawns, and on a new question produces a saved note with a plan, sources and a freshness stamp.

- **Add a URL page cache keyed by URL+date, exposed through `fm fetch`** — PERFORMANCE — value 4 — effort M — risk low — category: research cache
  Why: the pack says there is no cache of fetched pages, and parallel recon agents refetch the same docs. A stdlib file cache under `~/.claude/foreman/cache` holds body hash, fetch date and ETag. Recon fetches a page through the cache, and the cross-check agent reuses it. This saves tokens and time. Assumption: WebFetch can't be intercepted, so recon briefs must route through a Bash `fm fetch`, which needs a guard allowance.
  Done when: fetching the same URL twice within the TTL makes one network call, and the second result says "cached <date>".

- **Tag each claim in research notes with source tier, date and verify status** — FEATURE — value 4 — effort S — risk low — category: research quality
  Why: the pack says there is no source-quality ranking or freshness. Change the fm-recon output format to one line per claim: `claim | url | tier (primary/vendor/blog/forum) | date | confidence`. `fm research add` parses and warns on untiered load-bearing claims. `fm recall` can then downrank stale notes.
  Done when: `fm research add` rejects or warns on a note with a claim line missing tier or date, and `fm recall` output shows the age of each hit.

- **Spot-check web claims mechanically with a quote-anchor requirement** — SECURITY — value 4 — effort M — risk low — category: research verification
  Why: the main thread today spot-checks two claims by hand. Require recon to give a verbatim ≤20-word quote for each load-bearing claim. `fm research verify NOTE` then re-fetches via the cache and string-matches the quotes, with no LLM and no extra agent. This replaces the cross-check agent at near-zero token cost.
  Done when: a note with a fabricated quote fails `fm research verify` and one with real quotes passes.

- **Auto-trigger research on repeated failures and unknown-library errors** — FEATURE — value 4 — effort M — risk med — category: research triggers
  Why: after 3 failed attempts a step blocks with a diagnosis, and no research step is offered. Have `fm next` first run `fm recall` on the error text and then suggest a bounded recon. Cap it at one per task. Assumption: the error text is available from the hook's failed-tool record.
  Done when: a step with 2 failures of the same error yields a `fm next` line that cites recall hits or a research plan, once per task.

- **Wild: Run a "premortem" recon that argues the leading answer is wrong** — FEATURE — value 3 — effort M — risk low — category: research adversarial
  Why: this builds on the red-herring idea. Instead of always running it, `fm research ask --deep` runs it only when the first note's confidence is below high or its sources are all one tier. It must find a counter-source, or it reports "none found" as a cited negative.
  Done when: `--deep` on a seeded wrong premise produces a note with a "counter-evidence" section that is non-empty or explicitly "none found" with the queries listed.

- **Wild: Keep a known-unknowns shelf that fills when usage is low** — FEATURE — value 3 — effort M — risk med — category: research idle
  Why: the pack gives the idea and the user's pattern of "don't stop". Gate it on the weekly-usage data that `fmcost` already has (economy mode). Only run below 50% weekly usage, 1 recon per idle window, 2 h minimum gap like the improve pass. Unknowns come from "not checked" lists in prior notes. The user is token-sensitive, so make it opt-in.
  Done when: with usage under the threshold and the shelf non-empty, one unknown is researched and the shelf shrinks. Over the threshold, nothing runs.

- **Wild: Make research notes self-expiring tripwires tied to the files they influenced** — FEATURE — value 3 — effort M — risk low — category: research freshness
  Why: `fm why FILE:LINE` already surfaces lessons. Record which research note informed which decision or task. When the note passes its TTL (say, a fast-moving API versus a stable RFC), `fm next` on a later task touching those files says "note X is stale, recheck". This makes freshness actionable, not only metadata.
  Done when: touching a file linked to an expired note makes `fm next` name the note and a recheck action once.

- **Wild: Make a "research diff" mode that re-runs an old note's queries and reports only what changed** — FEATURE — value 3 — effort M — risk low — category: research incremental
  Why: it builds on the cache and the stored question tree. `fm research refresh NOTE` re-fetches only expired sources, then diffs the claims and sends recon just the changed parts. This keeps output small and avoids rewriting whole notes, so it suits a token-sensitive user.
  Done when: refresh on an unchanged note spawns no agent and prints "no change"; on a changed source it prints only the changed claims.

- **Measure research yield per note to tune the recon budget** — CLEAN — value 3 — effort S — risk low — category: research metrics
  Why: the pack says playbooks and research are not measured. Log per `fm research add` the recon tokens (from `fmcost`), the number of later `fm recall` hits and the citing tasks. Show the yield in `fm friction`, so over-researching on low-yield topics gets flagged and the planner's stop rule can adapt.
  Done when: `fm friction` lists the notes with tokens spent versus later citations, and a note with zero citations after N tasks is flagged.
