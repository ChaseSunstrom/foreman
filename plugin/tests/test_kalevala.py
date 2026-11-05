"""Kalevala part 1 (T-3053): many Rune towers in one project. Each tower is its own home (research/genesis/towers/NAME);
the root tower behaves as before; moons, exam scenarios and the user's steers stay at the root for every tower."""
import json
import os

from helpers import CLEAN_READER, ForemanTestCase, read_text
from sampo import core as c


def setUpModule():
    os.environ["PATH"] = CLEAN_READER + os.pathsep + os.environ["PATH"]


def tearDownModule():
    os.environ["PATH"] = os.environ["PATH"].replace(CLEAN_READER + os.pathsep, "", 1)


class Kalevala(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")

    def gen0(self, name, text):
        path = os.path.join(self.tmp, name)
        with open(path, "w") as f:
            f.write(text)
        return path

    def project(self):
        return c.find_project(self.repo, create=False)

    def test_a_tower_seals_its_own_gen0_and_leaves_the_root_alone(self):
        res = self.fm_json("genesis", "--tower", "ahti", "init", "--file", self.gen0("a.md", "water tower\n"))
        self.assertTrue(res["dir"].endswith(os.path.join("research", "genesis", "towers", "ahti")), res["dir"])
        self.assertEqual(read_text(os.path.join(res["dir"], "gen-0.md")), "water tower\n")
        root = self.fm_json("genesis", "status")
        self.assertFalse(root["gen0"])  # the root has no gen-0 yet
        self.assertTrue(self.fm_json("genesis", "--tower", "ahti", "status")["gen0"])
        # the root seals a different gen-0: a tower's seal (ledger) never stands for it
        self.fm("genesis", "init", "--file", self.gen0("r.md", "root tower\n"))
        self.assertEqual(self.fm_json("genesis", "--tower", "ahti", "status")["gen0"], True)
        import hashlib
        self.assertEqual(self.fm_json("genesis", "status")["seal"], hashlib.sha256(b"root tower\n").hexdigest()[:8])
        self.assertEqual(self.fm_json("genesis", "--tower", "ahti", "status")["seal"],
                         hashlib.sha256(b"water tower\n").hexdigest()[:8])
        # a second tower init is refused on that tower only
        again = self.fm("genesis", "--tower", "ahti", "init", "--file", self.gen0("b.md", "other\n"), check=False)
        self.assertNotEqual(again.returncode, 0)
        self.fm("genesis", "--tower", "tapio", "init", "--file", self.gen0("c.md", "forest tower\n"))

    def test_a_tower_files_docs_and_steps_in_its_own_home(self):
        self.fm("genesis", "--tower", "ahti", "init", "--file", self.gen0("a.md", "water tower\n"))
        step = self.fm_json("genesis", "--tower", "ahti", "step")
        self.assertIn("seed", json.dumps(step))
        res = self.fm_json("genesis", "--tower", "ahti", "put", "gap-map.md", "--file", self.gen0("g.md", "# Gap map\n"))
        self.assertIn(os.path.join("towers", "ahti", "gap-map.md"), res["path"])
        root = os.path.join(self.project().dir, "research", "genesis")
        self.assertFalse(os.path.exists(os.path.join(root, "gap-map.md")))
        self.assertFalse(os.path.exists(os.path.join(root, "gen-0.md")))

    def test_the_shared_stores_stay_at_the_root_and_a_tower_steer_file_adds(self):
        from sampo import moonscale, rune
        p = self.project()
        rune.set_tower("ahti")
        try:
            self.assertEqual(rune.root(p), os.path.join(p.dir, "research", "genesis"))
            self.assertEqual(rune.home(p), os.path.join(rune.root(p), "towers", "ahti"))
            self.assertEqual(moonscale._dir(p), os.path.join(rune.root(p), "moons"))  # moons: shared
            from sampo import steer
            self.assertEqual(steer._path(p, "steer.jsonl"), os.path.join(rune.root(p), "steer.jsonl"))
            os.makedirs(rune.home(p))
            with open(os.path.join(rune.home(p), "steers.md"), "w") as f:
                f.write("- keep it watery\n")
            self.assertIn("keep it watery", " ".join(rune.tower_steers(p)))
        finally:
            rune.set_tower(None)
        self.assertEqual(rune.home(p), rune.root(p))
        self.assertNotIn("keep it watery", " ".join(rune.tower_steers(p)))  # the root's file isn't the tower's

    def test_the_towers_list_and_bad_names(self):
        self.fm("genesis", "--tower", "ahti", "init", "--file", self.gen0("a.md", "water tower\nmore\n"))
        self.fm("genesis", "--tower", "tapio", "init", "--file", self.gen0("c.md", "forest tower\n"))
        rows = self.fm_json("genesis", "towers")["towers"]
        by = {r["name"]: r for r in rows}
        self.assertEqual({"ahti", "tapio"}, set(by))
        self.assertEqual(by["ahti"]["aspect"], "water tower")
        self.assertEqual(by["ahti"]["generation"], 0)
        self.assertIsNone(by["ahti"]["select"])
        self.assertIsNone(by["ahti"]["drift"])
        os.makedirs(os.path.join(self.project().dir, "research", "genesis", "towers", "x-"))  # stray folders and files
        open(os.path.join(self.project().dir, "research", "genesis", "towers", "note"), "w").close()
        os.makedirs(os.path.join(self.project().dir, "research", "genesis", "towers", "root"))
        self.assertEqual({"ahti", "tapio"}, {r["name"] for r in self.fm_json("genesis", "towers")["towers"]})

    def test_a_bad_tower_name_is_refused_and_makes_no_folder(self):
        for bad in ("../x", "Root", "a/b", "root", "", "-x", "x-", "x" * 40):
            r = self.fm("genesis", "--tower", bad, "init", "--file", self.gen0("a.md", "x\n"), check=False)
            self.assertNotEqual(r.returncode, 0, bad)
        self.assertFalse(os.path.exists(os.path.join(self.project().dir, "research", "genesis", "towers")))

    def test_events_are_tagged_and_towers_shows_their_verdicts(self):
        from sampo import rune
        p = self.project()
        rune.set_tower("ahti")
        try:
            os.makedirs(os.path.join(rune.home(p), "gen-2"))
            rune._log(p, "genesis_select", data={"gen": 2, "verdict": "kept"})
            rune._log(p, "genesis_drift", data={"gen": 2, "verdict": "clean"})
        finally:
            rune.set_tower(None)
        c.log_event(p, "genesis_select", data={"gen": 1, "verdict": "reverted"})
        evs = [e for e in c.ledger_events(p, kinds=["genesis_select", "genesis_drift"])]
        self.assertEqual([(e["event"], (e["data"]).get("tower")) for e in evs],
                         [("genesis_select", "ahti"), ("genesis_drift", "ahti"), ("genesis_select", None)])
        self.assertEqual(rune._events(p, ["genesis_select"])[0]["data"]["verdict"], "reverted")  # root sees only its own
        os.makedirs(os.path.join(rune.root(p), "towers", "ahti"), exist_ok=True)
        got = {r["name"]: r for r in rune.towers(p)}["ahti"]
        self.assertEqual((got["generation"], got["select"], got["drift"]), (2, "kept", "clean"))
        self.assertIsNone(rune._TOWER)

    def test_a_towers_steers_reach_its_prompts_and_the_roots_never_do(self):
        from sampo import rune
        p = self.project()
        rune.set_tower("ahti")
        try:
            os.makedirs(rune.home(p))
            with open(os.path.join(rune.home(p), "steers.md"), "w") as f:
                f.write("- keep it watery\n")
            self.assertIn("keep it watery", rune._charter(p, "goal\nMUST: x.\n"))
            self.assertIn("keep it watery", rune._breakable(p, "goal\n"))
        finally:
            rune.set_tower(None)
        self.assertNotIn("keep it watery", rune._charter(p, "goal\nMUST: x.\n"))

    def test_publish_export_and_live_are_refused_under_a_tower(self):
        self.fm("genesis", "--tower", "ahti", "init", "--file", self.gen0("a.md", "water\n"))
        for verb, extra in (("publish", []), ("export", [os.path.join(self.tmp, "out")]), ("live", ["on"])):
            r = self.fm("genesis", "--tower", "ahti", verb, *extra, check=False)
            self.assertNotEqual(r.returncode, 0, verb)
            self.assertIn("root tower", r.stderr + r.stdout)
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "out")))

    def test_exam_lines_are_per_tower_and_the_lean_record_is_keyed_by_tower(self):
        from sampo import louhi, rune
        p = self.project()
        self.fm("genesis", "--tower", "ahti", "init", "--file", self.gen0("a.md", "water\n"))
        self.fm("genesis", "init", "--file", self.gen0("r.md", "root\n"))
        with open(os.path.join(rune.home(p), "exam.jsonl"), "w") as f:
            f.write('{"run": "r1"}\n')
        self.assertEqual(self.fm_json("genesis", "status")["exam_lines"], 1)
        self.assertEqual(self.fm_json("genesis", "--tower", "ahti", "status")["exam_lines"], 0)  # its own lines, none yet
        ov = {k: 1 for k in louhi.LEAN_METRICS}
        louhi._lean_grew(p, "r", "agent", "s1", ov)
        rune.set_tower("ahti")
        try:
            louhi._lean_grew(p, "r", "agent", "s1", ov)
        finally:
            rune.set_tower(None)
        with open(os.path.join(louhi.root(p), "lean-start.json")) as f:
            book = json.load(f)
        self.assertEqual(sorted(book), ["0", "ahti/0"])
