# Spec suite

A neutral toy repo of fully specified tasks with hidden tests, for `fm bench duel` (T-1232).

`make.py` builds `kit`, a small Python package (3.10+, standard library only), as a git repo: one base
commit (the package, a text-helper module and its unittest tests, a README with the conventions), then one
commit per task. Each task commit adds `kit/<name>.py` and `tests/test_<name>.py`, and its message is the
task's complete spec: the module path, the signatures, every rule and edge case the tests check, the error
types and the exact output formats.

## Why

The duel's first cases came from Foreman's own history, where a hidden test can check wording the request
never stated, and Foreman's guard protects that repo's core in both arms. Here every hidden test checks only
behaviour its commit message states, in a repo neither arm knows, so a duel measures diligence, cost and time
rather than luck at guessing wording.

## Tasks

| module | what |
|---|---|
| duration | `parse_duration("1h30m")` to seconds |
| lru | `LRUCache`: get, put, len, `in` |
| semver | `compare(a, b)` by SemVer 2.0.0 precedence |
| table | `render_table(rows, headers)` with an exact text layout |
| ranges | `merge_ranges` and `subtract` on half-open ranges |
| dotted | `get` and `set` in nested dicts and lists by a path such as `a.b.0.c` |
| tokenbucket | `TokenBucket(rate, capacity, clock).allow(n)` |
| csvlite | `parse_line(line, sep)`: one CSV line to fields |

## Run

    python3 bench/spec-suite/make.py --check   # build in a temp folder; prove each task fail-to-pass
    python3 bench/spec-suite/make.py /path/x   # build the repo in a new or empty folder
    cd /path/x
    fm bench build --commits "$(git rev-list --max-parents=0 HEAD)..HEAD" --verify 'python3 -m unittest {tests}'
    fm bench duel --vs none --runs 3 --jobs 4

`make.py DIR` prints the same commands with the base commit filled in. `--check` proves, for each task, that
its hidden tests fail at the parent commit and pass at the task's own, that the whole suite passes at HEAD,
and that a second build gives the same commits: the author and dates are fixed, so the case ids
(`C-<sha>`) stay the same from one build to the next.

## Adding a task

Add an entry to `TASKS` in `make.py`: its name, its message (the spec), its reference solution and its hidden
tests. A test may check only what the message states, in words a careful engineer could implement from the
message alone. Then run `--check`. Changing any task changes the commit ids from that task on.
