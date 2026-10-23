"""T-1556: fm extras: a run folds into a valid eight-page zine and turns into a watertight vase STL; the cursor
choreography is valid SVG; Breakout opens in the fm code app only while the checks run, closes when they stop, and
gives every key it doesn't play with back to the app, so the prompt keeps its keys."""
import json
import os
import xml.etree.ElementTree as ET
from collections import Counter

from helpers import PLUGIN, ForemanTestCase, read_text

import fmcodetui as T
import fmextras as x

SVG = "{http://www.w3.org/2000/svg}"
RUN = [dict(e) for e in T.SAMPLE_RUN]
RUN[0] = dict(RUN[0], request="fix <add> & co")


def facets(stl):
    """[(normal, [v, v, v])] from an ASCII STL, or an AssertionError naming what isn't."""
    lines = [ln.split() for ln in stl.splitlines()]
    assert lines[0][0] == "solid" and lines[-1][0] == "endsolid", "solid … endsolid"
    out, i = [], 1
    while i < len(lines) - 1:
        assert lines[i][:2] == ["facet", "normal"] and lines[i + 1] == ["outer", "loop"], lines[i]
        vs = [tuple(float(v) for v in lines[i + 2 + k][1:]) for k in range(3)]
        assert all(lines[i + 2 + k][0] == "vertex" for k in range(3))
        assert lines[i + 5] == ["endloop"] and lines[i + 6] == ["endfacet"]
        out.append((tuple(float(v) for v in lines[i][2:]), vs))
        i += 7
    return out


class Zine(ForemanTestCase):
    def test_a_run_folds_into_eight_imposed_pages(self):
        root = ET.fromstring(x.zine(RUN))
        self.assertEqual(root.get("viewBox"), "0 0 1100 850")
        pages = {int(g.get("data-page")): g for g in root.iter(SVG + "g") if g.get("class") == "page"}
        self.assertEqual(sorted(pages), list(range(1, 9)))
        for n, g in pages.items():  # the top row upside down, so it reads the right way up once folded
            self.assertEqual("rotate(180" in g.get("transform"), x.IMPOSE[n][1] == 0, n)
        at = {spot: n for n, spot in x.IMPOSE.items()}
        ring = [at[(c, 1)] for c in range(4)] + [at[(c, 0)] for c in (3, 2, 1, 0)]  # the panels round the sheet
        self.assertTrue(all((b - a) % 8 == 1 for a, b in zip(ring, ring[1:] + ring[:1])), ring)  # pages in order
        self.assertEqual(at[(3, 1)], 1, "the cover on the outer panel, not on the cut")
        text = [t.text for t in root.iter(SVG + "text")]
        self.assertIn("fix <add> & co", text)
        self.assertIn("Make calc.add", text)  # the plan's title, wrapped on the cover
        self.assertNotIn(None, text, "a blank line is space, not an empty text element")
        self.assertTrue(any("python3 test_calc.py" in (t or "") for t in text))

    def test_the_verb_writes_it_from_a_recorded_run(self):
        events = os.path.join(self.tmp, "run.jsonl")
        with open(events, "w") as f:
            f.write("\n".join(json.dumps(e) for e in RUN) + "\nnot json\n")
        out = os.path.join(self.tmp, "z.svg")
        self.fm("extras", "zine", "--events", events, "--out", out)
        self.assertIn("fix &lt;add&gt; &amp; co", read_text(out))
        self.assertNotEqual(self.fm("extras", "zine", "--events", events + ".gone", check=False).returncode, 0)


