"""T-2970: Jeff Examples from the training lake (intake-type from user tags only, intake-tier from the realized size,
close-holds from the outcome), split by whole projects with the held-out project in none, no agent text in any state;
and the LoRA runner: refuses a busy GPU (fake nvidia-smi), runs a fake jeff-train, keeps the adapter. No real training."""
import json
import os
import stat

from helpers import SampoTestCase
from test_lake import Lake

from sampo import jeffexport as jx
from sampo import louhi


def row(proj, i, text, label="held", typ="FIX", files=1, agent="AGENT-WORDS"):
    return {"prov": {"project": proj, "task": f"{proj}{i}", "day": "2026-01-01"}, "label": label, "type": typ, "tier": "S",
            "fields": {"request": {"author": "user", "text": text}, "interpretation": {"author": "agent", "text": agent}},
            "features": {"files": files, "criteria": 2, "tests_run": 3}, "tool_text": {"text": agent}}


def lake(n=6):
    rows = []
    for k in range(n):
        p = f"proj{k}"
        rows += [row(p, 0, "FIX: the parser crashes", "held", files=1),
                 row(p, 1, "FEATURE!: add csv export", "reverted", files=4),
                 row(p, 2, "no tag here, just words", "regret", files=9),
                 row(p, 3, "RESEARCH?: compare two things", "settling", files=0),
                 row(p, 4, "PERF: make it faster", "held", files=2)]
    return rows


class Export(SampoTestCase):
    def split(self, **kw):
        return jx.examples(lake(), **kw)

    def uses(self, exs, use):
        return [e for e in exs if e["suite"] == "sampo-" + use]

    def test_type_is_labelled_only_where_the_user_tagged_and_the_tag_is_not_in_the_state(self):
        sp, _ = self.split()
        t = self.uses(sp["train"], "intake-type")
        self.assertEqual({e["label"] for e in t}, {"FIX", "FEATURE", "RESEARCH", "PERFORMANCE"})  # PERF -> the bench's name
        self.assertTrue(all(e["question"]["type"] == "choice" for e in t))
        self.assertFalse(any("no tag here" in e["state"] for e in t))  # untagged: no type row
        self.assertFalse(any(e["state"].lstrip().upper().startswith(("FIX", "FEATURE", "PERF")) for e in t))

    def test_tier_comes_from_the_realized_size_and_a_row_without_one_is_dropped(self):
        sp, _ = self.split()
        t = {e["state"]: e["label"] for e in self.uses(sp["train"], "intake-tier")}
        self.assertEqual(t["the parser crashes"], "S")
        self.assertEqual(t["add csv export"], "M")
        self.assertEqual(t["no tag here, just words"], "L")
        self.assertNotIn("compare two things", t)  # 0 files: neither a diff nor a scope
        self.assertEqual(jx.tier_of(0), None)
        self.assertEqual([jx.tier_of(n) for n in (1, 2, 3, 7, 8)], ["S", "S", "M", "M", "L"])

    def test_close_holds_is_the_outcome_and_settling_rows_are_left_out(self):
        sp, _ = self.split()
        h = self.uses(sp["train"], "close-holds")
        self.assertEqual({e["label"] for e in h}, {True, False})
        self.assertEqual(h[0]["question"]["type"], "noul")
        self.assertEqual(len(h), 4 * 4)  # 4 train projects x (held, reverted, regret, held); settling skipped
        self.assertEqual(h[0]["state"]["features"], {"files": h[0]["state"]["features"]["files"], "criteria": 2, "tests_run": 3})

    def test_no_agent_or_tool_text_reaches_any_state(self):
        sp, _ = self.split()
        every = [e for part in sp.values() for e in part]
        self.assertTrue(every)
        self.assertNotIn("AGENT-WORDS", json.dumps(every))

    def test_whole_projects_and_the_holdout_is_in_none(self):
        sp, info = self.split(holdout="proj5")
        seen = {k: {e["family"] for e in v} for k, v in sp.items()}
        self.assertTrue(all(seen.values()), seen)  # none of the three empty
        self.assertFalse(seen["train"] & seen["dev"] or seen["train"] & seen["temperature"] or seen["dev"] & seen["temperature"])
        self.assertNotIn("proj5", json.dumps(sp))
        self.assertNotIn("proj5", {f for s in seen.values() for f in s})
        self.assertEqual(info["holdout"], "proj5")
        ids = [e["id"] for v in sp.values() for e in v]
        self.assertEqual(len(ids), len(set(ids)))

    def test_deterministic_and_a_missing_holdout_is_an_error(self):
        self.assertEqual(self.split()[0], self.split()[0])
        with self.assertRaises(ValueError):
            jx.examples(lake(), holdout="nope")

    def test_auto_holdout_leaves_most_of_the_rows_to_train(self):
        rows = lake() + [row("big", i, "FIX: x%d" % i) for i in range(60)]
        h = jx.auto_holdout(rows)
        self.assertNotEqual(h, "big")
        self.assertIsNone(jx.auto_holdout(lake()[:2]))


