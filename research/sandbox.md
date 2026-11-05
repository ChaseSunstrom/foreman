# Sampo's sandbox: layers, proof and cost (T-3222)

The user asked on 2026-11-05 for network and filesystem sandboxing, then for container isolation too. Sampo
already confined some work: Landlock limited fm code workers' writes, calling cards ran in a Landlock and seccomp
jail, and a few checks ran under `unshare -n`. A command run in your own session, a test run and most of Sampo's jobs
had nothing below Ward, which reads command text. This note records what now confines them and what it costs.

## Layers

| Layer | What confines it | Turned on by | Covers |
|---|---|---|---|
| job | bubblewrap: own user, mount, pid, ipc and uts namespaces | `sampo sandbox run`, `run.py --sandbox` | any command Sampo or you run through it |
| image | docker: no capabilities, read-only filesystem, this uid | `sampo sandbox run --image IMAGE` | a job that needs its own userland |
| session | Claude Code's own sandbox (bwrap and a proxy) | `sampo sandbox on --session` | your sessions' Bash commands |
| landlock | Landlock ABI 10 | always, for fm code workers | their writes |

`sampo sandbox status` and `sampo doctor` name each layer and whether it is live here.

## What a job can and can't do

Each row is a test in `plugin/tests/test_sandbox.py` that runs the escape and checks it failed.

| Attempt | Result |
|---|---|
| write outside the project and `--write` folders | refused: the system is read-only |
| read ~/.ssh, ~/.config/sampo/secrets.env, ~/.git-credentials | empty folder, or /dev/null for a file |
| the same with `$HOME` pointed elsewhere | still masked: the account's real home is masked too |
| plant a git hook, rewrite `.git/config` (core.fsmonitor), write `.claude/settings.json` | refused: read-only inside the project |
| create a `.git/hooks`, `.vscode`, `.envrc` or `.mcp.json` the project lacks | refused: an empty read-only stand-in, gone after |
| rename `.git` away and `git init` a new one with hooks | refused: each git dir is a mount point |
| plant hooks or config in a submodule's git dir or a nested repo's `.git` (three folders down) | refused: the same guard on each |
| a root of `/`, the home folder or `~/.claude` | refused before anything runs |
| see or signal a process outside | not visible: its own pid namespace |
| keep `LLM_API_KEY`, `GITHUB_TOKEN`, `PGPASSWORD`, `MYSQL_PWD`, `NGROK_AUTHTOKEN` | dropped from its environment |
| reach the docker socket or the session bus | gone: /run is fresh |
| connect anywhere with `--net off` | no route: its own network namespace |
| with `--net allow`, a host not on the list | 403 from the proxy, named on stderr |
| with `--net allow`, 169.254.169.254 even when listed | 403: link-local never passes |
| with `--net allow`, a loopback, private or CGNAT address | 403 unless an entry names it with its port |
| with `--net allow`, a direct connection around the proxy | no route |
| a malformed proxy request | 400, no crash |

Ordinary work runs unchanged inside: git init and commit, Python, its own /tmp, and HTTPS to an allowed host
(`https://pypi.org/simple/pip/` returned 200 through `--net allow --allow pypi.org`).

## What it costs

Startup per job, the mean of 20 runs of `python3 -c pass` at load 25 on 16 CPUs (2026-11-05):

| How it ran | ms per job |
|---|---|
| plain | 24 |
| bare bwrap (namespaces, read-only root) | 39 |
| `sampo sandbox run` (the CLI, then bwrap) | 186 |

bwrap itself adds about 15 ms; the rest of `sampo sandbox run`'s time is the sampo CLI starting. `run.py --sandbox`
calls bwrap directly, so a test class pays the 15 ms once.

The first two sandboxed full runs died at 12 to 14 minutes: /tmp ran out of inodes. A test class that runs Sampo
against the real home found its state read-only inside the sandbox, and `core.state_dir()` then copied all of it
(361,211 files) into the class's /tmp as a fallback. Inside a job, `FOREMAN_STATE_FALLBACK=0` now keeps the state
read-only in place. An overlay that discards the job's writes would be cleaner, but this kernel refuses overlayfs to
unprivileged users. run.py also fails a class whose temp folder can't be made by name, instead of crashing the run
(T-3236).

### Test suite under the job tier

`run.py --sandbox -j 12` on 2026-11-05, every class with the repo read-only, only its own temp folder writable and no
network: **all green**, 6,863 tests in 3,319 jobs, 758 s at load about 30 on 16 CPUs, /tmp at most 19% full and 51% of its inodes. Getting
there took five runs, and each fix was a real one:

| Run | Result | What it found |
|---|---|---|
| 1, 2 | died at 12 to 14 min | run.py crashed when /tmp ran out of inodes (now fails that class: T-3236) |
| 3 | 3,024 classes red | Sampo copied all of its state (361,211 files) into a class's /tmp when the real one was read-only |
| 4 | 120 red | no /run/user/UID in the fresh /run (XDG_RUNTIME_DIR) |
| 5 | 6 red | a missing `fmsandbox` shim (red without the sandbox too), the state-fallback and fsck tests needing their own environment, two Landlock tests writing temp folders in the real home, and one settings test locking the real state's settings |
| 6 | green | |

At about 15 ms a job (3,319 jobs) the sandbox's own cost is under a minute of CPU, a few seconds of wall time on
12 workers.

## Limits

- The credential list is fixed (`CREDENTIALS`): a project's own `.env` stays readable.
- An allowlisted name on a shared CDN can carry another tenant's traffic: the proxy checks the CONNECT name, not TLS SNI.
- A protected path the project lacks (`.git/hooks`, `.claude`, `.vscode`, `.mcp.json`, `.envrc`) gets an empty read-only
  stand-in for the job's run, so the job can't create it. Its mount point is an empty file or folder in the project
  while the job runs, removed after; a Claude Code session opened in that project meanwhile sees an empty `.mcp.json`.
- A job can create `.git` where the project has none (git init must work); a project inside a parent repo then has a
  repo of its own, whose hooks run if you use git in that folder.
- Claude Code's sandbox never covers hooks; in bypass-permissions mode an unlisted host is allowed unless strict.
- Without bubblewrap or unprivileged user namespaces, `sampo sandbox run` exits 3 and says why, and `run.py --sandbox`
  runs plain with a note.

Follow-ups: fm code's tool commands in the job tier (T-3231), ship's scratch tests (T-3232), local-model tool runs
(T-3233), host and denial logging with `sampo sandbox learn` (T-3234), Ward trusting a proven sandbox (T-3235).
