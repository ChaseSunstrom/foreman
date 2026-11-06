# T-2228 review (fm-reviewer, self + adversary, two passes)

Pass 1 (first fix: quotes of gone lines resolved):
- MEDIUM, fixed: a FAIL re-quoting a trivially edited line's old text passed the put. Reworked so a finding follows its line to the closest current one (difflib) and blocks there; the reader never sees gone text.
- LOW, fixed by the rework: gone entries lingered in previous-reads.

Pass 2 (rework):
- MEDIUM, fixed: the re-key was compared against the re-keyed list, so a pass that dropped findings never cleared genesis-reads.json; a stale finding could later attach to a new similar row. Now compared against what was stored; test checks the file after a pass.
- LOW, fixed: cutoff 0.6 matched unrelated templated rows (measured: 109 of 160 coverage rows have a sibling >= 0.6, max 0.77). Now 0.8 (the T-2205 test's real revision is 0.83).
- LOW, fixed: two findings re-keyed onto one line both stayed; now one per line, the newest.
- Checked, no finding: normalization only widens over markdown and quote marks, the 8-character floor applies after it; the DRIFT caller can only move "didn't count" to "drifted"; ACCEPTED write correct.
