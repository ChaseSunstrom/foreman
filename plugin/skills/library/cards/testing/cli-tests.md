---
name: cli-tests
title: CLI tests
area: testing
tags: [testing, cli, subprocess, exit-code, stdout, stderr, integration]
detect: []
related: [integration-testing, golden-files, test-isolation, approval-tests]
---
Test a command-line tool through its real entrypoint: exit code, stdout, stderr, files written, in an isolated temp directory and environment.

## Verify
- `./tool --help; echo $?`: help prints and exits 0.
- `./tool --bogus; echo $?`: an unknown flag exits non-zero (usually 2) and says why on stderr.
- `./tool input.txt 2>err.txt >out.txt; echo $?`: stdout, stderr and exit code are separable.
- `pytest -q tests/cli` (or `go test ./cmd/...`, `npx jest tests/cli`): the CLI suite passes.

## Test first
Run the real binary or command function, assert the exit code and the split streams.
```python
import subprocess, sys

def test_missing_file_exits_2_with_message(tmp_path):
    r = subprocess.run([sys.executable, "-m", "mytool", str(tmp_path / "nope.txt")],
                       capture_output=True, text=True, cwd=tmp_path)
    assert r.returncode == 2
    assert "nope.txt" in r.stderr
    assert r.stdout == ""
```
In-process alternatives: Click `CliRunner`, Typer `CliRunner`, Go `cmd.SetOut` with `Execute`, Node `execa`.

## Do
- Assert exit code, stdout and stderr separately; errors belong on stderr, results on stdout.
- Run in a fresh temp directory with explicit `cwd` and a minimal `env` (set `HOME`, `NO_COLOR=1`, `TZ`, `LANG`) so the developer's machine does not leak in.
- Test the argument surface: no args, `--help`, `--version`, bad flag, missing value, conflicting flags, `--` handling.
- Test stdin input and piping (`input=` in subprocess), and output when stdout is not a TTY.
- Check files the command creates or modifies, and that failure leaves no partial output.
- Cover exit codes as a contract: 0 success, 1 failure, 2 usage error, and the distinct codes you document.
- Use golden files for large outputs and scrub paths, timestamps and versions.
- Run with a timeout so a hang fails the test.

## Avoid
- Calling internal functions only: argument parsing and exit paths ship untested. Invoke the entrypoint.
- Asserting on combined stdout and stderr (`2>&1`): hides which stream carried what. Capture separately.
- Using the real home directory, config or network: nondeterministic and destructive. Redirect `HOME` and stub the network.
- Asserting colorized or wrapped output: breaks across terminals. Set `NO_COLOR` and a fixed width.
- Matching the whole help text: brittle churn. Assert key flags exist, or use an approved file.
- `sleep` waiting on a subprocess: use `communicate(timeout=...)` or `wait`.

## Review
- [ ] Entrypoint is run, with exit code and streams asserted separately.
- [ ] Temp directory and a controlled environment are used.
- [ ] Bad input, missing files and pipe cases are covered.
- [ ] Failure leaves no partial files.
- [ ] A timeout guards against hangs.
