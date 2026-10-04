"""Crash damage in fm doctor (T-0268): zero-byte loose git objects, zero-byte briefs and unreadable state JSON are
named; fm doctor --repair quarantines the empty objects (they hold nothing) and touches nothing else."""
import json
import os

from helpers import ForemanTestCase


class _Case(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        import fmcore as c
        import fmdoctor
        self.c, self.d, self.p = c, fmdoctor, c.find_project(self.repo)
        self.obj = os.path.join(self.repo, ".git", "objects", "ab", "c" * 38)
        os.makedirs(os.path.dirname(self.obj), exist_ok=True)

    def empty_object(self, path=None):
        path = path or self.obj
        open(path, "w").close()
        os.utime(path, (1, 1))  # written long ago: a file being written now isn't damage


class Check(_Case):
    def test_a_clean_repo_passes(self):
        self.assertEqual(self.d.check_integrity([self.repo], [self.p]).status, "PASS")

    def test_an_empty_object_fails_with_its_repo(self):
        self.empty_object()
        r = self.d.check_integrity([self.repo], [self.p])
        self.assertEqual(r.status, "FAIL")
        self.assertIn("1 empty git object", r.detail)
        self.assertIn(self.repo, r.detail)
        self.assertIn("fm doctor --repair", r.detail)

    def test_in_flight_and_fresh_files_are_not_damage(self):
        tmp = os.path.join(os.path.dirname(self.obj), "tmp_obj_abc123")
        self.empty_object(tmp)  # git's own temp file, zero-byte for a moment
        open(self.obj, "w").close()  # an object being written right now
        self.assertEqual(self.d.check_integrity([self.repo], [self.p]).status, "PASS")
        self.fm("doctor", "--repair")
        self.assertTrue(os.path.exists(tmp) and os.path.exists(self.obj))

    def test_a_non_git_root_is_skipped_not_counted(self):
        r = self.d.check_integrity([self.repo, os.path.join(self.tmp, "not-a-repo")], [self.p])
        self.assertEqual((r.status, r.detail.split()[0]), ("PASS", "1"))

    def test_truncated_state_fails(self):
        tid = json.loads(self.fm("capture", "a thing", "--json").stdout)["id"]
        brief = self.c.find_brief(self.p, tid).path
        open(brief, "w").close()
        with open(os.path.join(self.p.dir, "hints.json"), "w") as f:
            f.write('{"ignored": ')
        r = self.d.check_integrity([self.repo], [self.p])
        self.assertEqual(r.status, "FAIL")
        self.assertIn(os.path.basename(brief), r.detail)
        self.assertIn("hints.json", r.detail)


class Repair(_Case):
    def test_repair_quarantines_empty_objects_only(self):
        self.empty_object()
        good = os.path.join(self.repo, ".git", "objects", "ab", "d" * 38)
        with open(good, "wb") as f:
            f.write(b"x")
        out = self.fm("doctor", "--repair").stdout
        self.assertIn("1", out)
        self.assertFalse(os.path.exists(self.obj))
        self.assertTrue(os.path.exists(good))
        moved = [os.path.join(d, f) for d, _, fs in os.walk(os.path.join(self.c.state_dir(), "quarantine")) for f in fs]
        self.assertTrue(any(m.endswith("ab" + "c" * 38) for m in moved), moved)
        self.assertEqual(self.d.check_integrity([self.repo], [self.p]).status, "PASS")

    def test_nothing_to_repair(self):
        self.assertIn("nothing to repair", self.fm("doctor", "--repair").stdout.lower())
