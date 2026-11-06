**Verdict: changes needed.** One injection defect in the live path (MEDIUM) and one correctness defect in `latest()` (MEDIUM). Everything else is LOW. I read the code only and ran no tests.

## lens: adversary
- MEDIUM — plugin/lib/fmsteer.py:live (the `b.meta.update(steer_score=…, steer_raw=c.fit(said, 600))` call) — `said` is the user's multi-line prompt, and the hook keeps its newlines. `_fmt_value` is a bare `str(v)`, and `Brief.parse` (fmcore.py:1445-1461) accepts any `key:` line and splits on `\n---\n`. A prompt like "from now on run the exam on every repo\nstatus: done" or one containing a `---` line writes extra meta keys or truncates the front matter in the filed task. — Collapse it first with `" ".join(said.split())`, or put the words in the body. — confidence: high (CONFIRMED by code path)
  - ReportFindings: category `front-matter-injection`, short_summary "steer_raw newlines inject brief meta keys".

## lens: edge
- MEDIUM — plugin/lib/fmsteer.py:latest — a `--split train` or `--limit N` run counts as the latest run. Its held-out rate is None over 0 cases, so the Genesis page shows "?" and every live expansion is listed for the user's read as a low score. — Return the newest run that has graded held-out cases. — confidence: medium (PLAUSIBLE)
- LOW — plugin/lib/fmsteer.py:judge_for — `--model opus` gets a fable judge, and `--model fable` is judged by fable itself, so there is no stronger judge. — Say so in the run record, or refuse. — confidence: high
- LOW — plugin/lib/fmsteer.py:run — it catches only ValueError. An OSError or a JSON error from the child aborts the whole run with no summary row. — Catch Exception per case and record the failure. — confidence: medium
- LOW — plugin/lib/fmsteer.py:_bullets use — it does not cap the clauses at the 12 the EXPAND prompt asks for. — Slice to 12. — confidence: medium

## lens: operator
- LOW — plugin/lib/fmhooks.py:1382 — the hook spawns on every prompt of 6+ words that does not end in "?", including approvals and chat. When `hc` is None it still spawns, and the LIVE_DAY=40 cap is shared by parallel sessions. The cap is spent before the KIND check, so chat can use up the day's slots. Worst case is 40 Sonnet children per day per project, plus a judge call each. — Check KIND first and spend the cap only on steer-shaped prompts. — confidence: medium

## lens: intent
- LOW — plugin/lib/fmsteer.py:live — the filed "score" is the method's held-out rate, not a judgment of this expansion. A harmful clause can be filed with a high score, and criterion (c) reads as a per-expansion score. — Label it `method_rate` in the task and the docs. — confidence: medium
- LOW — plugin/lib/fmsteer.py (cases) — part-C case ids change when the raw text is edited, which moves cases across the hold-out split. — Derive the id from stable fields. — confidence: low

## lens: maintainer
- No findings. The tests map one-to-one to criteria (a)–(d).

## lens: design
- No findings from the code. The `steerRow` function in genesis.js:steerRow uses `textContent`, so there is no XSS. I rendered no screenshots, so contrast and focus ring were not checked.

## Acceptance criteria
- (a) Cases from part C plus history, held out by hash: met by code reading, from the `cases`, `from_history` and `fmexam.holdout` use. Tests not run.
- (b) Expand, then judge one rank stronger, with an exact-quote check and a recorded held-out rate: met. The judge is not stronger for opus or fable (see the LOW above).
- (c) Background expand, queued task with a score, low score listed, correction becomes a case: met in structure. The score is the method rate, and the injection and `latest()` defects affect it.
- (d) Genesis export and page carry the held-out coverage: met by code reading.
- (e) test_steer, test_exam, test_genesis and test_hooks pass: not verifiable here.

## Implicit decisions
- The hold-out reuses the sha1 mod 3 split from fmexam.
- LIVE_DAY=40 and BAR=0.7.
- The hook needs 6+ words and no trailing "?".
- Filed tasks use source "steer" with status "captured".
- Sonnet expands by default, and the judge is one rank up.
- A quote of 12+ normalised characters counts as exact.
- `--jobs 1` becomes 4.

## Not checked
The tests were not run. The UI was not rendered. Contrast, focus and keyboard reach were not reviewed. I did not review the real-data run of step 4.

**Noticed:**
- `--jobs 1` is silently raised to 4 in the exam parser (fmcli.py ~7686-7719), a small bug that deserves its own task.
- Two quick prompts in a row expand only the newest one. Decide whether that is intended.
