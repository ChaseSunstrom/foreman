# Mission — Genesis as a feature (gen 1, #13)

Task: T-2093 (brief 1, fm genesis check), T-2095 (brief 2, fm genesis step), T-2099 (brief 3, fm genesis draft/spec), T-2102 (brief 4, fm genesis select/seed), T-2104 (brief 5, fm genesis drift/sweep). Briefs 6–8 are added here as they are intaken.

Self-contained for a fresh `fm run` in ~/.claude/foreman. Parent: gen-1/seed.md → gen-0.md §2 #13, §3.
Ideas: 606 from `fm ideas --rounds 4 --deepen 3 --falsify --crossbreed --seen` (brainstorm-20261029-233136), lenses
below; about 135 placed by tier after merging duplicates.

## Capability (gen-0 §2 #13)
`fm genesis` plus a skill: from one line, a sweeping request or nothing, it writes its own gen-0 for the project, runs
the whole tower (Seed → ≤ 8 Missions → briefs → critiques → selection → drift → sweep), writes the project's own
capability spec with a held-out exam, starts by itself when the queue runs dry or the gap map shows big gaps, and
carries over what a run learned. From gen 2 on, the feature writes the Seed.

## Lenses (pack: fitted + required + invented)
- Required: **inversion** (how Genesis fails or is abused: runs forever, rewrites rules toward easier exams, burns a
  week of usage, drifts from the user's MUSTs, grants itself something, overfits the held-out third); **sci-fi**
  (the 2030 self-writing harness, worked back to what Python and Foreman can do today); **self-modification** (Genesis
  improving its templates, exam, lenses and selection rule, each change measured, reversible and inside the NEVERs).
- Invented: **cold-start stranger** (a repo never seen, no history, one line or nothing: what the first ten minutes
  write and get wrong); **tower archaeology** (a fresh session opens a three-generation tower with no chat: what the
  files alone must say to resume); **economics of a generation** (cost and wall-clock per scenario closed; when to stop
  early, wait for a reset or spend more).
- Fitted: user value, reliability, simplicity, bold bets, blind spots.

## Gaps closed (gap map #13)
| Gap | Tier | Brief |
|---|---|---|
| Coverage grid with no empty cell; not-yet ledger retried every generation | 3 | 1 (T-2093, built) |
| Tower orchestrator: one next action from the files alone, resumable after any kill | 4 | 2 |
| gen-0 writer from one line, a sweeping request or nothing | 3 | 3 |
| Per-project capability spec with a held-out exam | 3 | 3 |
| Selection + lineage + carry-over; the feature writes the Seed | 3 | 4 |
| Drift check against gen-0 + one-shot §7 sweep | 3 | 5 |
| Auto-start from loop/scout; routing line as a core candidate | 3 | 6 |
| No exam for #13 itself | 3 | 7 |
| Nothing stops a generation from rewriting the user's MUSTs or widening its own grants | 3 | 8 |

## Approaches
A. **Chosen — the tower files are the state.** The stage is the first missing or unfinished file in a fixed order
   (gen-0 → seed → missions → their tasks closed → critiques → lineage line → drift → sweep → next seed). No journal
   to disagree with the files; a kill anywhere resumes for free; a fresh session reads the same files (archaeology).
B. A JSON state machine with a journal and schema version. Rejected for now: a second record of the same facts that
   can drift from the files; kept as the fallback if A can't express a stage (the spike in brief 2 decides).
C. A headless driver (`fm run` over the tower) that executes every step. Built on top of A later, not instead: the
   step function must exist and be tested before anything runs it unattended.
D. Make the tower a `fm loop` mode. Rejected: the loop is open-ended by design (dry yield stops it); the tower has a
   fixed shape, caps and a done test.

## Design
1. **Checker — `fm genesis check`** (built, T-2093). coverage.md: `## <area>` rows, 64 cells each
   (`- <stage> × <surface>: F|I|N/A: …`); F names an existing path, I ends with the file it builds on, N/A gives a
   reason; every gen-0 capability has its row. not-yet.md: `## <idea>` items with `- blocker:`, `- tried: a; b`
   (two different approaches), `- unblocks-with:`, and `- retried: gen-N …` or `- added: gen-N …` for the newest
   generation; `## Removed` lines say harm or duplicate. Exit 1 on any problem; `fm genesis` shows the counts.
2. **Orchestrator — `fm genesis step [--json]`** (tier 4). Prints the one next action and its command, from the files:
   no gen-0 → `fm genesis draft`; no seed → write it (gen 1: by hand from gen-0; gen ≥ 2: `fm genesis seed`); a seed
   row without its mission file → `fm mission` + `fm ideas …` for that capability; a mission whose `Task:` ids aren't
   closed → `fm focus` the first open one; no critique → write it; all critiques → `fm genesis select`; then
   `fm genesis drift`, `fm genesis sweep`, next seed. Caps: ≤ 8 seed rows, ≤ 4 levels, refuses past them. One
   `c.lock` around state changes. Each step's failure is classed retryable (rerun), user-needed (into the final
   report) or fatal (the tower stops and says why). A budget line between stages (`fmcost.quote_line`). `fm next`'s
   idle path names `fm genesis step` while a tower is open. A stalled tower (no file change in 24 h with work left)
   is named in the next session's start note. Tests: kill after every stage and resume to the same next action; a
   corrupt or out-of-shape file is refused by name; a lock collision is refused; the caps hold.
