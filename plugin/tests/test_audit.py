"""T-0723: the diff a reviewer reads (fm audit prep) leaves out what it needn't read in full: a change repeated in
synced copies, the far end of long context lines, fixtures and lockfiles. Changed lines always stay whole."""
import json
import os

from helpers import ForemanTestCase
from test_hooks import HookCase

import fmcli
import fmcore as c


def block(path, body):
    return f"diff --git a/{path} b/{path}\nindex 1111111..2222222 100644\n--- a/{path}\n+++ b/{path}\n{body}"


RULE = "@@ -1,3 +1,3 @@\n same\n-old rule\n+new rule\n"


class CompactDiff(ForemanTestCase):
    def test_copies_long_context_and_fixtures_shrink_and_changes_stay_whole(self):
        long_ctx, long_add = " " + "c" * 500, "+" + "a" * 500
        diff = (block("plugin/rules/foreman.md", RULE) + block("plugin/evals/x/prompt.md", RULE)
                + block("plugin/evals/y/prompt.md", RULE)
                + block("MASTER.md", f"@@ -1,2 +1,2 @@\n{long_ctx}\n-a\n{long_add}\n")
                + block("plugin/tests/fixtures/run.txt", "@@ -0,0 +1,3 @@\n+f1\n+f2\n+f3\n")
                + block("package-lock.json", "@@ -1 +1 @@\n-x\n+y\n"))
        out = fmcli._compact_diff(diff)
        self.assertEqual(out.count("+new rule"), 1, "one copy of a repeated change")
        self.assertIn("plugin/evals/x/prompt.md: the same change as plugin/rules/foreman.md", out)
        self.assertIn("plugin/evals/y/prompt.md: the same change as plugin/rules/foreman.md", out)
        self.assertNotIn("c" * 300, out, "long context is cut")
        self.assertIn(long_add, out, "a changed line stays whole")
        self.assertNotIn("+f2", out)
        self.assertIn("plugin/tests/fixtures/run.txt: a fixture or lockfile, +3 −0 lines, left out", out)
        self.assertIn("package-lock.json: a fixture or lockfile, +1 −1 lines, left out", out)
        self.assertLess(len(out), len(diff))

    def test_pre_audit_flags_a_hotspot_file_only(self):
        import fmmap
        found = [x for x in fmmap.pre_audit(self.repo, "", ["a.py", "b.py"], {"fixy": {"a.py": 4}}) if "hotspot" in x]
        self.assertEqual(len(found), 1)
        self.assertIn("a.py", found[0])

    def test_a_file_with_a_changed_line_over_4000_chars_is_left_out(self):
        long = "x" * 20000
        out = fmcli._compact_diff(block("demo/live.cast", f"@@ -0,0 +1,2 @@\n+{long}\n+short\n")
                                  + block("a.py", "@@ -1 +1 @@\n-x = 1\n+x = 2\n"))
        self.assertIn("demo/live.cast: generated or minified (a changed line over 4000 characters), +2 −0 lines, left out", out)
        self.assertNotIn("x" * 100, out)
        self.assertIn("+x = 2", out)

    def test_a_plain_diff_is_unchanged(self):
        diff = block("a.py", "@@ -1 +1 @@\n-x = 1\n+x = 2\n")
        self.assertEqual(fmcli._compact_diff(diff), diff)


PERSONAS = ("art director", "accessibility reviewer", "first-time user")


