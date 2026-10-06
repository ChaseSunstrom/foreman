"""fm install-user / uninstall-user on a fake HOME: merge, idempotence, exact reversal, dry run."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

from helpers import FM, read_text, read_json

import fmsetup

ORIGINAL = {
    "permissions": {"defaultMode": "bypassPermissions", "deny": ["Bash(sudo *)"]},
    "statusLine": {"type": "command", "command": "$HOME/.claude/hooks/statusline-ratelimits.sh", "padding": 1},
    "env": {"KEEP": "1"},
    "theme": "dark",
}


class SetupCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.home = os.path.realpath(self._tmp.name)
        self.fhome = os.path.join(self.home, ".claude", "foreman")
        os.makedirs(os.path.join(self.fhome, "plugin", "rules"))
        with open(os.path.join(self.fhome, "plugin", "rules", "foreman.md"), "w") as f:
            f.write("# Foreman operating rules\n")
        self.settings = os.path.join(self.home, ".claude", "settings.json")
        with open(self.settings, "w") as f:
            json.dump(ORIGINAL, f, indent=2)
        self.claude_md = os.path.join(self.home, ".claude", "CLAUDE.md")
        with open(self.claude_md, "w") as f:
            f.write("# graphify\n- keep me\n")

    def tearDown(self):
        self._tmp.cleanup()

    def run_fm(self, *args):
        env = dict(os.environ, HOME=self.home, FOREMAN_HOME=self.fhome)
        return subprocess.run([sys.executable, FM, *args], capture_output=True, text=True, env=env, timeout=30)

    def load(self):
        with open(self.settings) as f:
            return json.load(f)

    def manifest_path(self):
        return os.path.join(self.fhome, "state", "install-manifest.json")


class Install(SetupCase):
    def test_install_wires_everything_and_records_originals(self):
        p = self.run_fm("install-user")
        self.assertEqual(p.returncode, 0, p.stderr)
        s = self.load()
        self.assertEqual(s["statusLine"]["command"], os.path.join(self.fhome, "plugin", "hooks", "statusline"))
        self.assertEqual(s["statusLine"]["padding"], 1)
        for rule in fmsetup.DENY_RULES:
            self.assertIn(rule, s["permissions"]["deny"])
        self.assertIn("Bash(sudo *)", s["permissions"]["deny"])
        self.assertEqual(s["env"]["KEEP"], "1")
        self.assertEqual(s["env"]["CLAUDE_CODE_STOP_HOOK_BLOCK_CAP"], fmsetup.STOP_CAP)
        self.assertEqual(s["env"]["CLAUDE_AUTOCOMPACT_PCT_OVERRIDE"], "70", "compact earlier: Foreman state makes it cheap")
        self.assertEqual((s["theme"], s["permissions"]["defaultMode"]), ("dark", "bypassPermissions"))
        md = read_text(self.claude_md)
        self.assertTrue(md.startswith("# graphify\n- keep me\n"))
        self.assertIn("<!-- foreman:begin -->", md)
        self.assertIn("~/.claude/rules/foreman.md", md)
        link = os.path.join(self.home, ".claude", "rules", "foreman.md")
        self.assertEqual(os.path.realpath(link), os.path.join(self.fhome, "plugin", "rules", "foreman.md"))
        m = read_json(self.manifest_path())
        self.assertEqual(m["statusLine_original"], ORIGINAL["statusLine"])
        self.assertTrue(m["statusline_hud"])
        self.assertTrue(any(b.startswith("settings.json.") for b in os.listdir(os.path.join(self.fhome, "backups"))))

    def test_selects_the_foreman_output_style_only_when_none_is_set(self):
        self.run_fm("install-user")
        self.assertEqual(self.load()["outputStyle"], fmsetup.OUTPUT_STYLE)
        self.run_fm("uninstall-user")
        self.assertNotIn("outputStyle", self.load())
        with open(self.settings, "w") as f:
            json.dump(dict(ORIGINAL, outputStyle="Concise"), f)
        self.run_fm("install-user")
        self.assertEqual(self.load()["outputStyle"], "Concise", "the user's own style stays")
        self.run_fm("uninstall-user")
        self.assertEqual(self.load()["outputStyle"], "Concise")

    def test_second_install_is_a_noop(self):
        self.run_fm("install-user")
        s1, md1, m1 = self.load(), read_text(self.claude_md), read_text(self.manifest_path())
        p = self.run_fm("install-user")
        self.assertEqual(p.returncode, 0)
        self.assertEqual((self.load(), read_text(self.claude_md)), (s1, md1))
        self.assertEqual(read_text(self.manifest_path()), m1)
        self.assertIn("already", p.stdout)

    def test_dry_run_changes_nothing(self):
        before = read_text(self.settings)
        p = self.run_fm("install-user", "--dry-run")
        self.assertEqual(p.returncode, 0)
        self.assertIn("statusLine", p.stdout)
        self.assertEqual(read_text(self.settings), before)
        self.assertFalse(os.path.exists(os.path.join(self.home, ".claude", "rules", "foreman.md")))

    def test_refuses_to_replace_a_foreign_rules_file(self):
        rules_dir = os.path.join(self.home, ".claude", "rules")
        os.makedirs(rules_dir)
        with open(os.path.join(rules_dir, "foreman.md"), "w") as f:
            f.write("my own file")
        p = self.run_fm("install-user")
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(read_text(os.path.join(rules_dir, "foreman.md")), "my own file")

    def test_missing_settings_file_is_created(self):
        os.remove(self.settings)
        self.assertEqual(self.run_fm("install-user").returncode, 0)
        self.assertIn("statusLine", self.load())

    def test_record_disabled_plugins_is_additive_and_only_touches_the_manifest(self):
        self.run_fm("install-user")
        before = self.load()
        self.assertEqual(self.run_fm("install-user", "--record-disabled", "ecc@ecc", "--record-disabled", "x@y").returncode, 0)
        self.run_fm("install-user", "--record-disabled", "ecc@ecc")
        self.assertEqual(read_json(self.manifest_path())["plugins_disabled"], ["ecc@ecc", "x@y"])
        self.assertEqual(self.load(), before)


class Uninstall(SetupCase):
    def test_round_trip_restores_originals(self):
        self.run_fm("install-user")
        p = self.run_fm("uninstall-user")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(self.load(), ORIGINAL)
        self.assertEqual(read_text(self.claude_md), "# graphify\n- keep me\n")
        self.assertFalse(os.path.lexists(os.path.join(self.home, ".claude", "rules", "foreman.md")))
        self.assertFalse(os.path.exists(self.manifest_path()))

    def test_user_changes_after_install_are_kept(self):
        self.run_fm("install-user")
        s = self.load()
        s["permissions"]["deny"].append("Bash(curl *)")
        s["env"]["CLAUDE_CODE_STOP_HOOK_BLOCK_CAP"] = "99"
        with open(self.settings, "w") as f:
            json.dump(s, f)
        self.run_fm("uninstall-user")
        s = self.load()
        self.assertIn("Bash(curl *)", s["permissions"]["deny"])
        self.assertEqual(s["env"]["CLAUDE_CODE_STOP_HOOK_BLOCK_CAP"], "99", "a value the user changed is not ours to remove")

    def test_empty_plugin_maps_left_by_claude_plugin_uninstall_are_dropped(self):
        # uninstall.sh removes the plugin and marketplace first; Claude Code leaves the emptied maps behind.
        self.run_fm("install-user")
        s = self.load()
        s.update(enabledPlugins={}, extraKnownMarketplaces={})
        with open(self.settings, "w") as f:
            json.dump(s, f)
        self.run_fm("uninstall-user")
        self.assertEqual(self.load(), ORIGINAL)

    def test_plugin_maps_with_entries_are_kept(self):
        self.run_fm("install-user")
        s = self.load()
        s["enabledPlugins"] = {"other@x": True}
        with open(self.settings, "w") as f:
            json.dump(s, f)
        self.run_fm("uninstall-user")
        self.assertEqual(self.load()["enabledPlugins"], {"other@x": True})

    def test_users_own_compaction_threshold_is_kept(self):
        s = dict(ORIGINAL, env={"KEEP": "1", "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "50"})
        with open(self.settings, "w") as f:
            json.dump(s, f)
        self.run_fm("install-user")
        self.assertEqual(self.load()["env"]["CLAUDE_AUTOCOMPACT_PCT_OVERRIDE"], "50")
        self.run_fm("uninstall-user")
        self.assertEqual(self.load()["env"]["CLAUDE_AUTOCOMPACT_PCT_OVERRIDE"], "50")

    def test_restores_recorded_default_mode(self):
        self.run_fm("install-user")
        m = read_json(self.manifest_path())
        m["defaultMode_original"] = "auto"
        with open(self.manifest_path(), "w") as f:
            json.dump(m, f)
        self.run_fm("uninstall-user")
        self.assertEqual(self.load()["permissions"]["defaultMode"], "auto")

    def test_without_manifest_is_harmless(self):
        p = self.run_fm("uninstall-user")
        self.assertEqual(p.returncode, 0)
        self.assertEqual(self.load(), ORIGINAL)


class UninstallScript(SetupCase):
    def test_purge_uses_the_state_dir_in_use(self):
        alt = os.path.join(self.home, "alt-state")
        os.makedirs(os.path.join(alt, "projects"))
        uninstall = os.path.join(os.path.dirname(os.path.dirname(FM)), "uninstall.sh")
        env = dict(os.environ, HOME=self.home, FOREMAN_HOME=self.fhome, FOREMAN_STATE=alt)
        p = subprocess.run(["bash", uninstall, "--dry-run", "--purge-state", "--yes"], capture_output=True, text=True,
                           env=env, timeout=60)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn(alt, p.stdout)
        self.assertTrue(os.path.isdir(alt), "dry run removes nothing")


class InstallScript(unittest.TestCase):
    """install.sh with stub claude and setup-plugins.sh: plugin-dev (--build-tools) only when building."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = os.path.realpath(self._tmp.name)
        self.fhome = os.path.join(tmp, "foreman")
        os.makedirs(self.fhome)
        subprocess.run(["git", "init", "-q", "-b", "scratch", self.fhome], check=True)
        subprocess.run(["git", "-C", self.fhome, "-c", "user.email=t@example.com", "-c", "user.name=t",
                        "commit", "-q", "--allow-empty", "-m", "init"], check=True)
        repo = os.path.dirname(os.path.dirname(os.path.dirname(FM)))
        with open(os.path.join(repo, "install.sh")) as src, open(os.path.join(self.fhome, "install.sh"), "w") as dst:
            dst.write(src.read())
        self.args_file = os.path.join(tmp, "setup-args")
        stubs = {os.path.join(self.fhome, "setup-plugins.sh"): f'echo "$@" > {self.args_file}\n',
                 os.path.join(tmp, "bin", "claude"): "exit 0\n"}
        for path, body in stubs.items():
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write("#!/usr/bin/env bash\n" + body)
            os.chmod(path, 0o755)
        self.env = dict(os.environ, HOME=tmp, FOREMAN_HOME=self.fhome,
                        PATH=os.path.join(tmp, "bin") + os.pathsep + os.environ["PATH"])

    def tearDown(self):
        self._tmp.cleanup()

    def setup_args(self, *flags):
        p = subprocess.run(["bash", os.path.join(self.fhome, "install.sh"), "--no-bypass", "--no-wiring", *flags],
                           capture_output=True, text=True, env=self.env, stdin=subprocess.DEVNULL, timeout=60)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        return read_text(self.args_file).split()

    def test_plain_install_skips_build_tools(self):
        self.assertEqual(self.setup_args("--security"), ["--security"])

    def test_build_install_adds_build_tools(self):
        self.assertIn("--build-tools", self.setup_args("--build"))

    def install_python(self, system):
        """install.sh where python3 is 3.12.3 (Ubuntu 24.04's, too old) until brew or uv installs one; uname says
        `system`. Returns the run and the installer calls made."""
        home = self.env["HOME"]
        mark, calls = os.path.join(home, "installed"), os.path.join(home, "calls")
        stubs = {"python3": f'[ -e {mark} ] && exec {sys.executable} "$@"\necho "Python 3.12.3"; exit 1\n',
                 "uname": f"echo {system}\n",
                 "brew": f'echo "brew $*" >> {calls}; touch {mark}\n',
                 "uv": f'[ "$2" = dir ] && {{ echo {home}/bin; exit; }}\necho "uv $*" >> {calls}; touch {mark}\n'}
        for name, body in stubs.items():
            path = os.path.join(home, "bin", name)
            with open(path, "w") as f:
                f.write("#!/usr/bin/env bash\n" + body)
            os.chmod(path, 0o755)
        p = subprocess.run(["bash", os.path.join(self.fhome, "install.sh"), "--no-plugins", "--no-bypass", "--no-wiring"],
                           capture_output=True, text=True, env=self.env, stdin=subprocess.DEVNULL, timeout=60)
        return p, read_text(calls) if os.path.exists(calls) else ""

    def test_too_old_python_is_replaced_by_uv_on_linux(self):
        p, calls = self.install_python("Linux")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        # update-shell: later shells (and the hooks) find this python3 too, not only the rest of install.sh
        self.assertEqual(calls, "uv python install 3.13 --default\nuv python update-shell\n")

    def test_too_old_python_is_replaced_by_homebrew_on_macos(self):
        p, calls = self.install_python("Darwin")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertEqual(calls, "brew install python\n")

    def test_native_windows_is_pointed_at_wsl(self):
        p, calls = self.install_python("MINGW64_NT-10.0-26100")
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("WSL", p.stderr)
        self.assertEqual(calls, "")

    def test_fresh_machine_round_trip_leaves_no_settings_file(self):
        repo = os.path.dirname(os.path.dirname(os.path.dirname(FM)))
        os.symlink(os.path.join(repo, "plugin"), os.path.join(self.fhome, "plugin"))
        settings = os.path.join(self.env["HOME"], ".claude", "settings.json")
        self.assertFalse(os.path.exists(settings))
        p = subprocess.run(["bash", os.path.join(self.fhome, "install.sh"), "--no-plugins"], capture_output=True,
                           text=True, env=self.env, stdin=subprocess.DEVNULL, timeout=60)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertEqual(read_json(settings)["permissions"]["defaultMode"], "bypassPermissions")
        p = subprocess.run([sys.executable, FM, "uninstall-user"], capture_output=True, text=True, env=self.env,
                           timeout=60)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertFalse(os.path.exists(settings), read_text(settings) if os.path.exists(settings) else "")


