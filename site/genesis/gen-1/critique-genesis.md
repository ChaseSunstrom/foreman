# Critique — Mission 2, Genesis as a feature (gen 1, #13)

Tasks: T-2093, T-2095, T-2099, T-2102, T-2104, T-2105, T-2112, T-2113 (briefs 1–8, all done and on main), plus
T-2114 (found by the first live drift read, done and on main). Mission: gen-1/mission-genesis.md.

## Exam scenarios: closed vs planned
| Planned | State |
|---|---|
| 1. `fm genesis check`: coverage grid + not-yet ledger, exit 1 on any gap | closed — test_genesis; the live tower exits 0 |
| 2. `fm genesis step`: one next action from the files alone; kill after every stage gives the same action | closed — kill-and-resume test per stage; lock and caps hold |
| 3. `fm genesis draft/spec`: gen-0 from a line or nothing; spec with a held-out third | closed — test_genesis; secrets refused by init |
| 4. `fm genesis select/seed`: fewer closed loses, a tie loses; the feature writes the next Seed | closed — test_genesis (mirror selector: the inverted rule loses) |
| 5. `fm genesis drift/sweep`: reworded MUST, added NEVER, unpointed file drift; §7 sweep in one command | closed — tests; live gen-1 read went unread → drifted → clean (see What failed) |
| 6. Auto-start offer, `/foreman:genesis` skill, routing line as a core candidate | closed except the routing line, which waits on `fm ask core` (protected core, the user's call) |
| 7. #13 exam: G-line, G-none, G-sweep held out (9 scenarios) | closed — genesis 9/9 strict and 9/9 given; plain 0/9 strict and 9/9 given |
| 7. #13 exam: G-tower (a whole generation in a throwaway repo, `fm exam run --agent genesis`) | built, run below; see Outside signals |
| 8. Charter seal + privilege diff | closed — the ledger's logged seal wins over a forged or deleted gen-0.sha256; grants aren't uses; archived months count |
| Exam of the exam: oracle 100%, empty 0, each checklist item load-bearing, held-out ids never in train | closed — tests |

## Outside signals
- **Plain vs Genesis drafts, held out (9 scenarios):** on what each arm was given they tie (9/9 each); Genesis costs
  ~$0.09–0.12 a set against plain's ~$0.23. Strict (the hand gen-0 checklist + planted lines) is 9/9 vs 0/9, but the
  red-team spike says that gap is partly by construction: the drafter was built to the checklist's shape and plain
  never sees it. The honest reading: **Genesis is as complete as plain on its input, at about half the cost, and only
  Genesis carries the user's own MUST/NEVER lines through verbatim.** Selection should use the given score.
- **G-tower (a whole generation in a throwaway repo, one held-out scenario a kind):** genesis found 3/3, fixed 0/3,
  13 false alarms, $0.70; plain found 3/3, fixed 3/3 (test-first 2/2), 9 false alarms, $0.52. Neither closes a
  scenario, both on false alarms. Genesis fixed nothing because `fm genesis step` read its hand-listed Missions
  (a bullet list, no table) as a dry generation and jumped from seed to select (T-2119, fixed: a seed with no rows
  must say "no Missions this generation"). The false-alarm count is the lever for #1: report only what's proven.
- **fm second (the drift cold read, §3.7):** caught a real drift in my own hand-written gen-1 seed — the Completeness
  bullet had dropped "other agents, Desktop", the Safety bullet had dropped "grant yourself anything" and "merging
  stays my call". Fixed by quoting all six gen-0 MUST/NEVER lines verbatim. Clean now.
- **fm outcomes (all time):** 1301 of 1346 finished tasks held, 44 fixed later, 1 reverted. Mission 2's nine tasks:
  none reopened yet.
- **fm bench duel:** not run for #13 (the exam arms are the duel here).

## Coverage cells filled
#13 in coverage.md: find, understand, plan, build, verify, ship and learn × Claude Code (the scout offer and the
`/foreman:genesis` skill), verify × site (drift and sweep verdicts on the Genesis page), verify × CLI (drift, sweep,
exam, seal). Still ideas: operate × Claude Code (statusline tower health, inbox) and every #13 cell on fm code, other
agents, MCP, Desktop and headless/server.

## Not-yet items
None added. gen-0's Completeness MUST names fm code, other agents and Desktop for every capability; #13 has none of
them yet. That is open work, not a not-yet: a brief for the next generation (captured), since `fm genesis` is a CLI
verb any agent with a shell can already run, and what's missing is the surface (a shim line, a Desktop panel).

## Spike verdicts
| Spike | Verdict |
|---|---|
| Red-team twin that games the checklist | kept as a finding: the oracle arm is the checklist's echo and scores 100% by construction, so the exam holds only while the checklist stays hidden from every Mission; strict scores are a ceiling, the given score decides |
| Planted absurd MUST | covered: G-line plants MUST/NEVER lines and grades that the draft carries them verbatim; a child can't add constraints, and ones not from the user are marked unconfirmed (test_genesis) |
| Mutation-tested exam | covered: each MUST/NEVER removed from the hand gen-0 scores below 100% (exam-of-the-exam test) |
| Mirror-universe selector | covered: select's tests (an inverted rule, a tie and fewer closed all lose) |
| Never-seen repo vs plain | approximated: the generated-project arms are never-seen repos; `fmbench.stranger` not run separately |
| Rebuild-from-gen-0 challenger | not done: retry next generation (a fresh session rebuilds gen-1's seed from gen-0 alone; drift and select compare) |

## What failed
1. The first live drift read came back "unread": the reader quoted a bullet wrapped over two lines, and the quote
   check matched physical lines only. Fixed (T-2114): quotes match whole logical lines.
2. Then it flagged real drift: my seed paraphrased gen-0's MUST/NEVER lines and lost words. The check worked; the
   author didn't. Fixed: every Seed quotes them verbatim, and `fm genesis seed` already says so.
3. The cold read didn't know the user's later steers (9 scenarios a kind, Mission 8, the coverage grid), so a Seed
   that followed them would read as drift. Fixed (T-2114): steers cited `user steer` go in a fence; a steer can only
   add to gen-0.
4. T-2112/T-2113 each needed a review-round fix (fallback drafts counted as wins; a forged seal file laundered an
   edit). Both caught before ship by the one reviewer pass, not by the briefs' own tests.
5. A flaky test (test_run.Hang, ProcessLookupError) during gates; captured as T-2115.
6. The G-tower arm's tower never built a Mission: step took a table-less seed for a dry generation (T-2119). No
   unit test had a seed in any shape but the table; the live arm found it.

## Deviations
Whole-file hash, not MUST/NEVER-only (gen-0 never changes at all); the seal is read from the ledger first; the
routing line has no candidate yet (waits on `fm ask core`); G-sweep checks a tier is named on every brief, not that
it is right; three low findings left (an n>1 sweep rerun moves the window start; a garbage seal file gets no hint;
step and check don't read the seal).

## What the next Seed should change
- Quote gen-0's MUST/NEVER lines verbatim in every Seed and Mission file; never summarise them.
- Grade #13 drafts on the given score; keep strict as a ceiling and the hand checklist hidden.
- A brief for #13 on every surface gen-0 names: fm code, other agents (the shim's line), Desktop (a tower panel),
  plus statusline tower health.
- Run the rebuild-from-gen-0 challenger and `fmbench.stranger` once each.
- Size G-tower's session to a whole generation (time and budget), or grade one Mission of it, so the arm can finish.
