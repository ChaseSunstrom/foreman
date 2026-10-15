---
name: lora-fine-tuning
title: LoRA fine-tuning
area: ml
tags: [llm, fine-tuning, lora, peft, qlora, training]
detect: [dep:peft, dep:trl, dep:bitsandbytes, dep:unsloth]
related: [transformers, hf-datasets, pytorch, cuda, vllm, llm-evals]
---
Parameter-efficient fine-tuning with PEFT: LoRA adapters on a frozen base model, optionally 4-bit quantized, trained with TRL or Trainer.

## Verify
- `python -c "import peft, trl; print(peft.__version__, trl.__version__)"`: versions installed.
- `pytest -q`: a tiny-model training smoke test passes on CPU.
- `python -c "from peft import PeftModel"`: adapter loading imports cleanly.
- `python -m evals.run --suite finetune`: the tuned model beats the base on held-out cases (your own harness).

## Test first
Train a few steps on a tiny random model and assert only adapter weights train and the loss is finite.
```python
from transformers import AutoConfig, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model

def test_only_lora_params_are_trainable():
    cfg = AutoConfig.for_model("gpt2", n_layer=1, n_head=2, n_embd=16, vocab_size=50)
    m = get_peft_model(AutoModelForCausalLM.from_config(cfg),
                       LoraConfig(r=4, lora_alpha=8, target_modules=["c_attn"], task_type="CAUSAL_LM"))
    names = [n for n, p in m.named_parameters() if p.requires_grad]
    assert names and all("lora_" in n for n in names)
```

## Do
- Create a `LoraConfig` with `r`, `lora_alpha`, `lora_dropout`, `target_modules` and `task_type`. Target attention and, for more capacity, MLP projections.
- Wrap with `get_peft_model` and print `model.print_trainable_parameters()` to confirm a small trainable share.
- For QLoRA, load the base with `BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=...)` and call `prepare_model_for_kbit_training`.
- Format training data with the model's chat template, and mask prompt tokens so loss covers only the response, or use TRL's `SFTTrainer` options for it.
- Hold out an eval split, evaluate on your task and keep the base-model result as the baseline.
- Save the adapter with `save_pretrained`, and record the base model id and revision beside it.
- Serve by loading the adapter, or merge with `merge_and_unload()` into a full-precision base for deployment.
- Start with a low learning rate and few epochs, and watch eval loss.

## Avoid
- Loss on prompt tokens and padding: the model learns to echo prompts. Mask them with labels set to -100.
- Forgetting the chat template or using a different one at inference: format mismatch hurts quality. Use the same template.
- Merging adapters into a quantized base: lossy or unsupported. Merge into the full-precision base.
- Leaving the base model unpinned: the adapter silently mismatches later. Record id and revision.
- Wrong `target_modules` names for the architecture: no trainable parameters or an error. Inspect module names first.
- Training on test data or duplicated examples: inflated results. Deduplicate and split first.
- Judging by training loss: it falls while behavior regresses. Use held-out task evals.

## Review
- [ ] Trainable parameters are only the adapter, and the share is printed.
- [ ] Prompt masking and chat template match inference.
- [ ] Base model id and revision are saved with the adapter.
- [ ] Held-out eval compares tuned model with the base.
- [ ] Merge and serving path is tested end to end.
