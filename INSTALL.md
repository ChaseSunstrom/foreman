# Installing Sampo (for an agent doing it on someone's behalf)

If a person asked you to install Sampo, follow these steps in order. Ask before each change to their machine; don't
assume yes. The command it installs is `sampo`; `fm` still works as an alias for it.

1. **Check the basics.** Sampo needs Linux, macOS or WSL (not native Windows), `git` and Python 3.12.7 or newer as
   `python3`; Claude Code (`claude`) is optional. Run `uname -s`, `git --version`, `python3 --version` and
   `claude --version`: without Claude Code the installer skips its plugin and settings, puts `sampo` on PATH and wires
   Codex, Gemini CLI or opencode if they're installed.
   If Python is older or missing, the installer can install one (Homebrew on macOS, `uv` elsewhere, no sudo); say so.

2. **Read the installer before running it.** Fetch
   `https://raw.githubusercontent.com/ChaseSunstrom/sampo/main/install.sh` and read it. Tell the person, in plain
   words, what it will do by default:
   - clone Sampo to `~/.claude/foreman` and, with Claude Code, register it as a Claude Code plugin; without Claude
     Code, put `sampo` on PATH and run `sampo agents install` for each of Codex, Gemini CLI and opencode it finds;
   - install a set of third-party Claude Code plugins it works well with (skip with `--no-plugins`);
   - install the sampo-ui mod: a status band and dashboard pane (skip with `--no-mod`);
   - wire Sampo into `~/.claude`: a status line wrapper, deny rules for catastrophic commands, a marked block in
     `~/.claude/CLAUDE.md`, a rules file link, and a `~/.local/bin/fm` link (skip all of it with `--no-wiring`);
   - ask whether to make `bypassPermissions` the default permission mode. Sampo is built for bypass mode: its Ward
     blocks dangerous commands instead of Claude Code asking about every one. Use `--bypass` to turn it on without the
     question or `--no-bypass` to keep the current mode. Running non-interactively, the installer can't ask, so
     without `--bypass` the mode stays as it was.
   Every change is recorded so `~/.claude/foreman/plugin/uninstall.sh` can undo it.

3. **Ask which of those they want**, and build the command from the answers, for example
   `curl -fsSL https://raw.githubusercontent.com/ChaseSunstrom/sampo/main/install.sh | bash -s -- --no-plugins --bypass`.
   Run it only after they agree. The options (`install.sh --help` prints the same):

   | Flag | What it does |
   |---|---|
   | `--no-plugins` | skip the third-party plugin setup |
   | `--no-mod` | skip the sampo-ui mod (status band, dashboard pane, toasts) |
   | `--no-wiring` | leave `~/.claude` alone: no status line wrapper, deny rules, `CLAUDE.md` block, rules link or `sampo` link |
   | `--bypass` | make `bypassPermissions` the default permission mode without asking |
   | `--no-bypass` | don't set it and don't ask |
   | `--desktop` | also install Sampo Desktop from its newest release |
   | `--build` | open Claude Code on the Sampo build (rebuild or resume from `BUILD_PROMPT.md`) |
   | anything else | passed through to `setup-plugins.sh` (for example `--security`, `--docs`, `--apply-conflicts`) |

   Environment: `FOREMAN_REPO` (git URL to clone), `FOREMAN_HOME` (where to put it, default `~/.claude/foreman`).

4. **Check it worked:** `~/.claude/foreman/plugin/bin/sampo doctor`. It lists only warnings and failures; "sampo doctor: OK"
   at the end means it's healthy. Fix or explain anything it reports.

5. **Hand over.** Tell them to restart their agent (in Claude Code, or run `/reload-plugins`), then give it any request
   in plain words, for example "fix the login timeout". `sampo demo` shows what Sampo does in about a minute, without using
   the model. `sampo --help` lists the everyday commands.

To remove it later: `~/.claude/foreman/plugin/uninstall.sh` (`--dry-run` previews; `state/` is kept unless
`--purge-state`).
