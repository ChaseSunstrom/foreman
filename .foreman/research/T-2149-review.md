**Verdict: approve with nits.** I found no defect that breaks the acceptance criteria. I did not run the tests or the `python3 plugin/tests/run.py test_exam.ExamAuthors` command, because I was read-only.

## lens: intent
Ok. The child now writes the whole key. `_keyed` (`plugin/lib/fmexam.py:414-446`) builds only the child's items, and `CHILD_DEFECTS` (`:508`) no longer lists the goal kinds, so no template item is added. The 4-to-6 count, the one-of-each-kind rule and the same-function rule are enforced at `:586` and `:608-613`. The CHANGELOG entry matches the code.
- LOW — `plugin/lib/fmexam.py:608-613` — Two README items can cover the same gap: the duplicate-function check covers only code and test items. Two items with the same line, or a pattern that also matches the other item's line, get closed by one added line. Nothing catches this, because the planted README has no item lines and the clean README has all of them. The key then quietly holds fewer than 4 distinct gaps. — Fix: reject duplicate README lines or patterns, and reject any README pattern that matches another README item's line. — confidence 70%

## lens: adversary
- LOW — `plugin/lib/fmexam.py:594` and `:717` — The child's regex runs with no time limit, at authoring (`re.search(pat, line)`) and at grading (`_static` over README text up to 1 MB). Reproducer: `line="a"*30+"!"`, `pattern="(a+)+$"`. The same pattern backtracks without end on any README line it can't match. One such pattern freezes the whole `fm exam gen` or `fm exam grade` process, since Python's `re` has no timeout. The child sees only template text, so this needs an accidental pathological pattern, not an attacker. — Fix: reject a pattern with a nested quantifier such as `\)[+*]`, or test it in a short-timeout subprocess. — confidence 55%

## lens: edge
Ok. A bad item drops the whole scenario with its reason. An anchored pattern such as `^…$` fails on the clean README, because `_static` uses no MULTILINE, so it is dropped and does not slip through. Every other path I traced fails closed.

## lens: operator
- LOW — `plugin/lib/fmexam.py:753-759` — `_check_one` now runs, per code item, a check on the planted repo, a check on the clean repo and a suite with the overlay. A key with 2 or 3 code items is therefore about 2 to 3 times the builds of the old single-bug key, which matters most for Rust and C. The cost is bounded by the pool of 8 and the build timeouts. The number of child calls is unchanged, at one per scenario. — Fix: none needed; record it next to the T-2140 note about default gen cost. — confidence 60%

## lens: maintainer
- LOW — `plugin/lib/fmexam.py:507,529` — `CHILD_KINDS` still holds a text for the goal kinds that nothing reads now (`_author` never gets them), and only its keys gate the child author at `:640`. `and s["kind"] not in GOALS` at `:529` is now dead. — Fix: drop the goal text and the dead clause, and say in a comment that the keys also gate `gen`. — confidence 85%
- LOW — `plugin/tests/test_exam.py:311-316` — Four reject modes are tested. These rejects are not: more than 6 items, a key missing a kind, a bad `kind` value, a `says` that is missing, and a test item whose function is still called in another test, which `_check_one` catches. Each is a branch with its own message. The stub is Python-only, so `_keyed` for the other five languages is unexercised. — Fix: add stub modes `many`, `nokind` and `badkind`. — confidence 80%

## Acceptance criteria
- **Child keys hold only the child's items, with one code, one test and one README item; check passes; the oracle closes all, empty closes none:** met by the code, not run by me. The test at `test_exam.py:266-296` asserts the kinds, the `tf` flags, `fm exam check` ok, the oracle closing every scenario and the empty arm closing none.
- **Under 4 items, two code items on one function, a README regex the planted README already matches, or a bad regex is dropped with its reason:** met by the code, not run by me. The four stub modes at `:311-316` assert the reasons.

## Implicit decisions
- Resume marks items at index 2 and 5 as met, whatever their kind.
- A test item is checked only by the regex `\bF\(` in files with "test" in the name, the same weak check as the old "untested".
- One bad item drops the whole reply, with no retry.
- Key names are `kind+position` (code1, readme4).
- Limits: `says` ≤1000 characters (cut to 300), the README line is cut to 200, and the pattern is ≤200.
- A goal child's `request` is never read.

## Not checked
MASTER.md (the diff leaves it out, one line over 4000 characters), the non-Python languages (no stub), and the large-file and hotspot pre-audit notes for CHANGELOG.md and MASTER.md.

Noticed: none
