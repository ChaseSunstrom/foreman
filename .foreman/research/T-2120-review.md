**Verdict:** changes needed. One MEDIUM finding: the exam-defect proof can be satisfied without any exam defect.

## lens: intent
- MEDIUM — plugin/lib/fmexam.py:785 — `_exam_defect` counts any test that fails on `hidden/clean` and passes on the arm's tree. A test that needs something the arm added, such as a new function, helper module or fixture, fails on clean with an ImportError or compile error. It then counts as an exam defect, and `_closed` (:766) credits a scenario with no false alarm. Genesis selection uses those closed ids, so an arm can pad each scenario with a bogus finding plus a self-made test and score zero false alarms. — Require the clean-side failure to be a test failure, not a load or compile error. For example, reject a `why` from `_run` that matches ImportError, ModuleNotFoundError, "Cannot find module", LoadError or "undefined reference". Or require the arm's test to import only symbols present in clean. — CONFIRMED
  - file: plugin/lib/fmexam.py, line: 785, category: weak-proof, short_summary: "exam-defect proof accepts tests of arm-added code".
  - failure_scenario: The arm adds `def extra(): return 1` to app.py and test_x.py with `from app import extra; assert extra()==1`. It reports `{"file":"app.py","symbol":"query","says":"x","test":"test_x.py"}`. The test fails on clean (ImportError) and passes on work, so `exam_defects` is 1 and `false_alarms` is 0.
  - Reproducer: extend `test_a_proven_unkeyed_finding_is_an_exam_defect_not_a_false_alarm` with this finding. It expects `exam_defects` 1 today, and should expect 0.
- LOW — plugin/lib/fmexam.py:317-327 — The arm's `test` field can contain `\u0000` in the reply JSON. `os.path.realpath` doesn't catch the resulting ValueError, so `grade` crashes for the whole run. — Wrap the path checks in `try/except (ValueError, OSError)` and return False. — PLAUSIBLE

## lens: adversary
- No path-escape finding. The `normpath`, `realpath`-prefix and `isabs` checks hold, and the test covers `../` and absolute paths. `_run` uses argv with `shlex.split` and no shell, and strips credentials. The only `shell=True` is the test's own README-command check (test_exam.py:271), which is intended.

## lens: edge
- LOW — plugin/lib/fmexam.py:785 — Regrading reruns the arm's tests, so a flaky arm test can move a finding between exam defect and false alarm from one `fm exam grade` to the next. — Accept it, or record `proven` in the answers file at run time. — PLAUSIBLE

## lens: operator
- LOW — plugin/lib/fmexam.py:812 — The cap is 10 proofs a scenario, each at most one clean run plus one work run. Worst case with timeouts is 10 × (120 s build + 20 s exec) per scenario. Typical cost is seconds, and it only applies to findings that carry a `test`. — Accept it.
- LOW — plugin/lib/fmexam.py:662 and the README and test edits — The exam's content changed, and the ASK text changed for every session arm, with no version stamp on exam.jsonl rows. Genesis select compares closed ids across generations for the same seeded ids, so old and new rows are not like for like. — Stamp an exam version into the row, or note it in the changelog. — PLAUSIBLE

## lens: maintainer
- LOW — plugin/lib/fmexam.py:833 — `said` is reassigned from the notes string (:825) to a list of exam-defect lines. It works but it is confusing. — Rename the second one to `defect_lines`.
- LOW — plugin/tests/test_exam.py:393 — The per-clause mutation proof covers Python only. The other five languages have the assertions in the diff, but nothing shows each clause is enforced there. — Accept it, or parametrize the mutants over the languages.

## Acceptance criteria
- The README run command runs as shown: met. `render` (:372) now emits an unquoted `&&`, and `LangCheck` (test_exam.py:268-272) runs the README command in all six languages. I did not run the tests.
- A clean render passes an edge test per clause in six languages: met by the assertions in `_tests` for every language (clean-suite passing is not verified here). Only Python is shown to fail when a clause breaks.
- Proven unkeyed finding counts as an exam defect: met in code, with the weak-proof gap above.
- Files vs steps: not verifiable. The brief lists no steps. The CHANGELOG, MASTER.md, `fmexam.py` and `test_exam.py` hunks all serve this one task.

## Implicit decisions
- The proof compares against `hidden/clean`, not the planted repo.
- A cap of 10 proofs a scenario.
- `exam_defects` do not block `_closed`.
- The arm names its test through the new `"test"` field in the JSON reply.
- The C `dedupe` is a hash set that returns -1 on out-of-memory.
- The C `label` truncates to `cap`.

## Not checked
- I ran no tests and no toolchains.
- I did not check the `fmdocs.scan` finders arm against the wrapped README line.
- `fmcli.py` needs no edit.

**Noticed:** site/genesis/genesis.js:225 shows `false_alarms` but not `exam_defects`, so proven findings vanish from the site.