if __name__ == "__main__":
    unittest.main()


class SetupPluginsInSession(unittest.TestCase):
    """T-0039: inside a Claude Code session the guard can't see the installs in the script's body, so a real run
    refuses there and points at the pinned path (fm ask ID plugin --pin, then fm plugins install)."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = os.path.realpath(self._tmp.name)
        self.calls = os.path.join(tmp, "calls")
        os.makedirs(os.path.join(tmp, "bin"))
        with open(os.path.join(tmp, "bin", "claude"), "w") as f:
            f.write(f'#!/usr/bin/env bash\necho "claude $*" >> {self.calls}\n'
                    f'if [ "$2" = list ]; then echo "[]"; fi\nexit 0\n')
        os.chmod(os.path.join(tmp, "bin", "claude"), 0o755)
        self.script = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(FM))), "setup-plugins.sh")
        self.env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
        self.env.update(HOME=tmp, PATH=os.path.join(tmp, "bin") + os.pathsep + os.environ["PATH"])

    def tearDown(self):
        self._tmp.cleanup()

    def run_script(self, *args, **env):
        return subprocess.run(["bash", self.script, *args], capture_output=True, text=True, timeout=120,
                              env=dict(self.env, **env), stdin=subprocess.DEVNULL)

    def installs(self):
        return [l for l in (read_text(self.calls) if os.path.exists(self.calls) else "").splitlines()
                if " install " in l or " enable " in l]

    def test_a_real_run_inside_a_session_refuses_and_changes_nothing(self):
        p = self.run_script(CLAUDECODE="1")
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("fm plugins install", p.stderr)
        self.assertEqual(self.installs(), [])
        self.assertEqual(self.run_script("--dry-run", CLAUDECODE="1").returncode, 0)

    def test_outside_a_session_it_runs_as_before(self):
        p = self.run_script()
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertTrue(self.installs(), "the curated plugins are installed")
