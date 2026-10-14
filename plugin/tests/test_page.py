"""fm page (T-0786): the queue and a research catalogue as one self-contained HTML page for a claude.ai Artifact."""
import json
import os
import re

from helpers import ForemanTestCase, read_text

import fmcore as c

CATALOGUE = [
    {"id": "step-truth", "capability": "Step pointer follows the work", "mark": "build", "why": "user-reported",
     "grounding": "fmcore.py:1029 track_step", "value": 5, "effort": "S", "risk": "low",
     "ideas": [{"n": 32, "title": "Detect step drift", "type": "FIX", "value": "4", "effort": "M", "lens": "intake"}]},
    {"id": "artifact-cockpit", "capability": "The cockpit on the phone", "mark": "later", "why": "no self-hosting",
     "grounding": "plugin/lib/fmserve.py", "value": 4, "effort": "M", "risk": "low",
     "ideas": [{"n": 7, "title": "Publish the queue", "type": "FEATURE", "value": "4", "effort": "S", "lens": "user"}]},
]
ABSOLUTE = re.compile(r"/home/|/Users/|/root/|~/")


class Page(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def _task(self, title):
        return json.loads(self.fm("task", "new", title, "--type", "FIX", "--tier", "S", "--step", "do it",
                                  "--ac", "works :: true", "--json").stdout)["id"]

    def test_the_page_holds_the_queue_and_every_cluster_and_no_path_or_secret(self):
        active = self._task("Active work in plugin/lib/fmcore.py")
        self.fm("focus", active)
        self._task("Leaky token sk-ant-abcdefghijklmnop1234 here")
        self._task("Break out </script><img src=x onerror=alert(1)>")
        self.fm("capture", "an inbox item")
        os.makedirs(os.path.join(self.p.dir, "research"), exist_ok=True)
        with open(os.path.join(self.p.dir, "research", "cat.json"), "w") as f:
            json.dump(CATALOGUE, f)
        r = self.fm("page", "--catalogue", "cat")
        path = os.path.join(self.p.dir, "page.html")
        self.assertIn(path, r.stdout)
        html = read_text(path)
        self.assertNotIn("__DATA__", html)
        for cid in ("step-truth", "artifact-cockpit", active, "plugin/lib/fmcore.py"):
            self.assertIn(cid, html)
        self.assertIsNone(ABSOLUTE.search(html), "no absolute path or home dir")
        self.assertNotIn(self.tmp, html)
        self.assertNotIn("sk-ant-abcdefghijklmnop1234", html)
        self.assertNotIn("</script><img", html, "embedded JSON can't close its script tag")
        self.assertEqual(html.count("</script>"), 2, "the data block and the code block only")
        data = json.loads(re.search(r'<script type="application/json" id="data">(.*?)</script>', html, re.S).group(1))
        self.assertEqual(data["now"]["active"]["id"], active)
        self.assertEqual(data["now"]["active"]["step"], {"n": 1, "of": 1})
        self.assertEqual(data["now"]["inbox"], 1)
        self.assertIn("[REDACTED]", json.dumps(data))
        self.assertEqual([x["id"] for x in data["catalogue"]], ["step-truth", "artifact-cockpit"])
        self.assertIn('capabilities {"db": {}, "user": {}}', r.stdout)
        self.assertIn("ArtifactData list collection picks", r.stdout)
        self.assertNotIn("url https", r.stdout, "no url until one is recorded")

    def test_an_absolute_path_refuses_the_write_and_names_the_field(self):
        tid = self._task("Fix the thing in /home/alice/app/x.py")
        r = self.fm("page", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("queue[0].title", r.stderr)
        self.assertFalse(os.path.exists(os.path.join(self.p.dir, "page.html")))
        self.fm("task", "drop", tid, "test")
        os.makedirs(os.path.join(self.p.dir, "research", "brain"), exist_ok=True)
        bad = [dict(CATALOGUE[0], grounding="see ~/.claude/rules")]
        with open(os.path.join(self.p.dir, "research", "brain", "catalogue.json"), "w") as f:
            json.dump(bad, f)
        r = self.fm("page", "--catalogue", "brain", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("catalogue[0].grounding", r.stderr)

    def test_a_recorded_url_is_printed_on_later_runs(self):
        self.fm("page", "--url", "https://claude.ai/artifact/abc123")
        r = self.fm("page")
        self.assertIn("url https://claude.ai/artifact/abc123", r.stdout)
        self.assertNotEqual(self.fm("page", "--url", "http://evil.example/x", check=False).returncode, 0)
        r = self.fm("page", "--catalogue", "nope", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("nope", r.stderr)
