# T-3006: Smith's --reason arms, first live comparison (2026-11-04)

Arms: `off` (thinking off, today's default), `state` (a compact thought state carried between turns, thinking on only on
low confidence, a failed check or a loop break, the named check asked for before an edit), `native` (the model's own
thinking on). Same seeded held-out scenarios (s5-019, Python bugs, 3 per arm), `sampo exam run s5-019 --agent smith
--model PROFILE --reason ARM`.

| model | off | state | native |
|---|---|---|---|
| gemma 4 12B (gpu-gemma12-32k) | 0/3 fixed · ends other 2, loop 1 | **1/3** · loop 2, budget 1 | 1/3, then 0/3 on a rerun · budget 3 both times |
| MiMo 9B (gpu-mimo9) | 0/3 · no plan 3 | 0/3 · no plan 2, budget 1 | 0/3 · no plan 3 |
| Qwen 3.8 27B (jarvis-nothink) | 0/3 · other 3 | 0/3 · other, loop, plan refused | 0/3 · plan refused 2, loop 1 |

T-3016's rerun of s4-018 on the 27B (off): 0/3, ends loop, plan refused (the re-plan fired), other.

## Reading
- No arm separates at n = 3. gemma's state 1/3 against off 0/3 is one scenario, inside the noise.
- Native thinking ends on the budget: 6 of 6 gemma native runs ran out of tokens thinking (one native run used 305k
  tokens), where state ended on the budget once in 3. That is the "maybe this, wait no" burn the user named; state's
  deliberate turns cut it.
- gemma 4 over Ollama ignored enable_thinking false and reasoning_effort none once (1 of 3 off runs: no text in 8,192
  tokens), logged on the task: a backend quirk, not an arm effect.
- MiMo 9B never produced a plan in any arm: its failure is planning format, not reasoning; the arms can't help it.
- The 27B's ends are plan refusals and loops: the plan gate (T-3016) and loop breaking matter more than thinking there.

## Next
The larger slice (T-2878's measurement: --limit 60 on s8-008 and s32-015, 27B and 35B, two jobs) gives n large enough
to call an arm; it runs after the merge chain.
