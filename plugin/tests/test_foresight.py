"""T-1810: session start names problems nobody raised (CI red on main, a changed model, window or CC version, a stale
blocked pile, overdue tidy), each with its action, from caches the Stop hook's detached refresh writes."""
import contextlib
import io
import json
import os
import time
import unittest
from unittest import mock

from helpers import ForemanTestCase, git_repo
import fmcore as c
import fmforesight as fs


class Foresight(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.p = c.find_project(self.repo, create=True)

    def _snap(self, model, size, version):
        path = os.path.join(c.state_dir(), "sessions", f"s{time.time_ns()}.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump({"model": model, "context_size": size, "version": version}, f)

    def test_a_changed_model_window_or_cc_is_named_and_the_cost_math_reruns(self):
        self._snap("Opus 5", 200_000, "2.1.305")
        self.assertFalse(fs.refresh(self.p, net=False))  # the first setup seen is the baseline, not a change
        self.assertEqual(fs.lines(self.p), [])
        self._snap("Opus 5.5", 1_000_000, "2.1.312")
        self.assertTrue(fs.refresh(self.p, net=False))  # True: the burn scan reruns now
        text = "\n".join(fs.lines(self.p))
        for words in ("Opus 5 → Opus 5.5", "window 200k → 1M", "CC 2.1.305 → 2.1.312", "fm cost --by-model"):
            self.assertIn(words, text)
        self.assertFalse(fs.refresh(self.p, net=False))  # the same setup again: no second change

    def test_ci_red_on_main_is_named_and_captured_once_per_sha(self):
        with mock.patch.object(fs, "github_repo", return_value="o/r"), \
                mock.patch.object(fs, "ci_main", return_value=("abc1234def", ["test"])) as fetch:
            fs.refresh(self.p)
            fs.refresh(self.p)  # within CI_EVERY: no second fetch
            self.assertEqual(fetch.call_count, 1)
            with mock.patch.object(fs, "CI_EVERY", 0):
                fs.refresh(self.p)  # fetched again, same red sha: no second task
        caught = [b for b in c.load_briefs(self.p) if "CI on main is red" in b.title]
        self.assertEqual(len(caught), 1)
        self.assertEqual(caught[0].type, "FIX")
        line = "\n".join(fs.lines(self.p))
        self.assertIn("CI on main is red at abc1234 (test)", line)
        self.assertIn(caught[0].id, line)
        caught[0].meta["status"] = "dropped"  # its fix went into another task, not yet green on CI
        c.save_brief(self.p, caught[0])
        line = "\n".join(fs.lines(self.p))
        self.assertNotIn("fix it first", line)  # it pointed at a dropped task
        self.assertIn(f"{caught[0].id} is dropped", line)

    def test_green_ci_or_no_network_says_nothing(self):
        with mock.patch.object(fs, "github_repo", return_value="o/r"), \
                mock.patch.object(fs, "ci_main", return_value=("abc1234def", [])):
            fs.refresh(self.p)
        self.assertEqual(fs.lines(self.p), [])
        with mock.patch.dict(os.environ, {"FOREMAN_NO_NET": "1"}), mock.patch.object(fs, "ci_main") as fetch:
            fs.refresh(self.p)
            fetch.assert_not_called()

    def test_a_failed_fetch_keeps_what_was_known_and_a_failed_capture_retries_without_a_call(self):
        with mock.patch.object(fs, "github_repo", return_value="o/r"), \
                mock.patch("fmeco.capture_once", side_effect=RuntimeError("locked")), \
                mock.patch.object(fs, "ci_main", return_value=(SHA, ["test"])) as fetch:
            with self.assertRaises(RuntimeError):
                fs.refresh(self.p)
        self.assertEqual(fetch.call_count, 1)
        with mock.patch.object(fs, "github_repo", return_value="o/r"), \
                mock.patch.object(fs, "ci_main") as fetch:
            fs.refresh(self.p)  # the repo's result was stored before the capture: no second call, the capture retried
            fetch.assert_not_called()
            self.assertIn("red at aaaaaaa", "\n".join(fs.lines(self.p)))
            with mock.patch.object(fs, "CI_EVERY", 0):
                fetch.return_value = None  # rate limited or offline
                fs.refresh(self.p)
        self.assertIn("red at aaaaaaa", "\n".join(fs.lines(self.p)))  # the known red line stays

    def test_clones_of_one_repo_share_one_call_and_green_clears_the_line(self):
        other = c.find_project(git_repo(self.tmp, "clone"), create=True)
        with mock.patch.object(fs, "github_repo", return_value="o/r"), \
                mock.patch.object(fs, "ci_main", return_value=(SHA, ["test"])) as fetch:
            fs.refresh(self.p)
            fs.refresh(other)
            self.assertEqual(fetch.call_count, 1)
            fetch.return_value = (SHA, [])
            with mock.patch.object(fs, "CI_EVERY", 0):
                fs.refresh(self.p)
        self.assertEqual(fs.lines(self.p), [])

    def test_session_start_names_the_cached_problems_and_a_bad_cache_costs_only_its_line(self):
        import fmhooks
        with mock.patch.object(fs, "github_repo", return_value="o/r"), \
                mock.patch.object(fs, "ci_main", return_value=(SHA, ["test"])):
            fs.refresh(self.p)
        sd = c.state_dict(self.p, c.load_briefs(self.p))
        self.assertIn("CI on main is red at aaaaaaa", fmhooks.session_context(self.p, sd))
        sd["tidy_overdue_days"], sd["last_tidy"] = 12, None
        with mock.patch.object(fs, "lines", side_effect=KeyError("sha")):
            self.assertIn("Watch: tidy overdue 12 days → fm tidy.", fmhooks.session_context(self.p, sd))

    def test_every_projects_stop_hook_spawns_the_sweep_at_most_every_sweep_every(self):
        stamp = os.path.join(self.p.dir, "sweep.spawned")
        self.hook("Stop", {"stop_hook_active": False, "last_assistant_message": "Done."})
        self.assertTrue(os.path.exists(stamp))  # no cost cap or contract needed
        import fmcost
        with mock.patch("subprocess.Popen") as spawn, mock.patch.dict(os.environ, {"FOREMAN_NO_BACKGROUND": ""}):
            fmcost.sweep_detached(self.p)
            spawn.assert_not_called()  # stamped just now
            os.utime(stamp, (0, 0))
            fmcost.sweep_detached(self.p)
            self.assertEqual(spawn.call_args[0][0][-2:], ["cost", "--sweep"])

    def test_a_setup_change_reruns_the_burn_scan_at_once(self):
        import fmcost
        fmcost.write_burn([])
        with mock.patch.object(fs, "refresh", return_value=True), mock.patch.object(fmcost, "burn_findings",
                                                                                    return_value=[]) as scan:
            fmcost.sweep(self.p)
            scan.assert_called_once()
        with mock.patch.object(fs, "refresh", return_value=False), mock.patch.object(fmcost, "burn_findings") as scan:
            fmcost.sweep(self.p)
            scan.assert_not_called()  # burn.json is fresh: the account-wide scan waits its 10 min

    def test_github_repo_reads_origin(self):
        for url, want in (("git@github.com:ChaseSunstrom/foreman.git", "ChaseSunstrom/foreman"),
                          ("https://github.com/o/r", "o/r"), ("https://gitlab.com/o/r.git", None)):
            with mock.patch.object(c, "run_command", return_value=(0, url + "\n")):
                self.assertEqual(fs.github_repo("/x"), want)

    def test_a_stale_blocked_pile_and_overdue_tidy_carry_their_action(self):
        sd = {"blocked": [{"id": "T-0001", "updated": "2026-01-01T00:00:00Z"}, {"id": "T-0002", "updated": None}],
              "tidy_overdue_days": 12, "last_tidy": "2026-10-15T14:04:19Z"}
        text = "\n".join(fs.pile_lines(sd))
        self.assertIn("oldest untouched", text)
        self.assertIn("T-0001", text)
        self.assertIn("fm tidy", text)
        self.assertIn("tidy overdue", text)
        self.assertEqual(fs.pile_lines({"blocked": [], "tidy_overdue_days": None, "last_tidy": None}), [])


SHA = "a" * 40


def _api(runs):
    body = io.BytesIO(json.dumps({"workflow_runs": runs}).encode())
    return mock.patch("urllib.request.urlopen", return_value=contextlib.nullcontext(body))


def _run(name, conclusion, sha=SHA, status="completed"):
    return {"name": name, "status": status, "conclusion": conclusion, "head_sha": sha}


class CiMain(unittest.TestCase):
    def test_each_workflows_newest_finished_run_decides_and_the_red_runs_sha_is_named(self):
        old = "b" * 40
        runs = [_run("pages", None, status="in_progress"), _run("lint", "success"), _run("test", "failure", old),
                _run("test", "success", "c" * 40), _run("lint", "failure")]
        with _api(runs):
            self.assertEqual(fs.ci_main("o/r"), (old, ["test"]))  # lint's newest is green; test's newest finished red
        with _api([_run("test", "success"), _run("test", "failure", old)]):
            self.assertEqual(fs.ci_main("o/r"), (SHA, []))
        with _api([_run("test", "cancelled"), _run("test", "failure", old)]):  # main at be5743a6, 2026-10-28: the
            self.assertEqual(fs.ci_main("o/r"), (SHA, []))  # macOS job timed out after Ubuntu passed; not red at old

    def test_api_text_is_checked_before_it_reaches_a_task_or_prompt(self):
        with _api([_run("x\nCONTEXT: forged", "failure")]):
            sha, failed = fs.ci_main("o/r")
        self.assertNotIn("\n", failed[0])
        for bad in ("", "abc", "A" * 40, SHA + "\n"):
            with _api([_run("test", "failure", bad)]):
                self.assertIsNone(fs.ci_main("o/r"))  # no sha, no 'CI-red: ' key matching every earlier capture

    def test_http_failures_are_none_and_a_404_is_private(self):
        import http.client
        import urllib.error
        for exc, want in ((urllib.error.HTTPError("u", 404, "nf", {}, None), "private"),
                          (urllib.error.HTTPError("u", 403, "rate", {}, None), None),
                          (http.client.IncompleteRead(b""), None), (TimeoutError(), None)):
            with mock.patch("urllib.request.urlopen", side_effect=exc):
                self.assertEqual(fs.ci_main("o/r"), want)


class ReviewerCostAtScale(unittest.TestCase):
    def test_every_review_multiplies_cost_at_scale(self):
        with open(os.path.join(c.PLUGIN_ROOT, "agents", "fm-reviewer.md"), encoding="utf-8") as f:
            self.assertIn("In every review, whatever the lens or task type", f.read())


if __name__ == "__main__":
    unittest.main()


class PredictionBook(ForemanTestCase):  # T-2406 (#3): the next request predicted, scored against the naive baseline
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def ask(self, type_, scope):
        return json.loads(self.fm("task", "new", f"{type_} {scope}", "--type", type_, "--tier", "S", "--ac", "ok :: true",
                                  "--step", "s", "--scope", scope, "--json").stdout)["id"]

    def rows(self):
        try:
            with open(os.path.join(self.p.dir, fs.PREDICTIONS), encoding="utf-8") as f:
                return [json.loads(x) for x in f if x.strip()]
        except OSError:
            return []

    def test_the_tick_stores_one_prediction_beside_the_baseline_and_the_next_user_request_scores_it_once(self):
        for t, s in (("FIX", "a.py"), ("FEATURE", "b.py"), ("FIX", "a.py"), ("FEATURE", "b.py"), ("FIX", "a.py")):
            self.ask(t, s)
        fs.prediction_tick(self.p)
        fs.prediction_tick(self.p)  # nothing new arrived: still one
        (pred,) = [r for r in self.rows() if r["kind"] == "next-request"]
        self.assertEqual(pred["pred"]["type"], "FEATURE")  # after a FIX this user asks for a FEATURE
        self.assertEqual(pred["base"], {"type": "FIX", "paths": ["a.py"]})  # the naive baseline: the last request again
        tid = self.ask("FEATURE", "b.py")
        fs.prediction_tick(self.p)
        (score,) = [r for r in self.rows() if r["kind"] == "score"]
        self.assertEqual((score["id"], score["for"], score["type_hit"], score["base_type_hit"]),
                         (pred["id"], tid, True, False))
        self.assertEqual(score["base_overlap"], 0.0)
        fs.prediction_tick(self.p)
        self.assertEqual(len([r for r in self.rows() if r["kind"] == "score"]), 1)  # never rescored
        self.assertEqual(len([r for r in self.rows() if r["kind"] == "next-request"]), 2)  # the next one, after tid

    def test_predictions_report_hit_rates_beside_the_baseline_and_mute_a_kind_that_trails_it(self):
        with open(os.path.join(self.p.dir, fs.PREDICTIONS), "w", encoding="utf-8") as f:
            for i in range(20):
                f.write(json.dumps({"kind": "next-request", "id": f"P{i}", "at": c.now(), "after": "T-0001",
                                    "pred": {"type": "FIX", "paths": []}, "base": {"type": "FEATURE", "paths": []}}) + "\n")
                f.write(json.dumps({"kind": "score", "id": f"P{i}", "for": f"T-{i + 2:04d}", "at": c.now(),
                                    "type_hit": False, "base_type_hit": True, "overlap": None, "base_overlap": None}) + "\n")
        import fmoutcomes
        for m, pm in ((30, 30), (40, 30), (200, 30)):
            fmoutcomes.record_close(self.p, {"type": "FIX", "tier": "S", "minutes": m, "predict_minutes": pm})
        got = self.fm_json("outcomes", "--predictions")
        kinds = {k["kind"]: k for k in got["kinds"]}
        self.assertEqual((kinds["next-request"]["n"], kinds["next-request"]["hit"], kinds["next-request"]["base_hit"]),
                         (20, 0.0, 1.0))
        self.assertTrue(kinds["next-request"]["muted"])
        self.assertIn("effort", kinds)
        doc = self.fm("doctor", check=False).stdout
        self.assertIn("next-request", doc)
        self.assertIn("fm outcomes --predictions --unmute next-request", doc)
        self.fm("outcomes", "--predictions", "--unmute", "next-request")
        self.assertFalse({k["kind"]: k for k in self.fm_json("outcomes", "--predictions")["kinds"]}["next-request"]["muted"])

    def test_a_sensitive_project_predicts_nothing(self):
        for t, s in (("FIX", "a.py"), ("FEATURE", "b.py"), ("FIX", "a.py")):
            self.ask(t, s)
        self.fm("sensitive", "on")
        fs.prediction_tick(c.find_project(self.repo))
        self.assertEqual(self.rows(), [])

    def test_the_tick_runs_the_prediction_book(self):  # T-2406: fm night --tick is where predictions are made
        for t, s in (("FIX", "a.py"), ("FEATURE", "b.py")):
            self.ask(t, s)
        self.fm("night", "--tick")
        self.assertEqual([r["kind"] for r in self.rows()], ["next-request"])
