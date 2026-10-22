<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Python: the standard library first

Use when you are about to add a Python dependency, write a helper, or review code that rebuilds something the
standard library already has. Every dependency is code you didn't read, a version to keep current and a supply-chain
risk; the standard library ships with the interpreter and is already reviewed.

## The procedure

1. **Name the job before the package.** "Parse TOML", not "add tomli". Look it up in the table below and check
   what the project already depends on (`pyproject.toml`, the lock file). Pass: a new dependency's commit or brief
   says which job it does and why the standard-library row doesn't cover it.
2. **Check the version floor.** The module must exist in the oldest Python the project supports (`requires-python`).
   `sys.stdlib_module_names` (3.10+) answers it on the floor interpreter:
   `python3 -c "import sys; print([m for m in ('tomllib', 'zoneinfo', 'requests') if m not in sys.stdlib_module_names])"`
   prints the ones you would have to install (`['requests']` on 3.11+).
3. **Use the safe form** of each module (the last section). Pass: none of the unsafe forms appears in the diff.
4. **When a dependency wins,** add one per task, pin it in the lock file, and record why
   (`../release/dependency-upgrade.md` covers bumping it later).

## Job → module

| Job | Standard library | A dependency earns its place when |
|---|---|---|
| command-line arguments | `argparse` | many subcommands share options and help → `click` or `typer` |
| paths, files, temp files | `pathlib`, `shutil`, `tempfile` | — |
| JSON, CSV, reading TOML | `json`, `csv`, `tomllib` (3.11+) | writing TOML, or YAML at all |
| HTTP calls | `urllib.request` | retries, pooling, HTTP/2 or async → `httpx` |
| dates and time zones | `datetime`, `zoneinfo` (3.9+) | — |
| records and enums | `dataclasses`, `typing.NamedTuple`, `enum` | validating outside input → `pydantic` |
| running programs | `subprocess.run([...], check=True)` | — |
| concurrency | `concurrent.futures`, `asyncio` | — |
| memoising | `functools.cache`, `functools.lru_cache` | sharing across processes |
| counting and grouping | `collections.Counter`, `defaultdict`, `itertools` | — |
| logging | `logging` (JSON lines: `../ops/observability.md`) | — |
| tests | `unittest`, `unittest.mock`, `doctest` | fixtures and parametrising at scale → `pytest` |
| a local database | `sqlite3` | migrations or an ORM |
| tokens, hashes, signatures | `secrets`, `hashlib`, `hmac` | password storage beyond `hashlib.scrypt` → `argon2-cffi` |
| text diffs, simple templates | `difflib`, `string.Template` | HTML templates → `jinja2` |
| archives and compression | `zipfile`, `tarfile`, `gzip` | — |

## Safe forms

- `subprocess` with a list of arguments; never `shell=True` with any outside text in the command.
- `secrets.token_urlsafe()` for tokens and ids people can't guess; never `random`.
- `json.loads` for outside data; never `eval`, `pickle` or `marshal` on it.
- `tempfile.mkstemp` or `TemporaryDirectory`; never a hand-built `/tmp/name`.
- `tarfile.extractall(path, filter="data")`, so an archive can't write outside `path`; check the archive's names
  before extracting from a `zipfile`.
- `urllib.request.urlopen(url, timeout=...)` always with a timeout, and only `https://` URLs you chose.

## Checks

- [ ] Each new dependency names its job and why the standard library doesn't do it.
- [ ] Every module used exists at the project's `requires-python` floor.
- [ ] `grep -rnE "shell=True|pickle\.loads|eval\(|extractall\(" --include=*.py .` hits only reviewed, commented lines.
- [ ] No helper reimplements a table row (a hand-rolled argument parser, a home-made temp path).

## Library cards

`fm lib show python` (the baseline toolchain), `fm lib show python-typing`, `fm lib show python-performance`,
`fm lib show python-packaging`, `fm lib show click-typer`, `fm lib show httpx`, `fm lib show pydantic`. See also
`python-patterns.md` and `python-testing.md` in this folder.
