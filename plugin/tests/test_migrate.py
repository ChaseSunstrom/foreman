"""T-2746: fm migrate moves the Foreman home and its siblings to sampo names once, leaves symlinks at the old paths,
backs up the record, writes a manifest with hashes, reruns safely, resumes a half-done move and undoes exactly."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from helpers import FM, ForemanTestCase

import fmhomemove as hm

REAL_SNAPSHOTS = os.path.expanduser("~/.claude/foreman/state/snapshots")  # read only, captured before any HOME patch
SIBLINGS = ("draft", "evolve", "lanes")


class Migrate(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.h = os.path.join(self.tmp, "h")
        self.cl = os.path.join(self.h, ".claude")
        self.old = os.path.join(self.cl, "foreman")
        self.new = os.path.join(self.cl, "sampo")
        os.makedirs(self.old)
        for s in SIBLINGS:
            d = os.path.join(self.cl, f"foreman.{s}", "sub")
            os.makedirs(d)
            with open(os.path.join(d, "f.txt"), "w") as f:
                f.write(s)
            os.symlink("sub/f.txt", os.path.join(self.cl, f"foreman.{s}", "link"))
        env = {"HOME": self.h, "FOREMAN_HOME": self.old}
        p = mock.patch.dict(os.environ, env)
        p.start()
        self.addCleanup(p.stop)
        self.slug = self._lay_record()

    def _lay_record(self):
        """The newest real upgrade snapshot when this machine has one, else a project made through fm."""
        import fmrollback
        snaps = sorted(s for s in os.listdir(REAL_SNAPSHOTS) if s.endswith(".tar.gz") and not s.startswith(fmrollback.PRE)) \
            if os.path.isdir(REAL_SNAPSHOTS) else []
        if snaps:
            import shutil
            stage = os.path.join(self.tmp, "stage")
            try:
                slugs = fmrollback._stage(os.path.join(REAL_SNAPSHOTS, snaps[-1]), stage, True)
                for s in slugs:
                    shutil.copytree(os.path.join(stage, s), os.path.join(self.old, "state", "projects", s))
                if slugs:
                    return sorted(slugs)[0]
            except Exception:  # a snapshot that won't unpack here: fall through to the synthetic record
                shutil.rmtree(os.path.join(self.old, "state"), ignore_errors=True)
        self.fm("task", "new", "t", "--type", "FIX", "--tier", "S", "--ac", "x :: true", "--step", "s",
                env={"HOME": self.h, "FOREMAN_HOME": self.old})
        return sorted(os.listdir(os.path.join(self.old, "state", "projects")))[0]

    def _checks(self):
        """fmdrill.RESTORE_CHECKS through the new path."""
        import fmdrill
        e = dict(os.environ, HOME=self.h, FOREMAN_HOME=self.new, FOREMAN_INHIBITED="1", FOREMAN_NO_BACKGROUND="1",
                 FOREMAN_NO_LINK="1")
        for label, verb in fmdrill.RESTORE_CHECKS:
            r = subprocess.run([sys.executable, FM, verb, "-p", self.slug], cwd=self.repo, env=e,
                               capture_output=True, text=True, timeout=120)
            self.assertEqual(r.returncode, 0, f"{verb}: {r.stdout}{r.stderr}")
            self.assertNotIn("Traceback", r.stderr)

    def test_moves_links_backs_up_and_the_record_reads_back(self):
        r = hm.migrate()
        self.assertEqual(r["status"], "done", r)
        for s in ("",) + tuple("." + x for x in SIBLINGS):
            o, n = os.path.join(self.cl, "foreman" + s), os.path.join(self.cl, "sampo" + s)
            self.assertTrue(os.path.isdir(n) and not os.path.islink(n))
            self.assertEqual(os.readlink(o), n)
        man = json.load(open(os.path.join(self.cl, "sampo-migrate.json")))
        self.assertEqual(man["status"], "done")
        self.assertEqual(len(man["folders"]), 4)
        self.assertTrue(all(len(f["hash"]) == 64 for f in man["folders"]))
        self.assertTrue(os.path.getsize(os.path.join(self.cl, "sampo-migrate-backup.tar.gz")) > 0)
        self._checks()

    def test_a_second_run_changes_nothing(self):
        hm.migrate()
        man = open(os.path.join(self.cl, "sampo-migrate.json")).read()
        self.assertEqual(hm.migrate()["status"], "done")
        self.assertEqual(open(os.path.join(self.cl, "sampo-migrate.json")).read(), man)

    def test_a_run_killed_after_the_move_resumes(self):
        with mock.patch.object(hm, "_link", side_effect=RuntimeError("killed")):
            with self.assertRaises(RuntimeError):
                hm.migrate()
        self.assertFalse(os.path.lexists(self.old))
        self.assertTrue(os.path.isdir(self.new))
        self.assertEqual(hm.migrate()["status"], "done")
        self.assertEqual(os.readlink(self.old), self.new)
        self._checks()

    def test_undo_restores_the_old_layout_byte_for_byte(self):
        before = {n: hm.tree_hash(os.path.join(self.cl, n)) for n in os.listdir(self.cl)}
        hm.migrate()
        r = hm.migrate(undo=True)
        self.assertEqual(r["status"], "undone", r)
        # the backup and the manifest stay: they are the record of what happened
        self.assertEqual([n for n in sorted(os.listdir(self.cl)) if not n.startswith("sampo-migrate")], sorted(before))
        for n, h in before.items():
            self.assertFalse(os.path.islink(os.path.join(self.cl, n)))
            self.assertEqual(hm.tree_hash(os.path.join(self.cl, n)), h)

    def test_undo_with_nothing_migrated_is_a_clear_refusal(self):
        with self.assertRaises(ValueError):
            hm.migrate(undo=True)

    def test_both_paths_real_is_refused_and_nothing_moves(self):
        os.makedirs(self.new)
        with self.assertRaises(ValueError):
            hm.migrate()
        self.assertTrue(os.path.isdir(self.old) and not os.path.islink(self.old))

    def test_a_dry_run_writes_nothing(self):
        r = hm.migrate(dry=True)
        self.assertEqual(r["status"], "plan")
        self.assertEqual(sorted(os.listdir(self.cl)), ["foreman", "foreman.draft", "foreman.evolve", "foreman.lanes"])

    def test_a_sensitive_project_stays_sensitive(self):
        e = {"HOME": self.h, "FOREMAN_HOME": self.old}
        self.fm("sensitive", "on", env=e)
        def sens(home):
            pd = os.path.join(home, "state", "projects")
            return sorted(s for s in os.listdir(pd) if os.path.isfile(os.path.join(pd, s, "meta.json"))
                          and json.load(open(os.path.join(pd, s, "meta.json"))).get("sensitive"))
        before = sens(self.old)
        self.assertTrue(before)  # the scratch repo's project
        hm.migrate()
        self.assertEqual(sens(self.new), before)
        self.assertEqual(sens(self.old), before)  # through the symlink


if __name__ == "__main__":
    unittest.main()
