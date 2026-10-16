"""T-1187: fm guard mine lists real guard refusals from this project's Claude Code transcripts, each with its full
command, today's verdict and what the session did next."""
import json
import os
import re
import unittest

from helpers import ForemanTestCase

# as a real transcript holds it (T-1187 review: the fixture lacked the hook-error prefix, so real refusals were missed)
REFUSAL = ("PreToolUse:Bash hook error: Foreman guard: blocked state-direct: {p} is Foreman state. Change it through "
           "fm (fm task …, fm capture, fm checkpoint).")


class GuardMine(ForemanTestCase):
    def seed(self, name, calls, at=None, junk=False, same_msg=False):
        """calls: (command, result text, is_error) in order; one transcript file in the folder Claude Code names after
        the session's cwd (`at`, default the repo root); same_msg: all calls come from one assistant message."""
        cfg = os.path.join(self.tmp, "cfg")
        at = at or self.repo
        folder = os.path.join(cfg, "projects", re.sub(r"[^A-Za-z0-9]", "-", os.path.realpath(at)))
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, name + ".jsonl"), "w") as f:
            if junk:
                f.write('{"is_error": broken "Bash"\n')
            for i, (cmd, result, err) in enumerate(calls):
                f.write(json.dumps({"type": "assistant", "cwd": at, "message": {
                    "id": "m0" if same_msg else f"m{i}", "content": [
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
        self.assertEqual(got["rm -f " + self.home + "/state/b.json"]["label"], "rewritten-not-refused")
        c = got["echo c > " + self.home + "/state/c.json"]
        self.assertEqual(c["label"], "abandoned")
        self.assertEqual(c["rule"].split(":")[0], "state-direct")
        self.assertEqual(c["today"], "state-direct")  # the guard still blocks it, no grants
        self.assertNotIn("cat notes.txt", got)
        self.assertEqual(out["rules"]["state-direct"], 4)

    def test_subdirectory_and_worktree_sessions_and_other_projects(self):
        msg = REFUSAL.format(p="/x")
        sub = os.path.join(self.repo, "sub")
        wt = os.path.join(self.repo, ".claude", "worktrees", "agent-1")
        for d in (sub, wt):
            os.makedirs(d)
        env = self.seed("a", [("echo sub", msg, True)], at=sub, junk=True)
        self.seed("b", [("echo wt", msg, True)], at=wt)
        self.seed("c", [("echo other", msg, True)], at=self.repo + "-other")  # a sibling project shares the prefix
        got = {r["command"] for r in json.loads(self.fm("guard", "mine", "--json", env=env).stdout)["refusals"]}
        self.assertEqual(got, {"echo sub", "echo wt"})

    def test_from_home_and_clamped_days(self):
        env = self.seed("a", [("ls", "x", False)])
        out = self.fm("guard", "mine", "--json", "--days", "-5", cwd=os.path.expanduser("~"), env=env)
        self.assertEqual(json.loads(out.stdout)["days"], 1)

    def test_parallel_siblings_are_not_the_next_call_and_output_is_inert(self):
        msg = REFUSAL.format(p="/x") + " " + "y" * 5000
        env = self.seed("a", [("echo \x1b]0;pwned\x07 ‮ hi", msg, True), ("echo sibling", "ok", False),
                              ("echo later", "ok", False)], same_msg=True)
        out = json.loads(self.fm("guard", "mine", "--json", env=env).stdout)["refusals"]
        self.assertEqual(out[0]["label"], "abandoned")  # siblings of one message are no reaction to it
        self.assertLessEqual(len(out[0]["message"]), 600)
        text = self.fm("guard", "mine", env=env).stdout
        self.assertNotIn("\x1b", text)
        self.assertNotIn("‮", text)

    def test_text_output_and_empty(self):
        env = self.seed("none", [("ls", "a b", False)])
        self.assertIn("No guard refusals", self.fm("guard", "mine", env=env).stdout)
        msg = REFUSAL.format(p="/x")
        env = self.seed("one", [("echo x > " + self.home + "/state/a.json", msg, True)])
        self.assertIn("abandoned", self.fm("guard", "mine", "--days", "3", env=env).stdout)


if __name__ == "__main__":
    unittest.main()
