**Verdict: approve with nits.** Nothing here blocks. The face winding and `--days` bounds hold. I found one name-collision bug, one git-parsing bug, and a few doc and test gaps. I could only read files, so I traced the code by hand and ran nothing.

## lens: intent
- LOW — `CHANGELOG.md:9`, `plugin/lib/fmscene.py:1290` — The changelog says each ridge rises with "the lines changed there each day". The docstring says "a column per day". The default 90 days is capped at 40 columns, so each column sums about 2.25 days. At `--days 3650` a column covers roughly 90 days. — Reword to "per column, one day each up to 40 columns, then buckets of the whole span". — high

## lens: adversary
- No findings. Mesh names are reduced to `[A-Za-z0-9_-]` before they reach JSON or the terminal. The only unfiltered text printed is git's own stderr, which can't carry attacker-chosen paths. `git` is called with a list argv and `days` is an int.

## lens: edge
- LOW — `plugin/lib/fmscene.py:1267` — The collision fallback `f"{n[:56]}-{i + 1}"` can itself collide, and `validate` then refuses the whole scene with "names an earlier mesh too". Trigger: top-level paths `a-b` (rank 1), `a-b-3` (rank 2) and `a.b` (rank 3). `a.b` becomes `a-b`, which is taken, so it falls back to `a-b-3`, which is also taken. The command exits 2 with a confusing error. — Replace the single `if` with `while n in taken: n = f"{n[:56]}-{k}"; k += 1`. — high
- LOW — `plugin/lib/fmscene.py:1295` — Without `-c core.quotepath=false` (or `-z`), git quotes non-ASCII paths in numstat, so `café/x.py` arrives as `"caf\303\251/x.py"`. The top-level key becomes `"caf\303\251` and the mesh is named `p--caf-303-251`. Files in a non-ASCII directory and a root file with the same name end up as separate keys. — Add `-c core.quotepath=false` before `log`. Tabs, quotes and backslashes stay quoted, which only gives an ugly name. — high
- LOW — `plugin/lib/fmscene.py:1295`, `plugin/lib/fmscene.py:1332-1345` — `subprocess.run` has no timeout and its output is fully buffered. `--days 3650` on a large repo can take minutes and use hundreds of MB. A `TimeoutExpired` added later would not be caught, because `cmd_scene` catches only `OSError` and `ValueError`. — Add `timeout=60` and convert `subprocess.TimeoutExpired` to `ValueError`. — medium
- LOW — `plugin/lib/fmcli.py:6727`, `plugin/lib/fmscene.py:1345` — `--days 1` is refused ("2 to 3650") although `churn` copes with it, because the column count is already clamped to at least 2. — Allow 1 and relax the bound. — high

Cases that hold up:
- **Binary lines:** `-\t-` lines are skipped, and a repo of only binaries gives a clear error.
- **Spaces and tabs in paths:** spaces are fine. A path containing a tab arrives quoted, so it still splits into 3 parts.
- **Outside git:** a non-repo raises `ValueError`. `git` missing raises `OSError`, which `cmd_scene` catches.
- **Reserved names:** `camera` and `floor` are in `taken`, so those paths get a `-N` suffix.
- **Length:** the longest name is 62 characters, within the 63 limit.

## lens: operator
- No findings. `fm scene terrain` is a one-shot command with no hook, loop or schedule. The timeout point above is its only cost issue. The `MASTER.md`, `CHANGELOG.md` and playbook lines match the code.

## lens: maintainer
- LOW — `plugin/tests/test_scene.py:198-211` — The acceptance criteria and the review brief both turn on the winding, but no test checks it. Flipping a face index passes the suite. — Assert that the cross product of each face has a positive y for the top faces and a positive z for the front faces. — high
- LOW — `plugin/tests/test_scene.py:213-225` — Three behaviours the code handles have no test: a name collision, the reserved names `camera` and `floor`, and a binary `-` numstat line. — Add `terrain(rows, ["floor", "camera", "a.b", "a-b"])` and check the resulting names are unique and valid. — high

## Acceptance criteria
- **Criterion:** `fm scene terrain` prints a scene.json that `fm scene check` accepts, with one ribbon per busiest path, heights by churn, and an error outside git.
- **Status:** Met. `terrain()` returns `validate(...)` output, and the test at `plugin/tests/test_scene.py:227-233` covers print, `--out`, `check` and the non-git error. Heights are log-scaled, so they track churn in order but not proportionally. I did not run `python3 plugin/tests/run.py Terrain`.

## Implicit decisions
- Heights use `log1p` against the global maximum.
- Columns run from the oldest commit in range to now, up to 40, summed into buckets.
- Churn counts added plus deleted lines, with merges and renames excluded.
- Mesh names are the path with illegal characters turned into `-`.
- A leading `p-` is added when the name doesn't start with a letter.
- Ridges have no back or end caps, so they show only from the front and above.

## Not checked
I did not run the tests, render the scene, or check `_write_out` (unchanged code).

Noticed: none
