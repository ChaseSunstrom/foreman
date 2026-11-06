# Brainstorm — lens: security and safety

- **Log what default mode would have asked, so bypass can be earned** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: newcomers get `bypassPermissions` plus 20 deny rules with no evidence for the trust ask (A2), and earned-bypass ideas exist but need data. Assumption: each guard verdict can also be classified as "default mode would have prompted".
  Done when: after a session, `fm status` prints "N actions bypass skipped prompts for (top 3 classes)", and a unit test feeds a recorded hook trace and gets the expected count.

- **Interlock edits to files that run code on the next test or build** — SECURITY — value 5 — effort M — risk med — category: guard
  Why: Foreman's gates (1,586 test-runner calls) execute `conftest.py`, `sitecustomize.py`, `.pth` files, `setup.py`, Makefile targets, `package.json` lifecycle scripts, `.envrc`, `.git/hooks` and devcontainer commands. An edit to one of these becomes code execution at the next gate, outside what the guard judged. Existing ideas cover persistence at done, not this pre-gate path.
  Done when: a task whose diff adds a line to `conftest.py` makes `fm check` refuse to run until one yes is recorded, and a replay case proves it.

- **Lint allow rules that equal arbitrary code execution** — SECURITY — value 4 — effort S — risk low — category: config
  Why: rival ECC ships AgentShield, a config scanner (B). Rules such as `Bash(python:*)`, `Bash(bash -c:*)`, `Bash(npx:*)` or `Bash(git:*)` give arbitrary execution and make the deny rules decorative. Assumption: the user's accumulated "always allow" clicks already contain some.
  Done when: `fm doctor` flags each such rule with a narrower suggestion, and a fixture settings file with `Bash(python:*)` fails the check.

- **Stop the installer's Python shadowing the system `python3`** — SECURITY — value 4 — effort M — risk med — category: install
  Why: when Python is old or missing, the installer fetches one via `uv` and puts `python3` in `~/.local/bin` (A3 and README). A user-writable directory that shadows `python3` is a PATH-hijack surface, and the downloaded interpreter's checksum is not mentioned.
  Done when: the installer uses a private `~/.claude/foreman/py/bin/python` verified against a pinned hash, `command -v python3` is unchanged after install, and `fm doctor` reports that path.

- **Write a session blast-radius receipt** — FEATURE — value 4 — effort M — risk low — category: transparency
  Why: bypass users have no after-the-fact view of what the agent did to the machine. Assumption: hooks already record paths and commands, so the receipt is an aggregation.
  Done when: at session end or `fm receipt`, it lists writes outside the project root, hosts contacted by spawned commands, secret-pattern paths read, and files deleted, and a golden test covers a recorded session.

- **Protect the user's own uncommitted work from the agent** — SECURITY — value 4 — effort M — risk med — category: undo
  Why: `git checkout .`, `reset --hard`, `clean` and whole-tree formatters destroy changes Foreman never made. Existing snapshot ideas trigger on risky commands; this keys on who owns the dirty files. Assumption: the task-start file set separates agent-owned from user-owned changes.
  Done when: with a user-modified untracked file present, a blocked-class command first writes a recoverable ref and the guard message names the restore command.

- **Run a no-model hostile-repo drill at first install (wild)** — FEATURE — value 5 — effort L — risk med — category: trust
  Why: a clean install fails its own `fm doctor` and there is no published safety evidence (A8, C). Idea: build a throwaway repo with hostile `CLAUDE.md`, `.envrc`, `conftest.py`, symlinks and git config, replay the hook payloads, and print "N of N attacks stopped".
  Done when: `fm doctor --drill` ends with a pass/fail count, and removing a deny rule makes the count drop.

- **Demote the session after a dangerous-command strike (wild)** — SECURITY — value 4 — effort M — risk high — category: guard
  Why: a blocked `rm -rf ~` or exfiltration attempt in bypass mode suggests injection or drift, yet the next call runs with full power. Assumption: a PreToolUse `ask` decision still prompts under bypass; if it doesn't, fall back to blocking outward and destructive classes.
  Done when: after one critical block, the next destructive-class call prompts the user, and the greeting says why.

- **Publish what the guard cannot stop, generated from xfail tests (wild)** — FEATURE — value 4 — effort S — risk low — category: honesty
  Why: the README asks for a large trust leap, and "known gaps" is prose that drifts from the code. Idea: every known bypass in the guard corpus becomes an `xfail` case, and a generated "Limits" section lists them.
  Done when: adding an xfail corpus case changes the generated Limits text, and a test fails if the doc is stale.

- **Seed the guard corpus from public agent-incident postmortems** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the guard corpus is built from the user's own commands, so it misses what has hurt strangers (wiped home directories, force-pushes, dropped databases, leaked `.env` files). Assumption: about 40 incidents can be written as commands and expected verdicts with no network use.
  Done when: a corpus file of at least 40 sourced cases runs in the suite, and each case names its incident.

- **Probe whether a rival plugin's hook can override Foreman's deny** — SECURITY — value 4 — effort M — risk med — category: interoperability
  Why: the rivals are popular (B), and ECC ships hook profiles after hook-conflict complaints. Foreman's guard is only as strong as the verdict precedence it sits under. Assumption: Claude Code resolves conflicting hook decisions in a way testable offline with recorded payloads.
  Done when: `fm doctor` reports "deny holds with <plugin> enabled" per installed plugin, using a synthetic dangerous payload.

- **Make the installer's trust grants individually declinable and auto-expiring (wild)** — SECURITY — value 3 — effort M — risk med — category: install
  Why: the installer sets bypass, the output style, autocompact and 20 deny rules behind a single "confirm once" (A2). Idea: bypass is granted for 14 days and then silently re-asks with the counterfactual log from the first idea.
  Done when: the install receipt lists the bypass lease expiry, and a fake clock test shows the mode returning to default after expiry unless renewed.
