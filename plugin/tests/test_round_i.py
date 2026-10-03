"""Round I (T-0082 brainstorm): literal-aware sensitive(), section aliases and kept ticks, check timeouts, one-call
planning."""
from helpers import ForemanTestCase

import fmcore as c


class RoundI(ForemanTestCase):
    def test_sensitive_ignores_patterns_inside_string_literals(self):
        self.assertEqual(c.sensitive([], '+_RE = re.compile(r"(\\beval\\(|shell=True)")\n'), [])
        self.assertEqual(c.sensitive([], "+msg = 'never call eval( here'\n"), [])
        self.assertEqual(c.sensitive([], "+x = eval(user_input)\n"), ["eval("])
        self.assertEqual(c.sensitive([], '+subprocess.run(cmd, shell=True)  # "quoted"\n'), ["shell=True"])
        self.assertTrue(c.sensitive(["plugin/lib/fmguard.py"]), "a guard is security code")
        self.assertEqual(c.sensitive([], '+x = f"{eval(user)}"\n'), ["eval("], "an f-string's fields are code")
        self.assertEqual(c.sensitive([], "+x = rf'{exec(user)}'\n"), ["exec("])
        self.assertEqual(c.sensitive([], "+x = fr'{exec(user)}'\n"), ["exec("])

    def test_a_regex_literal_exec_is_matching_not_running_code(self):
        # T-0118: `/^✔ (T-\d+) done/.exec(line)` asked for an adversary lens on a mod's toast parsing
        self.assertEqual(c.sensitive([], "+const id = /^✔ (T-\\d+) done/.exec(l)?.[1]\n"), [])
        self.assertEqual(c.sensitive([], "+const m = /a\\/b/gi.exec(s)\n"), [])
        self.assertEqual(c.sensitive([], "+child_process.exec(cmd)\n"), ["exec("], "a shell exec is still code")
        self.assertEqual(c.sensitive([], "+exec(source)\n"), ["exec("])

    def brief(self, tid):
        p = c.find_project(self.repo)
        return next(b for b in c.load_briefs(p) if b.id == tid)

    def test_section_short_name_fills_the_template_heading(self):
        self.fm("init")
        self.fm("task", "new", "Big", "--type", "FEATURE", "--tier", "M")
        self.fm("task", "set", "T-0001", "--section", "Approach", "--text", "a vs b: a")
        b = self.brief("T-0001")
        self.assertEqual(b.section("Approach (options → choice → why)").strip(), "a vs b: a")
        self.assertEqual([h for h, _ in b.sections].count("Approach"), 0, "no second, bare Approach section")

    def test_rewriting_criteria_keeps_ticks_of_unchanged_ones(self):
        self.fm("init")
        self.fm("task", "new", "Fix", "--type", "FIX", "--tier", "S", "--ac", "works :: true", "--step", "do")
        self.fm("task", "evidence", "T-0001", "--ac", "1", "--run", "true")
        self.fm("task", "ac", "T-0001", "check", "1", check=False)
        self.assertTrue(self.brief("T-0001").acceptance()[0].checked)
        old = self.brief("T-0001").section("Acceptance criteria").strip()
        self.fm("task", "set", "T-0001", "--section", "Acceptance criteria", "--text",
                old.replace("[x]", "[ ]") + "\n- [ ] also fast")
        acs = self.brief("T-0001").acceptance()
        self.assertEqual([a.checked for a in acs], [True, False])

    def test_timeouts_say_so(self):
        code, out = c.run_command(self.repo, "sleep 5", timeout=1)
        self.assertEqual(code, 124)
        self.assertTrue(c.run_result(code, out).startswith("✗ exit 124 (timed out after 1s)"))
        self.assertIn("timed out after", self.fm("quiet", "--timeout", "1", "--", "sleep 5", check=False).stdout)

    def test_task_new_plans_an_m_brief_in_one_call(self):
        self.fm("init")
        self.fm("task", "new", "Mid", "--type", "FEATURE", "--tier", "M", "--interpretation", "what it means",
                "--approach", "a vs b: a", "--ac", "works :: pytest -q", "--step", "build", "--focus")
        b = self.brief("T-0001")
        self.assertEqual(b.status, "active")
        self.assertEqual(b.section("Interpretation").strip(), "what it means")
        self.assertEqual(b.section("Approach (options → choice → why)").strip(), "a vs b: a")

    def test_finish_closes_an_m_task_in_one_call(self):
        # T-0097: close-out cost ~18 fm calls a task across 287 real tasks; one call does it now
        self.fm("init")
        self.fm("task", "new", "Mid", "--type", "FEATURE", "--tier", "M", "--interpretation", "x", "--approach", "a vs b: a",
                "--ac", "works :: python3 -c 'print(1)'", "--ac", "fast :: python3 -c 'print(2)'", "--step", "build", "--focus")
        self.fm("task", "step", "T-0001", "done", "1", "--evidence", "python3 -c 'print(0)'", "ok")
        p = self.fm("task", "finish", "T-0001", "--audit", "fm-reviewer pass (research T-0001-review)",
                    "--lens", "intent: matches the request", "--lens", "edge: empty input handled",
                    "--docs", "README.md", "--lesson", "one call closes it", check=False)
        self.assertEqual(p.returncode, 0, p.stderr)
        b = self.brief("T-0001")
        self.assertEqual(b.status, "done")
        self.assertTrue(all(a.checked for a in b.acceptance()))
        self.assertEqual(b.section("Docs impact").strip(), "README.md")

    def test_finish_on_an_m_task_refuses_an_unknown_lens(self):
        self.fm("init")
        self.fm("task", "new", "Mid", "--type", "FEATURE", "--tier", "M", "--interpretation", "x", "--approach", "y",
                "--ac", "works :: python3 -c 'print(1)'", "--step", "build", "--focus")
        p = self.fm("task", "finish", "T-0001", "--run", "python3 -c 'print(0)'", "--audit", "review",
                    "--lens", "vibes: fine", check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("vibes", p.stderr)
