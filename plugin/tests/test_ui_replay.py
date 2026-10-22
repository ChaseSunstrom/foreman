"""T-1534: the foreman-ui pane drawn from a recorded fixture with no live session, and two runs of one fixture
byte-identical. Tests never reach the real claude (T-0283), so the drawing itself is the mod's own test,
mods/foreman-ui/tests/replay.test.tsx, run by `claude plugin test mods/foreman-ui` (a gate) and, two processes and an
environment matrix apart, by mods/foreman-ui/tools/replay.py twin; this checks the tool, the fixture and the wiring."""
import base64
import importlib.util
import json
import os
import re
import struct
import tempfile
import unittest

MOD = os.path.join(os.path.dirname(__file__), "..", "..", "mods", "foreman-ui")
FIXTURE = os.path.join(MOD, "tests", "fixtures", "pane-busy.ts")


def load():
    spec = importlib.util.spec_from_file_location("replay_t1534", os.path.join(MOD, "tools", "replay.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read(*parts):
    with open(os.path.join(MOD, *parts), encoding="utf-8") as f:
        return f.read()


def text(s):
    return {"type": "Text", "props": {}, "children": [s]}


class Layout(unittest.TestCase):
    """The drawn tree as plain text."""

    def test_columns_stack_rows_sit_side_by_side_and_rasters_draw_their_cells(self):
        cells = base64.b64encode(b"".join(struct.pack("<III", ord(c), 0, 0) for c in "━━─")).decode()
        tree = {"type": "Box", "props": {"flexDirection": "column", "paddingX": 1}, "children": [
            {"type": "Box", "props": {"flexDirection": "row", "gap": 1}, "children": [
                text("FIX"), {"type": "Text", "props": {}, "children": [text("T-0007"), " Login"]}]},
            {"type": "Box", "props": {"flexDirection": "row"}, "children": [
                {"type": "Box", "props": {"flexDirection": "column"}, "children": [text("a"), text("b")]},
                {"type": "Raster", "props": {"columns": 3, "rows": 1, "cells": cells}}]},
            {"type": "Button", "props": {"label": "next"}},
        ]}
        self.assertEqual(load().text(tree, 12, 5), " FIX T-0007\n a━━─\n b\n next\n\n", "five rows, each ending in a newline")

    def test_a_line_wider_than_the_pane_is_cut_and_a_fixed_height_clips(self):
        tree = {"type": "Box", "props": {"flexDirection": "column", "height": 1}, "children": [
            text("界" * 10), text("hidden")]}
        self.assertEqual(load().text(tree, 5, 2), "界界\n\n")

    def test_odd_cells_and_nodes_draw_as_blanks_not_errors(self):
        cells = base64.b64encode(struct.pack("<III", 0xD800, 0, 0) + struct.pack("<III", 0, 0, 0) + b"\x01").decode()
        tree = {"type": "Box", "props": {}, "children": [
            {"type": "Raster", "props": {"columns": 2, "cells": cells}}, None, 7, {"type": "Engine", "children": ["x"]}]}
        self.assertEqual(load().text(tree, 10, 3), "\n7\nx\n")


class Tool(unittest.TestCase):
    def test_the_view_reaches_the_kit_as_data_never_as_code(self):
        # a title can hold anything: quotes, a template literal, a closing tag, a __proto__ key
        view = {"title": "\"'`${process.exit(1)}`</x>  }, print: false, x: {", "__proto__": {"polluted": True}}
        src = load().options(view, 80, 40)
        m = re.fullmatch(r'export default \{ view: JSON\.parse\(("(?:[^"\\]|\\.)*")\), columns: 80, rows: 40, '
                         r'print: true \}\n', src)
        self.assertIsNotNone(m, src)
        self.assertEqual(json.loads(json.loads(m.group(1))), view)

    def test_twin_runs_diff_on_the_text_else_on_the_tree(self):
        tool = load()
        same = ("run 1", '{"c":"#fff"}', "a\n")
        self.assertEqual(tool.diff([same, ("run 2", *same[1:])]), [])
        moved = tool.diff([same, ("run 2", '{"c":"#fff"}x', "b\n")])
        self.assertIn("-a\n", moved)
        self.assertIn("+b\n", moved)
        tinted = "".join(tool.diff([same, ("TZ=x", '{"c":"#000"}', "a\n")]))  # same text, another colour
        self.assertIn('+ "c": "#000"', tinted)
        self.assertIn("+++ TZ=x", tinted)

    def test_the_copy_holds_the_replay_test_alone_with_its_own_options(self):
        tool = load()
        with tempfile.TemporaryDirectory() as tmp:
            mod = tool.stage({"v": 1, "project": "p"}, 100, 30, tmp)
            tests = sorted(n for _, _, files in os.walk(mod) for n in files if re.search(r"\.test\.tsx?$", n))
            self.assertEqual(tests, ["replay.test.tsx"], "the mod's other tests stay behind")
            self.assertFalse(os.path.exists(os.path.join(mod, "tools")))
            self.assertTrue(os.path.isfile(os.path.join(mod, ".claude-plugin", "plugin.json")))
            self.assertTrue(os.path.isfile(os.path.join(mod, "hooks", "register.tsx")))
            with open(os.path.join(mod, "tests", "fixtures", "replay.ts"), encoding="utf-8") as f:
                self.assertIn("columns: 100, rows: 30, print: true", f.read())
        self.assertIn("print: false", read("tests", "fixtures", "replay.ts"), "the mod's own run stays quiet")
        with self.assertRaises(ValueError):
            tool.stage(["not", "a", "view"], 80, 40, tempfile.gettempdir())

    def test_the_kit_test_draws_the_pane_prints_the_mark_and_compares_two_runs(self):
        src = read("tests", "replay.test.tsx")
        self.assertIn("from './fixtures/replay'", src)
        self.assertIn(f"const MARK = '{load().MARK}'", src, "the tool finds the line the test prints")
        self.assertIn("component: 'Pane'", src)
        self.assertIn("mock.clock(on)", src, "a frozen clock")
        self.assertIn("expect(drawn).toBe(runs[0]!)", src, "the second run draws the same bytes")


class Fixture(unittest.TestCase):
    def test_the_fixture_is_synthetic_data(self):
        view = load().load(FIXTURE)  # JSON after `export default`: data, no code
        self.assertEqual((view["project"], view["root"]), ("demo-1a2b3c", "/repo"))
        raw = read("tests", "fixtures", "pane-busy.ts")
        for real in (os.path.expanduser("~"), "/home/", "/Users/", "@", "http"):
            self.assertNotIn(real, raw)

    def test_a_module_reads_from_its_line_starting_export_and_one_without_is_refused(self):
        tool = load()
        with tempfile.TemporaryDirectory() as tmp:
            good, bad = os.path.join(tmp, "good.ts"), os.path.join(tmp, "bad.ts")
            with open(good, "w", encoding="utf-8") as f:
                f.write('// see the export default below\nexport default {"v": 1, "title": "x export default y"};\n')
            with open(bad, "w", encoding="utf-8") as f:
                f.write("export const x = 1\n")
            self.assertEqual(tool.load(good), {"v": 1, "title": "x export default y"})
            with self.assertRaises(ValueError):
                tool.load(bad)


if __name__ == "__main__":
    unittest.main()
