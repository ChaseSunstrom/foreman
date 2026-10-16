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

## Round 2: `--suite hard`

Round 1 was too easy to tell the arms apart (both 24 of 24), so round 2 (T-1237, `hard.py`) adds tasks where
checking your work pays. It builds `ledger`, a small invoicing package whose modules share helpers (`money`,
`text`), and is graded by the whole test suite, so a change that breaks another module fails its case.

| task | kind | what | its naive variant fails |
|---|---|---|---|
| grouping | keep rule | thousands separators in `invoice.render` only | `test_export` (existing) |
| wrap | edge cases | `text.wrap` with indents, paragraphs and long words cut; invoice notes indented | `test_text` (hidden) |
| filenames | keep rule | export file names spell out `&` `+` `@`, capped, never empty | `test_customers` (existing) |
| ini | edge cases | `ini.parse`: sections, comments, continued values | `test_ini` (hidden) |
| prices | keep rule | typed invoice lines take `1,234.50`, `12.5`, `€12` | `test_importer` (existing) |
| interval | edge cases | exact interval arithmetic | `test_interval` (hidden) |
| taxround | keep rule | tax rounds half to even, discounts don't | `test_money` (existing) |
| lexer | edge cases | `lexer.tokenize`: numbers, names, strings, operators | `test_lexer` (hidden) |

A keep-rule task asks for behaviour one caller of a shared helper gets, and its spec's "Keep:" lines say what
the other callers keep: the obvious edit to the helper breaks their existing tests. An edge-case task has a
dense spec whose rules the quick shortcut (`textwrap`, `configparser`, one regex) gets wrong.

    python3 bench/spec-suite/make.py --suite hard --check
    python3 bench/spec-suite/make.py --suite hard /path/y
    cd /path/y
    fm bench build --commits "$(git rev-list --max-parents=0 HEAD)..HEAD" --verify 'python3 -m unittest discover -s tests'

`--check` runs the whole suite each time, as that `--verify` does: each task fails at its parent (its tests
restored) and passes at its commit, and its recorded naive variant (the plausible shortcut, applied to the
parent) fails the test module it names. The output lists every module the naive variant fails, hidden (the
task's own tests) or existing.

## Adding a task

Add an entry to `TASKS` in `make.py`: its name, its message (the spec), its reference solution and its hidden
tests. A test may check only what the message states, in words a careful engineer could implement from the
message alone. Then run `--check`. Changing any task changes the commit ids from that task on.

In `hard.py` a task's `files` map each path to its new text or to `(old, new)` edits of the parent's, and its
`naive` entry gives the shortcut (`what`, `files`) and the test module it must fail (`fails`).
