"""T-2995: a green exam Smith run keeps its conversation journal beside its events; `sampo exam models --traces DIR`
exports the kept journals as chat JSONL. Fakes only: a fake fm code writes a journal the way Smith does."""
import json
import os
import tempfile
import unittest
from unittest import mock

from helpers import ForemanTestCase  # noqa: F401  (puts plugin/lib on the path)

from sampo import louhi, models, smithbench, traces

FAKE_FM = """import json, os, sys
d = os.path.join(os.environ["FOREMAN_HOME"], "state", "code"); os.makedirs(d)
recs = json.loads(%r)
with open(os.path.join(d, "T-0001.jsonl"), "w") as f:
    for r in recs: f.write(json.dumps(r) + "\\n")
for e in json.loads(%r): print(json.dumps(e))
"""
CALL = {"id": "c1", "type": "function", "function": {"name": "read_file", "arguments": '{"path": "a.py"}'}}


def journal(model="gemma", planner=None, worker=None):
    return [{"kind": "start", "task": "T-0001", "request": "fix it", "model": model, "planner": planner,
             "options": {"worker": worker, "escalate": None}, "messages": []},
            {"kind": "msg", "phase": "s1", "msg": {"role": "system", "content": "You are Smith."}},
            {"kind": "msg", "phase": "s1", "msg": {"role": "user", "content": "fix /home/zed/proj/a.py\n    indented"}},
            {"kind": "msg", "phase": "s1", "msg": {"role": "assistant", "content": "", "tool_calls": [CALL]}},
            {"kind": "msg", "phase": "s1", "msg": {"role": "tool", "tool_call_id": "c1", "content": "x = 1"}},
            {"kind": "msg", "phase": "s1", "msg": {"role": "assistant", "content": "done"}},
            {"kind": "end", "status": "done"}]


GREEN = [{"event": "verify", "label": "verify", "exit": 0}, {"event": "closed", "text": "ok"}]
RED = [{"event": "verify", "label": "verify", "exit": 1}, {"event": "blocked", "text": "no"}]


class Traces(unittest.TestCase):
    def arm(self, recs, events, model="gemma", planner=None, tmp=None):
        base, work = os.path.join(tmp, "base"), os.path.join(tmp, "work")
        os.makedirs(os.path.join(base, "repo"), exist_ok=True)
        with open(os.path.join(base, "repo", "a.py"), "w") as h:
            h.write("x = 1\n")
        fm = os.path.join(tmp, "fm.py")
        with open(fm, "w") as h:
            h.write(FAKE_FM % (json.dumps(recs), json.dumps(events)))
        log = os.path.join(tmp, "answers", "smith", "s1.events.jsonl")
        os.makedirs(os.path.dirname(log), exist_ok=True)
        key = {"id": "s1", "request": "fix it", "kind": "bug", "lang": "python", "origin": "minted"}
        with mock.patch.object(smithbench, "FM", fm), mock.patch.object(models, "resolve", lambda m: {"name": m}), \
                mock.patch.object(models, "complete", lambda *a, **k: {"text": "{}", "tool_calls": []}):
            louhi._smith_arm(base, key, work, model, None, log, planner)
        return log[:-len(".events.jsonl")] + ".journal.jsonl"

    def test_green_keeps_stripped_journal_red_keeps_none(self):
        with tempfile.TemporaryDirectory() as t1, tempfile.TemporaryDirectory() as t2:
            j = self.arm(journal(), GREEN, tmp=t1)
            self.assertTrue(os.path.isfile(j))
            with open(j) as f:
                text = f.read()
            self.assertNotIn("/home/zed", text)
            self.assertIn("    indented", text, "code keeps its indentation")
            self.assertEqual(json.loads(text.splitlines()[0])["meta"]["origin"], "minted")
            self.assertFalse(os.path.exists(self.arm(journal(), RED, tmp=t2)))

    def test_a_claude_slot_keeps_nothing(self):
        for kw in ({"model": "claude-sonnet-5-5"}, {"planner": "my-opus"}):
            with tempfile.TemporaryDirectory() as t:
                self.assertFalse(os.path.exists(self.arm(journal(planner=kw.get("planner")), GREEN, tmp=t, **kw)))
        with tempfile.TemporaryDirectory() as t:
            self.assertFalse(os.path.exists(self.arm(journal(worker="claude"), GREEN, tmp=t)))

    def test_the_size_cap_bounds_a_journal(self):
        recs = journal() + [{"kind": "msg", "phase": "s1", "msg": {"role": "user", "content": "y" * 5000}}] * 400
        with tempfile.TemporaryDirectory() as t:
            j = self.arm(recs, GREEN, tmp=t)
            self.assertLessEqual(os.path.getsize(j), traces.CAP + 20000)

    def export(self, files):
        with tempfile.TemporaryDirectory() as t:
            ans = os.path.join(t, "answers", "smith")
            os.makedirs(ans)
            for n, lines in files.items():
                with open(os.path.join(ans, n), "w") as f:
                    f.write("".join(json.dumps(x) + "\n" for x in lines))
            res = traces.export(ans, os.path.join(t, "out"))
            with open(res["file"]) as f:
                return {**res, "rows": [json.loads(x) for x in f]}

    def kept(self, model="gemma", planner=None, worker=None):
        meta = {"meta": {"scenario": "s1", "language": "python", "kind": "bug", "origin": "seeded", "model": model,
                         "planner": planner, "worker": worker, "outcome": "green"}}
        return [meta] + [r for r in journal(model) if r["kind"] == "msg"]

    def test_export_chat_shape_provenance_and_dedupe(self):
        res = self.export({"s1.journal.jsonl": self.kept(), "s2.journal.jsonl": self.kept()})
        self.assertEqual((res["conversations"], res["dupes"], res["refused"]), (1, 1, 0))
        row = res["rows"][0]
        self.assertEqual([m["role"] for m in row["messages"]], ["system", "user", "assistant", "tool", "assistant"])
        self.assertEqual(row["messages"][2]["tool_calls"][0]["id"], "c1")
        self.assertEqual(row["provenance"], {"scenario": "s1", "language": "python", "kind": "bug", "origin": "seeded",
                                             "model": "gemma", "outcome": "green"})

    def test_export_refuses_a_claude_slot(self):
        res = self.export({"s1.journal.jsonl": self.kept(model="claude-haiku-4-5"),
                           "s2.journal.jsonl": self.kept(planner="sonnet-x")})
        self.assertEqual((res["conversations"], res["refused"]), (0, 2))


if __name__ == "__main__":
    unittest.main()
