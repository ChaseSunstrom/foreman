Verdict: changes needed (2 HIGH, 6 MEDIUM, 5 LOW); fixed or skipped with reason. Reviewer: one foreman:fm-reviewer, five lenses, read-only.

## lens: edge
- HIGH — in a builder lane the criterion went green unrun: trust is per realpath, so the lane's copy was untrusted and every untested finding became a NO_RUN lead, exit 0. FIXED: _lane_trusted maps a lane path to the main checkout's same tree; and any lead not shown fixed exits 1. Test: a git worktree lane is red, then green after the fix there.
- HIGH — a fix that broke the suite (or a timeout, an instrument failure, the deadline) read green. FIXED: --only exits 0 only when the finding is gone from fm find or shown fixed (marker ran; not re-found cold); every other lead is 1 ("still open"). Test: a broken suite keeps it red. Note: once a test names the function fm find stops reporting it (gone = fixed); the suite's own redness is the full gates' job at close.
- MEDIUM — an unknown id printed 0/0 and exited 0. FIXED: it says "fm find no longer reports it (or the id is from another tree)"; still 0 (gone is fixed). Test added.
- MEDIUM — --limit was spent on kinds no check here can prove. FIXED: provable kinds (COLD + untested) sort first. Test (SQL lead ranked first) is red without the fix.
- MEDIUM — the receipt hid held and cut findings. FIXED: found, held and tried counts. Test asserts them.
- LOW — twin numbers shift when the first twin is fixed. Accepted (documented in MASTER as keyed like fm find --capture).

## lens: adversary
- No repo text reaches the criterion: hex id and a shlex-quoted path. --capture/--only run repo code only on the user's yes.
- LOW — receipt wrote file names raw (line injection into research/). FIXED: json.dumps(c.plain()), evidence c.plain'd.
- LOW — a tree path with a newline would split the criterion line. FIXED: --capture refuses control characters (exit 2). Test added.

## lens: intent
- MEDIUM — the skill's step 4 named fm task prove, which can't work for these tasks (no test files for cold kinds; the untested fix is the test). FIXED: step 4 now closes with fm task finish --run "<criterion>"; the red is the filing-time proof.

## lens: operator
- MEDIUM — each --only re-check scans and runs the suite up to three times. SKIPPED with a ponytail note: per task it is one finding; cache per tree id if it drags.

## lens: maintainer
- LOW — duplicated --capture validation strings with fm find. SKIPPED: two strings, not worth a helper.
- LOW — missing tests for lanes, broken suite, unknown id, receipt counts. FIXED (all four added).

Noticed: a folder named "..cache" was treated as outside the project. FIXED in the same change (rel == ".." or starts with "../").
Also found in the gates: the rules line I added pushed rules past fmdoctor's 6400-char budget (test_doctor, test_board_verbs). Reverted; the leads note and the skill carry --capture.
