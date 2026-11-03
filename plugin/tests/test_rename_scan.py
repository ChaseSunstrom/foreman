"""T-2742 (SAMPO.md): the rename's automatic check. Counts the lines on user-visible surfaces that still say Foreman,
leaving out history and the names kept as aliases. A ratchet: the count may only go down, and the rename is done at 0.
Lower BASELINE in the same commit that removes mentions; never raise it."""
import os
import re
import subprocess
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASELINE = 402  # 2026-11-03: 876 before the rename, 720 after the site and README (T-2753, T-2760), 475 after the skills, commands and output style (T-2768), 402 after the library strings and the mod (T-2779; the rest are protocol: the release subject, fmguard's refusal and posture text, which older transcripts and the guard still carry); the goal is 0
SURFACES = ("README.md", "MASTER.md", "INSTALL.md", "site/*.html", "site/*.js", "plugin/skills/**/*.md",
            "plugin/commands/*.md", "plugin/agents/*.md", ".claude-plugin/marketplace.json",
            "plugin/.claude-plugin/plugin.json", "plugin/output-styles/*", "mods/foreman-ui/**", "plugin/rules/*.md")
# names kept on purpose: old plugin ids, commands, agents, env, trailer and path, each an alias of its Sampo name, and
# the one line that says what Sampo was called
KEPT = re.compile(r"foreman(?:-ui)?@foreman|/foreman:|foreman:fm-|FOREMAN_|Foreman-Task|\.claude/foreman|"
                  r"formerly Foreman|was called Foreman|renamed from Foreman|"
                  r"chasesunstrom(?:\.github\.io)?/foreman", re.I)  # the repo's address moves only when it is renamed


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


def leftover():
    """The (path, line) pairs on a surface that name Foreman outside the kept forms."""
    out = subprocess.run(["git", "-C", ROOT, "grep", "-niw", "foreman", "--", *SURFACES], capture_output=True,
                         text=True).stdout
    rows = []
    for ln in out.splitlines():
        path, _, rest = ln.partition(":")
        text = rest.partition(":")[2]
        if re.search(r"\bforeman\b", KEPT.sub("", text), re.I):
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


if __name__ == "__main__":
    unittest.main()
