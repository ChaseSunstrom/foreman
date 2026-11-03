"""T-2742 (SAMPO.md): the rename's automatic check. Counts the lines on user-visible surfaces that still say Foreman,
leaving out history and the names kept as aliases. A ratchet: the count may only go down, and the rename is done at 0.
Lower BASELINE in the same commit that removes mentions; never raise it."""
import os
import re
import subprocess
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASELINE = 19  # 2026-11-03 (T-2818: widened to install.sh, workflows, templates, site/*.py and site/genesis; their prose renamed, Foreman Desktop and the release-subject grep kept, count unchanged at 19):876 before the rename, 720 after the site and README (T-2753, T-2760), 475 after the skills, commands and output style (T-2768), 402 after the library strings and the mod (T-2779; the rest are protocol: the release subject, fmguard's refusal and posture text, which older transcripts and the guard still carry), 61 after MASTER.md (T-2810: MASTER's lines, and the lowercase-id forms KEPT now keeps on every surface), 42 after the mod (T-2807: the code-matched forms it keeps are listed in KEPT), 23 after the agents, listing, output style and install.sh (T-2808), 19 after the rules (T-2809); the goal is 0
SURFACES = ("README.md", "MASTER.md", "INSTALL.md", "site/*.html", "site/*.js", "plugin/skills/**/*.md",
            "plugin/commands/*.md", "plugin/agents/*.md", ".claude-plugin/marketplace.json",
            "plugin/.claude-plugin/plugin.json", "plugin/output-styles/*", "mods/foreman-ui/**", "plugin/rules/*.md",
            "install.sh", ".github/workflows/*.yml", "plugin/templates/**", "site/*.py",
            "site/genesis/*.html", "site/genesis/*.js", "site/genesis/*.css")
# names kept on purpose: old plugin ids, commands, agents, env, trailer and path, each an alias of its Sampo name, and
# the one line that says what Sampo was called. T-2807: also the strings code matches (the mod's pane id 'foreman', the
# skill namespace foreman:next, the install folder /foreman/, the resume prompt the plugin and the mod both read, the
# guard's refusal and ask prefixes); each moves in the task that changes its reader (T-2809 for the guard and prompt)
KEPT = re.compile(r"foreman(?:-ui)?@foreman|foreman-ui|/foreman:|(?-i:foreman:(?=[a-z]))|foreman:fm-|FOREMAN_|Foreman-Task|"
                  r"\.claude/foreman|(?-i:/foreman/)|'foreman'|(?-i:Continue the Foreman drive)|"
                  r"(?-i:Foreman guard:|Foreman asks |Foreman\(\?: guard\)\?:)|"  # the last: register.tsx's guard regex source
                  r"formerly Foreman|was called Foreman|renamed from Foreman|"
                  # T-2810: lowercase ids a page names as code (.foreman/, refs/foreman/, foreman-ui, foreman.md, a `foreman` arm,
                  # `claude mcp add foreman`): a folder, ref, file, plugin or arm name, kept like the plugin id; a capital F is prose
                  r"(?-i:[`|/.$~-]foreman|foreman[`|/.:=-]|mcp add foreman)|"
                  # strings the code still prints or matches, which a page quotes until the code is renamed (eco.py, bench.py,
                  # release.py, cost.py, the mod's drive prompt): the quote must keep matching what runs
                  # T-2818: the desktop app and its .desktop entry keep the name until its outward rename
                  r"Foreman Desktop|Name=Foreman|Foreman\.app|\^Foreman \[0-9\]|"
                  r"\"Foreman\"|\(Foreman ID\)|false done: Foreman|Foreman X\.Y\.Z|Continue the Foreman drive", re.I)


LIB_KEPT = re.compile(r"Foreman(?=\)-Task|-Task|\(\?)|user\.name=Foreman|Foreman@|;Foreman-|foreman:Foreman|\(\?:Foreman\||Foreman guard\)|Foreman \{v\}|\(\?:Sampo\|Foreman\)|\(Sampo\|Foreman\)|Foreman\) snapshot")
# kept: trailer, git identity, the output style id, and the old name as a regex alternative (older transcripts say it)


