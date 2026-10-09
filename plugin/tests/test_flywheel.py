"""T-0712 (Frontier 12, first slice): Foreman measures its own burden on real sessions and scores a candidate guard on
the replay corpus of real commands before it ships."""
import datetime
import json
import os
import re
import shutil

from helpers import PLUGIN, ForemanTestCase

TS = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def turn(n, cmd):
    return {"type": "assistant", "sessionId": "sess-a", "timestamp": TS, "cwd": "/w",
            "message": {"id": f"m{n}", "role": "assistant", "usage": {"input_tokens": 1, "output_tokens": 1},
                        "content": [{"type": "tool_use", "id": f"t{n}", "name": "Bash", "input": {"command": cmd}}]}}


def result(n, text):
    return {"type": "user", "sessionId": "sess-a", "timestamp": TS,
            "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": f"t{n}", "content": text}]}}


class Burden(ForemanTestCase):
    def test_bookkeeping_refusals_and_injected_context_per_version(self):
        self.fm("init")
        cfg = os.path.join(self.tmp, "cfg")
        folder = os.path.join(cfg, "projects", re.sub(r"[^A-Za-z0-9]", "-", os.path.realpath(self.repo)))
        os.makedirs(folder)
        rows = [turn(1, "fm task evidence T-0001 --step 1 --run 'pytest'"), result(1, "evidence recorded"),
                turn(2, "pytest -q"), result(2, "Foreman guard: blocked core: x"),
                turn(3, "fm focus T-0001 && fm task finish T-0001 --audit self"),
                result(3, "fm: refused: T-0001 can't be marked done"),
                {"type": "attachment", "sessionId": "sess-a", "timestamp": TS,
                 "attachment": {"type": "hook_additional_context", "content": ["Foreman: " + "x" * 291]}}]
        with open(os.path.join(folder, "sess-a.jsonl"), "w") as f:
            f.write("\n".join(json.dumps(r) for r in rows) + "\n")
        self.fm("log", "session_start", json.dumps({"root": "/u/.claude/plugins/cache/foreman/foreman/1.2.21"}),
                env={"CLAUDE_CODE_SESSION_ID": "sess-a"})
        env = {"CLAUDE_CONFIG_DIR": cfg}
        out = self.fm("burden", env=env).stdout
        self.assertIn("1.2.21", out)
        data = json.loads(self.fm("burden", "--json", env=env).stdout)
        v = data["versions"]["1.2.21"]
        self.assertEqual((v["turns"], v["bookkeeping_turns"], v["guard_refusals"], v["fm_refusals"]), (3, 2, 1, 1))
        self.assertEqual(v["injected_chars"], 300)


class Candidate(ForemanTestCase):
    def test_a_candidate_guard_that_loosens_is_named_and_fails(self):
        self.fm("init")
        home = os.path.join(self.tmp, "uhome")
        logs = os.path.join(home, ".claude", "projects", "-w")
        os.makedirs(logs)
        with open(os.path.join(logs, "s.jsonl"), "w") as f:
            for n, cmd in enumerate(["ls -la", "rm -rf ~/.claude/foreman/plugin"]):
                f.write(json.dumps(dict(turn(n, cmd), cwd=self.repo)) + "\n")
        cand = os.path.join(self.tmp, "fmguard.py")
        shutil.copy(os.path.join(PLUGIN, "lib", "fmguard.py"), cand)
        with open(cand, "a") as f:
            f.write("\n\ndef check(*a, **k):  # a candidate that allows everything\n    return None\n")
        r = self.fm("replay", "--candidate", cand, env={"HOME": home}, check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("loosened", r.stdout)
        self.assertIn("rm -rf", r.stdout)
        same = self.fm("replay", "--candidate", os.path.join(PLUGIN, "lib", "fmguard.py"), env={"HOME": home})
        self.assertIn("0 loosened", same.stdout)
