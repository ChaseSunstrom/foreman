"""T-2553: a top-level name a module defines twice is a silent replacement: the later def wins, and the earlier one's
callers get it. Twice in one session a new helper was shadowed this way (_grounded in fmgenesis, _TID in fmrecall).
T-2630: the same finding, at the edit that adds the second definition, as a PostToolUse note (redefinitions is in fmcore)."""
import glob
import os
import unittest

from test_hooks import HookCase

from fmcore import redefinitions

LIB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib")


class Redefinitions(unittest.TestCase):
    def test_a_shadowed_helper_is_caught_and_an_in_place_rebinding_is_not(self):
        shadowed = "import re\n\ndef _grounded(a):\n    return a\n\n_TID = re.compile('x')\n\ndef _grounded(b):\n    return b\n"
        self.assertEqual(redefinitions(shadowed), [(8, "_grounded", 3)])
        self.assertEqual(redefinitions("A = 1\nA = 2\n"), [(2, "A", 1)])
        self.assertEqual(redefinitions("DEFS = {'py': ['x']}\nDEFS = {k: v for k, v in DEFS.items()}\n"), [])

    def test_no_plugin_lib_module_redefines_a_top_level_name(self):
        bad = []
        for path in sorted(glob.glob(os.path.join(LIB, "*.py"))):
            with open(path, encoding="utf-8") as f:
                bad += [f"{os.path.basename(path)}:{line} {name} (first at {first})"
                        for line, name, first in redefinitions(f.read())]
        self.assertEqual(bad, [], "a later definition silently replaces an earlier one: rename one of them")


class RedefinitionNote(HookCase):
    """T-2630: an edit that adds a top-level name its module already has is told so at once, once per name."""
    def setUp(self):
        super().setUp()
        self.fm("init")

    def edit(self, rel, file_text, new, tool="Edit", sid="s1"):
        path = os.path.join(self.repo, rel)
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_text)
        ti = {"file_path": path, "new_string": new} if tool == "Edit" else {"file_path": path, "content": new}
        return self.ctx_of(self.hook("PostToolUseValidate", {"tool_name": tool, "tool_input": ti,
                                                              "tool_response": {}, "session_id": sid}))

    def test_a_second_top_level_def_gets_a_note_with_both_lines_once(self):
        src = "def _name(a):\n    return a\n\n\ndef _name(b):\n    return b\n"
        note = self.edit("m.py", src, "def _name(b):\n    return b\n")
        self.assertIn("_name", note)
        self.assertIn("line 5", note)
        self.assertIn("line 1", note)
        self.assertEqual(self.edit("m.py", src, "def _name(b):\n    return b\n"), "", "once per name per session")
        self.assertIn("_name", self.edit("m.py", src, "def _name(b):\n    return b\n", sid="s2"))

    def test_a_rebinding_or_an_edit_that_adds_no_top_level_name_gets_none(self):
        self.assertEqual(self.edit("a.py", "X = 1\nX = f(X)\n", "X = f(X)\n"), "")
        self.assertEqual(self.edit("b.py", "def f():\n    return 1\n\n\ndef f():\n    return 2\n", "    return 2\n"), "")
        self.assertEqual(self.edit("c.py", "def f():\n    return 1\n\n\ndef g():\n    return 2\n", "def g():\n"), "")

    def test_a_write_of_a_shadowing_module_gets_the_note(self):
        self.assertIn("A", self.edit("w.py", "A = 1\nA = 2\n", "A = 1\nA = 2\n", tool="Write"))


if __name__ == "__main__":
    unittest.main()
