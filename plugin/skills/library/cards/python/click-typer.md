---
name: click-typer
title: Click and Typer
area: python
tags: [python, cli, click, typer, commands, arguments]
detect: [dep:click, dep:typer]
related: [pytest, python-packaging, pydantic, uv]
---
Python command-line apps with Click (decorators) or Typer (type hints on top of Click): groups, options, prompts, exit codes.

## Verify
- `python -m app --help`: the CLI imports and every command shows usage.
- `app COMMAND --help` for each command: options and help text render.
- `pytest -q`: CLI tests through the runner (`CliRunner`).
- `python -m app BAD_ARG; echo $?`: a usage error exits 2.

## Test first
Invoke the command in process with `CliRunner`; assert output and exit code.
```python
from typer.testing import CliRunner   # click.testing.CliRunner for Click
from app.cli import app

def test_add_rejects_negative():
    r = CliRunner().invoke(app, ["add", "--qty", "-1"])
    assert r.exit_code != 0
    assert "qty" in r.output
```
For Click use `from click.testing import CliRunner` and `invoke(cli, [...])`.

## Do
- Click: `@click.group()`, `@click.command()`, `@click.option("--n", type=int, default=1, show_default=True)`, `@click.argument("path", type=click.Path(exists=True))`.
- Typer: `app = typer.Typer()`, `@app.command()`, and typed parameters with `typer.Option(...)`/`typer.Argument(...)`; use `Annotated[...]` form.
- Return results by printing to stdout; send diagnostics to stderr (`click.echo(..., err=True)` or `typer.echo(..., err=True)`).
- Signal failure with `raise click.ClickException("msg")`, `typer.Exit(code=1)` or `ctx.exit`, not `sys.exit` scattered through code.
- Read secrets from `envvar=` or prompts with `hide_input=True`, not from flags that land in shell history.
- Keep commands thin: parse, call a plain function, print. Test the function directly.
- Expose the entry point as `[project.scripts] app = "app.cli:app"` in `pyproject.toml`.
- Use `--json` output for scriptable commands.

## Avoid
- Business logic inside the command body: only testable through the runner. Extract functions.
- `input()` and `print()` for prompts and output: skip Click's testing and stream handling. Use `click.prompt` and `echo`.
- `sys.exit(0)` inside commands: breaks `CliRunner` flows and callers. Return normally or raise `Exit`.
- Mutable defaults and `default=[]` on options: use `multiple=True` (Click) or `list[str] | None` (Typer).
- `type=str` for paths: loses existence and permission checks. Use `click.Path` or `pathlib.Path` in Typer.
- Importing heavy modules at CLI import time: slow `--help`. Import inside the command.
- Assuming Typer's `typer[all]` extra exists: newer releases bundle Rich; install `typer` alone and check the docs for the pinned version.

## Review
- [ ] Every command has help text and tests for success, bad input and exit code.
- [ ] Errors go to stderr with a nonzero exit; results go to stdout.
- [ ] Secrets are not accepted as plain flags.
- [ ] The console script entry point is declared and installable.
- [ ] `--help` is fast (lazy imports).
