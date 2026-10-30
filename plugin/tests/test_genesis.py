"""fm genesis (T-2078): the Genesis tower's home under research/genesis: gen-0 kept verbatim and read-only, tower docs
filed only in the tower's shape, and a status that shows every generation."""
import os
import re
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
        for ok in ("gap-map.md", "lineage.md", "not-yet.md", "coverage.md", "exam.jsonl", "gen-1/mission-initiative.md",
                   "gen-12/critique-self-triggering.md"):
            self.fm("genesis", "put", ok, "--file", src)
        for bad in ("gen-0.md", "../escape.md", "gen-1/../../x.md", "gen-1/notes.md", "gen-0/seed.md", "/etc/x.md",
                    "gen-1/mission-.md", "random.md"):
            p = self.fm("genesis", "put", bad, "--file", src, check=False)
            self.assertNotEqual(p.returncode, 0, bad)
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "escape.md")))

    def test_file_dash_reads_stdin(self):
        res = self.fm_json("genesis", "init", "--file", "-", input=GEN0)
        with open(res["path"], "rb") as f:
            self.assertEqual(f.read(), GEN0.encode())
        res = self.fm_json("genesis", "put", "gen-1/seed.md", "--file", "-", input="# Seed\nfrom stdin\n")
        self.assertEqual(read_text(res["path"]), "# Seed\nfrom stdin\n")

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


GEN0_CAPS = ("go\n\n## 2. The capability spec\n\n1. **Initiative.** Find the real bugs. Then fix them.\n"
             "2. **Exhaustive thinking.** List every reading.\n\n## 3. The tower\n")
GAPS = "# Gap map\n\n## 1. Initiative\n- Exists: fm scout\n- Gaps: project scout (3) · find→prove→fix (4)\n  · value ranking (3).\n"
SEED = ("# Seed\n\n| # | Mission file | Capabilities | Gaps closed (gap-map tier) | Depends on |\n|---|---|---|---|---|\n"
        "| 1 | mission-exam.md | #13 exam, #6 | exam generator (3); scoring (3) | — |\n"
        "| 2 | mission-genesis.md | #13 | grid (3) | 1 |\n")


