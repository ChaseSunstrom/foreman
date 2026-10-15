---
name: dvc
title: DVC
area: ml
tags: [dvc, data-versioning, pipelines, mlops, reproducibility, remote]
detect: [dep:dvc, file:dvc.yaml, file:dvc.lock, file:.dvc/config]
related: [mlflow, feature-stores, wandb, hf-datasets]
---
Version data and models beside git with DVC, and express training as a pipeline whose lock file makes it reproducible.

## Verify
- `dvc status`: workspace matches the lock file and tracked data.
- `dvc repro`: pipeline stages rerun only when deps changed and outputs match `dvc.lock`.
- `dvc push`: tracked data reached the remote; follow with `git status` to confirm only small pointer files changed.
- `dvc metrics diff`: metric changes versus the previous commit.

## Test first
Check the pipeline definition is consistent.
```python
import subprocess

def test_pipeline_is_up_to_date():
    r = subprocess.run(["dvc", "status", "--json"], capture_output=True, text=True)
    assert r.returncode == 0 and r.stdout.strip() in ("{}", "")
```

## Do
- Track large files with `dvc add`; commit the `.dvc` pointer files and `dvc.lock`, not the data.
- Define stages in `dvc.yaml` with explicit `deps`, `params`, `outs`, `metrics` and `plots`.
- Keep hyperparameters in `params.yaml` and reference them in stages so changes trigger reruns.
- Configure a remote (object store) and set credentials through environment or local config, not in git.
- Run `dvc push` and `git push` together; reproduce on a clean clone with `dvc pull` and `dvc repro`.
- Mark non-deterministic outputs and fix seeds; use `cache: false` for small outputs git should hold.
- Use `dvc exp run` for experiments and compare with `dvc exp show`.
- In CI, pull data and run `dvc repro --dry` or full repro on small data.

## Avoid
- Committing data files or `.dvc/cache` to git: bloat. Ignore the cache and push to the remote.
- Editing a tracked output by hand: the hash mismatches. Rerun the stage.
- Forgetting `dvc push`: teammates get pointers without data. Add it to the workflow or CI check.
- Stages that read files not listed in `deps`: stale results. Declare every input.
- Secrets in `.dvc/config`: use `config.local`, which is git-ignored.
- Editing `dvc.lock` manually: regenerate with `dvc repro`.

## Review
- [ ] All inputs and outputs declared in `dvc.yaml`.
- [ ] `dvc.lock` committed and `dvc status` is clean.
- [ ] Remote configured without committed secrets.
- [ ] Params live in `params.yaml`.
- [ ] A clean clone reproduces results.
