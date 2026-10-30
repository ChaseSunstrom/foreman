# Seed — generation 1

Parent: gen-0.md (read it; this Seed never overrides a MUST or NEVER there). Inputs: gap-map.md (13 recon passes at
ae98159e), not-yet.md and coverage.md (both in this tower). No exam results yet: generation 1 builds the exam, so its
own scores are the baseline the next Seed beats.

## What this generation is for
Gen 0's cross-cutting finding is that Foreman *advises* and stops: the parts exist, the trigger and the closed loop
don't. Every Mission below is judged by one question: after it, does Foreman **act** on its own, in a repo it has
never seen, and **prove** it, where before it printed a hint? A Mission that only adds a report is tier 1–2 and goes
to the inbox.

## Standing rules (user steers, recorded with fm decide; every later Seed and Mission carries them)
1. **No idea is killed for ambition.** A failed spike gets at least two genuinely different approaches (different
   mechanism, not a retuned parameter). If all fail, the idea goes to `not-yet.md` (`fm genesis put not-yet.md`) with
   what blocked it, the approaches tried and the capability that would unblock it — never dropped. Every Seed re-reads
   not-yet.md and retries each item whose blocker a capability built since may have removed. Only proven harm or an
   exact duplicate removes an idea for good, and the reason is recorded in not-yet.md's "Removed" section.
2. **Coverage by grid, not by luck.** `coverage.md` rows are every capability area: the 13 of gen-0 §2 plus everything
   a best-in-class agent harness and Claude Code plugin could do, including onboarding, UX, docs, ecosystem,
   multi-user, observability, security, performance, portability. Columns are every surface (Claude Code, fm code,
   other agents, MCP, Desktop, site, CLI, headless/server) × every stage (find, understand, plan, build, verify, ship,
   operate, learn). Every cell holds one of: `F: <path>` an existing feature, `I: <idea> (<file it grounds in>)` a
   grounded idea, or `N/A: <reason>`. Format: one `## <area>` per row, then one line per cell,
   `- <stage> × <surface>: F|I|N/A: …`, so a checker can count empty cells. Every generation fills empty cells first.
3. **Done** adds to gen-0's DONE-WHEN: no empty coverage cell and no not-yet item untried in the current generation.
4. Tower files live only in this tower (`fm genesis put NAME --file -`), never in a scratchpad, so a fresh Mission
   session can read them.
5. **Weakness-finding uses signals Foreman didn't author.** Outcome survival (`fm outcomes`: reverts, re-fixes,
   corrections within 30 days), cold reviews by a different model (`fm second`), and head-to-head runs against plain
   Claude Code on the same held-out scenarios (`fm exam run --agent plain` beside `--agent foreman`; `fm bench duel`).
   Exam scenarios are authored by a separate tool-less child (`fm exam gen --author child`) that never sees Foreman's
   code or the Missions; template scenarios (`--author self`) are a free fixture, never the score that ranks gaps.
   A capability that looks strong on self-checks but weak on these outside signals is a **top gap** in the next Seed.

## Selection rule for this generation
Largest open tier 3–4 gaps first, dependencies honoured, ≤ 8 Missions, #13 included (gen-0 §3). The exam comes
first because every later Mission, critique and selection is graded by it; the coverage grid comes second because
every later Mission fills its cells.

| # | Mission file | Capabilities | Gaps closed (gap-map tier) | Depends on |
|---|---|---|---|---|
| 1 | mission-exam.md | #13 exam, #6 | multi-language exam generator with hidden keys and holdout (3); exam.jsonl scoring (3) | — |
| 2 | mission-genesis.md | #13 | coverage grid + empty-cell check (3); not-yet ledger retried per generation (3); tower orchestrator (4); gen-0 writer from a line or nothing (3); per-project spec (3); selection + lineage (3); drift + sweep (3); auto-start (3) | 1 |
| 3 | mission-initiative.md | #1 | project scout probes (3); finders (3); find → prove → fix pipeline (4); value ranking (3) | 1 |
| 4 | mission-finish.md | #4 | goal ledger (4); done vs stopped (4); clauses wired to Stop (3) | — |
| 5 | mission-thinking.md | #2, #8 | readings/approaches gate by tier (3); auto race by evidence (4); unsure → research trigger (3) | — |
| 6 | mission-tools.md | #5 | capability-miss trigger (4); build-test-use loop (3); install-grant queue (3) | — |
| 7 | mission-proof.md | #6, #10 | proof kinds for docs/infra/data/perf (3); unproven rollup (4) | 1 |
| 8 | mission-self.md | #7, #9, #11, #12, #3 | signal → fix loop (3); trigger table (4); model router (3); lean ratchet (3); prediction scored (4) | 1 |

