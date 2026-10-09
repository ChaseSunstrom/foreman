"""T-0724: outline-first reads. A first full Read of a big file gets its outline and a pointer to read a range, so the
model reads the part it needs (T-0717: 925 Read results over 5k tokens held 8.6M tokens in 30 days)."""
import json
import os
import time

from helpers import ForemanTestCase


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.big = os.path.join(self.repo, "big.py")
        with open(self.big, "w") as f:
            for i in range(80):
                f.write(f"def handler_{i}(x):\n" + "    y = x\n" * 8 + "    return y\n\n")

    def pre(self, tool_input, **extra):
        p = self.hook("PreToolUse", dict({"tool_name": "Read", "tool_input": tool_input}, **extra))
        try:
            return json.loads(p.stdout or "{}").get("hookSpecificOutput") or {}
        except ValueError:
            return {}

    def write(self, name, text):
        path = os.path.join(self.repo, name)
        with open(path, "w") as f:
            f.write(text)
        return path


class OutlineFirst(Base):
    def test_a_first_full_read_of_a_big_file_gets_its_outline(self):
        out = self.pre({"file_path": self.big})
        self.assertEqual(out.get("permissionDecision"), "deny")
        reason = out["permissionDecisionReason"]
        self.assertIn("def handler_0", reason)
        self.assertIn("def handler_79", reason)
        self.assertIn("offset", reason)
        self.assertEqual(self.pre({"file_path": self.big}), {}, "asked again: it reads whole")

    def test_a_range_a_small_file_or_another_agent_reads(self):
        self.assertEqual(self.pre({"file_path": self.big, "offset": 100, "limit": 50}), {})
        small = self.write("small.py", "x = 1\n")
        self.assertEqual(self.pre({"file_path": small}), {})
        self.assertEqual(self.pre({"file_path": os.path.join(self.repo, "nope.py")}), {})
        self.pre({"file_path": self.big})
        self.assertEqual(self.pre({"file_path": self.big}, agent_id="sub-1").get("permissionDecision"), "deny",
                         "a subagent has its own context")

    def test_markdown_and_diffs_outline_too(self):
        md = self.write("notes.md", "".join(f"## Part {i}\n" + "text\n" * 20 for i in range(40)))
        self.assertIn("Part 39", self.pre({"file_path": md}).get("permissionDecisionReason", ""))
        diff = self.write("t.diff", "".join(f"diff --git a/f{i}.py b/f{i}.py\n@@ -1 +1 @@\n" + "+x\n" * 30
                                            for i in range(25)))
        reason = self.pre({"file_path": diff}).get("permissionDecisionReason", "")
        self.assertIn("f24.py", reason)

    def test_a_compaction_resets_it(self):
        self.pre({"file_path": self.big})
        self.hook("SessionStart", {"source": "compact"})
        self.assertEqual(self.pre({"file_path": self.big}).get("permissionDecision"), "deny")


class ReadHookSafety(Base):
    def test_its_own_entry_never_blocks_and_stays_fast(self):
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hooks",
                               "hooks.json")) as f:
            entries = json.load(f)["hooks"]["PreToolUse"]
        read = [e for e in entries if "Read" in e["matcher"].split("|")]
        self.assertEqual(len(read), 1)
        self.assertNotEqual(read[0]["hooks"][0].get("onFailure"), "block", "a Read hook failure never blocks reading")
        guard = [e for e in entries if "Bash" in e["matcher"].split("|")]
        self.assertNotIn("Read", guard[0]["matcher"].split("|"))
        unreadable = self.write("locked.py", "x\n" * 900)
        os.chmod(unreadable, 0)
        try:
            self.assertEqual(self.pre({"file_path": unreadable}), {}, "can't judge it: the Read decides")
        finally:
            os.chmod(unreadable, 0o644)
        small = self.write("small.py", "x = 1\n")
        t0 = time.monotonic()
        self.pre({"file_path": small})
        self.assertLess(time.monotonic() - t0, 2.0)