class GenesisExport(ForemanTestCase):
    def test_export_writes_the_tower_as_data_and_docs(self):
        import json
        self.fm("init")
        self.fm("genesis", "init", "--file", "-", input=GEN0_CAPS)
        tid = self.fm_json("task", "new", "build the exam", "--type", "FEATURE", "--tier", "S",
                           "--step", "one", "--step", "two")["id"]
        home = os.path.expanduser("~")
        for name, text in (("gap-map.md", GAPS), ("gen-1/seed.md", SEED),
                           ("gen-1/mission-exam.md", f"# Mission: exam\nTask: {tid}\nnotes in {home}/work/x.md\n")):
            self.fm("genesis", "put", name, "--file", "-", input=text)
        out = os.path.join(self.tmp, "site-genesis")
        res = self.fm_json("genesis", "export", out)
        data = json.loads(read_text(os.path.join(out, "genesis.json")))
        self.assertEqual(res["path"], os.path.join(out, "genesis.json"))
        self.assertEqual([(c["n"], c["name"]) for c in data["capabilities"]], [(1, "Initiative"), (2, "Exhaustive thinking")])
        self.assertTrue(data["capabilities"][0]["text"].startswith("Find the real bugs"))
        self.assertEqual(data["gaps"]["1"], [{"text": "project scout", "tier": 3}, {"text": "find→prove→fix", "tier": 4},
                                             {"text": "value ranking", "tier": 3}])
        g1 = data["generations"][0]
        self.assertEqual(g1["n"], 1)
        m1, m2 = g1["missions"]
        self.assertEqual((m1["name"], m1["caps"], m1["depends"], m1["written"]), ("exam", [13, 6], [], True))
        self.assertEqual(m1["gaps"], [{"text": "exam generator", "tier": 3}, {"text": "scoring", "tier": 3}])
        self.assertEqual((m2["name"], m2["depends"], m2["written"]), ("genesis", [1], False))
        task = m1["tasks"][0]
        self.assertEqual((task["id"], task["steps"], task["done"]), (tid, 2, 0))
        doc = data["docs"]["gen-1/mission-exam.md"]
        self.assertNotIn(home + "/", doc)
        self.assertIn("~/work/x.md", doc)
        self.assertEqual(read_text(os.path.join(out, "gen-1", "mission-exam.md")), doc)  # readable on GitHub too
        self.assertEqual(data["docs"]["gen-0.md"], GEN0_CAPS)
        self.assertIn("exam", data)

    def test_export_scrubs_every_field_and_skips_junk_exam_lines(self):
        import json
        self.fm("init")
        home = os.path.expanduser("~")
        self.fm("genesis", "init", "--file", "-", input=GEN0_CAPS)
        tid = self.fm_json("task", "new", f"fix {home}/proj", "--type", "FIX", "--tier", "S",
                           "--step", f"edit {home}/proj/a.py")["id"]
        self.fm("genesis", "put", "gen-1/seed.md", "--file", "-", input=SEED)
        self.fm("genesis", "put", "gen-1/mission-exam.md", "--file", "-", input=f"# Mission: exam\nTask: {tid}\n")
        self.fm("genesis", "put", "exam.jsonl", "--file", "-",
                input=json.dumps({"agent": "oracle", "run": f"{home}/runs/x"}) + "\nnull\n5\n")
        out = os.path.join(self.tmp, "site-genesis")
        self.fm_json("genesis", "export", out)
        raw = read_text(os.path.join(out, "genesis.json"))
        self.assertNotIn(home + "/", raw)
        data = json.loads(raw)
        self.assertEqual([e["run"] for e in data["exam"]], ["~/runs/x"])  # only objects; null and 5 dropped

    def test_export_without_a_tower_is_refused(self):
        self.fm("init")
        r = self.fm("genesis", "export", os.path.join(self.tmp, "out"), check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "out", "genesis.json")))

    def test_site_page_reads_the_export_and_loads_nothing_outside(self):
        import sys
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        sys.path.insert(0, os.path.join(root, "site"))
        import build
        page = os.path.join(root, "site", "genesis", "index.html")
        html = read_text(page)
        self.assertIn("genesis.json", read_text(os.path.join(root, "site", "genesis", "genesis.js")))
        self.assertIn('<script src="genesis.js"', html)
        self.assertEqual(build.outside_hosts(os.path.join(root, "site", "genesis")), [])
        landing = read_text(os.path.join(root, "site", "index.html"))
        self.assertIn("genesis/index.html", landing)  # linked from the site
        # T-2087: one site, not two: the shared stylesheet (its dark palette too) and the landing page's own nav
        self.assertIn('<link rel="stylesheet" href="../style.css">', html)
        self.assertIn("prefers-color-scheme: dark", read_text(os.path.join(root, "site", "style.css")))
        nav = lambda page: re.search(r'<nav class="nav".*?</nav>', page, re.S).group(0)
        links = lambda page: re.findall(r">([^<>]+)</a>", nav(page))
        self.assertEqual(links(html), links(landing))
        self.assertIn('href="index.html" aria-current="page">Genesis</a>', html)
        self.assertNotRegex(read_text(os.path.join(root, "site", "genesis", "genesis.css")), r"(?m)--bg:\s*#|Inter|\.sheet|^\.head\b")


LIVE_WAIT_FLOOR = 200  # seconds: well inside the 300 s window


