## Step 2, round 1: small-model mode on vs off, paired (2026-11-07)

What changed (lane foreman/T-2878): T-3530 `extract_json` keeps an action holding an invalid `\'` escape (2e2a4b67d);
Smith reads an argument under its one alias sent or nested one level, else says in one line what was sent and the
shape wanted (88e8cffb5); `fm code --small` / `sampo exam run --agent smith --small` (6847d1892): every change type's
check must fail before the work, a request whose words ask for a change can't be planned as RESEARCH or answered
read-only (sent back once), and a change plan's last step can't end with nothing changed.

Method: fresh runs of the same seeds (44 scenarios each: 11 kinds x 6 languages, a quarter held out), one arm with
--small and one without, both on the new code, paired by scenario id. Outcome: the grader's pass (every keyed defect
found, fixed and said, no false alarm). Two-sided sign test on the pairs that differ. A pair where either side ended on
the endpoint's error is dropped (jarvis was down 00:34-00:41Z: s29-033/034 lost 30 scenarios and were rerun as
s29-035/036; 3 more dropped in all). Readers: scratchpad t2878_paired.py, t2878_fail.py, t2878_parse.py.

| model | pairs (train/held out) | pass on | pass off | on only / off only | p | held out on/off | fixed on/off | act-turn parse on/off |
|---|---|---|---|---|---|---|---|---|
| qwen3.8-27b (s28-027:028, s29-035:036, s30-037:038) | 129 (97/32) | 9 (7.0%) | 8 (6.2%) | 4 / 3 | 1.0 | 2 / 1 | 21 / 17 of 144 | 92.9% / 90.1% |
| mimo-v2.6:9b (s28-031:032) | 44 (33/11) | 0 | 0 | 0 / 0 | 1.0 | 0 / 0 | 1 / 1 of 48 | 86.6% / 88.3% |
| gemma4:12b 32k (s28-029:030) | 44 (33/11) | 0 | 0 | 0 / 0 | 1.0 | 0 / 0 | 5 / 5 of 48 | 98.9% / 96.0% |

Before (step 1, old code, small off) -> after (new code, small on), the same seed-28 scenarios: qwen3.8-27b pass 2/44 ->
4/44 (s28-020 -> s28-027), fixed 5 -> 7 of 48, parse 84.2% -> 93.5%; gemma4:12b pass 0/44 -> 0/44, fixed 2 -> 5,
parse 98.5% -> 98.9%; mimo-v2.6:9b pass 1/44 -> 0/44, fixed 7 -> 1, parse 87.5% -> 86.6%. Across runs these move with
the day's noise as much as with the code: the paired on/off rows above are the comparison that counts.

**Gain: none on the pass rate.** +0.8 points on qwen (n=129, p=1.0), 0 on gemma and mimo; far from the +15 the brief asks.
gemma's ends barely move (loops 18 vs 19, hollow closes 14 vs 13): its hollow closes were red-before checks at step 1,
which these controls don't touch; its false alarms rise 19 -> 27, as qwen's do.
What the controls did move (qwen, the same 129 pairs):
- Change requests (bug, dep, vague, ambiguous; 44 pairs): read-only answers 4 -> 0, hollow closes 29 -> 25, but loops
  7 -> 11 and plan or finish refusals 3 -> 8. Forced to change, the 27B more often loops or fails a gate; none passes
  either way.
- Test-first 0 -> 4 of 72 keyed; fixed 17 -> 21 of 144.
- False alarms 47 -> 68: the findings call adds more on the small arm, and a false alarm alone fails the grade.
- The hollow closes left are review requests ("Check the docs are right", "Review this for security problems")
  closed as RESEARCH: RESEARCH is right there; what fails is the findings (missed defects, false alarms), not the close.
- T-3530 and the parse fixes: the act-turn parse rate is 90.1% (off) to 92.9% (on) against 89.1% at step 1, still under
  the 95% gate; prose turns with no call stay qwen's largest parse loss.

mimo-v2.6:9b: no valid plan is still most of its ends (30 on, 27 off of 44). The alias reader showed what it sends:
`write` with only `file` (28 of its write errors), a key literally named "file content", `edit` with no `old`: its
native tool calls lose arguments, which no alias can restore.

What this says for the next round (captured): T-3569 findings precision for review requests (the remaining hollow
closes and the false alarms), T-3567 a plan normaliser for mimo's enum misses (PERF, tier), T-3568 mimo in text-action
mode. Small-model mode stays opt-in (no profile sets "small"), as the brief requires until the held-out split shows a
gain. qwen3.6-35b still unmeasured: the moons grow keeps the 27B loaded on jarvis.
