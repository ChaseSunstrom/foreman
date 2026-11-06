Verdict: approve with nits (tests not run by the reviewer).

## lens: intent
- MEDIUM — fmgenesis._misses — the exam only checked each clause head as a substring, so a draft with nine heads (or a stray "generally") passed: a format check. FIXED: each clause's whole line, whitespace-normalised, must be in the draft; test drops a body but keeps the head word.
- MEDIUM — drift/check — generations had no mechanical grade on the intent. FIXED: drift(p, n) from gen 2 fails a seed without a '## Standing intent' section holding the file verbatim (fm genesis seed writes it); tested both ways.
- LOW — draft test repeated the production expression. FIXED: asserts every intent line is in the draft.

## lens: adversary
ok. Trusted repo file; _fence covers the tag; plain_lines in the charter; the site escapes both parts.

## lens: edge
- LOW — intent() has no OSError guard; same as genesis.md's read in draft. No change.

## lens: operator
ok. ~430 Haiku input tokens more per cold read.

## lens: maintainer
- LOW — the 'given' exemption has no test. Skipped: needs an arm whose draft lacks only the intent; the exemption is one condition on one line.
- LOW — JS and Python parsed the clauses with two regexes. FIXED: intent_clauses() parses once; genesis.json's intent is the parsed list the page renders.
