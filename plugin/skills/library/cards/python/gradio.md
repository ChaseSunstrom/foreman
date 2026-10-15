---
name: gradio
title: Gradio
area: python
tags: [python, gradio, ml, web-ui, demo, blocks]
detect: [dep:gradio, dep:gradio-client]
related: [fastapi, streamlit, pytest, httpx]
---
Gradio: quick ML and tool UIs with Interface or Blocks, with queueing, validation and a safe launch configuration.

## Verify
- `python -c "import gradio as gr; print(gr.__version__)"`: the installed major version (APIs differ across majors).
- `pytest -q`: handler functions tested directly, and the app through `gradio_client`.
- `python app.py`: launches on the default local port; open it and exercise each tab.
- `python -c "from app import demo; print(demo.get_api_info() if hasattr(demo,'get_api_info') else 'n/a')"`: endpoints and their typed signatures.

## Test first
Keep logic in plain functions and test those. Test the wiring through the client.
```python
from app.logic import classify

def test_classify_rejects_empty():
    assert classify("") == "Please enter some text."

def test_classify_returns_label():
    assert classify("great product") in {"positive", "negative"}
```
For end to end, launch with `demo.launch(prevent_thread_lock=True)` and call it with `gradio_client.Client(url).predict(..., api_name="/classify")`, then `demo.close()`.

## Do
- Write handlers as ordinary functions with type hints, and wire them with `gr.Interface(fn, inputs, outputs)` or `gr.Blocks()` and `.click(fn, inputs, outputs, api_name="classify")`.
- Validate inputs inside the handler and raise `gr.Error("message")` for user-facing errors; use `gr.Warning` and `gr.Info` for notices.
- Call `demo.queue(default_concurrency_limit=N)` (or `concurrency_limit=` per event) to bound heavy work like model inference.
- Load models once at module level or in `gr.State`-free globals, not inside the handler.
- Stream with generator handlers (`yield`) for progress and token streaming.
- Use `gr.ChatInterface` for chat UIs.
- Set `demo.launch(server_name="0.0.0.0")` only in containers behind a proxy, and add `auth=` or deploy behind real authentication.
- Mount into FastAPI with `gr.mount_gradio_app(app, demo, path="/ui")` to share auth and routes.

## Avoid
- `share=True` with private data or models: it creates a public tunnel link. Keep it off.
- Binding `0.0.0.0` on a laptop or server without auth: exposes the app. Bind localhost unless proxied.
- Heavy model loads per click: slow and memory hungry. Load once.
- Unbounded queues and concurrency: out of memory under load. Set concurrency limits.
- Trusting uploaded file paths and names: path traversal and unsafe parsing. Validate type and size, and process in a temp dir.
- Copying examples from other majors (`.style()`, `gr.inputs`, `gr.outputs`): removed APIs. Use current component arguments.
- Mutating module globals per user session: crossed state. Use `gr.State`.

## Review
- [ ] Logic lives in tested functions, with the UI as thin wiring.
- [ ] Errors reach users through `gr.Error`, not tracebacks.
- [ ] Concurrency is bounded and models load once.
- [ ] Launch settings expose nothing publicly by default.
