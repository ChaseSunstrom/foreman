# Mission 5 — staying lean and safe (gen 3, #12)

Task: T-2666 (the Mission's own grounding and filing). Briefs: below, taken in after this file is put.

Parent: gen-3/seed.md row 5 → gen-0.md #12 "Staying lean and safe". gen-0's goal, MUSTs and NEVERs are quoted in the
seed and apply here unchanged.

## Capability
Foreman's own cost is measured whole, and its safety layer holds under input built to slow it. #12 has two halves:
lean, meaning Foreman's tokens, context and spend; and safe, meaning the guard and unattended runs keep a bounded blast
radius. This Mission adds one measured gap to each half and one to where they meet, unattended spend.

## Grounding
- Brainstorm: fm mission for #12, then fm ideas --rounds 4 --deepen 3 --falsify --crossbreed --seen-latest 6 with the
  performance and security lenses added: 525 distinct ideas (research/brainstorm-20261102-142457). Three recon passes
  grounded 524 of them in 46 clusters (55 built, 179 partial, 289 new, 1 false premise; 29 marked build), recorded with
  fm research add as research/brainstorm-20261102-m5.md, which names the one idea a pass lost.
- Spot check, false: "fmrelproof.py:82 extracts zips unfiltered". fmrelproof.py:79-81 refuse absolute and `..` names
  before extractall, so the slate drops it.
- Spot check, true but deliberate: fmsession._child_env (fmsession.py:289) drops only the nesting variables. Child
  sessions do the user's work with the user's environment, so an allowlist would break them; skipped.
- Baseline, counted before fixing: `fm burden --days 7` reports 26 and 49 injected chars per turn, which reads low.
  Claude Code delivers SessionStart's additionalContext as a `hook_success` attachment whose `stdout` holds the JSON (42
  in this session alone); fmcost.INJECTS (fmcost.py:1506) lacks `hook_success`, and fmcost.burden reads only `content`,
  so the largest injection is uncounted.
- Re-grepped for brief 2: no test_guard* file times fmguard.check (no perf_counter, no ReDoS case).
- Re-grepped for brief 3: fmserve.cmd_run caps total spend with --max-usd (run_usd, fmserve.py:899); nothing compares
  spend since the last close.

## Gaps this Mission targets (coverage: #12)
- learn × fm code (lean): the burden count misses SessionStart's context, and no reader says which note source costs
  what. Without both, a lean change can't be priced.
- verify × Claude Code (safe): the guard runs on every Bash call, and one quadratic regex would slow every command
  without a test noticing.
- operate × headless/server (lean and safe): a run can keep spending while closing nothing, under its total cap.
- Not in this Mission: bypass-mode leases, outbound-text secret scans for PR bodies, slopsquatting checks. They are
  marked build in the catalogue but are design-heavy (L) or need network calls on the hook path; the catalogue carries
  them to the next seed.

## Ideas (from the brainstorm, grounded)
- "Add fm trim, a menu of injected context with usage counts" is partial. Brief 1 builds its measuring half.
- "Time guard regexes on pathological input" is new. That is brief 2.
- "Stop a drive burning money without progress" is partial (fm contract and fm budget cap totals). That is brief 3.
- The rest of the 29 build clusters stay in the catalogue with their marks; none is dropped silently.

## Exam
- Brief 1: a transcript with a SessionStart `hook_success` carrying additionalContext counts its characters, and
  `fm burden --by-source` lists sources by chars per turn. The live 7-day number is recorded before and after.
- Brief 2: every pathological input finishes inside its bar, and a planted quadratic pattern fails the test.
- Brief 3: a stubbed run that spends past the bar with no close stops and names why; one that closes keeps going.
- The exam kinds that reach #12 (lean, T-2363) are unchanged; they run in the end-of-run exam.

## Long-horizon goal (end of run)
Every lean claim prices itself in whole injected characters per turn, by source, and the guard's worst case is a
measured number, ratcheted like the hook p95.

## Lean
Brief 1 adds one flag to an existing verb, brief 2 one test file, brief 3 one option on fm run. No new verb, no new
state file.

## Tier share
All three are tier 2 to 3 (S-M): measured gaps, each with its check.

## Done when
- Each brief closes with its own criterion command green on the closing tree.
- After brief 1, `fm burden --days 7` runs again. The 26 and 49 chars per turn baseline and the new numbers go into
  gen-3/critique-staying-lean-and-safe.md.
- CHANGELOG gets one line per brief. MASTER's fmcost line names `--by-source`, and its fmserve line names
  `--stall-usd`.

## Briefs (fm intake)
```
FIX: fm burden counts SessionStart context delivered as hook_success stdout (additionalContext), which fmcost.INJECTS misses, and fm burden --by-source lists each note source (SessionStart, stack card, ambient tests, Next, guard) by chars per turn; MASTER and CHANGELOG say it
FEATURE: a test times fmguard.check on pathological commands (long quoted runs, deep nesting, many heredocs, 50k-char lines) and fails on any over its bar, with a planted quadratic pattern proving the test can fail
FEATURE: fm run --stall-usd N stops the run when it has spent N dollars since its last task close and names why in the receipt; a run that keeps closing tasks is never stopped by it
```
