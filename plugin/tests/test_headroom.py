"""T-3316: headroom.census lists a project's caps and fixed sets; headroom.raised counts how often a cap went up."""
import glob
import os
import subprocess
import tempfile
import time
import unittest

from helpers import ForemanTestCase

from sampo import headroom as h

PY = ("import time\n"
      "BUILDERS_MAX = {n}\n"
      "TIMEOUT = {t}\n"
      "SAME: int = 7\n"
      "BIG = 50_000\n"
      "LENSES = ('intent', 'edge', 'security')\n"
      "PAIR = ('a', 'b')\n"
      "def go(xs):\n"
      "    time.sleep(TIMEOUT)\n"
      "    if xs == SAME or len(xs) >= BUILDERS_MAX:\n"
      "        return xs[:BUILDERS_MAX]\n"
      "    return xs[:5] if len(xs) < BIG else xs\n")
JS = "const MAX_ITEMS = {n};\nif (xs.length > MAX_ITEMS) {{}}\n#define LIMIT {n}\n"


def git(root, *a):
    subprocess.run(["git", "-C", root, "-c", "user.email=a@b", "-c", "user.name=a", *a], check=True,
                   capture_output=True)


class HeadroomTest(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.root = os.path.join(self.tmp, "repo")
        os.makedirs(self.root)
        git(self.root, "init", "-q")
        for n, t, j in ((6, 30, 8), (16, 60, 12), (100, 90, 20), (50, 90, 5)):
            self.write(PY.format(n=n, t=t))
            self.write(JS.format(n=j), "a.js")
            git(self.root, "add", "-A")
            git(self.root, "commit", "-qm", str(n))

    def write(self, text, name="m.py"):
        with open(os.path.join(self.root, name), "w") as f:
            f.write(text)

    def test_census_lists_caps_and_sets_not_bare_timeout(self):
        found = {e["name"]: e for e in h.census(self.root)}
        self.assertEqual(found["BUILDERS_MAX"]["value"], 50)
        self.assertEqual(found["BIG"]["value"], 50000)
        self.assertEqual(found["LENSES"]["members"], ["intent", "edge", "security"])
        for bare in ("TIMEOUT", "PAIR", "SAME"):  # sleep() use, 2 members, == use only
            self.assertNotIn(bare, found)
        self.assertEqual(found["MAX_ITEMS"]["file"], "a.js")

    def test_raised_counts_value_increases_per_file_and_name(self):
        entries = h.census(self.root)
        got = h.raised(self.root, entries)
        self.assertEqual(got[("m.py", "BUILDERS_MAX")], 2)
        self.assertEqual(got[("a.js", "MAX_ITEMS")], 2)
        # TIMEOUT also went up (30 to 60 to 90) but is no cap, so the census filter drops it
        self.assertNotIn(("m.py", "TIMEOUT"), got)
        self.assertEqual(h.raised(self.root)[("m.py", "TIMEOUT")], 2)

    def test_incremental_update_extends_cached_count(self):
        h.raised(self.root)
        self.write(PY.format(n=70, t=90))
        git(self.root, "commit", "-qam", "70")
        self.assertEqual(h.raised(self.root)[("m.py", "BUILDERS_MAX")], 3)

    def test_git_failure_is_an_error_not_empty(self):
        with self.assertRaises(h.HeadroomError):
            h.census(os.path.join(self.tmp, "no-such-repo"))

    def test_no_hook_module_imports_headroom(self):
        lib = os.path.join(os.path.dirname(os.path.abspath(h.__file__)), "..")
        files = glob.glob(os.path.join(lib, "sampo", "*hook*.py")) + glob.glob(os.path.join(lib, "*hook*.py"))
        files += glob.glob(os.path.join(lib, "..", "hooks", "*"))
        self.assertTrue(files)
        for f in files:
            if os.path.isfile(f):
                with open(f, encoding="utf-8", errors="replace") as fh:
                    self.assertNotIn("headroom", fh.read(), f)

    def test_warm_run_on_this_repo_under_3_cpu_seconds(self):
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        cpu = lambda: sum(os.times()[:4])  # own + child CPU seconds: wall time inflates on a loaded host
        h.raised(root, h.census(root))  # cold: several seconds, fills the cache in this test's state folder
        t = cpu()
        found = h.census(root)
        h.raised(root, found)
        self.assertLess(cpu() - t, 3)
        self.assertTrue(found)


if __name__ == "__main__":
    unittest.main()
