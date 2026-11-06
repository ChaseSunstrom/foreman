T-2372 review (fm-reviewer, one pass): changes needed; fixed in 4814b463 before merge, red first.
HIGH fixed: fail-open by chmod 000 (safe_gaps returned []): now per tool, an unreadable tool is refused by name; only a broken ledger read fails open.
HIGH fixed: the use proof was a name mention in a transcript (cat/git add counted; no transcript closed anyway): transcript dropped; an fm [ran] evidence line after green must run the tool in executable position, exit 0.
Fixed: red-then-green needs the test path in executable position; the scratch runs get the user env minus fmbench.CREDENTIALS.
Open: runs() is lexical, so cd tools && python3 x.py or python3 -W error x.py are false negatives (the refusal names the form that works).
