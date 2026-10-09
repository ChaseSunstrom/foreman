"""fm mission (T-0375): Foreman composes the mission and the brainstorm seeds for an open-ended request itself, for any
project: the user's own words, the open work, the surfaces it finds and the pillars a complete pass covers."""
import json
import os
import subprocess

from helpers import ForemanTestCase, read_text


class Mission(ForemanTestCase):
    def files(self, names):
        for name, text in names.items():
            path = os.path.join(self.repo, name)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(text)
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "files"], check=True)

    def test_mission_composes_pack_pillars_and_lenses(self):
        # the user asked twice for a hand-written JARVIS prompt; Foreman now writes it from the project itself
        self.files({"README.md": "# Jarvis\nA home assistant that runs on my server, phone and car.\n",
                    "web/src/App.svelte": "<main/>\n", "android/app/src/main/AndroidManifest.xml": "<manifest/>\n",
                    "server/requirements.txt": "anthropic\nfastapi\n", "Dockerfile": "FROM python\n"})
        self.fm("init")
        self.fm("capture", "make the car voice reliable")
        res = json.loads(self.fm("mission", "--request", "super improve jarvis, everything", "--json").stdout)
        text = read_text(res["path"])
        for part in ("super improve jarvis, everything", "make the car voice reliable", "A home assistant"):
            self.assertIn(part, text)
        self.assertTrue({"web UI", "mobile app", "server", "AI and agents"} <= set(res["surfaces"]), res["surfaces"])
        for lens in ("capability map", "approaches", "beautiful UI and motion", "every device and surface",
                     "agents of agents", "privacy and local-first"):
            self.assertIn(lens, res["lenses"])
            self.assertIn(f"--lens '{lens}'", res["ideas"])
        self.assertIn(res["pack"], res["ideas"])
        self.assertTrue(os.path.isfile(res["pack"]))
        for pillar in ("Capability map", "every idea", "screenshot", "real path", "repo sweep", "comes back dry",
                       "builder lanes"):
            self.assertIn(pillar.lower(), text.lower())

    def test_a_cli_project_gets_no_ui_lenses(self):
        self.files({"README.md": "# tool\nA command-line tool.\n", "src/main.rs": "fn main() {}\n",
                    "Cargo.toml": "[package]\nname = \"tool\"\n", "docs/index.html": "<p/>\n",
                    "server/Main.kt": "fun main() {}\n"})  # docs pages and server Kotlin aren't apps
        self.fm("init")
        res = json.loads(self.fm("mission", "--json").stdout)
        self.assertNotIn("beautiful UI and motion", res["lenses"])
        self.assertNotIn("every device and surface", res["lenses"])
        self.assertIn("capability map", res["lenses"])
        self.assertFalse({"web UI", "mobile app"} & set(res["surfaces"]), res["surfaces"])