3. **gen-0 writer + spec — `fm genesis draft [LINE]`, `fm genesis spec`** (tier 3). Extraction first (project kind,
   languages, gates from CI config, the user's MUST/NEVER-shaped corrections from Foreman's memory and decisions, the
   gap map), then one tool-less model call that fills the hand gen-0's skeleton (§1–§8, MUST/NEVER/DONE-WHEN). Each
   MUST taken from the user's own words quotes its source; inferred ones are marked `(unconfirmed)`; cold-start
   assumptions are listed. Generated and vendored code is fenced out. `spec` writes spec.md: "complete and best in
   class for this kind of project" as capability rows, each with exam scenarios from `fm exam gen` in the project's
   languages (a third held out). A tiny project gets a one-generation tower; a project the exam can't run gets a spec
   with no exam, flagged. Tests: the hand gen-0's own text yields every MUST and NEVER; empty input gives a valid
   draft; a planted absurd MUST in the history is marked unconfirmed, not adopted.
4. **Selection, lineage, Seed — `fm genesis select N`, `fm genesis seed N`** (tier 3). Selection reads exam.jsonl's
   train ids only (built: gen-0 §4 keeps the held-out third out of selection): a generation's rewrite stays only if
   it closes more scenarios than its parent on the same run; a tie reverts whatever the cost (cost is reported, never
   a tie-break; both fm decide, T-2102); no reopening what the parent closed (ratchet); reruns for variance when the
   margin is one scenario on a single line. Every decision is a lineage.md line and a `fm decide`.
   The exam's held-out ids are hash-locked for the generation. `seed N` writes gen-N/seed.md from the parent seed,
   its critiques, empty coverage cells (first), not-yet items (each retried), exam scores and lineage; the Seed's
   size is capped. Tests: a child that closes fewer loses; a tie loses; a reopened scenario fails.
5. **Drift + sweep — `fm genesis drift N`, `fm genesis sweep N`** (tier 3). Drift: every unfenced MUST:/NEVER: line
   in gen-N's seed and mission files is one of gen-0's verbatim (reworded or added is drift; fenced intake blocks are
   briefs, whose MUSTs are task constraints), each file quotes gen-0's constraints or points to gen-0 (a seed points,
   never restates), and one tool-less cold read of the seed against gen-0's goal, MUSTs, NEVERs and DONE-WHEN names
   drifted lines, counted only when the seed holds them. Verdict clean, drifted or unread (no read is no pass). Sweep:
   §7's list in one command — fm genesis check, mission tasks closed or blocked with a reason, no planned/active task,
   no unreasoned block, no unmerged lane, fm docs, fm doctor, a full fm check pass on this exact tree (read, never
   rerun), an exam line for gen N — into gen-N/sweep.md, exit 1 on any red. step stays on either until its Verdict is
   clean. Tests: a reworded MUST, an added NEVER and an unpointed file drift; a clean seed passes; no read fails; a
   red sweep keeps step on it, a clean one moves to the next seed.
