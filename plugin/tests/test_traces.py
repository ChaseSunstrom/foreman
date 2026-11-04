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
d = os.path.join(os.environ["FOREMAN_HOME"], "state", "code") if not %r else os.path.join(os.getcwd(), "code")
os.makedirs(d)
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
    def arm(self, recs, events, model="gemma", planner=None, tmp=None, plant=False, check="suite"):
        base, work = os.path.join(tmp, "base"), os.path.join(tmp, "work")
        os.makedirs(os.path.join(base, "repo"), exist_ok=True)
        with open(os.path.join(base, "repo", "a.py"), "w") as h:
            h.write("x = 1\n")
        fm = os.path.join(tmp, "fm.py")
        with open(fm, "w") as h:
            h.write(FAKE_FM % (plant, json.dumps(recs), json.dumps(events)))
        log = os.path.join(tmp, "answers", "smith", "s1.events.jsonl")
        os.makedirs(os.path.dirname(log), exist_ok=True)
        key = {"id": "s1", "request": "fix it", "kind": "bug", "lang": "python", "origin": "minted",
               "defects": [{"kind": "bug", "check": {"type": check}}]}
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

    def test_a_run_the_grader_calls_fixed_keeps_its_journal_without_a_close(self):  # live: 27B fixed 1 of 4, no close
        with tempfile.TemporaryDirectory() as t1, tempfile.TemporaryDirectory() as t2:
            timeout = [{"event": "timeout", "text": "used all 40 turns"}]
            with mock.patch.object(louhi, "passes", lambda base, key, d, target: True):
                self.assertTrue(os.path.isfile(self.arm(journal(), timeout, tmp=t1)))
            with mock.patch.object(louhi, "passes", lambda base, key, d, target: False):
                self.assertFalse(os.path.exists(self.arm(journal(), timeout, tmp=t2)))

    def test_only_proof_keeps_a_run(self):  # T-2995 review: a close with no verify, or a guard-only pass, proves nothing
        timeout = [{"event": "timeout", "text": "used all 40 turns"}]
        with tempfile.TemporaryDirectory() as t1, tempfile.TemporaryDirectory() as t2, \
                tempfile.TemporaryDirectory() as t3:
            with mock.patch.object(louhi, "passes", lambda base, key, d, target: False):
                self.assertFalse(os.path.exists(self.arm(journal(), [{"event": "closed", "text": "ok"}], tmp=t1)))
            with mock.patch.object(louhi, "passes", lambda base, key, d, target: True):
                self.assertFalse(os.path.exists(self.arm(journal(), timeout, tmp=t2, check="intact")))
                with open(self.arm(journal(), timeout, tmp=t3)) as f:
                    self.assertEqual(json.loads(f.readline())["meta"]["outcome"], "fixed")

    def test_a_journal_planted_in_the_repo_is_never_kept(self):  # T-2995 review: the model can write its repo
        with tempfile.TemporaryDirectory() as t:
            self.assertFalse(os.path.exists(self.arm(journal(), GREEN, tmp=t, plant=True)))

    def test_names_secrets_and_home_go_code_paths_stay_calls_stay_whole(self):  # T-2995 review
        big = json.dumps({"path": "a.py", "content": "x" * (traces.STR_CAP + 500)})
        call = {"id": "c2", "type": "function", "function": {"name": "write_file", "arguments": big}}
        text = ("zedx ran /home/zedx/p/a.py; key sk-ant-api03-" + "a" * 40 + "; app.get('/api/users'); "
                "#!/usr/bin/env python3")
        recs = journal()[:-2] + [{"kind": "msg", "phase": "s1", "msg": {"role": "user", "content": text}},
                                 {"kind": "msg", "phase": "s1", "msg": {"role": "assistant", "content": "y" * (traces.STR_CAP + 9),
                                                                     "tool_calls": [call]}}, journal()[-1]]
        with tempfile.TemporaryDirectory() as t, mock.patch.object(traces, "_user", return_value="zedx"):
            with open(self.arm(recs, GREEN, tmp=t)) as f:
                rows = [json.loads(x) for x in f]
        body = json.dumps(rows)
        for gone in ("zedx", "a" * 40):
            self.assertNotIn(gone, body)
        for kept in ("/api/users", "#!/usr/bin/env python3", "~/p/a.py", "<user> ran"):
            self.assertIn(kept, body)
        last = rows[-1]["msg"]
        self.assertEqual(len(last["content"]), traces.STR_CAP)
        self.assertEqual(json.loads(last["tool_calls"][0]["function"]["arguments"])["path"], "a.py")

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
            self.assertLessEqual(os.path.getsize(j), traces.CAP + 2)
            with open(j) as f:
                self.assertEqual(json.loads(f.readlines()[-1])["msg"]["role"], "assistant", "never ends mid-call")

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

    def test_export_refuses_a_journal_with_no_model_in_its_meta(self):  # T-2995 review: fail closed
        res = self.export({"s1.journal.jsonl": [r for r in self.kept() if "meta" not in r]})
        self.assertEqual((res["conversations"], res["refused"]), (0, 1))

    def test_export_refuses_a_claude_slot(self):
        res = self.export({"s1.journal.jsonl": self.kept(model="claude-haiku-4-5"),
                           "s2.journal.jsonl": self.kept(planner="sonnet-x")})
        self.assertEqual((res["conversations"], res["refused"]), (0, 2))


class TracesExport(ForemanTestCase):
    def test_a_sensitive_project_exports_no_traces(self):  # T-2995 review
        self.fm("init")
        self.fm("sensitive", "on")
        r = self.fm("exam", "models", "--traces", os.path.join(self.tmp, "out"), check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("sensitive", r.stderr)
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "out", "traces.jsonl")))


if __name__ == "__main__":
    unittest.main()
