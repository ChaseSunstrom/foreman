"""T-1879: malformed state never tracebacks a read verb, and a mutating verb run twice changes nothing the second time."""
import hashlib
import json
import os
import re
import unittest

from helpers import ForemanTestCase

import fmcore as c

MALFORMED = {
    "T-0090-truncated.md": b"---\nid: T-0090\ntype: FIX\ntier: S\n",
    "T-0091-binary.md": b"\xff\xfe\x00---\x00\x9c garbage \x00\n",
    "T-0092-wrong-types.md": (b"---\nid: T-0092\ntype: 7\ntier: [S]\nstatus: banana\npriority: {a: 1}\nscope: x\n"
                              b"depends_on: 5\nallow: 7\ncreated: never\nupdated: 12\ngroup: [1, 2]\n---\n# Odd\n"),
    "T-0093-empty.md": b"",
    "T-0094-no-id.md": b"---\ntype: FIX\nstatus: queued\n---\n# No id\n",
    "T-0095-bad-yaml.md": b"---\nid: T-0095\n: : :\n  - [unclosed\n---\n# Bad\n",
}
READ_VERBS = [["status"], ["queue"], ["next"], ["inbox"], ["digest"], ["task", "list"], ["task", "show", "T-0001"],
              ["tidy"], ["fsck"], ["cost"], ["risk"], ["status", "--json"], ["queue", "--json"], ["inbox", "--json"],
              ["task", "show", "T-0092"], ["task", "show", "T-0090"], []]


class Robustness(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)
        self.tasks = os.path.join(self.p.dir, "tasks")
        self.fm("task", "new", "A thing", "--type", "FIX", "--tier", "S", "--ac", "ok :: true", "--step", "s", "--focus")

    def test_malformed_briefs_never_traceback_a_read_verb(self):
        for name, data in MALFORMED.items():
            with open(os.path.join(self.tasks, name), "wb") as f:
                f.write(data)
        self.no_traceback()

    def no_traceback(self):
        for verb in READ_VERBS:
            p = self.fm(*verb, check=False)
            self.assertNotIn("Traceback", p.stdout + p.stderr, f"fm {' '.join(verb)}")
        for event, payload in (("SessionStart", {"source": "startup"}), ("UserPromptSubmit", {"prompt": "fix it"}),
                               ("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": "ls"}}),
                               ("PreToolUse", {"tool_name": "Edit", "tool_input": {"file_path": "app.py"}}),
                               ("Stop", {"stop_hook_active": False})):
            p = self.hook(event, payload)
            self.assertNotIn("Traceback", p.stdout + p.stderr, event)

    def test_a_cut_off_or_binary_meta_is_named_never_a_traceback(self):
        meta = os.path.join(self.p.dir, "meta.json")
        for data in (b'{"slug": "app', b"\xff\xfe\x00\x9c\x00"):
            with open(meta, "wb") as f:
                f.write(data)
            self.no_traceback()
            self.assertIn("fm fsck", self.fm("status", check=False).stderr)

    def snapshot(self):
        """Every brief, view and meta file; when tidy last ran is a record of the run, not state it changed."""
        out = {}
        for root, _, files in os.walk(self.p.dir):
            for n in files:
                if n.endswith((".md", ".json")) and "logs" not in root:
                    with open(os.path.join(root, n), "rb") as f:
                        data = re.sub(rb'"last_tidy": "[^"]*"|Last tidy: \S+|_Generated \S+', b"", f.read())
                    out[os.path.relpath(os.path.join(root, n), self.p.dir)] = hashlib.sha1(data).hexdigest()
        return out

    def test_a_mutating_verb_run_twice_changes_nothing_the_second_time(self):
        self.fm("capture", "Spare idea")
        self.assertIn("near-duplicate", self.fm("capture", "Spare idea", check=False).stderr)  # the same text is one item
        tid = "T-0002"
        for verb in (["drive", "off"], ["sensitive", "on"], ["task", "drop", tid, "--reason", "no"],
                     ["tidy", "--apply"], ["task", "defer", "T-0001"], ["checkpoint"]):
            self.fm(*verb)  # the first run works, so an equal snapshot isn't two equal failures
            before, at = self.snapshot(), os.stat(os.path.join(self.p.dir, "STATE.md")).st_mtime_ns
            self.fm(*verb, check=False)
            after = self.snapshot()
            changed = {k for k in set(before) | set(after) if before.get(k) != after.get(k)}
            self.assertEqual(changed, set(), f"fm {' '.join(verb)} run twice")
            if verb[0] != "tidy":  # a view that differs only in its Generated time isn't rewritten
                self.assertEqual(os.stat(os.path.join(self.p.dir, "STATE.md")).st_mtime_ns, at, verb)
        self.assertIn("already deferred", self.fm("task", "defer", "T-0001").stdout)
        self.assertIn("already dropped", self.fm("task", "drop", tid, "--reason", "no").stdout)
        with open(os.path.join(self.p.dir, "STATE.md"), encoding="utf-8") as f:
            self.assertNotIn("Last tidy: never", f.read())  # the view is written after the run is recorded
        self.fm("task", "defer", "T-0001", "--reason", "a new why")  # something new is still recorded
        self.assertIn("deferred: a new why", c.find_brief(self.p, "T-0001").section("Log"))
        for _ in range(2):
            self.fm("task", "block", "T-0001", "--reason", "waits", "--until", "2099-01-01")
        log = c.find_brief(self.p, "T-0001").section("Log")
        self.assertEqual(log.count("blocked: waits (revisit 2099-01-01)"), 1, "a repeat with --until: one line")


if __name__ == "__main__":
    unittest.main()
