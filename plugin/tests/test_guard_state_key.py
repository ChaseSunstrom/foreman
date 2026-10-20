import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import fmguard  # noqa: E402


class ScriptVerdictKey(unittest.TestCase):
    def test_a_moved_state_fallback_is_not_judged_by_the_old_verdict(self):
        # T-1293: the cache key had the scratch folders but not where state lives
        base = os.path.realpath(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, base)
        fh, lane, moved = (os.path.join(base, x) for x in ("fh", "lane", "moved"))
        os.makedirs(os.path.join(fh, "state"))
        os.makedirs(lane)
        os.makedirs(moved)
        with open(os.path.join(lane, "s.sh"), "w") as f:
            f.write(f"echo x > {moved}/out.json\n")
        ctx = lambda fb: fmguard.Ctx(cwd=lane, project_root=lane, home=os.path.join(base, "h"), foreman_home=fh,
                                     state_fallbacks=fb)
        run = lambda c: fmguard.check("Bash", {"command": "bash s.sh"}, c)
        first = run(ctx([]))
        second = run(ctx([moved]))
        self.assertNotEqual(bool(first), bool(second), (first, second))


if __name__ == "__main__":
    unittest.main()
