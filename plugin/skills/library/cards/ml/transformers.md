---
name: transformers
title: Hugging Face Transformers
area: ml
tags: [python, nlp, llm, huggingface, tokenizers, inference]
detect: [dep:transformers, dep:tokenizers, dep:accelerate]
related: [pytorch, hf-datasets, lora-fine-tuning, vllm, onnx]
---
Hugging Face Transformers: AutoModel and AutoTokenizer loading, pipelines, generate, Trainer, and device and dtype handling.

## Verify
- `python -c "import transformers, torch; print(transformers.__version__, torch.cuda.is_available())"`: install and device.
- `pytest -q`: tests on a tiny random-weight config pass offline.
- `HF_HUB_OFFLINE=1 pytest -q`: tests do not silently download from the hub.
- `ruff check . && ruff format --check .`: lint and format.

## Test first
Build a tiny model from a config so tests are fast and offline.
```python
import torch
from transformers import AutoConfig, AutoModelForCausalLM

def test_forward_shape_and_loss():
    cfg = AutoConfig.for_model("gpt2", n_layer=1, n_head=2, n_embd=16, vocab_size=50)
    m = AutoModelForCausalLM.from_config(cfg)
    ids = torch.randint(0, 50, (2, 6))
    out = m(input_ids=ids, labels=ids)
    assert out.logits.shape == (2, 6, 50) and out.loss.isfinite()
```

## Do
- Load the tokenizer and model from the same checkpoint id and pin `revision` for reproducibility.
- Set `torch_dtype` (for example `torch.bfloat16`) and `device_map="auto"` for large models. `device_map` needs `accelerate`.
- Call `model.eval()` and use `torch.inference_mode()` for inference.
- Tokenize with `padding`, `truncation` and `max_length`, and pass the `attention_mask` through to the model.
- For chat models, build prompts with `tokenizer.apply_chat_template(messages, add_generation_prompt=True)`.
- Decode only the new tokens: slice off the prompt length before `batch_decode`.
- Set `pad_token` explicitly when it is missing (often to `eos_token`), and use left padding for batched generation.
- Use `trust_remote_code=True` only for reviewed, pinned repos.

## Avoid
- Hand-formatting chat prompts: wrong special tokens degrade output. Use the chat template.
- Right padding for decoder-only batched `generate`: garbage continuations. Set `tokenizer.padding_side="left"`.
- `do_sample=False` with `temperature` set, or the reverse: the setting is ignored or warns. Match `do_sample` to the intent.
- Forgetting `max_new_tokens`: generation stops at a small default or runs to the model limit. Set it.
- `model.to("cuda")` on a model loaded with `device_map`: conflicts with dispatch. Pick one.
- `trust_remote_code=True` on arbitrary repos: runs downloaded code. Review and pin the revision.
- `use_auth_token=`: deprecated. Use `token=`.
- Loading weights in fp32 by default for a large model: memory blowup. Pass `torch_dtype`.

## Review
- [ ] Tokenizer and model come from the same pinned checkpoint.
- [ ] Padding side, pad token and attention mask are correct for the architecture.
- [ ] Generation parameters are explicit (`max_new_tokens`, sampling flags).
- [ ] Tests use tiny configs and run offline.
- [ ] No unreviewed `trust_remote_code`.
