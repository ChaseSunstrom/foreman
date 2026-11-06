**Verdict: changes needed.** The main hole is that the "gitignored and identical to the checkout" rule reads attacker-writable ignore rules. I read the code but could not run anything, so every finding below is from the code path only.

## lens: adversary
- HIGH — `plugin/lib/fmdoctor.py:1292-1299` (extras branch) — Untracked install files pass when `git check-ignore` says ignored and the bytes equal the checkout's copy. The root `.gitignore` has broad rules: `*.pyc`, `local/` and `state/` at any depth, and `*.bak`. Concrete input: a worker (or anything that can write the checkout) drops `plugin/lib/json.pyc`, a sourceless pyc that shadows stdlib `json`. It is never committed or reviewed and is invisible to `git status` and the judge's diff. The directory marketplace copies it into the install, the bytes equal the checkout's copy, and doctor auto-accepts with no human step. Fix: replace the check-ignore test with a hard allowlist of the two known generated paths (`mods/foreman-ui/tsconfig.json` and `mods/foreman-ui/.claude-plugin/types/**`). Refuse `.pyc`, `.so`, `.py`, `.js`, `.ts`, `.tsx`, `.sh` and any exec-bit file among extras. — confidence: medium. The Python shadowing semantics are certain. I did not confirm the hook's `sys.path` order.
- MEDIUM — `plugin/lib/fmdoctor.py:1292` — The ignore verdict comes from the working-tree `.gitignore`, `.git/info/exclude` and `core.excludesFile`, none of which are in HEAD. The root `.gitignore` is outside `plugin/` and `mods/foreman-ui/`, so it is never copied or compared. Editing it widens what counts as "ignored" without touching any compared file. Fix: the same allowlist, or evaluate against HEAD's `.gitignore` only.
- MEDIUM — `mods/foreman-ui/tsconfig.json` (gitignored, exists in the checkout now) — `compilerOptions.paths` or `extends` can redirect module resolution, and Bun and tsx apply tsconfig at runtime. So an attacker-written ignored tsconfig can steer which code `register.tsx` loads. The test `test_an_ignored_file_equal_to_the_checkouts_is_accepted` blesses exactly this. Fix: accept tsconfig only if it has no `paths`, `extends`, `plugins` or `baseUrl`, or require it to equal a tracked template. — confidence: medium. I did not verify which runtime loads the mod.
- MEDIUM — `plugin/lib/fmdoctor.py:1280` (and `_tree_hash` at 1116) — `__pycache__`, `node_modules`, `.venv`, `.pytest_cache` and `.git` are never compared. A planted unchecked-hash `.pyc` in `plugin/lib/__pycache__/` executes, and `node_modules/react` would resolve for the `.tsx` hooks. The docstring discloses this, but the task's "file for file" claim does not hold for executable content. The hole existed before T-1441, but the new path now vouches for the tree. Fix: reject any skipped folder that holds files, and only tolerate `__pycache__` if empty. — confidence: medium. It needs write access to the install cache.
- MEDIUM — `plugin/lib/fmdoctor.py:1269` — `ls-tree HEAD` trusts whatever branch or commit is checked out. The live checkout is on `foreman/build`, not `main`. A worker's commit to `plugin/` is auto-accepted the moment the install is refreshed, which is the human gate this check existed for. Also, `git replace` refs are honoured. Fix: require HEAD to be an ancestor of, or equal to, a reviewed ref such as `main`, or a recorded released sha. — confidence: high.
- LOW — `plugin/lib/fmdoctor.py:1269,1292` — `c.foreman_home()` reads `FOREMAN_HOME` from the environment. If a project's `env` can set it, doctor consults an attacker repo. If only `FOREMAN_HOME` is set, `state_dir()` also moves, so the supply baseline was already forgeable and this adds nothing. Setting `FOREMAN_STATE` separately makes it count. Fix: derive the checkout from `__file__`, or compare against the realpath of `~/.claude/foreman`. — confidence: low.
- LOW — `plugin/lib/fmdoctor.py:1301-1308` — Time-of-check/time-of-use. The tree is compared at t1 and re-hashed at t2, but it is compared with `cur` from t0. A tree that is evil at t0 and t2 and HEAD-equal at t1 is recorded as accepted. This needs two timed swaps by someone with install write access. — confidence: low.
- LOW — `plugin/lib/fmdoctor.py:1297-1299` — Unbounded read. `read(mine, size)` loads an ignored checkout file of any size into memory before any comparison, and a large tracked blob in HEAD does the same. Fix: cap the size, and compare in chunks. — confidence: medium.

## lens: edge
- Held as intended: third-party ids (the content must equal HEAD), symlinked roots, files and folders (`O_NOFOLLOW` plus the `islink` checks), FIFOs, unreadable files, and more than 200 extras. Newline or quoted names fail closed because the check-ignore output set stops matching.
- Hard links to the checkout are accepted. This is harmless, because a later edit changes the hash and falls back to a HEAD comparison.
- Gap: the mode (exec bit) of install files is not compared with HEAD's 100644/100755. LOW.
- Untested: `*.pyc` or `local/` extras, a skipped folder with content, a hard link, more than 200 extras, and HEAD on a non-`main` branch.

## lens: intent
- Tracked files equal to HEAD blobs: met.
- Untracked file only if the checkout's same path is a gitignored, regular, byte-identical file: met literally. It is not met in spirit, because "gitignored" is far wider than the two generated paths the task cites, and the checkout's copy is not trusted.
- Everything else, and every third-party plugin, stays held: met. The `unread` hold still applies.
- "No human step" for a changed HEAD is by design, but it removes the review gate for an unmerged HEAD.

## Implicit decisions
- Trust is anchored to whatever branch HEAD is.
- `FOREMAN_HOME` comes from the environment.
- Ignore status comes from the live working tree's rules.
- Skipped folders count as matching.
- A 200-extras cap and a 10 s git timeout.

## Not checked
I did not run the tests. I did not check how Claude Code copies a directory marketplace, or whether hooks run with `plugin/lib` first on `sys.path`.

**Noticed:**
- `_tree_hash` stops hashing at 4000 files and 4 MB per file, so the plain supply check has a blind spot for large files. T-1434's `skipped` stand-in covers only their size and mtime.
- `plugin/tests/__pycache__` is copied into installs, and nothing prunes it.
