"""fm genesis (T-2078): the Genesis tower's home under research/genesis: gen-0 kept verbatim and read-only, tower docs
filed only in the tower's shape, and a status that shows every generation."""
import os
import stat

from helpers import ForemanTestCase, read_text

GEN0 = "super improve it\n\nMUST: full autonomy.\nNEVER: lower the guard.\n  trailing spaces kept  \n"


class Genesis(ForemanTestCase):
    def write(self, name, text):
        path = os.path.join(self.tmp, name)
        with open(path, "w") as f:
            f.write(text)
        return path

    def setUp(self):
        super().setUp()
        self.fm("init")

    def test_init_keeps_gen0_verbatim_read_only_and_once(self):
        res = self.fm_json("genesis", "init", "--file", self.write("g0.md", GEN0))
        path = os.path.join(res["dir"], "gen-0.md")
        with open(path, "rb") as f:
            self.assertEqual(f.read(), GEN0.encode())  # byte-identical: no redaction, no trailing-space trim
        self.assertFalse(os.stat(path).st_mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
        again = self.fm("genesis", "init", "--file", self.write("g1.md", "other\n"), check=False)
        self.assertNotEqual(again.returncode, 0)
        self.assertIn("already", again.stderr + again.stdout)
        with open(path, "rb") as f:
            self.assertEqual(f.read(), GEN0.encode())

    def test_put_files_tower_docs_and_refuses_anything_else(self):
        self.fm("genesis", "init", "--file", self.write("g0.md", GEN0))
        src = self.write("seed.md", "# Seed\nclose initiative first\n")
        res = self.fm_json("genesis", "put", "gen-1/seed.md", "--file", src)
        self.assertEqual(read_text(os.path.join(res["dir"], "gen-1", "seed.md")), "# Seed\nclose initiative first\n")
        for ok in ("gap-map.md", "lineage.md", "exam.jsonl", "gen-1/mission-initiative.md",
                   "gen-12/critique-self-triggering.md"):
            self.fm("genesis", "put", ok, "--file", src)
        for bad in ("gen-0.md", "../escape.md", "gen-1/../../x.md", "gen-1/notes.md", "gen-0/seed.md", "/etc/x.md",
                    "gen-1/mission-.md", "random.md"):
            p = self.fm("genesis", "put", bad, "--file", src, check=False)
            self.assertNotEqual(p.returncode, 0, bad)
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "escape.md")))

    def test_failure_paths_name_what_is_wrong(self):
        secret = "MUST: ship\npassword: hunter2hunter2\n"  # pragma: allowlist secret
        bad = self.fm("genesis", "init", "--file", self.write("s.md", secret), check=False)
        self.assertNotEqual(bad.returncode, 0)
        self.assertIn("a password or secret value", bad.stderr + bad.stdout)
        self.assertFalse(self.fm_json("genesis")["gen0"])
        res = self.fm_json("genesis", "put", "gen-1/seed.md", "--file", self.write("p.md", secret))
        self.assertEqual(res["redacted"], ["a password or secret value"])
        self.assertNotIn("hunter2", read_text(res["path"]))
        none = self.fm("genesis", "put", "gen-1/seed.md", check=False)
        self.assertNotEqual(none.returncode, 0)
        self.assertIn("--file", none.stderr + none.stdout)

    def test_status_shows_the_tower(self):
        empty = self.fm_json("genesis")
        self.assertFalse(empty["gen0"])
        self.fm("genesis", "init", "--file", self.write("g0.md", GEN0))
        src = self.write("x.md", "x\n")
        for name in ("gap-map.md", "gen-1/seed.md", "gen-1/mission-initiative.md", "gen-1/mission-genesis.md",
                     "gen-1/critique-initiative.md", "gen-2/seed.md"):
            self.fm("genesis", "put", name, "--file", src)
        self.fm("genesis", "put", "exam.jsonl", "--file", self.write("e.jsonl", '{"a":1}\n{"a":2}\n{"a":3}\n'))
        res = self.fm_json("genesis")
        self.assertTrue(res["gen0"] and res["gap_map"])
        self.assertEqual(res["exam_lines"], 3)
        self.assertEqual([g["n"] for g in res["generations"]], [1, 2])
        g1 = res["generations"][0]
        self.assertTrue(g1["seed"])
        self.assertEqual(g1["missions"], ["genesis", "initiative"])
        self.assertEqual(g1["critiques"], ["initiative"])
        text = self.fm("genesis").stdout
        for part in ("gen-0", "gap map", "gen-1", "2 missions", "1 critique", "gen-2", "exam: 3"):
            self.assertIn(part, text)