class DesignLens(HookCase):
    """T-1501: a UI diff gets a design read by three personas; any other diff costs nothing extra."""

    def write(self, rel, text="x\n"):
        path = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(path) or self.repo, exist_ok=True)
        with open(path, "w") as f:
            f.write(text)

    def prep(self, tier="M"):
        self.fm("init")
        self.tid = self.task(tier=tier)

    def brief(self):
        data = json.loads(self.fm("audit", "prep", self.tid, "--json").stdout)
        with open(data["brief"]) as f:
            return data["lenses"], f.read()

    def test_ui_paths_finds_ui_files_and_leaves_the_rest(self):
        ui =["web/app.css", "web/x.scss", "a/b.less", "src/App.tsx", "src/c.jsx", "v/a.vue", "s/a.svelte",
              "p/index.astro", "site/index.html", "mods/foreman-ui/hooks/state.ts", "plugin/lib/fmcodetui.py",
              "plugin/templates/tui/cost_meter.py", "app/templates/home.jinja"]
        other = ["a.py", "plugin/templates/brief.md", "plugin/templates/mcp-server/server.py", "lib/intuition.py",
                 "plugin/tests/test_code_tui.py", "mods/foreman-ui/tests/pane.test.tsx",
                 "plugin/tests/fixtures/design/slop.css", "README.md", "mods/foreman-ui/tools/shot.py",
                 "mods/foreman-ui/hooks/hooks.json", "roles/web/templates/nginx.conf.j2", "demo/code-tui.mp4"]
        self.assertEqual(c.ui_paths(ui + other), ui)

    def test_ui_paths_skips_what_design_lint_skips(self):  # review: built, vendored and generated files aren't UI
        self.assertEqual(c.ui_paths(["dist/app.css", "node_modules/x/a.html", "src/app.css"]), ["src/app.css"])
        skipped = ["web/vendor/b.css", "build/i.html", "out/i.html", "target/site/i.html", "venv/lib/a.html",
                   "static/app.min.css", "htmlcov/index.html", "coverage/lcov-report/index.html"]
        self.assertEqual(c.ui_paths(skipped), [])
        self.assertEqual(c.ui_paths(["plugin/hooks/statusline", "plugin/hooks/subagent-statusline", "bin/status"]),
                         ["plugin/hooks/statusline", "plugin/hooks/subagent-statusline"], "Foreman's own UI")

    def test_a_screenshot_under_a_dot_directory_is_never_listed(self):  # review: ~/.ssh, .config and the like
        self.prep()
        self.write("web/app.css")
        self.write(".cache/shot.png", "png")
        self.write("shots/ok.png", "png")
        self.fm("task", "log", self.tid, "see .cache/shot.png and shots/ok.png")
        design = self.brief()[1].split("## design")[1]
        self.assertNotIn("shot.png", design)
        self.assertIn("ok.png", design)

    def test_only_a_lens_heading_switches_the_lens(self):  # review: "## Design notes" is not the design lens
        import fmlanes
        got = fmlanes.reviewer_findings("## maintainer\n- LOW — a.py:1 — x\n## Design notes\n- LOW — b.py:2 — y\n"
                                        "## Edge cases\n- LOW — c.py:3 — z\n## lens: design\n- LOW — d.py:4 — w\n"
                                        "## edge: changes needed\n- LOW — e.py:5 — v")
        self.assertEqual([x[0] for x in got], ["maintainer"] * 3 + ["design", "edge"])
        self.fm("init")
        self.task()
        self.fm("research", "add", "t0009-review", input="## design-system\n**HIGH — tokens drift**\n"
                                                         "## design: changes needed\n**HIGH — no focus ring**\n")
        out = self.fm("audit", "prep", "--print", "T-0001", "--lens", "design").stdout
        self.assertIn("no focus ring", out)
        self.assertNotIn("tokens drift", out)

    def test_the_reviewer_prompt_and_template_define_the_three_personas(self):
        for rel in (("agents", "fm-reviewer.md"), ("skills", "intake", "references", "audit.md")):
            with open(os.path.join(c.PLUGIN_ROOT, *rel)) as f:
                text = f.read().lower()
            for who in PERSONAS:
                with self.subTest(file=rel[-1], persona=who):
                    self.assertIn(who, text)
            self.assertIn("design", text)
        self.assertIn("design", c.AUDIT_LENSES, "recordable with fm task audit ID design")
        self.assertNotIn("design", c.DEFAULT_LENSES)
        self.assertFalse(any("design" in g for t in c.REQUIRED_AUDITS.values() for g in t), "advisory, not required")

    def test_prep_names_the_design_lens_for_a_ui_diff_with_its_screenshots(self):
        self.prep()
        self.write("web/app.css", "body { color: #333 }\n")
        self.write("shots/home.png", "png")
        self.fm("task", "log", self.tid, "screenshot shots/home.png and shots/gone.png")
        lenses, text = self.brief()
        self.assertEqual(lenses, list(c.DEFAULT_LENSES) + ["design"])
        self.assertIn("## design", text)
        for who in PERSONAS:
            self.assertIn(who, text.lower())
        self.assertIn("web/app.css", text.split("## design")[1])
        self.assertIn(os.path.join(self.repo, "shots", "home.png"), text, "a screenshot the task names, to read")
        self.assertNotIn("gone.png", text.split("## design")[1], "a named screenshot that isn't there is left out")

    def test_an_s_task_with_a_ui_diff_gets_the_design_lens_too(self):
        self.prep(tier="S")
        self.write("src/App.tsx", "export const A = () => null\n")
        lenses, text = self.brief()
        self.assertEqual(lenses, ["self", "design"])
        self.assertIn("No screenshots", text)

    def test_a_backend_diff_gets_no_design_lens(self):
        self.prep()
        self.write("a.py", "x = 1\n")
        lenses, text = self.brief()
        self.assertEqual(lenses, list(c.DEFAULT_LENSES))
        self.assertNotIn("## design", text)