class GenesisLive(ForemanTestCase):
    """T-2090: fm genesis live on keeps the site's Genesis page current: tower changes are pushed to main as data only."""

    def setUp(self):
        import subprocess
        super().setUp()
        self.fm("init")
        self.fm("genesis", "init", "--file", "-", input=GEN0_CAPS)
        self.fm("genesis", "put", "gap-map.md", "--file", "-", input=GAPS)
        self.origin = os.path.join(self.tmp, "origin.git")
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", self.origin], check=True)
        self.git("remote", "add", "origin", self.origin)
        self.git("push", "-q", "origin", "main")

    def git(self, *a, at=None):
        import subprocess
        return subprocess.run(["git", "-C", at or self.repo, *a], capture_output=True, text=True, check=True).stdout

    def granted(self):
        tid = self.fm_json("task", "new", "go live", "--type", "FEATURE", "--tier", "S", "--step", "one",
                           "--ac", "live :: true")["id"]
        self.fm("task", "set", tid, "--allow", "publish")
        self.fm("focus", tid)
        return tid

    def test_live_on_needs_and_spends_a_publish_grant(self):
        import fmcore as c
        bad = self.fm("genesis", "live", "on", check=False)
        self.assertNotEqual(bad.returncode, 0)
        self.assertIn("publish grant", bad.stderr + bad.stdout)
        self.assertFalse(self.fm_json("genesis")["live"])
        tid = self.granted()
        self.git("remote", "set-url", "origin", os.path.join(self.tmp, "gone.git"))
        nowhere = self.fm("genesis", "live", "on", check=False)  # nowhere to publish: refused, the grant kept
        self.assertNotEqual(nowhere.returncode, 0)
        p0 = c.find_project(self.repo)
        self.assertIn("publish", c.find_brief(p0, tid).meta.get("allow") or [])
        self.git("remote", "set-url", "origin", self.origin)
        self.fm("genesis", "live", "on")
        p = c.find_project(self.repo)
        self.assertNotIn("publish", c.find_brief(p, tid).meta.get("allow") or [])  # one yes, spent on switching on
        self.assertEqual(self.fm_json("genesis")["live"]["remote"], "origin")
        self.fm("genesis", "live", "on")  # already on: no second grant needed or spent
        self.assertIn("site: live", self.fm("genesis").stdout)
        self.fm("genesis", "live", "off")
        self.assertFalse(self.fm_json("genesis")["live"])
        self.assertIn("site: off", self.fm("genesis").stdout)

    def test_publish_pushes_tower_data_to_main_only_when_it_changed(self):
        off = self.fm("genesis", "publish", check=False)
        self.assertNotEqual(off.returncode, 0)
        self.assertIn("live on", off.stderr + off.stdout)
        self.granted()
        self.fm("genesis", "live", "on")
        with open(os.path.join(self.repo, "local.txt"), "w") as f:
            f.write("not for main\n")
        self.git("add", "local.txt")
        self.git("commit", "-qm", "local only")
        first = self.fm_json("genesis", "publish")
        self.assertEqual(first["result"], "pushed")
        main = self.git("rev-parse", "main", at=self.origin).strip()
        self.assertEqual(first["sha"], main)
        files = self.git("diff", "--name-only", "main~1", "main", at=self.origin).split()
        self.assertIn("site/genesis/genesis.json", files)
        self.assertIn("site/genesis/gap-map.md", files)
        self.assertTrue(all(f.startswith("site/genesis/") for f in files), files)
        self.assertNotIn("local only", self.git("log", "--format=%s", "main", at=self.origin))
        self.assertEqual(self.fm_json("genesis", "publish")["result"], "up to date")
        self.assertEqual(self.git("rev-parse", "main", at=self.origin).strip(), main)
        self.fm("genesis", "put", "gen-1/seed.md", "--file", "-", input=SEED)
        again = self.fm_json("genesis", "publish")
        self.assertEqual(again["result"], "pushed")
        self.assertIn("site/genesis/gen-1/seed.md", self.git("diff", "--name-only", "main~1", "main", at=self.origin))
        self.assertIn("last push", self.fm("genesis").stdout)

    def test_kick_schedules_one_trailing_publish_per_window(self):
        import fmcore as c
        import fmgenesis
        p = c.find_project(self.repo)
        pending = os.path.join(p.dir, "genesis-publish.pending")
        self.assertFalse(fmgenesis.kick(p))
        self.assertFalse(os.path.exists(pending))
        self.granted()
        self.fm("genesis", "live", "on")
        self.assertTrue(fmgenesis.kick(p))
        self.assertFalse(fmgenesis.kick(p))  # one publish waits already, however many puts and turns follow
        self.assertEqual(self.fm_json("genesis", "publish", "--settle")["result"], "pushed")
        self.assertFalse(os.path.exists(pending))
        self.assertGreater(fmgenesis._wait(p), LIVE_WAIT_FLOOR)  # the next one waits out the window...
        self.fm("genesis", "put", "gen-1/seed.md", "--file", "-", input=SEED)
        self.assertTrue(os.path.exists(pending))  # ...but a change right after a publish is still scheduled
        os.utime(os.path.join(p.dir, "genesis-publish.last"), (0, 0))
        self.assertEqual(fmgenesis._wait(p), 0)
        self.assertEqual(self.fm_json("genesis", "publish", "--settle")["result"], "pushed")
        self.assertIn("site/genesis/gen-1/seed.md", self.git("diff", "--name-only", "main~1", "main", at=self.origin))
        self.assertTrue(fmgenesis.kick(p))
        os.utime(pending, (0, 0))  # a waiter that died: its leftover doesn't block the next change
        self.assertTrue(fmgenesis.kick(p))

    def test_failed_publish_shows_in_status_and_the_next_one_retries(self):
        self.granted()
        self.fm("genesis", "live", "on")
        self.git("remote", "set-url", "origin", os.path.join(self.tmp, "gone.git"))
        bad = self.fm("genesis", "publish", check=False)
        self.assertNotEqual(bad.returncode, 0)
        self.assertIn("failed:", self.fm("genesis").stdout)
        self.git("remote", "set-url", "origin", self.origin)
        self.assertEqual(self.fm_json("genesis", "publish")["result"], "pushed")

    def test_turn_end_kicks_a_publish(self):
        import fmcore as c
        self.granted()
        self.fm("genesis", "live", "on")
        pending = os.path.join(c.find_project(self.repo).dir, "genesis-publish.pending")
        self.assertFalse(os.path.exists(pending))
        self.hook("Stop", {"last_assistant_message": "done"})
        self.assertTrue(os.path.exists(pending))