class Train(SampoTestCase):
    def script(self, name, body):
        path = os.path.join(self.tmp, name)
        with open(path, "w") as f:
            f.write("#!/bin/sh\n" + body)
        os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)
        return path

    def data(self):
        d = os.path.join(self.tmp, "data")
        sp, _ = jx.examples(lake(), holdout="proj5")
        jx.write(d, sp)
        return d

    def jeff(self):
        d = os.path.join(self.tmp, "jeff")
        os.makedirs(d)
        return d

    def smi(self, used, total=24000):
        return self.script("smi", f'case "$*" in *memory.total*) echo {total};; '
                                  f'*) printf "%s\\n" "11, ollama, {used}";; esac\n')

    def test_a_busy_gpu_refuses_and_names_the_holder_and_never_starts_jeff_train(self):
        marker = os.path.join(self.tmp, "ran")
        fake = self.script("jt", f"touch {marker}\n")
        with self.assertRaises(jx.Refused) as cm:
            jx.train(self.jeff(), self.data(), smi=[self.smi(15000)], cmd=[fake])
        self.assertIn("ollama", str(cm.exception))
        self.assertFalse(os.path.exists(marker))

    def test_no_nvidia_smi_refuses_too(self):
        with self.assertRaises(jx.Refused):
            jx.train(self.jeff(), self.data(), smi=[os.path.join(self.tmp, "absent")], cmd=["true"])

    def test_a_free_gpu_trains_with_the_lora_flags_and_keeps_the_last_step_as_the_adapter(self):
        j = self.jeff()
        log = os.path.join(self.tmp, "argv")
        fake = self.script("jt", f'echo "$@" > {log}; echo "$JEFF_EVENTS" >> {log}\n'
                                 'out=""; while [ $# -gt 0 ]; do [ "$1" = --output ] && out=$2; shift; done\n'
                                 'mkdir -p "$out/step-00010" "$out/step-00020"; echo a > "$out/step-00010/w"; echo b > "$out/step-00020/w"\n')
        res = jx.train(j, self.data(), smi=[self.smi(2000)], cmd=[fake])
        argv = open(log).read()
        for want in ("--lora-rank 16", "--initial-checkpoint jeff-base-v1.3", "--train ", "--development ", "--temperature "):
            self.assertIn(want, argv)
        self.assertIn("events", argv.splitlines()[1])  # JEFF_EVENTS is set: jeff-train refuses to start without it
        with open(os.path.join(j, "adapters", "sampo-decide", "w")) as f:
            self.assertEqual(f.read().strip(), "b")
        self.assertEqual(res["profile"]["name"], "jeff-sampo-decide")
        self.assertEqual(res["profile"]["model"], "sampo-decide")
        self.assertEqual(res["profile"]["kind"], "systemone")
        # a second run keeps the old adapter until the new one has landed, then replaces it
        jx.train(j, self.data(), smi=[self.smi(2000)], cmd=[fake])
        self.assertEqual(sorted(os.listdir(os.path.join(j, "adapters"))), ["sampo-decide"])

    def test_a_failed_train_keeps_the_old_adapter_and_raises(self):
        j = self.jeff()
        keep = os.path.join(j, "adapters", "sampo-decide")
        os.makedirs(keep)
        open(os.path.join(keep, "old"), "w").close()
        with self.assertRaises(jx.Refused):
            jx.train(j, self.data(), smi=[self.smi(0)], cmd=[self.script("bad", "exit 3\n")])
        self.assertTrue(os.path.exists(os.path.join(keep, "old")))

    def test_empty_folds_refuse_before_the_gpu_is_asked(self):
        d = os.path.join(self.tmp, "thin")
        jx.write(d, {"train": [], "dev": [], "temperature": []})
        with self.assertRaises(jx.Refused):
            jx.train(self.jeff(), d, smi=["false"], cmd=["true"])


class Wired(Lake):
    def test_the_cli_writes_the_three_files_and_the_holdout_is_named(self):
        out = os.path.join(self.tmp, "jeffdata")
        r = self.fm("exam", "models", "--jeff", out, "--holdout", "none-such", "--json", check=False)
        self.assertNotEqual(r.returncode, 0)
        r = self.fm("exam", "models", "--jeff", out, "--json")
        res = json.loads(r.stdout)
        self.assertEqual(sorted(os.listdir(out)), ["dev.jsonl", "manifest.json", "temperature.jsonl", "train.jsonl"])
        self.assertIn("counts", res)
        self.assertNotIn("task number", open(os.path.join(out, "train.jsonl")).read())

    def test_the_adapter_scores_only_where_it_never_trained(self):
        seen = []
        make = louhi._held_out_only(lambda train, use: (lambda text: seen.append(text) or ("FIX", 0.9)), "pX")
        self.assertIsNone(make([{"project": "pX"}], "intake-type")("t"))  # trained on pX: abstains
        self.assertEqual(make([{"project": "pY"}], "intake-type")("t"), ("FIX", 0.9))  # pX is the held-out one
        self.assertEqual(seen, ["t"])
