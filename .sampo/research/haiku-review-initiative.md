# Cold Haiku review of #1 (Initiative) code, 2026-10-30 (a different model than the builder's, same family)

Scope: fmfind.py, fmprove.py, fmscout.py, fmhooks._leads_note. Adversary + edge. Two claims spot-checked and confirmed (marked ✓); the rest unverified leads.

- ✓ MEDIUM edge: fmfind.py:150 skips every path with a dot-directory component even when git lists it, so tracked .github/workflows/*.yml and other dot-dirs are never scanned by any finder, secrets included.
- ✓ MEDIUM edge: `fm prove --capture N` (fmprove.py:326 → fmfind.capture, fmfind.py:508) enforces only N per run: no 24-hour cap (FIND_DAY) or open-count cap (MAX_OPEN) as probe_find has, and its briefs carry no key probe_find counts.
- MEDIUM adversary: repo text goes into captured task titles/raw through c.plain only (fmscout.py:390, fmfind.py:524-528), and a tree whose recent commits all carry the user's email gets no confirm step, so its leads are captured for the drive unattended.
- MEDIUM adversary: COLD kinds (docs, dep, secret) count as proven by re-running the same finder on a copy, which holds by construction; `dep` reads the host interpreter (fmfind.py:394-428).
- MEDIUM adversary: fmfind.py:149-158 lstat checks only the last path component; an intermediate symlinked directory (worktree diverged from the index) is followed.
- LOW edge: fmprove.py:249,266 checks the deadline only between candidates; `_pick` can run two 300 s suites past it.
- Noticed: fmprove.py:289-291 records --yes-run consent before argument validation; fmfind.py:74-79 triple-quote tracking can flip on '"""' strings or `# """` comments and hide later defs from the untested finder.
