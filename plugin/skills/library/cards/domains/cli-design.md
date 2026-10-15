---
name: cli-design
title: CLI Design
area: domains
tags: [cli, flags, exit-codes, stdout, stderr, shell]
detect: [dep:commander, dep:yargs, dep:click, dep:typer, dep:clap, dep:cobra, dep:urfave/cli, dep:argparse, dep:oclif, dep:picocli]
related: [cron-jobs, legacy-code, unicode]
---
Command-line tools that compose: predictable flags, data on stdout, messages on stderr, meaningful exit codes.

## Verify
- `mytool --help; echo $?`: help prints and exits 0.
- `mytool --bogus; echo $?`: unknown flag prints usage to stderr and exits nonzero (2 by convention).
- `mytool list --json | jq .`: machine output is valid JSON with no decoration mixed in.
- `mytool list 2>/dev/null | head -1`: stdout carries data alone; the pipe closing does not crash it.

## Test first
Run the real entry point as a subprocess and check streams and code separately.
```python
import subprocess, json

def run(*args):
    return subprocess.run(["mytool", *args], capture_output=True, text=True)

def test_json_output_is_clean_and_errors_go_to_stderr():
    ok = run("list", "--json")
    assert ok.returncode == 0
    json.loads(ok.stdout)
    bad = run("show", "missing-id")
    assert bad.returncode == 1 and bad.stdout == "" and "not found" in bad.stderr
```

## Do
- Exit 0 on success, 1 for runtime failure, 2 for usage errors; document any further codes.
- Results to stdout, logs, progress and errors to stderr.
- Provide `--help` and `-h` with examples, `--version`, and subcommands as `noun verb` (`tool repo create`).
- Offer `--json` (or `--format`) for scripts; keep human tables for TTYs only.
- Detect a TTY: color and spinners only when `isatty`; honor `NO_COLOR` and a `--no-color` flag.
- Read from stdin when given `-` or when piped; accept `--yes` to skip prompts, and never prompt without a TTY.
- Order config precedence: flags, then environment variables, then config file, then defaults; show the source in a debug mode.
- Make destructive commands support `--dry-run` and confirmation.
- Handle SIGINT cleanly and `BrokenPipeError`/EPIPE silently when output is piped to `head`.
- Provide shell completions from the parser library.

## Avoid
- Printing status chatter on stdout: pollutes pipes. Send it to stderr.
- Always exiting 0 or 1: scripts cannot tell failures apart. Use distinct documented codes.
- Interactive prompts in CI: hang forever. Detect non-TTY and fail with a clear message or take flags.
- Secrets as command-line arguments: visible in `ps` and shell history. Read from env, file or stdin.
- Hand-parsing `sys.argv` or `process.argv`: fragile edge cases. Use the library.
- Stack traces for expected user errors: noisy. Print one actionable line; trace under `--debug`.
- Changing output format between versions without notice: breaks scripts. Version `--json` schemas.
- Unicode and colors assumed everywhere: garbled logs. Check TTY and encoding.

## Review
- [ ] Help text has examples; every flag is documented with its default.
- [ ] stdout is parseable data; diagnostics are on stderr.
- [ ] Exit codes are consistent and tested.
- [ ] Non-interactive and piped use work without prompts or color.
- [ ] Destructive actions need confirmation or `--yes`, and offer a dry run.
