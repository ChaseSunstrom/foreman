"""T-3083: a long loop's progress file (core.progress), jeff-train's events, and live.jobs() reading both."""
import json
import os
import subprocess
import sys
import time
import unittest.mock as mock

from helpers import LIB, ForemanTestCase
from test_moons_scale import reply

from sampo import core as c
from sampo import live

FUNNEL = "python3 plugin/bin/sampo moons funnel --stage kill"
TRAIN = "python3 /x/jeff-train --profile decide"


def _file(pid):
    return os.path.join(c.state_dir(), "progress", f"{pid}.json")


class Progress(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.p = c.find_project(self.repo)
        live._CACHE.clear()
        c._PROG.clear()

    def _job(self, pid=4242, cmd=FUNNEL):
        with mock.patch.object(live, "_procs", return_value=[(pid, cmd)]):
            return live.jobs(self.p)

    def _write(self, pid, n, t, ticks=99, total=90, note="grow"):
        with mock.patch("os.getpid", return_value=pid), mock.patch.object(c, "_progress_t", return_value=t), \
                mock.patch.object(c, "_self_ticks", return_value=ticks):
            c.progress(n, total, "moons", note)

    def test_a_loop_writes_by_pid_and_jobs_reads_done_total_rate_eta(self):
        self._write(4242, 10, 100.0)
        self._write(4242, 30, 110.0)
        with mock.patch.object(live, "_ticks", return_value=99):
            j = self._job()[0]["progress"]
        self.assertEqual((j["done"], j["total"], j["unit"], j["note"]), (30, 90, "moons", "grow"))
        self.assertAlmostEqual(j["rate"], 2.0)  # 20 moons in 10 s, from the first and latest samples
        self.assertEqual(j["eta_s"], 30)

    def test_a_new_unit_or_note_starts_a_new_rate_and_a_reused_pid_inherits_nothing(self):
        self._write(4242, 10, 100.0)
        self._write(4242, 50, 110.0, note="other")  # a second loop in one process
        with mock.patch.object(live, "_ticks", return_value=99):
            self.assertIsNone(self._job()[0]["progress"]["rate"])
        c._PROG.clear()  # the process died; a new one took the pid and writes its own first sample
        self._write(4242, 5, 200.0, ticks=100)
        with mock.patch.object(live, "_ticks", return_value=100):
            self.assertIsNone(self._job()[0]["progress"]["rate"])
        with mock.patch.object(live, "_ticks", return_value=101):  # the file's start ticks differ from the process's
            self.assertIsNone(self._job()[0]["progress"])
        with mock.patch.object(live, "_ticks", return_value=None):  # can't tell: not trusted
            self.assertIsNone(self._job()[0]["progress"])

    def test_a_loop_that_ends_clears_its_file(self):
        self._write(4242, 10, 100.0)
        self.assertTrue(os.path.exists(_file(4242)))
        with mock.patch("os.getpid", return_value=4242):
            c.progress_end()
            c.progress_end()  # a second end is nothing
        self.assertFalse(os.path.exists(_file(4242)))
        self.assertFalse(c._PROG)

    def test_a_file_whose_pid_is_gone_is_ignored_and_cleaned(self):
        self._write(777, 1, 1.0, total=2)
        self.assertIsNone(self._job()[0]["progress"])  # 4242 is the only live job; 777 is not in the process list
        self.assertFalse(os.path.exists(_file(777)))

    def test_a_real_process_writes_its_file_and_is_read_with_its_real_start(self):  # no mock of the start ticks
        code = ("import sys, time; sys.path.insert(0, sys.argv[1]); from sampo import core as c; "
                "c.progress(5, 10, 'u', 'n'); time.sleep(60)")
        proc = subprocess.Popen([sys.executable, "-c", code, LIB], env={**os.environ, "FOREMAN_STATE": c.state_dir()})
        try:
            for _ in range(100):
                if os.path.exists(_file(proc.pid)):
                    break
                time.sleep(0.1)
            j = self._job(proc.pid)[0]
            self.assertEqual((j["progress"]["done"], j["progress"]["total"]), (5, 10))
            self.assertLess(abs(time.time() - live._started(proc.pid)), 60)
            self.assertEqual(j["since"], c.iso(live._started(proc.pid)))
            with open(_file(proc.pid)) as f:
                rec = json.load(f)
            rec["start"] += 1
            with open(_file(proc.pid), "w") as f:
                json.dump(rec, f)
            self.assertIsNone(self._job(proc.pid)[0]["progress"])
        finally:
            proc.kill()
            proc.wait()

    def test_a_garbled_or_hostile_file_is_nothing_not_a_crash(self):
        os.makedirs(os.path.dirname(_file(4242)), exist_ok=True)
        for text in ("{not json", '{"done": "x", "total": [1]}', '{"done": 5, "total": 0}', "[]", " " * 9000):
            with open(_file(4242), "w") as f:
                f.write(text)
            self.assertIsNone(self._job()[0]["progress"], text[:20])

    def test_a_fifo_a_symlink_and_a_unicode_digit_name_in_the_folder_are_harmless(self):
        d = os.path.dirname(_file(4242))
        os.makedirs(d, exist_ok=True)
        os.mkfifo(_file(4242))  # opening it blocking would hang the page
        os.symlink("/etc/hostname", _file(4243))
        open(os.path.join(d, "²².json"), "w").close()  # '²²'.isdigit() is True, int() raises
        self.assertIsNone(self._job()[0]["progress"])

    def _events(self, rows, name="events.jsonl"):
        ev = os.path.join(self.repo, name)
        with open(ev, "w") as f:
            f.write("\n".join(json.dumps(r) for r in rows) + "\n")
        return ev

    def _steps(self, n):
        return [{"kind": "training_step", "step": i, "loss": 2.0 - i / 100, "process_elapsed_seconds": 10.0 + 2 * i}
                for i in range(1, n + 1)]

    def test_jeff_train_events_give_step_loss_and_eta_from_its_environ(self):
        ev = self._events([{"kind": "training_started", "total_steps": 100}] + self._steps(20))
        with mock.patch.object(live, "_environ", return_value={"JEFF_EVENTS": ev}):
            j = self._job(cmd=TRAIN)[0]["progress"]
        self.assertEqual((j["done"], j["total"], j["unit"]), (20, 100, "steps"))
        self.assertIn("loss 1.8", j["note"])
        self.assertEqual(j["eta_s"], 160)  # 80 steps at 2 s

    def test_a_resumed_run_reads_the_latest_start_and_a_relative_path_the_trainers_cwd(self):
        ev = self._events([{"kind": "training_started", "total_steps": 100}] + self._steps(5)
                          + [{"kind": "training_started", "total_steps": 300}] + self._steps(7))
        with mock.patch.object(live, "_environ", return_value={"JEFF_EVENTS": "events.jsonl"}), \
                mock.patch.object(os, "readlink", return_value=self.repo):
            j = self._job(cmd=TRAIN)[0]["progress"]
        self.assertEqual((j["done"], j["total"]), (7, 300))

    def test_a_start_older_than_the_tail_is_found_at_the_files_head(self):
        ev = self._events([{"kind": "training_started", "total_steps": 100}] + self._steps(60))
        with mock.patch.object(live, "TAIL_B", 2000), mock.patch.object(live, "_environ", return_value={"JEFF_EVENTS": ev}):
            j = self._job(cmd=TRAIN)[0]["progress"]
        self.assertEqual((j["done"], j["total"]), (60, 100))

    def test_environ_is_read_only_of_a_process_this_uid_owns(self):
        with mock.patch.object(live, "_mine", return_value=False), mock.patch("builtins.open", side_effect=AssertionError):
            self.assertEqual(live._environ(4242), {})

    def test_an_events_path_that_is_missing_a_symlink_or_another_users_is_ignored(self):
        with mock.patch.object(live, "_environ", return_value={"JEFF_EVENTS": "/nonexistent/events.jsonl"}):
            self.assertIsNone(self._job(cmd=TRAIN)[0]["progress"])
        ev = self._events([{"kind": "training_started", "total_steps": 9}] + self._steps(2))
        link = os.path.join(self.repo, "link.jsonl")
        os.symlink(ev, link)
        with mock.patch.object(live, "_environ", return_value={"JEFF_EVENTS": link}):
            self.assertIsNone(self._job(cmd=TRAIN)[0]["progress"])
        with mock.patch.object(live, "_environ", return_value={"JEFF_EVENTS": ev}), \
                mock.patch.object(os, "getuid", return_value=os.stat(ev).st_uid + 1):
            self.assertIsNone(self._job(cmd=TRAIN)[0]["progress"])

    def test_moon_grow_writes_progress_while_it_runs_and_clears_it_at_the_end(self):
        from sampo import moonscale as ms
        self.fm("init")
        self.p = c.find_project(self.repo)
        seen = []

        def fake(p, system, prompt, cheap=True, paid=0):
            seen.append(os.path.exists(_file(os.getpid())))
            return reply(4), "jarvis"
        with mock.patch.object(ms, "_ask", side_effect=fake):
            ms.grow(self.p, 8, batch=4)
        self.assertEqual(seen, [False, True])  # the second call follows the first batch's progress
        self.assertFalse(os.path.exists(_file(os.getpid())))

    def test_moon_funnel_reports_rows_waiting_in_the_stage_and_clears_at_the_end(self):
        from sampo import moonscale as ms
        self.fm("init")
        self.p = c.find_project(self.repo)
        seen = []
        with mock.patch.dict(ms.__dict__, {"_exact": lambda *a: seen.append(json.load(open(_file(os.getpid())))) }):
            ms.funnel(self.p, stage="exact")
        self.assertEqual((seen[0]["unit"], seen[0]["note"], seen[0]["done"]), ("rows", "exact", 0))
        self.assertFalse(os.path.exists(_file(os.getpid())))
