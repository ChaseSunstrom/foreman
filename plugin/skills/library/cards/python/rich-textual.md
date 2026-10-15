---
name: rich-textual
title: Rich and Textual
area: python
tags: [python, terminal, tui, rich, textual, cli]
detect: [dep:rich, dep:textual, dep:textual-dev]
related: [click-typer, pytest, pytest-asyncio, loguru]
---
Rich for styled terminal output and Textual for full-screen TUIs, with tests driven by Textual's pilot and Rich consoles that record.

## Verify
- `python -c "from rich.console import Console; Console().print('[bold]ok[/]')"`: Rich renders.
- `pytest -q`: Textual tests through `App.run_test()` and Rich output tests through a recording console.
- `textual run --dev app.py` (textual-dev installed): live reload and CSS errors while developing.
- `textual console`: a second terminal that shows `print` and `log` output from the running app.

## Test first
Textual apps run headless with `run_test` and the pilot.
```python
import pytest
from app.tui import CounterApp

@pytest.mark.asyncio
async def test_press_plus_increments():
    app = CounterApp()
    async with app.run_test() as pilot:
        await pilot.press("plus")
        await pilot.pause()
        assert app.query_one("#count").renderable == "1"
```
For Rich, use `Console(record=True, width=80)` and assert on `console.export_text()`.

## Do
- Pass an injected `Console` into functions: `Console(file=io.StringIO(), force_terminal=False, width=80)` in tests, a stderr console for diagnostics.
- Use Rich tables, `Progress` (`track()` for simple loops) and `Console.status()` for long tasks. Use `rich.traceback.install()` for readable errors.
- Escape untrusted text with `rich.markup.escape(text)` before putting it into markup strings.
- In Textual, compose widgets in `compose()`, style with `.tcss` (`CSS_PATH`), and communicate with messages (`post_message`, `on_<widget>_<message>` handlers).
- Keep UI state in reactive attributes (`reactive(0)`) with `watch_<name>` methods.
- Put blocking work in `@work(thread=True)` or async workers so the UI stays responsive, and update widgets with `call_from_thread` when needed.
- Bind keys with `BINDINGS = [("q", "quit", "Quit")]` and expose them in the footer.
- Test snapshots with `pytest-textual-snapshot` for layout regressions.

## Avoid
- Printing user data into Rich markup unescaped: `[red]` in the data changes colours or raises `MarkupError`. Escape.
- Blocking calls (network, `time.sleep`) in message handlers: the UI freezes. Use workers.
- Using `print` inside a running Textual app: it garbles the screen. Use `self.log(...)` and the textual console.
- Mixing `Progress` or `Live` displays with plain `print`: broken redraws. Print through `console.print` or `progress.console`.
- Colour-only meaning and fixed widths: breaks `NO_COLOR` and narrow terminals. Add text cues and respect console width.
- Asserting on ANSI output in tests: brittle. Use `export_text()` or disable colour.

## Review
- [ ] Console is injected, so output is testable and goes to the right stream.
- [ ] Untrusted strings are escaped before markup.
- [ ] Long work runs in workers and the UI never blocks.
- [ ] A pilot test covers each key binding and screen.
