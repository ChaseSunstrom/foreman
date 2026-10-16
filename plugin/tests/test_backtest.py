"""T-1058: fm backtest counts where a changed rule, known fix or card would have fired on recorded sessions."""
import json
import os
import unittest

from helpers import ForemanTestCase


class Backtest(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.uhome = os.path.join(self.tmp, "uhome")
        self.log = os.path.join(self.uhome, ".claude", "projects", "-work-app", "s1.jsonl")
        os.makedirs(os.path.dirname(self.log))

    def write(self, calls):
        """calls: (command, error text or None); each becomes a tool_use plus its tool_result."""
        with open(self.log, "w") as f:
            for i, (cmd, err) in enumerate(calls):
                f.write(json.dumps({"type": "assistant", "message": {"content": [
                    {"type": "tool_use", "id": f"t{i}", "name": "Bash", "input": {"command": cmd}}]}}) + "\n")
                f.write(json.dumps({"type": "user", "message": {"content": [
                    {"type": "tool_result", "tool_use_id": f"t{i}", "is_error": err is not None,
                     "content": err or "ok"}]}}) + "\n")

    def bt(self, *args, check=True):
        return self.fm("backtest", *args, env={"HOME": self.uhome}, check=check)

    def test_rule_counts_fires_and_errors(self):
        self.write([("npm install left-pad", "npm ERR! 404"), ("npm install lodash", None), ("ls", None)])
        r = self.bt("--rule", "npm install")
        self.assertIn("would have fired 2 times in 1 session(s)", r.stdout)
        self.assertIn("1 followed by an error", r.stdout)

    def test_json_keys_for_card(self):
        self.write([("cat react-hook-form.md", None), ("ls", None)])
        d = json.loads(self.bt("--card", "react-hook-form", "--json").stdout)
        self.assertEqual((d["fires"], d["sessions"], d["errored"]), (1, 1, 0))

    def test_fix_matches_error_text(self):
        self.write([("cargo build", "cargo: command not found"), ("ls", None)])
        d = json.loads(self.bt("--fix", "cargo: command not found", "--json").stdout)
        self.assertEqual((d["fires"], d["errored"]), (1, 1))

    def test_empty_corpus_and_bad_input(self):
        self.assertIn("no recent session", self.bt("--rule", "x").stdout)
        self.write([("ls", None)])
        self.assertNotEqual(self.bt("--rule", "(", check=False).returncode, 0)
        self.assertNotEqual(self.bt("--card", "no-such-card-zz", check=False).returncode, 0)


if __name__ == "__main__":
    unittest.main()
