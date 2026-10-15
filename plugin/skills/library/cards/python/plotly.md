---
name: plotly
title: Plotly
area: python
tags: [python, plotly, visualization, charts, dash, interactive]
detect: [dep:plotly, dep:dash, dep:kaleido]
related: [pandas, matplotlib, jupyter, streamlit]
---
Plotly: interactive charts through Plotly Express or graph_objects, exported as HTML or static images and embedded in Dash apps.

## Verify
- `python -c "import plotly.express as px; px.line(x=[1,2],y=[1,2]).to_json()"`: figures build and serialize.
- `python -c "import plotly.express as px; px.bar(x=['a'],y=[1]).write_html('t.html', include_plotlyjs='cdn')"`: HTML export works.
- `pytest -q`: figure-spec tests (data, layout, traces).
- `python -c "import plotly.io as pio; pio.write_image(__import__('plotly.graph_objects').graph_objects.Figure(), 'f.png')"`: static export works (needs kaleido and a browser it can drive).

## Test first
Assert on the figure object, not the rendered page.
```python
from app.charts import sales_by_region

def test_sales_chart_has_one_bar_per_region():
    fig = sales_by_region({"EU": 3, "US": 5})
    assert fig.layout.title.text == "Sales by region"
    assert list(fig.data[0].x) == ["EU", "US"]
    assert list(fig.data[0].y) == [3, 5]
```

## Do
- Start with `plotly.express` (`px.line`, `px.bar`, `px.scatter`) on tidy DataFrames. Drop to `graph_objects` for custom traces.
- Set title, axis titles and `labels={"col": "Nice name"}`, with units.
- Use `fig.update_layout(template="plotly_white", margin=dict(l=40, r=20, t=50, b=40))` for consistent style.
- Write self-contained HTML with `include_plotlyjs=True`, or `"cdn"` to keep files small.
- Use `fig.to_json()` or `fig.to_dict()` for APIs and `pio.from_json` to restore.
- In Dash: `dcc.Graph(figure=fig)`, callbacks with `Input`/`Output`, and `prevent_initial_call=True` where needed.
- Use `plotly.graph_objects.Scattergl` or `px.scatter(render_mode="webgl")` above roughly 50k points.
- Downsample or aggregate before plotting millions of rows.

## Avoid
- Sending huge DataFrames to the browser: slow pages and large HTML. Aggregate first.
- Static export without kaleido installed: `write_image` fails. Install and test it in CI, or skip image export.
- Treating HTML export as safe with untrusted strings: text fields render HTML in hover and titles. Escape user input.
- Debug mode in production Dash: `app.run(debug=True)` exposes the interactive debugger. Disable it, run behind gunicorn (`server = app.server`).
- Global mutable state in Dash callbacks: breaks multi-worker deployments. Use stores, a database or a cache.
- Callbacks with the same `Output` in several functions: duplicate-output error. Use `allow_duplicate=True` deliberately or merge callbacks.
- Wide-format frames passed to `px` without `melt`: wrong traces. Keep data tidy.

## Review
- [ ] Charts are built by pure functions that return figures and have tests.
- [ ] Axes have titles and units, colours are consistent and accessible.
- [ ] Data volume is capped before plotting.
- [ ] Dash apps are not in debug mode in production and hold no per-process state.
