T-2352 review (fm-reviewer, one pass): changes needed; fixed before close (tests added after the fixes, so not seen red first).
HIGH fixed: the gate ran the branch's own fmreplay.py/bench_hooks.py (a branch could print passing numbers) with the full env: the base's harness is copied into the branch tree, and subprocesses get only PATH/HOME/LANG/LC_ALL/TMPDIR/FOREMAN_HOME plus an empty FOREMAN_STATE.
HIGH fixed: the yes wasn't tied to a commit and the branch name was merged after minutes of checks: lane merge resolves one sha, the gate and git merge use it, refusals carry the sha, and approved() needs a yes after a refusal of that same sha.
MEDIUM fixed: git archive honoured the branch's .gitattributes (export-ignore hid rules growth): trees are written from ls-tree + cat-file.
MEDIUM fixed: temp FOREMAN_HOME made core-path rules judge as ordinary paths: real FOREMAN_HOME, empty FOREMAN_STATE.
MEDIUM fixed: a None verdict passed: any non-string branch verdict refuses; a failure both trees share doesn't.
MEDIUM fixed: fm serve's _integrate_lane merged --ff-only around the gate: gated. fm pr train captured as T-2430.
MEDIUM fixed: the branch's own budget was read: the base's (a new fixture takes the base's tightest).
LOW fixed: the bench now runs for any non-test non-prose plugin change or CHANGELOG.md (data files, importlib) instead of an import walk; ZeroDivision guarded.
Open: the branch's fmguard/hook code still runs before the yes (inherent: it is what's measured); base results aren't cached (2-4 min per gated merge, noted ponytail); sub-band growth across merges is caught only by the doctor and the ship ratchet.
