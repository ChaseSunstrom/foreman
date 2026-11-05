"""T-2970: Sampo's own decision model through the installed Jeff stack. The training lake's rows become Jeff Examples
(`sampo exam models --jeff DIR`) for three questions, and jeff-train fits a LoRA adapter on the v1.3 base
(`--train-jeff`). Labels come from outcomes and the user's own words only:
  intake-type   a choice, labelled only where the user tagged the request (FIX:, FEATURE:, ... at its start); the tag
                is cut from the state, so the model learns the words, not the tag
  intake-tier   a choice S/M/L from the realized size: the task's scope count (the lake carries no per-task line count,
                so a diff size stays a follow-up); a task with no scope has no tier row
  close-holds   a yes/no from the lake's outcome: held (true) against reverted or fixed later (false)
A state is the user's request text, plus for close-holds the lake's text-free features; never a section Claude wrote.
Whole projects split train, dev and temperature (Jeff refuses overlapping families), and the held-out project of the
bench (`--holdout`) is in none. The questions are the bench's own (models.shadow_uses, SYSTEMONE_ASK), so the served
adapter is asked what it was trained on."""
import json
import os
import re
import shutil
import subprocess
import tempfile

from sampo import core as c

USES = ("intake-type", "intake-tier", "close-holds")
SUITE = "sampo-"
TAG = re.compile(r"^\s*(FIX|FEATURE|CLEAN|PERF|SECURITY|RESEARCH)\s*[!?]?\s*:\s*(.*)$", re.I | re.S)
NAME = "sampo-decide"  # the adapter dir under Jeff's adapters/, and the model name the server serves it as
PROFILE = "jeff-sampo-decide"
META = os.path.join("research", "models", PROFILE + ".json")  # in the project's state dir: what the adapter held out
TIER_S, TIER_M = 2, 7  # scope files: up to 2 is S ("one or two files"), up to 7 M ("several"), more L
RANK, BASE = 16, "jeff-base-v1.3"
# jeff-train's defaults are full fine-tuning on ~65k rows (lr 2e-6, effective batch 256): on Sampo's ~1.5k that is
# about 6 steps that barely move an adapter. A small-data LoRA instead; dev loss picks the checkpoint every 10 steps.
RECIPE = ("--lr", "0.0001", "--batch-size", "8", "--effective-batch-size", "16", "--epochs", "3", "--eval-every", "10")
GPU_SHARE = 0.5  # another process holding more than this share of the card's memory blocks the train
SHARE = {"train": 0.7, "dev": 0.15, "temperature": 0.15}  # each fold's target share of the Examples, by whole projects
HOLDS = {"instructions": "Will this finished task hold: not reverted and not fixed later?",
         "type": "noul", "criteria": {"true": "it holds", "false": "it was reverted or needed a fix later"}}


class Refused(ValueError):  # a ValueError: `sampo exam` turns it into a usage error
    pass


def jeff_home():
    # T-3173: core moves a launch-time SAMPO_ name to FOREMAN_ at import, so read both
    return os.environ.get("SAMPO_JEFF_HOME") or os.environ.get("FOREMAN_JEFF_HOME") or os.path.expanduser("~/.local/share/sampo/jeff")


def tier_of(files):
    """S, M or L from a scope count; None when there is none (no realized size, no row)."""
    return None if not files else "S" if files <= TIER_S else "M" if files <= TIER_M else "L"


def _text(r):
    return ((r.get("fields") or {}).get("request") or {}).get("text") or ""


def _project(r):
    return (r.get("prov") or {}).get("project")


def _choice(use):
    from sampo import models
    return {"type": "choice", "instructions": models.SYSTEMONE_ASK, "criteria": dict(models.shadow_uses()[use])}


def _example(use, r, state, label):
    return {"id": f"{SUITE}{use}:{r['prov']['task']}", "suite": SUITE + use, "family": _project(r), "state": state,
            "question": _choice(use) if use != "close-holds" else {k: v for k, v in HOLDS.items()},
            "label": label, "target": label, "source": {"dataset": "sampo-lake", "use": use, "day": r["prov"].get("day")}}


def _rows_of(r):
    """[(use, state, label)] one lake row gives."""
    text = _text(r)
    if not text or not _project(r):
        return []
    out = []
    m = TAG.match(text)
    body = (m.group(2) if m else text).strip()
    if m and body:
        t = m.group(1).upper()
        out.append(("intake-type", body, "PERFORMANCE" if t == "PERF" else t))
    feats = (r.get("features") or {})
    if (tier := tier_of(feats.get("files"))) and body:
        out.append(("intake-tier", body, tier))
    if isinstance(r.get("features"), dict) and r.get("label") in ("held", "reverted", "regret") and body:
        out.append(("close-holds", {"features": r["features"], "request": body}, r["label"] == "held"))
    return out


