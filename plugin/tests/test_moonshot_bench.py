"""T-2721: a moonshot kill script in bench/moonshot is evidence only with its output beside it. T-2687 moved M-02's
script there without its result, which lived only in a scratch file's tail, and the gen-3 review caught it (#20)."""
import glob
import json
import os
import re
import unittest

BENCH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "bench", "moonshot")


def missing(folder):
    """The kill scripts in folder whose '<id>-result.json' is absent or carries no verdict."""
    out = []
    for script in sorted(glob.glob(os.path.join(folder, "kill_*.py"))):
        mid = re.sub(r"^kill_|\.py$", "", os.path.basename(script))
        path = os.path.join(folder, f"{mid}-result.json")
        try:
            with open(path, encoding="utf-8") as f:
                d = json.load(f)
            res = d.get("result", d) if isinstance(d, dict) else {}
            ok = res.get("verdict") in ("viable", "not-yet")
        except (OSError, ValueError, AttributeError):
            ok = False
        if not ok:
            out.append(os.path.basename(script))
    return out


class MoonshotBench(unittest.TestCase):
    def test_every_kill_script_has_its_result(self):
        self.assertEqual(missing(BENCH), [])

    def test_every_kill_script_states_its_sample_before_it_runs(self):  # T-2724: M-12's run 1 drew its classes
        import ast  # from different eras; a trial pre-registers how its arms are drawn for this reason
        for script in sorted(glob.glob(os.path.join(BENCH, "kill_*.py"))):
            with open(script, encoding="utf-8") as f:
                doc = ast.get_docstring(ast.parse(f.read())) or ""
            self.assertRegex(doc, r"(?m)^Sample\b.*:", os.path.basename(script))

    def test_a_script_without_its_result_is_named(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            for name in ("kill_m07.py", "kill_m08.py"):
                open(os.path.join(d, name), "w").close()
            with open(os.path.join(d, "m08-result.json"), "w") as f:
                json.dump({"result": {"verdict": "not-yet"}}, f)
            self.assertEqual(missing(d), ["kill_m07.py"])


if __name__ == "__main__":
    unittest.main()