STAGES = ("find", "understand", "plan", "build", "verify", "ship", "operate", "learn")
SURFACES = ("Claude Code", "fm code", "other agents", "MCP", "Desktop", "site", "CLI", "headless/server")


def grid(area, skip=(), over=None):
    """One coverage.md row: every stage × surface cell filled, minus `skip`, with `over` replacing given cells."""
    over, lines = over or {}, [f"## {area}"]
    for i, (s, f) in enumerate((s, f) for s in STAGES for f in SURFACES):
        if (s, f) in skip:
            continue
        cell = over.get((s, f)) or ("F: real.py — the feature", "I: a better probe (real.py)", "N/A: no stage here")[i % 3]
        lines.append(f"- {s} × {f}: {cell}")
    return "\n".join(lines) + "\n"


class GenesisCheck(ForemanTestCase):
    """Standing rules 1-3 (gen-1 seed): coverage.md has no empty or ungrounded cell; not-yet.md items were tried two
    ways and retried this generation."""
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.fm("genesis", "init", "--file", "-", input=GEN0_CAPS)
        self.fm("genesis", "put", "gen-1/seed.md", "--file", "-", input=SEED)
        with open(os.path.join(self.repo, "real.py"), "w") as f:
            f.write("x = 1\n")

    def put(self, name, text):
        self.fm("genesis", "put", name, "--file", "-", input=text)

    def check(self):
        p = self.fm("genesis", "check", "--json", check=False)
        import json
        return p.returncode, json.loads(p.stdout)

    def test_a_full_grid_and_a_tried_ledger_pass(self):
        self.put("coverage.md", "# Coverage\n\n" + grid("1. Initiative") + "\n" + grid("2. Exhaustive thinking") + grid("UX"))
        self.put("not-yet.md", "# Not yet\n\n## Self-hosted model router\n- blocker: no local model\n"
                               "- tried: ollama probe; llama.cpp spike\n- unblocks-with: #5 getting tools\n"
                               "- retried: gen-1 still no model on this box\n")
        code, res = self.check()
        self.assertEqual(code, 0, res)
        self.assertEqual((res["coverage"]["areas"], res["coverage"]["cells"], res["coverage"]["filled"]), (3, 192, 192))
        self.assertEqual((res["not_yet"]["items"], res["not_yet"]["open"]), (1, 0))
        text = self.fm("genesis", "check").stdout
        self.assertIn("✓ coverage: 3 areas, 192 of 192 cells filled", text)
        self.assertIn("✓ not-yet: 1 item", text)

    def test_empty_ungrounded_and_unknown_cells_are_flagged(self):
        bad = {("find", "MCP"): "F: nope.py", ("plan", "site"): "I: a dashboard", ("ship", "CLI"): "N/A:",
               ("learn", "Desktop"): "F: ../outside.py", ("build", "fm code"): "I: idea (gone.py)"}
        row2 = grid("2. Exhaustive thinking", skip={("verify", "MCP"), ("operate", "site")}, over=bad)
        self.put("coverage.md", grid("1. Initiative") + row2 + "- verify × Slack: F: real.py\n- just prose\n")
        code, res = self.check()
        self.assertEqual(code, 1)
        probs = "\n".join(res["coverage"]["problems"])
        for part in ("verify × MCP: empty", "operate × site: empty", "find × MCP: nope.py doesn't exist",
                     "plan × site: an I cell names the file it builds on", "ship × CLI: N/A needs its reason",
                     "learn × Desktop: ../outside.py", "build × fm code: gone.py doesn't exist", "verify × Slack isn't",
                     "just prose"):
            self.assertIn(part, probs)
        self.assertEqual(res["coverage"]["empty"], 2)
        self.assertIn("✗ coverage:", self.fm("genesis", "check", check=False).stdout)

    def test_every_capability_needs_its_row(self):
        self.put("coverage.md", grid("1. Initiative"))
        code, res = self.check()
        self.assertEqual(code, 1)
        self.assertIn("no row for capability 2. Exhaustive thinking", "\n".join(res["coverage"]["problems"]))

    def test_no_grid_at_all_is_a_failure(self):
        code, res = self.check()
        self.assertEqual(code, 1)
        self.assertIn("coverage.md doesn't exist", "\n".join(res["coverage"]["problems"]))
        self.assertEqual(res["not_yet"]["items"], 0)  # no ledger is an empty ledger

    def test_not_yet_items_need_two_tries_and_this_generations_retry(self):
        self.put("coverage.md", grid("1. Initiative") + grid("2. Exhaustive thinking"))
        self.put("not-yet.md", "# Not yet\n\n## A\n- blocker: x\n- tried: one way\n- unblocks-with: y\n- added: gen-1\n\n"
                               "## B\n- tried: p; q\n- retried: gen-1 no\n\n"
                               "## C\n- blocker: z\n- tried: p; q\n- unblocks-with: w\n- added: gen-1\n\n"
                               "## Removed\n- D: duplicate of C\n- E: too hard\n")
        code, res = self.check()
        self.assertEqual(code, 1)
        probs = "\n".join(res["not_yet"]["problems"])
        for part in ("A: tried 1 approach", "B: no blocker", "B: no unblocks-with", "E: removed only for proven harm or "
                     "an exact duplicate"):
            self.assertIn(part, probs)
        self.assertNotIn("C:", probs)
        self.assertNotIn("D:", probs)
        self.assertEqual((res["not_yet"]["items"], res["not_yet"]["open"]), (3, 2))
        self.put("gen-2/seed.md", SEED)  # a new generation: C was only tried in gen 1
        code, res = self.check()
        self.assertIn("C: not retried in gen-2", "\n".join(res["not_yet"]["problems"]))

    def test_an_empty_field_never_borrows_the_next_line_and_tries_must_differ(self):
        self.put("coverage.md", grid("1. Initiative") + grid("2. Exhaustive thinking"))
        self.put("not-yet.md", "# Not yet\n\n## F\n- blocker:\n- notes: x\n- tried: a; b\n- unblocks-with: y\n- added: gen-1\n\n"
                               "## G\n- blocker: z\n- tried: same; Same \n- unblocks-with: w\n- added: gen-1\n\n"
                               + "".join(f"## H{i}\n- tried: one\n\n" for i in range(4)))
        code, res = self.check()
        probs = "\n".join(res["not_yet"]["problems"])
        self.assertIn("F: no blocker", probs)
        self.assertIn("G: tried 1 approach", probs)
        self.assertIn("more (--json lists all)", self.fm("genesis", "check", check=False).stdout)

    def test_a_grid_without_rows_and_punctuated_paths(self):
        self.put("coverage.md", "# Coverage\n\n### Initiative\n- find × CLI: F: real.py\n")
        code, res = self.check()
        self.assertIn("coverage.md has no '## <area>' rows", "\n".join(res["coverage"]["problems"]))
        cells = grid("1. Initiative").replace("F: real.py — the feature", "F: real.py, the feature")
        self.put("coverage.md", cells + grid("2. Exhaustive thinking"))
        code, res = self.check()
        self.assertEqual(res["coverage"]["problems"], [])

    def test_status_shows_the_check(self):
        self.put("coverage.md", grid("1. Initiative", skip={("find", "MCP")}))
        res = self.fm_json("genesis")
        self.assertEqual(res["check"]["coverage"]["empty"], 1)
        self.assertIn("coverage: 63 of 64 cells filled, 1 empty", self.fm("genesis").stdout)


