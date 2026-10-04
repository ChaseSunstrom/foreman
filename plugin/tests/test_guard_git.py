"""Guard: git's own write and exec channels (T-0270, from the T-0269 adversary pass). A command git runs is checked as
if typed, a file git writes is a write target, and config git loads from a file is refused; everyday git still passes."""
from helpers import ForemanTestCase  # noqa: F401  (puts plugin/lib on the path)
from test_guard import GuardCase

CORE = "{fhome}/plugin/lib/fmguard.py"
EVIL = "rm -rf ~/Documents"  # blocked only when read as a command (rm-outside), never by a word scan


class GitChannels(GuardCase):
    def test_channels_are_blocked(self):
        for cmd in (
            # git config: command-valued keys, aliases, include paths, and the file it writes
            f"git config core.fsmonitor '{EVIL}'",
            f"git config --global core.pager '{EVIL}'",
            f"git config set core.sshCommand '{EVIL}'",
            f"git config alias.x '!{EVIL}'",
            "git config alias.co checkout",
            "git config include.path /tmp/evil.cfg",
            "git config core.hooksPath /tmp/hooks",
            f"git config --file {CORE} user.name x",
            f"git config -f {CORE} user.name x",
            # environment that makes git write a file, or load config from one
            f"GIT_TRACE={CORE} git status",
            f"GIT_TRACE2_EVENT={CORE} git status",
            f"GIT_INDEX_FILE={CORE} git add .",
            "GIT_CONFIG_GLOBAL=/tmp/evil.cfg git status",
            "GIT_CONFIG_SYSTEM=/tmp/evil.cfg git status",
            "HOME=/tmp/evil git status",
            "XDG_CONFIG_HOME=/tmp/evil git status",
            "GIT_TEMPLATE_DIR=/tmp/tpl git init /tmp/r",
            "git init --template=/tmp/tpl /tmp/r",
            "git -c include.path=/tmp/evil.cfg status",
            "git -c includeIf.onbranch:main.path=/tmp/evil.cfg status",
            # an exec variable exported earlier in the same command line
            f"export GIT_SSH_COMMAND='{EVIL}'; git fetch",
            f"GIT_SSH_COMMAND='{EVIL}'; export GIT_SSH_COMMAND; git fetch",
            # review: behind wrappers and keywords, appended, cloned with, templated, abbreviated
            f"timeout 5 env GIT_SSH_COMMAND='{EVIL}' git fetch",
            f"env -u HOME GIT_SSH_COMMAND='{EVIL}' git fetch",
            f"for i in 1; do GIT_SSH_COMMAND='{EVIL}' git fetch; done",
            f"nice env GIT_TRACE={CORE} git status",
            f"GIT_SSH_COMMAND+='{EVIL}' git fetch",
            "X+=1 git -C {fhome} checkout -- plugin/lib/fmguard.py",
            f"git clone -c core.sshCommand='{EVIL}' ssh://h/r /tmp/r",
            f"git clone --config core.sshCommand='{EVIL}' ssh://h/r /tmp/r",
            "git config init.templateDir /tmp/t",
            "git -c init.templateDir=/tmp/t clone https://example.com/r.git /tmp/r",
            "git init --separate-git-dir /tmp/g {fhome}/plugin/lib/r",
            f"git rebase --exe='{EVIL}' HEAD~1",
            f"git difftool --extc='{EVIL}' HEAD",
            f"git config mergetool.x.path '{EVIL}'",
            f"git fast-export --export-marks={CORE} HEAD",
            # subcommand options that run a command
            f"git rebase -x '{EVIL}' HEAD~1",
            f"git rebase --exec='{EVIL}' HEAD~1",
            f"git bisect run {EVIL}",
            f"git submodule foreach '{EVIL}'",
            f"git difftool -x '{EVIL}' HEAD",
            f"git difftool --extcmd='{EVIL}' HEAD",
            f"git grep -O'{EVIL}' foo",
            f"git grep --open-files-in-pager='{EVIL}' foo",
            f"git fetch --upload-pack='{EVIL}' origin",
            f"git ls-remote --upload-pack '{EVIL}' origin",
            f"git push --receive-pack='{EVIL}' origin",
            f"git filter-branch --tree-filter '{EVIL}' HEAD",
            # files and trees git writes
            f"git archive -o {CORE} HEAD",
            f"git bundle create {CORE} HEAD",
            "git worktree add {fhome}/plugin/lib/wt",
            "git init {fhome}/plugin/lib/r",
            "git format-patch -o {fhome}/plugin/lib HEAD~1",
            "git format-patch --output-directory={fhome}/plugin/lib HEAD~1",
            "git format-patch -o{fhome}/plugin/lib HEAD~1",
            "git clone --separate-git-dir={fhome}/plugin/lib/g https://example.com/r.git /tmp/r",
            "git checkout-index -a --prefix={fhome}/plugin/lib/",
            "git submodule add https://example.com/r.git {fhome}/plugin/lib/sub",
        ):
            with self.subTest(cmd=cmd):
                self.assertIsNotNone(self.bash(cmd), cmd)

    def test_everyday_git_still_passes(self):
        for cmd in (
            "git status", "git -c user.name=x -c user.email=y commit --allow-empty -m x", "git log --oneline -5",
            "git config user.name", "git config --get core.pager", "git config --list", "git config user.email a@b.c",
            "git config --unset alias.x", "git rebase -i HEAD~2 --autosquash", "git grep -n foo",
            "git fetch origin", "git push origin HEAD", "git archive -o /tmp/x.tar HEAD",
            "git bundle create /tmp/x.bundle HEAD", "git worktree add /tmp/wt", "git format-patch -o /tmp/p HEAD~1",
            "GIT_TRACE=1 git status", "GIT_TRACE=/tmp/trace.log git status", "export EDITOR=vim",
            "git submodule status", "git bisect start", "git difftool --tool=meld HEAD",
            "GIT_EDITOR=true git rebase --continue", "GIT_SEQUENCE_EDITOR=: git rebase -i HEAD~2", "GIT_PAGER=cat git log",
            "EDITOR=$VISUAL git commit", "GIT_SEQUENCE_EDITOR='sed -i s/pick/squash/' git rebase -i HEAD~3",
            "git clone -c http.sslVerify=false https://example.com/r.git /tmp/r", "X=1; Y+=2; echo $X",
        ):
            with self.subTest(cmd=cmd):
                self.assertIsNone(self.bash(cmd), cmd)
