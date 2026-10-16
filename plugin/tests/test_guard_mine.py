"""T-1187: fm guard mine lists real guard refusals from this project's Claude Code transcripts, each with its full
command, today's verdict and what the session did next."""
import json
import os
import re
import unittest

from helpers import ForemanTestCase

REFUSAL = ("Foreman guard: blocked state-direct: {p} is Foreman state. Change it through fm (fm task …, fm capture, "
           "fm checkpoint).")


class GuardMine(ForemanTestCase):
    def seed(self, name, calls):
        """calls: (command, result text, is_error) in order; one transcript file in this project's folder."""
        cfg = os.path.join(self.tmp, "cfg")
        folder = os.path.join(cfg, "projects", re.sub(r"[^A-Za-z0-9]", "-", os.path.realpath(self.repo)))
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, name + ".jsonl"), "w") as f:
            for i, (cmd, result, err) in enumerate(calls):
                f.write(json.dumps({"type": "assistant", "cwd": self.repo, "message": {"content": [
                    {"type": "tool_use", "id": f"t{i}", "name": "Bash", "input": {"command": cmd}}]}}) + "\n")
                f.write(json.dumps({"type": "user", "message": {"content": [
                    {"type": "tool_result", "tool_use_id": f"t{i}", "content": result, "is_error": err}]}}) + "\n")
        return {"CLAUDE_CONFIG_DIR": cfg}

    def test_each_refusal_is_labelled_from_what_the_session_did_next(self):
        bad = f"echo x > {self.home}/state/a.json"
        msg = REFUSAL.format(p=f"{self.home}/state/a.json")
        env = self.seed("retry", [(bad, msg, True), (bad, msg, True)])
        self.seed("rewrite", [("rm -f " + self.home + "/state/b.json", msg, True), ("fm task list", "ok", False)])
        self.seed("abandon", [("echo c > " + self.home + "/state/c.json", msg, True)])
        # outputs that merely quote the refusal: a cat of a file, and an error that doesn't open with the prefix
        self.seed("quote", [("cat notes.txt", "see: " + msg, False), ("cat gone.txt", "cat: gone.txt: " + msg, True),
                            ("cat ok.txt", msg, False)])
        out = json.loads(self.fm("guard", "mine", "--json", env=env).stdout)
        got = {r["command"]: r for r in out["refusals"]}
        self.assertEqual(len(out["refusals"]), 4, out)  # the retry's two are both listed
        self.assertEqual([r["label"] for r in out["refusals"] if r["command"] == bad], ["retried-unchanged", "abandoned"])
        self.assertEqual(got["rm -f " + self.home + "/state/b.json"]["label"], "rewritten-passed")
        c = got["echo c > " + self.home + "/state/c.json"]
        self.assertEqual(c["label"], "abandoned")
        self.assertEqual(c["rule"].split(":")[0], "state-direct")
        self.assertEqual(c["today"], "state-direct")  # the guard still blocks it, no grants
        self.assertNotIn("cat notes.txt", got)
        self.assertEqual(out["rules"]["state-direct"], 4)

    def test_text_output_and_empty(self):
        env = self.seed("none", [("ls", "a b", False)])
        self.assertIn("No guard refusals", self.fm("guard", "mine", env=env).stdout)
        msg = REFUSAL.format(p="/x")
        env = self.seed("one", [("echo x > " + self.home + "/state/a.json", msg, True)])
        self.assertIn("abandoned", self.fm("guard", "mine", "--days", "3", env=env).stdout)


if __name__ == "__main__":
    unittest.main()
