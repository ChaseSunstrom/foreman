## Verdict
Changes needed, but only for the MEDIUM items. I read the code and could not run it; no shell was available. The 9 PlanContent tests are green in the task's recorded evidence.

## lens: edge
- MEDIUM — fmcore.py:2655-2658, 2703 — Numbered options with indented sub-bullets are mis-split. When bullets outnumber numbered markers (3 options plus 4 detail bullets), `_split_options` takes the bullets as the options. The first option line, which holds its `fails if:` and any `use what exists:` label, is dropped. Every bullet is then refused with "option N has no likely outcome", and the exists and less checks look only at bullet text. A normal plan written as `1) … fails if: x` with `- touches fmcore` lines under it is refused. A nested `1.` or `2.` inside option text also becomes a premature marker (:2651). Fix: use the numbered, lettered or word run when it reaches 3 or more, and fall back to bullets only when no run does. Confidence: high from reading, not run.
- MEDIUM — fmcli.py:2962 — `fm batch` writes a fixed Interpretation with no readings and no "ruled out". For 3 or more members the host is tier M, so `fm focus` now flags a gap. The builder rewrote the Interpretation inside test_batch.py:53 instead of fixing the generator. Fix: have the batch text carry "Reading 1: all as one batch. Reading 2: each alone; ruled out, …". Confidence: high.
- LOW — fmcore.py:2671 — `_distinct` measures overlap against the shorter part, with no stopword filter. A short option such as "do less: skip it" can merge into a long earlier one, and a short second reading can merge into a long first one. Fix: ignore stopwords, or require the shorter part to have 5 or more words before it can merge.

## lens: adversary
- MEDIUM — fmcore.py:2688-2689 — Bullets count as readings. Interpretation is checked with `_count_options(it)`, whose default is `bullets=True`. Two scope bullets such as "- adds a flag" and "- updates docs" pass the 2-reading check. This is the most common way an Interpretation is already written. Fix: count only Reading/Option/lettered/numbered markers for Interpretation, and give `_split_options` a matching `bullets=False`.
- MEDIUM — fmcore.py:2707-2711 — The exists and less checks run over the joined options, so one option ("extend the existing gate, minimal") satisfies both. The label alone passes: fmcode.py:2770-2774 ships "2) use what exists: a human plan first" in every fm code task, which is not a real repo option. Fix: require the exists and less matches to come from different options, and give fm code's harness-written plan a plain exemption instead of boilerplate.
- LOW — fmcore.py:2641 — "no other reading" or "rejected" bypasses the check, with no why. The acceptance criterion asks for the reading ruled out and why. Fix: require a clause after the cue (about 5 words).
- LOW — fmcore.py:2637 — The outcome words include `but|only if|stays|gives|cuts|results|likely`, so almost any English sentence qualifies. Fix: narrow it to `fails if|likely outcome|breaks|→`.

Keywords are an acceptable floor for a plan gate only if nobody calls it substance. The brief itself says the calibration ledger scores whether the choice was right. As built, a label such as "use what exists:" satisfies the check, and fm code does exactly that.

## lens: operator
- LOW — fmcore.py:2636 — `_CHOICE_AT_RE` is quadratic on a long run of newlines or dots: `\W*` backtracks from every `[.\n]`. About 20,000 blank lines take several seconds, and `stage()` runs this on every board render. Fix: bound it to `\W{0,8}`, or cap the part at about 20,000 characters.
- LOW — fmcore.py:2731 — Every queued, unstarted M or L brief written the old way now shows stage "planning". `fm lane` builds refuse it (fmlanes.py:478, 677) and `fm run` stalls on it. Per call the cost is small: about ten regexes per section and no tokens. Add one line to the close note saying the old queue needs re-planning.

## lens: maintainer
- LOW — fmcore.py:2627 vs 2644 — Two option parsers disagree: a set-based run versus in-order marks, and bullets taken by "more than" versus "max". `n` is computed from one and the option numbers in the messages from the other. Fix: derive the count from `len(_split_options)`.
- LOW — plugin/tests (46 uses of "use what exists" across 26 files) — The plan fixture is pasted by hand in each file. The next gate change touches them all again. Fix: add one shared `valid_m_plan` helper.
- LOW — CHANGELOG.md — No T-2335 entry, although step 4 is ticked done.

## lens: intent
- **False refusals from generators:** `fm code`'s plan passes. Its Interpretation contains "ruled out" and its three options carry outcome words. Stray digits such as "4.5" in the model name only over-count. `fm batch` fails (see edge). `fm intake` only captures, so it is unaffected.
- **Regex cost:** the 5,000-bullet case is capped at 40 parts, so it is fine. The `_CHOICE_AT_RE` case above is the only superlinear one I found.

## Acceptance criteria
- Refuses fewer than 2 readings, an option with no outcome, and a plan with neither a use-what-exists nor a do-less option: met by the code and tests, with the bypasses above.
- Near-copies count once: met.
- Each gap names its fix: met.
- A started task isn't re-gated: met (the `_started` guard).
- S is untouched: met.
- Verify command: not run by me; the recorded evidence shows it passing.

## Implicit decisions
- 0.8 overlap threshold against the shorter part.
- 40-option cap.
- Bullets count as options and as readings.
- "Ruled out" wording bypasses the reading check.
- Old unstarted briefs are re-gated rather than grandfathered.

## Not checked
- The diff against `foreman/build`.
- The full test suite.
- The wording of planning.md.

**Noticed:** fmhooks.py:767 and 845 auto-create tier M SECURITY tasks with no Interpretation or Approach, so each needs a manual plan before focus.
