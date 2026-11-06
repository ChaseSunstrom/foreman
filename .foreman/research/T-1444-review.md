**Verdict:** changes needed. Both acceptance tests target the stated cases, but the "unreadable thing can't hide a change" goal still leaks through directories and exec-only files. I could not run code, so these come from reading the code and Python's `os.walk` semantics.

## lens: adversary
- HIGH — `plugin/lib/fmdoctor.py:1162` — `os.walk` is called without `onerror`, so a subdirectory it can't list is skipped without being named in the hash. A directory isn't named unless it is a symlink (lines 1163-1166), so its contents are never hashed. Failing input: `hooks/bin/` at mode 0111 holding an executable `run` that hooks.json references. Baseline it, then overwrite `run` (mode 0111 still allows writing an existing file). `sha` and `caps` are unchanged, so the check reports PASS "unchanged". The same input before this change also gave PASS, so the hole is not new, but it is the "one unreadable thing hides all later changes" class this task targets. Fix: `os.walk(root, onerror=lambda e: (h.update(os.path.relpath(e.filename, root).encode() + b"\0unlisted\0"), stand(...)))`. Add the directory's `st_mode`, `st_ctime_ns` and `st_mtime_ns` to `stand`. — confidence: high on the walk behaviour (not run)
- MEDIUM — `plugin/lib/fmdoctor.py:1186-1187` — the marker `rel\0unreadable\0` is the same on every run, so a file that is still unreadable can change content without changing the hash. Failing input: an ELF at `bin/tool`, mode 0111 (exec-only, which the kernel runs without read access), hooked from hooks.json. Baseline it, then replace it with a different ELF at mode 0111. The hash is identical and the result is PASS. The docstring says what `h` only names goes into `skipped`, but this branch never calls `stand`. Fix: in the except branch call `st = os.stat(full)` (guarded) and `stand(rel + f"\0{st.st_size} {st.st_mtime_ns} {st.st_ctime_ns}\0".encode())`. ctime is harder to forge than mtime. — confidence: high
- LOW — `plugin/lib/fmdoctor.py:1166,1175,1178,1180` — `islink`, `getsize`, `stat` and `readlink` sit outside the `try`. A file or symlink that vanishes mid-walk raises `FileNotFoundError`, and `_supply` puts the plugin in `errors`. That is the original bug (old baseline kept, WARN only). The window is a race and can't be timed reliably, but the fix is cheap. Fix: wrap the whole per-file body in `except OSError` and name the file, as the new branch does. — confidence: medium
- LOW — `plugin/lib/fmdoctor.py:1187` — there is no length framing. A readable file `a` whose content is exactly `unreadable\0` hashes the same as an unreadable `a`, and likewise for `skipped\0`. This can't carry a useful payload, but the markers should not be forgeable. Fix: use a prefix that can't be file content, for example `rel + b"\0!unreadable"`, or length-prefix every file's content. — confidence: high

## lens: edge
- LOW — `plugin/tests/test_supply_delta.py:406-411` — the `chmod(skill, 0)` assertion fails when the suite runs as root, because root can still read the file. Nothing in the file skips for root (no `geteuid` check). Fix: `skipIf(os.geteuid() == 0)`. — confidence: high
- LOW — `plugin/tests/test_supply_delta.py:436` — the comment "check_supply stops earlier (the tree hash can't read it: 'not checked')" is now false for files, and for directories it was never true. Fix: delete or reword it. — confidence: high

## lens: maintainer
- LOW — `plugin/lib/fmplugins.py:241,248` — `profile()` now reaches `_component_files`, which walks with `followlinks=True`. A symlinked directory inside a component folder (for example `commands/x -> ~/notes`) therefore puts the name and description of foreign `.md` files into profile output and the token estimate. This is up to 2000 files or 5000 directories, and each file read is capped at 4000 bytes. The old `glob` did not recurse. Fix: have `profile()` drop entries whose `realpath` is outside the plugin root, except the default-folder link case. — confidence: medium
- LOW — `plugin/lib/fmplugins.py:131-134` — `seen` dedupes on raw `os.path.join(d, f)` for walked files but on `realpath` for named files, so a file named both ways is counted twice in the token estimate. Fix: dedupe on `realpath`. — confidence: low

## Acceptance criteria
- Unreadable file still compared, and an unreadable SKILL.md holds the plugin: met. `test_an_unreadable_file_is_held_not_skipped` covers it. The hold is a delta against the baseline: a persistent unreadable file is not re-held after accept.
- `profile()` lists custom `plugin.json` paths and nested commands, confined to the root: met. `test_profile_reads_custom_component_paths` covers it, and an outside path such as `../../` is rejected.
- Inferred goal (an unreadable item can't hide later changes): not met for unreadable directories or for content changes on exec-only files (see the first two findings).

## Implicit decisions
- The "unreadable" marker is a fixed string, not a stat stand-in.
- Any `OSError` on open counts as unreadable.
- A component file that can't be read becomes the "?" event, not `caps['unread']` as the brief's approach said.
- `profile()` follows the default component folder wherever it links.

## Not checked
I could not run the tests or `git diff`. I did not check CHANGELOG, `capabilities()` internals beyond `_component_files`, or the other callers of `profile`.

**Noticed:** `_SUPPLY_SKIP` (`.git`, `node_modules`, `__pycache__`, `.venv`) at `plugin/lib/fmdoctor.py:1135` is neither hashed nor named, so a hook script under `hooks/node_modules/` is invisible to the supply check. It deserves its own task.