def auto_holdout(rows):
    """The project to hold out when none is named: the largest one that still leaves 60% of the rows to train on, else
    the smallest with 5 rows or more; None when no project qualifies."""
    n, per = {}, {}
    for r in rows:
        if _project(r):
            per[_project(r)] = per.get(_project(r), 0) + 1
    n = sum(per.values())
    ok = sorted((k for k, v in per.items() if v <= 0.4 * n), key=lambda k: (-per[k], k))
    if ok:
        return ok[0]
    big = sorted((k for k, v in per.items() if v >= 5), key=lambda k: (per[k], k))
    return big[0] if big else None


def examples(rows, holdout=None):
    """({train, dev, temperature: [Example]}, info): every lake row's Examples, whole projects to a part. The held-out
    project is in none; with fewer than 3 other projects everything trains (and the later check refuses empty folds)."""
    projs = sorted({_project(r) for r in rows if _project(r)})
    if holdout is not None and holdout not in projs:
        raise ValueError(f"holdout {holdout!r} is not a project in the lake ({len(projs)} projects)")
    # T-2970 live: only projects that give Examples take a fold (an empty one left temperature empty). Largest first,
    # each goes to the fold furthest below its share (70/15/15), so dev and temperature get rows when 3+ projects do
    size = {p: sum(len(_rows_of(r)) for r in rows if _project(r) == p and not r.get("canary")) for p in projs}
    rest = sorted((p for p in projs if p != holdout and size[p]), key=lambda p: (-size[p], p))
    total, have, part = sum(size[p] for p in rest), {"train": 0, "dev": 0, "temperature": 0}, {}
    for i, p in enumerate(rest):
        fold = "train" if len(rest) < 3 or i == 0 else (
            "dev" if not have["dev"] else "temperature" if not have["temperature"] else
            max(have, key=lambda f: SHARE[f] * total - have[f]))
        part[p], have[fold] = fold, have[fold] + size[p]
    out = {"train": [], "dev": [], "temperature": []}
    for r in rows:
        if r.get("canary") or _project(r) not in part:
            continue
        out[part[_project(r)]] += [_example(u, r, s, lab) for u, s, lab in _rows_of(r)]
    info = {"holdout": holdout, "projects": {k2: sorted(p for p, v in part.items() if v == k2) for k2 in out},
            "counts": {k2: {u: sum(e["suite"] == SUITE + u for e in v) for u in USES} for k2, v in out.items()}}
    return out, info


def write(out_dir, split, info=None):
    os.makedirs(out_dir, exist_ok=True)
    for name, exs in {"train": split["train"], "dev": split["dev"], "temperature": split["temperature"]}.items():
        c.write_atomic(os.path.join(out_dir, name + ".jsonl"),
                       "".join(json.dumps(e, sort_keys=True, ensure_ascii=False) + "\n" for e in exs))
    c.write_atomic(os.path.join(out_dir, "manifest.json"), json.dumps(info or {}, indent=2, sort_keys=True) + "\n")


def export(p, out_dir, holdout=None):
    """sampo exam models --jeff DIR: the lake's Examples to DIR (train.jsonl, dev.jsonl, temperature.jsonl, manifest.json)
    and the held-out project to this project's state (the bench reads it). Returns the manifest."""
    from sampo import lake
    rows = [r for r in lake.collect()[0] if not r.get("canary")]
    hold = holdout or auto_holdout(rows)
    split, info = examples(rows, hold)
    write(out_dir, split, info)
    c.write_atomic(os.path.join(p.dir, META), json.dumps({"holdout": hold, "at": c.now(), "counts": info["counts"]}) + "\n")
    return info


def holdout_of(p):
    """The project hash the adapter's data held out (None: no adapter data yet, or none was held out)."""
    try:
        with open(os.path.join(p.dir, META), encoding="utf-8") as f:
            return json.load(f).get("holdout")
    except (OSError, ValueError, AttributeError):
        return None


