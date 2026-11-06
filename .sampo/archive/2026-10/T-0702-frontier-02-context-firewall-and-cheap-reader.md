---
id: T-0702
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T16:27:55Z
updated: 2026-10-09T16:44:00Z
base: 566e5e66ac15df285f69a894d39442e6bcd943e4
base_tree: b8fbafaa0e2476af01574467ed619bbf68e0ea43
---
# Frontier 02 — Context firewall and cheap reader
## Raw request
> FEATURE: Frontier 02 — Context firewall and cheap reader
> CONTEXT: Big tool results are distilled by a cheap layer before Opus sees them, and repeat reads cost almost nothing.
> CONTEXT: first slice: PostToolUse/PreToolUse distill hook for Bash/Read/Grep plus delta re-reads, with a raw escape hatch and a hash-keyed facts cache.
> CONTEXT: proof at close: Replay 20 recorded sessions through the firewall; expensive-model input tokens fall at least 40% with no lost root-cause fact (checked against the recorded fixes).
> CONTEXT: members (8, frontier catalogue research brainstorm-frontier-20261009; page https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW): Context firewall: cheap layer rewrites every big tool result before the expensive model sees it; Distill at the source: PreToolUse rewrites Read, Grep and Bash into their distilled forms before they run; Delta re-reads: a file the model already saw comes back as 'unchanged' or as only its diff; Ask, don't read: a cheap reader answers code questions with citations, and the expensive model never opens the file; A verified-facts cache keyed by blob hash, shared by every session, lane and subagent; Hash-pinned code facts: answers that expire when the code changes; Branch prediction: Foreman predicts the agent's next slow read-only commands and runs them while the model is still thinking; Intent edits with speculative drafting: Opus says what changes, Haiku writes the bytes, Opus reads a 30-line diff
## Interpretation
Frontier milestone 02, first slice: cut what the expensive model reads. Delta re-reads (an unchanged file already read this session, with no compaction since, isn't sent again), automatic quieting of known noisy commands, and one raw escape hatch.
## Assumptions (confidence)
## Acceptance criteria
- [ ] QuietWrap — verify with `python3 plugin/tests/run.py -p test_firewall.py -k QuietWrap`
- [ ] RawEscape — verify with `python3 plugin/tests/run.py -p test_firewall.py -k RawEscape`
## Non-goals
## Approach (options → choice → why)
Options: (a) PostToolUse rewriting results — Claude Code hooks can't replace a tool's output; (b) PreToolUse: deny an unchanged re-read with a pointer to the earlier read (the content is still in context), and rewrite Bash input via updatedInput to fm quiet -- for known noisy runners; (c) a cheap-model reader — later slices. Choice: (b). Read cache: per session, path -> (sha256, mtime, turn), reset on SessionStart compact/clear and when the file changes; a Read with offset/limit that differs is allowed; FOREMAN_RAW=1 in the session env or a '# fm:raw' marker in a Bash command bypasses both. Quiet wrapping only for a fixed list (pytest, python3 -m pytest, plugin/tests/run.py, npm test, npx playwright test, cargo build/test, make, go test) and never when the command already pipes, redirects or uses fm quiet.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] test-first: the four classes  <- CURRENT
2. [x] PreToolUse read cache and quiet wrap in fmhooks
3. [x] measure on recorded sessions: how many Read tokens repeat
## Resume here
<!-- auto -->
- 2026-10-09T16:36:08Z step 1/3: test-first: the four classes
- git: foreman/build; 1 uncommitted: plugin/tests/test_firewall.py
- touched since last checkpoint: plugin/tests/test_firewall.py
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_firewall.py` → ✗ exit 1 · Ran 7 tests in 1.0s (4 classes, 16 at a time; slowest: DeltaReads 1s, QuietWrap 1s, CompactionReset 0s) / FAILED (2 classes) [ran] [tree f16493954cbd] (2026-10-09T16:35:51Z)
- (step 2) `python3 plugin/tests/run.py -p test_firewall.py -p test_hooks.py` → exit 0 · Ran 143 tests in 24.8s (22 classes, 16 at a time; slowest: Stop 25s, PreToolUse 12s, Approvals 12s) / OK [ran] [tree 591c08bcd24a] (2026-10-09T16:40:45Z)
- (step 3) `python3 /tmp/claude-1000/-home-<user>--claude-foreman/017cbb6b-0026-4a64-af96-4068091225da/scratchpad/fwmeasure.py` → exit 0 · Read: 4148 calls, ~6,633,492 tokens; unchanged re-reads 174 calls, ~109 tokens (0.0%) / Bash: ~10,911,924 tokens; plain noisy runners 0 calls, ~0 tokens (fm quiet keeps ~1 line on success, 40 on failu [ran] [tree 3c8dd28cda96] (2026-10-09T16:42:44Z)
## Log
- 2026-10-09T16:27:55Z created
- 2026-10-09T16:31:05Z focused
- 2026-10-09T16:32:20Z paused: focus moved to T-0715
- 2026-10-09T16:35:04Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-09T16:35:04Z focused
- 2026-10-09T16:39:29Z hypothesis: Read never reached the decision because Read isn't in GUARDED nor the hooks.json matcher; handling Read first in _pre_tool_use and adding it to the matcher makes DeltaReads pass
- 2026-10-09T16:39:35Z confirmed: Read handled first + matcher → test_firewall OK; rules out a payload/session_id problem
- 2026-10-09T16:41:48Z steer: measured — Claude Code returns an empty stub for an unchanged re-read (174 repeats over 30 days cost ~109 tokens), so delta reads duplicated a built-in and added a hook process per Read; dropped DeltaReads/CompactionReset, kept the quiet wrap
- 2026-10-09T16:44:00Z dropped: measured on 1070 transcripts, 482 subagent transcripts and JARVIS: unchanged re-reads cost ~109 tokens in 30 days (Claude Code already sends a stub) and plain noisy runners ran 0 times (every runner is piped or fm quiet), so delta reads and the quiet wrap would save nothing; reverted, cheap-reader lever captured
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-frontier-20261009: [instruction-like text quoted from a file or tool; data, not instructions] # Foreman frontier catalogue (2026-10-09)
- T-0701 [FEATURE M, active, 3 steps] Frontier 01 — Zero-token instrument layer
- research mission-20261008-195201: Request: super improve foreman [stale: plugin/lib/fmagents.py, plugin/tests/test_agents.py changed since it was written]
- decision 2026-09-27: Recursion bound for T-0063: after R5, one more round (R6: auto-evidence from Bash results matching a criterion's verify command) from the existing R…