class Vase(ForemanTestCase):
    def test_the_vase_is_a_closed_solid_wound_outward(self):
        fs = facets(x.vase(RUN, segments=24))
        edges = Counter()
        for _, vs in fs:
            for a, b in zip(vs, vs[1:] + vs[:1]):
                edges[(a, b)] += 1
        self.assertTrue(all(n == 1 for n in edges.values()), "each directed edge once")
        self.assertTrue(all(edges[(b, a)] == 1 for a, b in edges), "and its reverse once: watertight, one winding")
        volume = sum(a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0])
                     + a[2] * (b[0] * c[1] - b[1] * c[0]) for _, (a, b, c) in fs) / 6
        self.assertGreater(volume, 0, "outward normals enclose a positive volume")
        for n, _ in fs:
            self.assertAlmostEqual(sum(v * v for v in n), 1.0, places=3)
        zs = [v[2] for _, vs in fs for v in vs]
        self.assertEqual((min(zs), max(zs)), (0.0, 120.0))

    def test_the_run_shapes_the_wall(self):
        calm = x.profile([{"event": "step"}] * 6)
        rough = x.profile([{"event": "verify", "exit": 1}] * 3 + [{"event": "verify", "exit": 0}] * 3)
        self.assertNotEqual([r for r, _ in calm], [r for r, _ in rough])
        out = os.path.join(self.tmp, "v.stl")
        self.fm("extras", "vase", "--out", out)
        self.assertTrue(facets(read_text(out)))


class Cursor(ForemanTestCase):
    def test_the_choreography_is_valid_svg_with_a_ripple_a_move(self):
        root = ET.fromstring(x.cursor([(10, 10), (300, 200), (600, 80)]))
        motion = next(root.iter(SVG + "animateMotion"))
        keys, times = motion.get("keyPoints").split(";"), motion.get("keyTimes").split(";")
        self.assertEqual(len(keys), len(times))
        self.assertEqual(len(motion.get("keySplines").split(";")), len(times) - 1)
        self.assertEqual((float(times[0]), float(times[-1]), float(keys[-1])), (0.0, 1.0, 1.0))
        self.assertEqual(len(list(root.iter(SVG + "circle"))), 2)
        for bad in (["1,2"], ["1,2", "1,2"], ["1,2", "x"]):  # one point, no distance, not a point
            p = self.fm("extras", "cursor", *bad, check=False)
            self.assertEqual((p.returncode, "Traceback" in p.stderr), (1, False), (bad, p.stderr))
            self.assertIn("two points or more", p.stderr)


class Breakout(ForemanTestCase):
    def app(self):
        app = T.App(T.DEFAULTS, spawn=lambda *a, **k: None)
        for e in RUN:
            app.feed(e)
        return app

    def test_it_opens_only_while_the_checks_run(self):
        app = self.app()
        self.assertTrue(T.checks_running(app.state))
        app.key("B")
        self.assertEqual(app.mode, "breakout")
        before = app.game.paddle
        app.key("KEY_LEFT")
        self.assertEqual(app.game.paddle, before - 2)
        T.render(app.state, 100, 30, app.cfg, app, t=app.clock())
        app.feed({"event": "closed", "text": "T-0001 closed", "task": "T-0001"})
        app.poll()
        self.assertEqual(app.mode, "main", "the checks stopped: the game closes")
        self.assertIn("Breakout", app.message)
        app.key("B")
        self.assertNotEqual(app.mode, "breakout")

    def test_keys_it_does_not_play_go_back_to_the_app(self):
        app = self.app()
        app.key("B")
        app.key("n")  # a new request: the prompt opens and has the keys
        self.assertEqual(app.mode, "prompt")
        paddle = app.game.paddle if app.game else None
        app.key("KEY_LEFT")
        self.assertEqual(app.mode, "prompt")
        self.assertEqual(app.game.paddle if app.game else None, paddle)

    def test_the_ball_breaks_bricks_and_never_tunnels(self):
        g = x.Breakout(20, 10)
        bricks = len(g.bricks)
        g.ball, g.vel = [2.5, 6.0], [0.0, -40.0]
        g.step(0.2)
        self.assertEqual((len(g.bricks), g.score), (bricks - 1, 1))
        self.assertEqual(len(g.lines()), 10)
        self.assertTrue(all(len(r) == 20 for r in g.lines()))
        g.ball, g.vel, g.paddle = [15.0, 8.5], [0.0, 10.0], 0
        g.step(0.3)
        self.assertEqual(g.lives, 2, "a miss costs a life")


class SonicRecipes(ForemanTestCase):
    def test_the_recipes_are_off_by_default_and_linked(self):
        ref = os.path.join(PLUGIN, "skills", "directions", "references", "sonic.md")
        text = read_text(ref)
        self.assertIn("off by default", text)
        self.assertIn("references/sonic.md", read_text(os.path.join(PLUGIN, "skills", "directions", "SKILL.md")))
