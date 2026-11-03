"""T-2667: fm burden counts Foreman context that arrives as hook_success stdout (additionalContext, systemMessage) and
splits the injected characters by the hook that sent them."""
import json
import os
import unittest

from helpers import ForemanTestCase


def hook(name, payload, content=""):
    return {"type": "attachment", "timestamp": "2099-01-01T00:00:00Z",
            "attachment": {"type": "hook_success", "hookName": name, "content": content, "stdout": payload}}


class BurdenSources(ForemanTestCase):
    def test_hook_success_stdout_is_counted_by_source(self):
        from sampo import cost
        sc = "Foreman project " + "x" * 84  # 100 chars
        rows = [hook("SessionStart:resume", json.dumps({"hookSpecificOutput": {"additionalContext": sc}})),
                hook("PreToolUse:Bash", json.dumps({"systemMessage": "fm card " + "y" * 42})),  # 50
                hook("PostToolUse:Bash", json.dumps({"hookSpecificOutput": {"updatedToolOutput": "Foreman " * 500}})),
                hook("Stop", json.dumps({"hookSpecificOutput": {"additionalContext": "not ours " * 9}})),
                hook("Stop", "not json at all"), hook("Stop", json.dumps([1])),
                {"type": "assistant", "timestamp": "2099-01-01T00:00:00Z",
                 "message": {"id": "m1", "content": [{"type": "tool_use", "name": "Bash", "input": {"command": "ls"}}]}}]
        folder = os.path.join(self.tmp, "tr")
        os.makedirs(folder)
        with open(os.path.join(folder, "s1.jsonl"), "w") as f:
            f.write("\n".join(json.dumps(r) for r in rows) + "\n")
        s = cost.burden(folder, "2000")["s1"]
        self.assertEqual(s["injected_chars"], 150)
        self.assertEqual(s["src:SessionStart"], 100)
        self.assertEqual(s["src:PreToolUse"], 50)
        self.assertEqual(cost.by_source({"s1": s}, 1)[0], ("SessionStart", 100.0))


if __name__ == "__main__":
    unittest.main()
