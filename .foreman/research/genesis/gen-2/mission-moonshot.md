# Mission 8 — moonshot (gen 2): anergy for permission prompts

Task: T-2563 (brief 1, the spike).

Parent: gen-2/seed.md row 8 → the Moonshot section (far-domain lens: immune systems; judged on novelty and value
only). gen-0's goal, MUSTs and NEVERs are quoted in the seed and apply here unchanged.

## Capability
Borrowed mechanism: anergy. In the immune system, a signal that arrives without a confirming second signal stops
producing a response; the cell tolerates it. Its Foreman form: a permission prompt that a person approves by reflex,
within a second or two every time, has stopped carrying a decision. Each such prompt costs attention and confirms
nothing. The frontier digest's top complaint is exactly this: 15 or more approval prompts in one session, because
allow lists match command prefixes. Foreman sees every prompt (its PermissionRequest hook, plugin/lib/fmhooks.py,
gets each one's tool_use_id) and the call's PostToolUse with the same id, so the time a person took to approve can be
measured without any new hook.

## Grounding
- Brief 1: fmhooks.permission_request records only fm ask prompts today (_prompts_path); nothing pairs a prompt with
  its PostToolUse to time the person's decision. The frontier digest (gen-2/frontier.md) names approval fatigue first;
  the ledger holds 55 approval_granted events, and Claude Code's own prompts are not counted anywhere.

## Ideas (each with its prior art, how ours is better, and a novelty mark)
### Anergy for permission prompts
Time each permission prompt from PermissionRequest to the call's PostToolUse. Per
command class (the guard's own classification of the call), a class approved within 2 seconds in 5 or more prompts
is reported as reflex, with the allow rule that would retire it. Never for a class the guard counts as destructive
or outward, and never applied by Foreman: the user applies a rule.
Prior art: Claude Code's /fewer-permission-prompts skill (it scans transcripts for read-only calls); Codex's
approval modes (fixed tiers).
Better by: it measures what the person actually does (a reflex, or a pause to think) instead of guessing from the
command's shape, it keeps the prompts that people deliberate over, and the guard still decides what may never be
suggested.
Novelty: 4
### Pre-armed undo (immune memory)
Before a step whose files and command resemble a past change that was reverted,
make a checkpoint and name the past harm, so recovery is one step.
Prior art: fm checkpoint, git reflog, editor undo history.
Better by: it arms itself only where history shows harm, so it costs nothing elsewhere.
Novelty: 3
### Lessons scored by harm, not hits (autoimmunity check)
A recalled lesson that precedes worse outcomes (a revert
or a later fix on the file it was shown for) is flagged for retirement.
Prior art: fm recall --lessons counts times shown, never recalled and recurred (T-0617).
Better by: it scores a lesson by what followed it, not by how often it was shown.
Novelty: 3
Queued for the user, not built: compositional guard checks across calls (T-2561) and a polymorphic guard per
install (T-2562). Both are blocked with their reason. Designing them means enumerating guard-bypass forms, which a
standing safety hold (T-1937, T-1928) bars Foreman from doing on its own. They wait for the user's decision.

## Approaches
1. Spike idea 1 in a lane: pair PermissionRequest with PostToolUse by tool_use_id in a small store, compute latencies
   per guard class, and report reflex classes in fm doctor and fm digest. Fails if: PostToolUse time includes the
   tool's own run, inflating latency. The answer: the spike measures how often a slow tool masks a reflex, using the
   fast tools (reads, greps) as the reference.
2. Auto-apply allow rules for reflex classes. Fails if: it lowers a safety layer without the user (gen-0's NEVER).
3. Use what exists: the PermissionRequest hook and PostToolUse already run on every prompt; the guard already
   classifies every command. The spike only pairs and times them.
4. Do less: count prompts per session and report the total. Fails if: a count says nothing about which prompts
   carry a decision.

Choice: 1 on 3 (65%). The 35% doubt is the latency signal: a tool's run time folded into the measurement.

## Exam
No exam kind (a moonshot is judged on novelty and value). The spike's own check: on this machine's next sessions, the
store pairs at least 90% of prompts with their PostToolUse, and the report names at least one class or says none
qualified. A failed spike goes to not-yet.md with its blocker, never dropped.

## Long-horizon goal (end of run)
A person reading fm digest sees which prompt classes they approve by reflex, with the rule that would retire each,
and none of them is a class the guard counts as destructive.

## Lean
One small store of prompt timings (capped), written by the two hooks that already run. No new verb: the report rides
fm doctor and fm digest. Hook p95 grows by one append on PermissionRequest and one lookup on PostToolUse.

## Tier share
Brief 1 is tier 4: no harness measures whether its prompts carry a decision.

## Done when
The spike lane pairs prompts with their outcome and reports reflex classes, or the spike fails and its blocker is in
not-yet.md.

## Briefs (fm intake)
```
FEATURE: anergy for permission prompts (moonshot spike): pair each PermissionRequest with its PostToolUse by tool_use_id, time the person's approval per guard command class, and report classes approved within 2 s in 5+ prompts with the allow rule that would retire them (never destructive or outward classes, never applied by Foreman), in fm doctor and fm digest
```
