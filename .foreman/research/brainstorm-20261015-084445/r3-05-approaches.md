# Brainstorm — lens: approaches

- **Close this round with a five-item "Newcomer" release gate** — FEATURE — value 5 — effort M — risk low — category: focus
  Why: Rounds 2-3 came back nearly dry and the pile holds thousands of ideas, while section A shows concrete newcomer failures. Assumption: the strongest approach to "THE plugin" is to ship the known newcomer fixes (PATH, doctor-clean install, `fm demo`, duplicate-capture fix, bypass opt-in) behind one exit test, not to add more.
  Done when: a clean-HOME run with no model calls passes a scripted check that `fm` is on PATH, `fm doctor` is green, `fm demo` runs, and `defaultMode` is unchanged unless the user opted in, and the release is blocked if any step fails.

- **Measure Foreman's marginal lift on top of each rival** — FEATURE — value 5 — effort L — risk med — category: proof
  Why: The bench has 1 case and no published evidence (C), and section B shows that people compare Foreman with superpowers or ECC, not with bare Claude. The question that matters is "what do I gain by adding Foreman to what I already run?". Assumption: the rivals can be installed headlessly in a bench sandbox.
  Done when: `fm bench --stack superpowers` outputs a table of pass rate and held rate for bare, rival and rival+Foreman on the same cases, with N repeats and a variance floor.

- **Pick one headline persona: the safe overnight queue** — FEATURE — value 4 — effort M — risk med — category: positioning
  Why: Every rival owns a breadth slogan, while Foreman's distinct strengths are the queue, resume, the guard in bypass mode and verified done. The 108-verb surface and the "classifies, plans, sequences…" README blur this. Assumption: the user prefers depth in one story to parity across all of them.
  Done when: the README first screen, `fm help` and the install summary lead with the unattended queue story, and a cold-reader child told to describe Foreman in one sentence names it.

- **Publish an open evidence-receipt schema with a validator** — FEATURE — value 4 — effort M — risk low — category: interop
  Why: Foreman's real contribution is that "done" carries evidence. If any plugin or CI job can emit or check a receipt, Foreman becomes the reference rather than a competitor. Assumption: rivals' outputs (spec-kit tasks, Task Master) can be mapped to the schema without Foreman running.
  Done when: `fm receipt validate FILE` accepts and rejects fixture receipts, and a spec-kit tasks file converts to a valid receipt skeleton.

- **Run a randomized n-of-1 trial in the user's own repo** — FEATURE — value 4 — effort M — risk med — category: proof
  Why: Public proof is missing (C), and a newcomer will not trust bypass mode on someone else's numbers. Assumption: a few dozen coin-flipped tasks give a rough but honest signal. This is a variant of the holdout ideas, aimed at adoption and returning a verdict card.
  Done when: after N tasks, `fm trial` prints held-rate and rework for the on and off arms with counts, and says "inconclusive" when N is too small.

- **Move the installer's third-party plugins and bypass default out of the core install** — CLEAN — value 4 — effort S — risk med — category: trust
  Why: A.2 shows the default install adds plugins, bypass mode, an output style and 20 deny rules. The approach is subtraction: the core does only what Foreman needs, and everything else becomes a named, explained offer. Assumption: no core gate depends on the extras.
  Done when: `install.sh` with no flags makes no changes outside the Foreman dir and the listed hook wiring, and each extra is a `fm wire add NAME` that prints its diff.

- **Surface the first-session path as a single conversational `/foreman:start` skill** — FEATURE — value 3 — effort S — risk low — category: onboarding
  Why: Every rival has a help or setup wizard (B), and Foreman's 231-line `--help` is the opposite. A skill that asks what the repo is, picks a gate and runs one real tiny task costs less than building new CLI screens.
  Done when: `/foreman:start` on a fixture repo ends with one task closed with evidence and prints the next command.

- **Propose the kernel upstream as a concrete Claude Code feature request** — FEATURE — value 3 — effort S — risk low — category: ecosystem — wild
  Why: If Anthropic ships "done needs evidence" natively, Foreman's guard and receipts become the reference. File requests with a working hook reference and bench numbers. Assumption: Foreman's data is persuasive enough to attract attention.
  Done when: a drafted, redacted proposal with a repro hook and measured gate yield is ready for the user to file.

- **Turn the bench into a neutral plugin referee** — FEATURE — value 4 — effort L — risk high — category: ecosystem — wild
  Why: Whoever owns the benchmark frames the category. A harness that any plugin can run against with one command, with scores listed per cell, gives Foreman credibility even where it loses. Assumption: the bench grows past 1 case first.
  Done when: `fm bench --plugin PATH` runs a rival under the same cases and prints a comparable scorecard.

- **Graduate the user: bake the learned rules into the repo and let Foreman retire** — FEATURE — value 3 — effort M — risk med — category: trust — wild
  Why: Foreman's rules already total 1k words per session, and the pile has "eject" and "lite" ideas. Making the goal "you no longer need me" differs from them by pushing the adoption bet to week 4. Assumption: users value an exit that keeps the lessons.
  Done when: `fm graduate` writes a short repo-level instructions file from lessons and gates, removes the wiring, and a session without Foreman still follows the key rules.

- **Refuse to grow: a net-surface budget that fails the release** — CLEAN — value 4 — effort S — risk low — category: simplicity
  Why: The audit (D) found 108 verbs, 46 unused in 11 days, and seven `_git` copies. A release test that counts verbs, always-on words and hook events, and fails if they rise without a removal, makes subtraction automatic. Assumption: the registry can produce these counts today.
  Done when: the release gate prints the three counts against a committed baseline and fails on any increase.

- **Hand the newcomer a "you're here" strip after every command until three tasks close** — FEATURE — value 3 — effort S — risk low — category: onboarding — wild
  Why: A.5 and A.9 show empty-state dead ends. A one-line progress strip (capture → plan → finish) with the next valid command teaches the vocabulary without a tutorial. Assumption: it fits within the terse-output rule.
  Done when: on a fresh project every `fm` output ends with a single next-step line that disappears after the third closed task.
