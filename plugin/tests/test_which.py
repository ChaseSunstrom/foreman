"""T-1699: fm which TASK ranks the skills (read from the skills folder at run time), the playbooks' headers and the
fm verbs' help against a task's words and prints what to load, each with the command that loads it."""
import json
import os

from helpers import ForemanTestCase

SKILLS = os.path.join(os.path.dirname(__file__), "..", "skills")


class Which(ForemanTestCase):
    def skills(self, **found):
        """A skills folder of {name: (description, user_only)}: fm which reads whatever the folder holds."""
        root = os.path.join(self.tmp, "skills")
        for name, (desc, user_only) in found.items():
            os.makedirs(os.path.join(root, name))
            with open(os.path.join(root, name, "SKILL.md"), "w") as f:
                f.write(f"---\nname: {name}\ndescription: {desc}\n"
                        + ("disable-model-invocation: true\n" if user_only else "") + "---\n\n# body\n")
        return {"FOREMAN_SKILLS": root}

    def test_a_3d_hero_with_motion_gets_the_design_skill_and_the_scene_and_motion_playbooks(self):
        env = self.skills(**{"ui-design": ("Use whenever you build or restyle a UI: 3D scenes, motion, layout.", False),
                             "status": ("Use whenever you report where work stands.", False)})
        out = self.fm("which", "make a 3D hero with motion", env=env).stdout
        self.assertIn("Skill foreman:ui-design", out)
        self.assertNotIn("foreman:status", out, "a skill sharing no word isn't listed")
        self.assertIn("fm playbooks show ui/scene-3d", out)
        self.assertIn("fm playbooks show ui/motion", out)
        self.assertNotIn("INDEX", out, "procedures, not the index")
        got = json.loads(self.fm("which", "make a 3D hero with motion", "--json", env=env).stdout)
        self.assertIn("fm playbooks show ui/motion", [x["load"] for x in got["playbooks"]])

    def test_the_real_skills_folder_is_read_at_run_time(self):
        out = self.fm("which", "six style directions for a new look").stdout
        self.assertIn("Skill foreman:directions", out)
        got = json.loads(self.fm("which", "make a 3D hero with motion", "--json").stdout)
        self.assertIn("Skill foreman:ui-design", [x["load"] for x in got["skills"]])
        loads = [x["load"] for x in got["playbooks"]]
        self.assertIn("fm playbooks show ui/scene-3d", loads)
        self.assertIn("fm playbooks show ui/motion", loads)
        self.assertFalse(got["skills"][0]["summary"].startswith('"'), "a YAML-quoted description, unquoted")

    def test_a_user_only_skill_is_marked_as_typed(self):
        env = self.skills(tidy=("Use whenever the user asks to clean up Foreman memory and archives.", True))
        out = self.fm("which", "clean up the archives", env=env).stdout
        self.assertIn("(you type /foreman:tidy)", out)
        self.assertNotIn("Skill foreman:tidy", out)

    def test_a_verb_is_listed_with_its_command(self):
        out = self.fm("which", "notify me when a run finishes").stdout
        self.assertIn("fm notify", out)

    def test_a_task_subcommand_is_found_by_its_help(self):  # T-1908: only top-level commands were indexed
        self.assertIn("fm task drop", self.fm("which", "drop a task").stdout)
        self.assertIn("fm task evidence", self.fm("which", "record evidence for a step").stdout)
        self.assertIn("fm task defer", self.fm("which", "defer a task").stdout)
        self.assertIn("fm task drop", self.fm("help", "drop a task").stdout)
        self.assertIn("drop a task, with why", self.fm("task", "--help").stdout)

    def test_an_action_choice_is_found_as_its_own_command(self):  # T-1916: fm lane's actions are choices, not subparsers
        self.assertIn("fm lane merge", self.fm("which", "merge a lane").stdout)
        self.assertIn("fm lane resume", self.fm("which", "take back a stopped builder's work").stdout)
        self.assertIn("fm lane merge", self.fm("help", "merge a lane").stdout)
        self.assertNotIn("fm lane list", self.fm("which", "a git worktree beside the repo").stdout, "no echo per action")
        # review: actions listed in the positional's own help count; one that only restates its command doesn't
        self.assertIn("fm playbooks blame", self.fm("which", "blame each playbook line's task from git").stdout)
        self.assertNotIn("fm round close", self.fm("which", "close a round").stdout)

    def test_the_rules_plain_words_find_their_command_and_the_strongest_kind_prints_first(self):  # T-1908
        self.assertIn("fm drive", self.fm("which", "stop auto-continuing").stdout)
        self.assertIn("fm serve", self.fm("which", "serve this repo").stdout)  # review: the second verb on its line
        self.assertTrue(self.fm("which", "what did it cost").stdout.startswith("fm commands:"))

    def test_one_common_word_is_no_match(self):
        # T-1699 review: "page" alone listed the UI playbooks and fm page for a login task nothing covers
        p = self.fm("which", "add a login page with oauth", check=False)
        self.assertEqual(p.returncode, 1, p.stdout)
        self.assertIn("Nothing matches", p.stdout)

    def test_foremans_own_release_tool_is_not_a_users_release(self):
        out = self.fm("which", "ship a release").stdout
        self.assertIn("fm playbooks show release/release-and-changelog", out)
        self.assertNotIn("fm release", out)

    def test_only_a_playbooks_header_is_indexed(self):
        # a playbook without a ## section was indexed whole, so its body's common words outranked real headers
        import fmplaybooks
        import fmwhich
        root = os.path.join(self.tmp, "books")
        os.makedirs(os.path.join(root, "references", "ui"))
        with open(os.path.join(root, "references", "ui", "long.md"), "w") as f:
            f.write("# Long\n\nUse when a thing.\n\n" + "filler words here. " * 100 + "zebra crossing\n")
        old, fmplaybooks.ROOT = fmplaybooks.ROOT, root
        try:
            text = fmwhich.playbooks()[0]["text"]
        finally:
            fmplaybooks.ROOT = old
        self.assertNotIn("zebra", text)
        self.assertLessEqual(len(text), fmwhich.HEADER_MAX + 20)

    def test_a_big_library_reads_only_the_headers_the_index_returns(self):
        # T-1835: past BIG books, fm which takes its candidates from fmplaybooks.find, not a read of every header
        from unittest import mock
        import fmplaybooks
        import fmwhich
        from test_playbook_machinery import put
        root = os.path.join(self.tmp, "books")
        for i in range(12):
            put(root, f"references/misc/b{i}.md", f"# Book {i}\n\nUse when the gizmo{i} breaks.\n\n## Steps\n\n1. x\n")
        put(root, "references/fix/kiln.md", "# Kiln repair\n\nUse when the pottery kiln overheats.\n\n## Steps\n\n1. x\n")
        with mock.patch.object(fmplaybooks, "ROOT", root), mock.patch.object(fmwhich, "BIG", 10), \
                mock.patch.object(fmwhich, "_head", wraps=fmwhich._head) as head:
            got = fmwhich.rank("repair the pottery kiln", {"playbooks": fmwhich.playbooks("repair the pottery kiln")})
        self.assertEqual([x["name"] for x in got["playbooks"]], ["fix/kiln"])
        self.assertEqual(head.call_count, 1, "only the index's hit is read")

    def test_the_stemmer_is_fmrecalls_and_collapses_doubled_consonants(self):
        import fmrecall
        import fmwhich
        self.assertEqual(fmrecall.stem("shipping"), fmrecall.stem("ship"))
        self.assertEqual(fmrecall.stem("stopped"), "stop")
        self.assertEqual(fmrecall.stem("calling"), "call", "l, s and z stay doubled")
        self.assertEqual(fmwhich.words("Shipping 3D motions"), fmrecall.words("ship 3d motion", cut=6))

    def test_an_unknown_task_says_so(self):
        p = self.fm("which", "xyzzy frobnicate quux", check=False)
        self.assertEqual(p.returncode, 1, p.stderr)
        self.assertIn("Nothing matches", p.stdout)
        p = self.fm("which", "the and a with", check=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("nothing to look up", p.stderr, "only stop words: refused, saying so")

    def test_the_prompt_hook_mentions_it_once_when_no_skill_is_named(self):
        self.fm("init")

        def ctx(prompt, sid="sess-1"):
            out = self.hook("UserPromptSubmit", {"prompt": prompt, "session_id": sid}).stdout
            return json.loads(out).get("hookSpecificOutput", {}).get("additionalContext", "") if out.strip() else ""
        first = ctx("add a --verbose flag to the parser")
        self.assertIn('fm which "', first)
        self.assertLessEqual(len(first), 400)
        self.assertNotIn("fm which", ctx("add a --quiet flag to the parser"), "once a session")
        self.assertNotIn("fm which", ctx("add a --quiet flag via /foreman:intake", "sess-2"), "a skill named already")
        self.assertNotIn("fm which", ctx("why is the sky blue?", "sess-3"), "no task in it")


if __name__ == "__main__":
    import unittest
    unittest.main()
