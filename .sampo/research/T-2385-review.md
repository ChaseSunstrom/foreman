**Verdict: changes needed.** I found no network or live-account path in the validator table, but there are six real defects. I only read the code and ran nothing, so the severities below come from reading it.

## lens: adversary
- MEDIUM — `fminfra.py:35` — `docker compose -f f config -q` runs on an untrusted tree. Newer Compose versions resolve `include:` entries that are `oci://` or git refs by fetching them, so a repo-controlled compose file could reach the network. Nothing enforces "offline" except the choice of verbs. Fix: scan compose files for `include:` with a URL scheme and mark them unproven. Alternatively, run all validators under `unshare -n` when it is available. — medium (depends on the Compose version)
- LOW — `fminfra.py:172` — `{d}` is passed unprefixed, so a folder named `--something` that holds a `Chart.yaml` becomes a helm flag. `{f}` already gets the `./` guard. Fix: apply `safe` to `{d}` too. — high
- LOW — `fminfra.py:202,114` — `fm prove --infra` stdout and `--json` pass tool output through `c.plain` but not `c.redact`. A shellcheck snippet with a hard-coded token would be printed. The finish evidence path does redact, so only direct use is exposed. Fix: wrap `_first` in `c.redact`. — high

## lens: edge
- HIGH — `fminfra.py:183-184` — a validator that exits non-zero with no output is reported `pass`. Only the systemd benign filter justifies this. Triggering input: any tool that is killed, or that fails silently, with an empty `out` and `err` and `rc != 0`. A broken validator then counts as proof and the close is recorded as `[ran]` exit 0. Fix: pass on empty output only when `name == "systemd"`. For every other class, return `fail`, with `exit N` as the reason. Also catch `OSError` from `_run_tool`, because a bad shebang makes `Popen` raise and crashes `fm task finish`. — high
- MEDIUM — `fminfra.py:160-175` — `_copy` drops symlinks. Terraform with a plugin cache links `.terraform/providers` by symlink, so the copy has no providers. `validate` then says "Missing required provider" and the file is `fail`, which refuses the close on a valid config. Fix: map that message to `unproven`. — medium
- MEDIUM — `fminfra.py:25-26` — the refusal text comes from `run_result`, which keeps only the last two lines. With two or more failing files, the refusal shows the last failure and the summary line, so the first failure is hidden. Fix: `say()` every failing row, as is done for unproven ones. — high
- LOW — `fminfra.py:231` — `fmmap.changed` returns paths relative to the git root. If `p.root` is a subdirectory of the repo, `sel` never matches and touched infra files are silently skipped. Fix: use `--relative`, or prefix-strip against `p.root`. — low (unverified layout)

## lens: operator
- MEDIUM — `fminfra.py:130` — the copy is the whole tree, including untracked files, `.terraform` (a single provider binary can be 400 MB or more) and `.claude/worktrees/*` when finishing in the main checkout. It is made on every finish that touches infra and has a validator installed, into `/tmp`, which is often tmpfs. Fix: copy `fmlib._files` and the touched folders, with a byte cap (over the cap means unproven). — high
- MEDIUM — `fminfra.py:18` — the budget is checked only before each tool starts. Worst case is 300 s plus one 120 s tool, about 420 s per finish, and every retry after a refusal repeats it. The default Bash tool timeout is 120 s. Fix: use a smaller finish budget (about 60–90 s) and clamp each tool to the time remaining. — high
- LOW — `fminfra.py:84` — `classify` scans and fnmatches up to 20,000 files before applying `only`. Fix: filter to `only` and the helm ancestor `Chart.yaml` files first. — low (not measured)

## lens: intent
- MEDIUM — `fminfra.py:43` — `shellcheck {f}` runs at default severity. Any style or info finding exits 1, including SC1091 "not following" on `source`. SC2148, no shebang, is an error and is raised on sourced libraries. Foreman's own eight `.sh` files would be exposed wherever shellcheck is installed. `hadolint` has the same default threshold. Fix: `shellcheck -S warning`, and leave SC2148 to the repo's `.shellcheckrc`. For `hadolint`, use `--failure-threshold warning`. — high

## lens: maintainer
- LOW — `fminfra.py:169` — `__import__("shutil").Error` should be a normal import. The CHANGELOG has no entry for this task, although step 4 is ticked. MASTER.md and README are done. — high
- LOW — tests — all validators are stubs. There is no case for a silent non-zero exit, for terraform with missing providers, or for more than one failing file. — high

## Acceptance criteria
1. `fm prove --infra [PATH]` — **met**, with the HIGH silent-exit defect. Classification, per-class validators, the copy, the exit codes 0/1/2, the unproven label with the tool named, the terraform gates and the kubeconform gate are all present and tested with stubs. Nothing installs, downloads or runs against an account.
2. `fm task finish` — **partly met**. The proof runs on touched files, a failure refuses the close, and the capability-miss is filed once and nothing is installed. A pass is recorded as `[ran]` evidence. The silent-exit and shellcheck-threshold defects make that evidence unreliable.

**Implicit decisions:** `pass` means at least one file passed, even with others unproven. The terraform trust gate is the same `fm prove --yes-run` trust as migration. A capability-miss key is filed once ever, including after the task is archived. Compose `config` is treated as safe.

**Not checked:** real validators, because none ran. The measured copy and timing cost. The subdirectory-project path.

**Noticed:** none