MISSION = "# Mission\n\n{task}\n```\nFEATURE: one\nFEATURE: two\n```\n"
DRY = "# Seed\n\nNo tier 3-4 gap left; no Missions this generation.\n"


class GenesisStep(ForemanTestCase):
    """T-2095: fm genesis step names the tower's one next action from its files alone, so a kill anywhere resumes."""
    def setUp(self):
        super().setUp()
        self.fm("init")
        import fmcore as c
        self.p = c.find_project(self.repo)

    def put(self, name, text):
        import fmgenesis
        fmgenesis.put(self.p, name, text)

    def step(self):
        import fmgenesis
        return fmgenesis.step(self.p)

    def at(self, stage, *bits):
        import fmgenesis
        d = fmgenesis.home(self.p)
        before = {r: os.stat(os.path.join(r, f)).st_mtime_ns for r, _, fs in os.walk(d) for f in fs}
        s = self.step()
        self.assertEqual(s["stage"], stage, s)
        for b in bits:
            self.assertIn(b, s["action"] + " → " + s["command"])
        self.assertEqual(s, self.step())  # a kill and a rerun give the same action
        self.assertEqual(before, {r: os.stat(os.path.join(r, f)).st_mtime_ns for r, _, fs in os.walk(d) for f in fs})
        return s

    def task(self):
        return self.fm_json("task", "new", "a brief", "--type", "FEATURE", "--tier", "S", "--step", "one",
                            "--ac", "ok :: true")["id"]

    def test_walks_every_stage_in_order_from_the_files_alone(self):
        import fmgenesis
        self.at("gen-0", "fm genesis init")
        fmgenesis.init(self.p, GEN0_CAPS.encode())
        self.assertEqual(self.at("seed", "gen-1/seed.md")["gen"], 1)
        self.put("gen-1/seed.md", SEED)
        self.at("mission", "mission-exam", "fm mission", "fm ideas")
        self.put("gen-1/mission-exam.md", MISSION.format(task=""))
        self.at("intake", "0 of 2", "fm intake")
        a, b = self.task(), self.task()
        self.put("gen-1/mission-exam.md", MISSION.format(task=f"Task: {a} (brief 1)\n"))
        self.at("build", f"fm focus {a}")
        self.fm("task", "drop", a, "done elsewhere")
        self.at("intake", "1 of 2")
        self.put("gen-1/mission-exam.md", MISSION.format(task=f"Task: {a} (brief 1), {b} (brief 2)\n"))
        self.at("build", f"fm focus {b}")
        self.fm("task", "drop", b, "done elsewhere")
        self.at("critique", "gen-1/critique-exam.md")
        self.put("gen-1/critique-exam.md", "# Critique\n")
        self.at("mission", "mission-genesis")
        t = self.task()
        self.fm("task", "drop", t, "done elsewhere")
        self.put("gen-1/mission-genesis.md", f"# Mission\n\nTask: {t}\n")  # no intake block: one brief is enough
        self.at("critique", "gen-1/critique-genesis.md")
        self.put("gen-1/critique-genesis.md", "# Critique\n")
        self.at("select", "lineage.md", "fm decide")
        self.put("lineage.md", "# Lineage\n\n## gen-1\n- kept: the first generation\n")
        self.at("drift", "gen-1/drift.md", "fm second")
        self.put("gen-1/drift.md", "# Drift\n")
        self.at("sweep", "gen-1/sweep.md")
        self.put("gen-1/sweep.md", "# Sweep\n")
        self.assertEqual(self.at("seed", "gen-2/seed.md")["gen"], 2)

    def test_a_blocked_brief_is_named_as_blocked(self):
        import fmgenesis
        fmgenesis.init(self.p, GEN0_CAPS.encode())
        self.put("gen-1/seed.md", SEED)
        t = self.task()
        self.fm("focus", t)
        self.fm("task", "block", t, "waits on a usage reset")
        self.put("gen-1/mission-exam.md", f"Task: {t}\n")
        self.assertEqual(self.at("build", f"fm focus {t}")["kind"], "blocked")

    def test_two_dry_generations_end_in_the_report_then_done(self):
        import fmgenesis
        fmgenesis.init(self.p, GEN0_CAPS.encode())
        lineage = "# Lineage\n"
        for n in (1, 2):
            self.put(f"gen-{n}/seed.md", DRY if n > 1 else SEED.split("| 1 |")[0])  # gen 1: a table with no rows
            self.at("select")
            lineage += f"\n## gen-{n}\n- dry\n"
            self.put("lineage.md", lineage)
            self.put(f"gen-{n}/drift.md", "ok\n")
            self.put(f"gen-{n}/sweep.md", "clean\n")
            if n == 1:
                self.assertEqual(self.at("seed")["gen"], 2)  # one dry generation isn't two in a row
        s = self.at("report", "report.md")
        self.assertEqual(s["gen"], 2)
        self.put("report.md", "# Report\n")
        self.assertEqual(self.at("done")["kind"], "done")

    def test_every_third_generation_names_fm_evolve(self):
        import fmgenesis
        fmgenesis.init(self.p, GEN0_CAPS.encode())
        for n in (1, 2, 3):
            self.put(f"gen-{n}/seed.md", SEED.split("| 2 |")[0].replace("mission-exam.md", "mission-x.md"))
            t = self.task()
            self.fm("task", "drop", t, "x")
            for f, text in ((f"gen-{n}/mission-x.md", f"Task: {t}\n"), (f"gen-{n}/critique-x.md", "c\n"),
                            (f"gen-{n}/drift.md", "d\n"), (f"gen-{n}/sweep.md", "s\n")):
                self.put(f, text)
            self.put("lineage.md", "".join(f"## gen-{i}\n- kept\n" for i in range(1, n + 1)))
        s = self.at("seed", "fm evolve --runs 3")
        self.assertEqual(s["gen"], 4)

    def test_caps_and_unknown_tasks_stop_the_tower(self):
        import fmgenesis
        fmgenesis.init(self.p, GEN0_CAPS.encode())
        rows = "".join(f"| {i} | mission-m{i}.md | #1 | g (3) | — |\n" for i in range(1, 10))
        self.put("gen-1/seed.md", SEED.split("| 1 |")[0] + rows)
        s = self.at("fatal", "9 Missions", "8")
        self.assertEqual(s["kind"], "fatal")
        bad = self.fm("genesis", "step", check=False)
        self.assertEqual(bad.returncode, 1)
        self.assertIn("9 Missions", bad.stdout)
        self.put("gen-1/seed.md", SEED)
        self.put("gen-1/mission-exam.md", "Task: T-9999\n")
        self.assertIn("T-9999", self.at("fatal")["action"])
        with self.assertRaises(ValueError):
            self.put("gen-1/deeper/seed.md", "x")  # only gen-N/<doc>.md fits the tower's shape

    def test_a_missions_table_that_does_not_parse_is_fatal_not_dry(self):
        import fmgenesis
        fmgenesis.init(self.p, GEN0_CAPS.encode())
        self.put("gen-1/seed.md", "# Seed\n\n| 1 | `mission-a.md` | #1 | g (3) | — |\n")
        self.assertEqual(self.at("fatal", "parse", "gen-1/seed.md")["kind"], "fatal")

    def test_a_kill_after_fm_intake_names_its_briefs_not_another_intake(self):
        import fmgenesis
        fmgenesis.init(self.p, GEN0_CAPS.encode())
        self.put("gen-1/seed.md", SEED)
        self.put("gen-1/mission-exam.md", MISSION.format(task="FIX: an example line in prose, not a brief\n"))
        self.at("intake", "0 of 2")
        made = self.fm_json("intake", "FEATURE: one\nFEATURE: two\n")
        ids = [b["id"] for b in made["created"]] if isinstance(made, dict) else [b["id"] for b in made]
        s = self.at("intake", *ids, "Task:", "fm genesis put gen-1/mission-exam.md")
        self.assertNotIn("fm intake", s["command"])

    def test_fm_next_falls_through_when_step_breaks(self):
        import fmcore as c
        import fmgenesis
        from unittest import mock
        fmgenesis.init(self.p, GEN0_CAPS.encode())
        with mock.patch.object(fmgenesis, "step", side_effect=OSError("unreadable")):
            b, kind, _text = c.next_for(self.p)
        self.assertIsNone(b)
        self.assertNotEqual(kind, "genesis")

    def test_cli_status_export_and_fm_next_name_it(self):
        import json
        self.assertNotIn("fm genesis step", self.fm("next").stdout)  # no tower, no Genesis step
        self.fm("genesis", "init", "--file", "-", input=GEN0_CAPS)
        out = self.fm("genesis", "step").stdout
        self.assertIn("gen 1 · seed", out)
        self.assertIn("→ fm genesis put gen-1/seed.md", out)
        self.assertEqual(self.fm_json("genesis", "step")["stage"], "seed")
        self.assertIn("next: write gen-1/seed.md", self.fm("genesis").stdout)
        self.assertIn("fm genesis step", self.fm("next").stdout)
        res = self.fm_json("genesis", "export", os.path.join(self.tmp, "site"))
        with open(res["path"]) as f:
            self.assertEqual(json.load(f)["next"]["stage"], "seed")