6. **Auto-start** (tier 3). When user-origin work is dry and the gap map has tier 3–4 gaps, the idle path proposes a
   blocked task "Start Genesis here?" (never a silent run), with a cooldown and a breaker on Genesis's own failure
   and revert rate; `fm pause --now` stops it. `/foreman:genesis` skill drives `fm genesis step`. The routing line in
   rules/foreman.md is protected core: a built, evaluated candidate in a worktree and `fm ask ID core` at the end.
7. **#13 exam** (tier 3). See below. A genesis arm (`fm exam run RUN --agent genesis`) runs draft + spec + one
   generation on each scenario project; the plain arm gets "make this great" with no plugin.
8. **Charter seal + privilege diff** (tier 3). `fm genesis init` records the hash of gen-0's MUST/NEVER lines; drift
   fails if a seed contradicts one; each generation lists grants and allows used (fm ask, --allow) and halts on a new
   kind it didn't have before.

## Exam (#13; ≥ 9 scenarios per kind, ≥ 3 held out)
| Kind | Given | Graded on |
|---|---|---|
| G-line | a generated project + "make this great" | draft covers every MUST, NEVER and § of the hand gen-0 checklist |
| G-none | a generated project + nothing | same checklist; the draft names what it assumed |
| G-sweep | a generated project + "super improve this" | same checklist + a tier on every brief |
| G-tower | a generated project with planted gaps (fm exam key) | one generation closes the planted gaps (found + fixed, test first) |
Each kind 9 scenarios → 6 train + 3 held out, from `fm exam gen` projects (6 languages). Arms: genesis vs plain on the
held-out third, with cost.

## Exam of the exam
1. Oracle: the hand gen-0 itself scores 100% on the checklist; an empty draft scores 0.
2. Mutation: the hand gen-0 with any one MUST or NEVER removed scores below 100% (each item is load-bearing).
3. Held-out project ids never appear in a train run; the hand checklist is never shown to the writer.

## Spikes (tier 4, local, throwaway)
Red-team twin that games the gen-0 checklist; a planted absurd MUST; a mirror-universe selector (inverted rule must
lose); a mutation-tested exam; a never-seen repo vs plain Claude (`fmbench.stranger`); rebuild-from-gen-0 challenger.

## Inbox (tier 1–2, captured)
Generation receipt and digest with a publish secret scan; a resume verdict line; statusline tower health; a time-scrub
slider on the site page; publish only on green CI; tower rewind; and the rest of the ~40 tier 1–2 titles.

## Rejected
Cross-project genome import, specs sourced from competitors or dependencies, earned-trust autonomy or a user proxy,
persona bots on live products, signed attestations, upstream bug reports (all leave the machine or cross a NEVER).

## Tier share
Built here: 8 briefs, 1 at tier 4 and 7 at tier 3 (100% tier 3–4) plus 6 tier-4 spikes; tier 1–2 go to the inbox.

## Done when
`fm genesis check/step/draft/spec/select/seed/drift/sweep` work and are tested; the kill-and-resume test passes for
every stage; the #13 exam runs both arms on its held-out third and its exam-of-the-exam checks are tests; coverage.md
and not-yet.md are in the tower and `fm genesis check` exits 0; MASTER.md + CHANGELOG + the site's Genesis page show
it; the `/foreman:genesis` skill works in Claude Code; the routing candidate waits on `fm ask core`.

```
FEATURE: fm genesis check — coverage grid + not-yet ledger, exit 1 on any gap
FEATURE: fm genesis step — the tower's next action from its files alone, resumable after any kill
DONE-WHEN: killing after every stage and rerunning gives the same next action; caps and lock hold
FEATURE: fm genesis draft/spec — gen-0 from a line or nothing; per-project spec with a held-out exam
FEATURE: fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the next Seed
FEATURE: fm genesis drift/sweep — gen-0 MUST/NEVER drift check, §7 sweep in one command
FEATURE: Genesis auto-start proposal + /foreman:genesis skill + routing candidate (core, fm ask)
FEATURE: #13 exam — G-line, G-none, G-sweep, G-tower kinds; genesis vs plain arms
FEATURE: charter seal + privilege diff per generation
```
