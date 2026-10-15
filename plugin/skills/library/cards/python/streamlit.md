---
name: streamlit
title: Streamlit
area: python
tags: [python, streamlit, dashboard, data-app, ui, caching]
detect: [dep:streamlit]
related: [pandas, polars, pytest, plotly]
---
Streamlit apps: scripts that rerun top to bottom on each interaction, with `st.session_state`, caching and widgets.

## Verify
- `streamlit run app.py --server.headless true`: the app starts without opening a browser (stop it after the "You can now view" line).
- `python -c "from streamlit.testing.v1 import AppTest; print(AppTest)"`: the built-in test harness is available.
- `pytest -q`: the suite, including `AppTest` tests.
- `ruff check . && pyright`: lint and types for the script and helpers.

## Test first
Drive the script headlessly with `AppTest`; no browser.
```python
from streamlit.testing.v1 import AppTest

def test_empty_name_shows_error():
    at = AppTest.from_file("app.py").run()
    at.text_input[0].set_value("").run()
    at.button[0].click().run()
    assert at.error[0].value == "Name is required"
```
Put logic in plain functions and test those directly; use `AppTest` for flow.

## Do
- Treat the script as rerunning on every interaction; keep expensive work out of the top level.
- Cache data loads with `@st.cache_data` (returns copies, hashable args) and shared resources (clients, models, connections) with `@st.cache_resource`; set `ttl=`.
- Store per-user state in `st.session_state`; initialize keys with `if "k" not in st.session_state:`.
- Give widgets stable `key=` values and use `on_change`/`on_click` callbacks for state updates that must happen before the rerun.
- Wrap related inputs in `st.form` with `st.form_submit_button` to batch reruns.
- Read secrets from `st.secrets` (`.streamlit/secrets.toml`, gitignored) or env.
- Use `st.fragment` to rerun only part of a page, and `st.spinner` or `st.status` for long work.
- Split pages in a `pages/` directory or with `st.navigation`.

## Avoid
- Loading data or creating DB clients at top level without caching: repeated on every click. Cache them.
- Mutating a value returned by `@st.cache_data`: it is a copy, so changes are lost. Mutate `cache_resource` objects only with care for sharing across sessions.
- Module-level global variables as state: shared across users and sessions. Use `st.session_state`.
- Assuming a widget value changes immediately after assignment in the same run: it does not. Use callbacks or `st.rerun()`.
- Committing `secrets.toml` or API keys in the script: leaks. Use `st.secrets` with the file ignored.
- `st.experimental_*` APIs (`experimental_rerun`, `experimental_memo`, `experimental_singleton`): removed. Use `st.rerun`, `cache_data`, `cache_resource`.
- Duplicate widgets with identical labels and no `key`: `DuplicateWidgetID`. Add keys.

## Review
- [ ] Expensive calls are cached with appropriate `ttl` and scope.
- [ ] State lives in `st.session_state`, not module globals.
- [ ] Business logic is in plain functions with ordinary tests.
- [ ] Secrets are not in the repo, and user input is validated before use.
- [ ] No removed `experimental_*` calls remain.
