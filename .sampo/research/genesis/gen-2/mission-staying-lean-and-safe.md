# Mission 3 — staying lean and safe (gen 2, #12)

Task: T-2532 (brief 1); T-2536 (brief 5) waits for the end-of-run exam's first --ablate run. Grounding at planning
changed three briefs. Brief 3 (T-2534) was dropped as an exact duplicate: the exam's plain arm is already Claude with
only the guard (FOREMAN_QUIET=1 plus the bare guard settings, T-0963). Brief 2 (T-2533) is deferred to 2026-12-01: it
revives when hook notes pass 3% of what enters the context (now 0.8%), or when a per-call rate holds within 10% for a
week, so that a ratchet band can tell growth from noise. Brief 4 (T-2535) is deferred to 2026-12-01: it revives at
the first ratchet trip at a ship (none so far) whose cause isn't obvious from the shipped commits. Lesson for the next
Mission: ground each brief (is it built? has the failure happened?) before filing it.

Parent: gen-2/seed.md row 3 → gen-0.md #12: "Staying lean and safe. Each of the above keeps the hooks fast, keeps
context small and keeps the guard intact (see §6)." gen-0's goal, MUSTs and NEVERs are quoted in the seed and apply
here unchanged.

## Capability
Lean and safe by evidence, not by assertion. Foreman already holds most of the machinery: the lean ratchet
(fmdoctor.footprint, measured, grown: rules, descriptions, the largest SKILL, SessionStart and UserPromptSubmit chars,
each hook's p95, recorded at fm ship), the guard's fail-closed import path and its replay corpus (fm replay: 124
labelled cases, 0 drifted), what each agent harness enforces (fmagents), dead-project cleanup (fmtidy T-2091), and
the tower's own cost (fm budget: genesis-read $7.34 over 133 runs). Measured now: hook p95 278 ms over 13,533 runs;
Foreman's own share of what entered the context 4.4% (rules 2.5%, hook notes 0.8%); context per reply 387k on
average in this session, which comes from tool results, not from Foreman.
What it lacks: (a) the hooks that drive the work (Stop, SessionStart, UserPromptSubmit) silently switch off when a
self-edit breaks the library's import. The dispatcher exits 0 for a non-tool event with no fallback and no log, while
tool events fall back to the committed library. (b) Nothing measures what the injected context buys. The ratchet
keeps it from growing, but no run asks whether a block could be cut.

## Gaps this Mission targets (coverage: #12, 61 empty cells; the I cells below are planned, open until the exam closes them)
- Hooks survive a self-edit: operate × Claude Code, build × Claude Code, operate × other agents (the same dispatcher
  runs their adapters), operate × headless/server (headless sessions load the same hooks).
- Per-call notes in the ratchet: verify × Claude Code, learn × CLI (PreToolUse/PostToolUse notes are injected context
  that the ratchet doesn't measure today).
- What the context buys: verify × headless/server, learn × headless/server. Already measurable: plain is the
  guard-only arm, and fm bench duel --ablate (T-1375) switches each hook feature off in turn against full Foreman.
- Which commit made it heavier: ship × CLI (a tripped ratchet names the shipped commit behind each grown metric,
  from static char counts per commit).
- Subtract by evidence: understand × CLI, plan × Claude Code (after the end-of-run exam, each injected block's chars
  sit beside the foreman-vs-guard score delta; a block that buys nothing files a subtraction task).
- Not in this Mission: anything that changes how the guard parses commands, mutates it or fuzzes it (the standing
  safety rules hold that work for the user: T-1937, T-1928, T-2261, T-2068), retiring stack cards (5 of 1,219 used,
  but unused cards cost no context), SessionStart deltas (after a compact the note is the only copy). They stay idea
  cells.

## Approaches
1. Close the two gaps where they live. The dispatcher's non-tool branch takes the committed-library path that tool
   events already take, and logs to hooks.log. The ratchet gains the per-call notes metric and per-commit
   attribution. fm bench duel --ablate's verdicts file subtraction candidates. Fails if: an off arm ties full Foreman
   only because the duel's cases don't exercise what the feature helps with. The answer: a tie files a candidate,
   never a cut. The cut waits for every exam kind and the long-horizon tier.
2. Cut injected context now by judgment (shorter rules, fewer notes). Fails if: a cut removes what a session needed.
   Without an arm that measures it, a cut is a guess, and gen-0 §6 asks for subtraction backed by the exam.
3. Ablate in live sessions: withhold one injected block per session and compare outcomes. Fails if: the user's real
   work becomes the experiment. Sessions differ too much to read one block's effect at this volume.
4. Use what exists: FOREMAN_QUIET already runs only the guard (fmhooks T-0077), fmexam.SESSIONS already holds the
   session arms, fmdoctor.grown already judges metrics against the ship record, and fm cost already counts hook notes
   from transcripts. Approach 1 wires these together, with no new store.
5. Do less: only the dispatcher fallback (brief 1). It is the one gap that can silently stop the drive. The rest
   measures before it cuts, and could wait for the end-of-run exam.

Choice: 1 on 4 (75%). Brief 1 is a reliability fix with a clear failure (a syntax error mid-edit turns the drive off
with no trace). Briefs 2, 4 and 5 make the next cut evidence-based. The 25% doubt is whether --ablate's duel cases
separate any feature from full Foreman at all; if none do, that is the result the critique reports.

## Exam
#12's exam kind is lean (fmexam KINDS, T-2363: the foreman arm's overhead beside plain's on real work, with no growth
past the generation's first measure). Plain is already the guard-only arm, so foreman-minus-plain is what Foreman's
injections buy. This Mission adds no exam kind or arm. Zero-token arms run each generation, and the session arms run
at the end-of-run exam (rule 6). The lean kind's scenarios are small single tasks, so no one kind decides a cut. An
--ablate verdict of "no difference" files a candidate, never a cut. The candidate's own task cuts the feature only if
the arm without it scores no lower than full Foreman on every kind, held-out included, and on the long-horizon tier.
A loss anywhere keeps the feature.

## Long-horizon goal (end of run)
Across the long-horizon goals, no hook event is silently off (hooks.log shows every fallback). The footprint at the
end of the run is no larger than at its start, or each growth names its commit and the exam delta that pays for it.

## Lean
No new verb. fm exam gains one arm value, the ship footprint gains one metric, and the doctor's ratchet row gains
commit names. The dispatcher change runs only after a failed import. Hook p95, rules size and injected context don't
grow. Brief 5 exists to shrink them.

## Tier share
Brief 1 is tier 3, a capability Foreman lacks: hooks that survive their own breakage. Briefs 2, 4 and 5 are tier 2,
because the measuring they build on already exists (the ratchet, the plain arm, --ablate). One of four is 25%, under
gen-0 §3's 70%. #12's open tier 3-4 gaps sit in the guard's parser, which the safety rules hold for the user, and the
critique should weigh that rather than inflate the labels.

## Done when
A broken plugin/lib import leaves every hook event running from the committed library, with a hooks.log line that fm
doctor shows. The ship footprint holds the per-call notes metric, and a tripped ratchet names its commits. An fm
bench duel --ablate run captures one subtraction candidate for each feature that changed no pass and cost no more.
The candidate names its cases and the confirmation (every kind and the long-horizon tier) it needs before any cut.

## Briefs (fm intake)
```
FIX: a non-tool hook event (Stop, SessionStart, UserPromptSubmit, SessionEnd, Notification) whose working-copy library fails to import runs from the committed library like tool events do, and every such fallback is logged to hooks.log, so fm doctor shows it; nothing is silently off
FEATURE: per-call hook notes in the lean ratchet: the chars PreToolUse and PostToolUse notes injected per session (the median of the newest sessions, counted as fm cost counts hook notes) are recorded in the ship footprint and judged by fmdoctor.grown
FEATURE: a guard-only exam arm: fm exam run --agent guard runs a claude session with Foreman loaded and FOREMAN_QUIET=1 (only the guard), graded like foreman and plain on the same scenarios, so the end-of-run exam prices the injected context
FEATURE: a tripped lean ratchet names the shipped commit behind each grown static metric (rules, descriptions, largest SKILL chars, measured per commit with git show), at fm ship and in fm doctor
FEATURE: subtract by evidence: fm bench duel --ablate captures one subtraction candidate per hook feature whose off arm changed no pass and cost no more, naming its cases and that the cut needs the arm to score no lower on every exam kind and the long-horizon tier first
```
