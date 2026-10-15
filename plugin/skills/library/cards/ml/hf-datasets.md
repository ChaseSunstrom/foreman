---
name: hf-datasets
title: Hugging Face Datasets
area: ml
tags: [python, datasets, huggingface, arrow, preprocessing, streaming]
detect: [dep:datasets]
related: [transformers, pytorch, lora-fine-tuning, llm-evals]
---
Hugging Face Datasets: Arrow-backed Dataset and DatasetDict, map and filter pipelines, streaming and splits.

## Verify
- `python -c "from datasets import load_dataset; print(load_dataset('json', data_files='sample.jsonl', split='train'))"`: the loader reads the local sample with the expected columns.
- `pytest -q`: preprocessing tests pass on in-memory datasets.
- `HF_DATASETS_OFFLINE=1 pytest -q`: tests do not reach the network.
- `ruff check . && ruff format --check .`: lint and format.

## Test first
Build a small dataset in memory with `Dataset.from_dict`, run the transform, assert columns and values.
```python
from datasets import Dataset
from mypkg.prep import tokenize_batch

def test_map_adds_ids_and_drops_text():
    ds = Dataset.from_dict({"text": ["a b", "c"]})
    out = ds.map(tokenize_batch, batched=True, remove_columns=["text"])
    assert out.column_names == ["input_ids"]
    assert len(out) == 2
```

## Do
- Use `map(fn, batched=True)` and `remove_columns` for tokenization. Pass `num_proc` for CPU-heavy transforms.
- Make map functions pure and deterministic so the cache fingerprint is stable.
- Split with `train_test_split(test_size=..., seed=...)` and keep a held-out split that is never mapped over for tuning.
- Use `streaming=True` for corpora too large for disk, and `IterableDataset.shuffle(buffer_size=...)`.
- Call `set_format("torch")` or `with_format("torch")` to get tensors out. Pad in a collator, not in `map`.
- Use `save_to_disk` and `load_from_disk` for processed copies.
- Pin `revision` when loading hub datasets.

## Avoid
- Python loops over rows (`for r in ds`) to transform: slow. Use `map` batched.
- `ds[0]["x"]` in a loop for random access on huge data: materializes repeatedly. Use `ds["x"]` columns or iterate in batches.
- Streaming datasets with `len()` or random indexing: unsupported. Use `take`, `skip` and iteration.
- Shuffling before a split without a seed: leaks differ per run. Seed it.
- Padding to a global max length inside `map`: wastes memory. Pad dynamically in a collator.
- `trust_remote_code=True` for dataset scripts: runs downloaded code. Prefer parquet or json data files.
- Mapping non-deterministic functions (random, time): cache returns stale results or never hits. Pass `new_fingerprint` or seed explicitly.

## Review
- [ ] Transforms are batched, pure and remove raw columns.
- [ ] Splits are seeded and the test set is isolated from tuning.
- [ ] Revisions or file hashes pin the data.
- [ ] Padding happens in the collator.
- [ ] Tests build datasets in memory and run offline.
