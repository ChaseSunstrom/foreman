# Brainstorm — lens: unspoken needs

- **Sample-audit the unattended output** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: assumption: the user can't read what recursive rounds ship (they say "I shouldn't even need to ask", "don't stop until complete"), so they have no cheap way to judge quality. Pulling N random shipped items per round gives an estimate with an interval, in place of full review or blind trust.
  Done when: `fm round audit` draws 3 random shipped items with their evidence, takes a one-key keep/meh/wrong on each, stores the tally, and a test shows rounds pause when the lower bound falls below the configured floor.

- **Echo every recorded veto with a one-key retract** — FIX — value 4 — effort S — risk low — category: intake
  Why: "dont' stop until complete, full auto" was recorded as a veto of the very work the user asked for, and the user only learned of it through a later fix task. Intake misreads are silent.
  Done when: any veto or drop captured from free text appears in the next greeting as "I recorded: <paraphrase> (from '<quote>')", and `fm unveto N` or one key reverses it, with a test on the "don't stop" phrasing.

- **Answer rhetorical complaints, then queue the fix** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: "why cant i launch fm code as a tui…?" and "how come … isn't recognized" are complaints phrased as questions. The user got a split into five tasks later, but nothing answered the question itself.
  Done when: a captured "why can't I / how come" message produces both a short factual answer from the code and a linked FIX task, shown in a single reply.

- **Block close on stray top-level paths the plan never named** — CLEAN — value 3 — effort S — risk low — category: hygiene
  Why: T-1371 removed a stray `--check/` site build that T-1330 committed. A new root-level path with no mention in the plan or steps is a cheap mechanical signal.
  Done when: `fm task done` fails with the path and a `git rm` hint when the diff adds a top-level entry absent from plan and scope, and passes when the plan names it.

- **Fuzz every path-taking option with option-shaped values** — FIX — value 3 — effort S — risk low — category: CLI robustness
  Why: `site/build.py` accepted `--check` as its output folder. This class of bug is cheap to find by generating `--x`, `-`, and empty values for every path argument from the arg parsers.
  Done when: a test iterates all registered verbs and scripts, passes `--zz` as each path argument, and asserts a clean usage error with no file or dir created.

- **Gate key-to-paint feel against claude** — PERFORMANCE — value 4 — effort M — risk med — category: TUI parity
  Why: the user measures `fm code` against launching `claude`. A real line editor and wider layouts are planned, but nothing measures input feel (keystroke echo, paste, Ctrl-C, resize).
  Done when: a pty test records key-to-echo latency, paste of 5 KB, Ctrl-C returning a summary, and resize reflow, and CI fails if p95 echo exceeds the stored budget (assumption: baseline taken from `claude` once, by hand).

- **A feature without a runnable demo doesn't close** — FEATURE — value 3 — effort M — risk low — category: showcase
  Why: the user asked for "better examples of fm code on the website" and "real examples". Each feature closing with a no-model fixture script feeds the site gallery as a side effect.
  Done when: closing a FEATURE task requires a `demo/<id>.sh` that exits 0 on a fixture, and `site/build.py` lists it, with a test failing for a feature lacking one.

- **Fail the site build on any third-party request** — SECURITY — value 2 — effort S — risk low — category: privacy
  Why: assumption: a privacy-minded owner (passmail address, hardened kernel) wants a public site with no CDN fonts, trackers or remote images.
  Done when: `site/build.py --check` parses the output HTML and CSS and fails on any absolute URL whose host isn't the site's own, with a fixture test.

- **Wild: Reverse demo from a typescript of the user's own claude session** — FEATURE — value 4 — effort L — risk med — category: habits
  Why: wild. The user keeps saying "like I can in claude". An opt-in, local-only `script` typescript of a few claude sessions, analysed offline, would show which keys, slash commands and flows they actually use, so parity targets come from habit.
  Done when: `fm code habits <typescript>` prints the top 10 interactions with a supported/missing column, reads nothing outside the file, and makes no network call (tested with sockets denied).

- **Wild: Fuzzy money units for budgets** — FEATURE — value 2 — effort S — risk low — category: budgets
  Why: wild. A sweeping "etc." mandate needs a cap, and "a coffee", "lunch" or "the usual" is easier to say than dollars. Foreman maps the phrase to a number the user set once and echoes it before starting.
  Done when: `fm mandate "…up to a coffee"` echoes "$4.00 (from your units file)" and enforces it, and an unknown unit asks once and stores the answer.

- **Wild: Mirror the repo to a user-owned second remote with a divergence alarm** — FEATURE — value 2 — effort M — risk low — category: local-first
  Why: wild, assumption: releases go daily to one public GitHub repo, and there is no stated copy elsewhere. A local or self-hosted bare mirror gives a recovery point, and a hash comparison can flag a force-push or account problem.
  Done when: `fm mirror add PATH` pushes tags and main after each release, and `fm doctor` reports "mirror matches origin at <sha>" or names the divergence, tested with two local bare repos.
