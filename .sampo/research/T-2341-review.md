**Verdict: changes needed.** One HIGH problem, because the tests on the branch break once T-2335's plan gate is merged in. Several MEDIUM findings follow. I read the code and ran no tests, because I have no shell.

## lens: edge
- HIGH — `plugin/tests/test_second.py:91` — The `_RivalBase.new` fixture uses `approach="1) dict 2) redis 3) file Choice 1 (90%): dict"`. Main's T-2335 gate (`_content_gaps`) now also requires an outcome or failure mode on each option, a use-what-exists option and a do-less option. After the merge, every `self.focus(x, True)` call fails on those gaps rather than on the rival gap. Examples: `focus(sure, True)`, `test_answering_every_rival_line_unlocks_focus`, and the L unlock test. The `return gaps + rival_gap(b)` change probably merges textually (my guess, no git to confirm). The hunks are separate from T-2335's rewrite, and `plan_gaps` already skips harness plans through `own`. Fix: give the fixtures T-2335-compliant text, such as `1) … fails if: … 2) use what exists: … fails if: … 3) do less: … fails if: …`. Then re-run `test_second` on the merged tree. — high
- MEDIUM — `fmsecond.py:147,206` — An S brief has no Interpretation. `chosen_reading("")` returns `""`, and `_overlap(top, "")` is 0, so `rival_split` is set whenever the rival gives a specific top reading. The S one-way tasks, which are the only S tasks that reach this code, would all be marked ambiguous. Fix: set no split when the plan has no Interpretation text. — high
- MEDIUM — `fmcore.py:2672` — `_ONE_READING_RE` misses "no other honest reading". Main's `_RULED_RE` accepts exactly that phrase for T-2335, so the M "claims one reading" trigger is skipped depending on the wording used. Fix: add `no other (honest )?reading` to the regex. — medium
- LOW — `fmcore.py:2680` — `FOREMAN_NO_RIVAL=0` turns the gate off, because any non-empty string counts as set. Fix: test `in ("", "0")`. — high
- LOW — `fmsecond.py:201` — A rerun in which the child rewords its items adds fresh open lines, so the gate can keep moving. Fix: nothing needed now. — low

## lens: adversary
- MEDIUM — `fmsecond.py:57-68,186` — The prompt says "at most 4 bullets" but `_bullets` does not enforce it. A child that returns 100 bullets under a heading gets 100 open Dissent lines and 100 required resolves. Fix: `readings[:4]`, `approaches[:4]`, `modes[:4]`. — high
- MEDIUM — `fmcore.py:2689` — The gate only checks that "Rival plan" is non-empty. `fm task set ID --section "Rival plan" --text x` clears it with no child call. Fix: store a `rival_at` or `rival_model` meta key in `rival()` and gate on that. — medium
- LOW — `fmsecond.py:186` — A reply with no usable bullets saves "none" lines and passes the gate. Fix: treat zero bullets as a failed read and write a note. — medium
- Verified clean: the child gets only the redacted Raw request and the map. It never gets the title, steps, approach or criteria. All child lines pass `c.plain`, `c.defang` and `c.redact` before they reach the brief. A sensitive project sends nothing.

## lens: operator
- MEDIUM — `fmcore.py:2669,2684` — `HARD_RE` applies to every tier, S included. In the task store, about 123 of roughly 2,400 task files have a step line matching it. These are release and push chores, `fm lease drop`, `fm lane merge`, "delete dead code", "send a message", and the like. Each one is held for an opus child call (about $0.05–0.10 and 20–60 s). Across sessions that comes to roughly $1 and a few minutes per 100 tasks, which is small. The cost is that explicit user requests ("push to main") and trivial S steps get a pointless gate. The gate also reaches the S/M `fm lane brief` builder dispatch, through `fmlanes` lines 478 and 677. Fix: for S, use only a narrow irreversible set (deploy, publish, release, migrate, delete), or skip the gate when the Raw request itself names the verb. — medium
- LOW — `fmcore.py:2679` — The docstring says `FOREMAN_NO_RIVAL` is for "a headless run", but nothing sets it for `fm run` or `fm serve`. Fix: set it there, or reword the docstring. — high
- LOW — `plugin/protocols.json:4` — The M row leaves out the one-way-step trigger. Fix: mention it. — high

## lens: maintainer
- MEDIUM — `plugin/tests/helpers.py:273` — The global off-switch is the reason existing fixtures pass (`Stages` failed in the 15:11 check without it). No test shows an ordinary S, M or L plan reaching "ready" with the gate on. Fix: one gate-on test of `stage()`, and one of `fm next`, on a plan that has passed the rival read. — medium

## lens: intent
Nothing separate beyond the above.

## Acceptance criteria
- **1.** Met in code: it writes the Rival plan section, creates Dissent lines, gates focus, and names `fm second rival ID`. Not verifiable on the merged tree until the fixtures are fixed.
- **2.** Partly met. `rival_split` is set, and the M "optional" panel row is removed. "Brief 8 reads it" cannot be verified: no consumer of `rival_split` exists in main's `plugin/`.

**Noticed:** nothing in `plugin/` outside the test files reads `rival_split`, so T-2338's ambiguity routing is unwired.
