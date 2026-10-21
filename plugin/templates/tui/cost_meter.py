"""A sample fm code tui extension: what the run's tokens would cost at a per-token price.

Copy it into the tui folder in Foreman's home (~/.claude/foreman/tui/), then name its panel in a [layout] column of
~/.claude/foreman/tui.toml, for example:  columns = [["log"], ["checks", "files", "cost"]]. The c key cycles the prices.

An extension is a Python file with setup(api). The API is three calls (fmcodetui.API):
  api.panel(name, title, fn)              fn(state, width, height, app) -> lines, each a list of (text, style)
  api.command(name, fn, key=, label=)     fn(app); key binds it unless that key is taken; label shows under ?
  api.on(event, fn)                       fn(state, event) after each fm code event of that kind ("*": every one)
state.ext and app.ext are dicts for an extension's own data. Styles: text, strong, dim, accent, ok, bad, warn, chart,
chip_ok, chip_bad, chip_warn, chip_accent. Only Foreman's home folder is read: a project can't add an extension.
Keep them quick: a panel over 50 ms on 3 frames running, a handler over 50 ms, or a command over 2 s or one that
raises is switched off for the session, with a note in Activity."""

# Example prices in dollars per million tokens (in, out): put your provider's here.
PRICES = [("small model", 1.0, 5.0), ("mid model", 3.0, 15.0), ("large model", 15.0, 75.0)]


def setup(api):
    api.on("tokens", count)
    api.panel("cost", "Cost", panel)
    api.command("cost_price", next_price, key="c", label="the cost panel's next price")


def count(state, event):
    state.ext["model_calls"] = state.ext.get("model_calls", 0) + 1


def next_price(app):
    app.ext["price"] = (app.ext.get("price", 0) + 1) % len(PRICES)


def panel(state, width, height, app):
    name, per_in, per_out = PRICES[app.ext.get("price", 0) if app else 0]
    dollars = state.tokens[0] / 1e6 * per_in + state.tokens[1] / 1e6 * per_out
    calls = state.ext.get("model_calls", 0)
    return [[(f"${dollars:.4f}", "strong"), (f"  at {name} prices", "dim")],
            [(f"{calls} model call{'s' * (calls != 1)}", "dim"), ("   c: next price", "dim")]]