# ---------------------------------------------------------------- the train
def busy_gpu(smi=("nvidia-smi",), share=GPU_SHARE):
    """None when the card is free enough; else why not: the processes holding more than `share` of its memory (named),
    or that the card can't be read (an unreadable card is not a free one)."""
    q = lambda *a: subprocess.run([*smi, *a, "--format=csv,noheader,nounits"], capture_output=True, text=True,  # noqa: E731
                                  timeout=20)
    try:
        tot = q("--query-gpu=memory.total")
        apps = q("--query-compute-apps=pid,process_name,used_memory")
        total = max(int(x) for x in tot.stdout.split() if x.isdigit())
        if tot.returncode or apps.returncode:
            raise ValueError("nvidia-smi failed")
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return "cannot read the GPU (nvidia-smi missing or failing): not training blind"
    held = []
    for line in apps.stdout.splitlines():
        pid, _, rest = line.partition(",")
        name, _, mem = rest.rpartition(",")
        if mem.strip().isdigit():
            held.append((int(mem), name.strip() or "?", pid.strip()))
    used = sum(m for m, _, _ in held)
    if used > share * total:
        top = ", ".join(f"{n} (pid {p}, {m} MiB)" for m, n, p in sorted(held, reverse=True))
        return f"another model holds {used} of {total} MiB of the GPU: {top}; stop it or wait, then run again"
    return None


def profile():
    return {"name": PROFILE, "kind": "systemone", "base_url": "http://127.0.0.1:8766", "model": NAME, "key_env": None}


def _identity(jeff):
    """--base-model and --revision as the base checkpoint records them: jeff-train refuses a start whose requested
    model differs (its defaults name a 27B), so they come from BASE/decision_config.json (T-2970 live)."""
    try:
        with open(os.path.join(jeff, BASE, "decision_config.json"), encoding="utf-8") as f:
            cfg = json.load(f)
    except (OSError, ValueError) as e:
        raise Refused(f"no readable {BASE}/decision_config.json under {jeff}: {e}") from None
    if not (isinstance(cfg.get("base_model"), str) and isinstance(cfg.get("revision"), str)):
        raise Refused(f"{BASE}/decision_config.json names no base_model and revision")
    return ["--base-model", cfg["base_model"], "--revision", cfg["revision"]]


def train(jeff, data, smi=("nvidia-smi",), cmd=None, timeout=6 * 3600, rank=RANK):
    """Run jeff-train on DATA's folds (a LoRA of `rank` on the v1.3 base), then keep its last step as JEFF/adapters/
    sampo-decide (the old one stays until the new one has landed). Refused when a fold is empty, the GPU is held or
    unreadable, or jeff-train fails. Returns {adapter, run, profile}. Never run from a test without fakes."""
    paths = {k: os.path.join(data, k + ".jsonl") for k in ("train", "dev", "temperature")}
    for k, f in paths.items():
        if not os.path.exists(f) or not os.path.getsize(f):
            raise Refused(f"{k} fold is empty or missing ({f}): run sampo exam models --jeff first; Jeff needs all three")
    if why := busy_gpu(smi):
        raise Refused(why)
    stamp = c.now().replace(":", "").replace("-", "")
    run = os.path.join(jeff, "runs", f"{NAME}-{stamp}")
    out = os.path.join(run, "out")
    cmd = list(cmd or ["uv", "run", "--no-default-groups", "--extra", "lora", "--extra", "cuda", "jeff-train"])
    argv = [*cmd, "--train", paths["train"], "--development", paths["dev"], "--temperature", paths["temperature"],
            "--run", os.path.join(run, "state"), "--output", out, "--initial-checkpoint", BASE, "--lora-rank", str(rank),
            *RECIPE, *_identity(jeff)]
    os.makedirs(run, exist_ok=True)
    env = dict(os.environ, JEFF_EVENTS=os.path.join(run, "events.jsonl"))  # jeff-train won't start from a checkpoint without it
    try:
        r = subprocess.run(argv, cwd=jeff, env=env, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise Refused(f"jeff-train did not finish: {e}") from None
    steps = sorted(d for d in os.listdir(out) if d.startswith("step-")) if os.path.isdir(out) else []
    if r.returncode or not steps:
        raise Refused(f"jeff-train exited {r.returncode} with {len(steps)} checkpoints: {(r.stderr or r.stdout)[-400:]}")
    # jeff-train links out/selected to the step with the lowest dev loss; the last step only when it made no link
    sel = os.path.join(out, "selected")
    pick = os.path.basename(os.path.realpath(sel)) if os.path.islink(sel) else steps[-1]
    pick = pick if pick in steps else steps[-1]
    dest = os.path.join(jeff, "adapters", NAME)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    # staged in the run, not adapters/: the server loads every dir there, so a killed copy would be served
    tmp = tempfile.mkdtemp(prefix=NAME + ".", dir=run)
    try:
        shutil.copytree(os.path.join(out, pick), tmp, dirs_exist_ok=True)
        shutil.rmtree(dest, ignore_errors=True)
        os.rename(tmp, dest)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return {"adapter": dest, "run": run, "step": pick, "profile": profile()}
