"""An fm code panel, strict by default (T-1519): a tally of the run's events by kind, to rename and grow from.

`fm new panel` puts it in the tui folder of Foreman's home (~/.claude/foreman/tui/), where fm code loads extensions;
then name the panel in a [layout] column of ~/.claude/foreman/tui.toml:  columns = [["log"], ["checks", "tally"]].
`fm new check PATH` holds a copy to the rules below; plugin/templates/tui/cost_meter.py shows a command on a key.

The rules (fmcodetui.API has the three calls; the check runs each panel at several sizes on an empty run):
- draw returns at most `h` lines, each at most `w` columns: cut it here, so the box never cuts what matters;
- styles are theme names (text, strong, dim, accent, ok, bad, warn, chart, chip_ok, chip_bad, chip_warn,
  chip_accent), never colours, so every theme and palette still reads;
- it reads only the state it is given: no files, network or processes. It runs every frame, and a panel over
  50 ms three frames running is switched off for the session (a handler over 50 ms once);
- the state may have seen no event yet, an event may lack any field, and app is None in the check."""
import fmcodetui as tui  # fm code's own: fit and width count terminal columns (a wide glyph fills two)

NAME, TITLE = "tally", "Events"  # NAME is what the layout lists: rename both together


def setup(api):
    api.on("*", count)
    api.panel(NAME, TITLE, draw)


def count(state, event):
    kind = event.get("event") if isinstance(event, dict) else None
    if isinstance(kind, str):
        tally = state.ext.setdefault(NAME, {})
        tally[kind] = tally.get(kind, 0) + 1


def clip(segments, w):
    """(text, style) segments cut to w columns in all."""
    out = []
    for text, style in segments:
        text = tui.fit(text, w, strip=False)
        w -= tui.width(text)
        if text:
            out.append((text, style))
    return out


def draw(state, w, h, app):
    if w <= 0 or h <= 0:
        return []
    rows = sorted(state.ext.get(NAME, {}).items(), key=lambda kv: (-kv[1], kv[0]))
    if not rows:
        return [clip([("no events yet", "dim")], w)]
    digits, top = len(str(rows[0][1])), rows[0][1]
    label = min(14, max(0, w - digits - 2))
    bar = max(0, w - label - digits - 2)
    lines = [clip([(tui.pad(tui.fit(kind, label), label), "text"), (" " + str(n).rjust(digits), "strong")]
                  + ([(" " + "▆" * max(1, bar * n // top), "chart")] if bar else []), w) for kind, n in rows]
    if len(lines) > h:
        lines = lines[:h - 1] + [clip([(f"+{len(rows) - h + 1} more kinds", "dim")], w)]
    return lines
