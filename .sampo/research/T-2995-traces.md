# T-2995: verified Smith traces, first live counts (2026-11-04)

- Run: `sampo exam run s5-019 --agent smith --model jarvis-nothink --split all --limit 4` (qwen3.8-27b, thinking off, 40 steps), on 4 bugs minted from a real Python project (T-2978 minting, T-3004 request naming the failing command).
- Outcome: 1 of 4 fixed by the grader's hidden check (m04); no run closed within its 40 steps (all hit --max-steps). Earlier run with thinking on and no command named: 0 of 4.
- Kept: 1 journal (m04), kept because the grader said fixed (T-2995 live change: a grader-fixed run is the stronger proof than the run's own close). Red runs keep nothing; a Claude slot keeps nothing.
- Export: `sampo exam models --traces DIR` wrote 2 conversations (Smith's two phases of the m04 run; 22 and 64 messages), 0 dupes, 0 Claude runs refused, no user name or home path in the text.
- What it means for T-2971 (the distilled actor): the pipeline works end to end; the yield is the bottleneck (1 fix per 4 scenarios at ~20 min each on the 27B). Next levers: more minted scenarios across projects, the T-3006 reasoning layer (fewer wasted steps), and a higher step cap for exam runs.
