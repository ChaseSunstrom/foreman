---
name: matplotlib
title: Matplotlib
area: python
tags: [python, matplotlib, plotting, visualization, charts, figures]
detect: [dep:matplotlib, dep:pytest-mpl]
related: [numpy, pandas, plotly, jupyter, pytest]
---
Matplotlib: object-oriented figures and axes, headless backends and reproducible output for scripts and tests.

## Verify
- `MPLBACKEND=Agg python script.py`: the script renders with no display (CI and servers).
- `pytest -q --mpl`: image comparison tests when pytest-mpl is used (baselines in a `baseline` dir).
- `python -c "import matplotlib; print(matplotlib.get_backend())"`: which backend is active.
- `python -W error -c "import matplotlib.pyplot as plt; plt.subplots(); plt.close('all')"`: no warnings on setup.

## Test first
Assert on the figure's data and labels, not pixels.
```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from app.plots import revenue_chart

def test_revenue_chart_labels_and_data():
    fig = revenue_chart([1, 2, 3])
    ax = fig.axes[0]
    assert ax.get_xlabel() == "Month"
    assert list(ax.lines[0].get_ydata()) == [1, 2, 3]
    plt.close(fig)
```

## Do
- Use the object API: `fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")`, then `ax.plot(...)`, `ax.set_xlabel(...)`.
- Make plotting functions take an `ax` and return it or the figure, so they compose and test.
- Save with `fig.savefig("out.png", dpi=200, bbox_inches="tight")` and `fig.savefig("out.svg")` for vectors.
- Close figures: `plt.close(fig)` after saving, in loops and servers.
- Select the backend before importing pyplot on servers: `matplotlib.use("Agg")` or `MPLBACKEND`.
- Set style centrally with `plt.style.use(...)` or `plt.rc_context({...})`.
- Label axes with units, add legends from `label=` and use colorblind-safe colormaps (`viridis`).
- Pass `rasterized=True` for huge scatter plots in vector output.

## Avoid
- `plt.plot(...)` state-machine calls in reusable code: draws on whichever figure is current. Use explicit `ax`.
- Not closing figures in loops: memory growth and a "more than 20 figures" warning. Close each.
- `plt.show()` in servers or tests: blocks or fails headless. Save to a file or buffer.
- `pyplot` in web request threads: it is not thread safe. Use `matplotlib.figure.Figure()` directly with `fig.savefig(buffer, format="png")`.
- `tight_layout()` mixed with `constrained` layout: conflicts. Choose `layout="constrained"` only.
- Comparing rendered pixels across machines without fixed fonts and versions: flaky. Compare data, or pin the style and use tolerance.
- Rainbow `jet` colormaps for ordered data: misleading. Use a perceptual map.

## Review
- [ ] Functions take and return axes or figures, no hidden global state.
- [ ] Headless backend is set, and figures are closed.
- [ ] Output has labeled axes, units, legend and sensible size and dpi.
- [ ] Tests check data and text, with image baselines only where needed.
