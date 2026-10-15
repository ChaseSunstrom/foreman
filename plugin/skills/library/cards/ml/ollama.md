---
name: ollama
title: Ollama
area: ml
tags: [llm, local-inference, ollama, modelfile, api, python]
detect: [dep:ollama, file:Modelfile]
related: [vllm, transformers, rag, llm-evals]
---
Ollama local models: the daemon on port 11434, pull and run, Modelfiles, the REST and client APIs, and context settings.

## Verify
- `ollama list`: which models are installed locally.
- `curl -s localhost:11434/api/tags`: the daemon is up and returns installed models.
- `ollama show <model>`: the model's parameters, template and context length.
- `ollama create <name> -f Modelfile`: the Modelfile parses and builds a model.

## Test first
Smoke request with a tiny model, `stream` off and a fixed seed and `temperature` 0. Gate it so CI without the daemon skips.
```python
import httpx, pytest

def daemon_up():
    try: return httpx.get("http://localhost:11434/api/tags", timeout=2).status_code == 200
    except httpx.HTTPError: return False

@pytest.mark.skipif(not daemon_up(), reason="ollama not running")
def test_generate_returns_text(small_model):
    r = httpx.post("http://localhost:11434/api/chat", timeout=120, json={
        "model": small_model, "stream": False, "options": {"temperature": 0, "seed": 1},
        "messages": [{"role": "user", "content": "Say ok."}]})
    assert r.json()["message"]["content"].strip()
```

## Do
- Use `/api/chat` with a `messages` list so the model's template applies. `/api/generate` takes a raw prompt.
- Set `options` per request: `temperature`, `seed`, `num_ctx`, `num_predict`.
- Raise `num_ctx` when prompts are long: the default context is small and input is truncated silently.
- Pull exact tags (`name:tag`) and pin them in config. Pull in setup, not at request time.
- Write a `Modelfile` with `FROM`, `PARAMETER`, `SYSTEM` and `TEMPLATE`, and `ollama create` to bake in a config.
- For structured output, pass a JSON schema in the `format` field.
- Use `keep_alive` to control how long a model stays loaded.
- Embeddings: use `/api/embed` with an embedding model, and keep that model fixed per index.

## Avoid
- Expecting long inputs to work at the default `num_ctx`: the prompt is cut and answers ignore it. Set `num_ctx`.
- Using `latest` tags: behavior changes after a re-pull. Pin a tag.
- Binding the daemon to `0.0.0.0` (`OLLAMA_HOST`) with no auth or firewall: open model access. Keep it local or proxy with auth.
- Leaving streaming on in a client that parses one JSON body: it receives many lines. Set `stream: false` or parse line by line.
- Treating local model output as equal to a hosted frontier model in evals: re-run your evals per model.
- Loading a model larger than VRAM and ignoring slow CPU offload: check `ollama ps` for the processor split.
- Tests that need the daemon without a skip: fail in CI. Gate them.

## Review
- [ ] Model tags are pinned and pulled at setup.
- [ ] `num_ctx`, `num_predict` and sampling options are explicit.
- [ ] The daemon is not exposed beyond the host without auth.
- [ ] Streaming versus non-streaming matches the client parser.
- [ ] Daemon-dependent tests skip when it is absent.
