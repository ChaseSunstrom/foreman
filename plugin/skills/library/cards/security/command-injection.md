---
name: command-injection
title: Command injection
area: security
tags: [security, command-injection, shell, subprocess, rce, exec]
detect: []
related: [input-validation, path-traversal, unsafe-deserialization, semgrep]
---
Command injection: avoid the shell, pass arguments as an argv list, allowlist values, and use `--` to end options.

## Verify
- `semgrep scan --config p/command-injection --error`: no shell-string execution with user data.
- `grep -rnE "shell=True|os\.system|os\.popen|child_process\.exec\(|exec\.Command\(\"(sh|bash)\"|Runtime\.getRuntime\(\)\.exec\(" src/`: every hit is reviewed or removed.
- `bandit -r src -t B602,B605,B607`: subprocess shell and process-start findings clear.

## Test first
```python
import os, pytest
PAYLOADS = ["a; touch /tmp/pwned", "a && touch /tmp/pwned", "$(touch /tmp/pwned)",
            "`touch /tmp/pwned`", "a | tee /tmp/pwned", "--output=/tmp/pwned"]

@pytest.mark.parametrize("p", PAYLOADS)
def test_convert_does_not_execute_input(client, p):
    client.post("/convert", json={"filename": p})
    assert not os.path.exists("/tmp/pwned")
```
Clean up `/tmp/pwned` in a fixture so one failure does not mask the next.

## Do
- Prefer a library over spawning a process (an image library, zip module, DNS resolver, git library).
- When you must spawn: Python `subprocess.run([...], shell=False, check=True, timeout=10)`, Node `execFile` or `spawn` with an args array, Go `exec.Command(name, args...)`, Java `ProcessBuilder(list)`.
- Allowlist the command and its subcommand, and validate each argument by type or regex before use.
- Put `--` before user-supplied positional arguments so a leading `-` is not parsed as an option.
- Give the child a minimal explicit environment (`env=`) and a fixed working directory, and call executables by absolute path.
- Run with a low-privilege user and, where possible, in a sandbox or container with no network.
- Capture output and cap its size, and set timeouts.

## Avoid
- `subprocess.run(f"convert {name} out.png", shell=True)`: any `;` or `$()` in `name` runs. Use a list and `shell=False`.
- Node `exec(\`cmd ${x}\`)`: the string goes to a shell. Use `execFile("cmd", [x])`.
- Quoting by hand with `replace('"', '\\"')`: shells have many metacharacters. Use argv lists, or `shlex.quote` only when a shell is unavoidable.
- Ignoring option injection: a filename like `-rf` or `--config=evil` is parsed as a flag with no shell involved. Use `--` and validate.
- Passing user data to `git`, `tar`, `curl` or `ssh` without checking: they have flags that execute code or write files. Allowlist options.
- Templates that evaluate code (`eval`, server-side template injection) described as "just formatting": treat them as shells.

## Review
- [ ] No shell is invoked with user data, or each case is allowlisted.
- [ ] Arguments are lists with `--` before untrusted positionals.
- [ ] Commands, environment and working directory are fixed.
- [ ] Timeouts, output caps and a low-privilege user apply.
- [ ] A metacharacter and option-injection test covers each spawn.