def library_strings():
    """T-2779: the (path, text) pairs for string literals in the sampo library and the compact hook that say Foreman
    outside the kept forms (comments are not user-visible; docstrings are counted)."""
    import glob
    import io
    import tokenize
    mid = getattr(tokenize, "FSTRING_MIDDLE", -1)
    rows = []
    for f in sorted(glob.glob(os.path.join(ROOT, "plugin/lib/sampo/*.py"))) + [os.path.join(ROOT, "plugin/hooks/compact")]:
        with open(f, encoding="utf-8") as fh:
            src = fh.read()
        for t in tokenize.generate_tokens(io.StringIO(src).readline):
            if t.type in (tokenize.STRING, mid) and re.search(r"(?<![\w/.@-])Foreman\b", LIB_KEPT.sub("", t.string)):
                rows.append((os.path.relpath(f, ROOT), t.string.strip()[:100]))
    return rows


# T-2811: the repo is ChaseSunstrom/sampo now; its old address (and the Pages one, which 404s) counts wherever it appears.
# KEPT can't hide it: its lowercase-id forms keep any /foreman. (foreman-desktop is a separate repo, so `-` is not a match)
OLD_ADDR = re.compile(r"sunstrom(?:\.github\.io)?/foreman(?!-)", re.I)


def leftover():
    """The (path, line) pairs on a surface that name Foreman outside the kept forms."""
    out = subprocess.run(["git", "-C", ROOT, "grep", "-niw", "foreman", "--", *SURFACES], capture_output=True,
                         text=True).stdout
    rows = []
    for ln in out.splitlines():
        path, _, rest = ln.partition(":")
        text = rest.partition(":")[2]
        if OLD_ADDR.search(text) or re.search(r"\bforeman\b", KEPT.sub("", text), re.I):
            rows.append((path, text.strip()[:100]))
    return rows


class RenameScan(unittest.TestCase):
    def test_user_visible_foreman_only_goes_down(self):
        rows = leftover() + library_strings()
        self.assertLessEqual(len(rows), BASELINE, f"{len(rows)} lines still say Foreman (baseline {BASELINE}); "
                                                  f"first: {rows[:3]}")

    def test_kept_forms_are_not_counted(self):
        self.assertFalse(re.search(r"\bforeman\b", KEPT.sub("", "enable foreman@foreman or run /foreman:next"), re.I))
        self.assertTrue(re.search(r"\bforeman\b", KEPT.sub("", "Foreman plans before it edits"), re.I))
        self.assertFalse(re.search(r"\bforeman\b", KEPT.sub("", "pane 'foreman', skill foreman:next, /h/foreman/state"), re.I))
        self.assertFalse(re.search(r"\bforeman\b", KEPT.sub("", "Continue the Foreman drive: x"), re.I))
        self.assertFalse(re.search(r"\bforeman\b", KEPT.sub("", "Foreman guard: blocked core"), re.I))
        self.assertTrue(re.search(r"\bforeman\b", KEPT.sub("", "Foreman: open the pane"), re.I))  # display, not a kept form

    def test_old_repo_address_counts(self):  # T-2811
        for old in ("https://github.com/ChaseSunstrom/foreman/blob/main/INSTALL.md", "https://chasesunstrom.github.io/foreman/",
                    "raw.githubusercontent.com/ChaseSunstrom/foreman/main/install.sh", "gh repo clone ChaseSunstrom/foreman"):
            self.assertTrue(OLD_ADDR.search(old), old)
        self.assertFalse(OLD_ADDR.search("github.com/ChaseSunstrom/foreman-desktop"))
        self.assertFalse(OLD_ADDR.search("https://chasesunstrom.github.io/sampo/"))

    def test_lowercase_ids_are_kept_but_prose_is_not(self):  # T-2810
        for kept in ("the `foreman` arm", "writes .foreman/ in the repo", "refs/foreman/shipped", "foreman-ui mod", "rules/foreman.md",
                     "foreman.shiptest", "claude mcp add foreman -- fm mcp", "oracle|empty|foreman|plain"):
            self.assertFalse(re.search(r"\bforeman\b", KEPT.sub("", kept), re.I), kept)
        for prose in ("is foreman ok?", "Foreman.", "ask Foreman-owned work", "the foreman arm", "Foreman's ui"):
            self.assertTrue(re.search(r"\bforeman\b", KEPT.sub("", prose), re.I), prose)


if __name__ == "__main__":
    unittest.main()
