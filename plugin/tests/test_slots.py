"""T-3252: every run.py on the machine shares one pool of CPU slots, so four runners don't put 64 workers on 16 CPUs."""
import os
import subprocess
import sys
import threading
import time
import unittest
from unittest import mock

from helpers import ForemanTestCase

import run


class Slots(ForemanTestCase):
    def setUp(self):
        super().setUp()
        env = {"XDG_RUNTIME_DIR": self.tmp, "SAMPO_SLOTS": "1"}
        self.patch = mock.patch.dict(os.environ, env)
        self.patch.start()
        os.environ.pop(run.SLOT_ENV, None)
        self.addCleanup(self.patch.stop)

    def test_a_second_holder_waits_for_the_first(self):
        held, order = threading.Event(), []

        def first():
            with run.cpu_slot() as s:
                order.append(("first", s))
                held.set()
                time.sleep(0.4)
            order.append(("first done", None))

        t = threading.Thread(target=first)
        t.start()
        held.wait(5)
        start = time.monotonic()
        with run.cpu_slot() as s:
            waited = time.monotonic() - start
            order.append(("second", s))
        t.join()
        self.assertGreaterEqual(waited, 0.25)
        self.assertEqual([o[0] for o in order], ["first", "first done", "second"])
        self.assertEqual(order[0][1], 0)

    def test_a_dead_holder_frees_its_slot(self):
        code = ("import sys, time; sys.path.insert(0, %r); import run\n"
                "with run.cpu_slot():\n    print('held', flush=True); time.sleep(60)\n") % run.HERE
        p = subprocess.Popen([sys.executable, "-c", code], stdout=subprocess.PIPE, text=True, env=dict(os.environ))
        self.assertEqual(p.stdout.readline().strip(), "held")
        p.kill()
        p.wait()
        start = time.monotonic()
        with run.cpu_slot(wait=5) as s:
            self.assertEqual(s, 0)
        self.assertLess(time.monotonic() - start, 2)

    def test_a_runner_inside_a_slot_never_waits_on_its_parent(self):
        with run.cpu_slot() as outer:
            with mock.patch.dict(os.environ, {run.SLOT_ENV: str(outer)}):
                start = time.monotonic()
                with run.cpu_slot(wait=30) as inner:
                    self.assertIsNone(inner)
                self.assertLess(time.monotonic() - start, 1)

    def test_off_and_a_wait_that_runs_out_run_without_a_slot(self):
        with mock.patch.dict(os.environ, {"SAMPO_SLOTS": "0"}):
            with run.cpu_slot() as s:
                self.assertIsNone(s)
        with run.cpu_slot():
            start = time.monotonic()
            with run.cpu_slot(wait=0.3) as s:
                self.assertIsNone(s)  # never hangs: it runs anyway once the wait is up
            self.assertLess(time.monotonic() - start, 2)

    def test_an_unusable_slot_folder_runs_without_a_slot(self):
        # review (T-3297): a squatted or unwritable folder must not abort the run
        blocker = os.path.join(self.tmp, f"sampo-slots-{os.getuid()}")
        with open(blocker, "w") as f:
            f.write("not a folder")
        with run.cpu_slot(wait=1) as s:
            self.assertIsNone(s)
        os.remove(blocker)
        os.makedirs(blocker)
        os.chmod(blocker, 0o777)  # a folder others may write is someone else's to plant files in
        with run.cpu_slot(wait=1) as s:
            self.assertIsNone(s)

    def test_the_pool_is_the_cpus_this_cgroup_may_use(self):
        os.environ.pop("SAMPO_SLOTS")
        root = os.path.join(self.tmp, "cg")
        os.makedirs(os.path.join(root, "a", "b"))
        for rel, quota in (("a", "800000 100000"), ("a/b", "max 100000")):
            with open(os.path.join(root, rel, "cpu.max"), "w") as f:
                f.write(quota + "\n")
        with mock.patch.object(run, "_cgroup_dir", lambda: os.path.join(root, "a", "b")), \
                mock.patch.object(run, "CGROUP_ROOT", root), mock.patch("os.cpu_count", lambda: 16):
            self.assertEqual(run.slot_count(), 8)  # a 50% cap on 16 CPUs, set on the parent
        with mock.patch.object(run, "_cgroup_dir", lambda: None), mock.patch("os.cpu_count", lambda: 16):
            self.assertEqual(run.slot_count(), 16)

    def test_each_class_runs_in_a_slot_and_tells_its_children(self):
        seen = []
        real = subprocess.Popen

        def spy(argv, **kw):
            seen.append(kw["env"].get(run.SLOT_ENV))
            return real([sys.executable, "-c", "pass"], **{k: v for k, v in kw.items() if k != "cwd"})

        with mock.patch.object(run.subprocess, "Popen", spy):
            run.run_one("test_nothing.Nothing", [])
        self.assertEqual(seen, ["0"])


if __name__ == "__main__":
    unittest.main()
