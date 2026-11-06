# T-2235 five-lens review (fm-reviewer): approve with nits; all fixed or decided

- MEDIUM adversary, fixed: the proof path's raw quoted fm prove's evidence (which embeds the repo's file name) without defang. Now title and raw are defanged whole; a test feeds instruction-like evidence with a benign finding.
- MEDIUM operator, fixed: when capped, stdout said only "none new". `filed_line` now says "none (5 finder tasks open already: finish or drop some)" for fm find and fm prove.
- MEDIUM maintainer, fixed: tests added for the scout capture's defang, a partly free cap (4 open, ask 3, get 1) and the stderr note.
- LOW operator, fixed: the note names fm find, fm prove and the scout, prints only when the cap cut the filing to 0 and an unheld lead existed; `opened + 1 > OPEN_CAP` simplified away.
- MEDIUM intent, decided: no daily cap on --capture. An explicit --capture N is the user's or the session's own ask, and the open cap is what stops a flood; the scout's unattended day cap (FIND_DAY) stays.
- LOW adversary, by design: the scout's find probe files under its own caps and counts toward OPEN_CAP; noted in MASTER.
- LOW edge, not changed: one realpath per listed file (unmeasured; a per-directory cache if a large repo shows it); a second git listing timing out falls back to the walk.
- Checked, no finding: no path outside the tree is read (.. or absolute index paths, case/Unicode, symlinked root, .git); `remember` has no other caller; capture has two callers.
- Out of scope, captured as T-2237: COLD re-finds labelled proven, prove's deadline, triple-quote tracking.
