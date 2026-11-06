# Mission 4 — verifying anything (gen 4, #6): meaning checked when the plan is written

Task: T-2914 (brief 1).

Parent: gen-4/seed.md row 4 → gen-0.md #6: "Verifying anything. Proof beyond unit tests: UI (`fm shot`, `fm flow`),
data, docs against code, infra and ops, performance, and "does it do what the user meant". Whatever can't be proven
gets labelled as unproven." gen-0's goal, MUSTs and NEVERs are quoted in the seed and apply here unchanged.

## Capability
"Does it do what the user meant", proven per clause, at the moment proof is cheapest. Meaning is the largest unproven
class: `sampo prove --rollup` (2026-11-04) counts 767 unproven over 30 days, 599 of them meaning. The gen-3 critique
named it as #6's next lever: "fm spec's example assertions become runnable criteria at plan time, with no
confirmation step; a meaning label clears only when such a criterion ran green." Before naming a fix, this Mission
counted what each candidate would clear (the staying-lean critique's rule):
- Every shown reason is "no criterion checks it" (900 of the 900 reasons the rollup prints; it cuts each task to 3).
  None is "no green run" or "couldn't fail". The clauses are missing checks, not failing ones.
- By whose words: of the 599, 113 are user-sourced briefs. 273 are Sampo's own (discovered 159, followup 55, self 20,
  baseline 14, ci 12, genesis 7, genesis-review 3, steer 2, scout 1). 213 are archived briefs the index doesn't carry.
  The most common unproven clauses are Sampo's provenance notes, not requests: "(noticed by an agent;" 52, "Plugin
  parity: usable from Claude Code" 16, "Captured by fm check: the gates are red" 15, "Baseline red" 11.
- So the count mixes two things. The user's words lack criteria at plan time: 53 of 302 user M and L closes in the
  rollup's window carry the label. Sampo's notes were never anyone's meaning.
The brief does both halves honestly. The plan gate asks for the missing check while it is cheap. The rollup prints
the two counts side by side, adding up to today's 599, and drops nothing. That is the gen-3 review's lesson: the docs
kind's 601 → 421 "fell by narrowing what counts, not by proving anything".

## Grounding (each read in the code on 2026-11-04)
- plugin/lib/sampo/recall.py:691 `bind(b)` binds each Raw-request clause (CONTEXT lines aside) to the criterion
  sharing 2+ words. recall.py:718 `meaning_unproven` keeps those with no green, failable check.
- plugin/lib/sampo/core.py:4928 `_need_meaning` turns them into the label, and core.py:4937 registers
  `PROOF_KINDS["meaning"]`. It is a label, never a block.
- core.py:3130 `plan_gaps` is the plan gate (`sampo focus` refuses until it is empty). It calls `_content_gaps`
  (core.py:3019) for briefs not yet started, skips harness plans (`harness_plan`) and requires criteria. It never
  calls `bind`, so a plan can pass with a whole clause unchecked.
- Callers of the shared read (grep): `_content_gaps` is also called by Smith's M-plan check at smith.py:286 on a stub
  brief, which carries no source. The new gap lives in `plan_gaps`, not `_content_gaps`, so Smith's check is
  unchanged. `meaning_unproven` has one caller (core.py:4931).
- plugin/lib/sampo/change.py:65 `cmd_spec` writes assertions, but only for a Python `--module`, so it can't be the
  plan-time route for most clauses (UI, docs, process). It stays the route for a Python wish.
- Steer (d), the user's 2026-11-03 ask that public surfaces name models by role and the orchestrator as any agent: it
  is built and tested (T-2852: site/build.py:574-579 and site/genesis/genesis.js:86-89 rewrite the local endpoint's
  name to "a large local model"; test_genesis.py and test_site_sections.py hold it). Read here, not rebuilt.

## Gaps this Mission targets (coverage: #6)
- plan × Claude Code: the plan gate a Claude Code session meets asks for each clause's check before the first edit.
- verify × CLI: the rollup's meaning count says whose words are unproven.

## Ideas (from the brainstorm, grounded)
fm mission, then fm ideas --rounds 4 --falsify --crossbreed --seen-latest 6 (research/brainstorm-20261104-002904: 329
distinct ideas; --deepen dropped by today's risk budget, recorded). Grounded:
- "Turn spec examples into runnable criteria at plan time" (round 1): partial. `sampo spec` makes assertions for a
  Python module wish, and the plan gate never asks. Brief 1 moves the ask to plan time for every clause, and
  `sampo spec` stays one way to answer it.
- "Label every close with a three-valued meaning verdict" and the cross-bred "Close every task with a three-valued
  verdict, and show proved against unproven everywhere": partial. The rollup is two-valued per kind. The split by
  whose words is the first step, and three values is the next.
- "Compile spec examples into stub-first criteria with a small model": new. Held for T-2878's control step, because
  a model-drafted check needs the vacuous-check proof (`sampo task prove --vacuous`) behind it first.
- "Gate shipping on a role-word vocabulary lint driven by one role table" (cross-bred, steer d): built near T-2852
  (the render-time rewrite and its tests). Not rebuilt.

## Approaches
1. A plan-time gap from `recall.bind` in `plan_gaps` for user M and L briefs, plus a rollup split by whose words.
   Likely outcome: new user M and L closes stop arriving with meaning unproven. Fails if: bind's two-word rule binds a
   clause to an unrelated criterion. The close-time label still shows that case.
2. use what exists: `sampo spec` per wish. Fails if: Python-only, `--module` required.
3. do less: split the count only. Fails if: no clause gets proven, and the user count keeps growing.
4. A local model drafts each missing criterion. Fails if: drafted checks are written to pass. Held for T-2878.

Choice: 1 (70%).

## Exam (an outcome measure, with a live reading)
- Outcome measure: the share of user M and L closes that land with meaning unproven, from the rollup, for closes after
  T-2914 against 53 of 302 before. It counts once those closes exist. A close inside its window is read when the
  window ends, never early.
- Live reading at close: `sampo prove --rollup` prints the user's-words count and Sampo's-notes count, and they sum to
  the old meaning count on the same day (a test holds the sum).
- Exam kinds: #6's proof scenarios are unchanged; the end-of-run exam reads them.

## Long-horizon goal (end of run)
Every clause a user writes in an M or L request has a failable check before its first edit, and the rollup's
user's-words count falls by proof, not by relabelling.

## Risks
- Plan friction: one more gap on user M and L plans. Kept to clauses with no criterion at all, and escapable by naming
  the clause in Non-goals, which is honest scoping, not a waiver.
- Bind false positives: a shared-word bind can pass a clause that isn't really checked. The close-time label stays as
  the second net.
- Count honesty: the split must add up to the old count. A test holds it, so the split can't quietly shrink.

## Lean
No new verb, no hook. One call in the gate and one tag in a kind. Smith's plan check is untouched.

## Tier share
Brief 1 is tier 4: proof of intent beyond an LLM lens, the #6 tier-4 gap gen-2's gap map named.

## Hands to the next generation
The before and after share on user closes, and the Sampo's-notes count as its own lead: provenance lines inside Raw
request are a capture-format question for #7.

## Done when
T-2914's three criteria are green, the before and after counts are in its log, and MASTER.md (sampo prove --rollup,
the plan gate) and CHANGELOG say it.
