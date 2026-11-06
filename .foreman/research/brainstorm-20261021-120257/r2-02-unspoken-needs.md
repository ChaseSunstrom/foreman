# Brainstorm — lens: unspoken needs

- **Make `fm code` a drop-in for `claude` flags** — FEATURE — value 5 — effort M — risk med — category: compatibility
  Why: the user asked "why cant i launch fm code … like I can claude code" and wants it "modelled on the Claude Code GitHub repo". Muscle memory and scripts use `claude -c`, `-r`, `-p`, `--model`, `--output-format`, `--permission-mode`, `--add-dir`, and `claude mcp|plugin|doctor`. Assumption: no flag-level parity exists yet beyond opening the app.
  Done when: a test table built from the documented claude flags passes against `fm code`, each flag either honoured or refused with a named reason, and `alias claude='fm code'` runs `-p "hi" --output-format json` without error.

- **Measure "work with anything" with a request-kind coverage matrix** — FEATURE — value 4 — effort L — risk med — category: coverage
  Why: the user said "I should be able to do anything with it". Nothing measures breadth. Proposal: about 150 request kinds (sysadmin, docs, data cleanup, git archaeology, packaging, config edits, non-code files), each with a tiny fixture and a runnable check. Nightly run on the default runner, and the first failing kinds become briefs.
  Done when: `fm code bench --kinds` prints a kinds × outcome grid with pass/fail per kind, and a deliberately broken kind fails with its fixture path.

- **Preserve bytes the model didn't mean to change** — FIX — value 4 — effort S — risk low — category: edit safety
  Why: assumption: weaker models normalise CRLF, drop the final newline or BOM, lose the exec bit, or follow symlinks when rewriting a file. The harness already judges every changed file, so it can add this check cheaply.
  Done when: a fixture edit that flips CRLF→LF, strips the BOM or drops mode 0755 is refused or auto-restored, with the reason named in the run's checks.

- **Climb a slot-format ladder when a model fails a slot** — FEATURE — value 4 — effort M — risk low — category: small models
  Why: the harness has the model fill one small checked JSON slot at a time. A local small model that fails twice should not just retry. Descend: free JSON → choose from an enum → ranked options → a yes/no sequence, and remember the rung per model and slot. The failure evidence is the existing "misbehaving fake runners" item on the planned slate.
  Done when: a scripted fake model that only answers yes/no completes a plan slot via the ladder, and the next run starts on that rung.

- **Wild: ship a fake `claude` binary so other tools run on any model** — FEATURE — value 4 — effort M — risk med — category: interop
  Why: wild. IDE extensions, Agent SDK apps and plugins like ralph-wiggum spawn `claude`. `fm-claude` would speak claude's stream-json in and out and drive any runner behind it, with the guard still in the loop. Assumption: the stream-json shape is stable enough to conformance-test.
  Done when: a recorded stream-json session from a stub SDK client round-trips through `fm-claude` against a local model, and the output validates against the same schema as real claude's.

- **Wild: write the future README first and let its failing fences be the queue** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: wild. The user's mandates ("fully featured/implemented", "10x") are unbounded. Compile each mandate into a README section with runnable code fences. The gap between that README and reality is the build queue, and a round closes when every fence is green.
  Done when: `fm round readme "<mandate>"` writes a draft whose fences all fail, and a built feature turns its fence green.

- **Wild: make weak models explain themselves in smaller questions** — FEATURE — value 3 — effort M — risk med — category: small models
  Why: wild. When a plan slot fails on a small model, the harness rewrites the task into the next easier question (quote the line, pick A/B, confirm yes/no), then reassembles the answer itself. It borrows the prompt tutorial's "step-by-step, quote evidence, allow unknown" techniques as a mechanical fallback, not a prompt tip.
  Done when: a failing slot on a scripted weak fake completes through decomposed questions, and the reassembled answer passes the same schema check.

- **Show a requirements card on every adopted plugin** — SECURITY — value 3 — effort S — risk low — category: adoption
  Why: financial-services ships 12 paid MCP connectors, and many marketplace entries need API keys, binaries or network hosts. Users should learn that before enabling, not from a failed run. Assumption: `marketplace.json` and plugin manifests expose enough to extract most of it.
  Done when: `fm plugins show NAME` lists paid connectors, required keys, hosts and binaries, and enabling an entry with an unmet requirement says what is missing.

- **Watch for retired model IDs in `models.json` and propose the swap** — FIX — value 3 — effort S — risk low — category: runners
  Why: assumption: configured models retire (cloud IDs are deprecated, local models get removed from Ollama), and the user finds out as a silent stall. Runner preflight could catch the 404 or deprecation notice and propose a replacement as a diff.
  Done when: a stub endpoint returning "model not found" makes preflight name the retired ID and print a suggested `models.json` change, without applying it.

- **Record each runner's automation terms and warn before parallel overnight work** — SECURITY — value 3 — effort S — risk med — category: runners
  Why: assumption: driving a subscription login through a CLI with parallel lanes unattended may exceed the plan's documented automated-use limits, and the user is about to scale that up ("full auto", "don't stop"). A small table per runner would hold the auth kind (subscription or API key), a link to the terms, and a last-checked date. The user, not Foreman, confirms the contents.
  Done when: dispatching more lanes than a runner's recorded limit, or unattended hours on a subscription login, prints a one-line warning naming the table row and the terms link.

- **Edit JSON, TOML and YAML by key without reformatting the file** — FEATURE — value 3 — effort M — risk low — category: edit safety
  Why: assumption: models rewriting `package.json`, `pyproject.toml` or workflow YAML lose key order, indentation and comments, which inflates diffs and trips the "non-functional churn" check. A stdlib line-patch verb, `set KEY=VALUE`, would keep the diff to one line.
  Done when: setting one key in a commented TOML and a 4-space JSON fixture changes exactly one line each, and an unsupported shape is refused with a reason.

- **Wild: dry-run the "anything" sampler on stranger-domain requests invented by a child** — FEATURE — value 3 — effort M — risk med — category: coverage
  Why: wild. The fixed kinds matrix only tests what we thought of. A tool-less child generates requests from domains the user has never tried, and the harness runs them on scratch fixtures. Failures are filed as "can't do X yet" briefs, so "work with anything" widens without the user naming each gap.
  Done when: one run produces at least 20 generated requests with fixtures, a pass/fail line each, and a brief filed for every failure, with no writes outside the scratch folder.
