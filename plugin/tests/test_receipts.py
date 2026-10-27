"""T-1547: a UI task's receipt renders as a blueprint SVG and, signed with an SSH key, verifies with ssh-keygen -Y
verify (and stops verifying once changed); the pre-review brief lists the nits earlier reviews found in the same
files."""
import json
import os
import shutil
import subprocess
import unittest

from helpers import ForemanTestCase, read_text


class Receipts(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.tid = json.loads(self.fm("task", "new", "Warm the <buttons>", "--type", "FEATURE", "--tier", "S", "--ac",
                                      "done :: true", "--step", "style them", "--json").stdout)["id"]
        self.fm("focus", self.tid)
        with open(os.path.join(self.repo, "app.css"), "w") as f:
            f.write(".btn { color: #c99c74; transition: opacity 150ms; }\n")
        subprocess.run(["git", "-C", self.repo, "add", "app.css"], check=True)

    def test_the_receipt_as_a_blueprint(self):
        out = os.path.join(self.tmp, "receipt.svg")
        got = json.loads(self.fm("task", "receipt", self.tid, "--svg", out, "--json").stdout)
        self.assertEqual(got["svg"], out)
        svg = read_text(out)
        self.assertTrue(svg.startswith("<svg "))
        self.assertIn("app.css [UI]", svg)
        self.assertIn('fill="#c99c74"', svg)  # the swatch it added, drawn
        self.assertIn("Warm the &lt;buttons&gt;", svg)
        self.assertNotIn("<buttons>", svg)

    @unittest.skipUnless(shutil.which("ssh-keygen"), "signing needs ssh-keygen")
    def test_a_signed_receipt_verifies_and_a_changed_one_doesnt(self):
        key = os.path.join(self.tmp, "id_ed25519")
        subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", key], check=True)
        got = json.loads(self.fm("task", "receipt", self.tid, "--svg", os.path.join(self.tmp, "r.svg"), "--sign", key,
                                 "--json").stdout)

        def verify():
            with open(got["receipt"], "rb") as f:
                return subprocess.run(["ssh-keygen", "-Y", "verify", "-f", got["signers"], "-I", got["identity"], "-n",
                                       "foreman-receipt", "-s", got["signature"]], stdin=f, capture_output=True).returncode
        self.assertEqual(verify(), 0)
        self.assertIn(self.tid, read_text(got["receipt"]))
        with open(got["receipt"], "a") as f:
            f.write("one more line\n")
        self.assertNotEqual(verify(), 0, "a changed receipt no longer verifies")
        p = self.fm("task", "receipt", self.tid, "--sign", os.path.join(self.tmp, "nope"), check=False)
        self.assertNotEqual(p.returncode, 0)

    def test_the_review_brief_lists_past_nits_on_the_same_files(self):
        old = json.loads(self.fm("task", "new", "An earlier style pass", "--type", "FIX", "--tier", "S", "--ac",
                                 "x :: true", "--step", "x", "--json").stdout)["id"]
        self.fm("task", "finding", old, "design", "confirmed", "app.css: the hover colour fails 3:1 on the card")
        self.fm("task", "finding", old, "design", "rejected", "app.css: a nit that didn't hold up at all")
        self.fm("task", "finding", old, "edge", "confirmed", "other.py: unrelated to these files entirely")
        self.fm("audit", "prep", self.tid, check=False)
        brief = read_text(os.path.join(self.fm_project_dir(), "audits", f"{self.tid}.review.md"))
        self.assertIn("Past nits on these files", brief)
        self.assertIn("app.css: the hover colour fails 3:1 on the card (design, " + old + ")", brief)
        self.assertNotIn("didn't hold up", brief)
        self.assertNotIn("other.py", brief.split("Past nits on these files")[1])

    def fm_project_dir(self):
        import fmcore as c
        return c.find_project(self.repo).dir


if __name__ == "__main__":
    unittest.main()
