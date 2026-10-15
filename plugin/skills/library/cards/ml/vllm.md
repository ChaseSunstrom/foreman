---
name: vllm
title: vLLM
area: ml
tags: [python, llm, inference, serving, gpu, openai-compatible]
detect: [dep:vllm]
related: [transformers, cuda, lora-fine-tuning, ollama, llm-evals]
---
vLLM serving: batched LLM inference with paged attention, an OpenAI-compatible server and an offline `LLM` class.

## Verify
- `python -c "import vllm; print(vllm.__version__)"`: installed version.
- `vllm serve --help`: the server CLI is present and lists current flags.
- `curl -s localhost:8000/v1/models`: the running server answers and lists the served model.
- `curl -s localhost:8000/health`: the server is healthy.

## Test first
Smoke request against a small model, or a client test against the OpenAI-compatible endpoint, with a short deterministic prompt.
```python
import httpx

def test_completion_endpoint_returns_text(vllm_base_url, served_model):
    r = httpx.post(f"{vllm_base_url}/v1/chat/completions", timeout=60, json={
        "model": served_model, "temperature": 0, "max_tokens": 8,
        "messages": [{"role": "user", "content": "Reply with the word ok."}]})
    assert r.status_code == 200
    assert r.json()["choices"][0]["message"]["content"].strip()
```

## Do
- Serve with `vllm serve <model>` and call it through the OpenAI-compatible API, using the `openai` client with `base_url`.
- Size memory with `--gpu-memory-utilization` and `--max-model-len`. Lower `max-model-len` before reducing batch capacity.
- Use `--tensor-parallel-size` to shard across GPUs on one node.
- Set `--dtype` explicitly (`bfloat16` on supported GPUs), and a `--served-model-name` for stable client config.
- Serve LoRA adapters with `--enable-lora` and `--lora-modules name=path`.
- Use the model's chat template through `/v1/chat/completions` instead of hand-built prompts.
- Pass `SamplingParams(temperature=..., max_tokens=...)` in offline use, and batch many prompts to one `generate` call.
- Put `--api-key` and a reverse proxy in front of any shared deployment.

## Avoid
- A looping client that sends prompts one by one to the offline `LLM`: no batching gain. Submit lists.
- Leaving `--max-model-len` at the model maximum on a small GPU: out-of-memory at startup. Set it lower.
- Running the server with no `--api-key` on a reachable interface: open inference. Add auth or bind to localhost.
- Mixing vLLM and training in one process on the same GPU: memory contention. Separate them.
- Omitting `max_tokens`: long, costly generations. Set it per request.
- Assuming vLLM supports every Hugging Face architecture and quantization format: check the supported list for your version.
- Comparing outputs across runs without `temperature=0` and a seed: false regressions.

## Review
- [ ] Memory flags are set deliberately for the target GPU.
- [ ] Server has auth and is not exposed unintentionally.
- [ ] Clients set `max_tokens`, sampling and a timeout.
- [ ] A smoke test hits `/v1/models` and one completion.
- [ ] Adapters and quantization are checked against supported options.
