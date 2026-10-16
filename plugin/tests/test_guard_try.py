"""T-1146: fm guard try asks the real hook decision path (task, grants, cwd) about a command and prints the verdict,
never running it."""
import json
import os
import unittest

from helpers import ForemanTestCase


class GuardTry(ForemanTestCase):
    def try_(self, *args, cwd=None):
        return self.fm("guard", "try", *args, cwd=cwd)

    def test_allow_and_never_runs(self):
        self.assertEqual(self.try_("ls").stdout.strip(), "allow")
        self.try_("touch tried-marker")
        self.assertFalse(os.path.exists(os.path.join(self.repo, "tried-marker")))

    def test_state_write_is_denied_with_category_and_message(self):
        out = self.try_(f"echo x > {self.home}/state/x.json").stdout
        self.assertTrue(out.startswith("deny "), out)
        self.assertIn("state", out.lower())

    def test_cwd_changes_the_answer_for_a_relative_path(self):
        state = os.path.join(self.home, "state")
        os.makedirs(state, exist_ok=True)
        cmd = "python3 - <<'EOF'\np='x.json'\nopen(p,'w').write('x')\nEOF"
        self.assertEqual(self.try_(cmd, "--cwd", self.repo).stdout.strip(), "allow")
        self.assertTrue(self.try_(cmd, "--cwd", state).stdout.startswith("deny "))

    def test_edit_tool_path_and_json(self):
        out = json.loads(self.fm("guard", "try", "--tool", "Edit", "--path", f"{self.home}/state/x.json", "--json").stdout)
        self.assertEqual(out["decision"], "deny")
        self.assertTrue(out["category"] and out["message"])
        ok = json.loads(self.fm("guard", "try", "--tool", "Edit", "--path", os.path.join(self.repo, "a.txt"), "--json").stdout)
        self.assertEqual(ok["decision"], "allow")


if __name__ == "__main__":
    unittest.main()