**Mission 8 is overloaded.** If #3 anticipation or #11's trigger table don't get a full pass in it (their own exam
scenarios all passing, held-out included, and their completeness list met), the gen-1 critique hands each one to
gen 2 as its own Mission — it is never folded silently into "partly done".

## Every Mission carries these (do not restate gen-0; point to it)
- **Shape**: capability spec (from gen-0 §2), the gap-map rows it closes, the coverage cells it fills, exam scenarios
  with answer keys (≥ 9 per capability, so the held-out third is ≥ 3), 3+ approaches with the choice and why, tier
  3–4 share ≥ 70%, an `fm intake` block (L3), done-when.
- **Process**: `fm mission` for the pillars; `fm ideas --rounds 4 --deepen 3 --falsify --crossbreed --seen <earlier
  ideas.md>` with fitted lenses + inversion + sci-fi (2030 worked back) + self-modification + ≥ 2 invented lenses;
  first re-read not-yet.md for items in its area; tier 4 or uncertain → `fm lane new ID --spike`; two credible
  designs → `fm lane race`; tests red first; close with `fm task finish` and its audits.
- **Lean** (gen-0 §6): subtract as you add; hook p95, rules size and injected context may not grow. A new verb that
  replaces an old path removes the old path in the same task.
- **gen-0's MUSTs and NEVERs, verbatim** (quoted, never paraphrased: a paraphrase is drift):

MUST: full autonomy. Every decision through fm decide. Never ask me anything mid-run.
MUST: no spend cap on building and proving. Tokens go into Foreman's code and its tests, not into sweeping the outside world. Waiting out a usage limit is fine.
MUST: everything finishes completely. A capability is done only when it has its tests, its exam scenarios passing (§4), docs (MASTER.md, README where it belongs, CHANGELOG), a site page if it's user-facing, a pane/status surface if it has state, and it works on every surface it belongs on (Claude Code, fm code, other agents, Desktop).
MUST: unprompted actions stay local and reversible (a lane, a branch, a spike, a throwaway folder). Anything that leaves the machine needs its grant, so it goes into the final report.
NEVER: clone or sweep outside repos to brainstorm or to benchmark. Outside material is only allowed in the targeted form in §5.
NEVER: grant yourself anything or lower your own guard. Protected core gets a built, evaluated candidate in a worktree plus `fm ask ID core` at the end. Merging Foreman changes stays my call.

## Order of work
1 → 2 → 3, then 4–8 in that order, one at a time. After each Mission: its critique (gen-1/critique-<cap>.md: exam
scenarios closed vs planned, outside signals (fm outcomes, fm second, plain vs foreman on held-out), coverage cells filled, not-yet items added or retried, what failed, what the next Seed
should change). After all: selection against the exam, lineage.md, drift check against gen-0, completeness sweep
(§7, plus empty coverage cells and untried not-yet items), then gen 2's Seed — written by `fm genesis` itself (gen-0
§3: from generation 2 on, the feature writes the Seed).

## Retry and stop rules
- A step that fails with two genuinely different approaches → `fm decide` the diagnosis; the idea goes to
  not-yet.md with its blocker (standing rule 1), the task is blocked (not dropped), work moves on.
- A Mission whose exam scenarios can't pass because a part needs protected core → build the candidate in a worktree,
  queue `fm ask ID core`, count the scenario as "waiting on the user" (not closed) in the critique.
- Usage limits: wait them out; never trade a test or an exam scenario for tokens.
